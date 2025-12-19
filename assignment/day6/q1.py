import streamlit as st
import pandas as pd
import duckdb
import os
from langchain.chat_models import init_chat_model

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="groq",
    api_key=os.getenv("GROQ_API_KEY")
)
st.title("CSV Explorer with LLM-Powered SQL")
st.write("Upload a CSV file, ask questions about it, and get SQL + explanations.")
uploaded = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded is not None:
    df = pd.read_csv(uploaded)
    st.success("CSV loaded successfully!")

    st.subheader("Schema")
    st.write(df.dtypes)
    con = duckdb.connect()
    con.register("data", df)

    st.subheader("Ask a Question About CSV")

    user_question = st.text_input("Enter your question")

    if user_question:
        llm_input = f"""
        Table Name: data
        Table Schema: {df.dtypes}

        Question: {user_question}

        Instruction:
        Write a SQL query for the above question.
        Generate SQL query only in plain text.
        If the question is not related to the table, output Error.
        """

        with st.spinner("Generating SQL query..."):
            sql_query = llm.invoke(llm_input).content.strip()

        st.code(sql_query, language="sql")

        if sql_query.lower() == "error":
            st.error("LLM could not generate a valid SQL query.")
        else:
            try:
                result_df = con.execute(sql_query).df()
                st.subheader("Query Result")
                st.dataframe(result_df)
                explain_prompt = f"""
                Explain the following SQL query result in simple English.

                User Question:
                {user_question}

                SQL Query:
                {sql_query}

                Result (first 10 rows):
                {result_df.head(10).to_string(index=False)}

                Instruction:
                Explain the result in plain English.
                """

                with st.spinner("Generating explanation..."):
                    explanation = llm.invoke(explain_prompt).content

                st.subheader("Explanation")
                st.write(explanation)

            except Exception as e:
                st.error(f"SQL Execution Error: {e}")
