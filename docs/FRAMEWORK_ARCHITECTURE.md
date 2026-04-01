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

The framework also ships a **resumable audit artifact system**. It is **not** a fifth instruction layer. It is an operational recovery mechanism that runs alongside the four-layer loading model.

The framework also distinguishes **strategy** from **mechanism**:

1. strategy answers: which agent / CLI / reviewer is responsible for what kind of judgment
2. mechanism answers: how that work is frozen, validated, handed off, and recovered

The repository now also includes a **productization surface** around that model:

1. `scripts/bootstrap_adoption.py` turns adoption into a profile-aware initialization step
2. `scripts/validate_template.py` checks structural integrity beyond simple string greps
3. `examples/demo_project/` shows a tiny adopted repository with code, tests, and committed audit artifacts
4. `docs/COMPATIBILITY.md`, `CHANGELOG.md`, `VERSION`, and `.github/RELEASE_TEMPLATE.md` make release and support expectations explicit
5. `templates/execution_contract.template.md` gives the agent a standard pre-execution confirmation surface for long tasks
6. opt-in executable governance capabilities now exist for closeout truth audit, runtime surface guardrails, and hook installation

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

**On-demand principle**: Layer 2 is the discovery index, not the full knowledge base. Loading it does not mean loading everything it references. The agent reads only the entries relevant to the current task — speculative pre-loading of all canonical docs inflates context without benefit.

---

## Layer 3 — Canonical Docs

**Files**: `docs/INDEX.md` and topic-specific documents

**Load condition**: when a task **actually touches** a topic — not speculatively.

**Signal**: a topic keyword in the user's message, or a code path encountered during execution matches a trigger defined in the project adapter.

**Contains**: the authoritative explanation for a specific topic (network, architecture, agent design, etc.).

**Does NOT substitute for**: reading the actual code. When docs and code conflict, code wins.

**On-demand principle**: load one canonical doc at a time, only when a confirmed topic match occurs. Do not pre-load all docs in `docs/INDEX.md` at session start. Each doc loaded consumes context budget that would otherwise be available for code reading. Prefer narrow, triggered loads over broad upfront loads — this mirrors the Tool Search pattern: discover on demand, not in bulk.

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

## Resumable Audit Artifacts

The framework includes a portable artifact contract for multi-executor implementation and Git review work.

These artifacts are operational state, not instruction layers:

| Artifact | Purpose | Default location |
|---|---|---|
| `task packet` | Freeze goal, truth sources, allowed files, do-not-touch list, validation, acceptance boundary | `tmp/git_audit/<task_slug>/task_packet.md` |
| `audit receipt` | Record what a given executor or reviewer changed and verified | `tmp/git_audit/<task_slug>/audit_receipt.md` |
| `handoff packet` | Capture resume point, blocker, and next executor when a session is interrupted | `tmp/git_audit/<task_slug>/handoff_packet.md` |

These artifacts matter because semantic reviewers are replaceable, but hard gates are not. A new CLI session or reviewer should be able to resume from the artifacts without reconstructing state from memory alone.

### Why This Is Not A Fifth Layer

The load layers answer **what to read before acting**.

The audit artifacts answer **how to preserve execution state when work spans multiple sessions or executors**.

They do not change the layer order:

1. Load rules
2. Load adapter
3. Load canonical docs
4. Read code/config to edit
5. Externalize execution state into packet / receipt / handoff when work must survive interruption

### Default Flow

1. Freeze a task packet before fan-out or external audit
2. Execute a bounded scope
3. Record an audit receipt
4. If execution stops or ownership changes, create a handoff packet
5. Run hard gates outside the semantic auditor
6. Return to the main thread for owner review and Git closeout

## Strategy vs Mechanism Layering

This framework now makes an explicit distinction between two reusable surfaces.

### Strategy Layer

The strategy layer defines **who is responsible for which kind of judgment**.

Examples:

1. a runtime-correctness reviewer
2. a maintainability reviewer
3. a protocol-boundary reviewer
4. a benchmark/performance reviewer
5. a refactor-safety reviewer

This layer answers questions such as:

1. What is this reviewer optimizing for?
2. What should it ignore?
3. What evidence must it respect?
4. What kinds of findings are blocking vs optional?

### Mechanism Layer

