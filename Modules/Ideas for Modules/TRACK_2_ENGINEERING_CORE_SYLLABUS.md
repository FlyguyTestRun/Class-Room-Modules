# CoreSkills4AI: Track 2 - Engineering Core
**Duration:** 8 weeks self-paced | 2 full days intensive (40 hours)  
**Audience:** Junior developers, career switchers  
**Prerequisite:** Track 1 OR coding basics  
**Cert Alignment:** AWS Certified Cloud Practitioner, Developer, Solutions Architect

---

## TRACK OVERVIEW

Hands-on engineering: Build functional AI systems from API integration → production deployment. Beginner builds toy systems; advanced builds production-ready architecture.

**Full-Day Intensive (2 days, 40 hrs):**
- Day 1: M1-M3 (APIs, data, prompting) = 20 hours
- Day 2: M4-M7 (RAG, testing, deployment, capstone kickoff) = 20 hours

---

## MODULE 1: LLM BASICS & API INTEGRATION (1.5 weeks / 6 hours)

### Learning Outcomes
**Beginner:** Call OpenAI/Anthropic APIs, understand costs, basic error handling.  
**Advanced:** Model evaluation, fine-tuning trade-offs, deployment patterns.

### Syllabus

| Topic | Beginner | Advanced |
|-------|----------|----------|
| API Setup | Get API key, make first call | Rate limiting, retry logic, cost monitoring |
| Models | Pick Claude vs. GPT (which is better?) | Model selection framework (speed, cost, quality) |
| Tokens | Count tokens (affects cost) | Tokenization strategies, optimize input lengths |
| Temperature/TopP | Adjust randomness | When to use (creativity vs. determinism) |
| Cost Analysis | Your first bill | Cost attribution per user, token optimization |
| Fine-tuning | "What is it?" | When to fine-tune vs. prompt, ROI analysis |

### Hands-On Labs

**Beginner: Simple Chatbot**
```python
# Lab 1.1: First API Call
import anthropic
client = anthropic.Anthropic(api_key="your-key")
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.content[0].text)

# Lab 1.2: Cost Calculator
# Count tokens for 100 queries, calculate cost
# Deliverable: Cost report (CSV)

# Lab 1.3: Error Handling
# Handle API timeouts, rate limits, invalid requests
# Deliverable: Robust CLI chatbot with retry logic
```

**Advanced: Model Evaluation Framework**
```python
# Lab 1.1: Evaluate Claude vs. GPT vs. Open Source Models
# Task: Answer 20 test questions
# Metrics: Accuracy, latency, cost
# Deliverable: Comparison matrix

# Lab 1.2: Fine-tuning ROI Analysis
# Questions: Should we fine-tune for this task?
# Calculate: Training cost vs. inference improvement
# Deliverable: Fine-tuning recommendation report

# Lab 1.3: Production Cost Monitoring
# Build: Cost dashboard (API calls, tokens, spend/day)
# Deliverable: Flask app with cost visualization
```

### Deliverable
- **Beginner:** Simple chatbot (CLI or Streamlit) + cost report
- **Advanced:** Model evaluation framework + fine-tuning ROI analysis + cost dashboard

### Instructor Template
```
[BEGINNER]
- Live: Walk through API setup, first call (30 min)
- Hands-on: Each student makes API call, prints response (15 min)
- Lab: Build chatbot incrementally (error handling, token counting)
- Review: Code walkthrough, common mistakes

[ADVANCED]
- Case study: "Should we fine-tune or use prompt engineering?"
- Lab: Evaluate 3 models on task, cost comparison
- Project: Build cost monitoring dashboard
- Bonus: Explore fine-tuning dataset preparation
```

### Resources
- OpenAI API docs + Anthropic API docs
- Token counter: https://token-counter.llm.report
- Cost calculator template (provided)

---

## MODULE 2: DATA PIPELINES 101 (1.5 weeks / 6 hours)

### Learning Outcomes
**Beginner:** ETL basics, data flow from source → LLM, simple pipelines.  
**Advanced:** Streaming, real-time processing, scalability, data quality.

### Syllabus

| Concept | Beginner | Advanced |
|---------|----------|----------|
| ETL | Extract, Transform, Load | Idempotency, schema validation, error recovery |
| Data Flow | CSV → Processing → API | Real-time streaming, queuing, event-driven |
| Quality | "Is data clean?" | Schema enforcement, anomaly detection, SLAs |
| Storage | Local files, databases | Data warehouse, data lakes, partitioning |
| Scaling | Works for 100 rows? | Batching, parallelization, cost optimization |

