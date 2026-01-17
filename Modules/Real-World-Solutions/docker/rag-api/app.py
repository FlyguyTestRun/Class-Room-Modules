"""
RAG API Service for ZZZ Accounting Merger Platform
==================================================
Provides document search, Q&A, and knowledge retrieval endpoints
using ChromaDB for vectors and Ollama for LLM inference.
"""

import os
import logging
from datetime import datetime
from typing import Optional

from flask import Flask, jsonify, request
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import ollama
import redis
import psycopg2
from psycopg2.extras import RealDictCursor

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =============================================================================
# Flask App Configuration
# =============================================================================
app = Flask(__name__)
CORS(app)
metrics = PrometheusMetrics(app)

# Configuration
CHROMA_HOST = os.getenv('CHROMA_HOST', 'chromadb')
CHROMA_PORT = int(os.getenv('CHROMA_PORT', 8000))
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'ollama')
OLLAMA_PORT = int(os.getenv('OLLAMA_PORT', 11434))
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral')
REDIS_HOST = os.getenv('REDIS_HOST', 'merger-redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# Database config
DB_CONFIG = {
    'host': os.getenv('UNIFIED_DB_HOST', 'unified-db'),
    'port': int(os.getenv('UNIFIED_DB_PORT', 5432)),
    'dbname': os.getenv('UNIFIED_DB_NAME', 'zzz_unified'),
    'user': os.getenv('UNIFIED_DB_USER', 'unified_admin'),
    'password': os.getenv('UNIFIED_DB_PASSWORD', 'unified_secure_2024')
}

# =============================================================================
# Initialize Services
# =============================================================================

# Embedding model (runs locally, no API key needed)
embedding_model = None

def get_embedding_model():
    """Lazy load embedding model."""
    global embedding_model
    if embedding_model is None:
        logger.info("Loading embedding model: all-MiniLM-L6-v2")
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    return embedding_model

# ChromaDB client
chroma_client = None

def get_chroma_client():
    """Get ChromaDB client."""
    global chroma_client
    if chroma_client is None:
        logger.info(f"Connecting to ChromaDB at {CHROMA_HOST}:{CHROMA_PORT}")
        chroma_client = chromadb.HttpClient(
            host=CHROMA_HOST,
            port=CHROMA_PORT,
            settings=Settings(anonymized_telemetry=False)
        )
    return chroma_client

# Redis client
redis_client = None

def get_redis_client():
    """Get Redis client."""
    global redis_client
    if redis_client is None:
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True
        )
    return redis_client

def get_db_connection():
    """Get database connection."""
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

# =============================================================================
# Helper Functions
# =============================================================================

def generate_embedding(text: str) -> list:
    """Generate embedding for text using local model."""
    model = get_embedding_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()

def query_ollama(prompt: str, context: str = "") -> str:
    """Query Ollama LLM with optional context."""
    try:
        # Set Ollama host
        client = ollama.Client(host=f"http://{OLLAMA_HOST}:{OLLAMA_PORT}")

        # Build the full prompt
        if context:
            full_prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {prompt}