The mechanism layer defines **how any of those roles operate safely and recoverably**.

Examples:

1. task packet
2. audit receipt
3. handoff packet
4. hard gates
5. validation ordering
6. owner review

This layer does not care whether the reviewer is Codex, Claude, an internal subagent, or a future custom agent. It exists so role replacement does not break process continuity.

### Why The Split Matters

Without the split, repositories tend to entangle three different concerns:

1. reviewer identity
2. reviewer judgment criteria
3. workflow recovery and hard-gate mechanics

That creates brittle systems. If one CLI times out or one reviewer becomes unavailable, the whole workflow has to be reinvented.

With the split:

1. role profiles can change without rewriting the workflow machinery
2. packet / receipt / handoff can stay stable across reviewer changes
3. repositories can introduce domain-specific reviewers as first-class strategy implementations

---

## User Acceptance Gate

Technical validation (lint, type checks, unit tests) confirms the code is correct. User acceptance confirms the work satisfies the user's intent. These are distinct checks — passing one does not imply the other.

Rule 22 in `.github/copilot-instructions.md` makes user acceptance a mandatory gate, not an afterthought.

### The Problem This Solves

Agents tend to close tasks based on technical correctness: tests pass, lint is clean, no type errors. This produces work that is technically valid but behaviorally wrong from the user's perspective — wrong defaults, non-human-readable output, integration paths that unit tests mock away. The agent declares DONE; the user finds it broken.

The root cause is that acceptance criteria are written in technical language, by the agent, at implementation time. UAC fixes this by requiring criteria to be written in user-observable language, elicited from the user, before implementation begins.

### UAC Lifecycle

```
Task intake
   ↓
UAC Declaration — written in user-observable language before any code is written
   ↓
Implementation
   ↓
End-to-end validation — at least one complete user journey verified
   ↓
Gap check — "what would the user notice that our tests would not catch?"
   ↓
UAC Evidence — per-item evidence cited (not assumed); unverifiable items flagged
   ↓
Status: complete
```

### UAC vs Technical Validation

| Dimension | Technical validation | User acceptance |
|---|---|---|
| Written by | Agent | Elicited from user at task intake |
| Language | Technical (test pass, lint clean) | Behavioral (user does X, user sees Y) |
| Coverage | Individual components | Complete end-to-end journey |
| Verified by | Automated tools | Agent simulation + explicit gap check |
| Timing | After each change | Before declaring complete |

### The Gap Check

Before closing any task, the agent must answer: **"What would the user notice that our tests would not catch?"** This surfaces the class of failures most likely to reach the user: integration paths that are mocked in tests, output that is syntactically valid but not usable, features that work in isolation but break in context.

---

## Validation Toolchain Prerequisite

Rule 22 (User Acceptance Gate) requires end-to-end validation. End-to-end validation requires tooling. Rule 23 in `.github/copilot-instructions.md` makes toolchain setup a mandatory prerequisite — not optional preparation.

### Why Tooling Must Be Selected Upfront

Tooling chosen late creates two failure modes:
1. **UAC items are unverifiable** — the agent writes acceptance criteria it cannot execute, then declares DONE based on unit tests
2. **Wrong tool for the project type** — a Playwright setup is useless for a pure CLI tool; an httpx integration test is insufficient for a browser-rendered frontend

Tooling must be selected at project adoption time, matched to the actual project type, and documented in the project adapter so every agent can access it.

### Validation Tiers

```
Unit        → isolated component behavior; mocks acceptable
Integration → cross-component behavior; no mocks on user-facing paths
End-to-end  → complete user journey; no mocks
```

The E2E tier is the direct prerequisite for UAC execution. A project without an E2E tool cannot satisfy Rule 22.

### Tool Selection by Project Type

| Project type | E2E tool |
|---|---|
| Web frontend | Playwright / Cypress |
| Backend API | Postman+Newman / curl script |
| CLI tool | Full command invocation + output assertion |
| Library / SDK | Consumer integration test |
| Full-stack | Browser + API combined |

Full tier breakdown (Unit + Integration + E2E) is in Rule 23.

### Where the Toolchain Lives

The validated toolchain is recorded in `.github/project-context.instructions.md` under **Validation Toolchain**. This places it in Layer 2 (Project Adapter) — loaded at task start, available to all agents without re-eliciting.

