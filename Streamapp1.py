import streamlit as st
import pyodbc
import pandas as pd
import json
import requests
import os

# Streamlit app title
st.title("SQL Server Data Fetch and Google Drive Upload")

# Sidebar for input fields
st.sidebar.header("SQL Server Connection Details")
server = st.sidebar.text_input("Server Address", value=st.secrets.get("sql", {}).get("server", ""))
database = st.sidebar.text_input("Database Name", value=st.secrets.get("sql", {}).get("database", ""))
username = st.sidebar.text_input("Username", value=st.secrets.get("sql", {}).get("username", ""))
password = st.sidebar.text_input("Password", value=st.secrets.get("sql", {}).get("password", ""), type="password")

st.sidebar.header("Table Selection")
table_name = st.sidebar.text_input("Table Name", value="DemoTable")

# Button to fetch data
if st.sidebar.button("Fetch Data and Upload to Google Drive"):
    try:
        # Establish pyodbc connection
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};DATABASE={database};UID={username};PWD={password};"
            f"Connection Timeout=30;"
        )
        st.write("Attempting to connect to the database...")

        try:
            conn = pyodbc.connect(connection_string)
            st.success("Connected to the database successfully.")
        except pyodbc.Error as db_error:
            st.error(f"Database connection failed: {db_error}")
            raise

        # Fetch data
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)

        # Close the connection
        conn.close()

        # Display data
        st.write("Fetched Data:")
        st.dataframe(df)

        # Save data to a CSV file locally
        csv_file = f"{table_name}.csv"
        df.to_csv(csv_file, index=False)
        st.success(f"Data saved to {csv_file}")

        # Google Drive Upload - Replace with your access token
        access_token = st.secrets.get("google_drive", {}).get("access_token", "")
        if not access_token:
            st.error("Google Drive access token is missing. Please add it to your secrets file.")
            raise ValueError("Missing Google Drive access token.")

        headers = {"Authorization": f"Bearer {access_token}"}

        # Metadata
        para = {"name": csv_file}

        # Open the CSV file to upload
        files = {
            'data': ('metadata', json.dumps(para), 'application/json'),
            'file': open(csv_file, "rb")
        }

        # Upload file to Google Drive
        response = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers=headers,
            files=files
        )

        # Handling the response
        if response.status_code == 200:
            st.success("File uploaded successfully to Google Drive.")
            st.json(response.json())
        else:
            st.error(f"Failed to upload file: {response.status_code}, {response.text}")

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.stop()

# Debugging: Check environment details
if st.sidebar.checkbox("Show Debug Info"):
    st.write("Environment Variables:")
    st.json(dict(os.environ))
