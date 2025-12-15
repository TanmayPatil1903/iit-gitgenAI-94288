import streamlit as st
import requests

username = "darshan"
password = "1234"


if 'page' not in st.session_state:
    st.session_state.page = "login"


def login_page():
    st.header("Login Page")
    st.write("Please enter your credentials to login.")

    Name = st.text_input("Enter username")
    Pass = st.text_input("Enter password", type='password')

    if st.button("Login", type="primary"):
        if username == Name and password == Pass:
            st.success("Login Successful")
            st.session_state.page = "weather"
            st.rerun()
        else:
            st.error("Invalid Credentials")


def weather_app():
    st.header("🌤 Weather App")
    st.write("Welcome to the Weather App!")

    api_key = "56c6a94b317556f571753e1d2681b8c1"
    city = st.text_input("Enter city")

    if city:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            weather = response.json()

            if weather.get("cod") != 200:
                st.error("City not found")
            else:
                st.write("🌡 Temperature:", weather["main"]["temp"], "°C")
                st.write("💧 Humidity:", weather["main"]["humidity"], "%")
                st.write("🌬 Wind Speed:", weather["wind"]["speed"], "m/s")
        except:
            st.error("Some error occurred")

    if st.button("Logout", type="primary"):
        st.session_state.page = "login"
        st.toast("You have been logged out")
        st.rerun()


if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "weather":
    weather_app()