Bootstrap presets now help teams get to that state faster: `scripts/bootstrap_adoption.py` can render a first-pass project adapter for `backend-api`, `web-frontend`, `cli-tool`, `library`, or `full-stack` repositories. The generated values are starting points and still require project-specific confirmation.

### Toolchain Setup as Implementation Work

When a required toolchain tier is missing, the agent declares a setup subtask and completes it before any feature implementation step. Toolchain setup is not deferred. A task plan that skips toolchain setup when the toolchain is incomplete is invalid.

### Validation Contracts In This Repository

This template repository now validates itself in three layers:

1. `scripts/validate_template.py` checks required assets, key sections, cross-doc references, CI expectations, and bootstrap coverage
2. `python -m pytest tests/ -q` exercises the bootstrap helper, audit generator, and validator itself
3. `.github/workflows/ci.yml` runs the structured validator, the tests, and bootstrap smoke commands on supported Python versions

This does not eliminate project-specific verification, but it does reduce drift between the repository's claims and the assets it ships.

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
5. **Git closeout**: main thread commits and normally pushes after hard gates pass; only exception cases are escalated

---

## Long-Task Autonomous Execution

Multi-step tasks are the primary operational mode. The framework's default execution posture is autonomous forward progress — not wait-and-confirm. This posture is established by Rule 20 in `.github/copilot-instructions.md`.

Before entering that mode, the agent should emit a short execution contract for user confirmation. This is a one-time agreement on execution style, not a request for per-step permission.

### Execution Boundary

At task start, the agent declares an execution boundary that defines:

| Field | Content |
|---|---|
| Authorized scope | File set or module scope covered by this task |
| Authorized ops | Read, edit, lint, test, state updates, CLI fan-out |
| Hard stops | Protected paths, destructive git, scope conflict, Low-confidence irreversible decision |
| Check-in point | Phase boundary, acceptance criteria met, or explicit blocker |

Within the boundary, the agent proceeds without per-step confirmation. Operations such as reading files, loading the project adapter, running validation commands, and writing state documents are pre-authorized and do not produce STOP events.

### Execution Contract

The template ships `templates/execution_contract.template.md` to standardize this confirmation step. The contract should explicitly answer:

1. whether the default main-thread-agent ownership for normal `commit` and `push` should remain in place or be overridden
2. whether CLI or subagent fan-out is expected and what the fallback path is
3. whether autonomous while-loop execution is enabled
4. what technical and user-visible validation gates must pass before completion can be reported
5. what files are in scope, which paths are protected, and which conditions force escalation

This gives the user one high-leverage confirmation surface before the task enters autonomous execution without re-opening routine Git authorization on every task. The framework default remains: main-thread agent handles normal commit/push, and only exception cases escalate.

### Interruption Tiers

```
Tier 1 — Auto-proceed (no human needed):
  file reads · adapter loading · lint / test runs · state doc writes · CLI fan-out

Tier 2 — Batch at phase boundary (do not interrupt mid-task):
  Alignment: uncertain · pre-existing warnings · adjacent observations

Tier 3 — Hard stop (always interrupt, boundary cannot override):
  protected paths · destructive git ops · unresolvable source conflict ·
  Low-confidence irreversible decision · material scope expansion
```

### Interaction with Other Mechanisms

| Mechanism | Behavior inside a declared boundary |
|---|---|
| Self-check gate (Rule 12) | File reads and adapter loading auto-resolve — not surfaced as STOP |
| Failure recovery (Rule 13) | Missing context → resolve from code first; stop only if genuinely unresolvable |
| Progression loop (Rule 14) | `stop and ask` is last resort, not default for uncertain next steps |
| Reality check (Rule 17) | `uncertain` → flag and continue; `misaligned` → stop |

### Why This Is the Primary Mode

Short, interrupt-heavy loops degrade work quality. Context is lost between human turn-arounds, re-engagement adds latency, and reactive per-step confirmation is less safe than a clear boundary declared upfront. A well-declared boundary gives the agent permission to move and the human a precise contract for when they will be called.

---

## Demo And Release Surfaces

The framework now ships explicit assets for evaluation and rollout, not just operational rules.

### Demo Repository

`examples/demo_project/` exists to answer the question "what does an adopted repository actually look like?" It includes:

