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
server = st.sidebar.text_input("SERVER", value="DESKTOP-RCE6E1O")
database = st.sidebar.text_input("DATABASE", value="DE_MIGR_DB")
username = st.sidebar.text_input("UID", value="test1")
password = st.sidebar.text_input("PWD", value="cls", type="password")

st.sidebar.header("Table Selection")
table_name = st.sidebar.text_input("Table Name", value="DemoTable")

# Button to fetch data
if st.sidebar.button("Fetch Data and Upload to Google Drive"):
    try:
        # Construct connection string
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password}"
        )

        # Connect to the database
        st.info("Connecting to SQL Server...")
        conn = pyodbc.connect(connection_string)

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
        access_token = "YOUR_ACTUAL_ACCESS_TOKEN_HERE"  # Replace with your actual token
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        # Metadata
        para = {
            "name": csv_file,
        }

        # Open the CSV file to upload
        with open(csv_file, "rb") as file_data:
            files = {
                'data': ('metadata', json.dumps(para), 'application/json'),
                'file': file_data
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

    except pyodbc.Error as db_err:
        st.error(f"Database error: {db_err}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

    # Cleanup
    finally:
        if os.path.exists(csv_file):
            os.remove(csv_file)
