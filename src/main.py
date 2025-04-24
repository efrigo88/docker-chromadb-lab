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
    prepare_json_data,
    save_json_data,
)


def main() -> None:
    """Main function to process PDF, store in ChromaDB, and run queries."""
    doc = parse_pdf()
    text_content = get_text_content(doc)
    print("✅ Text content generated.")

    chunks = get_chunks(text_content)
    ids = get_ids(chunks)
    metadatas = get_metadata(chunks, doc)
    print("✅ Chunks, IDs and Metadatas generated.")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks).tolist()
    print("✅ Embeddings generated.")

    data = prepare_json_data(chunks, ids, metadatas, embeddings)
    save_json_data(data, "./data/data.json")
    print("✅ Saved data to ./data/data.json")

    client = get_client()
    collection = get_collection(client)
    collection.add(
        ids=ids, documents=chunks, metadatas=metadatas, embeddings=embeddings
    )
    print(f"✅ Stored {len(chunks)} chunks in ChromaDB.")

    run_queries(collection, model)
    print("✅ Process completed!")


if __name__ == "__main__":
    main()