1. a customized project adapter
2. a small code and test surface
3. a ROADMAP and session-state file
4. committed task packet, audit receipt, and handoff packet artifacts

This is intentionally small. The goal is comprehension, not realism at production scale.

### Release Surface

The repository also includes lightweight release assets:

1. `VERSION` — current framework version
2. `CHANGELOG.md` — notable changes by release
3. `.github/RELEASE_TEMPLATE.md` — release note starter for maintainers
4. `docs/COMPATIBILITY.md` — verified surfaces, intended integrations, and known limits

These files do not change the framework's behavior directly. They exist to make adoption, support, and upgrade conversations more reliable.

---

## Dispatch Decision Logic

Before proceeding serially on a multi-step task, the agent evaluates whether to fan out:

```
Can the task be split into 2+ scopes where BOTH of the following are true for each scope?
  □ independent owner file set
  □ independent summarizable result
    → YES: fan-out by default; assign CLI executors first (Rule 19); declare any serial exemption explicitly
    → NO:  proceed serially; state which criterion failed
```

Fan-out is the default when both criteria are met. Independent validation is desirable but not a gate.

The dispatch decision is always disclosed in the user-visible reply, not just in the footer.

---

## Dispatch Stability

Dispatch can get stuck in two phases: before the task packet is sent (underspecified) or during execution (executor stops without signaling). Rule 21 in `.github/copilot-instructions.md` addresses both.

### Pre-Dispatch Readiness Gate

Before any executor is dispatched, the task packet must satisfy four conditions:

| Condition | Why it matters |
|---|---|
| Observable acceptance criteria | Executor can self-determine completion without human input |
| Bounded file scope (≤ 5 files) | Prevents context window exhaustion mid-task |
| Unambiguous entry point | Executor knows the first concrete action |
| Explicit do-not-touch list | Prevents silent scope creep |

A task packet that fails any condition is not dispatched. The main thread rewrites it first.

### Terminal State Contract

Every executor must end in one of three explicit states:

```
DONE      → acceptance criteria met; audit receipt written
STUCK     → cannot proceed; handoff packet written; blocker stated
ESCALATE  → scope has changed; handoff packet written; finding stated
```

Silent stopping is treated as `STUCK`. The main thread does not wait indefinitely — absence of a terminal state after expected scope triggers a handoff and fallback to the next executor (Rule 19).

### Progress Signal

For tasks touching more than 3 files, the executor emits a one-line signal after each file change:

```
Step N: [filename] — [PASS / FAIL / SKIP]
```

This makes executor liveness visible to the main thread without requiring polling.

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

### Doc-First As A Repository Default

Some repositories may elevate the planning layer into a doc-first execution policy.

When that policy is active, the planning layer is no longer only an internal thought step written into `session_state.md`. It is also externalized into durable planning surfaces such as:

1. a roadmap or design doc
2. a file-level execution checklist
3. a validation reference
4. a state-tracking doc

In that model, non-trivial implementation starts from those planning surfaces rather than from chat memory alone.

This is not a new layer. It is a repository-level specialization of the planning layer.

The global framework still supplies Rule 16 planning mechanics. The repository chooses whether to make doc-first planning the default execution posture for non-trivial work.

If adopted, the project adapter and entry documentation should say so explicitly, so future sessions do not treat doc-first planning as optional.

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

For multi-session or multi-executor work, failure recovery should also preserve resumability:

1. wrong assumption → correct it in `session_state.md`
2. interrupted execution → write a handoff packet
3. partial implementation → append an audit receipt before switching executor
4. failing hard gate → keep the failure outside the auditor narrative; do not hand-wave it away

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
START of loop iteration
   ↓
COMPLETE subtask
   ↓
RE-EVALUATE → Is the goal done?
   ↓ NO
REALITY CHECK (Rule 17) → Are we aligned with the original intent?
   ├── confirmed  → proceed
   ├── uncertain  → flag it; proceed with caution
   └── misaligned → revise plan (Rule 16) or stop and ask
   ↓
IDENTIFY    → What is the next concrete step?
   ↓
DECIDE      → continue · decompose (Rule 15) · stop and ask
   ↓
UPDATE      → session_state.md: Current Step + Next Planned Step
   ↓
