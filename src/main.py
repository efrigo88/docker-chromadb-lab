from sentence_transformers import SentenceTransformer

from .helpers import (
    get_client,
    get_collection,
    parse_pdf,
    get_text_content,
    get_chunks,
    get_ids,
    get_metadata,
    run_queries,
)


def main() -> None:
    """Main function to process PDF, store in ChromaDB, and run queries."""
    doc = parse_pdf()
    text_content = get_text_content(doc)

    chunks = get_chunks(text_content)
    ids = get_ids(chunks)
    metadatas = get_metadata(chunks, doc)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks).tolist()

    client = get_client()
    collection = get_collection(client)
    collection.add(
        ids=ids, documents=chunks, metadatas=metadatas, embeddings=embeddings
    )
    print(f"✅ Stored {len(chunks)} chunks in ChromaDB.")

    run_queries(collection, model)
    print("✅ Done!")


if __name__ == "__main__":
    main()
