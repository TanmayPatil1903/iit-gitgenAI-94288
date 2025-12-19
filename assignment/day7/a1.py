from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool 
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

@tool 
def calculator(expression):
    """
    This calculator function solves any arithmatic expression containing all constant values.
    It supports basic arithmatic operators +,-,*,/, and parenthesis.
    
    :param expression: str input arithmatic expression 
    :returns expression result as str
    """
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error:cannot solve expression"
    
@tool 
def get_weather(city):
    """ This get_weather() function gets the current weather of given city.
    If weather cannot be found, it returns 'Error'.
    This function doesn't return historic or general weather of the city.

    :param city: str input - city name
    :returns current weather in json format or 'Error'
    """
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=metric&q={city}"
        response = requests.get(url)
        weather = response.json()
        return json.dumps(weather)
    except:
        return "Error"

@tool
def read_file(filepath: str):
    """
    Reads text files
    """
    try:
        with open(filepath, "r") as file:
            return file.read()
    except:
        return "File not found"

@tool    
def knowledge_lookup(query: str):
    """
    Fetches summary from Wikipedia
    """
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        response = requests.get(url)
        data = response.json()
        return data.get("extract", "No data found")
    except:
        return "Error fetching knowledge"

llm = init_chat_model(
    model = "google/gemma-3-4b",
    model_provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "non-needed"
)
agent = create_agent(
            model=llm, 
            tools=[
                calculator,
                get_weather
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
            