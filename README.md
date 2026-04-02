# Agent Framework Template

A minimal, reusable GitHub Copilot agent framework. Drop it into any project to give your AI coding assistant structured decision rules, state management, and a clean operating protocol.

---

## Why This Exists

Most agent setups fail in one of three ways:

- the rules live only in chat history
- the project-specific truth sources are never made explicit
- multi-step work cannot survive a reviewer swap or interrupted CLI session

This template exists to make those failure modes harder by default. It gives teams a repeatable operating layer, a project adapter, resumable audit artifacts, and now a product-style adoption path with bootstrap tooling, CI, and a concrete demo repository.

---

## What's Included

```
.github/
  copilot-instructions.md          ← operating rules (Rule 0–27, always loaded)
  project-context.instructions.md  ← project adapter (fill in for your project)
  RELEASE_TEMPLATE.md              ← lightweight release notes template
  workflows/
    ci.yml                         ← validates integrity and tests on push / PR
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
  COMPATIBILITY.md                 ← verified surfaces, intended integrations, known limits
  DOC_FIRST_EXECUTION_GUIDELINES.md ← repository-default doc-first planning rule for non-trivial work
  LEFTOVER_UNIT_CONTRACT.md        ← how to classify and record partial work truthfully
  STRATEGY_MECHANISM_LAYERING.md   ← strategy-layer vs mechanism-layer design pattern
  ROLE_STRATEGY_EXAMPLES.md        ← concrete reviewer / agent role examples
  RUNTIME_SURFACE_PROTECTION.md    ← guard-registry pattern for live user-facing paths
  runbooks/
    resumable-git-audit-pipeline.md ← packet / receipt / handoff workflow
  archive/                         ← TYPE-C docs (phase reports, analyses)

templates/
  doc_first_execution_guidelines.template.md ← reusable doc-first policy surface for adopters
  execution_contract.template.md   ← pre-execution confirmation contract for long tasks
  project-context.template.md      ← blank project adapter
  session_state.template.md        ← blank cross-session state file
  roadmap.template.md              ← blank ROADMAP with phase/subtask structure
  git_audit_task_packet.template.md ← task packet template for resumable audit work
  git_audit_receipt.template.md    ← audit receipt template
  git_audit_handoff_packet.template.md ← handoff packet template
  reviewer_role_profile.template.md ← formal role definition for reviewer or agent splits
  runtime_surface_registry.template.py ← registry skeleton for runtime surface guard definitions

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
  bootstrap_adoption.py           ← bootstraps minimal / standard / full adoption into another repo
  closeout_truth_audit.py         ← diff-aware receipt-anchor audit for truth-source closeout claims
  install_git_hooks.sh            ← activates the shipped .githooks path in an adopting repo
  runtime_surface_guardrails.py   ← registry-driven runner for runtime surface staged/live checks
  validate-template.sh             ← checks template integrity (run after setup)
  validate_template.py             ← structured validator used by CI and local checks
  git_audit_pipeline.py            ← generates task packet / receipt / handoff assets

.githooks/
  pre-commit                      ← optional hook that runs closeout audit and staged runtime guards
  pre-push                        ← optional hook that runs runtime push checks
```

---

## Quick Start

### Copy-Paste Adoption Prompt

If you want another agent to copy this framework into a local application repository in one pass, paste the prompt below and replace the placeholders first.

```text
You are working in my application repository at <TARGET_REPO_PATH>.

Use the local agent framework template at <TEMPLATE_REPO_PATH>.

Goal:
- bootstrap the agent framework from the template repo into this application repo
- use project name <PROJECT_NAME>
- use profile <minimal|standard|full>
- use project type <backend-api|web-frontend|cli-tool|library|full-stack>
- add optional capabilities only if requested: <closeout-audit runtime-guards git-hooks>

Required steps:
1. Run the template bootstrap script from <TEMPLATE_REPO_PATH> targeting <TARGET_REPO_PATH>.
2. Keep the generated framework files in their template paths.
3. Fill in the generated `.github/project-context.instructions.md` placeholders using this repo's real structure, commands, and protected paths.
4. Leave unrelated application code untouched.
5. Run validation from the target repo:
  - `python3 scripts/validate_template.py`
  - if the repo uses the full Python test path, also run `python3 -m pytest tests/ -q` when appropriate
6. Report:
  - what files were added or changed
  - what placeholders still need manual project-specific values
  - what validation was run and whether it passed

Constraints:
- do not delete existing application files unless required by the framework setup and explicitly justified
- prefer the standard profile unless I ask for a lighter or fuller setup
- if doc-first execution should be the default for this repo, also wire `docs/DOC_FIRST_EXECUTION_GUIDELINES.md`
```