Answer:"""
        else:
            full_prompt = prompt

        # Generate response
        response = client.generate(
            model=OLLAMA_MODEL,
            prompt=full_prompt,
            options={
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 1000
            }
        )

        return response['response']

    except Exception as e:
        logger.error(f"Ollama error: {e}")
        raise

def search_documents(query: str, n_results: int = 5) -> list:
    """Search documents in ChromaDB."""
    try:
        client = get_chroma_client()
        collection = client.get_or_create_collection(
            name="merger_documents",
            metadata={"description": "ZZZ Accounting merger documents"}
        )

        # Generate query embedding
        query_embedding = generate_embedding(query)

        # Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )

        # Format results
        formatted = []
        if results and results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                formatted.append({
                    'content': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'score': 1 - results['distances'][0][i] if results['distances'] else 0
                })

        return formatted

    except Exception as e:
        logger.error(f"Search error: {e}")
        return []

# =============================================================================
# API Endpoints
# =============================================================================

@app.route('/health', methods=['GET'])
@metrics.do_not_track()
def health_check():
    """Health check endpoint."""
    status = {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
    checks = {}

    # Check ChromaDB
    try:
        client = get_chroma_client()
        client.heartbeat()
        checks['chromadb'] = 'connected'
    except Exception as e:
        checks['chromadb'] = f'error: {str(e)}'
        status['status'] = 'degraded'

    # Check Ollama
    try:
        client = ollama.Client(host=f"http://{OLLAMA_HOST}:{OLLAMA_PORT}")
        models = client.list()
        checks['ollama'] = f"connected, models: {len(models.get('models', []))}"
    except Exception as e:
        checks['ollama'] = f'error: {str(e)}'
        status['status'] = 'degraded'

    # Check Redis
    try:
        r = get_redis_client()
        r.ping()
        checks['redis'] = 'connected'
    except Exception as e:
        checks['redis'] = f'error: {str(e)}'
        status['status'] = 'degraded'

    # Check Database
    try:
        conn = get_db_connection()
        conn.close()
        checks['database'] = 'connected'
    except Exception as e:
        checks['database'] = f'error: {str(e)}'
        status['status'] = 'degraded'

    status['checks'] = checks
    return jsonify(status)

@app.route('/api/v1/search', methods=['POST'])
def search():
    """Search documents endpoint."""
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({'error': 'Missing query parameter'}), 400

    query = data['query']
    n_results = data.get('limit', 5)

    logger.info(f"Search query: {query}")

    try:
        results = search_documents(query, n_results)
        return jsonify({
            'query': query,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/ask', methods=['POST'])
def ask_question():
    """RAG Q&A endpoint - search documents and generate answer."""
    data = request.get_json()

    if not data or 'question' not in data:
        return jsonify({'error': 'Missing question parameter'}), 400

    question = data['question']
    use_context = data.get('use_context', True)

    logger.info(f"Question: {question}")

    try:
        # Search for relevant context
        context = ""
        sources = []

        if use_context:
            results = search_documents(question, n_results=3)
            if results:
                context = "\n\n".join([r['content'] for r in results])
                sources = [r.get('metadata', {}) for r in results]

        # Generate answer
        answer = query_ollama(question, context)

        return jsonify({
            'question': question,
            'answer': answer,
            'sources': sources,
            'context_used': bool(context)
        })

    except Exception as e:
        logger.error(f"Q&A error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/chat', methods=['POST'])
def chat():
    """Simple chat endpoint without RAG."""
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({'error': 'Missing message parameter'}), 400

    message = data['message']

    try:
        response = query_ollama(message)
        return jsonify({
            'message': message,
            'response': response
        })
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/documents', methods=['GET'])
def list_documents():
    """List indexed documents."""
    try:
        client = get_chroma_client()
        collection = client.get_or_create_collection(name="merger_documents")

        # Get collection info
        count = collection.count()

        return jsonify({
            'collection': 'merger_documents',
            'document_count': count
        })
    except Exception as e:
        logger.error(f"List documents error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/documents/ingest', methods=['POST'])
def ingest_document():
    """Ingest a document into the vector store."""
    data = request.get_json()

    if not data or 'content' not in data:
        return jsonify({'error': 'Missing content parameter'}), 400

    content = data['content']
    metadata = data.get('metadata', {})
    doc_id = data.get('id', f"doc_{datetime.utcnow().timestamp()}")

    try:
        client = get_chroma_client()
        collection = client.get_or_create_collection(name="merger_documents")

        # Generate embedding
        embedding = generate_embedding(content)

        # Add to collection
        collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[metadata]
        )

        return jsonify({
            'success': True,
            'id': doc_id,
            'message': 'Document ingested successfully'
        })

    except Exception as e:
        logger.error(f"Ingest error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/clients/search', methods=['GET'])
def search_clients():
    """Search clients in unified database."""
    query = request.args.get('q', '')

    if not query:
        return jsonify({'error': 'Missing search query (q)'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT org_id, legal_name, dba_name, tax_id, org_type
            FROM organizations
            WHERE legal_name ILIKE %s OR dba_name ILIKE %s
            LIMIT 20
        """, (f'%{query}%', f'%{query}%'))

        results = cursor.fetchall()
        conn.close()

        return jsonify({
            'query': query,
            'results': [dict(r) for r in results],
            'count': len(results)
        })

    except Exception as e:
        logger.error(f"Client search error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/models', methods=['GET'])
def list_models():
    """List available Ollama models."""
    try:
        client = ollama.Client(host=f"http://{OLLAMA_HOST}:{OLLAMA_PORT}")
        models = client.list()
        return jsonify(models)
    except Exception as e:
        logger.error(f"List models error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """API documentation."""
    return jsonify({
        'service': 'ZZZ Accounting RAG API',
        'version': '1.0.0',
        'endpoints': {
            'GET /health': 'Health check',
            'POST /api/v1/search': 'Search documents',
            'POST /api/v1/ask': 'Ask question with RAG',
            'POST /api/v1/chat': 'Simple chat (no RAG)',
            'GET /api/v1/documents': 'List indexed documents',
            'POST /api/v1/documents/ingest': 'Ingest document',
            'GET /api/v1/clients/search?q=': 'Search clients',
            'GET /api/v1/models': 'List available LLM models'
        }
    })

# =============================================================================
# Run Application
# =============================================================================
if __name__ == '__main__':
    port = int(os.getenv('RAG_API_PORT', 5001))
    debug = os.getenv('RAG_API_DEBUG', 'false').lower() == 'true'

    logger.info(f"Starting RAG API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
