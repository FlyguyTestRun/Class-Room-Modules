# ZZZ Financial Services - Data Integration Platform

> **Project:** Real-World Data Integration & AI Training Module
> **Scenario:** ZZZ Financial Services acquires AAA Accounting
> **Duration:** 4 weeks part-time
> **Difficulty:** Beginner to Intermediate

---

## What You're Building

You're building a **complete enterprise data integration platform** that solves a real-world problem:

**The Business Problem:**
**ZZZ Financial Services** is acquiring **AAA Accounting**, a small regional accounting firm with 15 years of client data stored in legacy systems.

The challenge? AAA Accounting has:
- Legacy database with poor naming conventions
- Inconsistent data formats (phone numbers, addresses, dates)
- Duplicate client records
- Messy, unstructured data
- Documents scattered across file shares
- No data governance or quality standards

**Note:** BBB Construction data is included as an optional advanced exercise for students wanting to practice with JSON/UUID schemas.

**Your Solution:**
- Merge AAA's messy data into ZZZ's clean database
- Build an AI assistant that can answer questions about clients
- Create a modern web interface for the team
- Automate routine tasks

---

## Why This Matters (Learning Objectives)

| Skill | Real-World Application |
|-------|----------------------|
| Data Integration | 70% of IT projects involve legacy data migration |
| ETL Pipelines | Every enterprise needs data cleaning automation |
| RAG Systems | AI assistants are the future of enterprise search |
| MCP Servers | New standard for AI tool integration |
| Full-Stack Development | Complete application from database to UI |

---

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Docker Desktop** installed and running
  - Why: Containers isolate each service, making deployment predictable
  - Test: `docker --version` should return version 20+

- [ ] **Python 3.10+** installed
  - Why: We use Python for ETL scripts, RAG, and APIs
  - Test: `python --version` should return 3.10 or higher

- [ ] **Node.js 18+** installed
  - Why: React frontend requires Node.js
  - Test: `node --version` should return 18+

- [ ] **Git** installed
  - Why: Version control and collaboration
  - Test: `git --version`

- [ ] **8GB+ RAM** available
  - Why: Running 12 containers + local LLM requires memory
  - The Ollama LLM alone needs ~4GB

- [ ] **20GB+ disk space**
  - Why: Docker images, LLM models, and databases need space

---

## Phase 1: Environment Setup
**Time:** 2-3 hours | **Difficulty:** Beginner

### What You'll Learn
- How Docker Compose orchestrates multiple services
- How containers communicate via networks
- How to verify service health

### Tasks

#### 1.1 Clone and Explore the Repository
```bash
# Navigate to the module directory
cd "C:\CoreSkills4ai\ClassRoom Modules\Modules\Real-World-Solutions"

# Explore the structure
ls -la
```

**Why this structure?**
```
Real-World-Solutions/
├── docker/           # Container definitions (each service isolated)
├── data/             # Mock data files (CSV, JSON)
├── documents/        # Mock documents for RAG (PDFs, etc.)
├── scripts/          # Python automation scripts
├── labs/             # Your exercises
├── tests/            # Automated tests
└── monitoring/       # Grafana dashboards
```

#### 1.2 Start All Services
```bash
# Start the entire stack
docker-compose up -d

# Watch the startup (takes 2-3 minutes first time)
docker-compose logs -f
```

**What's happening:**
1. Docker downloads images for PostgreSQL, Redis, ChromaDB, Ollama
2. Each container starts in isolation
3. Health checks verify services are ready
4. Network connections established between containers

#### 1.3 Verify Services
```bash
# Check all containers are running
docker ps

# You should see 12 containers:
# - zzz-legacy-db (port 5433)
# - aaa-legacy-db (port 5434)
# - bbb-legacy-db (port 5435)
# - unified-db (port 5436)
# - redis (port 6379)
# - chromadb (port 8000)
# - ollama (port 11434)
# - rag-api (port 5001)
# - mcp-knowledge (port 5002)
# - mcp-financial (port 5003)
# - frontend (port 3001)
# - grafana (port 3000)
```

