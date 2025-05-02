# AI Real Estate Deal Analyzer

An AI-powered real estate deal analyzer that evaluates property listings and photos to provide financial analysis, risk assessment, and voice-interactive recommendations.

### Setup
```
python -m venv venv

# required for vapi: https://github.com/VapiAI/client-sdk-python
brew install portaudio

# Activate venv and install requirements
source venv/bin/activate && python -m pip install -r requirements.txt

```


### Let's go
```
streamlit run app.py
```

## Features

- Upload property listing text and photos
- AI-powered text analysis for risk detection
- Image analysis for property condition assessment
- Cap rate calculation and financial metrics
- Voice-interactive recommendations
- Downloadable analysis reports

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` with your API keys for VAPI and Gumloop

## Usage

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Open your browser to the provided local URL
3. Paste property listing text and upload photos
4. Click "Analyze Deal" to start the analysis
5. Use the "Ask DealSense" button for voice recommendations
6. Download the analysis report if needed

## API Integration

This application uses:
- VAPI for voice interaction
- Gumloop AI for text and image analysis

## Development

The application is built with:
- Streamlit for the frontend
- Python for backend processing
- Various AI APIs for analysis