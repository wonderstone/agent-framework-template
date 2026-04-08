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
  RELEASE_TEMPLATE.md              ← lightweight release notes template
  workflows/
    ci.yml                         ← validates integrity and tests on push / PR
  agents/
    architect.agent.md             ← analysis / planning / critique agent
    implementer.agent.md           ← execution / validation / change agent
  instructions/
    project-context.instructions.md ← project adapter (fill in for your project)
    backend.instructions.md        ← protocol for backend code changes
    docs.instructions.md           ← protocol for documentation changes

docs/
  INDEX.md                         ← navigation index for all TYPE-A docs
  FRAMEWORK_ARCHITECTURE.md        ← how the layer system works
  ADOPTION_GUIDE.md                ← step-by-step setup for a new project
  COMPATIBILITY.md                 ← verified surfaces, intended integrations, known limits
  STRICT_ADOPTION_AND_VERIFICATION.md ← strict adoption baseline, enforcement matrix, and local CLI verification flow
  SKILL_HARVEST_LOOP_V1_DRAFT.md   ← formal v1 design for post-task SKILL harvest and promotion governance
  SKILL_EXECUTION_LAYER_V1_DRAFT.md ← formal v1 design for invocation receipts, bounded candidate triggers, and typed evolution lineage
  SKILL_MECHANISM_V1_DRAFT.md      ← formal v1 design for the framework-native SKILL contract
  TRACEABILITY_AND_RECOVERY_V1_DRAFT.md ← formal v1 design for traceability and recovery layout
  AI_TRACEABILITY_AND_RECOVERY_DISCUSSION.md ← discussion history behind that design
  DEVELOPER_TOOLCHAIN_DESIGN.md    ← formal v1 design for the Developer Toolchain contract
  DEVELOPER_TOOLCHAIN_DISCUSSION.md ← discussion history and tradeoffs behind that contract
  DOC_FIRST_EXECUTION_GUIDELINES.md ← repository-default doc-first planning rule for non-trivial work
  LEFTOVER_UNIT_CONTRACT.md        ← how to classify and record partial work truthfully
  STRATEGY_MECHANISM_LAYERING.md   ← strategy-layer vs mechanism-layer design pattern
  ROLE_STRATEGY_EXAMPLES.md        ← concrete reviewer / agent role examples
  RUNTIME_SURFACE_PROTECTION.md    ← guard-registry pattern for live user-facing paths
  ANTI_DRIFT_RULE_REFACTOR_PLAN_V1.md ← mechanism-first plan for checkpoint, sync-audit, repair, and rule rebase work
  PROGRESS_UPDATE_TEMPLATE.md      ← stable format for in-progress while-loop status updates
  CLOSEOUT_SUMMARY_TEMPLATE.md     ← stable format for final closeout summaries
  runbooks/
    multi-model-discussion-loop.md ← append-only discussion workflow for open design questions
    resumable-git-audit-pipeline.md ← packet / receipt / handoff workflow
    state-reconciliation.md        ← drift-packet workflow for reconciling truth surfaces before closeout
  archive/                         ← TYPE-C docs (phase reports, analyses)

templates/
  discussion_packet.template.md   ← append-only discussion packet for design debates
  doc_first_execution_guidelines.template.md ← reusable doc-first policy surface for adopters
  execution_contract.template.md   ← pre-execution confirmation contract for long tasks
  execution_progress_receipt.template.md ← receipt-bearing checkpoint artifact for long-running execution
  skill_invocation_receipt.template.md ← runtime invocation evidence surface for skill use
  skill_candidate_packet.template.md ← candidate packet for post-task SKILL harvest proposals
  skill_promotion_receipt.template.md ← promotion receipt for canonical SKILL mutation decisions
  skill.template.md                ← framework-native SKILL contract template
  skill_tool_wrapper.template.md   ← starter scaffold for binding a skill to a declared toolchain surface
  skill_reviewer_gate.template.md  ← starter scaffold for receipt-anchored independent evaluation
  skill_pipeline.template.md       ← starter scaffold for staged execution with explicit handoff artifacts
  skill_artifact_generator.template.md ← bounded generator scaffold for schema-backed artifact initialization
  failure_packet.template.md       ← progressive runtime failure packet
  drift_reconciliation_packet.template.md ← reconciliation packet for unresolved execution-state drift
  project-context.template.md      ← blank project adapter
  root_cause_note.template.md      ← closeout note for cause-suspected vs cause-established recovery
  session_state.template.md        ← blank cross-session state file
  roadmap.template.md              ← blank ROADMAP with phase/subtask structure
  git_audit_task_packet.template.md ← task packet template for resumable audit work
  git_audit_receipt.template.md    ← audit receipt template
  git_audit_handoff_packet.template.md ← handoff packet template
  reviewer_role_profile.template.md ← formal role definition for reviewer or agent splits
  runtime_surface_registry.template.py ← registry skeleton for runtime surface guard definitions

