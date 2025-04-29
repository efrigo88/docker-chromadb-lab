#!/bin/bash

# Start containers
docker compose up -d --build

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
sleep 10

# Pull the model
echo "Pulling nomic-embed-text model..."
docker exec ollama ollama pull nomic-embed-text

echo "Setup complete!"
