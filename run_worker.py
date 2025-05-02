import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from run_workflow import (
    PropertyAnalysisWorkflow,
    scrape_properties,
    analyze_with_gumloop,
    estimate_rent,
    calculate_cap_rate,
    collate_results
)
from shared import PROPERTY_ANALYSIS_WORKFLOW_QUEUE_NAME

async def run_worker():
    """Run the Temporal worker to process property analysis tasks"""
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")
    
    # Run the worker
    worker = Worker(
        client,
        task_queue=PROPERTY_ANALYSIS_WORKFLOW_QUEUE_NAME,
        workflows=[PropertyAnalysisWorkflow],
        activities=[
            scrape_properties,
            analyze_with_gumloop,
            estimate_rent,
            calculate_cap_rate,
            collate_results
        ]
    )
    
    print(f"Starting worker for task queue: {PROPERTY_ANALYSIS_WORKFLOW_QUEUE_NAME}")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(run_worker())
