import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from backend.services.query_service import QueryService

async def main():
    service = QueryService()
    print("Testing Query: 'Has the built-up area increased?'")
    result = await service.process("Has the built-up area increased?")
    
    print("\n--- Answer ---")
    print(result.answer)
    
    print("\n--- Confidence ---")
    print(result.confidence)
    
    print("\n--- Execution Trace ---")
    for step in result.execution_trace:
        print(f"Step {step.step_number}: {step.module} -> {step.action} [{step.status}]")

if __name__ == "__main__":
    asyncio.run(main())
