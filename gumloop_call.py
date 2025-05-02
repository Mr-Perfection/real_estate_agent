import time

import requests

url = "https://api.gumloop.com/api/v1/start_pipeline"
user_id = "GOmsNcGoFfYWehO7H7LvKsWPkIe2"

payload = {
    "user_id": user_id,
    "saved_item_id": "f8o3ZHfQWw8WSxbwV3H76S",
    "pipeline_inputs": [{"input_name":"text","value":"$1,298,000\nStudio 1 ba1,400 sqft - House for sale"}]
}
headers = {
    "Authorization": "Bearer bef77c7707d9472cbaa4734ac1156688",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

data = response.json()
run_id = data["run_id"]

url = f"https://api.gumloop.com/api/v1/get_pl_run?run_id={run_id}&user_id={user_id}"
headers = {
    "Authorization": "Bearer bef77c7707d9472cbaa4734ac1156688"
}

while True:
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code != 200:
        raise Exception(f"error {response.status_code}")
    if data['state'] == 'RUNNING':
        time.sleep(1)
        continue
    if data['state'] == 'DONE':
        print(data['outputs']['output'])
        break
    raise Exception("Unknown state")
