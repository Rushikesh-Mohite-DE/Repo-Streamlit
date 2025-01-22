import oracledb
import pandas as pd
import streamlit as st

# Streamlit app title
st.title("Fetch Data from Oracle Table")

# Hardcoded Oracle database connection details
dsn = "WS_2005_SR"  # Replace with your actual DSN
username = "WS_2005_SR"  # Replace with your actual username
password = "Dataentrega@2024"  # Replace with your actual password

# Hardcoded table name
table_name = "V_DE_WHRM_1002"  # Replace with the actual table name

# Button to fetch and display data
if st.button("Fetch Data"):
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