### Hands-On Labs

**Beginner: Simple ETL Pipeline**
```python
# Lab 2.1: CSV → Process → LLM
import pandas as pd
# 1. Load CSV (customer feedback)
# 2. Clean: Remove duplicates, missing values
# 3. Transform: Lowercase, remove HTML
# 4. Call Claude on each row
# 5. Save results to output CSV

# Lab 2.2: Error Handling
# What if API fails mid-pipeline?
# Add checkpoints, retry logic
# Deliverable: Robust pipeline (restartable)

# Lab 2.3: Cost-Quality Trade-off
# Process 1000 rows, measure cost + time
# Batch vs. streaming: Which is cheaper?
```

**Advanced: Streaming Data Pipeline**
```python
# Lab 2.1: Real-time Kafka/SQS Setup
# Source: Stream of customer messages
# Processing: Batch or process individually?
# Storage: Results in DynamoDB/PostgreSQL
# Deliverable: Streaming pipeline architecture diagram

# Lab 2.2: Data Quality Framework
# Validate: Schema, distributions, anomalies
# Monitor: Drift detection (is data changing?)
# Deliverable: Data quality dashboard

# Lab 2.3: Cost-Optimized Pipeline
# Aggregate small requests into batches?
# Calculate: Cost savings vs. latency trade-off
# Deliverable: Optimization report + implementation
```

### Deliverable
- **Beginner:** Working ETL pipeline (CSV → processing → CSV) + cost report
- **Advanced:** Streaming pipeline architecture + data quality framework + cost optimization analysis

### Instructor Template
```
[BEGINNER]
- Demo: Pandas basics (load, clean, transform)
- Lab: Build pipeline step-by-step
- Debugging: Common errors (missing columns, API failures)
- Homework: Pipeline for real dataset

[ADVANCED]
- Architecture lesson: Streaming vs. batch
- Lab: Design pipeline for 1M rows/day
- Challenge: Cost optimization (batch size optimization)
- Bonus: Data quality metrics (completeness, freshness, validity)
```

### Resources
- Pandas tutorial + documentation
- Streaming concepts: Kafka, AWS SQS, Google Pub/Sub
- Data quality frameworks: Great Expectations

---

## MODULE 3: PROMPT ENGINEERING → PRODUCTION (1.5 weeks / 6 hours)

### Learning Outcomes
**Beginner:** Version prompts, test, iterate, deploy.  
**Advanced:** A/B testing, monitoring, optimization pipelines.

### Syllabus

| Step | Beginner | Advanced |
|------|----------|----------|
| Versioning | Git for prompts | Prompt registry, experiment tracking |
| Testing | Manual testing | Unit tests, benchmarks, automated evals |
| Monitoring | Log outputs | Production metrics, performance dashboards |
| Iteration | Change & retry | A/B testing framework, statistical significance |
| Deployment | Update code | Blue-green deployment, canary releases |

### Hands-On Labs

**Beginner: Prompt Testing Framework**
```python
# Lab 3.1: Version Control Prompts
# Git repo: Organize prompts by version
# Track: Changes, rationale, performance

# Lab 3.2: Manual Testing
# Create test set (inputs + expected outputs)
# Test 3 prompt versions
# Measure: Accuracy on test set
# Deliverable: Test results (which prompt wins?)

# Lab 3.3: Simple Monitoring
# Log: Input, output, token count, cost
# Analyze: Cost per request, token usage trends
# Deliverable: Cost/performance CSV

# Lab 3.4: Deployment
# Store best prompt in database
# Update production code to use it
# Measure: Improvement vs. old prompt
```

**Advanced: A/B Testing & Optimization**
```python
# Lab 3.1: A/B Testing Framework
# Randomly assign users to prompt v1 vs. v2
# Measure: Accuracy, satisfaction, cost
# Statistical test: Is difference significant?
# Deliverable: A/B test results + recommendation

# Lab 3.2: Prompt Optimization Pipeline
# Define: Prompt optimization space (examples, instructions, format)
# Search: Grid search or Bayesian optimization
# Measure: Find optimal hyperparameters
# Deliverable: Optimized prompt + performance curves

# Lab 3.3: Production Monitoring
# Dashboard: Real-time metrics (accuracy, cost, latency)
# Alerts: If performance degrades, alert
# Feedback loop: Log failures for improvement
# Deliverable: Monitoring dashboard (Grafana/Datadog)

# Lab 3.4: Blue-Green Deployment
# v1 (blue) in production
# Deploy v2 (green) to subset of users
# Monitor: If good, shift all traffic
# Rollback: If bad, revert instantly
```

