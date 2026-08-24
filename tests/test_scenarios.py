"""
SatQuery AI — Scenario Service Unit Tests
"""

import unittest
import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath('.'))

from backend.services.scenario_service import ScenarioService


class TestScenarioService(unittest.TestCase):

    def setUp(self):
        self.service = ScenarioService()

    def test_list_scenarios(self):
        scenarios = self.service.list_scenarios()
        self.assertEqual(len(scenarios), 3)
        ids = [s["id"] for s in scenarios]
        self.assertIn("disaster", ids)
        self.assertIn("agriculture", ids)
        self.assertIn("urban", ids)

    def test_load_scenario(self):
        async def run():
            res = await self.service.load_scenario_into_session("urban")
            self.assertIn("session_id", res)
            self.assertIn("images", res)
            self.assertGreaterEqual(len(res["images"]), 1)
        asyncio.run(run())


if __name__ == "__main__":
    unittest.main()
