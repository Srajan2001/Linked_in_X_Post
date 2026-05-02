import chromadb
import uuid
import os

# Ensure the memory directory exists
os.makedirs("memory/vectordb", exist_ok=True)

# Initialize local ChromaDB (saves to your hard drive)
chroma_client = chromadb.PersistentClient(path="./memory/vectordb")

# This creates a database collection. It automatically uses a free, local embedding model!
collection = chroma_client.get_or_create_collection(name="linkedin_posts")

def save_to_memory(post_text, topic):
    """Saves an approved post into the vector database."""
    collection.add(
        documents=[post_text],
        metadatas=[{"topic": topic}],
        ids=[str(uuid.uuid4())]
    )
    print("Post saved to long-term vector memory!")

def retrieve_past_posts(current_topic, n_results=2):
    """Fetches the most relevant past posts based on the current topic."""
    if collection.count() == 0:
        return "" # No memories exist yet
    
    # Query the database for posts similar to the current topic
    results = collection.query(
        query_texts=[current_topic],
        n_results=min(n_results, collection.count())
    )
    
    past_posts = results['documents'][0]
    
    # Format the past posts into a single string for the prompt
    formatted_memory = "\n\n---\n\n".join(past_posts)
    return formatted_memory