# CoreSkills4ai - Instructor Quick Start

**Get up to speed in 30 minutes.** This is your teaching playbook.

---

## YOUR ROLE

You're teaching production-grade AI skills. Your students will:
- **Beginners:** Understand AI fundamentals, build first projects
- **Advanced:** Design enterprise systems, mentor others

You provide:
- **Structure:** Clear learning path, labs, feedback
- **Mentorship:** Why decisions matter, real-world context
- **Validation:** Grading, code review, career guidance

---

## TEACHING PHILOSOPHY

**"Learn by building."**
- 20% lecture, 80% hands-on
- Show problems first ("This RAG system costs $1,000/month. How do we optimize?")
- Then teach the solution
- Students build proof-of-concept, iterate, optimize

**"Your real work is the best teacher."**
- Your client projects are case studies
- Share lessons learned, mistakes, what you'd do differently
- Show the messy, real engineering (not just final polish)

---

## BEFORE YOUR FIRST CLASS

### 1. Read the Syllabus (30 min)
- [ ] Skim Track 1-2 syllabi (shows progression)
- [ ] Deep dive into your assigned module
- [ ] Understand beginner vs. advanced tracks

### 2. Review the Config (10 min)
- [ ] Open `coreskills4ai_config.json`
- [ ] Find your module, understand the outcomes
- [ ] See how it connects to other modules

### 3. Check the 2026 Topics (10 min)
- [ ] Open `2026_ESSENTIAL_AI_TOPICS.md`
- [ ] Find your module's topics
- [ ] Ensure you're covering everything important

### 4. Gather Your Materials (20 min)
- [ ] Find template files (lesson plan, lab, capstone)
- [ ] Check your portfolio case studies (yours to use)
- [ ] Collect code samples, datasets, tools

**Total prep time:** 1.5 hours before first class.

---

## TEACHING STRUCTURE (Per Module)

### Week 1: Foundation
**Goal:** Students understand the "why."

**Format:**
1. **Live Session (30 min):** Lecture + demo + Q&A
2. **Lab (30 min):** Hands-on coding, instructor circulates
3. **Homework:** Read, watch video, start assignment

**Your role:**
- Make it concrete (show a real problem, show how AI solves it)
- Engage beginners (no heavy math, lots of examples)
- Challenge advanced (stretch with optimization, edge cases)

### Week 2: Building
**Goal:** Students build something real.

**Format:**
1. **Lab Review (15 min):** Common mistakes from homework
2. **Advanced Topics (15 min):** Deeper concepts
3. **Lab Extension (30 min):** Build on week 1
4. **Code Review:** Pair-program with students