#### 1.4 Test Individual Services
```bash
# Test RAG API
curl http://localhost:5001/health

# Test Ollama (may take a minute to load model)
curl http://localhost:11434/api/tags

# Test ChromaDB
curl http://localhost:8000/api/v1/heartbeat
```

### Success Criteria
- [ ] All 12 containers show "healthy" or "Up"
- [ ] Can access Grafana at http://localhost:3000
- [ ] RAG API returns health status
- [ ] No error messages in logs

---

## Phase 2: Data Discovery
**Time:** 3-4 hours | **Difficulty:** Beginner

### What You'll Learn
- How to explore unfamiliar databases
- How to identify data quality issues
- Why data profiling is essential before integration

### The Problem

You've inherited three databases, each with different:
- **Schema designs** (column names, data types)
- **Data quality** (nulls, duplicates, inconsistencies)
- **Business logic** (how IDs work, what fields mean)

### Tasks

#### 2.1 Connect to Legacy Databases

**ZZZ Accounting (Clean - the "good" example)**
```bash
# Connect to ZZZ database
docker exec -it zzz-legacy-db psql -U zzz_user -d zzz_accounting

# Explore tables
\dt

# View schema
\d clients

# Sample data
SELECT * FROM clients LIMIT 5;
```

**AAA Accounting (Messy - has problems)**
```bash
# Connect to AAA database
docker exec -it aaa-legacy-db psql -U aaa_user -d aaa_accounting

# Explore tables
\dt

# Notice: Different table names!
\d cust_master

# Look at the messy data
SELECT * FROM cust_master LIMIT 10;
```

**BBB Construction (Different schema entirely)**
```bash
# Connect to BBB database
docker exec -it bbb-legacy-db psql -U bbb_user -d bbb_construction

# Different structure
\d contractors

# JSON columns!
SELECT id, business_name, primary_contact FROM contractors LIMIT 5;
```

#### 2.2 Document Data Quality Issues

Create a data quality report. Look for:

| Issue Type | Where to Find It | Why It's a Problem |
|------------|------------------|-------------------|
| **Duplicate records** | Same client in AAA and ZZZ | Will create duplicate entries |
| **Inconsistent naming** | "ACME Corp" vs "Acme Corporation" | Can't match records |
| **Missing data** | NULL values, empty strings | Incomplete records |
| **Format variations** | Phone: (555) 123-4567 vs 5551234567 | Can't search consistently |
| **Schema mismatch** | `tax_id` vs `ein` vs `federal_id` | Different column names for same concept |
| **Data type conflicts** | Integer ID vs UUID vs String | Can't join tables |

#### 2.3 Run Data Profiling Queries

```sql
-- Count records in each database
-- ZZZ
SELECT COUNT(*) as total_clients FROM clients;

-- AAA
SELECT COUNT(*) as total_customers FROM cust_master;

-- BBB
SELECT COUNT(*) as total_contractors FROM contractors;

-- Find potential duplicates (same company in multiple DBs)
-- This query concept - you'll implement it
-- Look for matching tax_id/ein/federal_id values
```

### Success Criteria
- [ ] Connected to all 3 legacy databases
- [ ] Documented at least 5 data quality issues
- [ ] Identified potential duplicate records
- [ ] Understand the schema differences

---

## Phase 3: Data Integration Pipeline (ETL)
**Time:** 6-8 hours | **Difficulty:** Intermediate

### What You'll Learn
- Extract-Transform-Load (ETL) patterns
- Data cleaning techniques
- Handling edge cases (nulls, duplicates, encoding)

### The Goal

Build Python scripts that:
1. **Extract** data from 3 legacy databases
2. **Transform** (clean, normalize, deduplicate)
3. **Load** into the unified database

