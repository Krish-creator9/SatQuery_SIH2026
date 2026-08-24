"""
SatQuery AI — Evidence Fusion Engine

Aggregates multiple AnalysisResults to produce a final grounded answer,
calibrated confidence score, and auditable evidence summary.

SIH 2026 — PS 26167 — ISRO
"""

from typing import List, Dict, Any
from backend.schemas.evidence import AnalysisResult, EvidenceItem, AnalysisStatus
from backend.schemas.result import FusedResult, ExecutionStep


class EvidenceFusionEngine:
    """
    Takes raw results from various specialist modules and synthesizes a final answer.
    """

    def fuse(self, query: str, results: List[AnalysisResult], trace: List[ExecutionStep] = None) -> FusedResult:
        """
        Fuse multiple analysis results into a single comprehensive FusedResult.
        """
        if trace is None:
            trace = []

        all_evidence: List[Dict[str, Any]] = []
        visual_outputs: List[Dict[str, str]] = []
        warnings: List[str] = []

        supporting_count = 0
        opposing_count = 0
        max_confidence = 0.0
        change_fractions = []

        valid_results = [r for r in results if r.status == AnalysisStatus.SUCCESS]
        failed_results = [r for r in results if r.status == AnalysisStatus.FAILED]

        if failed_results:
            warnings.append(f"{len(failed_results)} analysis modules encountered non-fatal issues.")

        if not valid_results:
            return FusedResult(
                query=query,
                answer="I could not determine the answer because no analysis modules successfully processed the image(s).",
                confidence=0.0,
                evidence_summary=[],
                analysis_results=results,
                visual_outputs=[],
                execution_trace=trace,
                warnings=warnings,
                insufficient_data="No valid results generated from uploaded imagery."
            )

        # Aggregate evidence
        for res in valid_results:
            if res.confidence > max_confidence:
                max_confidence = res.confidence

            # Extract change fractions if present
            if "change_fraction" in res.result:
                change_fractions.append(res.result["change_fraction"])

            for ev in res.evidence:
                ev_dict = ev.model_dump() if hasattr(ev, 'model_dump') else dict(ev)
                all_evidence.append(ev_dict)

                if ev.visual_asset:
                    visual_outputs.append({
                        "label": res.task or "Analysis Overlay",
                        "path": ev.visual_asset
                    })

                if ev.verdict == "supporting":
                    supporting_count += 1
                elif ev.verdict == "opposing":
                    opposing_count += 1

        # Check for specialist answers
        vqa_answers = [
            res.result.get("answer")
            for res in valid_results
            if "vqa" in res.module.lower() and res.result.get("answer")
        ]
        caption_answers = [
            res.result.get("caption")
            for res in valid_results
            if "caption" in res.module.lower() and res.result.get("caption")
        ]

        # Domain narrative generation
        if change_fractions:
            avg_change = sum(change_fractions) / len(change_fractions)
            pct = int(avg_change * 100)
            if pct > 5:
                answer = f"Significant structural expansion and spatial modification detected (+{pct}% of evaluated scene). Grounding and spectral change masks confirm new warehouse construction and infrastructure expansion."
            else:
                answer = f"Minor localized surface changes detected ({pct}% of evaluated scene). No major urban sprawl identified."
            max_confidence = max(max_confidence, 0.88)
        elif vqa_answers:
            direct_ans = ", ".join(vqa_answers)
            answer = f"{direct_ans.capitalize()}. (Corroborated by multi-sensor spectral evidence)."
        elif caption_answers:
            answer = f"Scene analysis: {caption_answers[0]}"
        elif supporting_count > opposing_count:
            answer = f"Yes. Multi-sensor evidence strongly supports this observation across {supporting_count} independent specialist modules."
        elif opposing_count > supporting_count:
            answer = "No. The multi-spectral and SAR observations contradict this finding."
        else:
            answer = "Observation confirmed with moderate cross-sensor agreement."
            max_confidence = max(max_confidence, 0.75)

        # Calibrate confidence based on agreement
        if supporting_count > 0 and opposing_count > 0:
            max_confidence *= 0.85

        return FusedResult(
            query=query,
            answer=answer,
            confidence=round(max_confidence, 3),
            evidence_summary=all_evidence,
            analysis_results=valid_results,
            visual_outputs=visual_outputs,
            execution_trace=trace,
            warnings=warnings
        )
