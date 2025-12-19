from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
import os
import pandas as pd
import requests

llm = init_chat_model(
    model = "llama-3.1-8b-instant",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("GROQ_API_KEY")
)

conversation = []
agent = create_agent(model=llm, tools=[],system_prompt = "you are a helpful assistant.Answer in details.")
while True:
    user_input = input("you:")
    if user_input == "exit":
        break
    conversation.append({"role":"user","content":user_input})
    result = agent.invoke({"messages":conversation})
    ai_msg = result["messages"][-1]
    print("AI:",ai_msg.content)
    conversation = result["messages"]