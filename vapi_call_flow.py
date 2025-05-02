from vapi_client import VapiClient

# === Initialize Vapi Client ===
vapi = VapiClient()

# === Property Details ===
property_address = "123 Sunset Blvd, Los Angeles, CA"
roi = "12.5%"
risk_rating = "low"
team_name = "Propalyze AI"

# === Call Prompts ===
agent_prompt = f"""
Hi, I’m an AI assistant from {team_name}. We analyzed the property at {property_address} 
and rated it as a {risk_rating}-risk listing. Could you confirm its availability and provide any updates?
"""

investor_prompt = f"""
Hello! This is an AI assistant from {team_name}. We found a great investment property at {property_address} 
with an estimated ROI of {roi}. Would you like to receive a summary report or speak to an analyst?
"""

# === Target Phone Numbers (use your real mobile numbers to test) ===
real_estate_agent_number = "+16692121714"
investor_number = "+14156660123"

# === Trigger the Calls ===
vapi.create_call(real_estate_agent_number, agent_prompt, assistant_name="Real Estate AI Assistant")
vapi.create_call(investor_number, investor_prompt, assistant_name="Investor Opportunity Bot")
