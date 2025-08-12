import os
import mysql.connector
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
}

def init_database():
    try:
        # Connect to MySQL server without specifying a database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Create the database if it doesn't exist
        db_name = os.getenv('DB_NAME', 'restaurant_db')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created or already exists.")
        
        # Close the connection
        cursor.close()
        conn.close()
        
        print("Database initialization completed successfully.")
        print(f"You can now import the restaurant_db.sql file into your MySQL server using phpMyAdmin or the MySQL command line.")
        print("After importing, run 'python app.py' to start the application.")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print("\nTroubleshooting tips:")
        print("1. Make sure MySQL server is running (check XAMPP control panel)")
        print("2. Verify your database credentials in the .env file")
        print("3. Ensure you have the necessary permissions to create databases")

if __name__ == "__main__":
    print("Initializing Restaurant Management System database...")
    time.sleep(1)  # Small delay for better user experience
    init_database()