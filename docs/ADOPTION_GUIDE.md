# Adoption Guide

Step-by-step guide for adopting this agent framework in a new project.

---

## Prerequisites

- GitHub repository (new or existing)
- A coding assistant that reads `.github/copilot-instructions.md` (GitHub Copilot, Cursor, Augment, etc.)
- Python 3.11+ (to run the bootstrap, audit helper, and validation scripts)
- Bash is optional — `scripts/validate-template.sh` is a thin wrapper that calls `scripts/validate_template.py`; you can run either

---

## Step 1 — Bootstrap Or Copy The Core Files

### Recommended: bootstrap the target repository

Run this from the template repository:

```bash
python3 scripts/bootstrap_adoption.py ../your-repo \
  --project-name "Your Project" \
  --profile standard
```

Optional capability flags:

- `--capability closeout-audit` adds `scripts/closeout_truth_audit.py`
- `--capability runtime-guards` adds the runtime guard runner plus `.github/runtime_surface_registry.py`
- `--capability git-hooks` adds `.githooks/` and `scripts/install_git_hooks.sh`

Profile guide:

- `minimal` keeps only the core rules, state files, and doc index
- `standard` is the recommended default for most repositories and includes CI plus validation tooling
- `full` adds reviewer role examples, strategy docs, and the committed demo project

### Manual alternative

Copy these files into your new repository, preserving their paths:

```
.github/
  copilot-instructions.md          ← operating rules (Rule 0–27)
  RELEASE_TEMPLATE.md              ← release notes starting point
  agents/
    architect.agent.md             ← analysis/planning agent
    implementer.agent.md           ← execution/validation agent
  instructions/
    project-context.instructions.md ← project adapter (fill in Step 2)
    backend.instructions.md        ← backend change protocol
    docs.instructions.md           ← documentation change protocol

docs/
  INDEX.md                         ← TYPE-A doc navigation index
  FRAMEWORK_ARCHITECTURE.md        ← how the layers work (optional, keep for ref)
  ADOPTION_GUIDE.md                ← this file (optional, keep for ref)
  COMPATIBILITY.md                 ← verified surfaces and known limits
  SKILL_HARVEST_LOOP_V1_DRAFT.md   ← formal v1 design draft for post-task SKILL harvest and promotion governance
  SKILL_MECHANISM_V1_DRAFT.md      ← formal v1 design draft for the framework-native SKILL contract
  DEVELOPER_TOOLCHAIN_DESIGN.md    ← formal v1 design draft for the Developer Toolchain surface
  DEVELOPER_TOOLCHAIN_DISCUSSION.md ← discussion history and alternative viewpoints for that surface
  AI_TRACEABILITY_AND_RECOVERY_DISCUSSION.md ← discussion history for AI-era traceability, diagnosis, runtime evidence, and recovery mechanisms
  TRACEABILITY_AND_RECOVERY_V1_DRAFT.md ← formal v1 design draft for user-surface mapping, failure capture, runtime evidence ownership, and root-cause closeout
  LEFTOVER_UNIT_CONTRACT.md        ← how to record truthful partial-work state
  STRATEGY_MECHANISM_LAYERING.md   ← keep if you want formal reviewer or agent role splits
  ROLE_STRATEGY_EXAMPLES.md        ← keep if you want ready-to-adapt role examples for different reviewer families
  RUNTIME_SURFACE_PROTECTION.md    ← keep if your project has active runtime paths to protect
  runbooks/
    multi-model-discussion-loop.md ← recommended for framework choice, plan review, and other open design questions
    resumable-git-audit-pipeline.md ← recommended for external reviewer / multi-CLI workflows
  archive/                         ← empty dir for TYPE-C docs (keep it)

templates/
  discussion_packet.template.md   ← append-only discussion packet for open design questions
  doc_first_execution_guidelines.template.md ← blank doc-first execution policy to apply at the repo level
  execution_contract.template.md   ← pre-execution confirmation contract for long tasks
  skill_candidate_packet.template.md ← candidate packet for post-task SKILL harvest proposals
  skill_promotion_receipt.template.md ← promotion receipt for canonical SKILL mutation decisions
  skill.template.md                ← framework-native SKILL contract template
  failure_packet.template.md       ← progressive runtime failure packet for diagnosis and recovery
  project-context.template.md      ← blank project adapter to fill in
  root_cause_note.template.md      ← closeout note distinguishing cause-suspected from cause-established recovery
  session_state.template.md        ← blank session state to fill in
  roadmap.template.md              ← blank ROADMAP to fill in
  git_audit_task_packet.template.md ← task packet template
  git_audit_receipt.template.md    ← audit receipt template
  git_audit_handoff_packet.template.md ← handoff packet template
  reviewer_role_profile.template.md ← role profile template for external or internal reviewers

examples/
  skills/
    *.md                           ← starter SKILL examples to adapt when your repository formalizes skills
  reviewer_roles/
    *.md                           ← 10 ready-to-adapt starter role profiles

scripts/
  active_docs_audit.py            ← executable active-doc portability and stale-assertion audit
  bootstrap_adoption.py            ← bootstrap and profile-aware adoption helper
  closeout_truth_audit.py          ← executable Rule 25 enforcement for truth-source closeout claims
  discussion_pipeline.py           ← generator for discussion packet creation and append-only feedback/synthesis
  git_audit_pipeline.py            ← generator for packet / receipt / handoff assets
  install_git_hooks.sh             ← activates optional `.githooks/` in the adopter repo
  runtime_surface_guardrails.py    ← registry-driven runtime guard runner
  validate_template.py             ← structured validator used locally and in CI

.githooks/
  pre-commit                       ← optional closeout/runtime guard entrypoint
  pre-push                         ← optional runtime push-check entrypoint

templates/
  runtime_surface_registry.template.py ← runtime surface registry skeleton
```

