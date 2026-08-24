"""
SatQuery AI — SAR Water Detection Analyzer

Uses thresholding on SAR backscatter to identify water bodies.
Water typically appears very dark in SAR (specular reflection).
"""

from __future__ import annotations

import os
from typing import Any
import numpy as np

from analysis.base import BaseAnalyzer
from backend.schemas.evidence import AnalysisResult, EvidenceItem
from backend.config import OUTPUTS_DIR


class SARWaterAnalyzer(BaseAnalyzer):
    """
    Detects water bodies in SAR imagery using backscatter thresholding.
    Supports GeoTIFF (Sentinel-1) and standard radar images.
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
        try:
            has_rasterio = False
            try:
                import rasterio
                has_rasterio = True
            except ImportError:
                has_rasterio = False

            if has_rasterio:
                try:
                    with rasterio.open(image_path) as src:
                        if src.count >= 1:
                            band = src.read(1).astype(np.float32)
                            valid_mask = (band != 0)
                            if src.nodata is not None:
                                valid_mask &= (band != src.nodata)
                            if not is_db:
                                calc_arr = band.copy()
                                calc_arr[calc_arr <= 0] = 1e-6
                                db_arr = 10 * np.log10(calc_arr)
                            else:
                                db_arr = band
                        else:
                            has_rasterio = False
                except Exception:
                    has_rasterio = False

            if not has_rasterio:
                arr = self.load_image_array(image_path).astype(np.float32)
                if arr.ndim >= 3:
                    band = arr[:, :, 0]
                else:
                    band = arr
                valid_mask = np.ones_like(band, dtype=bool)
                # Map standard 0-255 grayscale values to approximate radar dB range (-30dB to 0dB)
                db_arr = (band / 255.0) * 30.0 - 30.0

            valid_db = db_arr[valid_mask]
            if valid_db.size == 0:
                return self.make_skipped("No valid pixels found in radar observation.")

            water_mask = (db_arr < threshold_db) & valid_mask
            water_pixels = int(np.sum(water_mask))
            total_valid_pixels = int(np.sum(valid_mask))
            water_fraction = float(water_pixels / total_valid_pixels)

            verdict = "supporting" if water_fraction > 0.03 else "neutral"
            detail = (
                f"SAR specular reflection identified water across {water_fraction * 100:.2f}% "
                f"of scene ({water_pixels} pixels below {threshold_db} dB threshold)."
            )

            evidence = [
                EvidenceItem(
                    source=self.module_id,
                    verdict=verdict,
                    detail=detail,
                    data={
                        "water_fraction": water_fraction,
                        "water_pixels": water_pixels,
                        "total_pixels": total_valid_pixels,
                        "threshold_db": threshold_db,
                    },
                )
            ]

            return self.make_success(
                task=self.name,
                result={
                    "water_fraction": water_fraction,
                    "water_pixels": water_pixels,
                    "threshold_applied_db": threshold_db,
                },
                confidence=0.88,
                evidence=evidence,
                metadata={"file": os.path.basename(image_path)},
            )

        except Exception as e:
            return self.make_failed(f"SAR water analysis error: {str(e)}")