examples/
  skills/
    01_discussion_packet_workflow.md ← workflow-style starter skill example
    02_no_placeholder_runtime_guardrail.md ← guardrail-style starter skill example
    03_developer_toolchain_wrapper.md ← wrapper-style starter skill example
    04_receipt_anchored_reviewer.md ← reviewer-style starter skill example
    05_staged_handoff_pipeline.md ← pipeline-style starter skill example
    06_bounded_artifact_generator.md ← bounded generator starter skill example
  full_stack_project/              ← minimal-profile full-stack reference repo for multi-runtime Developer Toolchain shape
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
  active_docs_audit.py           ← checks live docs for nonportable paths and stale framework assertions
  bootstrap_adoption.py           ← bootstraps minimal / standard / full adoption into another repo
  closeout_truth_audit.py         ← diff-aware receipt-anchor audit for truth-source closeout claims
  discussion_pipeline.py          ← generates and extends discussion packets for multi-model debate
  preference_drift_audit.py       ← detects agent preference drift against declared project-context rules
  state_sync_audit.py             ← contradiction-focused audit for task packets, receipts, session_state, and ROADMAP sync
  state_sync_pipeline.py          ← helper for progress receipts and drift reconciliation packets
  install_git_hooks.sh            ← activates the shipped .githooks path in an adopting repo
  skill_evolution_pipeline.py     ← initializes invocation receipts and candidate packets for execution-side skill evolution
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

If you want another agent to absorb this framework into its own project in one pass, paste the prompt below and replace the placeholders first. This version is intentionally strict: it is meant to stop downstream repositories from copying only the wording while skipping the mechanisms that make the framework real.

