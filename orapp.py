import oracledb

# Initialize Oracle client using the wallet and configuration
oracledb.init_oracle_client(config_dir="App/Wallet_DATAENTREGA", 
                            wallet_location="App/Wallet_DATAENTREGA/ewallet.p12", 
                            private_key_password="Melbourne@2025")  # Replace with your actual password

ORACLE_DSN = "adb.ap-mumbai-1.oraclecloud.com:1522/g10916f2e32ac91_dataentrega_high.adb.oraclecloud.com"
ORACLE_USERNAME = "DE_ORA_CLOUD_ADMIN"
ORACLE_PASSWORD = "Melbourne@2025"

# Connect to Oracle Cloud Database
try:
    connection = oracledb.connect(
        user=ORACLE_USERNAME,
        password=ORACLE_PASSWORD,
        dsn=ORACLE_DSN
    )
    print("Connected to Oracle Cloud DB successfully!")
    
    # Example query - replace with your actual query
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM your_table_name")  # Replace with your actual table
    rows = cursor.fetchall()

    for row in rows:
        print(row)

except oracledb.Error as e:
    print(f"Error connecting to Oracle: {e}")

finally:
    if 'connection' in locals() or 'connection' in globals():
        connection.close()
