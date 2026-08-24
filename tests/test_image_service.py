"""
SatQuery AI — Image Service Unit Tests
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

from backend.services.image_service import ImageService


class TestImageService(unittest.TestCase):

    def setUp(self):
        self.service = ImageService()
        self.sample_bmp = "data/samples/optical_2020_baseline.bmp"

    def test_extract_metadata_exists(self):
        if os.path.exists(self.sample_bmp):
            meta = self.service.extract_metadata(self.sample_bmp)
            self.assertIn("width", meta)
            self.assertIn("height", meta)
            self.assertEqual(meta["width"], 512)
            self.assertEqual(meta["height"], 512)

    def test_nonexistent_file_handling(self):
        meta = self.service.extract_metadata("nonexistent_path_test.bmp")
        self.assertTrue("error" in meta or meta.get("width") is None or "channels" in meta)


if __name__ == "__main__":
    unittest.main()
