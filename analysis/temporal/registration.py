"""
SatQuery AI — Temporal Registration Analyzer

Checks registration/alignment between two images from different times.
This is a prerequisite for change detection.
"""

import os
from typing import Any

import rasterio

from analysis.base import BaseAnalyzer
from backend.schemas.evidence import AnalysisResult, EvidenceItem


class RegistrationAnalyzer(BaseAnalyzer):
    """
    Checks if two images are spatially aligned.
    Change detection requires perfect or near-perfect alignment.
    """

    @property
    def name(self) -> str:
        return "Image Registration Checker"

    @property
    def module_id(self) -> str:
        return "analysis.temporal.registration"

    async def analyze(
        self,
        image_a_path: str,
        image_b_path: str,
        **kwargs,
    ) -> AnalysisResult:
        """
        Check alignment between image A (before) and image B (after).
        """
        try:
            with rasterio.open(image_a_path) as src_a, rasterio.open(image_b_path) as src_b:
                
                # Check dimensions
                dim_match = (src_a.width == src_b.width) and (src_a.height == src_b.height)
                
                # Check bounds
                bounds_match = False
                if src_a.bounds and src_b.bounds:
                    # Allow very small floating point differences
                    bounds_match = (
                        abs(src_a.bounds.left - src_b.bounds.left) < 1e-4 and
                        abs(src_a.bounds.right - src_b.bounds.right) < 1e-4 and
                        abs(src_a.bounds.bottom - src_b.bounds.bottom) < 1e-4 and
                        abs(src_a.bounds.top - src_b.bounds.top) < 1e-4
                    )

                # Check CRS
                crs_match = (src_a.crs == src_b.crs) if (src_a.crs and src_b.crs) else False

                aligned = dim_match and bounds_match and crs_match

                if aligned:
                    verdict = "supporting"
                    detail = "Images are perfectly aligned and suitable for pixel-level change detection."
                elif not dim_match:
                    verdict = "opposing"
                    detail = f"Dimension mismatch: {src_a.width}x{src_a.height} vs {src_b.width}x{src_b.height}."
                elif not bounds_match:
                    verdict = "opposing"
                    detail = "Spatial bounds do not match. Images cover different areas."
                else:
                    verdict = "opposing"
                    detail = "Coordinate Reference Systems (CRS) do not match."

                evidence = EvidenceItem(
                    source="temporal",
                    verdict=verdict,
                    detail=detail
                )

                return self.make_success(
                    task="Registration Check",
                    result={
                        "is_aligned": aligned,
                        "checks": {
                            "dimensions_match": dim_match,
                            "bounds_match": bounds_match,
                            "crs_match": crs_match
                        }
                    },
                    confidence=1.0,
                    evidence=[evidence],
                    metadata={"image_a": os.path.basename(image_a_path), "image_b": os.path.basename(image_b_path)}
                )

        except Exception as e:
            return self.make_skipped(f"Failed to check registration: {str(e)}")
