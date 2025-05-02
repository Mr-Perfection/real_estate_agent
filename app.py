import streamlit as st
import os
from PIL import Image
from datetime import datetime
import json
from dotenv import load_dotenv
import asyncio
from temporalio.client import Client
from run_workflow import PropertyAnalysisWorkflow
from shared import PROPERTY_ANALYSIS_WORKFLOW_QUEUE_NAME
from vapi_call_flow import initiate_vapi_call

# Load environment variables
load_dotenv()

async def run_property_analysis(listing_text: str) -> dict:
    """Run the property analysis workflow"""
    try:
        client = await Client.connect("localhost:7233")
        workflow_id = f"property-analysis-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        result = await client.execute_workflow(
            PropertyAnalysisWorkflow.run,
            listing_text,
            id=workflow_id,
            task_queue=PROPERTY_ANALYSIS_WORKFLOW_QUEUE_NAME
        )
        return result
    except Exception as e:
        return {'error': str(e), 'status': 'failed'}

def main():
    st.title("AI Real Estate Deal Analyzer")
    st.write("Upload a property listing and photos for analysis")

    # Initialize session state
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None

    # Input field
    listing_text = st.text_area("Paste the property listing text here:", height=200)

    # Analyze Button
    if st.button("Analyze Deal"):
        if not listing_text:
            st.warning("Please provide the property listing text.")
            return

        with st.spinner("Analyzing your property..."):
            try:
                result = asyncio.run(run_property_analysis(listing_text))
                if 'error' in result:
                    st.error(f"Analysis failed: {result['error']}")
                    return
                st.session_state.analysis_result = result
            except Exception as e:
                st.error(f"Error running analysis: {str(e)}")

    # Show results if available
    if st.session_state.analysis_result:
        result = st.session_state.analysis_result

        st.subheader("Analysis Results")

        st.write("### Text Analysis")
        for issue in result['risk_analysis']['issues']:
            st.warning(f"⚠️ {issue}")

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

        # Call Me Button
        if st.button("📞 Call Me to Discuss"):
            print("🟢 Button clicked — calling Vapi...")
            success, message = initiate_vapi_call(call_type="agent")
            print("🔁 Vapi response:", success, message)
            if success:
                st.success(message)
            else:
                st.error(message)

if __name__ == "__main__":
    main()
