"""
SatQuery AI — Results Router

Retrieve previously generated results, visual outputs, and execution traces.
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from backend.config import OUTPUTS_DIR

router = APIRouter(prefix="/results", tags=["Results"])


@router.get("/visual/{session_id}/{filename}")
async def get_visual_output(session_id: str, filename: str):
    """Serve a generated visual output file (change map, NDVI map, etc.)."""
    file_path = OUTPUTS_DIR / session_id / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Visual output not found")
    return FileResponse(str(file_path))


@router.get("/preview/{session_id}/{image_id}")
async def get_image_preview(session_id: str, image_id: str):
    """Serve the RGB preview of an uploaded image."""
    from backend.config import UPLOAD_DIR

    session_dir = UPLOAD_DIR / session_id
    if not session_dir.exists():
        raise HTTPException(status_code=404, detail="Session not found")

    # Look for preview file
    preview_path = session_dir / f"{image_id}_preview.png"
    if not preview_path.exists():
        raise HTTPException(status_code=404, detail="Preview not found")

    return FileResponse(str(preview_path))
