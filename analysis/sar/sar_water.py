"""
SatQuery AI — SAR Water Detection Analyzer

Uses thresholding on SAR backscatter to identify water bodies.
Water typically appears very dark in SAR (specular reflection).
"""

import os
import uuid
import numpy as np
import rasterio
import matplotlib.pyplot as plt

from analysis.base import BaseAnalyzer
from backend.schemas.evidence import AnalysisResult, EvidenceItem
from backend.config import OUTPUTS_DIR


class SARWaterAnalyzer(BaseAnalyzer):
    """
    Detects water bodies in SAR imagery using simple thresholding.
    """

    @property
    def name(self) -> str:
        return "SAR Water Detection"

    @property
    def module_id(self) -> str:
        return "analysis.sar.sar_water"

    async def analyze(
        self,
        image_path: str,
        threshold_db: float = -18.0,
        is_db: bool = False,
        **kwargs,
    ) -> AnalysisResult:
        """
        Identify water bodies.

        Args:
            image_path: Path to the SAR GeoTIFF.
            threshold_db: Threshold in decibels (dB) below which pixels are classified as water.
            is_db: Whether the input image is already in dB.
        """
        try:
            with rasterio.open(image_path) as src:
                if src.count < 1:
                    return self.make_skipped("SAR image has no bands.")

                band = src.read(1).astype(np.float32)

                valid_mask = (band != 0)
                if src.nodata is not None:
                    valid_mask &= (band != src.nodata)
                
                # Convert to dB if necessary
                if not is_db:
                    calc_arr = band.copy()
                    calc_arr[calc_arr <= 0] = 1e-10
                    db_band = 10 * np.log10(calc_arr)
                else:
                    db_band = band

                db_band[~valid_mask] = np.nan

                # Thresholding
                water_mask = (db_band < threshold_db)
                water_pixels = np.sum(water_mask & valid_mask)
                total_valid_pixels = np.sum(valid_mask)

                if total_valid_pixels == 0:
                    return self.make_skipped("No valid data pixels to analyze.")

                water_fraction = water_pixels / total_valid_pixels

                if water_fraction > 0.05: # > 5% of valid area is water
                    verdict = "supporting"
                    detail = f"Significant water bodies detected ({water_fraction:.1%} of area)."
                elif water_fraction > 0.005:
                    verdict = "neutral"
                    detail = f"Trace amounts of water or smooth surfaces detected ({water_fraction:.1%} of area)."
                else:
                    verdict = "opposing"
                    detail = "No significant water bodies detected."

                # Generate water map visualization
                heatmap_filename = f"{uuid.uuid4()}_sar_water_map.png"
                heatmap_path = OUTPUTS_DIR / heatmap_filename
                
                # Create a blue overlay for water
                vis_arr = np.zeros_like(db_band)
                vis_arr[water_mask & valid_mask] = 1
                vis_arr[~valid_mask] = np.nan
                
                plt.figure(figsize=(6, 6))
                plt.imshow(db_band, cmap="gray", vmin=-25, vmax=0, alpha=0.8) # Background
                plt.imshow(vis_arr, cmap="Blues", vmin=0, vmax=1, alpha=0.6) # Water overlay
                plt.axis("off")
                plt.title(f"SAR Water Detection (Thresh: {threshold_db} dB)")
                plt.savefig(heatmap_path, bbox_inches="tight", dpi=150, transparent=True)
                plt.close()

                evidence = EvidenceItem(
                    source="sar",
                    verdict=verdict,
                    detail=detail,
                    visual_asset=f"/static/outputs/{heatmap_filename}"
                )

                result_data = {
                    "water_fraction": float(water_fraction),
                    "threshold_used_db": threshold_db
                }

                # SAR water detection is reasonably robust but can be confused by flat sand/tarmac
                return self.make_success(
                    task="SAR Water Detection",
                    result=result_data,
                    confidence=0.85,
                    evidence=[evidence],
                    metadata={"image": os.path.basename(image_path)}
                )

        except Exception as e:
            return self.make_skipped(f"Failed to run SAR water detection: {str(e)}")
