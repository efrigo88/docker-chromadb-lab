import chromadb
from chromadb.config import Settings

# Connect to the ChromaDB server
client = chromadb.HttpClient(
    Settings(
        chroma_api_impl="rest",
        chroma_server_host="localhost",
        chroma_server_http_port=8000,
    )
)

# Create a new collection
collection = client.get_or_create_collection(name="my_collection")

# Add some data (IDs + documents + metadata)
collection.add(
    ids=["doc1", "doc2"],
    documents=[
        "Hello, this is a test document.",
        "This one talks about Python and ChromaDB.",
    ],
    metadatas=[{"category": "test"}, {"category": "python"}],
)

# Query with a simple sentence
results = collection.query(
    query_texts=["What does this document say about Python?"], n_results=2
)

print("Query Results:", results)