---

## Step 2 — Fill In the Project Adapter

Open `.github/instructions/project-context.instructions.md` and replace every `[placeholder]`:

| Placeholder | Replace with |
|---|---|
| `[Project Name]` | Your project name |
| Project Map rows | Your actual directory structure |
| Canonical Docs rows | Your actual key docs |
| Critical Topic Triggers | Keywords that matter in your domain |
| Developer Toolchain | Your language, package manager, diagnostics, run, health, repro, and build surfaces |
| Build and Test Commands | Your actual build/test/lint commands |
| Protected Paths | Paths that require explicit confirmation before destructive ops |
| Runtime Config Locations | Where your config files live |

Use `templates/project-context.template.md` as a blank starting point if preferred.

When filling the `Developer Toolchain` section, prefer an honest progressive contract over a fictional complete one.

Required first-pass fields:

1. primary language
2. package manager
3. diagnostics source or command
4. run entrypoint or explicit `none`
5. health or smoke path or explicit `none`
6. repro path for live runtime repositories, otherwise explicit `none`

If the relevant runtime path depends on a build step, also declare `Build`.

Strong recommendation:

record verification status and fallback or stop behavior for each declared surface so the agent can react differently to `declared-unverified`, `verified-working`, and `known-broken` commands.

Also fill the traceability surfaces honestly:

1. `Runtime Evidence` should stay inside `Developer Toolchain` by default and name where logs, health checks, and smoke paths actually live
2. `User Surface Map` should cover the top user-critical flows first; partial truthful coverage is better than a fake complete atlas
3. `Security-Sensitive Surfaces And Escalation` should identify the paths and flows that must trigger stronger failure tracking automatically

If your repository has live runtime paths, also keep and use:

1. `templates/failure_packet.template.md`
2. `templates/root_cause_note.template.md`

These surfaces help future agents distinguish:

1. behavior broken right now
2. cause only suspected
3. cause actually established

The structured validator now provides reminder-level advisories for obviously weak Developer Toolchain sections.