### Tasks

#### 3.1 Create Extraction Script

**File:** `scripts/etl/extract.py`

```python
"""
Extract data from legacy databases.

WHY: We need to pull data from each source before we can clean it.
Each database has different connection parameters and schemas.
"""
import psycopg2
import pandas as pd
from typing import Dict, Any

def extract_zzz_clients() -> pd.DataFrame:
    """
    Extract from ZZZ Accounting (the clean source).

    This is our "gold standard" - well-structured data.
    We'll use this as the baseline for data quality.
    """
    conn = psycopg2.connect(
        host="localhost",
        port=5433,
        database="zzz_accounting",
        user="zzz_user",
        password="zzz_password"
    )

    query = """
    SELECT
        client_id,
        company_name,
        tax_id,
        contact_email,
        created_date
    FROM clients
    """

    df = pd.read_sql(query, conn)
    conn.close()

    # Add source tracking
    df['source_system'] = 'ZZZ'

    return df

def extract_aaa_customers() -> pd.DataFrame:
    """
    Extract from AAA Accounting (the messy source).

    CHALLENGES:
    - Different column names (cust_num vs client_id)
    - Multiple email columns
    - Address in single field
    - Inconsistent formatting
    """
    # TODO: Implement extraction
    pass

def extract_bbb_contractors() -> pd.DataFrame:
    """
    Extract from BBB Construction (JSON schema).

    CHALLENGES:
    - UUID instead of integer IDs
    - JSON columns need flattening
    - Different business entity type
    """
    # TODO: Implement extraction
    pass
```

#### 3.2 Create Transformation Script

**File:** `scripts/etl/transform.py`

```python
"""
Transform and clean extracted data.

WHY: Raw data is messy. We need to:
1. Standardize column names
2. Clean formats (phones, addresses)
3. Handle missing values
4. Remove duplicates
5. Normalize company names
"""
import pandas as pd
import re
from typing import Optional

def standardize_column_names(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """
    Rename columns to unified schema.

    WHY: Each source uses different names for the same concept.
    - ZZZ: client_id, company_name, tax_id
    - AAA: cust_num, cust_name, ein
    - BBB: id, business_name, federal_id

    We standardize to: entity_id, entity_name, tax_identifier
    """
    column_mapping = {
        'ZZZ': {
            'client_id': 'entity_id',
            'company_name': 'entity_name',
            'tax_id': 'tax_identifier',
            'contact_email': 'primary_email'
        },
        'AAA': {
            'cust_num': 'entity_id',
            'cust_name': 'entity_name',
            'ein': 'tax_identifier',
            'email1': 'primary_email'
        },
        'BBB': {
            'id': 'entity_id',
            'business_name': 'entity_name',
            'federal_id': 'tax_identifier'
        }
    }

    return df.rename(columns=column_mapping.get(source, {}))

def clean_phone_number(phone: Optional[str]) -> Optional[str]:
    """
    Normalize phone numbers to consistent format.

    INPUT EXAMPLES:
    - "(555) 123-4567"
    - "555-123-4567"
    - "5551234567"
    - "+1 555 123 4567"

    OUTPUT: "555-123-4567"

    WHY: Users search for clients by phone. Without normalization,
    searching "555-123-4567" won't find "(555) 123-4567".
    """
    if not phone or pd.isna(phone):
        return None

    # Remove all non-digits
    digits = re.sub(r'\D', '', str(phone))

    # Handle country code
    if len(digits) == 11 and digits.startswith('1'):
        digits = digits[1:]

    # Format as XXX-XXX-XXXX
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"

    return phone  # Return original if can't parse

def normalize_company_name(name: Optional[str]) -> Optional[str]:
    """
    Standardize company names for matching.

    WHY: The same company appears differently in each database:
    - "ACME Corp"
    - "Acme Corporation"
    - "acme corp."
    - "ACME CORPORATION, INC."

    We normalize to enable duplicate detection.
    """
    if not name or pd.isna(name):
        return None

    # Convert to uppercase
    name = str(name).upper().strip()

    # Remove common suffixes
    suffixes = [
        ', INC.', ', INC', ' INC.', ' INC',
        ', LLC', ' LLC',
        ', CORP.', ', CORP', ' CORP.', ' CORP',
        ' CORPORATION', ', CORPORATION'
    ]

    for suffix in suffixes:
        if name.endswith(suffix):
            name = name[:-len(suffix)]

    # Remove extra whitespace
    name = ' '.join(name.split())

    return name

def deduplicate_records(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate records across sources.

    STRATEGY:
    1. Match on tax_identifier (most reliable)
    2. Match on normalized company name (fuzzy)
    3. Keep record from most trusted source (ZZZ > AAA > BBB)

    WHY: After merging 3 databases, we'll have duplicates.
    A client might exist in both ZZZ and AAA databases.
    """
    # TODO: Implement deduplication logic
    pass
```

