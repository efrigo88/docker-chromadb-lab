# PDF Text Analysis with ChromaDB

This project demonstrates how to process PDF documents, extract text, and perform semantic search using ChromaDB and Sentence Transformers.

## Project Structure

```
.
├── data/                     # Directory for data files
│   └── data.json             # Sample json ouptut file
├── src/                      # Source code
│   ├── __init__.py
│   ├── config.py             # Configuration settings
│   ├── helpers.py            # Utility functions
│   └── main.py               # Main script
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Data Output Format

The project generates a JSON file containing document chunks and their embeddings. The output format is as follows:

```json
{
    "source": "path/to/source/file.pdf",
    "timestamp": "2024-03-21T12:34:56.789012",
    "chunks": [
        {
            "id": "file.pdf_chunk_0",
            "text": "First chunk of text...",
            "metadata": {
                "source": "path/to/source/file.pdf",
                "chunk_index": 0,
                "title": "Document Title",
                "chunk_size": 123
            },
            "embedding": [0.1, 0.2, 0.3, ...]  // Vector embedding of the chunk
        },
        // ... more chunks
    ]
}
```

### Key Features of the Output

- **Source**: Original document path
- **Timestamp**: When the file was generated
- **Chunks**: Array of document segments containing:
  - **id**: Unique identifier for the chunk
  - **text**: The actual text content
  - **metadata**: Additional information about the chunk
  - **embedding**: Vector representation of the text

## Features

- PDF text extraction using Docling
- Text chunking with configurable chunk size
- Semantic search using Sentence Transformers
- Multiple query testing capabilities
- Metadata tracking for each text chunk

## Recent Changes

1. **Improved Project Structure**

   - Organized code into `src` package
   - Separated configuration into `config.py`
   - Better code organization and maintainability

2. **Improved Text Chunking**

   - Implemented fixed-size chunking (500 characters)
   - Added chunk size metadata
   - Better text boundary handling

3. **Enhanced Query System**

   - Added multiple query testing
   - Improved query formatting
   - Better result presentation

4. **Code Quality Improvements**
   - Fixed line length issues
   - Improved code formatting
   - Better error handling

## How It Works

1. **Document Processing**

   - PDF is loaded and converted using Docling
   - Text is extracted and split into manageable chunks
   - Each chunk is embedded using Sentence Transformers

2. **Storage**

   - Chunks are stored in ChromaDB with:
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

## Requirements

- Python 3.9+
- chromadb
- docling
- sentence-transformers

## Usage

1. Place your PDF in the project directory
2. Update `SOURCE_PATH` in `src/config.py` if needed
3. Run the script:
   ```bash
   python -m src.main
   ```

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
