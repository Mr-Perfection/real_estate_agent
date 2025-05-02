import requests

class VapiClient:
    def __init__(self):
        self.api_key = "606dfd10-467d-43a5-bf2e-a7650079bdf0"  # 🔐 Use your real private API key here
        self.base_url = "https://api.vapi.ai"  # ✅ No /v1
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def create_call(self, phone_number, prompt, assistant_name="AI Assistant"):
        url = f"{self.base_url}/call"
        print("📞 FULL URL:", url)
        print("🔐 API KEY START:", self.api_key[:6] + "...")

        payload = {
            "customer": {
                "number": phone_number
            },
            "assistant": {
                "name": assistant_name,
                "firstMessage": prompt,
                "voice": {
                    "voiceId": "nova",
                    "provider": "azure"
                },
                "model": {
                    "model": "gpt-4",
                    "provider": "openai"
                },
                "transcriber": {
                    "provider": "deepgram"
                }
            },
            "phoneNumberId": "32dd50de-7880-4adb-b1d5-6954bd2a6ef5"  # 🔁 Replace this with your real number ID from Vapi dashboard
        }

        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code in [200, 202]:
            print(f"✅ Call to {phone_number} queued successfully.")
            print("🪄 Listen:", response.json().get("monitor", {}).get("listenUrl"))
            print("🎛 Control:", response.json().get("monitor", {}).get("controlUrl"))
        else:
            print(f"❌ Call failed:", response.text)

