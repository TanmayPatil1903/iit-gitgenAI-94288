import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
headers = {
    "Authorization":f"Bearer {api_key}",
    "Content-Type":"application/json"
}

user_promt = input("Enter your promt:")
req_data = {
    "model":"llama-3.3-70b-versatile",
    "messages":[
        {"role":"user","content":user_promt}
    ],
}

response = requests.post(url,data = json.dumps(req_data),headers = headers)
print("Status:",response.status_code)
print(response.json())