"""
SatQuery AI — Query Router

Accepts natural-language queries and orchestrates the full analysis pipeline.
"""

from fastapi import APIRouter, HTTPException

from backend.config import is_feature_enabled
from backend.schemas.query import QueryRequest, ParsedQuery, TaskType
from backend.schemas.result import FusedResult, ExecutionStep

router = APIRouter(prefix="/query", tags=["Query"])


@router.post("/", response_model=FusedResult)
async def process_query(request: QueryRequest):
    """
    Process a natural-language query against uploaded images.

    Pipeline: Query Analyzer → Evidence Planner → Analysis → Fusion → Result
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        from backend.services.query_service import QueryService
        service = QueryService()
        result = await service.process(query=request.query, session_id=request.session_id)
        return result
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks")
async def list_supported_tasks():
    """List all supported analysis task types and their availability."""
    tasks = []
    for task in TaskType:
        tasks.append({
            "task_type": task.value,
            "available": True,  # All tasks are structurally defined; modules may not be connected yet
            "description": _task_descriptions.get(task, ""),
        })
    return {"tasks": tasks}


# Task type descriptions for the API
_task_descriptions = {
    TaskType.VQA: "Answer a natural-language question about an image",
    TaskType.CAPTIONING: "Generate a description of the image content",
    TaskType.GROUNDING: "Locate regions matching a text description",
    TaskType.CHANGE_DETECTION: "Detect changes between two temporal images",
    TaskType.VEGETATION_ANALYSIS: "Analyze vegetation health using spectral indices",
    TaskType.WATER_DETECTION: "Detect water bodies using spectral/SAR analysis",
    TaskType.URBAN_ANALYSIS: "Analyze urban/built-up areas",
    TaskType.SAR_ANALYSIS: "Extract structural evidence from SAR imagery",
    TaskType.OPTICAL_ANALYSIS: "General optical/multispectral analysis",
    TaskType.COMPARISON: "Compare optical and SAR observations",
    TaskType.GENERAL: "General-purpose image analysis",
}
