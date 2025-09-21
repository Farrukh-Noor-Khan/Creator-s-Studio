import requests

url = "http://localhost:8000/generate"
payload = {"text": "api is working"}

response = requests.post(url, json=payload)
print(response.json())
