# Real-World-Solutions: ZZZ Accounting Merger Integration

> **A hands-on training module for enterprise data integration, RAG systems, and agentic AI**

---

## Overview

Welcome to the **Real-World-Solutions** training module! This project simulates a real-world business scenario that IT professionals face regularly: integrating multiple legacy systems during a company merger.

### The Scenario

**ZZZ Accounting** is acquiring two companies:
- **AAA Accounting** - A regional accounting firm with legacy SaaS systems
- **BBB Construction** - A construction company's financial services division

**Your Mission:** Build the integration platform that will:
1. Merge 3 disparate databases with messy, poorly correlated data
2. Create a unified data layer for the new organization
3. Build a RAG (Retrieval Augmented Generation) system for knowledge transfer from the retiring CFO
4. Implement MCP servers for AI-assisted financial operations
5. Develop a React frontend for the merged organization

### Why This Matters

This isn't a toy project. Every skill you learn here maps directly to real enterprise work:

| Module Skill | Real-World Application |
|--------------|------------------------|
| ETL Pipelines | Data migration projects, warehouse loading |
| Data Quality | M&A due diligence, compliance audits |
| RAG Systems | Knowledge bases, customer support AI |
| MCP Servers | AI tool integration, automation |
| Containerization | DevOps, cloud deployment |

---

## Integration with CoreSkills4ai Platform

This module integrates seamlessly with the existing CoreSkills4ai Command Center:

### Shared Infrastructure
```
CoreSkills4ai Platform
├── Command Center (existing)        ← Session 1-3 work
│   ├── Flask API (Port 5000)
│   ├── PostgreSQL (Port 5432)
│   ├── Redis (Port 6379)
│   ├── Grafana (Port 3000)
│   └── Prometheus (Port 9090)
│
└── Real-World-Solutions (this module)
    ├── Legacy DBs (Ports 5433-5435)
    ├── Unified DB (Port 5436)
    ├── RAG API (Port 5001)
    ├── MCP Servers (Ports 5002-5003)
    ├── ChromaDB (Port 8000)
    ├── Ollama (Port 11434)
    └── React Frontend (Port 3001)
```

### Cross-Module Benefits
- **Shared Grafana:** Monitor both stacks from one dashboard
- **Shared Redis:** Job queuing works across modules
- **Unified Prometheus:** Metrics collection for all services
- **Common Patterns:** Flask API design, health checks, Docker networking

---

## Recommended Professional Tools (All FREE)

Based on real enterprise integration projects, here are tools that will enhance this module:

### Data Integration & Quality

| Tool | Purpose | Why It's Professional | Install |
|------|---------|----------------------|---------|
| **Great Expectations** | Data validation | Used by Airbnb, Shopify | `pip install great-expectations` |
| **dbt (Data Build Tool)** | Data transformation | Industry standard | `pip install dbt-postgres` |
| **Apache Airflow** | Workflow orchestration | Enterprise ETL | Docker available |
| **Pandas Profiling** | Data profiling | Quick data quality reports | `pip install ydata-profiling` |

### RAG & Vector Search

| Tool | Purpose | Why It's Professional | Install |
|------|---------|----------------------|---------|
| **LangChain** | RAG framework | Industry standard | `pip install langchain` |
| **LlamaIndex** | Document indexing | Excellent for complex docs | `pip install llama-index` |
| **Unstructured.io** | Document parsing | Handles any format | `pip install unstructured` |
| **Instructor** | Structured LLM output | Type-safe AI responses | `pip install instructor` |

### API Development

| Tool | Purpose | Why It's Professional | Install |
|------|---------|----------------------|---------|
| **FastAPI** | Modern API framework | Auto OpenAPI docs | `pip install fastapi` |
| **Pydantic** | Data validation | Type safety | `pip install pydantic` |
| **HTTPx** | Async HTTP client | Production-grade requests | `pip install httpx` |
| **Tenacity** | Retry logic | Enterprise resilience | `pip install tenacity` |

### Testing & Quality

| Tool | Purpose | Why It's Professional | Install |
|------|---------|----------------------|---------|
| **pytest** | Testing framework | Standard for Python | `pip install pytest` |
| **Hypothesis** | Property-based testing | Finds edge cases | `pip install hypothesis` |
| **Faker** | Test data generation | Realistic mock data | `pip install faker` |
| **testcontainers** | Integration testing | Real DB testing | `pip install testcontainers` |

