"""
SatQuery AI — Query Analyzer

Parses natural language queries and maps them to a structured TaskType intent.
Phase 6: Uses a rule-based/regex approach (fast, CPU-bound, deterministic).
"""

import re
from typing import Optional

from backend.schemas.query import ParsedQuery, TaskType


class QueryAnalyzer:
    """
    Analyzes natural language to determine the core remote sensing task.
    """

    # Keyword mappings to TaskTypes
    INTENT_RULES = {
        TaskType.VEGETATION_ANALYSIS: [
            r"\b(vegetation|plants|trees|forest|greenery|crops|ndvi)\b",
            r"\b(deforestation|logging|agriculture)\b"
        ],
        TaskType.WATER_DETECTION: [
            r"\b(water|lake|river|sea|ocean|flood|ndwi)\b",
            r"\b(reservoir|wetland|coast)\b"
        ],
        TaskType.URBAN_ANALYSIS: [
            r"\b(urban|buildings|city|roads|built-up|infrastructure|construction)\b",
            r"\b(settlement|houses)\b"
        ],
        TaskType.CHANGE_DETECTION: [
            r"\b(change|changed|difference|before and after|over time|new)\b",
            r"\b(disappeared|appeared|trend)\b"
        ],
        TaskType.SAR_ANALYSIS: [
            r"\b(sar|radar|backscatter|roughness)\b",
            r"\b(ships?|vessels?)\b" # Ships are classically detected via SAR
        ],
        # VQA, Captioning, Classification, Grounding fallback keywords 
        # for when ML models come online in Phase 11-12
        TaskType.VQA: [
            r"\b(how many|what is|count|describe|what do you see|explain)\b",
            r"\b(why|where is the)\b"
        ],
    }

    def parse(self, query: str) -> ParsedQuery:
        """
        Parse a raw query string into a structured ParsedQuery.
        """
        query_lower = query.lower().strip()
        
        # Default intent if no rules match
        primary_intent = TaskType.GENERAL
        matched_intents = set()

        # Check all rules
        for intent, patterns in self.INTENT_RULES.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    matched_intents.add(intent)
                    break # Move to next intent type once matched

        # Resolve primary intent (heuristic hierarchy)
        # Change detection overrides simple feature detection if present
        if TaskType.CHANGE_DETECTION in matched_intents:
            primary_intent = TaskType.CHANGE_DETECTION
        elif TaskType.SAR_ANALYSIS in matched_intents:
            primary_intent = TaskType.SAR_ANALYSIS
        elif TaskType.WATER_DETECTION in matched_intents:
            primary_intent = TaskType.WATER_DETECTION
        elif TaskType.VEGETATION_ANALYSIS in matched_intents:
            primary_intent = TaskType.VEGETATION_ANALYSIS
        elif TaskType.URBAN_ANALYSIS in matched_intents:
            primary_intent = TaskType.URBAN_ANALYSIS
        elif TaskType.VQA in matched_intents:
            primary_intent = TaskType.VQA
        elif len(matched_intents) > 0:
            # Fallback to the first matched intent if not explicitly caught above
            primary_intent = list(matched_intents)[0]

        return ParsedQuery(
            original_query=query,
            task_type=primary_intent,
            requires_temporal=(primary_intent == TaskType.CHANGE_DETECTION),
            requires_sar=(primary_intent == TaskType.SAR_ANALYSIS),
            requires_vlm=(primary_intent in [TaskType.VQA, TaskType.CAPTIONING, TaskType.GROUNDING])
        )
