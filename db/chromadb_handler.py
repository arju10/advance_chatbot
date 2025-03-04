# chromadb_client.py
import chromadb

def init_chromadb():
    # Initialize ChromaDB client with new configuration method
    client = chromadb.Client()
    return client

def get_collection(client, collection_name="question_answers"):
    # Try to get the collection, or create it if it doesn't exist
    try:
        collection = client.get_collection(name=collection_name)
    except chromadb.errors.InvalidCollectionException:
        # Create collection if it doesn't exist
        collection = client.create_collection(name=collection_name)
    return collection
