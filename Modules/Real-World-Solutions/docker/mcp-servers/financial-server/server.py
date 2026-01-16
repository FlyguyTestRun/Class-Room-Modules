"""
MCP Financial Server
====================
Model Context Protocol server for financial data access.
Includes Role-Based Access Control (RBAC) for sensitive operations.
"""

import os
import logging
from datetime import datetime
from decimal import Decimal
from typing import Optional

from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
MCP_PORT = int(os.getenv('MCP_PORT', 5003))

# Database config
DB_CONFIG = {
    'host': os.getenv('UNIFIED_DB_HOST', 'unified-db'),
    'port': int(os.getenv('UNIFIED_DB_PORT', 5432)),
    'dbname': os.getenv('UNIFIED_DB_NAME', 'zzz_unified'),
    'user': os.getenv('UNIFIED_DB_USER', 'unified_admin'),
    'password': os.getenv('UNIFIED_DB_PASSWORD', 'unified_secure_2024')
}

# =============================================================================
# Role-Based Access Control
# =============================================================================

# Define role hierarchy and permissions
ROLES = {
    "CFO": {
        "level": 100,
        "permissions": ["view_financials", "view_sensitive", "modify_financials", "generate_reports", "view_all_clients"]
    },
    "Financial_Director": {
        "level": 90,
        "permissions": ["view_financials", "view_sensitive", "generate_reports", "view_all_clients"]
    },
    "Senior_Accountant": {
        "level": 70,
        "permissions": ["view_financials", "generate_reports", "view_assigned_clients"]
    },
    "Staff_Accountant": {
        "level": 50,
        "permissions": ["view_financials", "view_assigned_clients"]
    },
    "Analyst": {
        "level": 30,
        "permissions": ["view_aggregate_data", "generate_reports"]
    },
    "Guest": {
        "level": 10,
        "permissions": ["view_public"]
    }
}

def check_permission(user_role: str, required_permission: str) -> bool:
    """Check if a role has a specific permission."""
    role_info = ROLES.get(user_role, ROLES["Guest"])
    return required_permission in role_info.get("permissions", [])

def get_role_level(user_role: str) -> int:
    """Get the numeric level for a role."""
    return ROLES.get(user_role, ROLES["Guest"]).get("level", 0)

# =============================================================================
# Database Functions
# =============================================================================

def get_db_connection():
    """Get database connection."""
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

def serialize_row(row: dict) -> dict:
    """Convert database row to JSON-serializable dict."""
    result = {}
    for key, value in row.items():
        if isinstance(value, Decimal):
            result[key] = float(value)
        elif isinstance(value, datetime):
            result[key] = value.isoformat()
        else:
            result[key] = value
    return result

# =============================================================================
# MCP Tool Definitions
# =============================================================================

TOOLS = {
    "get_client_financials": {
        "name": "get_client_financials",
        "description": "Get financial summary for a specific client. REQUIRES: CFO, Financial_Director, or Senior_Accountant role.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "client_id": {
                    "type": "integer",
                    "description": "The client/organization ID"
                },
                "user_role": {
                    "type": "string",
                    "description": "The requesting user's role",
                    "enum": list(ROLES.keys())
                }
            },
            "required": ["client_id", "user_role"]
        }
    },
    "search_invoices": {
        "name": "search_invoices",
        "description": "Search invoice records by client, status, or date range. Returns invoice details without sensitive payment information.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "client_name": {
                    "type": "string",
                    "description": "Client name to search (partial match)"
                },
                "status": {
                    "type": "string",
                    "description": "Invoice status filter",
                    "enum": ["PENDING", "PARTIAL", "PAID", "OVERDUE", "VOID"]
                },
                "from_date": {
                    "type": "string",
                    "description": "Start date (YYYY-MM-DD)"
                },
                "to_date": {
                    "type": "string",
                    "description": "End date (YYYY-MM-DD)"
                },
                "user_role": {
                    "type": "string",
                    "description": "The requesting user's role"
                }
            },
            "required": ["user_role"]
        }
    },
    "generate_report": {
        "name": "generate_report",
        "description": "Generate a financial report. Available reports: revenue_summary, outstanding_ar, client_aging.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "report_type": {
                    "type": "string",
                    "description": "Type of report to generate",
                    "enum": ["revenue_summary", "outstanding_ar", "client_aging"]
                },
                "user_role": {
                    "type": "string",
                    "description": "The requesting user's role"
                }
            },
            "required": ["report_type", "user_role"]
        }
    },
    "get_ar_summary": {
        "name": "get_ar_summary",
        "description": "Get accounts receivable summary - aggregate data showing total outstanding and aging buckets.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "user_role": {
                    "type": "string",
                    "description": "The requesting user's role"
                }
            },
            "required": ["user_role"]
        }
    }
}

# =============================================================================
# Tool Implementations
# =============================================================================