Those advisories are meant to nudge honest completion of the section, not to hard-fail first adoption.

Bootstrap-generated adopters now also carry a manifest-declared `required-core` contract for Developer Toolchain.

That means:

1. the required core must exist and stay structurally valid in newly bootstrapped repos
2. optional enrichment such as `Debug` or `Format` still remains advisory
3. multi-runtime repos may qualify labels with parentheses, for example `Run (frontend)` and `Run (backend)`

If your project will use external Codex, multiple CLI sessions, or explicit reviewer handoff, also keep the `audit|handoff|receipt|packet` trigger mapped to `docs/runbooks/resumable-git-audit-pipeline.md`.

If your project wants framework choice, architecture debates, or plan review to happen in a durable multi-model loop before coding, also keep the `discussion|debate|framework choice|plan review|architecture option` trigger mapped to `docs/runbooks/multi-model-discussion-loop.md`.

If you want doc-first execution to be the repository default for non-trivial work, also add `docs/DOC_FIRST_EXECUTION_GUIDELINES.md` to the canonical docs table and keep the `guideline|guidelines|doc-first|execution checklist|planning mode` trigger mapped to it.

If your project will define multiple reviewer or agent roles with different judgment responsibilities, keep `docs/STRATEGY_MECHANISM_LAYERING.md` and use `templates/reviewer_role_profile.template.md` to formalize them.

When doing so, define the role by judgment boundary first, not by tool name. For example, prefer `runtime correctness reviewer` over `Codex reviewer`, and `maintainability reviewer` over `Claude reviewer`. A CLI, subagent, or custom agent can then be listed as one possible executor of that role.

If you want concrete starting points instead of a blank role profile, keep `docs/ROLE_STRATEGY_EXAMPLES.md` and adapt the examples that fit your repository.

If your repository wants formal SKILL surfaces, keep `docs/SKILL_MECHANISM_V1_DRAFT.md`, `docs/SKILL_HARVEST_LOOP_V1_DRAFT.md`, and `templates/skill.template.md` together. The first draft defines the canonical framework-native contract, the harvest draft defines post-task promotion governance, and the template gives you one concrete file shape to fill in.

If you want examples before inventing your own skill files, adapt the starter files under `examples/skills/`. The current starter set covers one `workflow` skill and one `guardrail` skill.

When you do so, keep the field-level receipt and review matrix intact. It is the mechanism that turns broad "humans approve" guidance into an actual per-field update policy.

If your repository also wants receipt-bearing harvest artifacts rather than inventing them later, keep `templates/skill_candidate_packet.template.md` and `templates/skill_promotion_receipt.template.md` too.

Recommended starting posture if you want the repository to actually improve with repeated use rather than merely carry the files:

1. start with one or two high-frequency skills, not a large initial catalog
2. prefer a `workflow` skill for a repeated execution pattern or a `guardrail` skill for a repeated failure mode
3. keep the `promotion_tier` matrix intact so field authority stays explicit
4. treat closeout receipts, root-cause notes, and repeated failure patterns as candidate evidence
5. do not let raw transcripts mutate canonical skills directly
6. require candidate packets before proposed change and promotion receipts before canonical mutation
7. review trigger overlap aggressively so skill accumulation does not collapse progressive disclosure

This is the key difference between “the repo has SKILL files” and “the repo actually gets better with use”. The framework supports the latter, but only if repositories keep the evidence and promotion boundary explicit.

If you want a ready-made starter pack rather than starting from scratch, keep `examples/reviewer_roles/`. The template ships 10 formal role profiles split into:

1. first batch: goal/acceptance, plan/checkpoint, runtime correctness, boundary/contract, git closeout, maintainability
2. second batch: observability/failure-path, performance/benchmark, migration/compatibility, docs/spec drift

In most repositories, the first batch should be adapted first. The second batch becomes first-class when the codebase starts to need stronger observability, performance discipline, compatibility sequencing, or doc/spec governance.

