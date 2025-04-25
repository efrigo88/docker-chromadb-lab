from datetime import datetime
from typing import List, Dict, Any, Tuple

from sentence_transformers import SentenceTransformer
import pyspark.sql.functions as F
from pyspark.sql import DataFrame

from .helpers import (
    get_base_output_path,
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
    spark,
    schema,
)

from .queries import QUERIES

INPUT_PATH = "./data/input/sample2.pdf"
OUTPUT_PATH = f"{get_base_output_path()}/delta_table"
ANSWERS_PATH = "./data/answers/answers.jsonl"
CHUNK_SIZE = 100


def process_document() -> Tuple[
    List[str],
    List[str],
    List[Dict[str, Any]],
    List[List[float]],
    SentenceTransformer,
]:
    """Process PDF and generate embeddings."""
    doc = parse_pdf(INPUT_PATH)
    text_content = get_text_content(doc)
    print("✅ Text content generated.")

    chunks = get_chunks(text_content, CHUNK_SIZE)
    ids = get_ids(chunks, INPUT_PATH)
    metadatas = get_metadata(chunks, doc, INPUT_PATH)
    print("✅ Chunks, IDs and Metadatas generated.")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = get_embeddings(chunks, model)
    print("✅ Embeddings generated.")

    return ids, chunks, metadatas, embeddings, model


def create_dataframe(
    ids: List[str],
    chunks: List[str],
    metadatas: List[Dict[str, Any]],
    embeddings: List[List[float]],
) -> DataFrame:
    """Create and save DataFrame with processed data."""
    df = spark.createDataFrame(
        [
            {
                "id": id_val,
                "chunk": chunk,
                "metadata": metadata,
                "processed_at": datetime.now(),
                "embeddings": embedding,
            }
            for id_val, chunk, metadata, embedding in zip(
                ids, chunks, metadatas, embeddings
            )
        ],
        schema=schema,
    )

    return df


def deduplicate_data(df: DataFrame) -> DataFrame:
    """Deduplicate data and return processed DataFrame."""
    df = (
        df.orderBy(F.col("processed_at").desc())
        .groupBy("id")
        .agg(
            F.first("processed_at").alias("processed_at"),
            F.first("chunk").alias("chunk"),
            F.first("metadata").alias("metadata"),
            F.first("embeddings").alias("embeddings"),
        )
    )
    print(f"✅ Deduplicated DataFrame in {OUTPUT_PATH}")
    df.show(5)
    return df


def store_in_chromadb_and_run_queries(
    df_loaded: DataFrame, model: SentenceTransformer
) -> None:
    """Store data in ChromaDB and run queries."""
    client = get_client()
    collection = get_collection(client)

    rows = df_loaded.select("id", "chunk", "metadata", "embeddings").collect()
    id_list = [row.id for row in rows]
    doc_list = [row.chunk for row in rows]
    meta_list = [row.metadata.asDict() for row in rows]
    embed_list = [row.embeddings for row in rows]

    collection.upsert(
        ids=id_list,
        documents=doc_list,
        metadatas=meta_list,
        embeddings=embed_list,
    )
    print(f"✅ Upserted {df_loaded.count()} chunks in ChromaDB.")

    all_data = collection.get()
    total_docs = len(all_data["ids"])
    print(f"📊 Total documents in ChromaDB: {total_docs}")

    answers = prepare_queries(collection, model, QUERIES)
    save_json_data(answers, ANSWERS_PATH)
    print(f"✅ Saved answers in {ANSWERS_PATH}")


def main() -> None:
    """Process PDF, transform data, store in ChromaDB, and run queries."""
    try:
        # Process document and generate embeddings
        ids, chunks, metadatas, embeddings, model = process_document()

        df = create_dataframe(ids, chunks, metadatas, embeddings)

        # Save DataFrame to Delta table
        df.write.format("delta").mode("append").save(OUTPUT_PATH)
        print(f"✅ Saved Delta table in {OUTPUT_PATH}")

        # Load Delta table
        df_loaded = spark.read.format("delta").load(OUTPUT_PATH)

        # Deduplicate data
        df_deduplicated = deduplicate_data(df_loaded)

        print(df_deduplicated.show(5))

        # Store in ChromaDB and run queries
        store_in_chromadb_and_run_queries(df_deduplicated, model)

        print("✅ Process completed!")
    finally:
        # Stop Spark session
        spark.stop()
        print("✅ Spark session stopped.")


if __name__ == "__main__":
    main()
