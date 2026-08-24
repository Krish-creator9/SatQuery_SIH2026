"""
SatQuery AI — Base Analyzer

Abstract base class for all analysis modules.
Every analyzer (optical, SAR, temporal) must extend this class
and implement the `analyze` method.
"""

from __future__ import annotations

import time
import logging
from abc import ABC, abstractmethod
from typing import Any

from backend.schemas.evidence import AnalysisResult, AnalysisStatus, EvidenceItem

logger = logging.getLogger(__name__)


class BaseAnalyzer(ABC):
    """
    Abstract base for all SatQuery analysis modules.

    Subclasses must implement:
        - name: human-readable module name
        - module_id: fully qualified identifier (e.g., "analysis.optical.spectral_indices")
        - analyze(): perform the analysis and return AnalysisResult

    The base class provides:
        - Timing wrapper
        - Standard error handling
        - Result construction helpers
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name for this analyzer."""
        ...

    @property
    @abstractmethod
    def module_id(self) -> str:
        """Fully qualified module identifier."""
        ...

    @abstractmethod
    async def analyze(self, **kwargs) -> AnalysisResult:
        """
        Perform analysis and return a standardized AnalysisResult.

        Subclasses receive keyword arguments relevant to their analysis type
        (e.g., image_path, band_indices, comparison_path, etc.)
        """
        ...

    async def safe_analyze(self, **kwargs) -> AnalysisResult:
        """
        Wrapper that catches exceptions and measures timing.

        Call this instead of analyze() directly.
        """
        start = time.time()
        try:
            result = await self.analyze(**kwargs)
            elapsed_ms = (time.time() - start) * 1000
            result.metadata["processing_time_ms"] = round(elapsed_ms, 1)
            return result
        except Exception as e:
            elapsed_ms = (time.time() - start) * 1000
            logger.error(f"[{self.module_id}] Analysis failed: {e}", exc_info=True)
            return AnalysisResult(
                task=self.name,
                module=self.module_id,
                status=AnalysisStatus.FAILED,
                result={"error": str(e)},
                confidence=0.0,
                evidence=[],
                warnings=[f"Analysis failed: {str(e)}"],
                metadata={"processing_time_ms": round(elapsed_ms, 1)},
            )

    # === Helper methods for building results ===

    def make_success(
        self,
        task: str,
        result: dict[str, Any],
        confidence: float,
        evidence: list[EvidenceItem],
        warnings: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AnalysisResult:
        """Convenience method to build a successful AnalysisResult."""
        return AnalysisResult(
            task=task,
            module=self.module_id,
            status=AnalysisStatus.SUCCESS,
            result=result,
            confidence=confidence,
            evidence=evidence,
            warnings=warnings or [],
            metadata=metadata or {},
        )

    def make_skipped(self, reason: str) -> AnalysisResult:
        """Return a SKIPPED result when this analysis isn't needed."""
        return AnalysisResult(
            task=self.name,
            module=self.module_id,
            status=AnalysisStatus.SKIPPED,
            result={"reason": reason},
            confidence=0.0,
            evidence=[],
            warnings=[],
            metadata={},
        )

    def make_unavailable(self, reason: str) -> AnalysisResult:
        """Return an UNAVAILABLE result when this module isn't installed."""
        return AnalysisResult(
            task=self.name,
            module=self.module_id,
            status=AnalysisStatus.UNAVAILABLE,
            result={"reason": reason},
            confidence=0.0,
            evidence=[],
            warnings=[reason],
            metadata={},
        )
