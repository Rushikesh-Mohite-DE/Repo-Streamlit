import streamlit as st
import oracledb
import os

# Load Oracle credentials and wallet path from GitHub Secrets
wallet_path = os.getenv("ORACLE_WALLET_PATH", "/default/path/to/your/wallet")
oracle_username = os.getenv("ORACLE_USERNAME", "DE_ORA_CLOUD_ADMIN")
oracle_password = os.getenv("ORACLE_PASSWORD", "Melbourne@2025")
oracle_dsn = os.getenv("ORACLE_DSN", "adb.ap-mumbai-1.oraclecloud.com:1522/g10916f2e32ac91_dataentrega_high.adb.oraclecloud.com")

# Initialize Oracle client with wallet path
oracledb.init_oracle_client(config_dir=wallet_path)

# Connect to Oracle Cloud Database
try:
    connection = oracledb.connect(
        user=oracle_username,
        password=oracle_password,
        dsn=oracle_dsn
    )
    st.write("Connected to Oracle Cloud DB successfully!")
    
    # Example query - replace this with your actual query
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM your_table_name")
    rows = cursor.fetchall()

    for row in rows:
        st.write(row)

except oracledb.Error as e:
    st.error(f"Error connecting to Oracle: {e}")

finally:
    if 'connection' in locals() or 'connection' in globals():
        connection.close()