```text
You are working in my application repository at <TARGET_REPO_PATH>.

Template source of truth:
https://github.com/wonderstone/agent-framework-template

Do not assume the template already exists on the same machine.
If needed, first clone or otherwise fetch the template repository so you can read its real files before making changes.

Goal:
- absorb the framework in strict mode into this application repo
- use project name <PROJECT_NAME>
- use profile <minimal|standard|full>
- use project type <backend-api|web-frontend|cli-tool|library|full-stack>
- add optional capabilities only if requested: <closeout-audit runtime-guards git-hooks>
- if long-term skill accumulation matters in this repo, keep the SKILL and harvest-governance surfaces rather than dropping them during setup
- do not mechanically copy every template surface, but also do not silently weaken the mechanism stack and then blame the template for the resulting gap

Strict baseline to keep unless honestly inapplicable:
- truthful project-context adapter
- execution contract for long-running work
- checkpoint, receipt, drift-reconciliation, and state-sync surfaces for multi-step execution
- receipt-anchored closeout enforcement
- user-acceptance plus validation-toolchain honesty
- independent evaluation path for non-trivial or user-facing work
- resumable packet and handoff flow when multi-executor work is possible
- discussion-packet workflow when design ambiguity exists

Adoption status rule:
- only report `fully adopted` if all applicable strict-baseline mechanisms are present and locally verified
- if one baseline mechanism is downgraded or skipped, report `partially adopted` or `design-only upgrade path kept`
- do not overclaim policy-guided surfaces as if they were mechanically enforced

Required steps:
1. Fetch or clone the template repository from the public source-of-truth URL if you do not already have a readable copy.
2. Inspect the current application repository first and map every strict-baseline mechanism to a concrete target-repo file, script, runbook, or local equivalent.
3. If bootstrap is the right path, run the template bootstrap script from your fetched template copy targeting <TARGET_REPO_PATH>.
4. Keep the generated framework files in their template paths unless you have a project-specific reason to change them.
5. Fill in the generated `.github/instructions/project-context.instructions.md` placeholders:
   - project directory map, critical topic triggers, build/test commands, and protected paths
   - Developer Toolchain section (diagnostics, run, health, repro, build, verify) — the validator
     hard-fails if required-core fields are missing or malformed
6. Keep these high-value template mechanisms whenever they match the repository's real operating model:
   - truthful project-context adapter
   - execution contract for long-running work
   - progressive Developer Toolchain contract
   - runtime or failure traceability surfaces
   - resumable receipt or handoff surfaces for longer reviews or audits
   - closeout truthfulness surfaces
  - discussion-packet workflow for open design choice
  - independent evaluation path for non-trivial or user-facing work
7. If this repository should improve with repeated use, keep these SKILL and harvest-governance surfaces together:
   - `docs/SKILL_MECHANISM_V1_DRAFT.md`
   - `docs/SKILL_HARVEST_LOOP_V1_DRAFT.md`
  - `docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md`
   - `templates/skill.template.md`
  - `templates/skill_invocation_receipt.template.md`
   - `templates/skill_candidate_packet.template.md`
   - `templates/skill_promotion_receipt.template.md`
   - starter examples under `examples/skills/`
8. If you keep the SKILL path, adapt at least one initial repository-specific skill for a repeated pain point.
   Prefer one workflow skill or one guardrail skill first rather than a large skill catalog.
9. Preserve the governance boundary:
   - do not convert raw transcripts directly into canonical SKILL edits
   - harvest reusable observations into candidate packets first
   - use promotion receipts for canonical approved mutations
  - treat invocation receipts and runtime signals as candidate evidence, not as canonical truth by themselves
10. If this repository is not ready for SKILL-based accumulation yet, say so explicitly and keep only the future upgrade path that still makes sense.
11. Leave unrelated application code untouched.
12. Run validation from the target repo:
  - `python3 scripts/validate_template.py`
  - `python3 scripts/active_docs_audit.py` — checks for nonportable paths and stale framework assertions in shipped docs
  - if the repo uses the full Python test path, also run `python3 -m pytest tests/ -q` when appropriate
13. Run independent local CLI verification after the implementation pass:
  - use the same verification question against all locally available CLI executors, such as Claude, Codex, Gemini, and Copilot
  - keep each CLI pass read-only
  - require each CLI to answer whether the strict baseline mechanisms were truly kept, whether anything was silently downgraded, and whether any adoption claim overstates enforcement
  - if the repo keeps the discussion workflow, record these reviews in one durable discussion or verification packet
  - resolve critical or major gaps, then re-run target-repo validation
14. Report:
  - what files were added or changed
  - what placeholders still need manual project-specific values
  - what validation was run and whether it passed
  - which local CLI executors were used for independent verification and what unresolved gaps remained
  - whether the repo is `fully adopted`, `partially adopted`, or `design-only upgrade path kept`
  - whether the repo kept the SKILL and harvest surfaces, and if so which first skill was initialized
  - whether the repo also kept the execution-layer surfaces for invocation receipts and typed evolution lineage
  - which template features were intentionally kept, downgraded, or skipped based on project fit
  - which surfaces remain design-only or workflow-driven rather than mechanically enforced

Constraints:
- do not delete existing application files unless required by the framework setup and explicitly justified
- prefer the standard profile unless I ask for a lighter or fuller setup
- if doc-first execution should be the default for this repo, also wire `docs/DOC_FIRST_EXECUTION_GUIDELINES.md`
- do not claim the repo will automatically self-improve unless you also wire the SKILL and harvest-governance surfaces honestly
- do not claim that runtime skill usage rewrites canonical truth automatically; runtime receipts and triggers may propose candidates, but canonical mutation still needs the declared promotion path
- do not invent fake runtime paths, fake E2E, or fake enforcement just to match the template more closely
- do not let the main-thread agent self-certify strict adoption quality without independent local CLI review
```

For the strict baseline, enforcement-maturity matrix, and the local CLI verification flow in durable doc form, see [`docs/STRICT_ADOPTION_AND_VERIFICATION.md`](docs/STRICT_ADOPTION_AND_VERIFICATION.md).

### Fastest setup

Use the bootstrap script when you want a working starting point without manually copying files one by one:

```bash
python3 scripts/bootstrap_adoption.py ../your-repo \
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
mkdir -p your-repo/.github/instructions
cp .github/instructions/project-context.instructions.md  your-repo/.github/instructions/

# 2. Initialize session state
cp templates/session_state.template.md      your-repo/session_state.md

# 3. Fill in the project adapter
#    Edit your-repo/.github/instructions/project-context.instructions.md
#    Replace all [placeholders] with real values, including the Developer Toolchain section
```

