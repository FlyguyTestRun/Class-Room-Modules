# ZZZ Financial Services - Data Integration Platform

> **Enterprise Data Integration & AI Training Module**

---

## Executive Summary

This training module simulates a real-world M&A data integration scenario. **ZZZ Financial Services** is acquiring **AAA Accounting**, a small regional firm with 15 years of legacy data stored in poorly maintained systems.

**Your Mission:** Build the complete integration platform that merges AAA's messy data into ZZZ's clean systems, creates an AI-powered knowledge base, and delivers a modern web interface for the merged organization.

---

## Scenario Overview

| Entity | Role | Data Quality |
|--------|------|--------------|
| **ZZZ Financial Services** | Acquirer (clean data, proper schemas) | Gold Standard |
| **AAA Accounting** | Target acquisition (15 years of messy legacy data) | Needs cleaning |
| **BBB Construction** | Optional exercise (different schema patterns) | JSON/UUID practice |

### The Real-World Problem

AAA Accounting's legacy system has:
- Poor naming conventions (`cust_master`, `CUST_NUM`)
- Inconsistent data formats (multiple phone/date formats)
- Duplicate records across systems
- Missing data, NULL values, "TBD" placeholders
- Documents scattered with no organization
- No data governance or audit trail

### Your Solution

Build an integration platform that:
1. **Merges** AAA's data into ZZZ's unified schema
2. **Cleans** and normalizes inconsistent data
3. **Deduplicates** overlapping client records
4. **Creates** an AI knowledge base using RAG
5. **Provides** MCP tools for Claude integration
6. **Delivers** a React dashboard for the team

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│              ZZZ Financial Services Integration Platform                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  LEGACY TIER (Source Systems)                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                     │
│  │ ZZZ Primary │  │ AAA Legacy  │  │BBB Optional │                     │
│  │ PostgreSQL  │  │ PostgreSQL  │  │ PostgreSQL  │                     │
│  │ Port 5433   │  │ Port 5434   │  │ Port 5435   │                     │
│  │ (Clean)     │  │ (Messy)     │  │ (JSON/UUID) │                     │
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
│  │ PostgreSQL  │  │ Vectors     │  │ Cache/Queue │                     │
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

## Project Components

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Main walkthrough guide (this file) |
| `TODO.md` | Detailed task tracking with beginner explanations |
| `.env.template` | Environment variable configuration template |

### Container Stack (12 Services)

| # | Service | Port | Purpose |
|---|---------|------|---------|
| 1 | zzz-legacy-db | 5433 | ZZZ Financial Services (clean schema) |
| 2 | aaa-legacy-db | 5434 | AAA Accounting (messy legacy data) |
| 3 | bbb-legacy-db | 5435 | BBB Construction (optional - JSON/UUID) |
| 4 | unified-db | 5436 | Merged clean database |
| 5 | redis | 6379 | Cache and job queue |
| 6 | chromadb | 8000 | Vector database for RAG |
| 7 | ollama | 11434 | Local LLM (Mistral 7B) |
| 8 | rag-api | 5001 | RAG Flask service |
| 9 | mcp-knowledge | 5002 | Knowledge MCP server |
| 10 | mcp-financial | 5003 | Financial MCP server (RBAC) |
| 11 | frontend | 3001 | React application |
| 12 | prometheus | 9091 | Metrics collection |

### Docker Files

| Component | Files | Purpose |
|-----------|-------|---------|
| **Orchestration** | `docker-compose.yml` | 12-container stack definition |
| **ZZZ Database** | `docker/legacy-dbs/zzz-db/Dockerfile`, `init.sql` | Clean schema with 15 clients |
| **AAA Database** | `docker/legacy-dbs/aaa-db/Dockerfile`, `init.sql` | Messy schema with duplicates, bad formatting |
| **BBB Database** | `docker/legacy-dbs/bbb-db/Dockerfile`, `init.sql` | Different schema with UUIDs, JSON columns |
| **Unified DB** | `docker/unified-db/Dockerfile`, `schema.sql` | Clean target schema with data lineage tracking |
| **RAG API** | `docker/rag-api/Dockerfile`, `requirements.txt`, `app.py` | LangChain + ChromaDB + Ollama integration |
| **MCP Knowledge** | `docker/mcp-servers/knowledge-server/*` | Document search tools for Claude |
| **MCP Financial** | `docker/mcp-servers/financial-server/*` | RBAC-protected financial tools |
| **React Frontend** | `docker/frontend/*` | Full Vite + Tailwind setup |
| **Monitoring** | `monitoring/prometheus.yml` | Metrics collection config |

---

## Professional Tools Stack (All FREE)

### Data Integration & Quality

| Tool | Purpose | Why It's Professional | Install |
|------|---------|----------------------|---------|
| **Great Expectations** | Data validation & profiling | Used by Airbnb, Shopify for data quality | `pip install great-expectations` |
| **dbt (Data Build Tool)** | Data transformation | Industry standard for analytics engineering | `pip install dbt-postgres` |
| **Apache Airflow** | Workflow orchestration | Enterprise ETL scheduling | Docker available |
| **Pandas Profiling** | Automated data profiling | Quick data quality reports | `pip install ydata-profiling` |
| **Faker** | Test data generation | Realistic mock data | `pip install faker` |

