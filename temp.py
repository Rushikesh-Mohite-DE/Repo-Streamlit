import streamlit as st
import pyodbc

# Initialize connection.
@st.cache_resource
def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={st.secrets['server']};"
        f"DATABASE={st.secrets['database']};"
        f"UID={st.secrets['username']};"
        f"PWD={st.secrets['password']}"
    )

conn = init_connection()

# Function to run a query and fetch results
@st.cache_data(ttl=600)
def fetch_data(user_value):
    query = f"""
    SELECT *
    FROM DemoTable;
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

# Input for query parameter
user_value = st.text_input("Enter a value for column1:", "default_value")

# Call the fetch_data function and display results
if user_value:
    results = fetch_data(user_value)
    st.write("Query Results:")
    for result in results:
        st.write(f"Column1: {result[0]}, Column2: {result[1]}")
