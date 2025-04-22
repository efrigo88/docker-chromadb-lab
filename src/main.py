import chromadb
from chromadb.config import Settings

sample_data = [
    {
        "id": "1",
        "document": "ChromaDB is a vector database designed for AI applications.",
        "metadata": {"topic": "AI", "source": "docs"},
    },
    {
        "id": "2",
        "document": "Vector databases store embeddings and enable semantic search.",
        "metadata": {"topic": "databases", "source": "blog"},
    },
    {
        "id": "3",
        "document": "SentenceTransformers can be used to generate embeddings locally.",
        "metadata": {"topic": "ML", "source": "notebook"},
    },
    {
        "id": "4",
        "document": "OpenAI provides API access to powerful language models.",
        "metadata": {"topic": "NLP", "source": "api"},
    },
    {
        "id": "5",
        "document": "Retrieval-Augmented Generation (RAG) combines retrieval and generation steps in LLM pipelines.",
        "metadata": {"topic": "RAG", "source": "paper"},
    },
]

client = chromadb.HttpClient(
    host="chroma",
    port=8000,
    settings=Settings(allow_reset=True, anonymized_telemetry=False),
)

collection_status = False
while collection_status != True:
    try:
        collection = client.get_or_create_collection(name="my_collection")
        collection_status = True
    except chromadb.errors.ChromaError:
        pass

# Prepare data
ids = []
documents = []
metadatas = []

for item in sample_data:
    ids.append(item["id"])
    documents.append(item["document"])
    metadatas.append(item.get("metadata", {}))

# Insert into Chroma
collection.add(ids=ids, documents=documents, metadatas=metadatas)
print("Data inserted into ChromaDB.")

# Retrieve and print the added data
results = collection.get(
    ids=ids,
    include=["documents", "metadatas", "embeddings"],
)

# Print results in a readable format
print("Results retrieved from ChromaDB:")
for i, (doc_id, doc, meta) in enumerate(
    zip(results["ids"], results["documents"], results["metadatas"])
):
    print(f"\nDocument {i+1}:")
    print(f"ID: {doc_id}")
    print(f"Content: {doc}")
    print("Metadata:")
    for key, value in meta.items():
        print(f"  {key}: {value}")
    print("-" * 50)
