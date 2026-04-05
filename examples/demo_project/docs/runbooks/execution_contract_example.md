# Demo Execution Contract

> Filled example for the committed `add_task_priority` demo task.

---

## Task Summary

- Goal: add task priority labels to the demo CLI without breaking resumable audit review.
- Scope: `src/task_tracker.py`, `tests/test_task_tracker.py`, `tmp/git_audit/add_task_priority/`, and the demo roadmap or state surfaces needed for truthful closeout.
- Out of Scope: unrelated CLI features, packaging changes, or framework-level rule edits.

## Optional Fast-Start Block

Execution Boundary:
- Authorized scope: demo project code, tests, and the bounded audit artifacts for `add_task_priority`
- Authorized ops: read, edit, run focused tests, update task packet or receipt artifacts, and normal git closeout for the bounded demo task
- Hard stops: protected-path conflicts, destructive git operations, source-of-truth conflicts, or scope expansion beyond the demo feature
- Check-in point: feature acceptance reached, explicit blocker found, or review handoff required

Working Hypothesis:
- The feature can stay small if priority is modeled as additional task metadata plus focused CLI output assertions.

Decomposition Decision:
- serial
- owner files: `src/task_tracker.py`, `tests/test_task_tracker.py`, `tmp/git_audit/add_task_priority/`
- validation path: focused pytest plus audit-artifact review
- reason this split is not worth parallelizing: the code and audit artifacts are tightly coupled and small enough for one bounded pass

## Long-Loop Closeout Contract

- Progress unit: review pass
- True closeout boundary: feature implemented, focused tests pass, and packet or receipt artifacts are truthful
- Intermediate batch rule: finishing one file edit is progress only, not final closeout
- Host closeout rule: do not trigger host closeout until the demo feature and audit artifacts agree

## User Confirmation Checklist

### 1. Git Closeout Policy

- Normal `git add` / `git commit` / standard `git push` path: main thread agent
- High-risk Git operations requiring explicit user confirmation:
  - `push --force`
  - reset or rebase of published history
  - branch deletion
  - remote target change

### 2. Dispatch And Fallback Policy

- Fan-out allowed: no
- Preferred executors: main thread, then reviewer if the audit stalls
- Maximum file scope per dispatched subtask: `≤ 5 files`
- Parallel ceiling: `1`
- CLI or subagent fallback if execution fails, stalls, or times out:
  1. write a handoff packet in `tmp/git_audit/add_task_priority/`
  2. resume in a new bounded review session

### 3. Long-Task Execution Mode

- Autonomous while-loop mode: enabled
- Doc-first mode for non-trivial work: enabled
- Progress unit for while-mode work: review pass
- True closeout boundary for while-mode work: bounded feature complete or explicit blocker
- Intermediate batches may trigger progress updates only: yes
- Host closeout action reserved for the true boundary only: yes

### 4. Validation And Completion Gate

- Minimum technical validation: `python3 -m pytest tests/test_task_tracker.py -q`
- Task scope for developer execution: module
- Highest developer-tool layer needed for this task: lint plus focused test
- Runtime entrypoint required for this task: no
- Repro path required for this task: no
- Required user-observable validation: adding a priority is visible in CLI output and persisted in task state
- User Acceptance Criteria:
  - [x] When a user adds a task with a priority, the CLI stores and displays that priority.
  - [x] When review is interrupted, the packet or receipt artifacts still show what changed and how to resume.
- End-to-end scenario: add a priority-tagged task, list tasks, run focused tests, and inspect the packet or receipt trail.
- Gap check before closeout: terminal output formatting could still drift even if focused tests stay green, so the receipt should mention the visible output path.

### 5. Scope Boundary

- Allowed files or directories:
  - `src/task_tracker.py`
  - `tests/test_task_tracker.py`
  - `tmp/git_audit/add_task_priority/`
  - `ROADMAP.md`
  - `session_state.md`
- Protected or excluded files or directories:
  - framework-level files outside `examples/demo_project/`
- Unrelated cleanup allowed: no

### 6. Escalation Rules

- Escalate immediately for:
  - protected paths
  - destructive operations
  - source-of-truth conflict
  - material scope expansion
  - inability to satisfy the validation gate

### 7. State And Handoff Rules

- Update `session_state.md` when: feature checkpoint reached, blocker appears, or the owner changes
- Use packet or receipt or handoff artifacts when: review is interrupted or another executor must resume
- Host closeout action available: none
- Status line rule: routine progress uses `• 当前在做: ... | 下一步: ...`
- Final closeout summary lives in: final reply body

## Agent Self-Check Summary

- Git policy understood: yes
- Dispatch and fallback policy understood: yes
- Long-task mode understood: yes
- Validation gate understood: yes
- Scope and escalation rules understood: yes
- Status-line or closeout-summary rule understood: yes