### Full setup

See [`docs/ADOPTION_GUIDE.md`](docs/ADOPTION_GUIDE.md) for a complete walkthrough.

---

## Pre-Execution Confirmation

Before any long-running or multi-step task, the agent should produce an execution contract for user confirmation. Use [`templates/execution_contract.template.md`](templates/execution_contract.template.md) to confirm:

- whether the default main-thread-agent ownership for normal commit / push should stay in place or be overridden
- whether CLI or subagent fan-out is expected and what the fallback plan is
- whether the task runs in autonomous while-loop mode
- what stable task ID, checkpoint rule, truth surfaces, and state-sync schedule govern the task
- what technical plus end-to-end or user-visible validation must pass before completion is reported
- what scope, escalation, and state-update rules apply

The default is: main-thread agent handles normal `git add` / `commit` / standard `push`, and only exception cases are escalated. This confirmation is meant to override that default when needed, not to force per-step micromanagement.

This repository ships the execution-contract template and one filled demo example at [`examples/demo_project/docs/runbooks/execution_contract_example.md`](examples/demo_project/docs/runbooks/execution_contract_example.md). It does not automatically prove that every adopting repository instantiates an execution contract for every long task unless that repository adds its own workflow or validation checks.

When repositories want checkpoint truth to be mechanically recoverable instead of chat-only, they should also keep the state-sync surfaces together:

- [`docs/ANTI_DRIFT_RULE_REFACTOR_PLAN_V1.md`](docs/ANTI_DRIFT_RULE_REFACTOR_PLAN_V1.md)
- [`templates/execution_progress_receipt.template.md`](templates/execution_progress_receipt.template.md)
- [`templates/drift_reconciliation_packet.template.md`](templates/drift_reconciliation_packet.template.md)
- [`docs/runbooks/state-reconciliation.md`](docs/runbooks/state-reconciliation.md)
- [`scripts/state_sync_pipeline.py`](scripts/state_sync_pipeline.py)
- [`scripts/state_sync_audit.py`](scripts/state_sync_audit.py)

The template now absorbs Google's five skill patterns asymmetrically: Wrapper, Reviewer, and Pipeline ship as concrete starter scaffolds, Generator stays bounded to schema-backed artifact generation, and Inversion remains deferred until the framework can name a truthful host-runtime contract.

Starter scaffold paths: `templates/skill_tool_wrapper.template.md`, `templates/skill_reviewer_gate.template.md`, `templates/skill_pipeline.template.md`, and `templates/skill_artifact_generator.template.md`.

Progress and closeout preference summary:

- routine in-progress replies use `• 当前在做: ... | 下一步: ...`
- use `• 当前聚焦: ... | 正在做: ... | 下一步: ...` only when the focus needs to be explicit
- final closeout keeps exactly one `📍` footer and places `---` immediately before it

If a repository wants roadmap/design-first execution to be the default for non-trivial work, it can also ship [`docs/DOC_FIRST_EXECUTION_GUIDELINES.md`](docs/DOC_FIRST_EXECUTION_GUIDELINES.md) from [`templates/doc_first_execution_guidelines.template.md`](templates/doc_first_execution_guidelines.template.md) and route doc-first triggers to it through the project adapter.

If a repository wants open design questions to go through a durable multi-model discussion before coding, it can also ship [`docs/runbooks/multi-model-discussion-loop.md`](docs/runbooks/multi-model-discussion-loop.md), keep [`templates/discussion_packet.template.md`](templates/discussion_packet.template.md), and use [`scripts/discussion_pipeline.py`](scripts/discussion_pipeline.py) to collect executor feedback into one append-only Markdown packet.

If a repository wants formal SKILL surfaces instead of ad hoc prompt snippets, it can also ship [`docs/SKILL_MECHANISM_V1_DRAFT.md`](docs/SKILL_MECHANISM_V1_DRAFT.md), [`docs/SKILL_HARVEST_LOOP_V1_DRAFT.md`](docs/SKILL_HARVEST_LOOP_V1_DRAFT.md), keep [`templates/skill.template.md`](templates/skill.template.md), and adapt the starter examples under [`examples/skills/`](examples/skills/).

The current SKILL contract now also includes a field-level receipt and review matrix, so repositories can say which evidence tiers may propose changes to `purpose`, `triggers`, `entry_instructions`, `references`, `governance`, and `degradation`, and how `guardrail` skills become stricter.

