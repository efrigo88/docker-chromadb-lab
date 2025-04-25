from sentence_transformers import SentenceTransformer

from .helpers import (
    get_client,
    get_collection,
    parse_pdf,
    get_text_content,
    get_chunks,
    get_ids,
    get_metadata,
    get_embeddings,
    prepare_queries,
    prepare_json_data,
    save_json_data,
)

from .queries import QUERIES

FILE_PATH = "./data/input/sample2.pdf"
CHUNK_SIZE = 100


def main() -> None:
    """Main function to process PDF, store in ChromaDB, and run queries."""
    doc = parse_pdf(FILE_PATH)
    text_content = get_text_content(doc)
    print("✅ Text content generated.")

    chunks = get_chunks(text_content, CHUNK_SIZE)
    ids = get_ids(chunks, FILE_PATH)
    metadatas = get_metadata(chunks, doc, FILE_PATH)
    print("✅ Chunks, IDs and Metadatas generated.")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = get_embeddings(chunks, model)
    print("✅ Embeddings generated.")

    data = prepare_json_data(chunks, ids, metadatas, embeddings)
    save_json_data(data, "./data/output/data.jsonl")
    print("✅ Saved data to ./data/output/data.jsonl")

    client = get_client()
    collection = get_collection(client)
    collection.add(
        ids=ids, documents=chunks, metadatas=metadatas, embeddings=embeddings
    )
    print(f"✅ Stored {len(chunks)} chunks in ChromaDB.")

    questions_answers = prepare_queries(collection, model, QUERIES)
    save_json_data(questions_answers, "./data/answers/answers.jsonl")
    print("✅ Saved questions and answers to")
    print("./data/answers/answers.jsonl")
    print("✅ Process completed!")


if __name__ == "__main__":
    main()
