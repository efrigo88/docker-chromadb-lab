# Docker ChromaDB Lab

A simple lab environment for experimenting with ChromaDB in Docker.

## Project Structure

```
.
├── docker-compose.yml    # Docker Compose configuration
├── Makefile             # Helper commands
├── requirements.txt     # Python dependencies
└── src/
    └── main.py         # Main application code
```

## Features

- ChromaDB server running in a Docker container
- Python application with sample data
- Automatic retry mechanism for collection creation
- Formatted output of retrieved data

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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
