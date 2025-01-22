import streamlit as st
import oracledb


ORACLE_HOST = "adb.ap-mumbai-1.oraclecloud.com"  # Replace with your Oracle DB host
ORACLE_PORT = "1522"           # Replace with your Oracle DB port
ORACLE_SERVICE_NAME = "g10916f2e32ac91_dataentrega_high.adb.oraclecloud.com"  # Replace with your service name
ORACLE_USERNAME = "DE_ORA_CLOUD_ADMIN"          # Replace with your username
ORACLE_PASSWORD = "Melbourne@2025"          # Replace with your password

def connect_to_oracle():
    """Connect to Oracle Database using oracledb in thin mode."""
    try:
        connection = oracledb.connect(
            user=ORACLE_USERNAME,
            password=ORACLE_PASSWORD,
            dsn=f"{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE_NAME}",
            mode=oracledb.DEFAULT_AUTH
        )
        return connection
    except oracledb.DatabaseError as e:
        st.error(f"Error connecting to Oracle: {e}")
        return None

def main():
    st.title("Oracle Cloud Database Access")
    
    if st.button("Connect to Oracle"):
        connection = connect_to_oracle()
        
        if connection:
            st.success("Successfully connected to Oracle Database!")
            
            # Execute a simple query
            query = "SELECT * FROM DUAL"
            st.write(f"Executing query: {query}")
            
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()
                    st.write("Query Result:", result)
            except oracledb.DatabaseError as e:
                st.error(f"Error executing query: {e}")
            finally:
                connection.close()
        else:
            st.error("Failed to connect to Oracle Database.")

if __name__ == "__main__":
    main()

