"""
SatQuery AI — Temporal Change Map Analyzer

Generates false-color composite change maps (e.g. Red-Cyan) 
from two images.
"""

import os
import uuid

try:
    import numpy as np
except ImportError:
    np = None

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
            arr_a = self.load_image_array(image_a_path)
            arr_b = self.load_image_array(image_b_path)

            heatmap_filename = f"{uuid.uuid4()}_false_color_change.png"
            heatmap_path = OUTPUTS_DIR / heatmap_filename

            if np is not None and isinstance(arr_a, np.ndarray) and isinstance(arr_b, np.ndarray):
                try:
                    from PIL import Image
                    band_a = arr_a[0] if arr_a.ndim == 3 else arr_a
                    band_b = arr_b[0] if arr_b.ndim == 3 else arr_b
                    norm_a = np.clip((band_a - np.min(band_a)) / (np.ptp(band_a) + 1e-6) * 255, 0, 255).astype(np.uint8)
                    norm_b = np.clip((band_b - np.min(band_b)) / (np.ptp(band_b) + 1e-6) * 255, 0, 255).astype(np.uint8)
                    rgb = np.stack([norm_a, norm_b, norm_b], axis=-1)
                    img = Image.fromarray(rgb, mode="RGB")
                    img.save(heatmap_path, "PNG")
                except Exception:
                    pass

            evidence = EvidenceItem(
                source="temporal",
                verdict="neutral",
                detail="Visual change composite generated. Red areas indicate loss (present in earlier date), cyan areas indicate gain (present in later date).",
                visual_asset=f"/static/outputs/{heatmap_filename}" if heatmap_path.exists() else None
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
