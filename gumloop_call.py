import requests

url = "https://api.gumloop.com/api/v1/start_pipeline"

payload = {
  "user_id": "GOmsNcGoFfYWehO7H7LvKsWPkIe2",
  "saved_item_id": "f8o3ZHfQWw8WSxbwV3H76S",
  "pipeline_inputs": [{"input_name":"query","value":"90210"}]
}
headers = {
  "Authorization": "Bearer [INSERT GUMLOOP API KEY HERE, GENERATE FROM https://gumloop.com/credentials]",
  "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