REPORT      → ## Next Actions in the reply (includes Alignment field)
```

### How It Interacts with Other Layers

| Other mechanism | Interaction |
|---|---|
| **Self-check gate (Rule 12)** | Runs *within* a step — the loop runs *between* steps. They are not alternatives. |
| **Failure recovery (Rule 13)** | A failure can trigger "stop and ask" in the progression loop. The loop resumes after recovery is complete. |
| **Reality check (Rule 17)** | Runs *between* loop iterations — before IDENTIFY. Misalignment triggers plan revision or stop; uncertain alignment is flagged and tracked. |
| **Architect role** | Called by the progression loop when the next step requires design analysis before execution. |
| **Implementer role** | Called by the progression loop when the next step is a bounded execution task with known acceptance criteria. |
| **session_state.md** | Current Step and Next Planned Step are updated by the loop after every iteration. |

### Decomposition Decision (Rule 15)

When the "IDENTIFY" step reveals a next step that is compound, the agent runs the decomposition test:

```
All subtasks have independent owner files?    YES →
All subtasks produce summarizable results?    YES → fan-out (default); assign CLI first (Rule 19)
Either criterion fails?                        NO → proceed serially; state which criterion failed
```

Fan-out uses the Architect for design-uncertain or multi-option tasks and the Implementer for bounded execution tasks. Within each role, CLI is the primary executor and subagent is the fallback (Rule 19).

### Why This Matters

Without the progression loop, an agent that completes a step will stop and wait — even when the next step is obvious and safe. The loop makes forward motion the default and stopping the exception, while keeping explicit stop conditions for blockers and genuine ambiguity.

---

## Reality Check Layer

The reality check layer prevents the agent from confidently executing in the wrong direction. Where the progression model drives forward motion, the reality check layer provides a periodic course correction pulse — fast, not exhaustive.

### When It Runs

```
After every full loop cycle (not every micro-step)
   +
Before declaring Status: complete
   +
When Alignment: misaligned appears in any Next Actions block
```

### The Three Questions

The agent answers these three questions using evidence from the current session:

| Question | Evidence standard |
|---|---|
| Does the current state satisfy the user's original intent? | Traceable link from completed work → original goal statement |
| Are we solving the real problem — not just completing tasks? | Each step advances the goal, not just closes checklist items |
| Is there evidence (not assumption) that this works? | Validation ran, check passed, or user confirmed |

Unanswerable questions → `Alignment: uncertain`. Contradicted questions → `Alignment: misaligned`.

### Decision Outcomes

| Result | Action |
|---|---|
| `confirmed` | Continue — proceed to next step in the progression loop |
| `uncertain` | Flag it in `## Next Actions`; continue with caution; do not stop unless critical |
| `misaligned` | Revise the plan (Rule 16) if a better direction is visible; otherwise stop and ask |

### How It Interacts with Other Layers

| Mechanism | Interaction |
|---|---|
| **Progression loop (Rule 14)** | Reality check is a mandatory step inside the loop — between RE-EVALUATE and IDENTIFY |
| **Planning layer (Rule 16)** | Misalignment triggers a plan revision — reality check is the signal, Rule 16 is the response |
| **Failure recovery (Rule 13)** | A misaligned reality check is not a failure — it is a navigation correction. Record it in `session_state.md` as a plan revision, not a Mid-Session Correction, unless a wrong assumption caused it |
| **Next Actions contract** | Every `## Next Actions` block must carry an `Alignment` field: `confirmed / uncertain / misaligned` |

### Why This Matters

Planning (Rule 16) and progression (Rule 14) can both execute correctly and still miss the user's intent if the original goal was subtly mis-stated or if the execution drifted during a long task. The reality check is the mechanism that catches this drift before `Status: complete` is declared.

A fast alignment pulse — three questions, evidence only, one of three outcomes — is far less expensive than discovering at the end that the work addressed the wrong problem.

---

## Document Organization

| Type | Definition | Location |
|---|---|---|
| TYPE-A | Long-lived: architecture, runbooks, API specs | `docs/` or module root |
| TYPE-B | Module-local, evolves with code | module directory |
| TYPE-C | Phase reports, one-time analyses, summaries | `docs/archive/` |

`docs/INDEX.md` lists all TYPE-A docs. It is updated as part of the commit that adds or removes a TYPE-A doc.
