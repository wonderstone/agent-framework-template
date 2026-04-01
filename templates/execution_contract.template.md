# Execution Contract

> Confirm this before any long-running or multi-step task starts.
> Goal: align execution style once, then let the agent proceed autonomously inside that boundary.

---

## Task Summary

- Goal: [one-sentence user-visible task goal]
- Scope: [allowed modules / files / systems]
- Out of Scope: [what should not be touched]

---

## Planning Surfaces

- Roadmap or design doc: [path]
- Execution checklist: [path]
- Validation doc: [path]
- State doc: [path]
- Rule: if this is a non-trivial task and these surfaces do not exist yet, create or update them before implementation begins

---

## User Confirmation Checklist

### 1. Git Closeout Policy

- Normal `git add` / `git commit` / standard `git push` path: main thread agent (default; override only if this repository wants a different owner)
- High-risk Git operations requiring explicit user confirmation:
  - `push --force`
  - rebase or reset of published history
  - branch deletion
  - remote or branch target change

### 2. Dispatch And Fallback Policy

- Fan-out allowed: [yes / no]
- Preferred executors: [main thread / CLI / subagent / reviewer role]
- CLI or subagent fallback if execution fails, stalls, or times out:
  1. [fallback path 1]
  2. [fallback path 2]

### 3. Long-Task Execution Mode

- Autonomous while-loop mode: [enabled / disabled]
- Doc-first mode for non-trivial work: [enabled / disabled]
- Standard check-in points:
  - [phase boundary]
  - [acceptance checkpoint]
  - [explicit blocker]
  - [scope change]

### 4. Validation And Completion Gate

- Minimum technical validation: [lint / typecheck / focused tests / workspace checks]
- Required user-observable validation: [E2E path / smoke path / scenario simulation]
- Completion rule: do not report complete until both technical and user-visible acceptance evidence exist

### 5. Scope Boundary

- Allowed files / directories:
  - [path]
- Protected or excluded files / directories:
  - [path]
- Unrelated cleanup allowed: [yes / no]

### 6. Escalation Rules

- Escalate immediately for:
  - protected paths
  - destructive operations
  - source-of-truth conflict
  - material scope expansion
  - inability to satisfy the validation gate

### 7. State And Handoff Rules

- Update `session_state.md` when: [decision / checkpoint / interruption / blocker]
- Use packet / receipt / handoff artifacts when: [multi-executor / interrupted session / external audit]

---

## Agent Self-Check Summary

- Git policy understood: [yes / no]
- Dispatch and fallback policy understood: [yes / no]
- Long-task mode understood: [yes / no]
- Validation gate understood: [yes / no]
- Scope and escalation rules understood: [yes / no]

If any answer is `no`, the agent must stop and resolve the gap before entering execution mode.
