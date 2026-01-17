# =============================================================================
# MCP Knowledge Server
# =============================================================================
# Model Context Protocol server for document search and knowledge retrieval
# =============================================================================

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5002

# Health check
HEALTHCHECK --interval=15s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:5002/health || exit 1

CMD ["python", "server.py"]