def get_client_financials(client_id: int, user_role: str) -> dict:
    """Get financial summary for a client. RBAC protected."""
    # Check permissions
    if not check_permission(user_role, "view_financials"):
        return {
            "error": f"Access denied. Role '{user_role}' does not have permission to view financial data.",
            "required_roles": ["CFO", "Financial_Director", "Senior_Accountant"]
        }

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get client info
        cursor.execute("""
            SELECT org_id, legal_name, tax_id, annual_revenue
            FROM organizations
            WHERE org_id = %s
        """, (client_id,))
        client = cursor.fetchone()

        if not client:
            return {"error": f"Client {client_id} not found"}

        # Get invoice summary
        cursor.execute("""
            SELECT
                COUNT(*) as total_invoices,
                SUM(total_amount) as total_billed,
                SUM(amount_paid) as total_paid,
                SUM(total_amount - amount_paid) as outstanding
            FROM invoices
            WHERE org_id = %s AND status != 'VOID'
        """, (client_id,))
        invoice_summary = cursor.fetchone()

        conn.close()

        # Sensitive data only for high-level roles
        result = {
            "client": serialize_row(dict(client)),
            "invoice_summary": serialize_row(dict(invoice_summary))
        }

        # Add tax ID only for CFO/Director
        if not check_permission(user_role, "view_sensitive"):
            result["client"]["tax_id"] = "***-**-****"  # Mask sensitive data

        return result

    except Exception as e:
        logger.error(f"Error getting client financials: {e}")
        return {"error": str(e)}

def search_invoices(user_role: str, client_name: str = None,
                   status: str = None, from_date: str = None,
                   to_date: str = None) -> dict:
    """Search invoices with filters."""
    if not check_permission(user_role, "view_financials"):
        return {"error": "Access denied"}

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT
                i.invoice_id, i.invoice_number, o.legal_name as client_name,
                i.issue_date, i.due_date, i.total_amount, i.amount_paid, i.status
            FROM invoices i
            JOIN organizations o ON i.org_id = o.org_id
            WHERE 1=1
        """
        params = []

        if client_name:
            query += " AND o.legal_name ILIKE %s"
            params.append(f"%{client_name}%")

        if status:
            query += " AND i.status = %s"
            params.append(status)

        if from_date:
            query += " AND i.issue_date >= %s"
            params.append(from_date)

        if to_date:
            query += " AND i.issue_date <= %s"
            params.append(to_date)

        query += " ORDER BY i.issue_date DESC LIMIT 50"

        cursor.execute(query, params)
        invoices = cursor.fetchall()
        conn.close()

        return {
            "count": len(invoices),
            "invoices": [serialize_row(dict(inv)) for inv in invoices]
        }

    except Exception as e:
        logger.error(f"Search invoices error: {e}")
        return {"error": str(e)}

def generate_report(report_type: str, user_role: str) -> dict:
    """Generate financial reports."""
    if not check_permission(user_role, "generate_reports"):
        return {"error": "Access denied. Report generation requires appropriate permissions."}

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if report_type == "revenue_summary":
            cursor.execute("""
                SELECT
                    COUNT(DISTINCT org_id) as client_count,
                    COUNT(*) as invoice_count,
                    COALESCE(SUM(total_amount), 0) as total_revenue,
                    COALESCE(SUM(amount_paid), 0) as collected,
                    COALESCE(SUM(total_amount - amount_paid), 0) as outstanding
                FROM invoices
                WHERE status != 'VOID'
            """)
            summary = cursor.fetchone()
            result = {
                "report": "Revenue Summary",
                "data": serialize_row(dict(summary)),
                "generated_at": datetime.utcnow().isoformat()
            }

        elif report_type == "outstanding_ar":
            cursor.execute("""
                SELECT
                    o.legal_name as client_name,
                    i.invoice_number,
                    i.issue_date,
                    i.due_date,
                    i.total_amount - i.amount_paid as balance
                FROM invoices i
                JOIN organizations o ON i.org_id = o.org_id
                WHERE i.status NOT IN ('PAID', 'VOID')
                  AND i.total_amount > i.amount_paid
                ORDER BY i.due_date
            """)
            invoices = cursor.fetchall()
            result = {
                "report": "Outstanding Accounts Receivable",
                "count": len(invoices),
                "data": [serialize_row(dict(inv)) for inv in invoices],
                "generated_at": datetime.utcnow().isoformat()
            }

        elif report_type == "client_aging":
            cursor.execute("""
                SELECT
                    o.legal_name as client_name,
                    SUM(CASE WHEN i.due_date >= CURRENT_DATE THEN i.total_amount - i.amount_paid ELSE 0 END) as current_balance,
                    SUM(CASE WHEN i.due_date < CURRENT_DATE AND i.due_date >= CURRENT_DATE - 30 THEN i.total_amount - i.amount_paid ELSE 0 END) as days_1_30,
                    SUM(CASE WHEN i.due_date < CURRENT_DATE - 30 AND i.due_date >= CURRENT_DATE - 60 THEN i.total_amount - i.amount_paid ELSE 0 END) as days_31_60,
                    SUM(CASE WHEN i.due_date < CURRENT_DATE - 60 THEN i.total_amount - i.amount_paid ELSE 0 END) as over_60_days
                FROM invoices i
                JOIN organizations o ON i.org_id = o.org_id
                WHERE i.status NOT IN ('PAID', 'VOID')
                GROUP BY o.org_id, o.legal_name
                HAVING SUM(i.total_amount - i.amount_paid) > 0
                ORDER BY SUM(i.total_amount - i.amount_paid) DESC
            """)
            aging = cursor.fetchall()
            result = {
                "report": "Client Aging Report",
                "count": len(aging),
                "data": [serialize_row(dict(row)) for row in aging],
                "generated_at": datetime.utcnow().isoformat()
            }
        else:
            result = {"error": f"Unknown report type: {report_type}"}

        conn.close()
        return result

    except Exception as e:
        logger.error(f"Report error: {e}")
        return {"error": str(e)}

def get_ar_summary(user_role: str) -> dict:
    """Get AR summary - available to most roles as aggregate data."""
    if not check_permission(user_role, "view_aggregate_data") and \
       not check_permission(user_role, "view_financials"):
        return {"error": "Access denied"}

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) as open_invoices,
                COALESCE(SUM(total_amount - amount_paid), 0) as total_outstanding,
                COUNT(*) FILTER (WHERE due_date < CURRENT_DATE) as overdue_count,
                COALESCE(SUM(total_amount - amount_paid) FILTER (WHERE due_date < CURRENT_DATE), 0) as overdue_amount
            FROM invoices
            WHERE status NOT IN ('PAID', 'VOID')
              AND total_amount > amount_paid
        """)
        summary = cursor.fetchone()
        conn.close()

        return {
            "ar_summary": serialize_row(dict(summary)),
            "as_of": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"AR summary error: {e}")
        return {"error": str(e)}

