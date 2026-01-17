# PROJECT CONTEXT

- C:\CoreSkills4ai\ClassRoom Modules\ 
- Claude has full read/write access to subfolders.

## Purpose

- Production-grade Agentic AI, ML systems, and developer training modules.
- Focus on correctness, maintainability, and minimal diffs.

## Scope & Goals

Claude is responsible for:
- Code, configs, tests
- Incremental feature development and fixes

Claude is NOT responsible for:
- Large refactors unless approved
- Non-requested optimizations or rewrites

---

# PRIMARY STACK
- Primary language: Python 3.12
- Supporting automation: Node.js, PowerShell (when required)
- Runtime: Docker + WSL2
- Data: PostgreSQL, MongoDB, Redis
- API: Flask
- Testing: pytest, Jest, Cypress
- Linting: Black, ESLint

# CODE STANDARDS
- Prefer clarity over cleverness
- Strong typing and type hints where applicable
- Max line length: 120 (exceed only when necessary)
- Small, reviewable diffs only

---

# OPERATING RULES
1. PLAN before BUILD
2. BUILD only after approval
3. No breaking changes without explicit consent
4. Incremental changes only unless scoped otherwise
5. Security and tests required for logic changes
6. Commit only after successful logical milestones

---

# AUTHORITY ORDER
User > CLAUDE.md > Mode > Commands > Checklists

Commands, workflows, and checklists are defined under .claude/

# MODES & COMMANDS
Defined under: .claude/commands/

Claude must follow active mode behavior.

---

# CONTEXT DISCIPLINE
- Default to concise responses
- Claude should not restate unchanged code
- Do not explain code unless asked
- Ask clarifying questions only when required to proceed
- Prefer diffs over full file output
- Load only files required for the task
- No speculative refactors
- Use `/compact` after completing features

---