If your repository is multi-runtime, also inspect `examples/full_stack_project/`.

That example shows how to:

1. declare qualified Developer Toolchain labels for frontend and backend paths
2. keep one manifest-declared required-core contract
3. document a full-stack repro path without pretending the stack has only one runtime entrypoint

---

## Step 3 — Initialize session_state.md

Copy `templates/session_state.template.md` to the project root as `session_state.md`.

Fill in:
- **Current Goal**: one sentence describing what you are working on right now
- **Working Hypothesis**: state the current working assumption (e.g., "The fix requires X" or "The root cause is Y") — even for well-understood tasks, a brief hypothesis anchors the cognitive loop
- **Confidence**: High / Medium / Low
- **Acceptance Criteria**: the observable conditions that mark your first phase complete

Leave everything else blank or with placeholder text until the first subtask is confirmed done.

If the repository wants long-term skill accumulation, this is also the right point to decide whether post-task harvest is in scope from day one.

Practical rule:

1. if the team is still stabilizing basic execution, do not start with automatic harvest expectations
2. once the repo has trustworthy closeout receipts or root-cause notes, begin creating candidate packets for repeated patterns
3. only promote a harvested lesson into canonical SKILL content after it survives the repository's declared promotion path

---

## Step 3A — Confirm The Execution Contract

Before the first long-running task, copy `templates/execution_contract.template.md` into your working notes, issue tracker, or task packet and confirm the execution model once with the user or task owner.

If you want a concrete filled example rather than a blank template, inspect [`examples/demo_project/docs/runbooks/execution_contract_example.md`](../examples/demo_project/docs/runbooks/execution_contract_example.md).

At minimum, confirm:

- whether the default main-thread-agent ownership for normal commit and push should remain in place or be overridden
- whether fan-out to CLI or subagents is expected
- what fallback path applies when an executor fails or stalls
- whether the task runs in autonomous while-loop mode
- what one progress unit is for while-mode work
- what the true closeout boundary is for while-mode work
- what E2E or user-visible validation is required before the task can be reported complete

The template default is that the main-thread agent performs normal commit/push and only exception cases escalate. This confirmation should happen once at task start when a repository wants to change that default, not before every file edit.

Important honesty note: the template ships the contract surface and the demo example, but it does not automatically prove that every future task in your repository instantiated one. If you want execution contracts to be mandatory rather than recommended, add a local checklist, task-packet rule, or validator around that expectation.

Status-line and closeout preference to copy into local policy surfaces when relevant:

- routine in-progress replies use `• 当前在做: ... | 下一步: ...`
- the longer focus-bearing variant is only for ambiguous cases
- final closeout uses exactly one `📍` footer and places `---` immediately before it

---

## Step 4 — Create docs/INDEX.md

Your `docs/INDEX.md` starts with the core docs that exist. For a new project, that might be just:

```markdown
| Document | Description |
|---|---|
| `README.md` | Project entry point |
| `docs/DEVELOPER_TOOLCHAIN_DESIGN.md` | Formal v1 design draft for the agent-facing Developer Toolchain surface |
| `docs/DEVELOPER_TOOLCHAIN_DISCUSSION.md` | Discussion history and alternative viewpoints for that surface |
| `docs/AI_TRACEABILITY_AND_RECOVERY_DISCUSSION.md` | Discussion history for AI-era traceability, diagnosis, runtime evidence, and recovery mechanisms |
| `docs/TRACEABILITY_AND_RECOVERY_V1_DRAFT.md` | Formal v1 design draft for user-surface mapping, failure capture, runtime evidence ownership, and root-cause closeout |
| `docs/DOC_FIRST_EXECUTION_GUIDELINES.md` | Repository-default doc-first planning rule and required planning surfaces |
| `docs/FRAMEWORK_ARCHITECTURE.md` | Agent framework layer design |
| `docs/ADOPTION_GUIDE.md` | How to adopt this framework |
| `docs/STRATEGY_MECHANISM_LAYERING.md` | How to split role strategy from reusable workflow mechanism |
| `docs/ROLE_STRATEGY_EXAMPLES.md` | Concrete reviewer and agent role examples to adapt |
| `docs/runbooks/multi-model-discussion-loop.md` | Append-only discussion workflow for framework choice, plan review, and other open design questions |
| `docs/runbooks/resumable-git-audit-pipeline.md` | Packet / receipt / handoff workflow for resumable Git audit |
```

