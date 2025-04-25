# PDF Text Analysis with ChromaDB

This project demonstrates how to process PDF documents, extract text, and perform semantic search using ChromaDB and Sentence Transformers.

## Project Structure

```
.
├── data/                      # Directory for data files
│   ├── input/                # Input PDF files
│   ├── output/               # Processed data (JSONL files)
│   │   └── delta_table/      # Date-based delta table
│   └── answers/              # Query results
├── src/                      # Source code
│   ├── __init__.py
│   ├── queries.py           # Predefined queries for testing
│   ├── helpers.py           # Utility functions
│   └── main.py              # Main script
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Data Output Format

### Document Chunks (data.json)

The project generates a JSONL file containing document chunks and their embeddings. Each line is a complete JSON object:

```jsonl
{"id": "document_chunk_0", "text": "First chunk of text...", "metadata": {"source": "path/to/source/file.pdf", "chunk_index": 0, "title": "Document Title", "chunk_size": 123}, "embedding": [0.1, 0.2, 0.3, ...], "processed_at": "2024-03-21T12:34:56.789012"}
{"id": "document_chunk_1", "text": "Second chunk of text...", "metadata": {"source": "path/to/source/file.pdf", "chunk_index": 1, "title": "Document Title", "chunk_size": 123}, "embedding": [0.4, 0.5, 0.6, ...], "processed_at": "2024-03-21T12:34:56.789012"}
```

### Query Results (questions_answers.json)

Query results are saved in a JSONL file with similarity scores. Each line is a complete JSON object:

```jsonl
{"query": "Who are the crazy ones?", "timestamp": "2024-03-21T12:34:56.789012", "results": [{"text": "Retrieved text chunk", "similarity": 0.95}]}
{"query": "What do the crazy ones do?", "timestamp": "2024-03-21T12:34:56.789012", "results": [{"text": "Another text chunk", "similarity": 0.89}]}
```

### Understanding Similarity Scores

The similarity scores represent how closely the retrieved text matches the semantic meaning of your query:

- Scores are cosine similarity values between query and document embeddings
- Range: Typically between -1 and 1
  - 1.0: Perfect semantic match
  - 0: No similarity
  - Negative values: Opposite meanings
- Results are ranked by similarity, with higher scores indicating better matches

## Features

- PDF text extraction using Docling
- Text chunking with configurable chunk size
- Semantic search using Sentence Transformers
- Multiple query testing capabilities
- Metadata tracking for each text chunk
- Query results with similarity scores
- Delta Lake storage with date partitioning for efficient data management
- Data versioning and time-travel capabilities through Delta Lake

## Recent Changes

1. **Delta Lake Integration**

   - Added Delta Lake for efficient data storage
   - Implemented date-based partitioning (processed_dt)
   - Added data versioning capabilities
   - Improved query performance through partitioning

2. **Code Simplification**

   - Removed default parameters for better clarity
   - Simplified function signatures
   - Improved type annotations
   - Better code organization

3. **Query Results Enhancement**

   - Added similarity scores to query results
   - Improved result ranking based on semantic similarity
   - Structured JSON output for better analysis

4. **Improved Project Structure**

   - Organized code into `src` package
   - Separated queries file into `queries.py`
   - Better code organization and maintainability

5. **Improved Text Chunking**

   - Implemented fixed-size chunking
   - Added chunk size metadata
   - Better text boundary handling

6. **Enhanced Query System**

   - Added multiple query testing
   - Improved query formatting
   - Better result presentation

7. **Pandas Integration**
   - Added DataFrame operations for data processing
   - Implemented data deduplication using pandas
   - Added date-based file organization
   - Improved data storage and retrieval workflow

## How It Works

1. **Document Processing**

   - PDF is loaded and converted using Docling
   - Text is extracted and split into manageable chunks
   - Each chunk is embedded using Sentence Transformers

2. **Storage**

   - Chunks are stored in Delta Lake with:
     - Date-based partitioning (processed_dt)
     - Data versioning capabilities
     - Efficient query performance
   - Embeddings are stored in ChromaDB with:
     - Unique IDs
     - Text content
     - Pre-computed embeddings
     - Metadata (source, index, size)

3. **Search**
   - Multiple queries can be tested
   - Results are ranked by semantic similarity
   - Top matches are displayed with context

## Prerequisites

- Docker
- Docker Compose
- Make (optional, for using Makefile commands)

## Getting Started

1. Clone the repository:

   ```bash
   git clone git@github.com:efrigo88/docker-chromadb-lab.git
   cd docker-chromadb-lab
   ```

2. Build and start the containers:

   ```bash
   docker compose up -d --build
   ```

3. View logs:
   ```bash
   make logs
   ```

## Available Commands

- `make up` - Start containers
- `make down` - Stop containers
- `make build` - Build containers
- `make rebuild` - Rebuild and restart containers
- `make logs` - View container logs
- `make ps` - Check container status
- `make clean` - Remove containers and volumes

## Container Setup and Usage

1. Start the containers:

   ```bash
   docker compose up -d --build
   ```

   This will build and start both the app and chroma containers in the background.

2. Run your script in the app container:

   ```bash
   docker exec -it app python -m src.main
   ```

   The container will stay running, allowing you to:

   - Modify code in the `src` directory
   - Run the script multiple times
   - See the output in your terminal

3. To stop the containers when done (will delete the volume as well):
   ```bash
   docker compose down -v
   ```

## Usage

1. Place your PDF in the project directory
2. Update `FILE_PATH` in `src/main.py` if needed
3. Run the script as shown in the Container Setup section above

## Example Queries

The system currently tests these questions:

- Purpose and typography information
- Required characteristics
- Typography evaluation benefits
- Specific requirements

## Future Improvements

- Implement sentence-based chunking
- Add query expansion
- Include page number metadata
- Add result scoring display

## Troubleshooting

If you encounter connection issues:

1. Check if ChromaDB is running: `make ps`
2. View logs: `make logs`
3. Rebuild containers: `make rebuild`