### Observability

| Tool | Purpose | Why It's Professional | Install |
|------|---------|----------------------|---------|
| **OpenTelemetry** | Distributed tracing | Industry standard | `pip install opentelemetry-api` |
| **Structlog** | Structured logging | Production logging | `pip install structlog` |
| **Sentry** | Error tracking | Free tier available | `pip install sentry-sdk` |

### Development Workflow

| Tool | Purpose | Why It's Professional | Install |
|------|---------|----------------------|---------|
| **Pre-commit** | Git hooks | Code quality gates | `pip install pre-commit` |
| **Ruff** | Python linter | Fast, replaces flake8 | `pip install ruff` |
| **Typer** | CLI apps | Beautiful CLI tools | `pip install typer` |
| **Rich** | Console output | Professional terminal UI | `pip install rich` |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ZZZ Accounting Merger Platform                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  LEGACY TIER (Intentionally Messy)                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                     │
│  │ ZZZ Legacy  │  │ AAA Legacy  │  │ BBB Legacy  │                     │
│  │ PostgreSQL  │  │ PostgreSQL  │  │ PostgreSQL  │                     │
│  │ Port 5433   │  │ Port 5434   │  │ Port 5435   │                     │
│  │ (Clean)     │  │ (Messy)     │  │ (Different) │                     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                     │
│         │                │                │                             │
│         └────────────────┼────────────────┘                             │
│                          ▼                                              │
│  INTEGRATION TIER                                                       │
│              ┌───────────────────────┐                                  │
│              │   Python ETL Pipeline │                                  │
│              │   - Great Expectations│◄── Data validation               │
│              │   - Pandas transforms │◄── Data cleaning                 │
│              │   - dbt models        │◄── Business logic                │
│              └───────────┬───────────┘                                  │
│                          │                                              │
│  UNIFIED TIER                                                           │
│         ┌────────────────┼────────────────┐                             │
│         ▼                ▼                ▼                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                     │
│  │ Unified DB  │  │  ChromaDB   │  │   Redis     │                     │
│  │ PostgreSQL  │  │ Vectors     │  │  Cache/Queue│                     │
│  │ Port 5436   │  │ Port 8000   │  │ Port 6379   │                     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                     │
│         │                │                │                             │
│  API TIER                                                               │
│         └────────────────┼────────────────┘                             │
│                          ▼                                              │
│              ┌───────────────────────┐                                  │
│              │    Flask/FastAPI      │                                  │
│              │    RAG API Gateway    │◄── LangChain + Ollama            │
│              │    Port 5001          │                                  │
│              └───────────┬───────────┘                                  │
│                          │                                              │
│  AI TIER                                                                │
│         ┌────────────────┼────────────────┐                             │
│         ▼                ▼                ▼                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                     │
│  │   Ollama    │  │MCP Knowledge│  │MCP Financial│                     │
│  │ Mistral 7B  │  │   Server    │  │   Server    │                     │
│  │ Port 11434  │  │ Port 5002   │  │ Port 5003   │                     │
│  └─────────────┘  └─────────────┘  └─────────────┘                     │
│                                                                         │
│  PRESENTATION TIER                                                      │
│  ┌─────────────┐                  ┌─────────────┐                       │
│  │   React     │                  │  Grafana    │                       │
│  │  Frontend   │                  │ Monitoring  │                       │
│  │ Port 3001   │                  │ Port 3000   │                       │
│  └─────────────┘                  └─────────────┘                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Python 3.12+
- Node.js 20+ (for React frontend)
- 16GB RAM recommended (Ollama needs 8GB for Mistral)
- 20GB free disk space

### 1. Start the Full Stack

```bash
cd "C:\CoreSkills4ai\ClassRoom Modules\Modules\Real-World-Solutions"
docker-compose up -d
```

### 2. Verify All Services

```bash
# Check container health
docker ps

# Quick health check
curl http://localhost:5001/health
```

### 3. Pull the LLM Model

```bash
# This downloads Mistral 7B (~4GB)
docker exec -it ollama ollama pull mistral
```

### 4. Access the Services

