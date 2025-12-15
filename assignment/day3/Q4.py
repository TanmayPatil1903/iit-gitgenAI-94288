import streamlit as st
import pandas as pd
import os
from datetime import datetime


# ------------------ CSV FILES ------------------
USERS_FILE = "users.csv"
FILES_HISTORY = "userfiles.csv"

# Create CSVs if not exists
if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USERS_FILE, index=False)

if not os.path.exists(FILES_HISTORY):
    pd.DataFrame(columns=["username", "filename", "datetime"]).to_csv(FILES_HISTORY, index=False)

# ------------------ SESSION STATE ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

# ------------------ FUNCTIONS ------------------
def register_user(username, password):
    users = pd.read_csv(USERS_FILE, dtype=str)

    username = username.strip()
    password = password.strip()

    if username in users["username"].values:
        return False

    users.loc[len(users)] = [username, password]
    users.to_csv(USERS_FILE, index=False)
    return True


def login_user(username, password):
    users = pd.read_csv(USERS_FILE, dtype=str)

    username = username.strip()
    password = password.strip()

    users["username"] = users["username"].str.strip()
    users["password"] = users["password"].str.strip()

    return not users[
        (users["username"] == username) &
        (users["password"] == password)
    ].empty


def save_upload_history(username, filename):
    history = pd.read_csv(FILES_HISTORY)
    history.loc[len(history)] = [username, filename, datetime.now()]
    history.to_csv(FILES_HISTORY, index=False)

# ------------------ SIDEBAR MENU ------------------
with st.sidebar:
    st.title("📌 Menu")

    if not st.session_state.logged_in:
        menu = st.radio("Navigation", ["Home", "Login", "Register"])
    else:
        menu = st.radio("Navigation", ["Explore CSV", "See History", "Logout"])

# ------------------ PAGES ------------------

# HOME
if menu == "Home":
    st.title("🏠 Home")
    st.write("Welcome to the CSV Explorer App")
    st.info("Please login or register to continue.")

# REGISTER
elif menu == "Register":
    st.title("📝 Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if register_user(username, password):
            st.success("Registration successful! Please login.")
        else:
            st.error("Username already exists.")

# LOGIN
elif menu == "Login":
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")

# EXPLORE CSV
elif menu == "Explore CSV":
    st.title("📂 Explore CSV")
    st.write(f"Logged in as *{st.session_state.username}*")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("CSV Preview")
        st.dataframe(df)

        save_upload_history(st.session_state.username, uploaded_file.name)
        st.success("Upload history saved!")

# SEE HISTORY
elif menu == "See History":
    st.title("📜 Upload History")

    history = pd.read_csv(FILES_HISTORY)
    user_history = history[history.username == st.session_state.username]

    if user_history.empty:
        st.info("No uploads found.")
    else:
        st.dataframe(user_history)

# LOGOUT
elif menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = None
    st.success("Logged out successfully!")
    st.rerun()