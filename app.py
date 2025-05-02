import streamlit as st
import os
from PIL import Image
import tempfile
from datetime import datetime
import json
from dotenv import load_dotenv
from vapi_python import Vapi
from gumloop import GumloopClient
import pandas as pd
import numpy as np

# Load environment variables
load_dotenv()

# Initialize APIs
vapi_client = Vapi(api_key=os.getenv('VAPI_API_KEY'))
gumloop_client = GumloopClient(api_key=os.getenv('GUMLOOP_API_KEY'), user_id=os.getenv('GUMLOOP_USER_ID'), project_id=os.getenv('GUMLOOP_PROJECT_ID'))

def analyze_listing_text(text):
    """Analyze listing text using Gumloop AI Agent 1"""
    try:
        response = gumloop_client.analyze_text(
            text=text,
            agent_id="risk_keyword_analyzer"
        )
        return response
    except Exception as e:
        st.error(f"Error analyzing text: {str(e)}")
        return None

def analyze_images(images):
    """Analyze property images using Gumloop AI Agent 2"""
    try:
        results = []
        for img in images:
            response = gumloop_client.analyze_image(
                image=img,
                agent_id="property_image_analyzer"
            )
            results.append(response)
        return results
    except Exception as e:
        st.error(f"Error analyzing images: {str(e)}")
        return None

def calculate_cap_rate(price, annual_rent):
    """Calculate capitalization rate"""
    if price <= 0:
        return 0
    return (annual_rent / price) * 100

def generate_recommendation(text_analysis, image_analysis, cap_rate):
    """Generate final recommendation based on all analyses"""
    recommendation = {
        "text_issues": text_analysis.get("issues", []),
        "image_findings": [img.get("findings", []) for img in image_analysis],
        "financial_metrics": {
            "cap_rate": cap_rate,
            "risk_level": "High" if cap_rate < 5 else "Medium" if cap_rate < 8 else "Low"
        }
    }
    return recommendation

def main():
    st.title("AI Real Estate Deal Analyzer")
    st.write("Upload a property listing and photos for analysis")

    # File upload section
    listing_text = st.text_area("Paste the property listing text here:", height=200)
    uploaded_files = st.file_uploader("Upload property photos (2-3 images)", 
                                    type=['jpg', 'jpeg', 'png'],
                                    accept_multiple_files=True)

    if st.button("Analyze Deal"):
        if not listing_text or not uploaded_files:
            st.warning("Please provide both listing text and photos")
            return

        with st.spinner("Analyzing your property..."):
            # Process uploaded images
            images = []
            for uploaded_file in uploaded_files:
                image = Image.open(uploaded_file)
                images.append(image)

            # Run analyses
            text_analysis = analyze_listing_text(listing_text)
            image_analysis = analyze_images(images)
            
            # Mock financial data for demo
            price = 500000  # This would come from listing text analysis
            annual_rent = 30000  # This would come from listing text analysis
            cap_rate = calculate_cap_rate(price, annual_rent)

            # Generate recommendation
            recommendation = generate_recommendation(text_analysis, image_analysis, cap_rate)

            # Display results
            st.subheader("Analysis Results")
            
            # Text Issues
            st.write("### Text Analysis")
            for issue in recommendation["text_issues"]:
                st.warning(f"⚠️ {issue}")

            # Image Findings
            st.write("### Image Analysis")
            for i, findings in enumerate(recommendation["image_findings"]):
                st.image(images[i], caption=f"Photo {i+1}")
                for finding in findings:
                    st.info(f"📸 {finding}")

            # Financial Metrics
            st.write("### Financial Analysis")
            st.metric("Capitalization Rate", f"{recommendation['financial_metrics']['cap_rate']:.2f}%")
            st.metric("Risk Level", recommendation['financial_metrics']['risk_level'])

            # Voice Interaction
            st.write("### Ask DealSense")
            if st.button("🎤 Ask DealSense"):
                with st.spinner("Generating voice response..."):
                    try:
                        # Generate voice response
                        voice_response = vapi_client.generate_voice(
                            text=f"Based on the analysis, this property has a cap rate of {cap_rate:.2f}%. "
                                f"The risk level is {recommendation['financial_metrics']['risk_level']}. "
                                f"Key findings include: {', '.join(recommendation['text_issues'][:3])}",
                            voice_id="default"
                        )
                        st.audio(voice_response.audio_url)
                    except Exception as e:
                        st.error(f"Error generating voice response: {str(e)}")

            # Download Report
            if st.button("📥 Download Report"):
                report = {
                    "timestamp": datetime.now().isoformat(),
                    "analysis": recommendation
                }
                st.download_button(
                    label="Download JSON Report",
                    data=json.dumps(report, indent=2),
                    file_name="property_analysis_report.json",
                    mime="application/json"
                )

if __name__ == "__main__":
    main() 