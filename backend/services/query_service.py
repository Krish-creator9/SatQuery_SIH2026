"""
SatQuery AI — Query Service

Orchestrates the full analysis pipeline:
Query Analyzer → Evidence Planner → Analysis Modules → Evidence Fusion → Result

This is the central coordinator. It calls each component in sequence
and constructs the final FusedResult.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from backend.schemas.evidence import AnalysisResult, AnalysisStatus
from backend.schemas.result import ExecutionStep, FusedResult

logger = logging.getLogger(__name__)


class QueryService:
    """
    Orchestrates the full SatQuery pipeline.

    Currently a skeleton — modules are connected as they are built
    in subsequent phases.
    """

    def __init__(self):
        self._step_counter = 0

    async def process(self, query: str, session_id: str | None = None) -> FusedResult:
        """
        Run the full pipeline for a given query.

        Phase 1: Returns stub result with execution trace.
        Future: Connects all modules.
        """
        self._step_counter = 0
        start_time = time.time()
        trace: list[ExecutionStep] = []
        results: list[AnalysisResult] = []

        # Step 1: Parse query
        start_parse = time.time()
        from planner.query_analyzer import QueryAnalyzer
        analyzer = QueryAnalyzer()
        parsed_query = analyzer.parse(query)
        duration_parse = round((time.time() - start_parse) * 1000, 1)

        trace.append(self._make_step(
            module="planner.query_analyzer",
            action="parse_query",
            status="success",
            duration_ms=duration_parse,
            detail=f"Parsed intent: {parsed_query.task_type.value}"
        ))

        # Step 2: Plan evidence
        start_plan = time.time()
        from planner.evidence_planner import EvidencePlanner
        planner = EvidencePlanner()
        plan = planner.create_plan(parsed_query)
        duration_plan = round((time.time() - start_plan) * 1000, 1)

        trace.append(self._make_step(
            module="planner.evidence_planner",
            action="create_plan",
            status="success",
            duration_ms=duration_plan,
            detail=f"Created plan with {len(plan)} analysis modules: {[p.module_id for p in plan]}"
        ))

        # Step 3: Run analyses
        start_analysis = time.time()
        
        # We need the image paths from the session. For now, fetch from ImageService.
        # If no session, we skip this step or use dummy data.
        images = []
        if session_id:
            from backend.services.image_service import ImageService
            image_service = ImageService()
            from backend.config import UPLOAD_DIR
            session_dir = UPLOAD_DIR / session_id
            if session_dir.exists():
                images = list(session_dir.glob("*.*"))

        import importlib
        
        for plan_step in plan:
            # Instantiate the analyzer dynamically based on module_id
            # Example module_id: "analysis.optical.spectral_indices"
            try:
                module_path = plan_step.module_id
                # Quick mapping from module path to Class name
                if "spectral_indices" in module_path:
                    from analysis.optical.spectral_indices import SpectralIndicesAnalyzer
                    analyzer = SpectralIndicesAnalyzer()
                elif "band_analysis" in module_path:
                    from analysis.optical.band_analysis import BandAnalyzer
                    analyzer = BandAnalyzer()
                elif "backscatter" in module_path:
                    from analysis.sar.backscatter import BackscatterAnalyzer
                    analyzer = BackscatterAnalyzer()
                elif "sar_water" in module_path:
                    from analysis.sar.sar_water import SARWaterAnalyzer
                    analyzer = SARWaterAnalyzer()
                elif "registration" in module_path:
                    from analysis.temporal.registration import RegistrationAnalyzer
                    analyzer = RegistrationAnalyzer()
                elif "change_detection" in module_path:
                    from analysis.temporal.change_detection import ChangeDetectionAnalyzer
                    analyzer = ChangeDetectionAnalyzer()
                elif "change_map" in module_path:
                    from analysis.temporal.change_map import ChangeMapAnalyzer
                    analyzer = ChangeMapAnalyzer()
                elif "vqa_engine" in module_path:
                    from models.vqa.vqa_engine import VQAEngine
                    analyzer = VQAEngine()
                elif "caption_engine" in module_path:
                    from models.captioning.caption_engine import CaptionEngine
                    analyzer = CaptionEngine()
                elif "grounding_engine" in module_path:
                    from models.grounding.grounding_engine import GroundingEngine
                    analyzer = GroundingEngine()
                else:
                    raise ValueError(f"Unknown module {module_path}")

                # Prepare kwargs
                kwargs = plan_step.params.copy()
                is_temporal = "temporal" in module_path
                
                if is_temporal:
                    if len(images) >= 2:
                        kwargs["image_a_path"] = str(images[0])
                        kwargs["image_b_path"] = str(images[1])
                    else:
                        trace.append(self._make_step(
                            module=module_path,
                            action="analyze",
                            status="skipped",
                            detail="Requires at least 2 images for temporal analysis."
                        ))
                        continue
                elif len(images) >= 1:
                    kwargs["image_path"] = str(images[0])
                else:
                    trace.append(self._make_step(
                        module=module_path,
                        action="analyze",
                        status="skipped",
                        detail="No images available in session."
                    ))
                    continue

                if "image_path" in kwargs or ("image_a_path" in kwargs and "image_b_path" in kwargs):
                    result = await analyzer.safe_analyze(**kwargs)
                    results.append(result)
                    
                    trace.append(self._make_step(
                        module=module_path,
                        action="analyze",
                        status=result.status.value,
                        duration_ms=result.metadata.get("processing_time_ms", 0),
                        detail=f"Task: {result.task}. Verdicts: {[e.verdict for e in result.evidence]}"
                    ))

            except Exception as e:
                logger.error(f"Failed to run module {plan_step.module_id}: {e}")
                if plan_step.required:
                    trace.append(self._make_step(
                        module=plan_step.module_id,
                        action="analyze",
                        status="failed",
                        detail=str(e)
                    ))

        duration_analysis = round((time.time() - start_analysis) * 1000, 1)

        # Step 4: Fuse evidence
        start_fusion = time.time()
        from fusion.evidence_fusion import EvidenceFusionEngine
        fuser = EvidenceFusionEngine()
        
        # We don't pass trace in yet so we can append the fusion step first
        duration_fusion = round((time.time() - start_fusion) * 1000, 1)
        trace.append(self._make_step(
            module="fusion.evidence_fusion",
            action="fuse_evidence",
            status="success",
            duration_ms=duration_fusion,
            detail=f"Fused {len(results)} results."
        ))

        total_time = (time.time() - start_time) * 1000
        
        # The fuser constructs the final object
        final_result = fuser.fuse(query=query, results=results, trace=trace)
        return final_result

    def _make_step(
        self,
        module: str,
        action: str,
        status: str,
        detail: str = "",
        duration_ms: float = 0,
    ) -> ExecutionStep:
        """Create an execution step entry."""
        self._step_counter += 1
        return ExecutionStep(
            step_number=self._step_counter,
            module=module,
            action=action,
            status=status,
            duration_ms=duration_ms,
            detail=detail,
        )
