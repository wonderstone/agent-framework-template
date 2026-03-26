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
  Current Goal          — one sentence; survives phase transitions
  Working Hypothesis    — current assumption + confidence (High/Medium/Low) + evidence
  Plan                  — chosen approach + steps (max 5) + rationale; set by Rule 16
  Active Work
    Current Step        — what the agent is doing right now (one sentence)
    Next Planned Step   — what the agent will do after this step (one sentence)
  Completed This Phase  — verified subtasks; cleared on graduation
  Blocker / Decision Needed — items stalled on external input or a required decision
  Mid-Session Corrections   — mistakes and course corrections; never cleared mid-session
  Acceptance Criteria   — observable conditions marking phase complete
  Phase Decisions       — key choices made this phase with rationale
  Technical Insights    — durable patterns/traps; never auto-deleted
```

**Update triggers**: sub-phase completes · major technical decision made · task interrupted · goal diverges from actual state · progression loop runs (Rule 14).

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

## Cognitive Layer

The cognitive layer is not a fifth load layer — it is a reasoning discipline that runs **across** all four layers as they are loaded.

```
Layer 1 loads → initial hypothesis formed from operating rules context
Layer 2 loads → hypothesis refined with project-specific facts
Layer 3 loads → evidence gathered; hypothesis validated or revised
Layer 4 loads → final validation against actual code; confidence declared
```

| Concept | Definition | When it applies |
|---|---|---|
| **Hypothesis** | A working assumption about cause, solution, or design | Formed before Layer 3 is loaded |
| **Evidence** | Facts from docs or code that support or conflict with the hypothesis | Gathered during Layer 3–4 loading |
| **Confidence** | High / Medium / Low — reflects how well evidence supports the hypothesis | Declared before acting |
| **Revision** | An explicit update to the hypothesis when evidence conflicts | Required; never silent |

**Key constraint**: Low-confidence hypotheses must be surfaced to the user before proceeding. Do not act on a Low-confidence hypothesis without stating the uncertainty.

The current hypothesis and confidence are tracked in `session_state.md` under **Working Hypothesis**.

---

## Planning Layer

The planning layer sits between goal intake and step execution. It answers the question: *how* should the agent reach the goal? The cognitive layer (Rule 11) reasons about *what is true*; the planning layer (Rule 16) decides *what to do*.

### When Planning Runs

```
New multi-step task received
   ↓
Rule 16: Clarify goal → Identify approaches → Evaluate → Select → Record
   ↓
