"""
MCP Knowledge Server
====================
Model Context Protocol server for document search and knowledge retrieval.
Provides tools for Claude to search company documents and policies.
"""

import os
import logging
from datetime import datetime
from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS
import httpx

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
MCP_PORT = int(os.getenv('MCP_PORT', 5002))
RAG_API_HOST = os.getenv('RAG_API_HOST', 'rag-api')
RAG_API_PORT = int(os.getenv('RAG_API_PORT', 5001))
RAG_API_URL = f"http://{RAG_API_HOST}:{RAG_API_PORT}"

# =============================================================================
# MCP Tool Definitions
# =============================================================================

TOOLS = {
    "search_knowledge": {
        "name": "search_knowledge",
        "description": "Search company documents, policies, and knowledge base for relevant information. Use this when you need to find specific information about company procedures, client contracts, or merger documentation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query to find relevant documents"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default: 5)",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    },
    "get_policy": {
        "name": "get_policy",
        "description": "Retrieve a specific company policy by name or topic. Use this when you need the exact text of an accounting procedure, HR policy, or company guideline.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "policy_name": {
                    "type": "string",
                    "description": "Name or topic of the policy to retrieve"
                }
            },
            "required": ["policy_name"]
        }
    },
    "ask_knowledge_base": {
        "name": "ask_knowledge_base",
        "description": "Ask a question about company knowledge and get an AI-generated answer based on indexed documents. Use this for complex questions that require synthesizing information from multiple sources.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The question to ask"
                }
            },
            "required": ["question"]
        }
    },
    "list_procedures": {
        "name": "list_procedures",
        "description": "List available accounting procedures and their categories. Use this to discover what procedures are documented in the knowledge base.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Filter by category (optional): tax, audit, payroll, general",
                    "enum": ["tax", "audit", "payroll", "general"]
                }
            }
        }
    }
}

# =============================================================================
# Tool Implementations
# =============================================================================

async def search_knowledge(query: str, limit: int = 5) -> dict:
    """Search the knowledge base."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{RAG_API_URL}/api/v1/search",
                json={"query": query, "limit": limit},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Search error: {e}")
        return {"error": str(e)}

async def get_policy(policy_name: str) -> dict:
    """Get a specific policy."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{RAG_API_URL}/api/v1/search",
                json={"query": f"policy: {policy_name}", "limit": 1},
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            if data.get('results'):
                return {"policy": data['results'][0]}
            return {"error": f"Policy '{policy_name}' not found"}
    except Exception as e:
        logger.error(f"Policy error: {e}")
        return {"error": str(e)}

async def ask_knowledge_base(question: str) -> dict:
    """Ask the RAG system a question."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{RAG_API_URL}/api/v1/ask",
                json={"question": question},
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Ask error: {e}")
        return {"error": str(e)}

def list_procedures(category: str = None) -> dict:
    """List available procedures."""
    # Mock data - in production this would query the database
    procedures = {
        "tax": [
            "Individual Tax Return Preparation",
            "Business Tax Return Preparation",
            "Quarterly Estimated Tax Payments",
            "Tax Extension Filing"
        ],
        "audit": [
            "Financial Statement Audit",
            "Internal Control Review",
            "Compliance Audit",
            "Year-End Closing Procedures"
        ],
        "payroll": [
            "Payroll Processing",
            "Payroll Tax Deposits",
            "W-2 Preparation",
            "1099 Preparation"
        ],
        "general": [
            "Client Onboarding",
            "Engagement Letter Preparation",
            "Time Tracking",
            "Invoice Generation"
        ]
    }

    if category:
        return {"category": category, "procedures": procedures.get(category, [])}
    return {"procedures": procedures}

# =============================================================================
# MCP Endpoints
# =============================================================================

@app.route('/health', methods=['GET'])
def health():
    """Health check."""
    return jsonify({
        "status": "healthy",
        "service": "mcp-knowledge-server",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/mcp/tools', methods=['GET'])
def list_tools():
    """List available MCP tools."""
    return jsonify({
        "tools": list(TOOLS.values())
    })

@app.route('/mcp/call', methods=['POST'])
async def call_tool():
    """Execute an MCP tool."""
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({"error": "Missing tool name"}), 400

    tool_name = data['name']
    arguments = data.get('arguments', {})

    logger.info(f"Tool call: {tool_name} with args: {arguments}")

    if tool_name not in TOOLS:
        return jsonify({"error": f"Unknown tool: {tool_name}"}), 404

    try:
        if tool_name == "search_knowledge":
            result = await search_knowledge(
                arguments.get('query', ''),
                arguments.get('limit', 5)
            )
        elif tool_name == "get_policy":
            result = await get_policy(arguments.get('policy_name', ''))
        elif tool_name == "ask_knowledge_base":
            result = await ask_knowledge_base(arguments.get('question', ''))
        elif tool_name == "list_procedures":
            result = list_procedures(arguments.get('category'))
        else:
            return jsonify({"error": f"Tool not implemented: {tool_name}"}), 501

        return jsonify({
            "content": [{"type": "text", "text": str(result)}],
            "isError": "error" in result
        })

    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        return jsonify({
            "content": [{"type": "text", "text": f"Error: {str(e)}"}],
            "isError": True
        }), 500

@app.route('/', methods=['GET'])
def index():
    """Server info."""
    return jsonify({
        "name": "MCP Knowledge Server",
        "version": "1.0.0",
        "description": "Document search and knowledge retrieval for ZZZ Accounting",
        "tools": list(TOOLS.keys())
    })

# =============================================================================
# Run Server
# =============================================================================
if __name__ == '__main__':
    logger.info(f"Starting MCP Knowledge Server on port {MCP_PORT}")
    app.run(host='0.0.0.0', port=MCP_PORT, debug=False)
