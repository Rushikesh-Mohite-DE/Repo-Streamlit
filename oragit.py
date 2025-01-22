import oracledb
import pandas as pd
import streamlit as st
import os

# Streamlit app title
st.title("Fetch Data from Oracle Table")

# TNS data (inline within the script)
tns_data = """
WS_2005_SR = 
  (DESCRIPTION = 
    (ADDRESS = (PROTOCOL = TCPS)(HOST = adb.ap-mumbai-1.oraclecloud.com)(PORT = 1522))
    (CONNECT_DATA = 
      (SERVICE_NAME = g10916f2e32ac91_dataentrega_high.adb.oraclecloud.com)
    )
  )
"""

# Local path to save the tnsnames.ora file
local_tns_path = "D:\\Oracle\\Wallet_DATAENTREGA\\tnsnames.ora"  # Adjust path as needed

# Write TNS data to the file
try:
    with open(local_tns_path, "w") as f:
        f.write(tns_data)
    st.success("tnsnames.ora created successfully.")
except Exception as e:
    st.error(f"Failed to create tnsnames.ora: {e}")

# Set TNS_ADMIN to the directory containing tnsnames.ora
os.environ["TNS_ADMIN"] = os.path.dirname(local_tns_path)

# Database connection details
dsn = "WS_2005_SR"  # TNS alias
username = "WS_2005_SR"  # Replace with your username
password = "Dataentrega@2024"  # Replace with your password

# Hardcoded table name
table_name = "V_DE_WHRM_1002"  # Replace with your actual table name

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