Plan written to session_state.md (## Plan)
   ↓
Rule 14 progression loop executes plan step-by-step
```

Planning runs **once at the start** of a task. It re-runs (as a plan revision) only when:
- a failure invalidates a core assumption (Rule 13 recovery)
- a better path is discovered mid-execution
- the goal itself turns out to be mis-stated

Single-step tasks skip planning entirely (Rule 16 constraint).

### Role Assignment During Planning

| Planning scenario | Role |
|---|---|
| One obvious path, clear scope | Main thread — plan inline, proceed |
| 2–3 viable approaches, design uncertainty | Architect — enumerate options, recommend |
| Bounded execution after plan is chosen | Implementer — execute checklist from plan |

### How Planning Interacts with Other Mechanisms

| Mechanism | Interaction |
|---|---|
| **Cognitive layer (Rule 11)** | Hypothesis and evidence inform which approaches are viable |
| **Self-check gate (Rule 12)** | Runs per-step *inside* execution — planning happens *before* the first step |
| **Failure recovery (Rule 13)** | Recovery can trigger a plan revision; the revised plan re-feeds Rule 14 |
| **Progression loop (Rule 14)** | Consumes the plan — each loop iteration picks the next step from the recorded plan |
| **Decomposition (Rule 15)** | If the plan reveals independent subtasks, Rule 15 decides whether to fan out |
| **session_state.md** | The `## Plan` section holds the current approach, steps, and rationale |

### Why This Matters

Without a planning layer, the progression loop (Rule 14) executes steps without a map — it can pick individually correct steps that collectively miss the goal. Planning gives the loop a starting direction, while still allowing revision as new information surfaces.

A plan is short by design (max 5 steps). Long plans create false confidence and resist revision. Short plans are easy to update, easy to verify, and easy to discard when wrong.

---

## Self-Check Stage

Every action follows the sequence: **think → self-check → act**. The self-check stage is a mandatory gate between forming an intent and executing it.

```
THINK   → State the intended action and why (one sentence)
   ↓
SELF-CHECK → Answer five gate questions (all must pass)
   ↓
ACT     → Only if all checks pass; otherwise STOP and resolve
```

### Gate Questions

| # | Question | Failure action |
|---|---|---|
| 1 | Have I read every file I plan to change? | STOP — read missing files first |
| 2 | Are any target paths listed under Protected Paths? | STOP — request explicit user confirmation |
| 3 | Is `.github/project-context.instructions.md` loaded? | STOP — load it now |
| 4 | Do all sources (docs, code, config) agree on this change? | STOP — escalate the conflict; do not guess |
| 5 | Is the full scope of this change understood? | STOP — ask for clarification |

### Why This Matters

Without the self-check gate, an agent can act on stale assumptions, skip reading files, or miss protected paths — all of which produce incorrect or dangerous changes. The gate makes these failures visible **before** they happen, not after.

The self-check stage is defined as Rule 12 in `copilot-instructions.md` and is enforced in both agent role files.

---

## Failure Modes and Recovery

When the agent makes a wrong assumption, produces an invalid change, or encounters missing or inconsistent project context, it follows a four-step recovery protocol.

### Recovery Protocol

```
1. RECOGNIZE  → State the failure explicitly; never continue silently
2. RECORD     → Add to session_state.md under Mid-Session Corrections
3. RECOVER    → Apply the appropriate recovery action (see table below)
4. CONTINUE   → Resume only after the failure condition is resolved
```

### Recovery Actions by Failure Type

| Failure type | Recovery action |
|---|---|
| Wrong assumption | Re-read the source of truth; explicitly revise the working hypothesis |
| Invalid change | Revert or correct the change before continuing; do not layer fixes on top of errors |
| Missing context | STOP — request the missing information; do not substitute a guess |
| Conflicting project context | Escalate to the user; do not silently choose one source over another |
| Scope exceeded | Stop the current change; confirm revised scope before resuming |

### Key Constraint

Stopping is always preferred over continuing with Low confidence. A partial STOP is correct behavior, not a failure. An agent that continues on a known-wrong path is more dangerous than one that pauses.

Failure recognition and recovery are defined as Rule 13 in `copilot-instructions.md`. The **Mid-Session Corrections** section in `session_state.md` is where correction entries are recorded.

---

## Progression Model

The progression model gives the framework a "motor" — the mechanism that drives forward motion toward a goal after each subtask completes. It complements the safety brakes (self-check gate, failure recovery) with a mandatory forward-evaluation loop.

### The Loop (Rule 14)

After every completed subtask:

```
COMPLETE subtask
   ↓
RE-EVALUATE → Is the goal done?
   ↓ NO
IDENTIFY    → What is the next concrete step?
   ↓
DECIDE      → continue · decompose (Rule 15) · stop and ask
   ↓
UPDATE      → session_state.md: Current Step + Next Planned Step
   ↓
REPORT      → ## Next Actions in the reply
```

### How It Interacts with Other Layers

| Other mechanism | Interaction |
|---|---|
| **Self-check gate (Rule 12)** | Runs *within* a step — the loop runs *between* steps. They are not alternatives. |
| **Failure recovery (Rule 13)** | A failure can trigger "stop and ask" in the progression loop. The loop resumes after recovery is complete. |
| **Architect role** | Called by the progression loop when the next step requires design analysis before execution. |
| **Implementer role** | Called by the progression loop when the next step is a bounded execution task with known acceptance criteria. |
| **session_state.md** | Current Step and Next Planned Step are written by the loop after every iteration. |

### Decomposition Decision (Rule 15)

When the "IDENTIFY" step reveals a next step that is compound, the agent runs the decomposition test:

```
All subtasks have independent owner files?    YES → fan-out eligible
All subtasks have independent validation?     YES → fan-out eligible
All subtasks produce summarizable results?    YES → fan-out → apply role assignment
Any criterion fails?                          NO  → proceed serially, state why
```

Fan-out uses the Architect for design-uncertain or multi-option tasks and the Implementer for bounded execution tasks.

### Why This Matters

Without the progression loop, an agent that completes a step will stop and wait — even when the next step is obvious and safe. The loop makes forward motion the default and stopping the exception, while keeping explicit stop conditions for blockers and genuine ambiguity.

---

## Document Organization

| Type | Definition | Location |
|---|---|---|
| TYPE-A | Long-lived: architecture, runbooks, API specs | `docs/` or module root |
| TYPE-B | Module-local, evolves with code | module directory |
| TYPE-C | Phase reports, one-time analyses, summaries | `docs/archive/` |

`docs/INDEX.md` lists all TYPE-A docs. It is updated as part of the commit that adds or removes a TYPE-A doc.
