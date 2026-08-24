"""
SatQuery AI — Evidence Fusion Engine Unit Tests
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

from fusion.evidence_fusion import EvidenceFusionEngine
from backend.schemas.evidence import AnalysisResult, AnalysisStatus, EvidenceItem


class TestEvidenceFusion(unittest.TestCase):

    def setUp(self):
        self.fuser = EvidenceFusionEngine()

    def test_empty_results_handling(self):
        result = self.fuser.fuse("Is there change?", [])
        self.assertEqual(result.confidence, 0.0)
        self.assertIsNotNone(result.insufficient_data)

    def test_supporting_evidence_fusion(self):
        ev1 = EvidenceItem(type="textual", name="Change Ev", verdict="supporting", detail="12% expansion")
        res1 = AnalysisResult(
            task="Change Detection",
            module="analysis.temporal.change_detection",
            status=AnalysisStatus.SUCCESS,
            result={"change_fraction": 0.12},
            confidence=0.90,
            evidence=[ev1]
        )

        result = self.fuser.fuse("Has built-up area increased?", [res1])
        self.assertGreaterEqual(result.confidence, 0.85)
        self.assertIn("expansion", result.answer.lower())
        self.assertEqual(len(result.evidence_summary), 1)


if __name__ == "__main__":
    unittest.main()
