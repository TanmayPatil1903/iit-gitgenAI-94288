import requests
import os
from dotenv import load_dotenv

load_dotenv()  

api_key = os.getenv("Weather_API")
city = input("Enter city: ")

try:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    print("status:", response.status_code)
    weather = response.json()

    print("Temperature: ", weather["main"]["temp"])
    print("Humidity: ", weather["main"]["humidity"])
    print("Wind Speed: ", weather["wind"]["speed"])

except Exception as e:
    print("some error occurred:", e)