#### 3.3 Create Loading Script

**File:** `scripts/etl/load.py`

```python
"""
Load transformed data into unified database.

WHY: After cleaning, we need to persist the data in our
new unified schema for the application to use.
"""
import psycopg2
import pandas as pd

def create_unified_schema(conn):
    """
    Create the target schema for merged data.

    DESIGN DECISIONS:
    - Use SERIAL for auto-incrementing IDs
    - Keep source_system for audit trail
    - Add timestamps for tracking
    """
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS unified_entities (
        id SERIAL PRIMARY KEY,
        original_id VARCHAR(50),
        source_system VARCHAR(10),
        entity_name VARCHAR(200),
        entity_name_normalized VARCHAR(200),
        tax_identifier VARCHAR(50),
        primary_email VARCHAR(100),
        primary_phone VARCHAR(20),
        address_line1 VARCHAR(200),
        address_city VARCHAR(100),
        address_state VARCHAR(50),
        address_zip VARCHAR(20),
        entity_type VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Indexes for fast searching
    CREATE INDEX IF NOT EXISTS idx_entity_name
        ON unified_entities(entity_name_normalized);
    CREATE INDEX IF NOT EXISTS idx_tax_id
        ON unified_entities(tax_identifier);
    """)

    conn.commit()

def load_to_unified(df: pd.DataFrame, conn):
    """
    Insert transformed data into unified database.

    WHY: pandas to_sql with 'append' mode adds records.
    We use 'replace' during development, 'append' in production.
    """
    df.to_sql(
        'unified_entities',
        conn,
        if_exists='append',
        index=False
    )
```

### Success Criteria
- [ ] Extract scripts pull data from all 3 sources
- [ ] Transform scripts clean and normalize data
- [ ] Load script populates unified database
- [ ] Can query unified database with clean data

---

## Phase 4: Document Processing for RAG
**Time:** 4-5 hours | **Difficulty:** Intermediate

### What You'll Learn
- How RAG (Retrieval Augmented Generation) works
- Document chunking strategies
- Vector embeddings and semantic search

### The Concept

**RAG = Retrieval + Generation**

1. **Retrieval:** Find relevant documents using semantic search
2. **Generation:** Use LLM to generate answers based on retrieved docs

