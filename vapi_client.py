import requests

class VapiClient:
    def __init__(self):
        self.api_key = "606dfd10-467d-43a5-bf2e-a7650079bdf0"  # Replace with your actual API key
        self.phone_number_id = "06625064-2114-4c8b-90ac-8433f9daac3d"  # Your real phone number ID from Vapi 
        self.base_url = "https://api.vapi.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def create_call(self, phone_number, prompt, assistant_name="AI Assistant"):
        url = f"{self.base_url}/call"
        print("📞 FULL URL:", url)
        print("🔐 API KEY START:", self.api_key[:6] + "...")

        # ✅ Recommended: Use OpenAI's 'echo' voice for reliability
        payload = {
            "customer": {
                "number": phone_number
            },
            "assistant": {
                "name": assistant_name,
                "firstMessage": prompt,
                "voice": {
                    "provider": "openai",
                    "voiceId": "echo"
                },
                "model": {
                    "provider": "openai",
                    "model": "gpt-3.5-turbo"
                },
                "transcriber": {
                    "provider": "deepgram"
                }
            },
            "phoneNumberId": self.phone_number_id
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            if response.status_code in [200, 202]:
                print(f"✅ Call to {phone_number} queued successfully.")
                monitor = response.json().get("monitor", {})
                print("🪄 Listen:", monitor.get("listenUrl"))
                print("🎛 Control:", monitor.get("controlUrl"))
                return True, "Call successfully queued."
            else:
                print(f"❌ Call failed:", response.text)
                return False, f"Call failed: {response.text}"
        except Exception as e:
            print(f"❌ Exception during call:", str(e))
            return False, f"Exception during call: {str(e)}"
