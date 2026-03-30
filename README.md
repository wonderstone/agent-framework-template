# Agent Framework Template

A minimal, reusable GitHub Copilot agent framework. Drop it into any project to give your AI coding assistant structured decision rules, state management, and a clean operating protocol.

---

## What's Included

```
.github/
  copilot-instructions.md          ← operating rules (Rule 0–18, always loaded)
  project-context.instructions.md  ← project adapter (fill in for your project)
  agents/
    architect.agent.md             ← analysis / planning / critique agent
    implementer.agent.md           ← execution / validation / change agent
  instructions/
    backend.instructions.md        ← protocol for backend code changes
    docs.instructions.md           ← protocol for documentation changes

docs/
  INDEX.md                         ← navigation index for all TYPE-A docs
  FRAMEWORK_ARCHITECTURE.md        ← how the layer system works
  ADOPTION_GUIDE.md                ← step-by-step setup for a new project
  STRATEGY_MECHANISM_LAYERING.md   ← strategy-layer vs mechanism-layer design pattern
  ROLE_STRATEGY_EXAMPLES.md        ← concrete reviewer / agent role examples
  runbooks/
    resumable-git-audit-pipeline.md ← packet / receipt / handoff workflow
  archive/                         ← TYPE-C docs (phase reports, analyses)

templates/
  project-context.template.md      ← blank project adapter
  session_state.template.md        ← blank cross-session state file
  roadmap.template.md              ← blank ROADMAP with phase/subtask structure
  git_audit_task_packet.template.md ← task packet template for resumable audit work
  git_audit_receipt.template.md    ← audit receipt template
  git_audit_handoff_packet.template.md ← handoff packet template
  reviewer_role_profile.template.md ← formal role definition for reviewer or agent splits

examples/
  reviewer_roles/
    01_goal_acceptance_owner.md    ← first-batch strategy role
    02_plan_checkpoint_owner.md    ← first-batch strategy role
    03_runtime_correctness_reviewer.md ← first-batch strategy role
    04_boundary_contract_reviewer.md ← first-batch strategy role
    05_git_closeout_reviewer.md    ← first-batch strategy role
    06_maintainability_reviewer.md ← first-batch strategy role
    07_observability_failure_path_reviewer.md ← second-batch strategy role
    08_performance_benchmark_reviewer.md ← second-batch strategy role
    09_migration_compatibility_reviewer.md ← second-batch strategy role
    10_docs_spec_drift_reviewer.md ← second-batch strategy role

scripts/
  validate-template.sh             ← checks template integrity (run after setup)
  git_audit_pipeline.py            ← generates task packet / receipt / handoff assets
```

---

## Quick Start

### Minimal setup (3 files)

```bash
# 1. Copy the core rules
cp .github/copilot-instructions.md          your-repo/.github/
cp .github/project-context.instructions.md  your-repo/.github/

# 2. Initialize session state
cp templates/session_state.template.md      your-repo/session_state.md

# 3. Fill in the project adapter
#    Edit your-repo/.github/project-context.instructions.md
#    Replace all [placeholders] with real values
```

### Full setup

See [`docs/ADOPTION_GUIDE.md`](docs/ADOPTION_GUIDE.md) for a complete walkthrough.

---

## Core Concepts

**Layered instruction loading** — rules are loaded on-demand, not all at once:

| Layer | File | Loaded when |
|---|---|---|
| 1 — Operating rules | `copilot-instructions.md` | Always |
| 2 — Project adapter | `project-context.instructions.md` | Multi-step task starts / keyword match |
| 3 — Canonical docs | `docs/*.md` | Topic confirmed relevant |
| 4 — Code files | actual source files | Immediately before edit |

**Resumable audit assets** — multi-step implementation and git review work can be externalized into three portable artifacts:

- `task packet` — freezes truth sources, allowed files, validation, and acceptance boundary
- `audit receipt` — records what an executor or reviewer actually changed and verified
- `handoff packet` — captures resume point, blocker, and next executor when a CLI or agent session is interrupted

The template ships a canonical runbook, three templates, and `scripts/git_audit_pipeline.py` to generate these assets under `tmp/git_audit/<task_slug>/`.

**Self-check gate** — every action follows **think → self-check → act**. Before touching any file, the agent answers five gate questions (file read? path protected? adapter loaded? sources consistent? scope clear?). If any answer is NO, the agent stops and resolves the problem before proceeding. This is enforced in Rule 12.