Update this index every time you add or remove a TYPE-A document.

---

## Step 5 — Verify docs/archive/ Exists

The `docs/archive/` directory ships with the template (it contains a `.gitkeep`). Confirm it is present after copying:

```bash
ls docs/archive/
```

If it is missing (e.g., some copy tools skip empty-ish directories), recreate it:

```bash
mkdir -p docs/archive
touch docs/archive/.gitkeep
```

All TYPE-C documents (phase reports, one-time analyses, summaries) go here.

---

## Step 6 — Initialize ROADMAP.md

Copy `templates/roadmap.template.md` to the project root as `ROADMAP.md`.

Fill in:
- **Phase 1 name and goal**: one sentence describing what the first phase achieves
- **Initial subtasks**: the work items you know about right now
- **Acceptance criteria**: observable conditions that mark Phase 1 complete

Rules 9 and 10 both write to `ROADMAP.md` (updating rows to `✅ YYYY-MM-DD`), so this file must exist before the agent starts work.

---

## Step 6A — Initialize Doc-First Execution Guidelines

If you want non-trivial work to default to roadmap/design first, checklist second, implementation third, copy `templates/doc_first_execution_guidelines.template.md` to `docs/DOC_FIRST_EXECUTION_GUIDELINES.md`.

Customize these local references:

- active roadmap or design doc path
- execution checklist path
- validation doc path
- state-tracking doc path

Then make the rule visible in three places:

1. the repository's main instruction or policy surface
2. `.github/instructions/project-context.instructions.md`
3. the main entry README or module README that future sessions will read first

This makes doc-first execution a repository default rather than a conversational preference.

---

## Step 7 — Customize Rule 8 Status Line Language (Optional)

The default in-progress status line in `copilot-instructions.md` uses English. If your team works in another language, update the Rule 8 examples accordingly.

---

## Step 8 — Remove What You Don't Need

The following files are optional and can be removed for simpler projects:

| File | Remove if... |
|---|---|
| `.github/agents/architect.agent.md` | You don't use separate analysis agents |
| `.github/agents/implementer.agent.md` | Same as above |
| `.github/instructions/backend.instructions.md` | Not a backend project |
| `.github/instructions/docs.instructions.md` | Documentation is minimal |
| `docs/FRAMEWORK_ARCHITECTURE.md` | Team is familiar with the framework |
| `docs/STRATEGY_MECHANISM_LAYERING.md` | You do not need formal reviewer or agent role splits |
| `docs/ROLE_STRATEGY_EXAMPLES.md` | You do not need example reviewer families because you already have your own role model |
| `examples/reviewer_roles/` | You want the role examples as guidance only and do not need concrete starter files |
| `docs/runbooks/resumable-git-audit-pipeline.md` | No external reviewer, multi-CLI, or resumable handoff workflow is needed |
| `templates/git_audit_*.template.md` + `scripts/git_audit_pipeline.py` | Same as above |
| `docs/runbooks/multi-model-discussion-loop.md` | Open design questions do not need a durable multi-round discussion workflow |
| `templates/discussion_packet.template.md` + `scripts/discussion_pipeline.py` | Same as above |
| `templates/skill_candidate_packet.template.md` + `templates/skill_promotion_receipt.template.md` | You want post-task SKILL harvest artifacts without inventing the packet/receipt shape yourself |
| `templates/reviewer_role_profile.template.md` | Same as above |
| `templates/` | All templates have been applied |

