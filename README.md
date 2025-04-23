# Docker ChromaDB Lab

A simple lab environment for experimenting with ChromaDB in Docker.

## Project Structure

```
.
├── docker-compose.yml    # Docker Compose configuration
├── Makefile             # Helper commands
├── pyproject.toml       # Python project configuration
└── main.py             # Main application code
```

## Features

- ChromaDB server running in a Docker container
- Python application with sample data
- Automatic retry mechanism for collection creation
- Formatted output of retrieved data including:
  - Document content
  - Metadata
  - Vector embeddings (first 5 dimensions)

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

## Sample Data

The application includes sample data about AI and ML topics:

1. ChromaDB overview
2. Vector databases
3. SentenceTransformers
4. OpenAI API
5. RAG (Retrieval-Augmented Generation)

Each document includes:

- Unique ID
- Content text
- Metadata (topic and source)
- Vector embedding

## Troubleshooting

If you encounter connection issues:

1. Check if ChromaDB is running: `make ps`
2. View logs: `make logs`
3. Rebuild containers: `make rebuild`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