### Deliverable
- **Beginner:** Prompt testing framework + test results + versioning strategy
- **Advanced:** A/B testing framework + optimization results + production monitoring dashboard

### Instructor Template
```
[BEGINNER]
- Show: How production prompt breaks (version conflicts, outdated)
- Demo: Git workflow for prompts
- Lab: Build test set, test prompts, pick winner
- Deploy: Update production with best prompt

[ADVANCED]
- Case study: A/B test that discovered 15% improvement
- Lab: Design A/B test, run simulation
- Challenge: Optimize prompt on custom metric
- Bonus: Implement blue-green deployment
```

### Resources
- MLflow for experiment tracking
- Promptfoo for testing (open source)
- Your A/B testing case study

---

## MODULE 4: VECTOR DBS & RAG SYSTEMS (2 weeks / 8 hours)

### Learning Outcomes
**Beginner:** Build simple RAG (upload docs → ask questions).  
**Advanced:** Hybrid search, reranking, advanced RAG architectures.

### Syllabus

**Beginner:**
1. Embeddings (what they are, why useful)
2. Vector databases (Pinecone, Weaviate basics)
3. Simple RAG (retrieve + generate)
4. Testing RAG (does it find right docs?)

**Advanced:**
1. Embedding strategies (chunking, overlap, metadata)
2. Hybrid search (keyword + semantic)
3. Reranking & ranking models
4. Multi-hop retrieval, filters, metadata filtering
5. RAG evaluation frameworks

### Hands-On Labs

**Beginner: Simple RAG App**
```python
# Lab 4.1: Embedding + Storage
# Upload: 10 PDFs to Pinecone
# Embed: Use OpenAI embeddings
# Store: Vectors + metadata

# Lab 4.2: Retrieval
# Query: "What is return policy?"
# Retrieve: Top 3 docs
# Display: Sources, relevance score

# Lab 4.3: Generation
# Use Claude + retrieved docs
# Build prompt with context
# Generate answer

# Lab 4.4: Integration
# Build: Simple Streamlit UI
# Upload docs → Ask questions → Get answers
# Deliverable: Working RAG app
```

**Advanced: Production RAG System**
```python
# Lab 4.1: Smart Chunking
# Strategy: Size, overlap, metadata extraction
# Measure: Retrieval quality vs. chunk strategy
# Optimize: Find best chunking approach

# Lab 4.2: Hybrid Search
# Implement: Keyword (BM25) + semantic (vector) search
# Weight: Alpha parameter (keyword vs. semantic)
# Measure: Recall@10, MRR (mean reciprocal rank)

# Lab 4.3: Reranking
# Retrieve: Top 50 candidates
# Rerank: Using dedicated model (Cohere, jina)
# Measure: Improvement in relevance

# Lab 4.4: RAG Evaluation
# Build: Evaluation set (questions + correct answers)
# Metrics: Retrieval recall, generation BLEU, exact match
# Measure: End-to-end RAG quality
# Optimize: Improve weakest component

# Lab 4.5: Multi-modal & Metadata
# Handle: PDfs, images, tables (not just text)
# Metadata filtering: Only recent docs, certain categories
# Deliverable: Production RAG system (multi-modal)
```

### Deliverable
- **Beginner:** Working RAG app (Streamlit) + evaluation on 20 test queries
- **Advanced:** Production RAG system (hybrid search, reranking, evaluation framework) + optimization report

### Instructor Template
```
[BEGINNER]
- Concept: What is embedding? (visual explanation)
- Demo: Simple RAG in 10 minutes
- Lab: Build RAG (upload PDFs, ask questions)
- Test: Manually evaluate on 10 queries

[ADVANCED]
- Architecture: Components of production RAG
- Lab 1: Optimize chunking strategy
- Lab 2: Implement hybrid search + measure improvement
- Lab 3: Evaluate RAG on custom benchmark
- Bonus: Multi-modal RAG (images, tables)
```

### Resources
- LangChain RAG tutorials
- Vector DB docs (Pinecone, Weaviate, Milvus)
- RAG evaluation: RAGAS framework
- Your RAG case study

---

## MODULE 5: EVALUATION & TESTING FRAMEWORKS (1.5 weeks / 6 hours)

### Learning Outcomes
**Beginner:** Unit tests, basic metrics, manual evaluation.  
**Advanced:** Production metrics, automated evaluations, monitoring.

### Syllabus