---

## Minimal Viable Setup

If you want the smallest possible setup:

```
.github/
  copilot-instructions.md          ← keep (core rules)
  project-context.instructions.md  ← keep (fill in)

docs/
  INDEX.md                         ← keep (update as docs grow)
  DOC_FIRST_EXECUTION_GUIDELINES.md ← create from templates/doc_first_execution_guidelines.template.md if doc-first is your default
  archive/                         ← keep (ships empty)

session_state.md                   ← create from templates/session_state.template.md
ROADMAP.md                         ← create from templates/roadmap.template.md
```

Everything else is additive.

After setup, run the structured validator from the repo root to confirm no required files are missing:

```bash
python3 scripts/validate_template.py
# or equivalently: bash scripts/validate-template.sh  (thin wrapper for the above)
```

If you want to inspect the bootstrap plan before writing files, use:

```bash
python3 scripts/bootstrap_adoption.py ../your-repo \
  --project-name "Your Project" \
  --profile standard \
  --capability closeout-audit \
  --capability runtime-guards \
  --dry-run
```

If you opt into hooks, activate them after bootstrap:

```bash
bash scripts/install_git_hooks.sh
```

If you keep the resumable audit workflow, do a smoke run once:

```bash
python3 scripts/git_audit_pipeline.py init-task \
  --task-id "template-smoke" \
  --goal "Verify packet generation" \
  --truth-sources "- docs/runbooks/resumable-git-audit-pipeline.md" \
  --allowed-files "- docs/**" \
  --do-not-touch "- .env" \
  --validation "- bash scripts/validate-template.sh" \
  --acceptance-boundary "- task packet exists"
```

If you keep the multi-model discussion workflow, do a smoke run once:

```bash
python3 scripts/discussion_pipeline.py init-topic \
  --topic-id "discussion-smoke" \
  --decision-question "Should this repo require discussion packets before framework changes?" \
  --why-now "- We want to verify that the packet generator works." \
  --current-truth "- The repo already supports doc-first execution." \
  --constraints "- Keep the workflow lightweight." \
  --candidate-directions "- Always require it for open design questions\n- Keep it optional" \
  --evaluation-criteria "- Clarity\n- overhead\n- recoverability" \
  --suggested-executors "- codex\n- claude-code\n- internal-subagent"
```

---

## Next Upgrade Paths

Start with the smallest shape that matches your team today, then grow into the heavier workflow only when you need it.

| Starting point | Add next when you need... |
|---|---|
| `minimal` profile | cross-session state, stronger docs routing, and a repeatable bootstrap path |
| `standard` profile | reviewer specialization, committed demo patterns, and CI-enforced integrity |
| `full` profile | domain-specific role governance, packet-heavy audits, and internal operating standardization |

If you are unsure, begin with `standard`. It gives the best balance of real guardrails without the full reviewer-role surface area.

---

## Ongoing Maintenance

| Trigger | Action |
|---|---|
| New TYPE-A doc added | Update `docs/INDEX.md` |
| Phase complete | Archive to `docs/archive/`, rotate `session_state.md`, mark ROADMAP |
| Protected path changes | Update `project-context.instructions.md` |
| New topic trigger needed | Add row to Critical Topic Triggers in adapter |
| `session_state.md` exceeds ~100 lines | Archive old phase content; keep current phase + insights |

---

## Troubleshooting

**Agent ignores the rules**: confirm `.github/copilot-instructions.md` is being loaded by your AI assistant. Some tools require explicit activation.

**Agent doesn't load the right doc**: check the Critical Topic Triggers in your project adapter — ensure the keyword matches what appears in typical user messages.

**session_state.md is out of sync**: treat the actual code as truth; update session_state.md to match, not the other way around.

**Validation fails with missing checks**: re-run `python3 scripts/validate_template.py` after copying the latest `copilot-instructions.md` and `scripts/` from this template repository. `validate-template.sh` is a bash wrapper for the same command.