### RAG & Vector Search

| Tool | Purpose | Why It's Professional | Install |
|------|---------|----------------------|---------|
| **LangChain** | RAG framework | Industry standard for LLM apps | `pip install langchain` |
| **LlamaIndex** | Document indexing | Excellent for complex documents | `pip install llama-index` |
| **Unstructured.io** | Document parsing | Handles PDF, DOCX, images, etc. | `pip install unstructured` |
| **Instructor** | Structured LLM output | Type-safe AI responses | `pip install instructor` |
| **ChromaDB** | Vector database | Lightweight, embedded | `pip install chromadb` |

### Local LLM Stack

| Tool | Purpose | Size | Command |
|------|---------|------|---------|
| **Ollama** | LLM runtime | N/A | `ollama serve` |
| **Mistral 7B** | General purpose LLM | ~4GB | `ollama pull mistral` |
| **Llama 2 7B** | Instruction following | ~4GB | `ollama pull llama2` |
| **CodeLlama 7B** | Code generation | ~4GB | `ollama pull codellama` |
| **Phi-2** | Lightweight, fast | ~1.7GB | `ollama pull phi` |
| **all-MiniLM-L6-v2** | Embeddings | 22MB | Via sentence-transformers |

### API Development

| Tool | Purpose | Why It's Professional | Install |
|------|---------|----------------------|---------|
| **FastAPI** | Modern async API framework | Auto OpenAPI/Swagger docs | `pip install fastapi` |
| **Flask** | Lightweight API framework | Simple, flexible | `pip install flask` |
| **Pydantic** | Data validation | Type safety, serialization | `pip install pydantic` |
| **HTTPx** | Async HTTP client | Production-grade requests | `pip install httpx` |
| **Tenacity** | Retry logic | Enterprise resilience patterns | `pip install tenacity` |

### Testing & Quality

| Tool | Purpose | Why It's Professional | Install |
|------|---------|----------------------|---------|
| **pytest** | Testing framework | Python standard | `pip install pytest` |
| **pytest-asyncio** | Async test support | For async APIs | `pip install pytest-asyncio` |
| **Hypothesis** | Property-based testing | Finds edge cases automatically | `pip install hypothesis` |
| **testcontainers** | Integration testing | Real database testing | `pip install testcontainers` |
| **coverage** | Code coverage | Quality metrics | `pip install coverage` |

### Observability & Monitoring

| Tool | Purpose | Why It's Professional | Install |
|------|---------|----------------------|---------|
| **OpenTelemetry** | Distributed tracing | Industry standard | `pip install opentelemetry-api` |
| **Structlog** | Structured logging | Production logging best practice | `pip install structlog` |
| **Sentry** | Error tracking | Free tier, real-time alerts | `pip install sentry-sdk` |
| **Prometheus** | Metrics collection | Cloud-native monitoring | Docker |
| **Grafana** | Visualization | Dashboards, alerting | Docker |
| **prometheus-flask-exporter** | Flask metrics | API instrumentation | `pip install prometheus-flask-exporter` |

### Development Workflow

| Tool | Purpose | Why It's Professional | Install |
|------|---------|----------------------|---------|
| **Pre-commit** | Git hooks | Code quality gates | `pip install pre-commit` |
| **Ruff** | Python linter | Fast, replaces flake8/isort | `pip install ruff` |
| **Black** | Code formatter | Consistent style | `pip install black` |
| **Typer** | CLI apps | Beautiful terminal interfaces | `pip install typer` |
| **Rich** | Console output | Professional terminal UI | `pip install rich` |
| **python-dotenv** | Environment management | Config from .env files | `pip install python-dotenv` |

### Frontend (React)

| Tool | Purpose | Why It's Professional | Install |
|------|---------|----------------------|---------|
| **Vite** | Build tool | Fast dev server, HMR | `npm create vite@latest` |
| **React 18** | UI framework | Industry standard | Via Vite |
| **TailwindCSS** | Utility CSS | Rapid styling | `npm install tailwindcss` |
| **React Query** | Data fetching | Caching, sync state | `npm install @tanstack/react-query` |
| **React Router** | Routing | SPA navigation | `npm install react-router-dom` |
| **Lucide React** | Icons | Clean, consistent icons | `npm install lucide-react` |
| **Axios** | HTTP client | API requests | `npm install axios` |

---

## Data Quality Challenges (AAA Legacy)

The AAA Accounting database intentionally includes real-world data problems:

### Schema Issues
- **Poor naming:** `cust_master`, `CUST_NUM`, `inv_dt`
- **Inconsistent types:** Dates as strings, money as floats
- **Missing constraints:** No primary keys on some tables
- **Multiple columns for same data:** `email1`, `email2`, `email3`

