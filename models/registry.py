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
        self._models: dict[str, BaseModelWrapper] = {}

    def register(self, role: str, model: BaseModelWrapper) -> None:
        """
        Register a model under a role name.

        Roles: "vqa", "captioning", "grounding", "classifier", etc.
        """
        self._models[role] = model
        logger.info(
            f"Registered model '{model.model_name}' for role '{role}' "
            f"(size: {model.model_size_mb:.0f} MB, GPU required: {model.requires_gpu})"
        )

    def get(self, role: str) -> Optional[BaseModelWrapper]:
        """Get a registered model by role. Returns None if not registered."""
        return self._models.get(role)

    def is_available(self, role: str) -> bool:
        """Check if a model is registered AND available on current hardware."""
        model = self._models.get(role)
        if model is None:
            return False
        try:
            return model.is_available()
        except Exception:
            return False

    def is_loaded(self, role: str) -> bool:
        """Check if a model is currently loaded in memory."""
        model = self._models.get(role)
        return model.is_loaded if model else False

    def list_models(self) -> list[dict]:
        """List all registered models with their status."""
        return [
            {
                "role": role,
                "model_name": model.model_name,
                "size_mb": model.model_size_mb,
                "requires_gpu": model.requires_gpu,
                "available": self.is_available(role),
                "loaded": model.is_loaded,
            }
            for role, model in self._models.items()
        ]

    def unload_all(self) -> None:
        """Unload all models to free memory."""
        for role, model in self._models.items():
            if model.is_loaded:
                model.unload()
                logger.info(f"Unloaded model for role '{role}'")


# Singleton instance
model_registry = ModelRegistry()
