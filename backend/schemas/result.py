"""
SatQuery AI — Result Schemas

Final output structures returned to the frontend.
These combine evidence from all modules into a single response.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from .evidence import AnalysisResult


class ExecutionStep(BaseModel):
    """One step in the execution trace."""
    step_number: int
    module: str
    action: str
    status: str
    duration_ms: Optional[float] = None
    detail: str = ""


class FusedResult(BaseModel):
    """
    The final result returned to the user.

    Contains the answer, confidence, all evidence, visual outputs,
    execution trace, and any warnings or data-insufficiency notices.
    """
    result_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    query: str
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_summary: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Simplified evidence for display",
    )
    analysis_results: list[AnalysisResult] = Field(
        default_factory=list,
        description="Full analysis results from each module",
    )
    visual_outputs: list[dict[str, str]] = Field(
        default_factory=list,
        description="Paths and labels for generated visual evidence",
    )
    execution_trace: list[ExecutionStep] = Field(
        default_factory=list,
        description="Auditable trace of every processing step",
    )
    warnings: list[str] = Field(default_factory=list)
    insufficient_data: Optional[str] = Field(
        default=None,
        description="If evidence is insufficient, what additional data is needed",
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "query": "Has the built-up area increased?",
                "answer": "Built-up area has increased by approximately 12% between the two dates.",
                "confidence": 0.87,
                "evidence_summary": [
                    {"source": "optical", "verdict": "supporting", "detail": "Urban spectral signature increased"},
                    {"source": "temporal", "verdict": "strong", "detail": "12.3% area classified as new built-up"},
                ],
                "visual_outputs": [
                    {"label": "Change Map", "path": "outputs/session_123/change_map.png"},
                ],
                "execution_trace": [
                    {"step_number": 1, "module": "query_analyzer", "action": "parse_query", "status": "success", "duration_ms": 5},
                    {"step_number": 2, "module": "evidence_planner", "action": "plan", "status": "success", "duration_ms": 2},
                    {"step_number": 3, "module": "analysis.temporal", "action": "change_detection", "status": "success", "duration_ms": 1200},
                ],
                "warnings": [],
                "insufficient_data": None,
            }
        }


class SessionInfo(BaseModel):
    """Information about a user session."""
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    images: list[dict[str, Any]] = Field(default_factory=list)
    query_count: int = 0
