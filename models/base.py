"""
SatQuery AI — Base Model Interface

Abstract base class for all ML model wrappers.
Every model module (VQA, captioning, classification) must extend this.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseModelWrapper(ABC):
    """
    Abstract base for all ML model wrappers in SatQuery.

    Subclasses must implement:
        - model_name: identifier
        - is_available(): check if the model can be loaded
        - load(): load the model into memory
        - predict(): run inference
        - unload(): free memory
    """

    _loaded: bool = False

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Unique model identifier."""
        ...

    @property
    @abstractmethod
    def model_size_mb(self) -> float:
        """Approximate model size in MB (for display/logging)."""
        ...

    @property
    @abstractmethod
    def requires_gpu(self) -> bool:
        """Whether this model requires a GPU for practical use."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if this model can be loaded on current hardware.

        Should verify:
        - Dependencies installed (torch, transformers, etc.)
        - Sufficient RAM/VRAM
        - Model weights accessible (downloaded or downloadable)
        """
        ...

    @abstractmethod
    def load(self) -> None:
        """Load model weights into memory."""
        ...

    @abstractmethod
    def predict(self, **kwargs) -> dict[str, Any]:
        """
        Run inference.

        Returns a dict with at minimum:
        - "result": the prediction
        - "confidence": float 0-1
        """
        ...

    def unload(self) -> None:
        """Free model from memory. Override if special cleanup is needed."""
        self._loaded = False

    @property
    def is_loaded(self) -> bool:
        return self._loaded
