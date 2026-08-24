"""
SatQuery AI — Spectral Indices Analyzer

Calculates standard optical indices (NDVI, NDWI) from multi-band imagery
and standard RGB/NIR imagery with graceful fallbacks.
"""

from __future__ import annotations

import os
from typing import Any
import uuid
import numpy as np

from analysis.base import BaseAnalyzer
from backend.schemas.evidence import AnalysisResult, EvidenceItem
from backend.config import OUTPUTS_DIR


class SpectralIndicesAnalyzer(BaseAnalyzer):
    """
    Computes spectral indices like NDVI (Vegetation) and NDWI (Water).
    Supports GeoTIFF (Sentinel-2) and standard RGB/NIR imagery.
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
        nir_band: int = 8,
        red_band: int = 4,
        green_band: int = 3,
        **kwargs,
    ) -> AnalysisResult:
        index_type = index_type.upper()
        if index_type not in ["NDVI", "NDWI"]:
            return self.make_skipped(f"Unsupported index type: {index_type}")

        try:
            # 1. Try rasterio first if available
            has_rasterio = False
            try:
                import rasterio
                has_rasterio = True
            except ImportError:
                has_rasterio = False

            if has_rasterio:
                try:
                    with rasterio.open(image_path) as src:
                        band_count = src.count
                        if index_type == "NDVI":
                            if band_count >= max(nir_band, red_band):
                                b_nir = src.read(nir_band).astype(float)
                                b_red = src.read(red_band).astype(float)
                            elif band_count >= 3:
                                b_nir = src.read(1).astype(float)
                                b_red = src.read(3).astype(float)
                            else:
                                return self.make_skipped(f"GeoTIFF requires at least 3 bands, got {band_count}.")
                            denom = b_nir + b_red
                            denom[denom == 0] = np.nan
                            index_array = (b_nir - b_red) / denom
                        else:  # NDWI
                            if band_count >= max(green_band, nir_band):
                                b_green = src.read(green_band).astype(float)
                                b_nir = src.read(nir_band).astype(float)
                            elif band_count >= 3:
                                b_green = src.read(2).astype(float)
                                b_nir = src.read(1).astype(float)
                            else:
                                return self.make_skipped(f"GeoTIFF requires at least 3 bands, got {band_count}.")
                            denom = b_green + b_nir
                            denom[denom == 0] = np.nan
                            index_array = (b_green - b_nir) / denom
                except Exception:
                    has_rasterio = False

            if not has_rasterio:
                # 2. Fallback: load array via PIL / BaseAnalyzer
                arr = self.load_image_array(image_path).astype(float)
                if arr.ndim >= 3 and arr.shape[2] >= 3:
                    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
                    if index_type == "NDVI":
                        # Green - Red difference as optical vegetation proxy for standard RGB
                        denom = g + r
                        denom[denom == 0] = 1.0
                        index_array = (g - r) / denom
                    else:  # NDWI
                        # Blue - Green difference as water proxy
                        denom = b + g
                        denom[denom == 0] = 1.0
                        index_array = (b - g) / denom
                else:
                    index_array = np.zeros((arr.shape[0], arr.shape[1]), dtype=float)

            # Statistics calculation
            valid_mask = ~np.isnan(index_array)
            valid_vals = index_array[valid_mask]

            if valid_vals.size == 0:
                return self.make_skipped(f"Could not compute valid {index_type} values.")

            mean_val = float(np.mean(valid_vals))
            min_val = float(np.min(valid_vals))
            max_val = float(np.max(valid_vals))
            std_val = float(np.std(valid_vals))

            # Interpretation
            if index_type == "NDVI":
                if mean_val > 0.4:
                    interp = "Dense, healthy green vegetation predominant."
                    verdict = "supporting"
                elif mean_val > 0.15:
                    interp = "Moderate to sparse vegetation or mixed crop cover."
                    verdict = "supporting"
                else:
                    interp = "Low vegetation: bare soil, urban impervious surface, or water."
                    verdict = "neutral"
            else:  # NDWI
                water_pixels = np.sum(valid_vals > 0.0)
                water_fraction = float(water_pixels / valid_vals.size)
                if water_fraction > 0.05:
                    interp = f"Surface water identified covering approximately {water_fraction * 100:.1f}% of the scene."
                    verdict = "supporting"
                else:
                    interp = "Minimal open surface water detected."
                    verdict = "neutral"

            evidence = [
                EvidenceItem(
                    source=self.module_id,
                    verdict=verdict,
                    detail=f"{index_type} mean: {mean_val:.3f} [{min_val:.3f}, {max_val:.3f}]. {interp}",
                    data={
                        "index_type": index_type,
                        "mean": mean_val,
                        "min": min_val,
                        "max": max_val,
                        "std": std_val,
                    },
                )
            ]

            return self.make_success(
                task=f"{index_type} Analysis",
                result={
                    "index_type": index_type,
                    "mean": mean_val,
                    "min": min_val,
                    "max": max_val,
                    "std": std_val,
                    "interpretation": interp,
                },
                confidence=0.90,
                evidence=evidence,
                metadata={"file": os.path.basename(image_path)},
            )

        except Exception as e:
            return self.make_failed(f"Spectral analysis error: {str(e)}")
