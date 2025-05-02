from vapi_client import VapiClient

def initiate_vapi_call(call_type="agent"):
    """
    Initiates a Vapi call to either a real estate agent or investor.

    Args:
        call_type (str): 'agent' or 'investor'

    Returns:
        (bool, str): Tuple of (success status, message)
    """
    try:
        # Initialize Vapi Client
        vapi = VapiClient()

        # Property details
        property_address = "123 Sunset Blvd, Los Angeles, CA"
        roi = "12.5%"
        risk_rating = "low"
        team_name = "Propalyze AI"

        # Prompts
        agent_prompt = f"""
        Hi, I’m an AI assistant from {team_name}. We analyzed the property at {property_address} 
        and rated it as a {risk_rating}-risk listing. Could you confirm its availability and provide any updates?
        """

        investor_prompt = f"""
        Hello! This is an AI assistant from {team_name}. We found a great investment property at {property_address} 
        with an estimated ROI of {roi}. Would you like to receive a summary report or speak to an analyst?
        """

        # Phone numbers
        real_estate_agent_number = "+14242122846"
        investor_number = "+14156660123"

        # Call based on type
        if call_type == "agent":
            vapi.create_call(real_estate_agent_number, agent_prompt, assistant_name="Real Estate AI Assistant")
            return True, "Calling the real estate agent..."
        elif call_type == "investor":
            vapi.create_call(investor_number, investor_prompt, assistant_name="Investor Opportunity Bot")
            return True, "Calling the investor..."
        else:
            return False, "Invalid call type."

    except Exception as e:
        import traceback
        traceback.print_exc()
        return False, f"Call failed: {str(e)}"
