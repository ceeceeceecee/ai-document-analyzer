#!/bin/bash
set -e
echo "=== Installing ai-document-analyzer ==="

if ! command -v docker &> /dev/null; then
    echo "Docker is required. Please install Docker first."
    exit 1
fi
if ! docker compose version &> /dev/null; then
    echo "Docker Compose V2 is required."
    exit 1
fi

echo "Starting Ollama service..."
docker compose up -d ollama
sleep 5

echo "Pulling llama3 model (this may take a while on first run)..."
docker compose exec ollama ollama pull llama3 2>/dev/null || echo "Model pull initiated"

echo "Starting all services..."
docker compose up -d

echo "=== ai-document-analyzer is running ==="
echo "Open http://localhost:8502 in your browser"
