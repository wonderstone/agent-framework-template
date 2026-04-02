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

## Optional Fast-Start Block

Paste or adapt this block when a task-start ritual needs one compact surface that freezes execution, validation, and closeout rules up front:

```text
Planning Surfaces:
- Roadmap or design doc: [path]
- Execution checklist: [path]
- Validation doc: [path]
- State doc: [path]

Execution Boundary:
- Authorized scope: [file set or module scope]
- Authorized ops: read · edit · lint · test · state updates · fan-out to CLI
- Hard stops: [protected paths / destructive git / scope conflict / low-confidence irreversible decision]
- Check-in point: [phase boundary / acceptance criteria met / explicit blocker reached]
- Parallel ceiling: [default 5 when fan-out is used; `1` when no fan-out is intended]

Long-Loop Closeout Contract:
- Progress unit: [module / batch / slice / review pass]
- True closeout boundary: [full task complete / explicit blocker / user-requested checkpoint]
- Intermediate batch rule: finishing one progress unit is a progress update only, not final closeout
- Host closeout rule: do not trigger `task_complete` or equivalent host closeout action until the true closeout boundary is reached

Working Hypothesis:
- Hypothesis: [one sentence]
- Confidence: [High / Medium / Low]

User Acceptance Criteria (UAC):
- [ ] When [user does X], [user observes Y]
- [ ] When [user does X], [user observes Y]

End-to-end scenario:
- [entry point -> full path -> observable result]

Decomposition Decision:
- Scale: [Simple / Compound / Complex]
- Proceeding serially because: [reason]
  or
- Subtasks: [subtask -> owner files]
- Generator: [main thread / CLI / subagent]
- Evaluator: [separate CLI / subagent / context-reset main thread]
- Fallback: [CLI -> subagent / escalate]
```

Use this block when teams repeatedly miss execution-boundary declarations, task-specific UAC, dispatch disclosure, fallback ownership, or the progress-versus-closeout distinction for while-style work.

## Long-Loop Closeout Contract

- Progress unit: [module / batch / slice / review pass]
- True closeout boundary: [full task complete / explicit blocker / user-requested checkpoint]
- Intermediate batch rule: finishing one progress unit is a progress update only, not final closeout
- Host closeout rule: do not trigger `task_complete` or equivalent host closeout action until the true closeout boundary is reached

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
- Maximum file scope per dispatched subtask: [≤ 5 files / custom bound]
- Parallel ceiling: [default 5 / custom bound / `1`]
- CLI or subagent fallback if execution fails, stalls, or times out:
  1. [fallback path 1]
  2. [fallback path 2]

### 3. Long-Task Execution Mode

- Autonomous while-loop mode: [enabled / disabled]
- Doc-first mode for non-trivial work: [enabled / disabled]
- Progress unit for while-mode tasks: [module / batch / slice / review pass]
- True closeout boundary for while-mode tasks: [full wave / real blocker / explicit checkpoint]
- Intermediate batches may trigger progress updates only: [yes / no]
- Host closeout action reserved for the true boundary only: [yes / no]
- Standard check-in points:
  - [phase boundary]
  - [acceptance checkpoint]
  - [explicit blocker]
  - [scope change]

### 4. Validation And Completion Gate

- Minimum technical validation: [lint / typecheck / focused tests / workspace checks]
- Required user-observable validation: [E2E path / smoke path / scenario simulation]
- Bootstrap-mode allowance: [none / toolchain setup / runtime entrypoint setup]
- User Acceptance Criteria (UAC):
  - [ ] When [user does X], [user observes Y]
  - [ ] When [user does X], [user observes Y]
- End-to-end scenario: [entry point → full path → observable result]
- If full E2E is not yet possible: [record the missing surface and how it will be introduced later]
- Gap check before closeout: [what the user would notice that tests might not catch]
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
- Host closeout action available: [none / `task_complete` / other]
- Platform continuation markers to ignore as completion signals: [e.g. `Continued with Autopilot` / none]
- Status line rule:
- Routine in-progress replies use: `• 当前在做: <action> | 下一步: <next step>`
- Use the longer focus-bearing variant only when ambiguity exists: `• 当前聚焦: <focus> | 正在做: <action> | 下一步: <next step>`
- Final closeout may use exactly one footer and must place `---` immediately before it: `📍 当前聚焦: <final focus> | 已完成: <outcome> | 下一步: <none / next / blocker>`
- Final closeout summary lives in: [final reply body / `task_complete.summary` / other host closeout payload]
- Closeout summary template: [`docs/CLOSEOUT_SUMMARY_TEMPLATE.md` / custom]
- Progress update template: [`docs/PROGRESS_UPDATE_TEMPLATE.md` / custom]

---

## Agent Self-Check Summary

- Git policy understood: [yes / no]
- Dispatch and fallback policy understood: [yes / no]
- Long-task mode understood: [yes / no]
- Validation gate understood: [yes / no]
- Scope and escalation rules understood: [yes / no]
- Status-line / closeout-summary rule understood: [yes / no]

If any answer is `no`, the agent must stop and resolve the gap before entering execution mode.