**Enforcement rules** — rules 0–18 include explicit STOP conditions and recovery/progression hooks. When a required pre-condition is not met, the agent states why it is blocked and waits — it does not guess, skip, or proceed with Low confidence. Key STOP triggers: unread target file, protected path, conflicting sources, unclear scope, unresolved handoff state.

**Failure recovery** — when the agent makes a wrong assumption or produces an invalid change, Rule 13 requires it to state the failure explicitly, record it in `session_state.md` under Mid-Session Corrections, apply a defined recovery action, and only then resume. Stopping is always preferred over continuing on a known-wrong path.

**Cognitive reasoning loop** — a lightweight discipline that runs across all four layers:

- **Hypothesize**: form a working assumption before acting
- **Validate**: check against docs and code as each layer loads
- **Revise**: update the hypothesis explicitly when evidence conflicts — never silently
- **Calibrate**: state uncertainty when confidence is Low; do not act without flagging it

**State tracking** — `session_state.md` at repo root tracks:
- Current goal
- Working hypothesis, confidence level, and supporting evidence
- Active work and what's completed this phase
- Mid-session corrections (mistakes and course corrections)
- Acceptance criteria
- Technical decisions and durable insights

**Resumable git audit workflow** — when work is split across external Codex, subagents, or multiple CLI sessions, the agent does not rely on chat history alone. It creates a task packet before fan-out, records audit receipts after scoped execution, and emits a handoff packet when a session is interrupted. This behavior is governed by Rule 18 and the runbook at `docs/runbooks/resumable-git-audit-pipeline.md`.

**Strategy layer vs mechanism layer** — the template now makes an explicit distinction between:

- `strategy layer`: what each reviewer, CLI, or specialized agent is formally responsible for
- `mechanism layer`: how bounded work is frozen, validated, handed off, and recovered when execution is interrupted

This means repositories can define domain-specific role splits such as “runtime correctness reviewer” vs “maintainability reviewer” without re-inventing packet, receipt, handoff, and hard-gate behavior every time.

The important boundary is: roles should be named after the judgment they provide, not after the current tool that happens to implement them. A CLI, subagent, or custom agent is an executor choice, not the strategy-layer identity.

The template also ships a concrete example set in `docs/ROLE_STRATEGY_EXAMPLES.md`, covering not just two external CLIs but broader role families such as git closeout reviewer, protocol boundary reviewer, performance reviewer, observability reviewer, and migration reviewer. These examples are role-first and executor-pluggable by design.

If you want something more concrete than a doc example list, the template now also ships a starter set of 10 formal role profiles under `examples/reviewer_roles/`. The first batch covers goal/acceptance, plan/checkpointing, correctness, boundary/contracts, git closeout, and maintainability. The second batch covers observability/failure-paths, performance, migration/compatibility, and docs/spec drift.

**Completion checkpoints** — when a subtask is confirmed done, the agent updates ROADMAP, session state, acceptance criteria, and the reply footer before moving on.

---

## Compatibility

Works with any AI coding assistant that loads `.github/copilot-instructions.md`:

- GitHub Copilot (Workspace / Chat)
- Cursor
- Augment Code
- Windsurf
- Any tool that respects `.github/copilot-instructions.md` or a configurable system prompt

---

## Customization Points

| What to customize | Where |
|---|---|
| Project directory map | `project-context.instructions.md` → Project Map |
| Topic → doc routing | `project-context.instructions.md` → Critical Topic Triggers |
| Build/test commands | `project-context.instructions.md` → Build and Test Commands |
| Protected paths | `project-context.instructions.md` → Protected Paths |
| Footer language | `copilot-instructions.md` → Rule 8 |
| Agent roles/format | `.github/agents/*.agent.md` |
| Strategy-vs-mechanism guidance | `docs/STRATEGY_MECHANISM_LAYERING.md` |
| Concrete role examples | `docs/ROLE_STRATEGY_EXAMPLES.md` |
| Concrete starter role profiles | `examples/reviewer_roles/*.md` |
| Git audit packet defaults | `templates/git_audit_*.template.md` + `scripts/git_audit_pipeline.py` |
| Reviewer / CLI role profiles | `templates/reviewer_role_profile.template.md` |

---

## License

[Add your license here]
