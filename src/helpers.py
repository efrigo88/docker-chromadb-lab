import os
import json
from typing import List, Dict, Any
from datetime import datetime
import chromadb
from chromadb.config import Settings
from docling.datamodel.document import InputDocument
from docling.document_converter import DocumentConverter
from sentence_transformers import SentenceTransformer


def prepare_json_data(
    chunks: List[str],
    ids: List[str],
    metadatas: List[Dict[str, Any]],
    embeddings: List[List[float]],
    source_path: str,
) -> Dict[str, Any]:
    """Prepare data in json format."""
    return {
        "source": source_path,
        "timestamp": datetime.now().isoformat(),
        "chunks": [
            {
                "id": ids[i],
                "text": chunk,
                "metadata": metadata,
                "embedding": embedding,
            }
            for i, (chunk, metadata, embedding) in enumerate(
                zip(chunks, metadatas, embeddings)
            )
        ],
    }


def save_json_data(
    data: Dict[str, Any], file_path: str, overwrite: bool = True
) -> None:
    """Save data to a JSON file."""
    if not overwrite and os.path.exists(file_path):
        raise FileExistsError(
            f"File {file_path} already exists and overwrite=False"
        )
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_client() -> chromadb.HttpClient:
    """Initialize and return a ChromaDB HTTP client."""
    return chromadb.HttpClient(
        host="chroma",
        port=8000,
        settings=Settings(allow_reset=True, anonymized_telemetry=False),
    )


def get_collection(client: chromadb.HttpClient) -> chromadb.Collection:
    """Get or create a ChromaDB collection with retry logic."""
    collection_status = False
    while collection_status is not True:
        try:
            collection = client.get_or_create_collection(name="my_collection")
            collection_status = True
        except chromadb.errors.ChromaError:
            pass
    return collection


def parse_pdf(source_path: str) -> InputDocument:
    """Parse the PDF document using DocumentConverter."""
    converter = DocumentConverter()
    result = converter.convert(source_path)
    return result.document


def get_text_content(doc: InputDocument) -> List[str]:
    """Extract text content from the document."""
    return [
        text_item.text.strip()
        for text_item in doc.texts
        if text_item.text.strip() and text_item.label == "text"
    ]


def get_chunks(text_content: List[str], chunk_size: int) -> List[str]:
    """Split text content into chunks of specified size."""
    chunks = []
    for text in text_content:
        for i in range(0, len(text), chunk_size):
            chunk = text[i : i + chunk_size].strip()
            if chunk:
                chunks.append(chunk)
    if not chunks:
        raise ValueError("No text chunks found in the document.")
    return chunks


def get_ids(chunks: List[str], source_path: str) -> List[str]:
    """Generate unique IDs for each chunk."""
    return [f"{source_path}_chunk_{i}" for i in range(len(chunks))]


def get_metadata(
    chunks: List[str],
    doc: InputDocument,
    source_path: str,
) -> List[Dict[str, Any]]:
    """Generate metadata for each chunk."""
    return [
        {
            "source": source_path,
            "chunk_index": i,
            "title": doc.name,
            "chunk_size": len(chunk),
        }
        for i, chunk in enumerate(chunks)
    ]


def get_embeddings(
    chunks: List[str],
    model: SentenceTransformer,
) -> List[List[float]]:
    """Get embeddings for a list of chunks using a specified model."""
    return model.encode(chunks).tolist()


def prepare_queries(
    collection: chromadb.Collection,
    model: SentenceTransformer,
    queries: List[str],
) -> Dict[str, Any]:
    """Run queries and prepare results in json format."""
    timestamp = datetime.now().isoformat()
    all_results = []

    for query in queries:
        query_embedding = model.encode(query).tolist()
        results = collection.query(
            query_embeddings=[query_embedding], n_results=3
        )
        query_result = {
            "query": query,
            "timestamp": timestamp,
            "results": [
                {
                    "text": doc,
                    "similarity": sim,
                }
                for doc, sim in zip(
                    results["documents"][0], results["distances"][0]
                )
            ],
        }
        all_results.append(query_result)

    return {"queries": all_results}
