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

def create_data_tables():
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            
            # Create the queries and responses tables
            query = """
            CREATE TABLE IF NOT EXISTS queries (
                id SERIAL PRIMARY KEY,
                question TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS responses (
                id SERIAL PRIMARY KEY,
                query_id INT REFERENCES queries(id),
                response TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(query)
            connection.commit()
            print("Tables created successfully!")
        else:
            print("Connection not established.")
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        if connection:
            connection.close()
