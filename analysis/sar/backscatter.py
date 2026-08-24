"""
SatQuery AI — SAR Backscatter Analyzer

Analyzes Synthetic Aperture Radar (SAR) backscatter intensity.
Useful for detecting urban areas, rough terrain, or ships.
"""

import os
import uuid
import numpy as np
import rasterio
from rasterio.errors import RasterioIOError
import matplotlib.pyplot as plt

from analysis.base import BaseAnalyzer
from backend.schemas.evidence import AnalysisResult, EvidenceItem
from backend.config import OUTPUTS_DIR


class BackscatterAnalyzer(BaseAnalyzer):
    """
    Computes basic SAR backscatter statistics.
    Assumes input is already preprocessed (e.g., GRD, calibrated to sigma-nought or dB).
    """

    @property
    def name(self) -> str:
        return "SAR Backscatter Analyzer"

    @property
    def module_id(self) -> str:
        return "analysis.sar.backscatter"

    async def analyze(
        self,
        image_path: str,
        is_db: bool = False,
        **kwargs,
    ) -> AnalysisResult:
        """
        Analyze SAR backscatter.

        Args:
            image_path: Path to the SAR GeoTIFF.
            is_db: Whether the image is already in Decibels (dB). If False, 
                   assumes linear scale and optionally converts for visualization.
        """
        try:
            with rasterio.open(image_path) as src:
                # Typically, SAR images might have VV, VH, HH, or HV bands.
                # We'll just analyze the first available band for this base analyzer.
                if src.count < 1:
                    return self.make_skipped("SAR image has no bands.")

                band = src.read(1).astype(np.float32)

                # Mask nodata or exact zero
                valid_mask = (band != 0)
                if src.nodata is not None:
                    valid_mask &= (band != src.nodata)
                
                valid_pixels = band[valid_mask]
                
                if len(valid_pixels) == 0:
                    return self.make_skipped("No valid data pixels found in SAR image.")

                mean_val = float(np.mean(valid_pixels))
                max_val = float(np.max(valid_pixels))
                std_val = float(np.std(valid_pixels))

                # Heuristics based on whether data is in dB or linear
                verdict = "neutral"
                detail = "Moderate backscatter."
                
                if is_db:
                    # Typical dB ranges: Water: -20 to -30, Urban: 0 to +10, Veg: -15 to -5
                    if mean_val > -5:
                        verdict = "supporting"
                        detail = "High backscatter detected. Likely urban/built-up areas, rough terrain, or double-bounce targets."
                    elif mean_val < -18:
                        verdict = "opposing"
                        detail = "Low backscatter detected. Likely flat surfaces like calm water or bare soil."
                else:
                    # Linear scale heuristics
                    if mean_val > 0.3:
                        verdict = "supporting"
                        detail = "High backscatter detected. High structural complexity."
                    elif mean_val < 0.05:
                        verdict = "opposing"
                        detail = "Low backscatter detected. Smooth surfaces."

                # Generate a visualization (convert to dB if not already for better viewing)
                vis_arr = band.copy()
                if not is_db:
                    # Avoid log(0)
                    vis_arr[vis_arr <= 0] = 1e-10
                    vis_arr = 10 * np.log10(vis_arr)
                    vis_arr[~valid_mask] = np.nan
                
                heatmap_filename = f"{uuid.uuid4()}_sar_backscatter.png"
                heatmap_path = OUTPUTS_DIR / heatmap_filename
                
                plt.figure(figsize=(6, 6))
                # Grayscale for SAR is standard
                plt.imshow(vis_arr, cmap="gray", vmin=np.nanpercentile(vis_arr, 2), vmax=np.nanpercentile(vis_arr, 98))
                plt.colorbar(label="Backscatter (dB)")
                plt.axis("off")
                plt.title("SAR Backscatter Intensity")
                plt.savefig(heatmap_path, bbox_inches="tight", dpi=150)
                plt.close()

                evidence = EvidenceItem(
                    source="sar",
                    verdict=verdict,
                    detail=detail,
                    visual_asset=f"/static/outputs/{heatmap_filename}"
                )

                result_data = {
                    "statistics": {
                        "mean": mean_val,
                        "max": max_val,
                        "std": std_val
                    },
                    "scale": "dB" if is_db else "linear"
                }

                return self.make_success(
                    task="SAR Backscatter Analysis",
                    result=result_data,
                    confidence=0.8,
                    evidence=[evidence],
                    metadata={"image": os.path.basename(image_path), "bands_analyzed": 1}
                )

        except RasterioIOError:
            return self.make_skipped(f"Failed to open SAR image: {image_path}")
        except Exception as e:
            raise e
