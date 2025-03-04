from fastapi import FastAPI
from db.chromadb_handler import embadding_query_collection, get_collection, get_embedding, init_chromadb, insert_data_into_collection, load_data_from_json, query_collection
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
insert_data_from_file(data_file)  # Insert data into the table from the JSON file

# Initialize ChromaDB client
client = init_chromadb()

collection = get_collection(client) # Get or create the collection
print("Collection created or fetched:", collection.name)

# Insert the data into ChromaDB
insert_data_into_collection(collection, data)  # Pass the loaded data
print("Data loaded from JSON file successfully!")


# Document based search
@app.get("/search/")
def search(query: str, limit: int = 5):
    """Search for documents based on a query string."""
    results = query_collection(collection, query, limit)
    return {"results": results}

# Embedding based search
@app.get("/search/")
def search(query: str, limit: int = 5):
    """Search for documents based on a query string using embeddings."""
    query_embedding = get_embedding(query)  # Get the query's embedding
    results = embadding_query_collection(collection, query_embedding, limit)  # Pass the embedding to the query function
    return {"results": results}

@app.get("/")
def read_root():
    return {"message": "Data inserted from the JSON file successfully!"}
