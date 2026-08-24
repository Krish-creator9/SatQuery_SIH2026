"""
SatQuery AI — FastAPI Application Entry Point

An evidence-driven agentic remote-sensing assistant that dynamically
selects analyses required to answer natural-language queries, combines
optical, SAR and temporal evidence, and produces auditable results.

SIH 2026 — PS 26167 — ISRO
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import API_PREFIX, CORS_ORIGINS, OUTPUTS_DIR, UPLOAD_DIR

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)-30s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("satquery")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown."""
    logger.info("=" * 60)
    logger.info("  SatQuery AI — Starting up")
    logger.info("  SIH 2026 | PS 26167 | ISRO")
    logger.info("=" * 60)

    # Log feature status
    from backend.config import FEATURES
    enabled = [k for k, v in FEATURES.items() if v]
    disabled = [k for k, v in FEATURES.items() if not v]
    logger.info(f"  Enabled features:  {', '.join(enabled)}")
    logger.info(f"  Disabled features: {', '.join(disabled)}")
    logger.info("=" * 60)

    yield

    logger.info("SatQuery AI — Shutting down")


# Create FastAPI app
app = FastAPI(
    title="SatQuery AI",
    description=(
        "An Interactive Vision-Language Assistant for Multimodal "
        "Remote Sensing Image Analysis through Text Queries. "
        "Evidence-driven, agentic, and explainable."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving for outputs and previews
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static/outputs", StaticFiles(directory=str(OUTPUTS_DIR)), name="outputs")


# === Register Routers ===
from backend.routers import upload, query, results, scenarios

app.include_router(upload.router, prefix=API_PREFIX)
app.include_router(query.router, prefix=API_PREFIX)
app.include_router(results.router, prefix=API_PREFIX)
app.include_router(scenarios.router, prefix=API_PREFIX)


# === Root Endpoints ===

@app.get("/")
async def root():
    """Root endpoint — basic info."""
    return {
        "name": "SatQuery AI",
        "version": "0.1.0",
        "description": "Evidence-driven remote-sensing analysis assistant",
        "phase": "Phase 1 — Skeleton",
        "api_docs": "/docs",
    }


@app.get(f"{API_PREFIX}/health")
async def health():
    """Health check endpoint."""
    from backend.config import FEATURES
    from models.registry import model_registry

    return {
        "status": "healthy",
        "phase": "Phase 1 — Skeleton",
        "features": {k: v for k, v in FEATURES.items()},
        "models": model_registry.list_models(),
    }


@app.get(f"{API_PREFIX}/status")
async def system_status():
    """Detailed system status including hardware and module availability."""
    import sys
    import platform

    return {
        "system": {
            "python_version": sys.version,
            "platform": platform.platform(),
            "machine": platform.machine(),
        },
        "modules": {
            "rasterio": _check_import("rasterio"),
            "opencv": _check_import("cv2"),
            "numpy": _check_import("numpy"),
            "scikit_learn": _check_import("sklearn"),
            "scikit_image": _check_import("skimage"),
            "torch": _check_import("torch"),
            "transformers": _check_import("transformers"),
        },
    }


def _check_import(module_name: str) -> dict:
    """Check if a Python module is importable and get its version."""
    try:
        mod = __import__(module_name)
        version = getattr(mod, "__version__", "unknown")
        return {"available": True, "version": version}
    except ImportError:
        return {"available": False, "version": None}
