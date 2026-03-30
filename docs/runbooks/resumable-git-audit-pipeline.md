# Resumable Git Audit Pipeline

This runbook turns Git audit and reviewer handoff into a recoverable workflow rather than a chat-only memory exercise.

## Goal

Use this workflow whenever implementation, audit, and Git closeout may span multiple executors or multiple interrupted sessions.

The point is not to find one perfect reviewer. The point is to preserve enough state that a different reviewer or CLI session can resume safely.

## Core Roles

| Role | Responsibility |
|---|---|
| `Planner` | Freeze truth sources, allowed files, validation, and acceptance boundary |
| `Executor` | Perform the bounded implementation or investigation |
| `Auditor` | Review the result, risks, and validation status |
| `Gatekeeper` | Run hard gates outside the semantic auditor when possible |
| `Owner Review` | Final acceptance, conflict resolution, and Git closeout |

The auditor is replaceable. The hard gate should not be.

## Canonical Artifacts

| Artifact | Purpose | Default path |
|---|---|---|
| `task packet` | Freeze the task before fan-out or external review | `tmp/git_audit/<task_slug>/task_packet.md` |
| `audit receipt` | Record what happened in one scoped execution or review pass | `tmp/git_audit/<task_slug>/audit_receipt.md` |
| `handoff packet` | Preserve resume point and blocker when switching executor | `tmp/git_audit/<task_slug>/handoff_packet.md` |

## When To Use It

Use this workflow when any of the following is true:

1. The task is important enough that losing chat history would slow recovery.
2. An external Codex / CLI reviewer is involved.
3. More than one executor will touch or audit the same task.
4. Git closeout depends on a semantic audit that might need retry or replacement.

## Minimum Flow

1. Generate a task packet before dispatch.
2. Run the bounded execution.
3. Record an audit receipt after that execution.
4. If the session stops or ownership changes, write a handoff packet before resuming elsewhere.
5. Run hard gates.
6. Return to main-thread owner review and Git closeout.

## Hard-Gate Principle

Semantic reviewers can disagree. Hard gates exist to answer the question the reviewer cannot settle alone.

Examples:

1. tests
2. type checks
3. lint
4. schema validation
5. repository-specific sync checks

Do not let an auditor's narrative override a failing hard gate.

## Recommended CLI

Use the bundled generator script:

```bash
python scripts/git_audit_pipeline.py init-task ...
python scripts/git_audit_pipeline.py record-receipt ...
python scripts/git_audit_pipeline.py create-handoff ...
```

## Relationship To The Rest Of The Framework

This runbook does not add a fifth instruction layer.

It complements the framework like this:

1. `.github/copilot-instructions.md` decides when the workflow is mandatory.
2. `.github/project-context.instructions.md` routes `audit|handoff|receipt|packet` topics here.
3. `docs/FRAMEWORK_ARCHITECTURE.md` explains why these artifacts sit alongside the four-layer load model.
4. `scripts/git_audit_pipeline.py` and the templates make the workflow operational.