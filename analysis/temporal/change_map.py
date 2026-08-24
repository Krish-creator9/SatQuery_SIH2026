"""
SatQuery AI — Temporal Change Map Analyzer

Generates false-color composite change maps (e.g. Red-Cyan) 
from two images without doing statistical differencing.
"""

import os
import uuid
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from PIL import Image

from analysis.base import BaseAnalyzer
from backend.schemas.evidence import AnalysisResult, EvidenceItem
from backend.config import OUTPUTS_DIR


class ChangeMapAnalyzer(BaseAnalyzer):
    """
    Creates visual change composites. E.g., Date 1 mapped to Red, Date 2 mapped to Green+Blue.
    Areas that are unchanged appear gray/white, while changes appear brightly colored (red or cyan).
    """

    @property
    def name(self) -> str:
        return "Change Map Composite Generator"

    @property
    def module_id(self) -> str:
        return "analysis.temporal.change_map"

    async def analyze(
        self,
        image_a_path: str,
        image_b_path: str,
        **kwargs,
    ) -> AnalysisResult:
        """
        Generate a false-color change composite.
        """
        try:
            with rasterio.open(image_a_path) as src_a, rasterio.open(image_b_path) as src_b:
                if src_a.width != src_b.width or src_a.height != src_b.height:
                    return self.make_skipped("Images are not aligned. Cannot create composite.")

                band_a = src_a.read(1).astype(np.float32)
                band_b = src_b.read(1).astype(np.float32)

                # Normalize bands to 0-255 for visualization
                norm_a = self._normalize(band_a)
                norm_b = self._normalize(band_b)
                
                # Create RGB: Red = Before (A), Green = After (B), Blue = After (B)
                # Unchanged = Red+Green+Blue = Gray/White
                # Present in A, lost in B = Red only (e.g. vegetation loss)
                # Absent in A, gained in B = Cyan only (Green+Blue) (e.g. new construction)
                rgb = np.stack([norm_a, norm_b, norm_b], axis=-1).astype(np.uint8)
                
                heatmap_filename = f"{uuid.uuid4()}_false_color_change.png"
                heatmap_path = OUTPUTS_DIR / heatmap_filename
                
                # Resize if it's too large to save space
                img = Image.fromarray(rgb, mode="RGB")
                img.thumbnail((1024, 1024))
                img.save(heatmap_path, "PNG")

                evidence = EvidenceItem(
                    source="temporal",
                    verdict="neutral",
                    detail="Visual change composite generated. Red areas indicate loss (present in earlier date), cyan areas indicate gain (present in later date).",
                    visual_asset=f"/static/outputs/{heatmap_filename}"
                )

                return self.make_success(
                    task="False-Color Change Composite",
                    result={"composite_type": "Red-Cyan (Date1-Date2)"},
                    confidence=0.9,
                    evidence=[evidence],
                    metadata={"image_a": os.path.basename(image_a_path), "image_b": os.path.basename(image_b_path)}
                )

        except Exception as e:
            return self.make_skipped(f"Failed to create change composite: {str(e)}")

    @staticmethod
    def _normalize(band: np.ndarray) -> np.ndarray:
        """Normalize a band to 0-255 for preview display."""
        valid = band[np.isfinite(band) & (band > 0)]
        if valid.size == 0:
            return np.zeros_like(band)

        p2, p98 = np.percentile(valid, [2, 98])
        if p98 - p2 == 0:
            return np.zeros_like(band)

        stretched = np.clip((band - p2) / (p98 - p2), 0, 1) * 255
        return stretched
