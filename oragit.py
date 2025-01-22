import oracledb
import pandas as pd
import streamlit as st
import os
import requests

# Streamlit app title
st.title("Fetch Data from Oracle Table with GitHub-Hosted tnsnames.ora")

# GitHub raw file URL for tnsnames.ora
github_url = "https://raw.githubusercontent.com/Rushikesh-Mohite-DE/Repo-Streamlit/App/tnsnames.ora"  # Replace with your URL

# Local path to save tnsnames
local_tns_path = "/tmp/tnsnames.ora"  # Use a writable directory for the deployment environment

# Download tnsnames.ora from GitHub
try:
    response = requests.get(github_url)
    if response.status_code == 200:
        with open(local_tns_path, "w") as f:
            f.write(response.text)
        st.success("tnsnames.ora downloaded successfully.")
    else:
        st.error(f"Failed to download tnsnames.ora: {response.status_code}")
except Exception as e:
    st.error(f"Error downloading tnsnames.ora: {e}")

# Set TNS_ADMIN to the directory containing tnsnames.ora
os.environ["TNS_ADMIN"] = "/tmp"  # Adjust to the local path's directory

# Input fields for Oracle database connection details
username = st.text_input("Username", placeholder="Enter Username")
password = st.text_input("Password", placeholder="Enter Password", type="password")
dsn = st.text_input("DSN Name", placeholder="Enter DSN Name (from tnsnames.ora)")
table_name = st.text_input("Table Name", placeholder="Enter the table name to fetch data")

# Button to fetch and display data
if st.button("Fetch Data"):
    if not username or not password or not dsn or not table_name:
        st.error("Please provide all connection details and table name.")
    else:
        try:
            # Establish Oracle database connection
            conn = oracledb.connect(user=username, password=password, dsn=dsn)

            # Query to fetch data from the specified table
            query = f"SELECT * FROM {table_name}"

            # Execute the query and load data into a Pandas DataFrame
            df = pd.read_sql(query, conn)

            # Display data in the Streamlit app
            st.write(f"Fetched Data from {table_name}:")
            st.dataframe(df)

            # Close the connection
            conn.close()

        except Exception as e:
            st.error(f"An error occurred: {e}")
