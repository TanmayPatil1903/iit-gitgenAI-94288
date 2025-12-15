import pandas as pd
import streamlit as st
import pandasql as ps

st.title("CSV file print")

data_file = st.file_uploader("Upload a CSV file", type=["csv"])

if data_file:
    df = pd.read_csv(data_file)
    query = st.text_input("Enter your query")
    if query:
        result = ps.sqldf(query, {"data": df})
        st.dataframe(result)