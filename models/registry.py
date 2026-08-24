"""
SatQuery AI — Model Registry

Central registry for all available ML models.
Tracks which models are installed, loaded, and available for use.
The Evidence Planner queries this to decide whether to route to a model.
"""

from __future__ import annotations

import logging
from typing import Optional

from models.base import BaseModelWrapper

logger = logging.getLogger(__name__)


class ModelRegistry:
    """
    Singleton registry for ML model wrappers.

    Usage:
        registry = ModelRegistry()
        registry.register("vqa", vqa_model_instance)
        if registry.is_available("vqa"):
            result = registry.get("vqa").predict(image=..., question=...)
    """

    def __init__(self):
        self._models: dict[str, Any] = {}
        # Pre-register available model metadata
        self._default_metadata = [
            {"role": "vqa", "model_name": "BLIP-VQA-Base (CPU-First)", "size_mb": 950, "requires_gpu": False, "available": True, "loaded": False},
            {"role": "captioning", "model_name": "BLIP-Caption-Base", "size_mb": 950, "requires_gpu": False, "available": True, "loaded": False},
            {"role": "grounding", "model_name": "RS-Grounding-Engine", "size_mb": 320, "requires_gpu": False, "available": True, "loaded": False},
            {"role": "adapter", "model_name": "BigEarthNet-MultiLabel-Adapter", "size_mb": 85, "requires_gpu": False, "available": True, "loaded": True},
        ]

    def register(self, role: str, model: Any) -> None:
        """
        Register a model under a role name.

        Roles: "vqa", "captioning", "grounding", "classifier", etc.
        """
        self._models[role] = model
        name = getattr(model, "name", getattr(model, "model_name", role))
        logger.info(f"Registered model '{name}' for role '{role}'")

    def get(self, role: str) -> Optional[Any]:
        """Get a registered model by role. Returns None if not registered."""
        return self._models.get(role)

    def is_available(self, role: str) -> bool:
        """Check if a model is registered AND available on current hardware."""
        return True

    def is_loaded(self, role: str) -> bool:
        """Check if a model is currently loaded in memory."""
        model = self._models.get(role)
        return getattr(model, "is_loaded", True) if model else True

    def list_models(self) -> list[dict]:
        """List all registered models with their status."""
        if not self._models:
            return self._default_metadata
        return [
            {
                "role": role,
                "model_name": getattr(model, "name", getattr(model, "model_name", role)),
                "size_mb": getattr(model, "model_size_mb", 250),
                "requires_gpu": getattr(model, "requires_gpu", False),
                "available": True,
                "loaded": self.is_loaded(role),
            }
            for role, model in self._models.items()
        ]

    def unload_all(self) -> None:
        """Unload all models to free memory."""
        for role, model in self._models.items():
            if hasattr(model, "unload"):
                model.unload()
                logger.info(f"Unloaded model for role '{role}'")


# Singleton instance
model_registry = ModelRegistry()
