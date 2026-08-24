"""
SatQuery AI — Query Schemas

Pydantic models for incoming user queries and task specifications.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TaskType(str, Enum):
    """Recognized analysis task types."""
    VQA = "vqa"
    CAPTIONING = "captioning"
    GROUNDING = "grounding"
    CHANGE_DETECTION = "change_detection"
    VEGETATION_ANALYSIS = "vegetation_analysis"
    WATER_DETECTION = "water_detection"
    URBAN_ANALYSIS = "urban_analysis"
    SAR_ANALYSIS = "sar_analysis"
    OPTICAL_ANALYSIS = "optical_analysis"
    COMPARISON = "comparison"
    GENERAL = "general"


class ImageType(str, Enum):
    """Type of uploaded image."""
    OPTICAL = "optical"
    SAR = "sar"
    MULTISPECTRAL = "multispectral"
    UNKNOWN = "unknown"


class QueryRequest(BaseModel):
    """Incoming user query."""
    query: str = Field(..., min_length=1, max_length=2000, description="Natural language query")
    session_id: Optional[str] = Field(default=None, description="Session ID for image context")
    mode: Optional[str] = Field(default="change", description="Analysis mode: single, change, fusion, scenarios")


class ImageReference(BaseModel):
    """Reference to an uploaded image."""
    image_id: str
    filename: str
    image_type: ImageType = ImageType.UNKNOWN
    role: str = "primary"  # "primary", "secondary", "before", "after"


class ParsedQuery(BaseModel):
    """Output of the Query Analyzer — structured task specification."""
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    original_query: str
    task_type: TaskType
    requires_temporal: bool = False
    requires_sar: bool = False
    requires_optical: bool = True
    requires_vlm: bool = False
    keywords: list[str] = Field(default_factory=list)
    target_features: list[str] = Field(default_factory=list)
    images: list[ImageReference] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "original_query": "Has the built-up area increased?",
                "task_type": "change_detection",
                "requires_temporal": True,
                "requires_sar": False,
                "requires_optical": True,
                "requires_vlm": False,
                "keywords": ["built-up", "increased"],
                "target_features": ["urban", "construction"],
            }
        }
