"""
SatQuery AI — Evidence Planner

Maps structured intents to a concrete plan of analysis modules.
Determines what evidence is needed to answer a query.
"""

from typing import Any, List

from backend.schemas.query import ParsedQuery, TaskType
from backend.config import is_feature_enabled
from models.registry import model_registry


class AnalysisPlan:
    """Represents a planned analysis step."""
    def __init__(self, module_id: str, params: dict[str, Any], required: bool = True):
        self.module_id = module_id
        self.params = params
        self.required = required # If False, failure doesn't halt the pipeline


class EvidencePlanner:
    """
    Creates an execution plan based on the parsed query intent.
    """

    def create_plan(self, parsed_query: ParsedQuery) -> List[AnalysisPlan]:
        """
        Map a ParsedQuery to a list of AnalysisPlans.
        """
        plan: List[AnalysisPlan] = []
        intent = parsed_query.task_type

        if intent == TaskType.VEGETATION_ANALYSIS:
            if is_feature_enabled("optical_analysis"):
                plan.append(AnalysisPlan(
                    module_id="analysis.optical.spectral_indices",
                    params={"index_type": "NDVI"},
                    required=False
                ))
            if is_feature_enabled("sar_analysis"):
                # SAR can provide supplementary info on structure
                plan.append(AnalysisPlan(
                    module_id="analysis.sar.backscatter",
                    params={},
                    required=False
                ))
            if is_feature_enabled("vlm_vqa"):
                plan.append(AnalysisPlan(
                    module_id="models.vqa.vqa_engine",
                    params={"question": f"Is there vegetation or green cover in this satellite image? {parsed_query.original_query}"},
                    required=False
                ))

        elif intent == TaskType.WATER_DETECTION:
            if is_feature_enabled("optical_analysis"):
                plan.append(AnalysisPlan(
                    module_id="analysis.optical.spectral_indices",
                    params={"index_type": "NDWI"},
                    required=False
                ))
            if is_feature_enabled("sar_analysis"):
                plan.append(AnalysisPlan(
                    module_id="analysis.sar.sar_water",
                    params={},
                    required=False
                ))
            if is_feature_enabled("vlm_vqa"):
                plan.append(AnalysisPlan(
                    module_id="models.vqa.vqa_engine",
                    params={"question": f"Are there water bodies, lakes, rivers, or oceans in this satellite image? {parsed_query.original_query}"},
                    required=False
                ))

        elif intent == TaskType.CHANGE_DETECTION:
            if is_feature_enabled("temporal_analysis"):
                plan.append(AnalysisPlan(
                    module_id="analysis.temporal.registration",
                    params={}
                ))
                plan.append(AnalysisPlan(
                    module_id="analysis.temporal.change_detection",
                    params={}
                ))
                plan.append(AnalysisPlan(
                    module_id="analysis.temporal.change_map",
                    params={},
                    required=False
                ))

        elif intent == TaskType.URBAN_ANALYSIS or intent == TaskType.SAR_ANALYSIS:
            if is_feature_enabled("sar_analysis"):
                plan.append(AnalysisPlan(
                    module_id="analysis.sar.backscatter",
                    params={},
                    required=False
                ))
            if is_feature_enabled("optical_analysis"):
                plan.append(AnalysisPlan(
                    module_id="analysis.optical.band_analysis",
                    params={},
                    required=False
                ))
            if is_feature_enabled("vlm_vqa"):
                plan.append(AnalysisPlan(
                    module_id="models.vqa.vqa_engine",
                    params={"question": f"Are there buildings, urban areas, or infrastructure in this satellite image? {parsed_query.original_query}"},
                    required=False
                ))

        elif intent == TaskType.VQA or intent == TaskType.GENERAL:
            if is_feature_enabled("vlm_vqa"):
                plan.append(AnalysisPlan(
                    module_id="models.vqa.vqa_engine",
                    params={"question": parsed_query.original_query}
                ))
            if is_feature_enabled("vlm_captioning"):
                plan.append(AnalysisPlan(
                    module_id="models.captioning.caption_engine",
                    params={},
                    required=False
                ))
            if not is_feature_enabled("vlm_vqa") and is_feature_enabled("optical_analysis"):
                plan.append(AnalysisPlan(
                    module_id="analysis.optical.band_analysis",
                    params={}
                ))

        return plan
