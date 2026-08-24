"""
SatQuery AI — Scenarios Router

Provides endpoints to list and load operational mission scenarios.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from backend.services.scenario_service import ScenarioService

router = APIRouter(prefix="/scenarios", tags=["Scenarios"])
scenario_service = ScenarioService()


class LoadScenarioRequest(BaseModel):
    scenario_id: str
    session_id: Optional[str] = None


@router.get("/")
async def list_scenarios():
    """List all available operational mission scenarios."""
    return {"scenarios": scenario_service.list_scenarios()}


@router.get("/{scenario_id}")
async def get_scenario(scenario_id: str):
    """Get details for a specific mission scenario."""
    scenario = scenario_service.get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found")
    return scenario


@router.post("/load")
async def load_scenario(request: LoadScenarioRequest):
    """Load a scenario's sample datasets into a session."""
    try:
        result = await scenario_service.load_scenario_into_session(
            scenario_id=request.scenario_id,
            session_id=request.session_id,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
