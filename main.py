from fastapi import FastAPI
from db.chromadb_handler import get_collection, init_chromadb, insert_data_into_collection, load_data_from_json
from db.db import create_connection, create_table, insert_data_from_file


app = FastAPI()
# Path to your JSON file
data_file = './data/genzmarketing_cleaned_data.json'
# print(f"Loaded {len(data_file)} items from the JSON file.")

# Load data from JSON file
data = load_data_from_json(data_file)
print(f"Loaded {len(data)} items from the JSON file.")

create_connection()
create_table() # Create table (if it doesn't exist)

# Initialize ChromaDB client
client = init_chromadb()

collection = get_collection(client) # Get or create the collection
print("Collection created or fetched:", collection.name)

# Insert the data into ChromaDB
insert_data_into_collection(collection, data)  # Pass the loaded data
print("Data loaded from JSON file successfully!")

@app.get("/")
def read_root():
    return {"message": "Data inserted from the JSON file successfully!"}