import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"  # Your local MySQL root password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS gts_dev")
            print("Database 'gts_dev' created successfully")
            
            # Use the database
            cursor.execute("USE gts_dev")
            
            # Set character set
            cursor.execute("ALTER DATABASE gts_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("Database character set configured")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    create_database()
