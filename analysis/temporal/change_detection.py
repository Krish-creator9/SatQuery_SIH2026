"""
SatQuery AI — Temporal Change Detection Analyzer

Performs pixel-level image differencing to detect changes over time.
Requires two co-registered images.
"""

import os
import uuid
import numpy as np
import rasterio
import matplotlib.pyplot as plt

from analysis.base import BaseAnalyzer
from backend.schemas.evidence import AnalysisResult, EvidenceItem
from backend.config import OUTPUTS_DIR


class ChangeDetectionAnalyzer(BaseAnalyzer):
    """
    Calculates absolute difference between two aligned images to find areas of change.
    """

    @property
    def name(self) -> str:
        return "Change Detection Analyzer"

    @property
    def module_id(self) -> str:
        return "analysis.temporal.change_detection"

    async def analyze(
        self,
        image_a_path: str,
        image_b_path: str,
        threshold_std: float = 2.0,
        **kwargs,
    ) -> AnalysisResult:
        """
        Perform differencing between image A (before) and image B (after).
        Assumes registration has already been verified.
        
        Args:
            threshold_std: Number of standard deviations above the mean difference
                           to classify a pixel as "changed".
        """
        try:
            with rasterio.open(image_a_path) as src_a, rasterio.open(image_b_path) as src_b:
                if src_a.count < 1 or src_b.count < 1:
                    return self.make_skipped("Images must have at least one band.")
                if src_a.width != src_b.width or src_a.height != src_b.height:
                    return self.make_skipped("Images are not aligned. Registration failed.")

                # Read first band of both (could be extended to multi-band PCA or CVA)
                band_a = src_a.read(1).astype(np.float32)
                band_b = src_b.read(1).astype(np.float32)

                # Mask nodata
                mask_a = (band_a != 0)
                if src_a.nodata is not None:
                    mask_a &= (band_a != src_a.nodata)
                    
                mask_b = (band_b != 0)
                if src_b.nodata is not None:
                    mask_b &= (band_b != src_b.nodata)
                    
                valid_mask = mask_a & mask_b
                
                # Difference image (Absolute change magnitude)
                diff = np.abs(band_b - band_a)
                valid_diff = diff[valid_mask]
                
                if len(valid_diff) == 0:
                    return self.make_skipped("No overlapping valid pixels found.")

                mean_diff = float(np.mean(valid_diff))
                std_diff = float(np.std(valid_diff))
                
                # Thresholding
                threshold_val = mean_diff + (threshold_std * std_diff)
                change_mask = (diff > threshold_val) & valid_mask
                
                changed_pixels = np.sum(change_mask)
                total_valid = np.sum(valid_mask)
                change_fraction = changed_pixels / total_valid

                # Verdict
                if change_fraction > 0.1:
                    verdict = "supporting"
                    detail = f"Significant change detected ({change_fraction:.1%} of area)."
                elif change_fraction > 0.01:
                    verdict = "neutral"
                    detail = f"Minor or localized change detected ({change_fraction:.1%} of area)."
                else:
                    verdict = "opposing"
                    detail = "No significant change detected between the two dates."

                # Visualization (Change Map)
                heatmap_filename = f"{uuid.uuid4()}_change_map.png"
                heatmap_path = OUTPUTS_DIR / heatmap_filename
                
                # Display band B as background, and change mask as red overlay
                bg_vis = band_b.copy()
                bg_vis[~valid_mask] = np.nan
                # Simple contrast stretch for background
                p2, p98 = np.nanpercentile(bg_vis, [2, 98])
                
                change_overlay = np.zeros_like(diff)
                change_overlay[change_mask] = 1
                change_overlay[~change_mask] = np.nan
                
                plt.figure(figsize=(6, 6))
                plt.imshow(bg_vis, cmap="gray", vmin=p2, vmax=p98)
                plt.imshow(change_overlay, cmap="Reds", vmin=0, vmax=1, alpha=0.6)
                plt.axis("off")
                plt.title(f"Detected Changes (> {threshold_std} Std Dev)")
                plt.savefig(heatmap_path, bbox_inches="tight", dpi=150, transparent=True)
                plt.close()

                evidence = EvidenceItem(
                    source="temporal",
                    verdict=verdict,
                    detail=detail,
                    visual_asset=f"/static/outputs/{heatmap_filename}"
                )

                result_data = {
                    "change_fraction": float(change_fraction),
                    "threshold_applied": threshold_val,
                    "statistics": {
                        "mean_abs_difference": mean_diff,
                        "std_difference": std_diff
                    }
                }

                return self.make_success(
                    task="Temporal Change Detection",
                    result=result_data,
                    confidence=0.8,
                    evidence=[evidence],
                    metadata={"image_a": os.path.basename(image_a_path), "image_b": os.path.basename(image_b_path)}
                )

        except Exception as e:
            return self.make_skipped(f"Failed to detect changes: {str(e)}")