If a repository wants skills to improve through repeated execution rather than only through after-the-fact review, it can also ship [`docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md`](docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md), keep [`templates/skill_invocation_receipt.template.md`](templates/skill_invocation_receipt.template.md), and use [`scripts/skill_evolution_pipeline.py`](scripts/skill_evolution_pipeline.py) to initialize invocation receipts and candidate packets from real runtime evidence.

If a repository wants to make the harvest loop executable instead of leaving it as design-only guidance, it can also keep [`templates/skill_candidate_packet.template.md`](templates/skill_candidate_packet.template.md) and [`templates/skill_promotion_receipt.template.md`](templates/skill_promotion_receipt.template.md) as the default candidate/proof artifacts.

---

## Example Workflow

If you want one concrete path instead of reading the full framework first:

1. Run `python3 scripts/bootstrap_adoption.py ../your-repo --project-name "Your Project" --profile standard`
2. Open the generated `.github/instructions/project-context.instructions.md` and replace the default commands plus Developer Toolchain starter values
3. Run `python3 scripts/validate_template.py`
4. Review [`examples/demo_project/`](examples/demo_project/) for a tiny adopted repository with a committed packet / receipt / handoff cycle
5. Review [`examples/full_stack_project/`](examples/full_stack_project/) if your repo has multiple runtimes or a cross-layer repro path and you want a minimal-profile reference rather than a fully bootstrapped adopter

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

**Multi-model discussion loop** — when the problem is "which direction should we choose?" rather than "implement the obvious next step", the agent can freeze the decision question in a discussion packet, ask available executors such as Claude Code, Codex, Gemini, Copilot, repo-local agents, or subagents to append feedback, and then let the main thread synthesize whether to freeze a plan or run a narrower second round. This behavior is governed by the runbook at `docs/runbooks/multi-model-discussion-loop.md` and the generator at `scripts/discussion_pipeline.py`.

**Self-check gate** — every action follows **think → self-check → act**. Before touching any file, the agent answers five gate questions (file read? path protected? adapter loaded? sources consistent? scope clear?). If any answer is NO, the agent stops and resolves the problem before proceeding. This is enforced in Rule 12.

**Enforcement rules** — rules 0–27 include explicit STOP conditions, recovery/progression hooks, user-acceptance gating, validation-toolchain prerequisites, leftover-state discipline, receipt-anchored closeout constraints, independent evaluation, and policy-audit activation. When a required pre-condition is not met, the agent states why it is blocked and waits — it does not guess, skip, or proceed with Low confidence. Key STOP triggers: unread target file, protected path, conflicting sources, unclear scope, unresolved handoff state, unverifiable acceptance criteria, or closeout claims without evidence.

Current enforcement tier in this repository:

- mechanically checked surfaces include `scripts/validate_template.py`, `scripts/active_docs_audit.py`, `scripts/preference_drift_audit.py`, unit tests, CI, and `scripts/closeout_truth_audit.py` when the optional hooks are installed
- mechanically checked root-only self-hosting also now includes an obvious-stale-state audit for the repository's own `session_state.md`
- instruction-bound surfaces still include adopter-specific `session_state.md` freshness, execution-contract instantiation, and most Rule 0–27 behavioral discipline outside the shipped hooks

Adopters should not treat instruction-bound rules as hook-enforced guarantees unless they add repo-local checks for them.

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

**Developer Toolchain** — [`docs/DEVELOPER_TOOLCHAIN_DESIGN.md`](docs/DEVELOPER_TOOLCHAIN_DESIGN.md) defines the agent-facing contract for diagnostics, run, health, repro, build, and verification status. [`docs/DEVELOPER_TOOLCHAIN_DISCUSSION.md`](docs/DEVELOPER_TOOLCHAIN_DISCUSSION.md) preserves the discussion history and tradeoffs that led to the current design.

Bootstrap-generated adopters now also receive a manifest-declared Developer Toolchain required-core contract. That lets the copied validator hard-fail missing or malformed core fields while still leaving optional enrichment surfaces advisory.

**Traceability and recovery layout** — [`docs/TRACEABILITY_AND_RECOVERY_V1_DRAFT.md`](docs/TRACEABILITY_AND_RECOVERY_V1_DRAFT.md) defines how adopters should lay out `User Surface Map`, `Runtime Evidence`, `failure_packet`, and `root_cause_note` surfaces so future agents can reconstruct failures instead of patching blindly. [`docs/AI_TRACEABILITY_AND_RECOVERY_DISCUSSION.md`](docs/AI_TRACEABILITY_AND_RECOVERY_DISCUSSION.md) keeps the reasoning and tradeoffs behind that layout visible.

