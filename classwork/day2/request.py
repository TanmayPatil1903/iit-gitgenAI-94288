import requests
api_key="56c6a94b317556f571753e1d2681b8c1"
city = input("Enter city: ")

try:
  url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metirc"
  response = requests.get(url)
  print("status:", response.status_code)
  weather = response.json()
# print(weather)
  print("Temperature: ", weather["main"]["temp"])
  print("Humidity: ", weather["main"]["humidity"])
  print("Wind Speed: ", weather["wind"]["speed"])
except:
  print("some error occured")