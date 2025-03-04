import psycopg2
from psycopg2 import sql

from psycopg2 import OperationalError


# Define the connection parameters
"""
    Create and return a connection to the PostgreSQL database.
"""
def create_connection():
    try:
        connection = psycopg2.connect(
            dbname="advance_chatbot",  # replace with your database name
            user="postgres",        # replace with your username
            password="postgres",     # replace with your password
            host="localhost",             # or the appropriate host
            port="5432"                   # default port for PostgreSQL
        )
        print("Connection successful!")
        return connection
    except OperationalError as e:
        print(f"Error: {e}")
        return None
    # Closing the connection after use
        connection.close()

# Function to create the table if it doesn't exist
def create_table():
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS page_data (
                id SERIAL PRIMARY KEY,
                url TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(query)
            connection.commit()
            print("Table created successfully!")
        else:
            print("Connection to the database failed.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        if connection:
            connection.close()