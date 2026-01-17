
**Modules:**
- M204: LangChain & Agent Architecture
- M205: Tool Use, Memory, and Evaluation
- M206: Open-Source LLMs & VM Labs

---

### Agent Architect

**Capability:**
- Design multi-agent systems
- Implement orchestration, supervision, and recovery

**Modules:**
- M207: AutoGen (Multi-Agent Dialogue)
- M208: CrewAI (Role-Based Agent Teams)
- M209: Observability, Tracing, and Failure Recovery

---

### Agentic Systems

**Capability:**
- Deploy agentic systems responsibly at scale
- Balance autonomy, cost, governance, and performance

**Modules:**
- M210: Autonomous Systems (AutoGPT Case Study)
- M211: Platform & Toolchain Comparison
- M212: Colab, GPUs, and Scalable Experimentation

---

## Learning Outcomes & Assessment Rubrics

### Global Learning Outcomes
By certification completion, learners will be able to:
- Design agentic systems with explicit autonomy boundaries
- Select appropriate models and tools based on cost and context
- Build, test, and evaluate agents in controlled environments
- Explain failure modes and mitigation strategies
- Deploy agents using both proprietary and open-source models

---

### Assessment Rubric (Applied Across Modules)

| Dimension | Exemplary | Proficient | Developing | Insufficient |
|--------|-----------|------------|------------|--------------|
| Conceptual Understanding | Clear mental models, correct distinctions | Mostly accurate | Partial understanding | Confused definitions |
| System Design | Modular, resilient, scalable | Functional design | Fragile design | Ad-hoc |
| Cost Awareness | Explicit budgeting & controls | Reasonable estimates | Minimal awareness | No consideration |
| Safety & Governance | Guardrails + monitoring | Guardrails only | Ad-hoc safety | Unsafe |
| Implementation | Clean, documented, reproducible | Working | Partially working | Non-functional |

---


### M213 — Google Colab & Scalable Experimentation

**Purpose:** Teach low-friction GPU-based experimentation.

#### Topics
- What Colab is and is not
- Free vs Pro tiers
- Running notebooks as agent sandboxes
- Connecting Colab to GitHub repos
- Calling APIs and open-source LLMs

**Use Cases**
- Rapid prototyping
- Classroom demos
- Cost-controlled labs

**Duration:** 6–8 hours




### M214 — PyTorch Fundamentals for Agentic AI

**Does PyTorch Deserve Its Own Module?**
**Yes — but scoped.**

This is **not** deep learning theory.

#### What Students Must Understand
- What PyTorch is (tensor + autograd framework)
- Why models are trained in PyTorch
- How inference differs from training
- How agents consume models (not train them)

#### What Is Explicitly Out of Scope
- Training LLMs from scratch
- Advanced optimization

**Outcome:**
Students understand the **model layer beneath agents**, enabling informed infrastructure decisions.

**Duration:** 6–8 hours

---


## 206. VM Lab Architecture

### Goals
- Shared GPU
- Cost containment
- Reproducibility

### Stack
- Provider: RunPod / Vast.ai / EC2
- GPU: RTX 3090 or A10
- Runtime: Docker + vLLM
- Models: LLaMA 3, Mistral, Mixtral
- Access: Jupyter + API endpoint

### Classroom Model
- One VM per cohort
- Time-boxed access
- Instructor-controlled sessions

---

---







