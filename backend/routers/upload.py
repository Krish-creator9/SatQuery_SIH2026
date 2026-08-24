"""
SatQuery AI — Upload Router

Handles image upload, validation, and metadata extraction.
"""

import uuid
import shutil
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from backend.config import ALLOWED_EXTENSIONS, MAX_UPLOAD_SIZE_MB, UPLOAD_DIR
from backend.services.image_service import ImageService

router = APIRouter(prefix="/upload", tags=["Upload"])

image_service = ImageService()


@router.post("/")
async def upload_image(
    file: UploadFile = File(...),
    image_type: Optional[str] = Form(default="unknown"),
    role: Optional[str] = Form(default="primary"),
    session_id: Optional[str] = Form(default=None),
):
    """
    Upload a remote sensing image (GeoTIFF, TIFF, PNG, JPEG).

    Returns image metadata and a session-scoped image ID.
    """
    # Validate extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Generate session and image IDs
    if not session_id:
        session_id = str(uuid.uuid4())
    image_id = str(uuid.uuid4())

    # Create session directory
    session_dir = UPLOAD_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    # Save file
    save_path = session_dir / f"{image_id}{ext}"
    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Check file size
    file_size_mb = save_path.stat().st_size / (1024 * 1024)
    if file_size_mb > MAX_UPLOAD_SIZE_MB:
        save_path.unlink()
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({file_size_mb:.1f} MB). Maximum: {MAX_UPLOAD_SIZE_MB} MB",
        )

    # Extract metadata
    metadata = image_service.extract_metadata(str(save_path))

    # Generate preview
    preview_path = image_service.generate_preview(str(save_path), str(session_dir))

    return {
        "session_id": session_id,
        "image_id": image_id,
        "filename": file.filename,
        "image_type": image_type,
        "role": role,
        "file_size_mb": round(file_size_mb, 2),
        "metadata": metadata,
        "preview_path": preview_path,
    }


@router.get("/session/{session_id}")
async def get_session_images(session_id: str):
    """List all images in a session."""
    session_dir = UPLOAD_DIR / session_id
    if not session_dir.exists():
        raise HTTPException(status_code=404, detail="Session not found")

    images = []
    for f in session_dir.iterdir():
        if f.suffix.lower() in ALLOWED_EXTENSIONS:
            metadata = image_service.extract_metadata(str(f))
            images.append({
                "image_id": f.stem,
                "filename": f.name,
                "metadata": metadata,
            })

    return {"session_id": session_id, "images": images}
