# CoreSkills4AI — Outcome-Driven Module Definitions

---

## A1. AI Systems Mental Models

### Learning Outcome
Students can explain and diagram how data, context, models, tools, and feedback loops interact in an AI system.

### Key Concepts
- Tokens as compute currency
- Latency vs accuracy vs governance triangle
- Deterministic vs probabilistic systems

### Lab
Model Budget Game:
Students design three AI systems under a fixed monthly token budget and justify trade-offs.

---

## A2. AI Failure Modes & Anti-Patterns

### Learning Outcome
Students can diagnose *why* an AI system fails without changing the model.

### Key Concepts
- Hallucination vs missing data
- Prompt leakage
- Over-retrieval
- Agent runaway loops

### Lab
Broken system diagnosis with written root-cause analysis.

---

## B1. Context Is the Product

### Learning Outcome
Students can design context pipelines that outperform larger models.

### Key Concepts
- Chunking strategies
- Context compression
- Lost-in-the-middle phenomenon

### Lab
Same dataset ingested three ways, evaluated for quality and cost.

---

## B2. Retrieval-Augmented Generation Systems

### Learning Outcome
Students can select and justify RAG architectures based on workload, cost, and risk.

### Key Concepts
- Embedding dimensionality trade-offs
- Vector vs hybrid retrieval
- Query-time vs build-time cost

---

## C1. Agent Boundaries & Control Design

### Learning Outcome
Students can design agents that are intentionally constrained, safe, and auditable.

### Key Concepts
- Human-in-the-loop
- State vs memory
- Kill switches and timeouts

### Lab
Build an agent that refuses to act under defined conditions.

---

## C2. Multi-Agent Architecture Patterns

### Learning Outcome
Students can select the correct multi-agent pattern for a given business problem.

### Patterns
- Supervisor-Agent
- Swarm
- Tool-Only Agent
- Event-Driven Agent

Frameworks are treated as implementations, not objectives.

---

## D1. AI Cost Engineering

### Learning Outcome
Students can model, forecast, and optimize AI system costs.

### Key Concepts
- Token burn rates
- Caching strategies
- Model routing

### Lab
Deploy the same system three ways and compare monthly costs.

---

## E2. When NOT to Use AI

### Learning Outcome
Students can defend non-AI solutions in technical reviews.

### Lab
Replace an LLM with deterministic logic and justify the decision.
