"""
SatQuery AI — Evidence Schemas

The standard evidence structure returned by every analysis module.
This is the contract that makes the Evidence Fusion module work
without knowing the internals of each analyzer.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class EvidenceType(str, Enum):
    """Types of evidence an analysis module can produce."""
    NUMERIC = "numeric"
    CATEGORICAL = "categorical"
    SPATIAL = "spatial"          # Region/area-based evidence
    VISUAL = "visual"           # Generated image/map
    TEXTUAL = "textual"         # Text description
    CLASSIFICATION = "classification"


class EvidenceItem(BaseModel):
    """A single piece of evidence."""
    type: EvidenceType = Field(default=EvidenceType.TEXTUAL)
    name: str = Field(default="Evidence Item")
    value: Any = None
    interpretation: str = ""
    path: Optional[str] = None  # Path to visual evidence file
    source: Optional[str] = None
    verdict: Optional[str] = None
    detail: Optional[str] = None
    data: Optional[dict[str, Any]] = None
    visual_asset: Optional[str] = None


class AnalysisStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"         # Some evidence produced, with caveats
    FAILED = "failed"
    SKIPPED = "skipped"         # Module not needed for this query
    UNAVAILABLE = "unavailable" # Module not installed / feature disabled


class AnalysisResult(BaseModel):
    """
    Standard output from any analysis module.

    Every analyzer — optical, SAR, temporal, VLM — must return this structure.
    The Evidence Fusion module combines these without knowing their internals.
    """
    task: str = Field(..., description="What analysis was performed")
    module: str = Field(..., description="Fully qualified module name")
    status: AnalysisStatus = AnalysisStatus.SUCCESS
    result: dict[str, Any] = Field(default_factory=dict, description="Analysis-specific results")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Module-level confidence")
    evidence: list[EvidenceItem] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Input CRS, bands used, processing time, etc."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "task": "ndvi_analysis",
                "module": "analysis.optical.spectral_indices",
                "status": "success",
                "result": {
                    "mean_ndvi": 0.42,
                    "vegetation_coverage_pct": 67.3,
                    "summary": "Moderate vegetation across 67% of the image",
                },
                "confidence": 0.85,
                "evidence": [
                    {
                        "type": "numeric",
                        "name": "mean_ndvi",
                        "value": 0.42,
                        "interpretation": "Moderate vegetation",
                    },
                    {
                        "type": "visual",
                        "name": "ndvi_map",
                        "value": None,
                        "interpretation": "NDVI heatmap",
                        "path": "outputs/session_123/ndvi_map.png",
                    },
                ],
                "warnings": [],
                "metadata": {
                    "input_bands": ["B4", "B8"],
                    "processing_time_ms": 230,
                },
            }
        }
