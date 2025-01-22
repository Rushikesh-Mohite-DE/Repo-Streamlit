import oracledb

# Initialize Oracle client using the wallet and configuration
oracledb.init_oracle_client(wallet_location="App/Wallet_DATAENTREGA")  # Direct wallet location

# Now you can proceed with your database operations
try:
    # Example: Connect to the Oracle database
    connection = oracledb.connect(
        user="your_username",
        password="your_password",
        dsn="your_dsn"
    )

    # Example: Cursor execution
    cursor = connection.cursor()

    # Execute a simple query
    cursor.execute("SELECT * FROM your_table_name")

    # Fetch results
    rows = cursor.fetchall()

    for row in rows:
        print(row)

except oracledb.Error as e:
    print("Oracle Database error:", e)

finally:
    if connection:
        connection.close()
