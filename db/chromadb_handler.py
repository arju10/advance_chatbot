import json
from typing import List
import uuid
import chromadb
from sentence_transformers import SentenceTransformer


# Connect to the ChromaDB client
def init_chromadb():
    # Initialize ChromaDB client with new configuration method
    client = chromadb.Client()
    return client

# Create or fetch a collection in ChromaDB
def get_collection(client, collection_name="question_answers"):
    # Try to get the collection, or create it if it doesn't exist
    try:
        collection = client.get_collection(name=collection_name)
    except chromadb.errors.InvalidCollectionException:
        # Create collection if it doesn't exist
        collection = client.create_collection(name=collection_name)
    return collection

# Load data from a JSON file
def load_data_from_json(file_path: str):
    """Load data from a JSON file and ensure the structure is a list of dictionaries."""
    with open(file_path, "r") as file:
        data = json.load(file)
    #  Print the type and first few entries of the data
        # print(f"Data type: {type(data)}")
        # print(f"First entry: {data[0] if data else 'No data'}")
        # print(f"Full data sample: {data[:5]}")  # Print the first 5 entries to inspect

    # Ensure it's a list of dictionaries
    if not isinstance(data, list):
        raise ValueError("Expected a list of dictionaries in the JSON file.")
    
    return data

# Insert data into the ChromaDB collection
def insert_data_into_collection(collection, data: List[dict]):
    """Insert the data into the ChromaDB collection"""
    if not isinstance(data, list):
        raise ValueError("Data should be a list of dictionaries.")

    documents = []
    ids = []  # Initialize a list to hold the document IDs
    for item in data:
        if isinstance(item, dict):
            # Combine the fields 'title', 'url', and 'content' into a single string
            document = f"Title: {item.get('title', '')}\nURL: {item.get('url', '')}\nContent: {item.get('content', '')}"
            documents.append(document)
            # Generate a unique ID for each document
            ids.append(str(uuid.uuid4()))  # Use UUID to generate a unique ID
        else:
            print(f"Skipping invalid item: {item}")

    # Add the documents to the collection
    if documents:
        collection.add(documents=documents, ids=ids)
        print(f"Inserted {len(documents)} documents into the chromadb collection.")
    else:
        print("No valid documents to insert.")

# Document based search
# Query the ChromaDB collection
def query_collection(collection, query: str, limit: int = 5):
    """Query the collection with a search string."""
    # Query the collection for matching documents
    results = collection.query(query_texts=[query], n_results=limit)
    return results['documents']


# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text: str):
    """Generate a vector embedding for the input text."""
    return model.encode(text)
# Embedding based search -> Use embeddings for search for better results instead of document based search
def embadding_query_collection(collection, query_embedding: List[float], limit: int = 5):
    """Query the collection with a search embedding."""
    # Query the collection for matching documents using embeddings
    results = collection.query(query_embeddings=[query_embedding], n_results=limit)
    return results['documents']
