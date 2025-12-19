import os
import requests
import json
import time
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

LOCAL_API_KEY = "dummy-key"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  

MODELS = {
    "Phi-3 Mini (Local)": {
        "model": "phi-3-mini-4k-instruct",
        "url": "http://127.0.0.1:1234/v1/chat/completions",
        "api_key": LOCAL_API_KEY
    },
    "LLaMA-3.3-70B (Groq)": {
        "model": "llama-3.3-70b-versatile",
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "api_key": GROQ_API_KEY
    }
}

st.sidebar.title("Settings")

selected_model_name = st.sidebar.selectbox(
    "Select Model",
    list(MODELS.keys())
)

model_config = MODELS[selected_model_name]

st.sidebar.markdown(f"""
*Model:* {model_config['model']}  
""")

if "messages" not in st.session_state:
    st.session_state.messages = {}

if selected_model_name not in st.session_state.messages:
    st.session_state.messages[selected_model_name] = []

st.title("chatbot AI")
st.toast("thanks for visiting")

def is_image_request(prompt):
    keywords = ["image", "draw", "generate picture", "photo"]
    return any(word in prompt.lower() for word in keywords)



for msg in st.session_state.messages[selected_model_name]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_prompt = st.chat_input("Ask anything...")

if user_prompt:

    st.session_state.messages[selected_model_name].append(
        {"role": "user", "content": user_prompt}
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        with st.spinner("Thinking..."):
            headers = {
                "Authorization": f"Bearer {model_config['api_key']}",
                "Content-Type": "application/json"
            }

            req_data = {
                "model": model_config["model"],
                "messages": [
                    {"role": "system", "content": "You are a lawyer."},
                    *st.session_state.messages[selected_model_name]
                ]
            }

            response = requests.post(
                model_config["url"],
                headers=headers,
                data=json.dumps(req_data)
            )

            resp = response.json()
            full_text = resp["choices"][0]["message"]["content"]

        streamed_text = ""
        for word in full_text.split():
            streamed_text += word + " "
            message_placeholder.markdown(streamed_text)
            time.sleep(0.04)

    st.session_state.messages[selected_model_name].append(
        {"role": "assistant", "content": full_text}
    )