# =============================================================================
# MCP Endpoints
# =============================================================================

@app.route('/health', methods=['GET'])
def health():
    """Health check."""
    return jsonify({
        "status": "healthy",
        "service": "mcp-financial-server",
        "timestamp": datetime.utcnow().isoformat(),
        "rbac_enabled": True
    })

@app.route('/mcp/tools', methods=['GET'])
def list_tools():
    """List available MCP tools."""
    return jsonify({
        "tools": list(TOOLS.values())
    })

@app.route('/mcp/call', methods=['POST'])
def call_tool():
    """Execute an MCP tool."""
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({"error": "Missing tool name"}), 400

    tool_name = data['name']
    arguments = data.get('arguments', {})

    # Always require user_role
    user_role = arguments.get('user_role', 'Guest')

    logger.info(f"Tool call: {tool_name} by role: {user_role}")

    if tool_name not in TOOLS:
        return jsonify({"error": f"Unknown tool: {tool_name}"}), 404

    try:
        if tool_name == "get_client_financials":
            result = get_client_financials(
                arguments.get('client_id'),
                user_role
            )
        elif tool_name == "search_invoices":
            result = search_invoices(
                user_role,
                arguments.get('client_name'),
                arguments.get('status'),
                arguments.get('from_date'),
                arguments.get('to_date')
            )
        elif tool_name == "generate_report":
            result = generate_report(
                arguments.get('report_type'),
                user_role
            )
        elif tool_name == "get_ar_summary":
            result = get_ar_summary(user_role)
        else:
            return jsonify({"error": f"Tool not implemented: {tool_name}"}), 501

        is_error = "error" in result

        return jsonify({
            "content": [{"type": "text", "text": str(result)}],
            "isError": is_error
        })

    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        return jsonify({
            "content": [{"type": "text", "text": f"Error: {str(e)}"}],
            "isError": True
        }), 500

@app.route('/roles', methods=['GET'])
def list_roles():
    """List available roles and their permissions."""
    return jsonify({
        "roles": {role: info["permissions"] for role, info in ROLES.items()}
    })

@app.route('/', methods=['GET'])
def index():
    """Server info."""
    return jsonify({
        "name": "MCP Financial Server",
        "version": "1.0.0",
        "description": "Financial data access with RBAC for ZZZ Accounting",
        "rbac_enabled": True,
        "tools": list(TOOLS.keys()),
        "available_roles": list(ROLES.keys())
    })

# =============================================================================
# Run Server
# =============================================================================
if __name__ == '__main__':
    logger.info(f"Starting MCP Financial Server on port {MCP_PORT}")
    logger.info(f"RBAC enabled with {len(ROLES)} roles")
    app.run(host='0.0.0.0', port=MCP_PORT, debug=False)
