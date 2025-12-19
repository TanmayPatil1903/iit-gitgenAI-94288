from langchain.chat_models import init_chat_model
import os
import pandas as pd
import duckdb
import requests
import streamlit as st

st.title("Weather check Chatbot ")

llm = init_chat_model(
    model = "llama-3.1-8b-instant",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("GROQ_API_KEY")
)
user_input = st.chat_input("Enter the name of the city...")
if user_input:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        st.subheader(f"📍 Weather in {user_input}")
        st.write(f"Temperature: {data['main']['temp']} °C")
        st.write(f"Feels Like: {data['main']['feels_like']} °C")
        st.write(f"Humidity: {data['main']['humidity']} %")
        st.write(f"Condition: {data['weather'][0]['description'].title()}")
    else:
        st.write(None)

    explain_prompt = f"""
    Explain the following  result in simple English.
    In this explain the weather condition currently that the city has for the given city  {user_input}
    and using {data} 
    """

    explanation = llm.invoke(explain_prompt).content
    st.write("\nExplanation:")
    st.write(explanation)