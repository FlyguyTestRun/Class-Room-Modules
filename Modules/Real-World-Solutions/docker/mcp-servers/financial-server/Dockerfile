# =============================================================================
# MCP Financial Server
# =============================================================================
# Model Context Protocol server for financial data access
# Includes RBAC for sensitive financial operations
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
EXPOSE 5003

# Health check
HEALTHCHECK --interval=15s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:5003/health || exit 1

CMD ["python", "server.py"]
