f# A1 – Full Worked Lab 01: Data-First AI Systems

## Lab Data Migration & Management

**Data Before Models: Building AI Systems That Don’t Fail Silently**

Tasked with cleaning datasets: crucial for efficient powerful AI modeling. 

AI Systems with disorganized data fail to produce clean, clear answers, consistency matters. Ex: \<Insert clear real-world example> 

---

## Lab Position in Curriculum

- **Track:** A — AI Systems Thinking
- **Module:** A1 — AI Systems Mental Models
- **Timing:** First hands-on lab in System Thinking
- **Duration:** \~4 hours total

This lab is intentionally placed **before RAG, embeddings, or agents**.

Before we produce an effective agent we need to build a simple system understanding. Think of it as training a new employee. First, we must demonstrate how we run our existing system. Start with simple careful well-planned instructions. 

---

## Lab Purpose - Data Migration

This lab exists to permanently correct a common misconception:

> *“Better models fix bad data.”*

By the end of this lab, students will viscerally understand that:

- AI systems fail at the **data and context layer first**, not the model layer
- RAG and embeddings only amplify data problems if foundations are weak
- Proper data organization is an **AI capability**, not a preprocessing chore

---

## Scenario Overview (Student-Facing)

You are consulting for **ZZZ Financial Services**, which has acquired **AAA Accounting**, a firm with 15 years of disorganized legacy data.

ZZZ wants to:

1. Integrate AAA’s data into a clean, unified system
2. Prepare that data for future AI features (search, Q&A, assistants)
3. Avoid expensive AI failures caused by poor data foundations

Advanced method python w/libraries.

Class model will use AI tools. We will not be using embeddings or RAG until the data is ready. 

Your job is to decide:

> *Is this data even ready for AI?*

## Learning Outcomes (Assessed)

By the end of this lab, students can:

1. Explain why poor data guarantees poor AI outcomes
2. Identify data quality failures that RAG cannot fix
3. Design a data foundation suitable for downstream AI systems
4. Justify delaying AI features when prerequisites are not met

---

## Module Structure (4 Hours)

### Hour 1 — System Orientation & Mental Models

**Instructor-Led (30 - 45 min)**

- Review the AI System Loop:
  - Data → Context → Model → Action → Feedback
- Emphasize: *No context quality → no AI reliability*
- Challenge will be to use coding methods over AI tools

**Student Activity (60 min)**

- Read the scenario
- Review the provided architecture diagram
- Write a short answer:
  - *“Where do you think this system will fail first?”*

---

### Hour 2 — Data Discovery & Profiling

**Student Tasks**

Students connect to the **AAA Accounting legacy database** and:

- Inventory tables and columns
- Identify:
  - Inconsistent naming
  - Missing primary keys
  - Mixed data formats
  - Duplicates
  - Placeholder values ("TBD", "N/A")

**Required Artifacts**

- Data Quality Findings Report (Markdown or text):
  - Top 10 issues discovered
  - Why each issue matters *for AI*

**Key Teaching Moment**

> If you cannot explain your data to a human, an LLM will hallucinate explanations for you.

---

### Hour 3 — Data Normalization & Readiness Design

**Instructor Framing (15 min)**

- Explain *AI-readiness criteria*:
  - Stable identifiers
  - Consistent schemas
  - Semantic clarity
  - Provenance

**Student Tasks (45 min)**

Students must:

- Propose a **clean target schema** for client data
- Define:
  - Canonical client ID strategy
  - Field normalization rules
  - Deduplication logic (conceptual, not perfect)

**Deliverable**

- Unified Schema Proposal:
  - Table definitions
  - Field descriptions
  - Data lineage notes

---

### Hour 4 — AI Readiness Review & Go / No-Go Decision

**Student Task**

Students must write an **AI Readiness Decision Memo** answering:

1. Is this data ready for RAG? Why or why not?
2. What would embeddings amplify or distort?
3. What breaks first if leadership pushes AI now?
4. What *minimum* work must be done before AI is allowed?

**Optional Extension (Advanced Students)**

- Propose phased AI rollout milestones

---

## Evaluation Criteria

| Dimension        | What Good Looks Like                     |
| ---------------- | ---------------------------------------- |
| Systems Thinking | Connects data issues to AI failure modes |
| Data Reasoning   | Identifies real, non-trivial problems    |
| Judgment         | Willing to say “not ready”               |
| Clarity          | Executive-level explanations             |

**Important:**
A student can score highly **without writing perfect SQL or Python**.

---

## Common Student Failure Patterns (Instructor Only)

- Jumping ahead to embeddings mentally
- Assuming LLMs "figure it out"
- Underestimating identifier chaos
- Ignoring provenance

Do **not** rescue them early.

---

## Forward Linkage

This lab directly enables:

- A2 — Failure Modes & Anti-Patterns
- B1 — Context Is the Product

Students who skip this discipline will fail later labs expensively.

---

## Instructor Reflection Prompt

After class, ask:

> *“Which students tried to solve this with technology instead of judgment?”*

That distinction matters.

