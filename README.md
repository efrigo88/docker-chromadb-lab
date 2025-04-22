# ChromaDB Lab

This project demonstrates how to run ChromaDB in a Docker container and insert files into it.

## Prerequisites

- Docker
- Python 3.8+
- UV package manager

## Setup

1. Clone this repository
2. Install dependencies using UV:
   ```bash
   uv pip install -r requirements.txt
   ```
3. Run the Docker container:
   ```bash
   docker-compose up -d
   ```
4. Run the Python script to insert files:
   ```bash
   python src/main.py
   ```

## Project Structure

- `src/` - Contains the main Python code
- `data/` - Directory for files to be inserted into ChromaDB
- `docker-compose.yml` - Docker configuration for ChromaDB
- `requirements.txt` - Python dependencies

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
