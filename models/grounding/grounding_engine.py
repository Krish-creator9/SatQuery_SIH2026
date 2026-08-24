"""
SatQuery AI — Grounding Engine (Mock)

A placeholder for a visual grounding model (e.g. Grounding DINO).
Conforms to the BaseAnalyzer interface.
"""

from typing import Any

from analysis.base import BaseAnalyzer
from backend.schemas.evidence import EvidenceItem


class GroundingEngine(BaseAnalyzer):
    """
    Mock Grounding Engine. In Phase 6, this returns a stub response.
    """

    @property
    def name(self) -> str:
        return "Visual Grounding (Mock)"

    @property
    def module_id(self) -> str:
        return "models.grounding.grounding_engine"

    async def analyze(self, **kwargs) -> Any:
        image_path = kwargs.get("image_path")
        target_features = kwargs.get("target_features", ["object"])

        if not image_path:
            return self.make_skipped("No image provided for grounding.")

        mock_boxes = [{"label": feature, "box": [10, 10, 50, 50], "score": 0.8} for feature in target_features]
        mock_detail = f"Found {len(mock_boxes)} bounding boxes for features: {target_features}."

        evidence = [
            EvidenceItem(
                source=self.module_id,
                verdict="supporting",
                detail=mock_detail,
                data={"boxes": mock_boxes}
            )
        ]

        return self.make_success(
            task=self.name,
            result={"boxes": mock_boxes},
            confidence=0.8,
            evidence=evidence,
            warnings=["This is a mock visual grounding response."]
        )
