# Execution Contract

> Confirm this before any long-running or multi-step task starts.
> Goal: align execution style once, then let the agent proceed autonomously inside that boundary.

---

## Task Summary

- Goal: [one-sentence user-visible task goal]
- Scope: [allowed modules / files / systems]
- Out of Scope: [what should not be touched]

## Optional Fast-Start Block

Use this when the task is well-bounded and the repository wants a one-shot confirmation surface before execution begins.

Execution Boundary:
- Authorized scope: [file set or module scope]
- Authorized ops: [read / edit / lint / test / state updates / dispatch]
- Hard stops: [protected paths / destructive ops / source-of-truth conflicts / scope expansion]
- Check-in point: [phase boundary / acceptance checkpoint / explicit blocker]

Working Hypothesis:
- [one-sentence working assumption about cause, solution, or design direction]

Decomposition Decision:
- [fan-out / serial]
- [owner files or bounded scopes]
- [validation path per scope]
- [reason this split is or is not worth parallelizing]

---

## Planning Surfaces

- Roadmap or design doc: [path]
- Execution checklist: [path]
- Validation doc: [path]
- State doc: [path]
- Rule: if this is a non-trivial task and these surfaces do not exist yet, create or update them before implementation begins

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
- Task scope for developer execution: [file / module / service / full-stack]
- Highest developer-tool layer needed for this task: [diagnostics / lint / build / run / health / repro]
- If a command is `declared-unverified`: [attempt once and treat failure as recoverable / skip and log / custom]
- If a command is `known-broken`: [use fallback / stop and report / custom]
- Runtime entrypoint required for this task: [yes / no]
- Repro path required for this task: [yes / no]
- Required user-observable validation: [E2E path / smoke path / scenario simulation]
- Bootstrap-mode allowance: [none / toolchain setup / runtime entrypoint setup]
- User Acceptance Criteria (UAC):
  - [ ] When [user does X], [user observes Y]
  - [ ] When [user does X], [user observes Y]
- End-to-end scenario: [entry point → full path → observable result]
- If full E2E is not yet possible: [record the missing surface and how it will be introduced later]
- Gap check before closeout: [what the user would notice that tests might not catch]
- Completion rule: do not report complete until both technical and user-visible acceptance evidence exist
- If runtime behavior breaks during the task: [open or update a failure packet / lightweight note / custom]
- If cause remains only suspected at closeout: [create a root-cause note / record residual risk inline / custom]

Default developer-tool ladder:

`diagnostics → lint → build → run → health → repro`

Rule: stop at the minimum layer needed by the task scope unless runnable or user-visible proof was explicitly requested.

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
  - impacted surface marked sensitive in the project adapter
  - touched path or config declared security-sensitive in the project adapter

- After security-sensitive escalation, require:
  - impacted trust boundary
  - relevant config or secret surface
  - at least one negative-path or misuse-path validation claim

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
