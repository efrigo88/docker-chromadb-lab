import chromadb
from chromadb.config import Settings
from docling.document_converter import DocumentConverter
from sentence_transformers import SentenceTransformer

# Parse the PDF with Docling
SOURCE_PATH = "./sample.pdf"
converter = DocumentConverter()
result = converter.convert(SOURCE_PATH)

doc = result.document
# Get all text content first
text_content = [
    text_item.text.strip()
    for text_item in doc.texts
    if text_item.text.strip() and text_item.label == "text"
]

# Split text into smaller chunks
CHUNK_SIZE = 500  # characters per chunk
chunks = []
for text in text_content:
    for i in range(0, len(text), CHUNK_SIZE):
        chunk = text[i:i + CHUNK_SIZE].strip()
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)

if not chunks:
    raise ValueError("No text chunks found in the document.")

# Embed the chunks
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks).tolist()

# Prepare metadata with page information
ids = [f"{doc.name or 'doc'}_chunk_{i}" for i in range(len(chunks))]
metadatas = [
    {
        "source": SOURCE_PATH,
        "chunk_index": i,
        "title": doc.name,
        "chunk_size": len(chunk),
    }
    for i, chunk in enumerate(chunks)
]

# Store in Chroma
client = chromadb.HttpClient(
    host="chroma",
    port=8000,
    settings=Settings(allow_reset=True, anonymized_telemetry=False),
)

COLLECTION_STATUS = False
while COLLECTION_STATUS is not True:
    try:
        collection = client.get_or_create_collection(name="my_collection")
        COLLECTION_STATUS = True
    except chromadb.errors.ChromaError:
        pass

collection.add(
    ids=ids, documents=chunks, metadatas=metadatas, embeddings=embeddings
)
print(f"✅ Stored {len(chunks)} chunks in ChromaDB.")

# Query the collection
QUERIES = [
    "What is the purpose of this blind text and "
    "what information does it provide about typography?",
    "What characteristics should this blind text have "
    "according to the document?",
    "How does this text help in evaluating typography?",
    "What are the specific requirements mentioned for this sample text?",
]

for query in QUERIES:
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=3)

    print(f"\n❓ Question: {query}")
    print("\n🔍 Top matches:")
    for doc in results["documents"][0]:
        print("-", doc[:200], "...\n")  # Print first 200 characters
    print("-" * 50)
