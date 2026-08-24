"""
SatQuery AI — Application Configuration

Central configuration with feature flags for enabling/disabling
modules based on hardware availability and development phase.
"""

import os
from pathlib import Path


# === Paths ===
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SAMPLES_DIR = DATA_DIR / "samples"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
MODELS_DIR = PROJECT_ROOT / "models"

# Ensure directories exist
for _dir in [DATA_DIR, SAMPLES_DIR, OUTPUTS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

# === Upload Settings ===
UPLOAD_DIR = DATA_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_UPLOAD_SIZE_MB = 500  # Max file size in MB
ALLOWED_EXTENSIONS = {".tif", ".tiff", ".geotiff", ".png", ".jpg", ".jpeg"}

# === API Settings ===
API_HOST = os.getenv("SATQUERY_HOST", "0.0.0.0")
API_PORT = int(os.getenv("SATQUERY_PORT", "8000"))
API_PREFIX = "/api"
CORS_ORIGINS = [
    "http://localhost:5173",   # Vite dev server
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

# === Feature Flags ===
# These control which modules are active.
# Disable heavy modules until their phase is reached and hardware is verified.

FEATURES = {
    # Tier 1 — Always available (Phase 1-10)
    "image_upload": True,
    "geotiff_validation": True,
    "optical_analysis": True,       # NDVI, NDWI, band stats
    "sar_analysis": True,           # Backscatter, texture, water
    "temporal_analysis": True,      # Registration, change detection
    "query_analyzer": True,         # Rule-based query parsing
    "evidence_planner": True,       # Task → analysis plan
    "evidence_fusion": True,        # Multi-source evidence combination
    "confidence_estimation": True,  # Weighted confidence

    # Tier 2 — ML Models (Phase 11+, require PyTorch)
    "vlm_vqa": True,                # BLIP VQA
    "vlm_captioning": True,         # BLIP Captioning
    "vlm_grounding": True,          # Text-guided region grounding

    # Tier 3 — Adaptation (Phase 12, requires training)
    "bigearth_classifier": False,   # ResNet-18 on BigEarthNet
}


def is_feature_enabled(feature_name: str) -> bool:
    """Check if a feature is enabled."""
    return FEATURES.get(feature_name, False)


# === Session Settings ===
SESSION_TIMEOUT_MINUTES = 60
MAX_SESSIONS = 50