### Fastest setup

Use the bootstrap script when you want a working starting point without manually copying files one by one:

```bash
python scripts/bootstrap_adoption.py ../your-repo \
  --project-name "Your Project" \
  --profile standard
```

Optional capabilities:

- `--capability closeout-audit` — ship executable receipt-anchor auditing
- `--capability runtime-guards` — ship runtime guard runner plus registry skeleton
- `--capability git-hooks` — ship `.githooks/` and installer without forcing activation

Profiles:

- `minimal` — core rules, state files, and doc index only
- `standard` — recommended default; adds agents, framework docs, validation, audit tooling, and CI
- `full` — adds reviewer-role examples, strategy docs, and the committed demo project

### Manual minimal setup

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

## Pre-Execution Confirmation

Before any long-running or multi-step task, the agent should produce an execution contract for user confirmation. Use [`templates/execution_contract.template.md`](templates/execution_contract.template.md) to confirm:

- whether the default main-thread-agent ownership for normal commit / push should stay in place or be overridden
- whether CLI or subagent fan-out is expected and what the fallback plan is
- whether the task runs in autonomous while-loop mode
- what technical plus end-to-end or user-visible validation must pass before completion is reported
- what scope, escalation, and state-update rules apply

The default is: main-thread agent handles normal `git add` / `commit` / standard `push`, and only exception cases are escalated. This confirmation is meant to override that default when needed, not to force per-step micromanagement.

If a repository wants roadmap/design-first execution to be the default for non-trivial work, it can also ship [`docs/DOC_FIRST_EXECUTION_GUIDELINES.md`](docs/DOC_FIRST_EXECUTION_GUIDELINES.md) from [`templates/doc_first_execution_guidelines.template.md`](templates/doc_first_execution_guidelines.template.md) and route doc-first triggers to it through the project adapter.

---

## Example Workflow

If you want one concrete path instead of reading the full framework first:

1. Run `python scripts/bootstrap_adoption.py ../your-repo --project-name "Your Project" --profile standard`
2. Open the generated `.github/project-context.instructions.md` and replace the default commands
3. Run `python3 scripts/validate_template.py`
4. Review [`examples/demo_project/`](examples/demo_project/) for a tiny adopted repository with a committed packet / receipt / handoff cycle

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

**Enforcement rules** — rules 0–27 include explicit STOP conditions, recovery/progression hooks, user-acceptance gating, validation-toolchain prerequisites, leftover-state discipline, receipt-anchored closeout constraints, independent evaluation, and policy-audit activation. When a required pre-condition is not met, the agent states why it is blocked and waits — it does not guess, skip, or proceed with Low confidence. Key STOP triggers: unread target file, protected path, conflicting sources, unclear scope, unresolved handoff state, unverifiable acceptance criteria, or closeout claims without evidence.

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
- For while-style work, the progress unit, true closeout boundary, and host closeout action
- Mid-session corrections (mistakes and course corrections)
- Acceptance criteria
- Technical decisions and durable insights

**Resumable git audit workflow** — when work is split across external Codex, subagents, or multiple CLI sessions, the agent does not rely on chat history alone. It creates a task packet before fan-out, records audit receipts after scoped execution, and emits a handoff packet when a session is interrupted. This behavior is governed by Rule 18 and the runbook at `docs/runbooks/resumable-git-audit-pipeline.md`.

**Receipt-anchored closeout audit** — `scripts/closeout_truth_audit.py` turns Rule 25 into a diff-aware executable check. It inspects staged or working-tree diffs and fails when truth-source completion claims appear without a receipt anchor in the same batch.

**Runtime surface protection** — [`docs/RUNTIME_SURFACE_PROTECTION.md`](docs/RUNTIME_SURFACE_PROTECTION.md) now pairs the governance pattern with opt-in executable scaffolding. The template ships a generic guard runner, registry skeleton, and optional hooks, while adopters still provide the real surfaces, banned phrases, focused tests, and live validators.

