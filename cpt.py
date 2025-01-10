import streamlit as st
import pyodbc
import pandas as pd

# Title of the app
st.title("SQL Server Data Fetcher")

# Sidebar inputs for database connection
st.sidebar.header("Database Connection Details")
server = st.sidebar.text_input("Server Name", "your_server_name")
database = st.sidebar.text_input("Database Name", "your_database_name")
username = st.sidebar.text_input("Username", "your_username")
password = st.sidebar.text_input("Password", type="password")
table_name = st.sidebar.text_input("Table Name", "your_table_name")

# Function to connect to SQL Server and fetch data
def fetch_data(server, database, username, password, table_name):
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password}",
            timeout=5  # Set a timeout value in seconds
        )
        query = f"SELECT * FROM {table_name}"
        data = pd.read_sql(query, conn)
        conn.close()
        return data
    except pyodbc.InterfaceError as ie:
        st.error(f"Interface Error: {ie}")
    except pyodbc.Error as e:
        st.error(f"Database Error: {e}")
    except Exception as e:
        st.error(f"Unexpected Error: {e}")
    return None


# Fetch and display data when the user clicks the button
if st.sidebar.button("Fetch Data"):
    if not (server and database and username and password and table_name):
        st.error("Please fill in all the fields.")
    else:
        st.info("Fetching data...")
        data = fetch_data(server, database, username, password, table_name)
        if data is not None:
            st.success("Data fetched successfully!")
            st.dataframe(data)
