import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

req_data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        { "role": "system", "content": "You are experienced cricket commentator." },
        { "role": "user", "content": "who is M.S.dhoni?" },
    ],
}
response = requests.post(url, data=json.dumps(req_data), headers=headers)
print("Status:", response.status_code)

resp = response.json()
print(resp["choices"][0]["message"]["content"])