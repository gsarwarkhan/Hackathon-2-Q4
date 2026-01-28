# AGENTS.md

## Purpose
This project uses **Spec-Driven Development (SDD)** — a workflow where **no agent is allowed to write code until the specification is complete and approved**.
All AI agents (Claude, Copilot, Gemini, local LLMs, etc.) must follow the **Spec-Kit lifecycle**:

> **Specify → Plan → Tasks → Implement**

This prevents “vibe coding,” ensures alignment across agents, and guarantees that every implementation step maps back to an explicit requirement.

---

## How Agents Must Work
Every agent in this project MUST obey these rules:
1. **Never generate code without a referenced Task ID.**
2. **Never modify architecture without updating `speckit.plan`.**
3. **Never propose features without updating `speckit.specify` (WHAT).**
4. **Never change approach without updating `speckit.constitution` (Principles).**
5. **Every code file must contain a comment linking it to the Task and Spec sections.**

If an agent cannot find the required spec, it must **stop and request it**, not improvise.

---

## Spec-Kit Workflow (Source of Truth)

### 1. Constitution (WHY — Principles & Constraints)
File: `specs/constitution.md`
Defines the project’s non-negotiables: architecture values, security rules, tech stack constraints, performance expectations, and patterns allowed.

### 2. Specify (WHAT — Requirements & Acceptance Criteria)
File: `specs/features/*.md`
Contains user journeys, requirements, and acceptance criteria.

### 3. Plan (HOW — Architecture & Components)
File: `specs/architecture.md`
Includes component breakdown, APIs, and schema diagrams.

### 4. Tasks (BREAKDOWN — Atomic Work Units)
File: `task.md` (or specific task files)
Atomic, testable work units linked back to Specify + Plan.

---

## Agent Behavior in This Project
### When generating code:
Agents must reference:
```
[Task]: T-001
[From]: specs/features/task-crud.md
```
### When proposing new behavior or a new feature:
Requires update in `specs/features/` (WHAT).

---

## Developer–Agent Alignment
Humans and agents collaborate, but the **spec is the single source of truth**.
Before every session, agents should re-read:
1. `specs/constitution.md`
2. `AGENTS.md`