**Leftover unit contract** — [`docs/LEFTOVER_UNIT_CONTRACT.md`](docs/LEFTOVER_UNIT_CONTRACT.md) defines how to classify partial work, record why it stopped, and preserve a clean re-entry point instead of leaving vague TODO debt behind.

**Strategy layer vs mechanism layer** — the template now makes an explicit distinction between:

- `strategy layer`: what each reviewer, CLI, or specialized agent is formally responsible for
- `mechanism layer`: how bounded work is frozen, validated, handed off, and recovered when execution is interrupted

This means repositories can define domain-specific role splits such as “runtime correctness reviewer” vs “maintainability reviewer” without re-inventing packet, receipt, handoff, and hard-gate behavior every time.

The important boundary is: roles should be named after the judgment they provide, not after the current tool that happens to implement them. A CLI, subagent, or custom agent is an executor choice, not the strategy-layer identity.

The template also ships a concrete example set in `docs/ROLE_STRATEGY_EXAMPLES.md`, covering not just two external CLIs but broader role families such as git closeout reviewer, protocol boundary reviewer, performance reviewer, observability reviewer, and migration reviewer. These examples are role-first and executor-pluggable by design.

If you want something more concrete than a doc example list, the template now also ships a starter set of 10 formal role profiles under `examples/reviewer_roles/`. The first batch covers goal/acceptance, plan/checkpointing, correctness, boundary/contracts, git closeout, and maintainability. The second batch covers observability/failure-paths, performance, migration/compatibility, and docs/spec drift.

**Completion checkpoints** — when a subtask is confirmed done, the agent updates ROADMAP, session state, acceptance criteria, and the current status line or closeout summary before moving on.

**Progress vs closeout formatting** — [`docs/PROGRESS_UPDATE_TEMPLATE.md`](docs/PROGRESS_UPDATE_TEMPLATE.md) defines the stable shape for in-progress while-loop updates, and [`docs/CLOSEOUT_SUMMARY_TEMPLATE.md`](docs/CLOSEOUT_SUMMARY_TEMPLATE.md) defines the stable final closeout shape for hosts that expose a terminal action such as `task_complete`.

The current visual contract is:

- routine in-progress replies use `• 当前在做: ... | 下一步: ...`
- use `• 当前聚焦: ... | 正在做: ... | 下一步: ...` only when the focus needs to be explicit
- final closeout keeps exactly one `📍` footer and places `---` immediately before it

---

## Compatibility

Works with any AI coding assistant that loads `.github/copilot-instructions.md`:

- GitHub Copilot (Workspace / Chat)
- Cursor
- Augment Code
- Windsurf
- Any tool that respects `.github/copilot-instructions.md` or a configurable system prompt

Read [`docs/COMPATIBILITY.md`](docs/COMPATIBILITY.md) for what is actually verified in this repository versus what adopters still need to validate locally.

---

## Customization Points

| What to customize | Where |
|---|---|
| Project directory map | `project-context.instructions.md` → Project Map |
| Topic → doc routing | `project-context.instructions.md` → Critical Topic Triggers |
| Build/test commands | `project-context.instructions.md` → Build and Test Commands |
| Protected paths | `project-context.instructions.md` → Protected Paths |
| Status-line language | `copilot-instructions.md` → Rule 8 |
| Agent roles/format | `.github/agents/*.agent.md` |
| Strategy-vs-mechanism guidance | `docs/STRATEGY_MECHANISM_LAYERING.md` |
| Concrete role examples | `docs/ROLE_STRATEGY_EXAMPLES.md` |
| Concrete starter role profiles | `examples/reviewer_roles/*.md` |
| Git audit packet defaults | `templates/git_audit_*.template.md` + `scripts/git_audit_pipeline.py` |
| Adoption bootstrap flow | `scripts/bootstrap_adoption.py` |
| Doc-first execution default | `docs/DOC_FIRST_EXECUTION_GUIDELINES.md` + `templates/doc_first_execution_guidelines.template.md` |
| Long-task execution contract | `templates/execution_contract.template.md` |
| Closeout truth audit | `scripts/closeout_truth_audit.py` |
| Runtime guard registry | `templates/runtime_surface_registry.template.py` + `scripts/runtime_surface_guardrails.py` |
| Optional git hooks | `.githooks/` + `scripts/install_git_hooks.sh` |
| Reviewer / CLI role profiles | `templates/reviewer_role_profile.template.md` |

---

## License

MIT
