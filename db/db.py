import json
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve database credentials from environment variables
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Define the connection parameters
def create_connection():
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Connection successful!")
        return connection
    except OperationalError as e:
        print(f"Error: {e}")
        return None

# Function to create the table if it doesn't exist
def create_table():
    connection = None
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
            print("Table created successfully! in the database")
        else:
            print("Connection to the database failed.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        if connection:
            connection.close()  # Close the connection manually after the operation

# Function to insert data into the table from a JSON file
def insert_data_from_file(file_path):
    connection = None
    try:
        # Load JSON data from file
        with open(file_path, 'r') as file:
            json_data = json.load(file)

        connection = create_connection()
        if connection:
            cursor = connection.cursor()

            data_to_insert = []
            for entry in json_data:
                # Check for required fields before adding to the batch
                if 'title' in entry and 'url' in entry and 'content' in entry:
                    data_to_insert.append((entry['title'], entry['url'], entry['content']))
                else:
                    print(f"Skipping invalid entry: {entry}")

            if data_to_insert:
                query = """
                INSERT INTO page_data (title, url, content)
                VALUES (%s, %s, %s);
                """
                cursor.executemany(query, data_to_insert)

                connection.commit()
                print(f"Data from {file_path} inserted successfully!")
            else:
                print("No valid data to insert.")
        else:
            print("Connection to the database failed.")
    except Exception as e:
        print(f"Error inserting data from file: {e}")
    finally:
        if connection:
            connection.close()  # Close the connection manually after the operation



'''
Neccesseary commands
psql -U your_user_name -h localhost
psql -U your_user_name -h localhost -d your_database_name
uvicorn main:app --reload

'''