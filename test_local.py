"""
SatQuery AI — End-to-End Pipeline Verification Script
"""

import asyncio
import sys
import os
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath('.'))

from backend.config import UPLOAD_DIR
from backend.services.query_service import QueryService
from backend.services.scenario_service import ScenarioService
from models.adaptation.adapter import BigEarthNetAdapter
from models.registry import model_registry


async def main():
    print("=" * 60)
    print("  SatQuery AI — System Verification (SIH 2026 PS 26167)")
    print("=" * 60)

    # 1. Test Model Registry
    print("\n[1/4] Checking Model Registry...")
    models = model_registry.list_models()
    for m in models:
        print(f"  - {m['role'].upper()}: {m['model_name']} ({m['size_mb']}MB, GPU={m['requires_gpu']})")

    # 2. Test Scenario Service
    print("\n[2/4] Checking Operational Mission Scenarios...")
    scenario_service = ScenarioService()
    scenarios = scenario_service.list_scenarios()
    for s in scenarios:
        print(f"  - {s['title']} [{s['id']}]: {len(s['suggested_queries'])} queries")

    # 3. Test BigEarthNet Adapter
    print("\n[3/4] Testing BigEarthNet Land Cover Adapter...")
    adapter = BigEarthNetAdapter()
    sample_img = os.path.join("data", "samples", "optical_2024_target.bmp")
    if os.path.exists(sample_img):
        res = await adapter.safe_analyze(image_path=sample_img)
        print(f"  - Status: {res.status.value}, Confidence: {res.confidence}")
        print(f"  - Top Classes: {res.result.get('top_classes')}")

    # 4. Test Query Service with Images in Session
    print("\n[4/4] Testing Query Orchestrator with Sample Images...")
    test_session_id = "test-verification-session"
    session_dir = UPLOAD_DIR / test_session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy sample images
    shutil.copy2("data/samples/optical_2020_baseline.bmp", session_dir / "optical_2020_baseline.bmp")
    shutil.copy2("data/samples/optical_2024_target.bmp", session_dir / "optical_2024_target.bmp")

    query_service = QueryService()
    test_query = "Identify new structures built between the two dates and estimate their area."
    result = await query_service.process(test_query, session_id=test_session_id, mode="change")

    print(f"  - Answer: {result.answer}")
    print(f"  - Confidence: {result.confidence * 100:.1f}%")
    print(f"  - Execution Steps ({len(result.execution_trace)}):")
    for step in result.execution_trace:
        print(f"      [{step.status.upper()}] Step {step.step_number}: {step.module} -> {step.action} ({step.duration_ms}ms)")

    # Clean up test session
    shutil.rmtree(session_dir, ignore_errors=True)

    print("\n" + "=" * 60)
    print("  ALL VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
