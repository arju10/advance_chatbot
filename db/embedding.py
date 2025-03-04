# Initialize the sentence transformer model
from typing import List
from sentence_transformers import SentenceTransformer


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
