"""
SatQuery AI — Query Analyzer & Evidence Planner Unit Tests
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

from planner.query_analyzer import QueryAnalyzer
from planner.evidence_planner import EvidencePlanner
from backend.schemas.query import TaskType


class TestPlanner(unittest.TestCase):

    def setUp(self):
        self.analyzer = QueryAnalyzer()
        self.planner = EvidencePlanner()

    def test_change_detection_intent(self):
        query = "Identify changes and new buildings constructed between 2020 and 2024."
        parsed = self.analyzer.parse(query)
        self.assertEqual(parsed.task_type, TaskType.CHANGE_DETECTION)
        self.assertTrue(parsed.requires_temporal)

        plan = self.planner.create_plan(parsed)
        module_ids = [p.module_id for p in plan]
        self.assertIn("analysis.temporal.registration", module_ids)
        self.assertIn("analysis.temporal.change_detection", module_ids)

    def test_water_detection_intent(self):
        query = "Where are the flooded regions and water extent increase?"
        parsed = self.analyzer.parse(query)
        self.assertEqual(parsed.task_type, TaskType.WATER_DETECTION)

        plan = self.planner.create_plan(parsed)
        module_ids = [p.module_id for p in plan]
        self.assertTrue(any("spectral_indices" in m or "sar_water" in m or "vqa" in m for m in module_ids))

    def test_vegetation_analysis_intent(self):
        query = "Which agricultural parcels show severe vegetation stress?"
        parsed = self.analyzer.parse(query)
        self.assertEqual(parsed.task_type, TaskType.VEGETATION_ANALYSIS)

        plan = self.planner.create_plan(parsed)
        module_ids = [p.module_id for p in plan]
        self.assertTrue(any("spectral_indices" in m for m in module_ids))


if __name__ == "__main__":
    unittest.main()
