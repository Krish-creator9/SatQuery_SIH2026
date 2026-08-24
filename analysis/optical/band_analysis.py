"""
SatQuery AI — Band Analysis

Extracts basic statistical information across spectral bands.
"""

import os
from typing import Any

import numpy as np
import rasterio

from analysis.base import BaseAnalyzer
from backend.schemas.evidence import AnalysisResult, EvidenceItem


class BandAnalyzer(BaseAnalyzer):
    """
    Computes basic statistics (mean, std, min, max) for each band in an image.
    Useful for identifying bright/dark images, cloud cover anomalies, or general radiometry.
    """

    @property
    def name(self) -> str:
        return "Band Statistics Analyzer"

    @property
    def module_id(self) -> str:
        return "analysis.optical.band_analysis"

    async def analyze(
        self,
        image_path: str,
        **kwargs,
    ) -> AnalysisResult:
        """
        Calculate statistics for all bands.

        Args:
            image_path: Path to the GeoTIFF file.
        """
        try:
            with rasterio.open(image_path) as src:
                band_stats = {}
                is_mostly_dark = True
                is_mostly_saturated = True
                
                # Check all bands
                for i in range(1, src.count + 1):
                    band_data = src.read(i)
                    
                    # Ignore nodata if possible
                    if src.nodata is not None:
                        valid_data = band_data[band_data != src.nodata]
                    else:
                        # Fallback: ignore exact 0 if it looks like a padded edge
                        valid_data = band_data[band_data > 0]
                        
                    if valid_data.size == 0:
                        band_stats[f"Band_{i}"] = {"mean": 0, "std": 0, "min": 0, "max": 0}
                        continue

                    mean_val = float(np.mean(valid_data))
                    max_val = float(np.max(valid_data))
                    
                    band_stats[f"Band_{i}"] = {
                        "mean": mean_val,
                        "std": float(np.std(valid_data)),
                        "min": float(np.min(valid_data)),
                        "max": max_val,
                    }
                    
                    # Heuristic for 16-bit optical images
                    if mean_val > 500:
                        is_mostly_dark = False
                    if max_val < 10000: # not close to 16-bit max
                        is_mostly_saturated = False

                verdict = "neutral"
                detail = "Normal radiometric profile."
                
                if is_mostly_dark:
                    verdict = "opposing"
                    detail = "Image is unusually dark. Might be night-time or have severe shadow/sensor issues."
                elif is_mostly_saturated:
                    verdict = "opposing"
                    detail = "Image is highly saturated. Might be mostly clouds, snow, or sensor artifact."

                evidence = EvidenceItem(
                    source="optical",
                    verdict=verdict,
                    detail=detail,
                )

                return self.make_success(
                    task="Band Statistics Extraction",
                    result={"band_statistics": band_stats},
                    confidence=0.8,
                    evidence=[evidence],
                    metadata={"image": os.path.basename(image_path), "band_count": src.count}
                )

        except Exception as e:
            return self.make_skipped(f"Failed to analyze bands: {str(e)}")