| Service | URL | Credentials |
|---------|-----|-------------|
| React Frontend | http://localhost:3001 | - |
| RAG API | http://localhost:5001 | - |
| Grafana | http://localhost:3000 | admin / admin |
| ChromaDB | http://localhost:8000 | - |

---

## Learning Path

### Week 1: Foundation

**Day 1-2: Environment Setup**
- Clone and start all containers
- Explore each legacy database
- Document schema differences

**Day 3-4: Data Discovery**
- Run profiling on each database
- Identify data quality issues
- Create data quality report

**Day 5: ETL Foundation**
- Write extraction scripts
- Understand connection pooling
- Test basic queries

### Week 2: Integration

**Day 6-7: Data Transformation**
- Build cleaning functions
- Handle edge cases (nulls, duplicates)
- Normalize data formats

**Day 8-9: Data Loading**
- Create unified schema
- Load transformed data
- Validate integrity

**Day 10: Testing**
- Write pytest tests
- Validate transformations
- Document edge cases

### Week 3: AI/RAG

**Day 11-12: Document Processing**
- Process mock documents
- Generate embeddings
- Load into ChromaDB

**Day 13-14: RAG System**
- Build retrieval pipeline
- Create prompt templates
- Test Q&A functionality

**Day 15: MCP Servers**
- Create knowledge server
- Create financial server (with RBAC)
- Test with Claude Desktop

### Week 4: Frontend & Polish

**Day 16-17: React Frontend**
- Build search interface
- Create chat component
- Add visualizations

**Day 18-19: Integration**
- Connect all components
- End-to-end testing
- Performance optimization

**Day 20: Deployment**
- Documentation review
- Demo preparation
- Final presentation

---

## Module Structure

```
Real-World-Solutions/
├── README.md                    # You are here
├── TODO.md                      # Detailed task tracking
├── ARCHITECTURE.md              # Deep technical docs
├── .env.template                # Environment variables
├── docker-compose.yml           # Full stack orchestration
│
├── docker/                      # Container definitions
│   ├── legacy-dbs/              # 3 mock legacy databases
│   ├── unified-db/              # Target merged database
│   ├── rag-api/                 # RAG Flask service
│   ├── mcp-servers/             # MCP tool servers
│   └── frontend/                # React application
│
├── data/                        # Mock data files
├── documents/                   # Mock documents for RAG
├── scripts/                     # Python automation
├── labs/                        # Student exercises
├── solutions/                   # Lab solutions
├── tests/                       # Test suite
└── monitoring/                  # Grafana dashboards
```

---

## Container Services

| # | Service | Port | Purpose |
|---|---------|------|---------|
| 1 | zzz-legacy-db | 5433 | ZZZ Accounting (clean schema) |
| 2 | aaa-legacy-db | 5434 | AAA Accounting (messy schema) |
| 3 | bbb-legacy-db | 5435 | BBB Construction (different schema) |
| 4 | unified-db | 5436 | Merged clean database |
| 5 | redis | 6379 | Cache and job queue |
| 6 | chromadb | 8000 | Vector database |
| 7 | ollama | 11434 | Local LLM (Mistral 7B) |
| 8 | rag-api | 5001 | RAG Flask service |
| 9 | mcp-knowledge | 5002 | Knowledge MCP server |
| 10 | mcp-financial | 5003 | Financial MCP server |
| 11 | frontend | 3001 | React application |
| 12 | prometheus | 9091 | Metrics (new instance) |

---

## Data Quality Challenges

The legacy databases intentionally include real-world data problems:

### AAA Accounting Database (The Messy One)
- **Inconsistent naming:** "ACME Corp" vs "acme corporation" vs "A.C.M.E. Corp."
- **Multiple email columns:** email1, email2 (some have 3!)
- **Mixed phone formats:** (555) 123-4567, 555-123-4567, 5551234567
- **Full address in one field:** No city/state/zip separation
- **Sequence gaps:** Customer numbers with holes (1, 2, 5, 8, 15...)

### BBB Construction Database (The Different One)
- **UUID primary keys:** Instead of integers
- **JSON columns:** Nested data instead of normalized tables
- **Different terminology:** "contractors" vs "clients"
- **Date formats:** ISO vs American vs Unix timestamps

