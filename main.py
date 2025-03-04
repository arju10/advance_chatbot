from fastapi import FastAPI
from db.chromadb_handler import get_collection, init_chromadb
from db.db import create_connection, create_table, insert_data_from_file


app = FastAPI()
# Path to your JSON file
data_file = './data/genzmarketing_cleaned_data.json'

create_connection()
# Create table (if it doesn't exist)
create_table()

# Insert the data from the JSON file into the database
insert_data_from_file(data_file)

# Initialize ChromaDB
client = init_chromadb()

# Get or create the collection
collection = get_collection(client)

# Check if the collection is created successfully
print("Collection created or fetched:", collection.name)

@app.get("/")
def read_root():
    return {"message": "Data inserted from the JSON file successfully!"}