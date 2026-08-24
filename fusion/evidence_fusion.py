"""
SatQuery AI — Evidence Fusion Engine

Aggregates multiple AnalysisResults to produce a final verdict and confidence score.
"""

from typing import List
from backend.schemas.evidence import AnalysisResult, EvidenceItem, AnalysisStatus
from backend.schemas.result import FusedResult, ExecutionStep

class EvidenceFusionEngine:
    """
    Takes raw results from various modules and synthesizes a final answer.
    """

    def fuse(self, query: str, results: List[AnalysisResult], trace: List[ExecutionStep] = None) -> FusedResult:
        """
        Fuse multiple analysis results into a single comprehensive FusedResult.
        """
        if trace is None:
            trace = []
            
        all_evidence: List[EvidenceItem] = []
        visual_outputs: List[str] = []
        warnings: List[str] = []
        
        supporting_count = 0
        opposing_count = 0
        max_confidence = 0.0

        valid_results = [r for r in results if r.status == AnalysisStatus.SUCCESS]
        failed_results = [r for r in results if r.status == AnalysisStatus.FAILED]
        
        if failed_results:
            warnings.append(f"{len(failed_results)} analysis modules failed to execute.")

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
                insufficient_data="No valid results generated."
            )

        # Aggregate evidence
        for res in valid_results:
            # Keep track of the highest confidence module
            if res.confidence > max_confidence:
                max_confidence = res.confidence

            for ev in res.evidence:
                all_evidence.append(ev)
                if ev.visual_asset:
                    visual_outputs.append(ev.visual_asset)
                
                if ev.verdict == "supporting":
                    supporting_count += 1
                elif ev.verdict == "opposing":
                    opposing_count += 1

        # Check if VQA or Captioning produced a direct answer
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

        # Synthesize final answer based on rule-based voting and VLM responses
        if vqa_answers:
            direct_ans = ", ".join(vqa_answers)
            if supporting_count > 0:
                answer = f"{direct_ans.capitalize()}. (Evidence supports this detection)."
            else:
                answer = f"Model observation: {direct_ans}"
        elif caption_answers:
            answer = f"Scene analysis: {caption_answers[0]}"
        elif supporting_count > opposing_count:
            if opposing_count == 0:
                answer = "Yes. There is strong evidence supporting this."
            else:
                answer = "Yes, though the evidence is mixed, it leans towards supporting this."
        elif opposing_count > supporting_count:
            if supporting_count == 0:
                answer = "No. The evidence strongly contradicts this."
            else:
                answer = "No, the evidence leans against this."
        else:
            if supporting_count == 0 and opposing_count == 0:
                answer = "I could not find clear evidence either way."
                max_confidence = 0.3 # Low confidence if everything is neutral
            else:
                answer = "The evidence is inconclusive or perfectly split."
                max_confidence = 0.5

        # Penalize confidence slightly if evidence is mixed
        if supporting_count > 0 and opposing_count > 0:
            max_confidence *= 0.8

        return FusedResult(
            query=query,
            answer=answer,
            confidence=round(max_confidence, 2),
            evidence_summary=all_evidence,
            analysis_results=valid_results,
            visual_outputs=visual_outputs,
            execution_trace=trace,
            warnings=warnings
        )
