# Framework Architecture

This document explains how the agent framework layers work and why they are structured this way.

---

## Overview

The framework is a layered instruction system for AI coding agents. Each layer has a distinct responsibility and a well-defined load condition. Layers do not duplicate content across each other.

```
Layer 1 — Operating Rules         (always loaded)
Layer 2 — Project Adapter         (loaded on task start or keyword match)
Layer 3 — Canonical Docs          (loaded on confirmed topic match)
Layer 4 — Code / Config Files     (loaded immediately before any edit)
```

---

## Layer 1 — Operating Rules

**File**: `.github/copilot-instructions.md`

**Load condition**: unconditional — loaded at the start of every session.

**Contains**: HOW the agent behaves. The decision rules for:
- When to challenge vs. accept user claims
- When to read before acting
- When to evaluate dispatch
- How to validate after changes
- How to manage state across sessions
- The reply footer format

**Does NOT contain**: project facts, file paths, IP addresses, ports, or domain logic.

---

## Layer 2 — Project Adapter

**File**: `.github/project-context.instructions.md`

**Load condition**: triggered at the start of any multi-step task, OR when a critical topic keyword appears in the user's message.

**Contains**: WHERE to find project facts.
- Project map (directory → purpose)
- Critical topic → canonical doc mapping
- Protected paths
- Build/test commands
- Runtime config locations
- Dangerous operations policy

**Does NOT contain**: detailed architectural explanations or implementation logic. It is a navigation index, not a reference document.

---

## Layer 3 — Canonical Docs

**Files**: `docs/INDEX.md` and topic-specific documents

**Load condition**: when a task **actually touches** a topic — not speculatively.

**Signal**: a topic keyword in the user's message, or a code path encountered during execution matches a trigger defined in the project adapter.

**Contains**: the authoritative explanation for a specific topic (network, architecture, agent design, etc.).

**Does NOT substitute for**: reading the actual code. When docs and code conflict, code wins.

---

## Layer 4 — Code and Config Files

**Files**: the actual implementation files to be modified

**Load condition**: immediately before editing any file.

**Rule**: the agent must read the current file state before making any change. Docs and descriptions are not a substitute for reading the actual current state.

**Conflict resolution**: Layer 4 (code) > Layer 3 (docs) > Layer 2 (adapter).

---

## State Model

The framework tracks work state in `session_state.md` at the project root.

```
session_state.md structure:
  Current Goal        — one sentence; survives phase transitions
  Active Work         — what is in progress right now
  Completed This Phase — verified subtasks; cleared on graduation
  Blocked / Pending   — waiting on external input
  Acceptance Criteria — observable conditions marking phase complete
  Phase Decisions     — key choices made this phase with rationale
  Technical Insights  — durable patterns/traps; never auto-deleted
```

**Update triggers**: sub-phase completes · major technical decision made · task interrupted · goal diverges from actual state.

**File size rule**: keep under ~100 lines. When over limit, archive old phase content to `docs/archive/`.

---

## Completion Checkpoints

When a subtask is confirmed done, the agent executes a 4-step atomic ritual **before** discussing the next subtask:

1. ROADMAP row: `○` → `✅ YYYY-MM-DD`
2. Acceptance criteria: `[ ]` → `[x]`
3. `session_state.md`: move item to "Completed This Phase"
4. Footer: update `Next` to the next subtask

---

## Phase Graduation Protocol

When all acceptance criteria in a phase are ✅:

1. **Archive**: `docs/archive/Phase_N_<Name>_YYYY-MM-DD.md` — decisions + key notes
2. **Promote**: durable insights → appropriate TYPE-A docs
3. **Rotate**: clear phase content from `session_state.md`; load next phase criteria
4. **Mark**: ROADMAP.md row → `✅ YYYY-MM-DD`
5. **Git closeout**: commit, then ask before pushing

---

## Dispatch Decision Logic

Before proceeding serially on a multi-step task, the agent evaluates whether to fan out:

```
Can the task be split into 2+ scopes where ALL of the following are true for each scope?
  □ independent owner file set
  □ independent validation command
  □ independent summarizable result
  □ no sequential dependency on another scope
    → YES: evaluate fan-out (external agent / internal subagent / main thread)
    → NO:  proceed serially; state the exemption reason
```

The dispatch decision is always disclosed in the user-visible reply, not just in the footer.

---

## Document Organization

| Type | Definition | Location |
|---|---|---|
| TYPE-A | Long-lived: architecture, runbooks, API specs | `docs/` or module root |
| TYPE-B | Module-local, evolves with code | module directory |
| TYPE-C | Phase reports, one-time analyses, summaries | `docs/archive/` |

`docs/INDEX.md` lists all TYPE-A docs. It is updated as part of the commit that adds or removes a TYPE-A doc.
