import streamlit as st
import oracledb

# Oracle Database credentials (hardcoded for cloud deployment)
ORACLE_USERNAME = "DE_ORA_CLOUD_ADMIN"
ORACLE_PASSWORD = "Melbourne@2025"
ORACLE_DSN = "adb.ap-mumbai-1.oraclecloud.com:1522/g10916f2e32ac91_dataentrega_high.adb.oraclecloud.com"

# Initialize Oracle client with wallet path stored in GitHub repository
oracledb.init_oracle_client(config_dir="App/Wallet_DATAENTREGA")  # Path to wallet in GitHub repository

# Connect to Oracle Cloud Database
try:
    connection = oracledb.connect(
        user=ORACLE_USERNAME,
        password=ORACLE_PASSWORD,
        dsn=ORACLE_DSN
    )
    st.write("Connected to Oracle Cloud DB successfully!")
    
    # Example query - replace with your actual query
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM your_table_name")  # Replace with your actual table
    rows = cursor.fetchall()

    for row in rows:
        st.write(row)

except oracledb.Error as e:
    st.error(f"Error connecting to Oracle: {e}")

finally:
    if 'connection' in locals() or 'connection' in globals():
        connection.close()
