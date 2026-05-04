# Design-Gated Bounded Autonomy

This runbook defines a concrete workflow for tasks that are too open-ended for immediate implementation but still benefit from autonomous execution once the boundary is frozen.

It absorbs three external ideas into one local mechanism:

1. `Superpowers` — design or plan approval is a real gate before implementation
2. `gstack` — routing and project learnings should be explicit instead of implicit
3. `autoresearch` — long-running autonomy works best when the mutable surface, metric, and revert rule are tightly bounded

---

## When To Use

Use this runbook when all of the following are true:

1. the task is non-trivial enough that immediate coding would likely drift
2. there is a stable owner or user-visible outcome that can be approved before execution
3. the implementation can be broken into bounded loops with a clear keep or revert rule

Do not use this runbook when:

1. the task is a tiny local edit with one obvious path
2. the task depends on unresolved external decisions that the user has not approved
3. the task has no honest validation or revert surface

---

## Core Rule

Do not grant autonomy to an unfrozen problem.

Autonomy starts only after four things are explicit:

1. route
2. gate
3. loop boundary
4. evidence surface

---

## Workflow

### Step 1 — Route The Task Explicitly

State which local mechanism or role owns the task before implementation starts.

Minimum routing declaration:

```text
Route:
- Primary skill or mechanism: <name>
- Why this route: <one sentence>
- What is not being invoked: <one sentence>
```

Examples:

1. `frontend-design` for UI direction and implementation quality
2. `context7-docs` for version-sensitive upstream API truth
3. main-thread execution with bounded validator loop for local code changes

Rule:

if routing is ambiguous, do not start autonomous implementation yet.

### Step 2 — Freeze The Design Gate

Before implementation, produce the smallest reviewable design or plan artifact that answers:

1. what will change
2. what will not change
3. how success is observed
4. what would cause the implementation to be rejected or revised

Minimum gate artifact:

```text
Design Gate:
- Goal: <one sentence>
- In scope: <explicit bullets>
- Out of scope: <explicit bullets>
- Acceptance check: <command, scenario, or file proof>
- Approval state: pending | approved
```

Rule:

no implementation skill, subagent, or long-running loop begins until the gate is `approved`.

### Step 3 — Define The Bounded Loop

Convert the approved gate into a loop that can run honestly.

Minimum bounded-loop declaration:

```text
Loop Boundary:
- Mutable surface: <file, directory, or artifact set>
- Fixed surfaces: <read-only files, metrics, or harnesses>
- Keep rule: <what counts as an improvement>
- Revert rule: <when to discard and roll back>
- Timeout or stop rule: <max time, attempts, or batch size>
```

Preferred pattern:

1. one narrow mutable surface at a time
2. one focused validation action after each change
3. keep or revert immediately

Rule:

if the task cannot name a keep rule and revert rule, it is not ready for bounded autonomy.

### Step 4 — Execute With Keep-Or-Revert Discipline

For each loop iteration:

1. make one bounded change
2. run the defined validation
3. compare against the keep rule
4. keep or revert
5. record the result briefly before the next iteration

Minimum progress log:

```text
Loop Iteration N
- Change: <one sentence>
- Validation: <command or proof>
- Result: keep | revert | blocked
- Reason: <one sentence>
```

Rule:

do not stack multiple speculative edits before validating the current loop iteration.

### Step 5 — Land Reusable Learnings

At the end of the loop, decide whether the result changed future behavior.

If yes:

1. route it through post-task harvest
2. land it in the lightest truthful surface

If no:

1. do not manufacture a framework lesson

Rule:

local learnings are valuable only when they change future routing, gating, or loop setup.

---

## Default Packet Shape

Use this compact packet when a task needs the full runbook but not a larger discussion or audit packet.

Canonical starter file:

`templates/design_gated_bounded_autonomy_packet.template.md`

```text
Design-Gated Bounded Autonomy Packet

Route:
- Primary skill or mechanism:
- Why this route:
- What is not being invoked:

Design Gate:
- Goal:
- In scope:
- Out of scope:
- Acceptance check:
- Approval state:

Loop Boundary:
- Mutable surface:
- Fixed surfaces:
- Keep rule:
- Revert rule:
- Timeout or stop rule:
```

Rule:

use the shipped template when the packet should survive handoff or bootstrap; use the inline shape only for very small local planning notes.

---

## How This Maps To Existing Framework Surfaces

| Runbook step | Existing framework surface |
|---|---|
| explicit route | SKILL triggers and strategy-mechanism split |
| design gate | Rule 16 plan selection plus Rule 22 user acceptance framing |
| bounded loop | Rule 20 execution boundary plus Rule 4 validation floor |
| keep or revert | local validation plus honest stop or rollback discipline |
| learning landing | post-task harvest workflow |

---

## Non-Goals

This runbook does not:

1. create a new canonical skill taxonomy
2. replace discussion packets, task packets, or audit receipts where those are already the correct heavier-weight mechanism
3. justify indefinite autonomy without a bounded validation surface

---

## Updated Boundary

`Superpowers`, `gstack`, and `autoresearch` remain external references, not bundled host frameworks.

What the framework absorbs here is only the reusable execution behavior:

1. explicit routing
2. approval gates before implementation
3. bounded keep-or-revert autonomy
4. durable learnings only when behavior really changes

> Updated 2026-05-04: initial runbook created to turn the extracted `Superpowers`, `gstack`, and `autoresearch` patterns into one concrete local workflow, with a matching reusable packet template for adopters.