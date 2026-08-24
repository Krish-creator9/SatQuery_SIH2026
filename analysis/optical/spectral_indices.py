"""
SatQuery AI — Spectral Indices Analyzer

Calculates standard optical indices (NDVI, NDWI) from multi-band imagery
and generates heatmap visual evidence.
"""

import os
from typing import Any
import uuid

import numpy as np
import rasterio
from rasterio.errors import RasterioIOError
import matplotlib.pyplot as plt

from analysis.base import BaseAnalyzer
from backend.schemas.evidence import AnalysisResult, EvidenceItem
from backend.config import OUTPUTS_DIR


class SpectralIndicesAnalyzer(BaseAnalyzer):
    """
    Computes spectral indices like NDVI (Vegetation) and NDWI (Water).
    Requires a GeoTIFF with NIR and Red/Green bands.
    """

    @property
    def name(self) -> str:
        return "Spectral Indices Analyzer"

    @property
    def module_id(self) -> str:
        return "analysis.optical.spectral_indices"

    async def analyze(
        self,
        image_path: str,
        index_type: str = "NDVI",
        nir_band: int = 8,  # Sentinel-2 B8 (NIR)
        red_band: int = 4,  # Sentinel-2 B4 (Red)
        green_band: int = 3, # Sentinel-2 B3 (Green)
        **kwargs,
    ) -> AnalysisResult:
        """
        Calculate a spectral index.

        Args:
            image_path: Path to the GeoTIFF file.
            index_type: 'NDVI' or 'NDWI'.
            nir_band: 1-indexed band number for Near Infrared.
            red_band: 1-indexed band number for Red (used in NDVI).
            green_band: 1-indexed band number for Green (used in NDWI).
        """
        index_type = index_type.upper()
        if index_type not in ["NDVI", "NDWI"]:
            return self.make_skipped(f"Unsupported index type: {index_type}")

        try:
            with rasterio.open(image_path) as src:
                # Check if requested bands exist
                required_bands = [nir_band, red_band] if index_type == "NDVI" else [green_band, nir_band]
                if src.count < max(required_bands):
                    return self.make_skipped(
                        f"Image only has {src.count} bands. {index_type} requires bands {required_bands}."
                    )

                # Read bands as float32
                if index_type == "NDVI":
                    band1 = src.read(nir_band).astype(np.float32)
                    band2 = src.read(red_band).astype(np.float32)
                    colormap = "RdYlGn"
                    description = "Normalized Difference Vegetation Index (NDVI)"
                else: # NDWI
                    band1 = src.read(green_band).astype(np.float32)
                    band2 = src.read(nir_band).astype(np.float32)
                    colormap = "Blues"
                    description = "Normalized Difference Water Index (NDWI)"

                # Mask nodata or exactly zero values if they represent empty space
                # (Simple approach: if both bands are 0, consider it nodata)
                mask = (band1 == 0) & (band2 == 0)

                # Avoid division by zero
                denominator = (band1 + band2)
                denominator[denominator == 0] = 1e-10

                # Calculate index
                index_arr = (band1 - band2) / denominator
                index_arr[mask] = np.nan # Apply mask

                # Calculate statistics
                valid_pixels = index_arr[~np.isnan(index_arr)]
                if len(valid_pixels) == 0:
                    return self.make_skipped("No valid data pixels found to calculate index.")

                mean_val = float(np.mean(valid_pixels))
                min_val = float(np.min(valid_pixels))
                max_val = float(np.max(valid_pixels))
                
                # Determine verdict based on mean value
                if index_type == "NDVI":
                    if mean_val > 0.4:
                        verdict = "supporting"
                        detail = "High vegetation presence detected."
                    elif mean_val > 0.1:
                        verdict = "neutral"
                        detail = "Sparse or mixed vegetation detected."
                    else:
                        verdict = "opposing"
                        detail = "Very little to no vegetation detected."
                else: # NDWI
                    if mean_val > 0.1:
                        verdict = "supporting"
                        detail = "Water bodies detected."
                    else:
                        verdict = "opposing"
                        detail = "No significant water bodies detected."

                # Generate heatmap
                heatmap_filename = f"{uuid.uuid4()}_{index_type}_heatmap.png"
                heatmap_path = OUTPUTS_DIR / heatmap_filename
                
                # Save plot
                plt.figure(figsize=(6, 6))
                plt.imshow(index_arr, cmap=colormap, vmin=-1, vmax=1)
                plt.colorbar(label=index_type)
                plt.axis("off")
                plt.title(description)
                plt.savefig(heatmap_path, bbox_inches="tight", dpi=150)
                plt.close()

                # Build Evidence Item
                evidence = EvidenceItem(
                    source="optical",
                    verdict=verdict,
                    detail=detail,
                    visual_asset=f"/static/outputs/{heatmap_filename}"
                )

                result_data = {
                    "index_type": index_type,
                    "statistics": {
                        "mean": mean_val,
                        "min": min_val,
                        "max": max_val
                    }
                }

                # High confidence for basic optical math if we have valid data
                confidence = 0.9 if len(valid_pixels) > 1000 else 0.4

                return self.make_success(
                    task=f"Calculate {index_type}",
                    result=result_data,
                    confidence=confidence,
                    evidence=[evidence],
                    metadata={"image": os.path.basename(image_path), "bands_used": required_bands}
                )

        except RasterioIOError:
            return self.make_skipped(f"Failed to open image with rasterio: {image_path}")
        except Exception as e:
            raise e
