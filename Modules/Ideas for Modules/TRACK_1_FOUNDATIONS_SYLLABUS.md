# CoreSkills4AI: Track 1 - AI Foundations for Everyone
**Duration:** 5 weeks self-paced | 1 full day intensive (20 hours)  
**Audience:** Non-technical, business owners, career switchers  
**Cert Alignment:** NIST AI RMF (Module 4-5 only)

---

## TRACK OVERVIEW

This track teaches AI literacy and foundational thinking for decision-makers and professionals entering the AI space. Progression from business fundamentals → governance frameworks.

**Full-Day Intensive Schedule (20 hrs over 1 day + homework):**
- 8am-12pm: M1-M2 (Business Context + Vocabulary)
- 1pm-5pm: M3-M4 (Hands-on Prompts + Ethics)
- 6pm-9pm: M5 Capstone Setup

---

## MODULE 1: WHY AI NOW (1 week / 4 hours)

### Learning Outcomes
**Beginner:** Understand AI's business impact, ROI basics, and why now matters.  
**Advanced:** Strategic AI roadmapping, competitive analysis frameworks, market positioning.

### Syllabus

| Session | Topic | Beginner | Advanced |
|---------|-------|----------|----------|
| 1.1 | AI Market 2026 | Market size, growth trends | Sector-specific disruption analysis |
| 1.2 | ROI Fundamentals | Time-to-value, cost savings | NPV modeling, payback period, risk-adjusted returns |
| 1.3 | Use Case Mapping | Common AI applications | Competitive advantage mapping framework |
| 1.4 | Risk/Reward | Basic risk awareness | Strategic risk quantification |

### Deliverables
- **Beginner:** Industry research report (3 pages): "Why AI Matters to My Company"
- **Advanced:** AI Strategic Roadmap (6+ pages): Competitive positioning, 3-year investment plan

### Instructor Template
```
[BEGINNER COHORT]
- Day 1: Lecture + Q&A (30 min), Browse ChatGPT use cases (30 min)
- Assign: Industry report draft
- Day 2: Student presentations (15 min each), Feedback

[ADVANCED COHORT]
- Day 1: Case study (your client case: how AI changed their revenue/ops)
- Assign: Strategic roadmap framework (template provided)
- Day 2: Peer review, refinement
```

### Resources
- ChatGPT Enterprise case studies (OpenAI)
- Gartner AI Maturity Model
- Your real client case study (confidential)

---

## MODULE 2: AI VOCABULARY & MENTAL MODELS (1 week / 4 hours)

### Learning Outcomes
**Beginner:** Understand core AI terms (LLM, embedding, token, fine-tune, etc.).  
**Advanced:** System architecture thinking, data flow, trade-offs in design.

### Syllabus

| Concept | Beginner Definition | Advanced Depth |
|---------|-------------------|-----------------|
| LLM | "AI model trained on text" | Architecture (transformer), scaling laws, context windows |
| Prompt | "Instructions to AI" | Prompt engineering theory, few-shot learning, chain-of-thought |
| Token | "Words/chunks AI reads" | Tokenization strategies, BPE, impact on cost/latency |
| Embedding | "AI understands meaning" | Vector space, similarity search, dimensionality |
| Fine-tune | "Teaching AI your data" | Domain adaptation, overfitting, data requirements |
| Agent | "AI that takes actions" | Multi-step reasoning, tool use, memory systems |

### Deliverables
- **Beginner:** Concept map artifact (visual): How LLMs work (mind map)
- **Advanced:** System design document: Data flow for 3 AI systems

### Instructor Template
```
[BEGINNER]
- Interactive: Guess the token count game (ChatGPT tokenizer)
- Visual learning: Diagram how embedding works (similarity search demo)
- Homework: Create concept map in Miro/draw.io

[ADVANCED]
- Case study analysis: How do transformers solve NLP?
- Build: Simple embedding search (code template provided)
- Assign: System design doc (why choose fine-tune vs. RAG?)
```

