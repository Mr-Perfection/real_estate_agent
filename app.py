import streamlit as st
import os
from PIL import Image
import tempfile
from datetime import datetime
import json
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import asyncio
from temporalio.client import Client
from run_workflow import PropertyAnalysisWorkflow
from shared import PROPERTY_ANALYSIS_WORKFLOW_QUEUE_NAME

# Load environment variables
load_dotenv()

async def run_property_analysis(listing_text: str) -> dict:
    """Run the property analysis workflow"""
    try:
        # Connect to Temporal server
        client = await Client.connect("localhost:7233")
        
        # Create a unique workflow ID based on timestamp
        workflow_id = f"property-analysis-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Start the workflow
        result = await client.execute_workflow(
            PropertyAnalysisWorkflow.run,
            listing_text,  # Using listing text as the search URL for now
            id=workflow_id,
            task_queue=PROPERTY_ANALYSIS_WORKFLOW_QUEUE_NAME
        )
        
        return result
        
    except Exception as e:
        return {
            'error': str(e),
            'status': 'failed'
        }

def main():
    st.title("AI Real Estate Deal Analyzer")
    st.write("Upload a property listing and photos for analysis")

    # File upload section
    listing_text = st.text_area("Paste the property listing text here:", height=200)
    # uploaded_files = st.file_uploader("Upload property photos (2-3 images)", 
    #                                 type=['jpg', 'jpeg', 'png'],
    #                                 accept_multiple_files=True)

    if st.button("Analyze Deal"):
        if not listing_text:
            # print(f"No listing text or photos provided, {listing_text}, {uploaded_files}")
            print(f"No listing text or photos provided, {listing_text}")
            st.warning("Please provide both listing text and photos")
            return

        with st.spinner("Analyzing your property..."):
            # Process uploaded images
            # images = []
            # for uploaded_file in uploaded_files:
            #     image = Image.open(uploaded_file)
            #     images.append(image)

            # Run the Temporal workflow
            try:
                # Run the async workflow
                # result = asyncio.run(run_property_analysis(listing_text, images))
                result = asyncio.run(run_property_analysis(listing_text))
                
                if 'error' in result:
                    st.error(f"Analysis failed: {result['error']}")
                    return

                # Display results
                st.subheader("Analysis Results")
                
                # Text Issues
                st.write("### Text Analysis")
                for issue in result['risk_analysis']['issues']:
                    st.warning(f"⚠️ {issue}")

                # Image Findings
                # st.write("### Image Analysis")
                # for i, image in enumerate(images):
                #     st.image(image, caption=f"Photo {i+1}")
                    # Note: Image analysis results would be in the workflow result
                    # but we're using mock data for now

                # Financial Metrics
                st.write("### Financial Analysis")
                st.metric("Capitalization Rate", f"{result['financial_metrics']['cap_rate']:.2f}%")
                st.metric("Net Operating Income", f"${result['financial_metrics']['noi']:,.2f}")
                st.metric("Risk Level", result['financial_metrics']['risk_level'])

                # Download Report
                if st.button("📥 Download Report"):
                    report = {
                        "timestamp": datetime.now().isoformat(),
                        "analysis": result
                    }
                    st.download_button(
                        label="Download JSON Report",
                        data=json.dumps(report, indent=2),
                        file_name="property_analysis_report.json",
                        mime="application/json"
                    )

            except Exception as e:
                st.error(f"Error running analysis: {str(e)}")

if __name__ == "__main__":
    main() 