### Data Quality Issues
- **Duplicates:** Same client appears multiple times with slight variations
- **Inconsistent naming:** "ACME Corp" vs "Acme Corporation" vs "acme corp."
- **Mixed phone formats:** `(555) 123-4567`, `555-123-4567`, `5551234567`
- **Address chaos:** Full address in single field, no normalization
- **Missing data:** NULLs, empty strings, "N/A", "TBD"
- **Encoding problems:** UTF-8 vs Latin-1 characters

### What Students Will Learn
| Issue | Technique | Tool |
|-------|-----------|------|
| Duplicates | Fuzzy matching, deduplication | Great Expectations, Pandas |
| Naming inconsistencies | Text normalization | Python string methods |
| Format variations | Regular expressions, parsing | Pandas, regex |
| Schema mismatch | Column mapping | dbt, Pandas |
| Data validation | Expectations, constraints | Great Expectations |

---

## Quick Start

### Prerequisites

- Docker Desktop 4.0+
- Python 3.10+
- Node.js 20+
- 16GB RAM (Ollama needs 8GB for Mistral)
- 20GB free disk space

### 1. Start the Stack

```bash
cd "C:\CoreSkills4ai\ClassRoom Modules\Modules\Real-World-Solutions"
docker-compose up -d
```

### 2. Verify Services

```bash
docker ps  # Should show 12 containers

# Test endpoints
curl http://localhost:5001/health
curl http://localhost:8000/api/v1/heartbeat
```

### 3. Pull LLM Model

```bash
docker exec -it ollama ollama pull mistral
```

### 4. Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| React Frontend | http://localhost:3001 | - |
| RAG API | http://localhost:5001 | - |
| Grafana | http://localhost:3000 | admin / admin |
| ChromaDB | http://localhost:8000 | - |

---

## Learning Path

### Week 1: Foundation
- **Day 1-2:** Environment setup, Docker basics
- **Day 3-4:** Data discovery, explore legacy databases
- **Day 5:** Document data quality issues

### Week 2: Integration
- **Day 6-7:** Build ETL extraction scripts
- **Day 8-9:** Data transformation and cleaning
- **Day 10:** Load into unified database

### Week 3: AI/RAG
- **Day 11-12:** Document processing, embeddings
- **Day 13-14:** RAG system implementation
- **Day 15:** MCP server integration

### Week 4: Frontend & Polish
- **Day 16-17:** React dashboard development
- **Day 18-19:** End-to-end testing
- **Day 20:** Demo and deployment

---

## Integration with CoreSkills4ai Platform

This module integrates with the existing CoreSkills4ai Command Center:

### Shared Infrastructure
- **Grafana (Port 3000):** Unified monitoring for both stacks
- **Docker Network:** Services can communicate
- **Common Patterns:** Health checks, restart policies, logging

### Port Allocation
| Stack | Ports |
|-------|-------|
| Command Center | 5000, 5432, 6379, 3000, 9090 |
| Real-World-Solutions | 5001-5003, 5433-5436, 8000, 11434, 3001, 9091 |

---

## API Reference

### RAG API (Port 5001)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/api/v1/search` | POST | Search documents |
| `/api/v1/ask` | POST | Ask question (RAG) |
| `/api/v1/chat` | POST | Simple chat (no RAG) |
| `/api/v1/documents` | GET | List indexed documents |
| `/api/v1/clients/search` | GET | Search clients |
| `/api/v1/models` | GET | List LLM models |

### MCP Servers

**Knowledge Server (Port 5002):**
- `search_knowledge` - Search company documents
- `get_policy` - Retrieve specific policies
- `ask_knowledge_base` - RAG Q&A
- `list_procedures` - List accounting procedures

**Financial Server (Port 5003):**
- `get_client_financials` - Client financials (RBAC)
- `search_invoices` - Search invoice records
- `generate_report` - Create financial reports
- `get_ar_summary` - AR summary

---

## Troubleshooting

### Container Issues
```bash
docker logs [container_name]
docker-compose restart [service_name]
docker-compose down -v  # Nuclear option
```

### Ollama Issues
```bash
docker exec -it ollama ollama list
docker exec -it ollama ollama pull mistral
```

### Database Connection
```bash
docker exec -it zzz-legacy-db psql -U zzz_admin -d zzz_accounting
docker exec -it aaa-legacy-db psql -U aaa_user -d aaa_legacy
```

---

## Skills Demonstrated

| Category | Skills |
|----------|--------|
| **Data Engineering** | ETL, data quality, schema design, deduplication |
| **AI/ML** | RAG, embeddings, LLM integration, vector search |
| **Backend** | REST APIs, Flask/FastAPI, PostgreSQL, Redis |
| **Frontend** | React, TailwindCSS, data visualization |
| **DevOps** | Docker, monitoring, observability |
| **Integration** | MCP protocol, API design, RBAC |

---

## Resources

### Documentation
- [LangChain Docs](https://python.langchain.com/docs/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Ollama Docs](https://ollama.ai/)
- [Great Expectations Docs](https://docs.greatexpectations.io/)

### Learning
- [RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [dbt Learn](https://courses.getdbt.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

---

**Version:** 1.0
**Last Updated:** January 2026
**Scenario:** ZZZ Financial Services acquires AAA Accounting