**Beginner:**
1. Unit tests (input → expected output)
2. Basic metrics (accuracy, F1, BLEU)
3. Manual evaluation (human review)
4. Test sets & benchmarks

**Advanced:**
1. Production metrics (latency, throughput, cost)
2. Automated evaluation (LLM-as-judge, reference-free)
3. Error analysis & debugging
4. Monitoring & alerting
5. Cost-quality trade-off curves

### Hands-On Labs

**Beginner: Test Suite**
```python
# Lab 5.1: Unit Tests
# Task: Classification (sentiment)
# Test cases: Positive, negative, neutral, sarcasm
# Assertion: Expected vs. actual
# Deliverable: pytest test file

# Lab 5.2: Metrics
# Evaluate: Model on test set (100 samples)
# Compute: Accuracy, precision, recall, F1
# Deliverable: Metrics report

# Lab 5.3: Benchmark
# Create: Test dataset (inputs + correct answers)
# Evaluate: 2 prompts on benchmark
# Compare: Which is better?
# Deliverable: Benchmark scores
```

**Advanced: Production Evaluation**
```python
# Lab 5.1: Automated Evaluation
# LLM-as-judge: "Is this response good?"
# Metrics: Relevance, factuality, coherence
# Measure: Correlation with human judgment
# Deliverable: Evaluation framework

# Lab 5.2: Cost-Quality Curves
# Vary: Model size, temperature, context length
# Measure: Cost vs. quality (accuracy)
# Plot: Pareto frontier
# Deliverable: Cost-quality optimization curve

# Lab 5.3: Error Analysis
# Collect: Failures in production
# Analyze: Why did they fail?
# Categorize: Missing context, hallucination, etc.
# Plan: How to fix (prompt, fine-tune, retrieve more?)
# Deliverable: Error analysis report + action plan

# Lab 5.4: Monitoring Dashboard
# Track: Accuracy, cost, latency over time
# Alerts: If accuracy drops >5%, alert
# Root cause: Debug degradation
# Deliverable: Monitoring system
```

### Deliverable
- **Beginner:** Test suite (pytest) + metrics report + benchmark results
- **Advanced:** Automated evaluation framework + cost-quality curves + error analysis + monitoring system

### Instructor Template
```
[BEGINNER]
- Demo: Simple pytest (3 examples)
- Lab: Write tests for text classification
- Metrics lesson: When to use accuracy vs. F1
- Homework: Full test suite

[ADVANCED]
- Challenge: Correlate automated evaluation with human judgment
- Lab: Build LLM-as-judge evaluation
- Project: Cost-quality optimization (find sweet spot)
- Bonus: Time-series monitoring (detect drift)
```

### Resources
- pytest documentation
- Evaluation metrics: scikit-learn docs
- LLM evaluation: Weights & Biases, Arize

---

## MODULE 6: DEPLOY PATTERNS (1.5 weeks / 6 hours)

### Learning Outcomes
**Beginner:** Deploy to cloud (AWS/GCP), basic DevOps, serverless intro.  
**Advanced:** Kubernetes, auto-scaling, CI/CD pipelines.

### Syllabus

**Beginner:**
1. Cloud basics (AWS, GCP, Azure concepts)
2. Serverless (Lambda, Cloud Functions)
3. APIs (Flask → deployed API)
4. Monitoring basics

**Advanced:**
1. Containers (Docker)
2. Kubernetes (K8s) basics
3. CI/CD pipelines (GitHub Actions, GitLab CI)
4. Auto-scaling, load balancing
5. Cost optimization

### Hands-On Labs

**Beginner: Serverless Deployment**
```python
# Lab 6.1: Containerize
# Dockerfile: Python app with dependencies
# Build: Docker image
# Test locally: Does it work?

# Lab 6.2: Deploy to AWS Lambda (or similar)
# Function: Call Claude API, return response
# Trigger: API Gateway (HTTPS endpoint)
# Test: curl your endpoint
# Deliverable: Working API endpoint

# Lab 6.3: Monitoring
# CloudWatch logs: See API calls, errors
# Alerts: If error rate > 5%, email alert
# Deliverable: Monitoring set up
```

**Advanced: K8s + CI/CD**
```python
# Lab 6.1: Dockerize App
# Multi-stage build (optimize size)
# Test: Runs locally, ready for production

# Lab 6.2: Kubernetes Deployment
# Manifest: Deployment, Service, ConfigMap
# Scaling: Set replicas = 3
# Test: Kill a pod, auto-restarts

# Lab 6.3: CI/CD Pipeline
# GitHub Actions: On every git push
# Build: Docker image
# Test: Run test suite
# Deploy: Push to K8s if tests pass
# Deliverable: End-to-end pipeline

# Lab 6.4: Auto-scaling
# Horizontal Pod Autoscaler (HPA)
# Metric: CPU > 70%, scale up
# Test: Load test, watch scale
# Deliverable: Auto-scaling setup
```

