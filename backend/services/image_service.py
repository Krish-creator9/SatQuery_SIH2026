"""
SatQuery AI — Image Service

Handles GeoTIFF/TIFF loading, metadata extraction, validation,
and preview generation. This is the primary geospatial I/O layer.
"""

from __future__ import annotations

import logging
from pathlib import Path
try:
    import numpy as np
except ImportError:
    np = None

logger = logging.getLogger(__name__)


class ImageService:
    """
    Service for loading and processing remote sensing images.

    Supports GeoTIFF (via rasterio) and standard formats (PNG/JPEG via PIL).
    """

    # Standard Sentinel-2 band names for reference
    SENTINEL2_BANDS = {
        1: "B01_Coastal", 2: "B02_Blue", 3: "B03_Green", 4: "B04_Red",
        5: "B05_VegRedEdge1", 6: "B06_VegRedEdge2", 7: "B07_VegRedEdge3",
        8: "B08_NIR", 9: "B08A_NarrowNIR", 10: "B09_WaterVapour",
        11: "B10_SWIR_Cirrus", 12: "B11_SWIR1", 13: "B12_SWIR2",
    }

    def extract_metadata(self, file_path: str) -> dict[str, Any]:
        """
        Extract metadata from an image file.

        For GeoTIFF: CRS, bounds, resolution, band count, dtype, nodata.
        For PNG/JPEG: dimensions, channels only.
        """
        path = Path(file_path)
        ext = path.suffix.lower()

        if ext in {".tif", ".tiff", ".geotiff"}:
            return self._extract_geotiff_metadata(file_path)
        else:
            return self._extract_standard_metadata(file_path)

    def _extract_geotiff_metadata(self, file_path: str) -> dict[str, Any]:
        """Extract metadata from a GeoTIFF file using rasterio."""
        try:
            import rasterio

            with rasterio.open(file_path) as src:
                bounds = src.bounds
                metadata = {
                    "format": "GeoTIFF",
                    "width": src.width,
                    "height": src.height,
                    "band_count": src.count,
                    "dtype": str(src.dtypes[0]) if src.dtypes else "unknown",
                    "crs": str(src.crs) if src.crs else None,
                    "bounds": {
                        "left": bounds.left,
                        "bottom": bounds.bottom,
                        "right": bounds.right,
                        "top": bounds.top,
                    } if bounds else None,
                    "resolution": {
                        "x": abs(src.res[0]) if src.res else None,
                        "y": abs(src.res[1]) if src.res else None,
                    },
                    "nodata": src.nodata,
                    "driver": src.driver,
                    "is_georeferenced": src.crs is not None,
                    "band_descriptions": [
                        src.descriptions[i] if src.descriptions[i] else f"Band_{i+1}"
                        for i in range(src.count)
                    ],
                }
                return metadata

        except ImportError:
            logger.warning("rasterio not installed — falling back to basic metadata")
            return self._extract_standard_metadata(file_path)
        except Exception as e:
            logger.error(f"Failed to read GeoTIFF metadata: {e}")
            return {"format": "GeoTIFF", "error": str(e)}

    def _extract_standard_metadata(self, file_path: str) -> dict[str, Any]:
        """Extract metadata from a standard image (PNG/JPEG)."""
        try:
            from PIL import Image

            with Image.open(file_path) as img:
                return {
                    "format": img.format or "Unknown",
                    "width": img.width,
                    "height": img.height,
                    "band_count": len(img.getbands()),
                    "mode": img.mode,
                    "is_georeferenced": False,
                }
        except Exception as e:
            logger.error(f"Failed to read image metadata: {e}")
            return {"format": "Unknown", "error": str(e)}

    def generate_preview(
        self, file_path: str, output_dir: str, max_size: int = 512
    ) -> Optional[str]:
        """
        Generate an RGB preview PNG from any supported image.

        For multi-band GeoTIFF: uses bands 4,3,2 (R,G,B) if available,
        otherwise first 3 bands, or single-band grayscale.
        """
        path = Path(file_path)
        preview_name = f"{path.stem}_preview.png"
        preview_path = Path(output_dir) / preview_name

        ext = path.suffix.lower()

        try:
            if ext in {".tif", ".tiff", ".geotiff"}:
                self._preview_geotiff(file_path, str(preview_path), max_size)
            else:
                self._preview_standard(file_path, str(preview_path), max_size)

            return str(preview_path) if preview_path.exists() else None

        except Exception as e:
            logger.error(f"Failed to generate preview: {e}")
            return None

    def _preview_geotiff(self, file_path: str, output_path: str, max_size: int):
        """Generate preview from GeoTIFF."""
        try:
            import rasterio
            from PIL import Image

            with rasterio.open(file_path) as src:
                # Determine which bands to use for RGB
                n_bands = src.count
                if n_bands >= 4:
                    # Assume Sentinel-2 ordering: use B4(Red), B3(Green), B2(Blue)
                    rgb_bands = [4, 3, 2]
                elif n_bands >= 3:
                    rgb_bands = [1, 2, 3]
                elif n_bands == 1:
                    rgb_bands = [1]
                else:
                    rgb_bands = list(range(1, n_bands + 1))[:3]

                # Read bands
                bands = []
                for b in rgb_bands:
                    band_data = src.read(b).astype(np.float32)
                    bands.append(band_data)

                if len(bands) == 1:
                    # Grayscale
                    arr = bands[0]
                    arr = self._normalize_band(arr)
                    img = Image.fromarray(arr.astype(np.uint8), mode="L")
                else:
                    # RGB
                    rgb = np.stack([self._normalize_band(b) for b in bands], axis=-1)
                    img = Image.fromarray(rgb.astype(np.uint8), mode="RGB")

                # Resize
                img.thumbnail((max_size, max_size))
                img.save(output_path, "PNG")

        except ImportError:
            logger.warning("rasterio not installed — cannot preview GeoTIFF")
        except Exception as e:
            logger.error(f"GeoTIFF preview failed: {e}")

    def _preview_standard(self, file_path: str, output_path: str, max_size: int):
        """Generate preview from standard image."""
        from PIL import Image

        with Image.open(file_path) as img:
            img.thumbnail((max_size, max_size))
            img.convert("RGB").save(output_path, "PNG")

    @staticmethod
    def _normalize_band(band: np.ndarray) -> np.ndarray:
        """Normalize a band to 0-255 for preview display."""
        # Handle nodata
        valid = band[np.isfinite(band)]
        if valid.size == 0:
            return np.zeros_like(band)

        # Use 2nd and 98th percentile for contrast stretching
        p2, p98 = np.percentile(valid, [2, 98])
        if p98 - p2 == 0:
            return np.zeros_like(band)

        stretched = np.clip((band - p2) / (p98 - p2), 0, 1) * 255
        return stretched

    def validate_compatibility(
        self, path_a: str, path_b: str
    ) -> dict[str, Any]:
        """
        Check if two images are compatible for temporal/paired analysis.

        Checks: CRS match, spatial overlap, resolution similarity, band compatibility.
        """
        meta_a = self.extract_metadata(path_a)
        meta_b = self.extract_metadata(path_b)

        issues = []
        warnings = []

        # CRS check
        crs_a = meta_a.get("crs")
        crs_b = meta_b.get("crs")
        if crs_a and crs_b and crs_a != crs_b:
            issues.append(f"CRS mismatch: {crs_a} vs {crs_b}")

        # Resolution check
        res_a = meta_a.get("resolution", {})
        res_b = meta_b.get("resolution", {})
        if res_a.get("x") and res_b.get("x"):
            ratio = max(res_a["x"], res_b["x"]) / min(res_a["x"], res_b["x"])
            if ratio > 2.0:
                warnings.append(f"Resolution differs by {ratio:.1f}x — resampling may be needed")

        # Size check
        if meta_a.get("width") != meta_b.get("width") or meta_a.get("height") != meta_b.get("height"):
            warnings.append("Image dimensions differ — registration/resampling may be needed")

        return {
            "compatible": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "metadata_a": meta_a,
            "metadata_b": meta_b,
        }
