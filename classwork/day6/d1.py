from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import os

api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="openai/gpt-oss-120b", api_key=api_key)

user_input = input("You: ")
result = llm.stream(user_input)
for chunk in result:
    print(chunk.content, end="")