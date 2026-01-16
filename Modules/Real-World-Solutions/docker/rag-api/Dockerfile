# =============================================================================
# RAG API Service
# =============================================================================
# Flask-based API for RAG (Retrieval Augmented Generation) functionality
# Uses ChromaDB for vector storage and Ollama for LLM inference
# =============================================================================

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for documents
RUN mkdir -p /app/documents /app/data

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=15s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# Run the application
CMD ["python", "app.py"]
