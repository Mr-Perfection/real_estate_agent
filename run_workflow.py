from datetime import timedelta
from temporalio import workflow, activity
from temporalio.client import Client
from temporalio.worker import Worker
import asyncio
from typing import Dict, Any

from shared import PROPERTY_ANALYSIS_WORKFLOW_QUEUE_NAME

# Define activity interfaces
@activity.defn
async def scrape_properties(search_url: str) -> str:
    """Activity to scrape property data"""
    # This will be replaced with actual implementation
    import get_property_scraping
    listing = get_property_scraping.main(zillow_url=search_url)
    print(f"Listing: {listing}")
    return listing[0]
    
    # return {
    #     'price': 500000,
    #     'address': '123 Main St',
    #     'description': 'Sample property description'
    # }

@activity.defn
async def analyze_with_gumloop(property_data: str) -> Dict[str, Any]:
    from gumloop_call import get_gumloop_data
    """Activity to analyze property with Gumloop"""
    # This will be replaced with actual implementation
    print(f"Property data: {property_data}")
    return get_gumloop_data(property_data)

@activity.defn
async def estimate_rent(address: str) -> float:
    """Activity to estimate rent"""
    # This will be replaced with actual implementation
    return 3000.0

@activity.defn
async def calculate_cap_rate(purchase_price: float, monthly_rent: float, monthly_expenses: float) -> tuple[float, float]:
    """Activity to calculate cap rate"""
    annual_rent = monthly_rent * 12
    annual_expenses = monthly_expenses * 12
    noi = annual_rent - annual_expenses
    cap_rate = (noi / purchase_price) * 100
    return cap_rate, noi

@activity.defn
async def collate_results(property_data: Dict[str, Any], 
                   issues: Dict[str, Any], 
                   cap_rate: float, 
                   noi: float) -> Dict[str, Any]:
    """Activity to collate results"""
    return {
        'property_details': property_data,
        'risk_analysis': issues,
        'financial_metrics': {
            'cap_rate': cap_rate,
            'noi': noi,
            'risk_level': 'High' if cap_rate < 5 else 'Medium' if cap_rate < 8 else 'Low'
        }
    }

# Define the workflow
@workflow.defn
class PropertyAnalysisWorkflow:
    @workflow.run
    async def run(self, search_url: str) -> Dict[str, Any]:
        """Main workflow execution"""
        try:
            # 1. Scrape property data
            property_data = await workflow.execute_activity(
                scrape_properties,
                search_url,
                start_to_close_timeout=timedelta(minutes=5)
            )
            print(f"Property data: {property_data}")
            
            # 2. Analyze with Gumloop
            issues = await workflow.execute_activity(
                analyze_with_gumloop,
                property_data,
                start_to_close_timeout=timedelta(minutes=5)
            )
            print(f"Issues: {issues}")
            
            # 3. Calculate financial metrics
            monthly_rent = await workflow.execute_activity(
                estimate_rent,
                property_data['address'],
                start_to_close_timeout=timedelta(minutes=2)
            )
            
            cap_rate, noi = await workflow.execute_activity(
                calculate_cap_rate,
                args=[property_data['price'], monthly_rent, 1000],
                start_to_close_timeout=timedelta(minutes=2)
            )
            print(f"Cap rate: {cap_rate}, NOI: {noi}")
            
            # 4. Collate results
            final_results = await workflow.execute_activity(
                collate_results,
                args=[property_data, issues, cap_rate, noi],
                start_to_close_timeout=timedelta(minutes=2)
            )
            
            return final_results
            
        except Exception as e:
            print(f"Workflow error: {str(e)}")
            return {
                'error': str(e),
                'status': 'failed'
            }

async def run_workflow(search_url: str):
    """Helper function to run the workflow"""
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")
    
    # Start the workflow
    result = await client.execute_workflow(
        PropertyAnalysisWorkflow.run,
        search_url,
        id=f"property-analysis-{search_url}",
        task_queue=PROPERTY_ANALYSIS_WORKFLOW_QUEUE_NAME
    )
    
    return result

async def main():
    """Example usage"""
    search_url = 'https://www.zillow.com/homes/for_sale/?searchQueryState=%7B"isMapVisible"%3Atrue%2C"mapBounds"%3A%7B"west"%3A-124.61572460426518%2C"east"%3A-120.37225536598393%2C"south"%3A36.71199595991113%2C"north"%3A38.74934086729303%7D%2C"filterState"%3A%7B"sort"%3A%7B"value"%3A"days"%7D%2C"ah"%3A%7B"value"%3Atrue%7D%7D%2C"isListVisible"%3Atrue%2C"customRegionId"%3A"7d43965436X1-CRmxlqyi837u11_1fi65c"%7D'
    result = await run_workflow(search_url)
    print("Workflow Result:", result)

if __name__ == "__main__":
    asyncio.run(main()) 