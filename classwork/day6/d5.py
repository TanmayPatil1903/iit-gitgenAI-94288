from langchain.chat_models import init_chat_model
import os
import pandas as pd
import duckdb   
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="groq",
    api_key=os.getenv("GROQ_API_KEY")
)
csv_file = input("Enter path of a CSV file: ")
df = pd.read_csv(csv_file)
print("\nCSV schema:")
print(df.dtypes)
con = duckdb.connect()
con.register("data", df)
while True:
    user_input = input("\nAsk anything about this CSV? ")
    if user_input.lower() == "exit":
        break

    llm_input = f"""
Table Name: data
Table Schema: {df.dtypes}

Question: {user_input}

Instruction:
Write a SQL query for the above question.
Generate SQL query only in plain text.
If the question is not related to the table, output Error.
"""

    sql_response = llm.invoke(llm_input).content.strip()
    print("\nGenerated SQL:")
    print(sql_response)

    if sql_response.lower() == "error":
        print("LLM could not generate a valid SQL query.")
        continue
    try:
        result_df = con.execute(sql_response).df()
        print("\nQuery Result:")
        print(result_df)

    except Exception as e:
        print("SQL Execution Error:", e)
        continue
    explain_prompt = f"""
Explain the following SQL query result in simple English.

User Question:
{user_input}

SQL Query:
{sql_response}

Result (first 10 rows):
{result_df.head(10).to_string(index=False)}

Instruction:
Explain the result in english
"""

    explanation = llm.invoke(explain_prompt).content
    print("\nExplanation:")
    print(explanation)
