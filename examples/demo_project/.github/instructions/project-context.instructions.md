---
name: "Project Context Adapter"
applyTo: "**"
description: >
  Demo Task Tracker project adapter. Provides the project map, canonical docs,
  critical topic triggers, protected paths, build/test commands, and runtime
  config locations for the demo repository.
---

# Demo Task Tracker — Project Context

## Project Map

| Path | Purpose |
|---|---|
| `src/` | CLI commands, parsing, and task tracker logic |
| `tests/` | Unit and smoke-style tests |
| `docs/` | Architecture and workflow docs |
| `tmp/` | Generated audit artifacts for review recovery |
| `.github/` | Agent behavior rules and project adapter |

## Canonical Docs

| Doc | Purpose |
|---|---|
| `README.md` | Project entry point |
| `docs/ARCHITECTURE.md` | Domain model and command flow |
| `docs/runbooks/demo-workflow.md` | End-to-end bootstrap and audit walkthrough |
| `docs/INDEX.md` | TYPE-A doc navigation index |
| `ROADMAP.md` | Phase planning and acceptance targets |
| `session_state.md` | Current goal, working hypothesis, and decisions |

## Task Recovery Sequence

1. Read this file
2. Read `docs/INDEX.md`
3. Read `docs/ARCHITECTURE.md` for command and data flow context
4. Read the code or tests you plan to touch
5. If the work spans sessions, read `session_state.md` and any packet / receipt / handoff files under `tmp/git_audit/`

## Critical Topic Triggers

| Trigger keywords | Canonical doc |
|---|---|
| `architecture\|design\|command flow` | `docs/ARCHITECTURE.md` |
| `audit\|handoff\|receipt\|packet\|git closeout` | `docs/runbooks/demo-workflow.md` |
| `traceability\|recovery\|root cause\|incident\|failure packet\|runtime evidence\|user surface map` | `docs/runbooks/demo-workflow.md` |
| `roadmap\|phase\|milestone` | `ROADMAP.md` |
| `current focus\|hypothesis\|blocker` | `session_state.md` |
| `developer toolchain\|diagnostics\|repro path\|verification status` | Developer Toolchain section (this file) |

## Validation Toolchain

Project type: cli-tool

| Tier | Tool | Command |
|---|---|---|
| Unit | pytest | `pytest tests/ -q` |
| Integration | pytest | `pytest tests/test_task_tracker.py -q` |
| End-to-end | shell smoke test | `python -m src.task_tracker --demo` |

```bash
# Run full suite (all tiers in sequence)
pytest tests/ -q && python -m src.task_tracker --demo
```

## Developer Toolchain

Primary language: Python

Package manager: pip

| Surface | Command or source | Scope | Status | Fallback or stop | Notes |
|---|---|---|---|---|---|
| Diagnostics | `python -m compileall src tests` | `module` | `verified-working` | Stop after compile blockers are cleared unless broader proof is required | Fast syntax check for the demo CLI |
| Run | `python -m src.task_tracker --demo` | `service` | `verified-working` | Inspect stderr and stop if the demo entrypoint fails | Primary local CLI run path |
| Health or smoke | `python -m src.task_tracker --demo` | `service` | `verified-working` | Stop and report if the demo command cannot run honestly | The same command acts as the smoke path |
| Repro path | `python -m src.task_tracker --demo` | `service` | `verified-working` | Use the demo command output as the user-visible repro | Shortest user-visible flow |
| Build | `python -m compileall src tests` | `module` | `verified-working` | Stop after build blockers are cleared when runnable proof is unnecessary | No packaging step beyond compile check |
| Lint | `python -m compileall src tests` | `file` | `verified-working` | Stop after static blockers are cleared when task scope is local | Demo keeps lint surface lightweight |

### Runtime Evidence

| Evidence surface | Applies to | Priority | Status | Fallback or stop | Notes |
|---|---|---|---|---|---|
| Logs | `demo CLI execution` | `first` | `verified-working` | Fall back to stderr capture or stop and report missing runtime evidence | The demo command output is the primary runtime evidence surface |
| Health check | `demo command` | `first` | `verified-working` | Stop and report if the command cannot run honestly | `python -m src.task_tracker --demo` |
| Smoke path | `primary user flow` | `first` | `verified-working` | Fall back to logs and stop if the visible CLI path cannot be exercised honestly | The smoke path is the same as the user-visible demo path |

## User Surface Map

| Surface name | Owner path | Sensitive | Fastest repro path | Primary evidence source | Notes |
|---|---|---|---|---|---|
| `demo task listing flow` | `src/task_tracker.py` | `no` | `python -m src.task_tracker --demo` | `Logs` | Main user-visible CLI walkthrough |
| `audit recovery workflow` | `tmp/git_audit/` and `docs/runbooks/demo-workflow.md` | `yes` | inspect committed packet / receipt / handoff files and rerun the demo command | `Logs` | Sensitive because it demonstrates traceability and recovery truth to adopters |

## Security-Sensitive Surfaces And Escalation

Sensitive path declarations:

| Path or surface | Why sensitive |
|---|---|
| `tmp/git_audit/` | audit and handoff truth surface |
| `session_state.md` | cross-session source of truth |
| `.github/instructions/project-context.instructions.md` | long-lived repository truth for future sessions |

Escalation rule:

1. automatically escalate failure tracking when an impacted user surface is marked `Sensitive = yes`
2. automatically escalate when a failure touches a declared sensitive path, config surface, secret surface, or trust-boundary surface
3. after escalation, require the failure artifact to record:
   impacted trust boundary, relevant config or secret surface, and at least one negative-path or misuse-path validation claim
4. human classification may upgrade severity further, but should not be the only trigger

## Build and Test Commands

```bash
# Type check
python -m compileall src tests

# Run tests
pytest tests/ -q

# Lint
python -m compileall src tests

# Build
python -m compileall src tests

# Start
python -m src.task_tracker --demo
```

## Protected Paths

| Path | Why protected |
|---|---|
| `tmp/git_audit/` | Audit history — do not rewrite without preserving review trace |
| `session_state.md` | Cross-session source of truth — edit deliberately and explicitly |

## Runtime Config Locations

| Location | What it controls |
|---|---|
| `src/task_tracker.py` | Demo defaults and CLI behavior |
| `tmp/git_audit/` | Execution-state artifacts generated by the audit workflow |

## Dangerous Operations Policy

- `tmp/git_audit/` → do not delete audit artifacts casually; they demonstrate recovery flow
- `session_state.md` → revise explicitly when assumptions change

## Notes

- This demo keeps everything local and file-based so the workflow is easy to inspect.
- If runtime behavior breaks during demo work, open a failure packet first and add a root-cause note before claiming the issue is fully understood.