**Why RAG?**
- LLMs have knowledge cutoffs (don't know your company data)
- RAG gives LLMs access to your specific documents
- Reduces hallucination by grounding answers in real sources

### Tasks

#### 4.1 Understand Document Processing Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Documents  │ -> │   Chunking  │ -> │  Embedding  │ -> │  ChromaDB   │
│ (PDF, DOCX) │    │ (Split text)│    │ (Vectors)   │    │ (Storage)   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

**Why Chunking?**
- LLMs have token limits (can't process entire documents)
- Smaller chunks enable more precise retrieval
- Typical chunk size: 500-1000 characters

**Why Embeddings?**
- Transform text into numerical vectors
- Similar text = similar vectors
- Enables semantic search (meaning, not just keywords)

#### 4.2 Create Document Ingestion Script

**File:** `scripts/rag/ingest_documents.py`

```python
"""
Ingest documents into ChromaDB for RAG.

WHY: We need to process various document formats,
chunk them appropriately, and store embeddings
for semantic search.
"""
from langchain.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    CSVLoader,
    TextLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import os

def load_documents(docs_path: str):
    """
    Load documents from various formats.

    SUPPORTED FORMATS:
    - PDF: Contracts, reports, scanned docs
    - DOCX: Procedures, policies
    - CSV: Data exports, client lists
    - TXT/MD: Notes, READMEs

    WHY MULTIPLE FORMATS: Real companies have documents
    in various formats accumulated over years.
    """
    documents = []

    for root, dirs, files in os.walk(docs_path):
        for file in files:
            file_path = os.path.join(root, file)

            if file.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            elif file.endswith('.docx'):
                loader = Docx2txtLoader(file_path)
            elif file.endswith('.csv'):
                loader = CSVLoader(file_path)
            elif file.endswith(('.txt', '.md')):
                loader = TextLoader(file_path)
            else:
                continue

            docs = loader.load()

            # Add metadata for source tracking
            for doc in docs:
                doc.metadata['source_file'] = file
                doc.metadata['source_path'] = root

            documents.extend(docs)

    return documents

def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    """
    Split documents into chunks for embedding.

    PARAMETERS:
    - chunk_size: Target characters per chunk
    - chunk_overlap: Characters shared between chunks

    WHY OVERLAP: Ensures context isn't lost at boundaries.
    If a sentence spans two chunks, overlap preserves it.

    EXAMPLE:
    Original: "The client ACME Corp signed contract #123 on Jan 1."
    Chunk 1: "The client ACME Corp signed contract"
    Chunk 2: "Corp signed contract #123 on Jan 1."
    (Overlap preserves "Corp signed contract")
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]  # Try splitting at paragraphs first
    )

    return splitter.split_documents(documents)

def create_embeddings():
    """
    Initialize embedding model.

    MODEL: all-MiniLM-L6-v2
    - Size: 22MB (very lightweight)
    - Speed: Fast on CPU
    - Quality: Good for semantic search
    - Dimensions: 384

    WHY THIS MODEL: Best balance of size, speed, and quality
    for classroom/local deployment. No API costs!
    """
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}  # Use GPU if available
    )

def store_in_chromadb(chunks, embeddings, persist_dir="./chroma_db"):
    """
    Store document chunks with embeddings in ChromaDB.

    WHY CHROMADB:
    - Lightweight (single-file storage)
    - Easy to use API
    - Persistence built-in
    - Good for small-medium datasets
    """
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    # Persist to disk
    vectorstore.persist()

    return vectorstore

# Main ingestion pipeline
if __name__ == "__main__":
    print("Loading documents...")
    docs = load_documents("./documents")
    print(f"Loaded {len(docs)} documents")

    print("Chunking documents...")
    chunks = chunk_documents(docs)
    print(f"Created {len(chunks)} chunks")

    print("Creating embeddings...")
    embeddings = create_embeddings()

    print("Storing in ChromaDB...")
    vectorstore = store_in_chromadb(chunks, embeddings)
    print("Done! Vector store ready for queries.")
```

### Success Criteria
- [ ] All documents loaded from documents/ folder
- [ ] Documents chunked appropriately
- [ ] Embeddings generated using all-MiniLM-L6-v2
- [ ] ChromaDB populated and persisted

---

## Phase 5: RAG System Implementation
**Time:** 6-8 hours | **Difficulty:** Intermediate

### What You'll Learn
- How to query vector databases
- How to prompt local LLMs effectively
- Building RAG API endpoints

### Tasks

#### 5.1 Create RAG Query Function

**File:** `scripts/rag/query_rag.py`

```python
"""
Query the RAG system for answers.

FLOW:
1. User asks question
2. Embed the question
3. Search ChromaDB for similar chunks
4. Build prompt with context
5. Send to Ollama (local LLM)
6. Return answer with sources
"""
from langchain.llms import Ollama
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate

def query_rag(question: str, k: int = 3) -> dict:
    """
    Answer a question using RAG.

    PARAMETERS:
    - question: Natural language question
    - k: Number of relevant chunks to retrieve

    RETURNS:
    - answer: Generated response
    - sources: List of source documents
    """
    # Load embeddings and vector store
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )

    # Retrieve relevant documents
    docs = vectorstore.similarity_search(question, k=k)

    # Build context from retrieved docs
    context = "\n\n".join([doc.page_content for doc in docs])

    # Create prompt
    prompt_template = """You are a helpful assistant for ZZZ Accounting.
Use the following context to answer the question.
If you cannot answer based on the context, say "I don't have enough information."

Context:
{context}

Question: {question}

Answer:"""

    prompt = prompt_template.format(context=context, question=question)

    # Query local LLM via Ollama
    llm = Ollama(
        model="mistral",
        base_url="http://localhost:11434"
    )

    answer = llm(prompt)

    return {
        "answer": answer,
        "sources": [
            {
                "content": doc.page_content[:200] + "...",
                "source": doc.metadata.get('source_file', 'Unknown')
            }
            for doc in docs
        ]
    }
```

### Success Criteria
- [ ] Can query RAG system with natural language
- [ ] Answers are grounded in document content
- [ ] Sources are returned with answers
- [ ] Response time < 10 seconds

---

## Phase 6-9: Coming Soon

The remaining phases will cover:
- **Phase 6:** MCP Server Integration
- **Phase 7:** React Frontend Development
- **Phase 8:** Automation & Workflow
- **Phase 9:** Testing & Deployment

---

## Quick Reference Commands

### Docker
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f [service_name]

# Restart a service
docker-compose restart [service_name]

# Remove everything (including data)
docker-compose down -v
```

### Database Access
```bash
# ZZZ Database
docker exec -it zzz-legacy-db psql -U zzz_user -d zzz_accounting

# AAA Database
docker exec -it aaa-legacy-db psql -U aaa_user -d aaa_accounting

# BBB Database
docker exec -it bbb-legacy-db psql -U bbb_user -d bbb_construction

# Unified Database
docker exec -it unified-db psql -U unified_user -d unified_accounting
```

### API Testing
```bash
# Health checks
curl http://localhost:5001/health
curl http://localhost:11434/api/tags
curl http://localhost:8000/api/v1/heartbeat

# RAG query
curl -X POST http://localhost:5001/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the tax ID for ACME Corp?"}'
```

---

## Troubleshooting

### "Container keeps restarting"
```bash
# Check logs for error
docker logs [container_name]

# Common causes:
# - Port already in use
# - Missing environment variables
# - Database connection failed
```

### "Ollama model not loading"
```bash
# Pull model manually
docker exec -it ollama ollama pull mistral

# Check available models
docker exec -it ollama ollama list
```

### "ChromaDB connection refused"
```bash
# Verify container is running
docker ps | grep chromadb

# Check health
curl http://localhost:8000/api/v1/heartbeat
```

---

## Resources

### Documentation
- [LangChain RAG Guide](https://docs.langchain.com/docs/use_cases/question_answering/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Ollama Models](https://ollama.ai/library)

### Tutorials
- [RAG from Scratch (YouTube)](https://www.youtube.com/results?search_query=rag+from+scratch)
- [LangChain Tutorial](https://python.langchain.com/docs/tutorials/)

---

**Last Updated:** January 2026
**Version:** 1.0