**Leftover unit contract** — [`docs/LEFTOVER_UNIT_CONTRACT.md`](docs/LEFTOVER_UNIT_CONTRACT.md) defines how to classify partial work, record why it stopped, and preserve a clean re-entry point instead of leaving vague TODO debt behind.

**Strategy layer vs mechanism layer** — the template now makes an explicit distinction between:

- `strategy layer`: what each reviewer, CLI, or specialized agent is formally responsible for
- `mechanism layer`: how bounded work is frozen, validated, handed off, and recovered when execution is interrupted

This means repositories can define domain-specific role splits such as “runtime correctness reviewer” vs “maintainability reviewer” without re-inventing packet, receipt, handoff, and hard-gate behavior every time.

The important boundary is: roles should be named after the judgment they provide, not after the current tool that happens to implement them. A CLI, subagent, or custom agent is an executor choice, not the strategy-layer identity.

The template also ships a concrete example set in `docs/ROLE_STRATEGY_EXAMPLES.md`, covering not just two external CLIs but broader role families such as git closeout reviewer, protocol boundary reviewer, performance reviewer, observability reviewer, and migration reviewer. These examples are role-first and executor-pluggable by design.

If you want something more concrete than a doc example list, the template now also ships a starter set of 10 formal role profiles under `examples/reviewer_roles/`. The first batch covers goal/acceptance, plan/checkpointing, correctness, boundary/contracts, git closeout, and maintainability. The second batch covers observability/failure-paths, performance, migration/compatibility, and docs/spec drift.

**Completion checkpoints** — when a subtask is confirmed done, the agent updates ROADMAP, session state, acceptance criteria, and the current status line or closeout summary before moving on.

**Progress vs closeout formatting** — [`docs/PROGRESS_UPDATE_TEMPLATE.md`](docs/PROGRESS_UPDATE_TEMPLATE.md) defines the stable shape for in-progress while-loop updates, and [`docs/CLOSEOUT_SUMMARY_TEMPLATE.md`](docs/CLOSEOUT_SUMMARY_TEMPLATE.md) defines the stable final closeout shape for hosts that use a terminal action such as `task_complete`.

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
| Project directory map | `.github/instructions/project-context.instructions.md` → Project Map |
| Topic → doc routing | `.github/instructions/project-context.instructions.md` → Critical Topic Triggers |
| Build/test commands | `.github/instructions/project-context.instructions.md` → Build and Test Commands |
| Protected paths | `.github/instructions/project-context.instructions.md` → Protected Paths |
| Status-line language | `copilot-instructions.md` → Rule 8 |
| Agent roles/format | `.github/agents/*.agent.md` |
| Strategy-vs-mechanism guidance | `docs/STRATEGY_MECHANISM_LAYERING.md` |
| Concrete role examples | `docs/ROLE_STRATEGY_EXAMPLES.md` |
| Concrete starter role profiles | `examples/reviewer_roles/*.md` |
| Git audit packet defaults | `templates/git_audit_*.template.md` + `scripts/git_audit_pipeline.py` |
| Adoption bootstrap flow | `scripts/bootstrap_adoption.py` |
| Doc-first execution default | `docs/DOC_FIRST_EXECUTION_GUIDELINES.md` + `templates/doc_first_execution_guidelines.template.md` |
| Long-task execution contract | `templates/execution_contract.template.md` |
| SKILL harvest candidate packet | `templates/skill_candidate_packet.template.md` |
| SKILL promotion receipt | `templates/skill_promotion_receipt.template.md` |
| Runtime failure capture | `templates/failure_packet.template.md` |
| Root-cause closeout note | `templates/root_cause_note.template.md` |
| Closeout truth audit | `scripts/closeout_truth_audit.py` |
| Runtime guard registry | `templates/runtime_surface_registry.template.py` + `scripts/runtime_surface_guardrails.py` |
| Optional git hooks | `.githooks/` + `scripts/install_git_hooks.sh` |
| Reviewer / CLI role profiles | `templates/reviewer_role_profile.template.md` |
| Discussion packet defaults | `templates/discussion_packet.template.md` + `scripts/discussion_pipeline.py` |
| Preference drift detection | `scripts/preference_drift_audit.py` |

---

## License

MIT