### Key Ideas for Beginners
1. **Tokens = Money** for API users (directly impacts cost)
2. **Prompting = Communication** (clearer instructions = better outputs)
3. **LLMs = Pattern Matching** (powerful but not reasoning)
4. **Context Window = Memory Limit** (can't see all your data at once)

### Advanced Topics
- Scaling laws (Chinchilla optimal, model vs. data scaling)
- Vector databases vs. databases (why separate?)
- Cost-latency trade-offs (model size, quantization)

---

## MODULE 3: PROMPT ENGINEERING FUNDAMENTALS (1.5 weeks / 6 hours)

### Learning Outcomes
**Beginner:** Write effective prompts, control outputs, avoid common mistakes.  
**Advanced:** Prompt optimization, A/B testing, few-shot/chain-of-thought design.

### Syllabus

**Beginner Track:**
1. Prompt anatomy (role, context, instruction, output format)
2. Common mistakes (vague inputs, hallucinations, tone)
3. Output control (JSON formatting, temperature, top_p)
4. Testing & iteration

**Advanced Track:**
1. Prompt injection vulnerabilities & defense
2. Few-shot learning (examples improve performance)
3. Chain-of-thought prompting (step-by-step reasoning)
4. Prompt optimization frameworks (APE, DSPy)
5. Cost vs. quality trade-offs

### Hands-On Exercises

**Beginner:**
```
Exercise 1: Write a customer support prompt
→ Input: Customer complaint
→ Output: JSON (sentiment, category, response)
→ Test with 5 real complaints
→ Measure: Does JSON parse? Is response helpful?

Exercise 2: Fix a bad prompt
→ Given: Vague instruction, hallucinating outputs
→ Challenge: Rewrite to eliminate hallucinations
→ Test: Consistency across 10 runs
```

**Advanced:**
```
Exercise 1: Few-shot optimization
→ Build prompt with 0, 1, 3, 5 examples
→ Measure accuracy on test set
→ Plot: Examples vs. accuracy
→ Deliverable: Optimal few-shot prompt

Exercise 2: Chain-of-thought design
→ Task: Complex reasoning (e.g., math word problems)
→ Prompt v1: Direct answer
→ Prompt v2: "Let's think step by step"
→ Measure: Accuracy improvement
→ Cost analysis: Token trade-offs
```

### Deliverable
- **Beginner:** Prompt library (5 reusable prompts + testing results)
- **Advanced:** Optimized prompt suite + A/B test results (accuracy, cost, latency)

### Instructor Template
```
[BEGINNER]
- Live demo: ChatGPT vs. Bad ChatGPT (same query, different prompts)
- Hands-on: Fix bad prompts in pairs
- Homework: Build prompt library (template provided)

[ADVANCED]
- Code lab: Python script that evaluates prompt quality
- Project: A/B test your prompts on real task
- Assign: Write optimization report (findings + recommendations)
```

---

## MODULE 4: RISK & ETHICS FOR LEADERS (1 week / 4 hours)

### Learning Outcomes
**Beginner:** Recognize bias, understand compliance basics, ethical awareness.  
**Advanced:** NIST AI RMF, governance frameworks, risk quantification.

### Syllabus

**Beginner:**
1. AI Bias (gender, racial, socioeconomic)
2. Hallucinations (confidently wrong answers)
3. Data privacy (GDPR, training data)
4. Responsible AI principles

**Advanced:**
1. NIST AI Risk Management Framework (RMF)
2. Risk quantification (probability × impact)
3. Governance frameworks (decision trees, escalation)
4. Industry-specific compliance (healthcare, finance)

### Key Risk Categories

| Risk | Beginner Awareness | Advanced Management |
|------|------------------|-------|
| Bias | Recognize examples | Audit process, fairness metrics, mitigation |
| Hallucination | Know it happens | Detection methods, fact-checking systems |
| Privacy | GDPR exists | Data governance, PII detection, masking |
| Security | Prompt injection | Defense strategies, red teaming |
| Regulatory | Rules exist | Compliance mapping, audit trails |

### Case Study (Your Portfolio)
Include 1 real client risk scenario:
- **Beginner:** "How would you spot this risk?"
- **Advanced:** "How would you build a governance framework to prevent this?"

### Deliverable
- **Beginner:** Risk awareness checklist (5 pages)
- **Advanced:** Risk assessment framework (NIST-aligned, 10+ pages) + governance doc

### Instructor Template
```
[BEGINNER]
- Case study: Real AI bias scandal (e.g., hiring algorithms)
- Discussion: "What went wrong? How to prevent?"
- Assign: Checklist for evaluating AI risks

[ADVANCED]
- Introduce: NIST AI RMF (map_of_risk → measure → manage)
- Hands-on: Build risk register for hypothetical deployment
- Assign: Governance framework (escalation, approval processes)
- Resource: NIST AI RMF template
```

### Resources
- NIST AI Risk Management Framework (nist.gov)
- OECD AI Principles
- Your real client risk case study

---

## MODULE 5: CAPSTONE PROJECT

### Learning Outcomes
**Beginner:** Implement a simple AI workflow (idea → prompt → output → documentation).  
**Advanced:** Design production-ready AI governance system (with implementation roadmap).

### Projects

**Beginner Capstone: Simple AI Workflow**
- Pick a business process (customer support, email triage, content generation)
- Design AI solution (model choice, prompts, testing)
- Build in ChatGPT/Claude API
- Document: How it works, limitations, risks
- Deliverable: Runnable system + 5-page documentation

**Advanced Capstone: AI Governance System Design**
- Analyze your own (or case study) company
- Design: Risk framework, governance, monitoring, escalation
- Create: Implementation roadmap (phases, costs, timeline)
- Include: NIST RMF mapping, compliance checklist
- Deliverable: 15-page governance doc + risk register + metrics dashboard

### Instructor Guide
```
[BEGINNER]
- Week 1-2: Student picks use case, designs solution
- Week 3: Peer review + feedback
- Week 4: Refinement + final documentation
- Final: Live demo + Q&A

[ADVANCED]
- Week 1: Assign case study (your company or real client scenario)
- Week 2: Risk identification workshop (instructor + student)
- Week 3: Framework design + NIST mapping
- Week 4: Refinement + implementation roadmap
- Final: Present governance framework to "executive" (instructor)
```

### Rubric

| Criterion | Beginner | Advanced |
|-----------|----------|----------|
| Functionality | System works, basic docs | Full governance framework, NIST-aligned |
| Risk Analysis | Identifies 3+ risks | Quantifies probability × impact, mitigation |
| Documentation | Clear, 5 pages | Professional, 15 pages, implementation roadmap |
| Presentation | Explains workflow | Presents governance case, defends choices |

---

## TRACK COMPLETION & PROGRESSION

**Completion Requirements:**
- Attend all 5 modules (or asynchronous equivalent)
- Complete all module assignments
- Pass capstone project (70%+)

**Progression to Track 2 (Engineering Core):**
- If interested in technical role: Capstone score 85%+ OR additional assessment
- Recommended: Basic coding knowledge before starting Track 2

**Certificate/Badge:**
- CoreSkills4AI Foundations Completion Badge
- Opt-in: NIST AI RMF Practitioner (from Module 4-5)

---

## INSTRUCTOR NOTES

### Token Conservation
- This syllabus teaches **thinking**, not coding
- Use templates, case studies, not lengthy lectures
- Hybrid model: 20% instruction, 80% applied work

### Portfolio Integration
- Your real client case embedded in Modules 1, 4, 5 (anonymized)
- Show progression: How did governance solve risk?
- Demonstrate leadership: From awareness → strategy

### Full-Day Intensive (1 Day, 20 hrs)
- 8-12pm: M1-M2 (Why AI + Vocabulary) = 8 hours
- 1-5pm: M3-M4 (Prompts + Ethics) = 8 hours
- 6-9pm: M5 Setup + Q&A = 3 hours
- Homework: M5 projects (async)

### Common Pitfalls
- Don't over-technologize Module 1-2 (saves for Track 2)
- Beginner cohort: Avoid math/statistics
- Advanced cohort: Stretch with real governance work
- Always tie back to "Why this matters to your business"