### Common Issues Across All
- **Duplicate records:** Same company appears in multiple DBs
- **Missing data:** NULLs, empty strings, "N/A", "TBD"
- **Encoding problems:** UTF-8 vs Latin-1 characters
- **Type mismatches:** String IDs vs Integer IDs

---

## RAG Document Challenges

The mock documents simulate real organizational chaos:

```
documents/
├── zzz_accounting/
│   ├── client_contracts/
│   │   ├── contract_2023_acme.pdf           # Clean PDF
│   │   └── contract_2024_widgets.docx        # Different format
│   └── policies/
│       └── accounting_procedures.md
│
├── aaa_accounting/
│   ├── legacy_docs/
│   │   ├── client_list_2019.xlsx            # Old Excel
│   │   ├── procedures_v2_final_FINAL.doc    # Terrible naming
│   │   └── scan_001.pdf                     # Scanned, needs OCR
│   └── emails/
│       └── important_client_notes.eml       # Email exports
│
├── bbb_construction/
│   ├── contracts/
│   │   ├── subcontractor_agreement.pdf
│   │   └── insurance_cert_2024.jpg          # Image document!
│   └── financial/
│       └── quarterly_report_q3.csv
│
└── merger_docs/
    ├── due_diligence_report.pdf
    └── cfo_knowledge_transfer.md            # Critical retiring CFO notes
```

---

## Microsoft 365 Integration (Optional)

For students with M365 access, this module includes optional integration:

### Free Tier Resources
- **Azure AD B2C:** 50,000 MAU free (SSO/Authentication)
- **Microsoft 365 Developer:** Free E5 trial (90 days, renewable)
- **Power Automate:** 750 runs/month free

### Integration Points
- SharePoint for document storage
- Microsoft Teams for notifications
- Power Automate for approval workflows
- Azure SQL as alternative database

See `labs/optional_m365_integration.md` for setup instructions.

---

## Troubleshooting

### Ollama Out of Memory
```bash
# Check Ollama logs
docker logs ollama

# Use smaller model
docker exec -it ollama ollama pull phi
```

### ChromaDB Connection Refused
```bash
# Restart ChromaDB
docker-compose restart chromadb

# Check logs
docker logs chromadb
```

### Legacy DB Connection Issues
```bash
# Verify all DBs are running
docker ps | grep legacy

# Test connection
docker exec -it zzz-legacy-db psql -U postgres -c "SELECT 1"
```

### Port Conflicts
If you have the main CoreSkills4ai stack running:
- This module uses different ports (5433-5436, 5001-5003, 8000)
- Grafana can be shared (Port 3000)
- Redis can be shared (Port 6379)

---

## API Reference

### RAG API (Port 5001)

**Health Check**
```bash
curl http://localhost:5001/health
```

**Search Documents**
```bash
curl -X POST http://localhost:5001/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the payment terms for ACME Corp?"}'
```

**Ask Question (RAG)**
```bash
curl -X POST http://localhost:5001/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What did the CFO say about Q3 projections?"}'
```

### MCP Servers

**Knowledge Server (Port 5002)**
- Tool: `search_knowledge` - Search company documents
- Tool: `get_policy` - Retrieve specific policies
- Tool: `list_procedures` - List accounting procedures

**Financial Server (Port 5003)**
- Tool: `get_client_financials` - Requires CFO/Director role
- Tool: `search_invoices` - Search invoice records
- Tool: `generate_report` - Create financial reports

---

## Next Steps After Completion

1. **Portfolio Project:** This module is demo-ready for job interviews
2. **Extend RAG:** Add more document types, improve retrieval
3. **Production Deploy:** Add auth, HTTPS, proper secrets management
4. **Advanced Topics:** Kubernetes, CI/CD, multi-tenancy

---

## Credits

- **LangChain** - RAG framework
- **Ollama** - Local LLM inference
- **ChromaDB** - Vector database
- **CoreSkills4ai** - Base platform and patterns

---

## Support

- Check TODO.md for detailed task instructions
- Review ARCHITECTURE.md for technical deep-dives
- Labs include step-by-step solutions
- Join the CoreSkills4ai community for help

---

**Happy Learning!**

*This module was designed to teach real-world skills through realistic challenges.*
