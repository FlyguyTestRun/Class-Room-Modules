# A1 — AI Systems Mental Models

## Module Purpose (Learning Contract)

This module establishes the **correct mental model** of how AI systems function in the real world.

Students learn that:
> Models do not fail randomly — systems fail predictably.

This module is foundational and must be mastered before:
- RAG systems
- Agentic architectures
- Cost optimization

---

## Target Audience

- AI / ML Engineers
- Software Architects
- Technical Leaders transitioning into AI

---

## Prerequisites

Students must understand:
- Basic programming concepts
- High-level awareness of LLMs

No prior AI deployment experience is required.

---

## Learning Outcomes (Non-Negotiable)

By the end of this module, students can:

1. Diagram an AI system end-to-end (data → context → model → action → feedback)
2. Explain the difference between model failure and system failure
3. Reason about tokens as a cost and performance constraint

---

## Core Concepts

- Tokens as compute currency
- Context windows and degradation
- Latency vs accuracy vs governance triangle
- Deterministic vs probabilistic execution

---

## What This Module Is NOT

This module does NOT:
- Teach prompt engineering tricks
- Compare LLM vendors
- Optimize outputs

Those come later.

---

## Canonical Mental Models

### The AI System Loop
Data → Context → Model → Action → Feedback

### The Constraint Triangle
You can optimize **two**:
- Cost
- Accuracy
- Governance

Never all three simultaneously.

---

## Failure Modes Covered

- Over-contextualization
- Under-contextualization
- Treating models as deterministic logic
- Ignoring token economics

---

## Hands-On Lab

### Lab Objective
Design and explain three AI systems under explicit cost constraints.

### Constraints
- Fixed monthly token budget
- Single model choice
- No external tools

### Deliverables
- System diagram (hand-drawn or digital)
- Written justification of trade-offs

---

## Evaluation Criteria

| Dimension | Description |
|--------|------------|
| Systems Thinking | Correct end-to-end reasoning |
| Cost Awareness | Token usage considered |
| Trade-offs | Explicit and justified |
| Explanation | Clear and defensible |

---

## Reflection Questions (Required)

1. Where did the system fail first under constraint?
2. What improved more: model size or context quality?
3. How would governance change your design?

---

## Forward Linkage

This module directly enables:
- A2 — Failure Modes & Anti-Patterns
- B1 — Context Is the Product

Students who struggle here will struggle everywhere else.

---

## Instructor Notes (Hidden from Learners)

- Students will want to jump into tools — resist this.
- Force diagrams before discussion.
- Penalize vague explanations.