**Your role:**
- Debug errors (guide, don't just fix)
- Share optimization insights (this is where experience matters)
- Push advanced students (can you do this differently?)

### Week 3: Capstone Prep
**Goal:** Students plan their capstone.

**Format:**
1. **Case Study (20 min):** Your portfolio project
2. **Framework (20 min):** How to scope capstone
3. **Lab:** Students design their project
4. **Feedback:** You give written feedback on design

**Your role:**
- Tell your story (What problem did you solve? How?)
- Help students pick realistic scopes
- Warn them about common pitfalls

---

## GRADING RUBRIC (Use This)

### For Labs (Beginner)
| Criterion | Score |
|-----------|-------|
| Functionality | Does it work? (50%) |
| Code Quality | Is it readable? (25%) |
| Documentation | Does it explain itself? (25%) |

**Scoring:** 4 = excellent, 3 = good, 2 = adequate, 1 = needs work

### For Labs (Advanced)
| Criterion | Score |
|-----------|-------|
| Functionality | Does it work at scale? (40%) |
| Optimization | Is it cost/latency optimal? (30%) |
| Documentation | Is it production-ready? (30%) |

### For Capstone (Use 0-10 scale)
- **10:** Exceeds expectations, publishable quality
- **8:** Meets expectations, production-ready
- **6:** Adequate, needs polish
- **4:** Below expectations, incomplete
- **<4:** Insufficient, please redo

---

## COMMON TEACHING PATTERNS

### Pattern 1: "Show-Then-Do" (20 min)
1. **Show:** Live code demo (5 min)
2. **Explain:** Why we did it this way (3 min)
3. **Do:** Students implement (10 min)
4. **Debrief:** Lessons, edge cases (2 min)

### Pattern 2: "Problem-First" (25 min)
1. **Problem:** "This system costs $10K/month. How do we optimize?" (2 min)
2. **Brainstorm:** Students suggest solutions (5 min)
3. **Teach:** Here's what actually works + why (8 min)
4. **Build:** Students implement the solution (10 min)

### Pattern 3: "Code Review" (15 min)
1. **Student presents:** Their code (3 min)
2. **Questions:** Instructor asks why they chose this (2 min)
3. **Feedback:** What's good, what to improve (5 min)
4. **Next steps:** What to do next (5 min)

---

## HANDLING DIFFERENT COHORTS

### Beginner Cohort
- **Pace:** Slower, more examples, visuals
- **Math:** Avoid heavy math, focus on intuition
- **Scaffolding:** Provide more code templates
- **Wins:** Celebrate every working prototype
- **Questions:** No question is dumb, encourage them

### Advanced Cohort
- **Pace:** Faster, less hand-holding
- **Depth:** Trade-offs, optimization, edge cases
- **Challenge:** "Can you do this with 50% less cost?"
- **Leadership:** Pair them with beginners (peer mentoring)
- **Rigor:** Expect production-grade work

### Mixed Cohort
- **Differentiation:** Offer "challenge" lab extensions
- **Grouping:** Pair advanced + beginner when possible
- **Timing:** Let advanced finish first, then deepen
- **Respect:** Make it clear both paths are valued

---

## YOUR PORTFOLIO INTEGRATION

**Use your real work as case studies:**

### Module 1 (Why AI Now)
- **Your story:** "I worked with [Company] who had [Problem]"
- **Solution:** How AI solved it
- **Results:** Metrics (cost saved, revenue, productivity)
- **Lesson:** What surprised you, what you learned

**Time:** 10-15 minutes of your first class.

### Module 4 (RAG Systems)
- **Your RAG system:** Architecture, choices
- **Cost optimization:** How you reduced costs
- **Lessons:** What didn't work, what you'd do differently

**Time:** 5-minute case study during lecture.

### Module 9 / Capstone (Enterprise System)
- **Your full engagement:** Problem → solution → results
- **Process:** How you approached it
- **Mistakes:** What went wrong, how you recovered
- **Impact:** Business outcomes, technical achievements

**Time:** 20-30 minute presentation.

**Why this matters:**
- Shows students real engineering (not textbook perfect)
- Builds your portfolio while teaching
- Makes concepts stick (concrete > abstract)

---

## TECHNOLOGY YOU'LL NEED

### Basics
- Laptop with internet
- GitHub account (where code lives)
- Python + Jupyter (for demos)

### By Module
| Module | Tools |
|--------|-------|
| M1-3 | ChatGPT/Claude, Python, prompt libraries |
| M4 | Vector DB (Pinecone), embeddings |
| M5 | Testing frameworks, evaluation tools |
| M6 | Docker, AWS/GCP account, GitHub Actions |
| M7 | Kubernetes, monitoring tools |

**Don't panic:** Setup scripts and templates provided for all.

---

## HANDLING COMMON ISSUES

### Student Falls Behind
- **Root cause:** Usually pacing or prerequisites
- **Solution:** Pair with peer, offer office hours, consider audit option
- **Prevention:** Regular check-ins, early warning system

### Lab Code Doesn't Work
- **Don't fix for them:** Guide them to the problem
- **Use debugging:** "What does the error mean? Let's read it together."
- **Share patterns:** "Common mistakes in this lab are..."

### Student Disagrees with Your Approach
- **Good sign:** They're thinking critically
- **Response:** "That's a valid approach. Let's compare trade-offs."
- **Outcome:** You both learn

### Advanced Student Bored
- **Solution:** Offer "stretch" challenges
- **Examples:** "Can you implement this 50% faster?" or "Can you handle 10x more data?"
- **Recognition:** Public praise for solving hard problems

---

## OFFICE HOURS BEST PRACTICES

**Schedule:** 2 hours/week (1-on-1 or group)

**How to run them:**
1. **First 5 min:** Let them ask anything (technical or career)
2. **Debug:** Work through their code together
3. **Feedback:** Review their approach, suggest improvements
4. **Next steps:** What to focus on next
5. **Document:** Share notes in shared doc (helps others)

**Common topics:**
- "My code doesn't work" → Debug together
- "Is my approach right?" → Code review
- "How do I get a job?" → Career mentoring
- "Should I use X or Y?" → Trade-off analysis

---

## MEASURING SUCCESS

### Student Perspective
- Did they learn what was promised?
- Can they build something production-ready?
- Do they feel confident moving forward?
- **Metric:** Post-module survey, capstone quality

### Your Perspective
- Did you engage students?
- Did they complete assignments?
- Are they asking good questions?
- **Metric:** Completion rate 85%+, capstone score 75%+

### Program Perspective
- Are students getting jobs?
- Are they happy? (NPS > 60)
- Are they recommending the program?
- **Metric:** 3-month job placement, alumni referrals

---

## YOUR FIRST WEEK CHECKLIST

- [ ] Read Track 1-2 syllabi (30 min)
- [ ] Deep dive into your module (1 hour)
- [ ] Gather code samples, datasets (30 min)
- [ ] Test all your demos (1 hour)
- [ ] Create your first lesson (1.5 hours)
- [ ] Set up your office hours (15 min)
- [ ] Send intro email to students (15 min)

**Total:** ~5 hours of prep.

---

## INTRO EMAIL TO STUDENTS (Template)

```
Subject: Welcome to [Module Name]!

Hi everyone,

I'm excited to teach this module. Here's what we'll cover:
- [Outcome 1]
- [Outcome 2]
- [Outcome 3]

By the end, you'll build [Capstone Project].

I've built this in production. Happy to share war stories and lessons learned.

Office hours: [Time], [Link]

Let's build something great together!

[Your name]
```

---

## RESOURCE MAP

| Need | File |
|------|------|
| Curriculum overview | `coreskills4ai_config.json` |
| Full Track 1 syllabus | `TRACK_1_FOUNDATIONS_SYLLABUS.md` |
| Full Track 2 syllabus | `TRACK_2_ENGINEERING_CORE_SYLLABUS.md` |
| All 2026 topics | `2026_ESSENTIAL_AI_TOPICS.md` |
| Integration info | `TRACK_3_4_AND_INTEGRATION.md` |
| Module templates | `TEMPLATE_*.md` (in folder) |
| Curriculum map | `coreskills4ai_curriculum_map.xlsx` |

---

## QUESTIONS? START HERE

**"How do I structure my first class?"**
→ See "Teaching Structure (Per Module)" above

**"What should my capstone be?"**
→ Open syllabus for your module, find Capstone section

**"How do I grade this lab?"**
→ See "Grading Rubric" section

**"Should I teach this to beginners or advanced?"**
→ Check `coreskills4ai_config.json` for track audience

**"How do I connect to other modules?"**
→ Open curriculum map for your module's place in sequence

---

## FINAL THOUGHT

**You're not just teaching AI. You're training the next generation of builders.**

Make it real. Share your mistakes. Show them how you'd solve problems.

The best lesson is: "Here's what I learned from this client project. Let me teach you the shortcut."

Welcome to the team. Let's build amazing AI educators together.

