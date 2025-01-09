import streamlit as st
import pyodbc
import pandas as pd

# Streamlit app title
st.title("SQL Server Data Fetch")

# Sidebar for input fields
st.sidebar.header("SQL Server Connection Details")
server = st.sidebar.text_input("Server Address", value="DESKTOP-RCE6E1O")
database = st.sidebar.text_input("Database Name", value="DE_MIGR_DB")
username = st.sidebar.text_input("Username", value="test1")
password = st.sidebar.text_input("Password", value="cls", type="password")

st.sidebar.header("Table Selection")
table_name = st.sidebar.text_input("Table Name", value="DemoTable")

# Button to fetch data
if st.sidebar.button("Fetch Data"):
    try:
        # Establish pyodbc connection
        connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        conn = pyodbc.connect(connection_string)

        # Fetch data
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)

        # Close the connection
        conn.close()

        # Display data
        st.write("Fetched Data:")
        st.dataframe(df)

        # Save data to a CSV file
        csv_file = f"{table_name}.csv"
        df.to_csv(csv_file, index=False)
        st.success(f"Data saved to {csv_file}")

    except Exception as e:
        st.error(f"An error occurred: {e}")