### Deliverable
- **Beginner:** Deployed API endpoint (serverless) + monitoring
- **Advanced:** K8s deployment + CI/CD pipeline + auto-scaling

### Instructor Template
```
[BEGINNER]
- Concept: Containers, serverless, APIs
- Demo: Deploy simple Flask app to Lambda
- Lab: Students deploy their own chatbot
- Troubleshooting: Common deployment errors

[ADVANCED]
- Architecture: When to use serverless vs. K8s
- Lab 1: Dockerfile, push to registry
- Lab 2: Deploy to K8s cluster
- Lab 3: Set up CI/CD pipeline
- Bonus: Multi-region deployment
```

### Resources
- Docker documentation
- AWS Lambda / Google Cloud Functions
- Kubernetes basics: https://kubernetes.io/docs
- CI/CD: GitHub Actions, GitLab CI examples

---

## MODULE 7: CAPSTONE PROJECT - PRODUCTION RAG SYSTEM

### Learning Outcomes
**Beginner:** Build RAG app (upload docs → deploy).  
**Advanced:** Enterprise RAG system (multi-user, cost tracking, monitoring).

### Projects

**Beginner Capstone: RAG App**
- Pick domain (customer docs, product manual, knowledge base)
- Build: Upload PDFs → embed → retrieve → answer
- Deploy: Streamlit app on Hugging Face Spaces or similar
- Test: 20 test queries, document accuracy
- Deliverable: Live RAG app + test results + code repo

**Advanced Capstone: Enterprise RAG**
- Design: Multi-user RAG (authentication, access control)
- Implement: Chunking strategy, hybrid search, reranking
- Deploy: K8s cluster with auto-scaling
- Monitor: Cost per query, latency, accuracy
- CI/CD: GitHub Actions pipeline
- Deliverable: Production system + architecture doc + monitoring dashboard + cost analysis

### Instructor Guide
```
[BEGINNER]
- Week 1-2: Domain selection, data collection
- Week 3: Build RAG (iterative feedback)
- Week 4: Deploy + test + documentation
- Final: Live demo + Q&A

[ADVANCED]
- Week 1: Design phase (architecture, tech stack)
- Week 2-3: Implementation (RAG + deployment)
- Week 4: Optimization (cost, performance, monitoring)
- Final: Present to "board" (instructor + peers), defend choices
```

### Rubric

| Criterion | Beginner | Advanced |
|-----------|----------|----------|
| Functionality | RAG works, answers questions | Multi-user, cost-tracked, monitored |
| Performance | Retrieval accuracy > 70% | Retrieval + gen accuracy > 85%, < 2s latency |
| Deployment | Live endpoint | K8s, auto-scaling, CI/CD |
| Monitoring | Basic logs | Cost dashboard, alerting, SLOs |
| Documentation | Clear, 5 pages | Professional, 15 pages, architecture diagrams |

---

## TRACK COMPLETION & PROGRESSION

**Requirements:**
- Complete all 7 modules
- Pass all labs with >70% accuracy
- Capstone project score 75%+

**Progression to Track 3 (Enterprise):**
- Capstone score 85%+, OR
- Recommend if showing leadership/architectural thinking

**Certifications:**
- CoreSkills4AI Engineering Core Badge
- Opt-in: AWS Certified Cloud Practitioner (after M1-2)
- Opt-in: AWS Certified Developer (after M6)
- Opt-in: AWS Certified Solutions Architect (after M7)

---

## INSTRUCTOR NOTES

### Token Conservation
- Code-first learning (build, then explain)
- Reuse templates, scripts, configs
- Labs can be completed in parallel

### Portfolio Integration
- Your RAG system as case study (Module 4)
- Your deployment architecture (Module 6)
- Your monitoring dashboard (Module 5)

### Full-Day Intensive (2 days, 40 hrs)
- Day 1: M1-M3 (APIs, pipelines, prompting) = 20 hrs
- Day 2: M4-M7 (RAG, testing, deploy, capstone) = 20 hrs
- Self-paced capstone follows

### Pacing
- Beginner: 1.5-2 weeks per module
- Advanced: 1 week per module (faster, deeper)
- Capstone: 4-6 weeks (largest project)

