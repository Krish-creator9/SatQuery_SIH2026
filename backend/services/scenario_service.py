"""
SatQuery AI — Scenario Service

Manages operational mission scenarios (Disaster Response, Agriculture Monitoring, Urban Expansion)
and sets up pre-configured datasets and sessions for immediate testing.
"""

import os
import shutil
from pathlib import Path
from typing import Any, Dict, List

from backend.config import DATA_DIR, UPLOAD_DIR
from backend.services.session_service import SessionService


class ScenarioService:
    """Service providing pre-configured remote sensing mission scenarios."""

    SCENARIOS: Dict[str, Dict[str, Any]] = {
        "disaster": {
            "id": "disaster",
            "title": "Disaster Response",
            "subtitle": "Flood Extent & Emergency Infrastructure Assessment",
            "icon": "water_damage",
            "accent_color": "#00f2ff",
            "description": "Rapid assessment of flood extents, standing water, and infrastructure damage using Optical + SAR radar passes.",
            "modalities": ["Sentinel-2 (Optical MSI)", "Sentinel-1 (SAR C-Band)"],
            "mode": "fusion",
            "sample_files": [
                "optical_2020_baseline.bmp",
                "sar_cband_backscatter.bmp",
            ],
            "default_query": "Where are the flood-affected regions and how much did water extent increase?",
            "suggested_queries": [
                "Where are the flood-affected regions and how much did water extent increase?",
                "Show flooded roads and assess building damage",
                "Find safe zones outside flood inundation",
                "SAR flood extent delta across observation dates",
            ],
        },
        "agriculture": {
            "id": "agriculture",
            "title": "Agriculture Monitoring",
            "subtitle": "Crop Health, NDVI Anomalies & Irrigation Stress",
            "icon": "eco",
            "accent_color": "#74f5ff",
            "description": "Track crop health, predict yield variations, and monitor irrigation levels across vast regions using NDVI and NDWI spectral indices.",
            "modalities": ["Sentinel-2 (Red, Green, NIR Multi-Spectral)"],
            "mode": "change",
            "sample_files": [
                "optical_2020_baseline.bmp",
                "optical_2024_target.bmp",
            ],
            "default_query": "Which regions show vegetation stress and where has crop health decreased between the two dates?",
            "suggested_queries": [
                "Which regions show vegetation stress and where has crop health decreased between the two dates?",
                "NDVI anomalies across eastern crop parcels",
                "Water stress and crop drought impact",
                "Crop classification and vegetation vitality delta",
            ],
        },
        "urban": {
            "id": "urban",
            "title": "Urban Expansion",
            "subtitle": "Sprawl Analysis & Industrial Structure Growth",
            "icon": "location_city",
            "accent_color": "#adc6ff",
            "description": "Analyze sprawl, detect informal settlements, and track structural changes over multi-year periods with bi-temporal change detection.",
            "modalities": ["Sentinel-2 Multi-Temporal Pairs", "Sentinel-1 SAR"],
            "mode": "change",
            "sample_files": [
                "optical_2020_baseline.bmp",
                "optical_2024_target.bmp",
            ],
            "default_query": "Identify new structures built between the two dates and estimate their area and expansion percentage.",
            "suggested_queries": [
                "Identify new structures built between the two dates and estimate their area and expansion percentage.",
                "New industrial warehouse construction and road expansion",
                "Deforestation vs urban development footprint",
                "Classify bare soil to built-up transitions",
            ],
        },
    }

    def list_scenarios(self) -> List[Dict[str, Any]]:
        """Return list of all configured scenarios."""
        return list(self.SCENARIOS.values())

    def get_scenario(self, scenario_id: str) -> Dict[str, Any] | None:
        """Get scenario details by ID."""
        return self.SCENARIOS.get(scenario_id)

    async def load_scenario_into_session(self, scenario_id: str, session_id: str | None = None) -> Dict[str, Any]:
        """
        Loads the scenario's sample images into an active session.
        """
        scenario = self.get_scenario(scenario_id)
        if not scenario:
            raise ValueError(f"Unknown scenario ID: {scenario_id}")

        session_service = SessionService()
        if not session_id or not session_service.get_session(session_id):
            session_id = session_service.create_session()

        session_dir = UPLOAD_DIR / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        samples_dir = DATA_DIR / "samples"

        loaded_images = []
        for filename in scenario["sample_files"]:
            src = samples_dir / filename
            if src.exists():
                dst = session_dir / filename
                shutil.copy2(src, dst)
                loaded_images.append({
                    "filename": filename,
                    "path": str(dst),
                    "size_mb": round(dst.stat().st_size / (1024 * 1024), 2),
                })

        return {
            "session_id": session_id,
            "scenario": scenario,
            "images": loaded_images,
        }
