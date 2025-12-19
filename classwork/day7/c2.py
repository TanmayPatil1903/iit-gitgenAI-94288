from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
import os
import pandas as pd
@tool
def calculator(expression):
    """
    This calculator function solves any arithmetic expression containing all constant values.
    It supports basic arithmetic operators +, -, *, /, and parenthesis. 
    
    :param expression: str input arithmetic expression
    :returns expression result as str
    instruction:
    give me the answer in one sentences
    """
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error: Cannot solve expression"
llm = init_chat_model(
    model = "llama-3.1-8b-instant",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("GROQ_API_KEY")
)
agent = create_agent(
            model=llm, 
            tools=[
                calculator
            ],
            system_prompt="You are a helpful assistant. Answer in short."
        )
while True:
    user_input = input("You: ")
    if user_input == "exit":
        break
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": user_input}
        ]
    })
    llm_output = result["messages"][-1]
    print("AI: ", llm_output.content)
    print("\n\n", result["messages"])