from datetime import datetime

from sentence_transformers import SentenceTransformer
import pandas as pd

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
    save_json_data,
)

from .queries import QUERIES

INPUT_PATH = "./data/input/sample2.pdf"
OUTPUT_PATH = "./data/output/data.jsonl"
ANSWERS_PATH = "./data/answers/answers.jsonl"
CHUNK_SIZE = 100


def main() -> None:
    """Main function to process PDF, store in ChromaDB, and run queries."""
    doc = parse_pdf(INPUT_PATH)
    text_content = get_text_content(doc)
    print("✅ Text content generated.")

    chunks = get_chunks(text_content, CHUNK_SIZE)
    ids = get_ids(chunks, INPUT_PATH)
    metadatas = get_metadata(chunks, doc, INPUT_PATH)
    print("✅ Chunks, IDs and Metadatas generated.")

    # Create DataFrame for data manipulation
    df = pd.DataFrame({"id": ids, "chunk": chunks, "metadata": metadatas})

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = get_embeddings(df["chunk"].tolist(), model)
    print("✅ Embeddings generated.")

    # Enrich DataFrame with embeddings and processed_at
    df["embeddings"] = embeddings
    df["processed_at"] = datetime.now().isoformat()

    # Save DataFrame to JSON
    # Reorder columns before saving
    df = df[["processed_at", "id", "chunk", "metadata", "embeddings"]]
    df.to_json(OUTPUT_PATH, orient="records", lines=True, mode="w")
    print("✅ Saved DataFrame to")
    print(OUTPUT_PATH)

    # Read data back from JSON
    df_loaded = pd.read_json(OUTPUT_PATH, lines=True)

    # Store data in ChromaDB
    client = get_client()
    collection = get_collection(client)
    collection.add(
        ids=df_loaded["id"].tolist(),
        documents=df_loaded["chunk"].tolist(),
        metadatas=df_loaded["metadata"].tolist(),
        embeddings=df_loaded["embeddings"].tolist(),
    )
    print(f"✅ Stored {len(df_loaded)} chunks in ChromaDB.")

    # Run queries and save results
    answers = prepare_queries(collection, model, QUERIES)
    save_json_data(answers, ANSWERS_PATH)
    print("✅ Saved answers to")
    print(ANSWERS_PATH)
    print("✅ Process completed!")


if __name__ == "__main__":
    main()
