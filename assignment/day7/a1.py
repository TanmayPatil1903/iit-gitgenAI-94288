from langchain.agents import create_agent
from langchain.tools import tool
from langchain.chat_models import init_chat_model
import requests
import json
import os
from langchain.agents.middleware  import wrap_model_call


@wrap_model_call
def model_logging(request,handler):
    print("Before model call ",'-' *20)
    #print request
    response = handler(request)
    print("After the model call ",'-'*20)
    #print response
    response.result[0].content = response.result[0].content.upper()
    return response

@wrap_model_call
def limit_model_context(request, handler):
    print("* Before model call: ", '-' * 20)
    # print request
    request.messages = request.messages[-5:]
    response = handler(request)
    print("* After model call: ", '-' * 20)
    # print response
    response.result[0].content = response.result[0].content.upper()
    return response

@tool
def calculator(expression):
    """
    This calculator function solves any arithmetic expression containing all constant values.
    It supports basic arithmetic operators +, -, *, /, and parenthesis. 
    
    :param expression: str input arithmetic expression
    :returns expression result as str
    """
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error: Connot solve expression"

@tool  
def get_weather(city):
    """
    This get_weather() function gets the current weather of given city.
    If weather cannot be found, it returns 'Error'.
    This function doesn't return historic or general weather of the city.

    :param city: str input - city name
    :returns current weather in json format or 'Error'
    """
    try:
        api_key = os.getenv("WEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=metric&q={city}" 
        response = requests.get(url)
        weather = response.json()
        return json.dumps(weather)
    except:
        return "Error"
    
@tool
def read_file(filepath):
    """
    Docstring for read_file
    
    :param filepath: Description
    """
    with open(filepath,'r') as file:
        text = file.read()
        return text
@tool
def knowledge_lookup(question):
    """
    Give information about the input question.
    
    Args:
        question (str): The question provided by the user.
    """

llm = init_chat_model(
    model = "phi-3-mini-4k-instruct",
    model_provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "non-needed"
)

agent = create_agent(
    model = llm,
    tools=[calculator,get_weather,read_file,knowledge_lookup],
    middleware=[model_logging,limit_model_context],
    system_prompt="You are a helpful assistant.Answer in short."
)

while True:
    user_input = input("\n\n You : ")
    if user_input == "exit":
        break
    result =  agent.invoke({
        "messages":[{
            "role":"user","content":user_input
        }]
    })

    llm_output = result["messages"][-1]
    print("AI: ",llm_output.content)
    print("\n\n ",result)