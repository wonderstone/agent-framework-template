---
name: "Template Project Context Adapter"
applyTo: "**"
description: >
  agent-framework-template repository adapter. Provides the project map,
  canonical docs, critical topic triggers, validation toolchain, protected paths,
  build/test commands, and release-control locations for this repository.
---

# agent-framework-template — Project Context

## Project Map

| Path | Purpose |
|---|---|
| `.github/` | Operating rules, repo adapter, agents, instruction packs, and workflows |
| `docs/` | TYPE-A framework architecture, adoption, compatibility, and runbook docs |
| `examples/` | Demo adopted repository plus starter reviewer-role profiles |
| `scripts/` | Bootstrap, validation, and audit tooling shipped by the template |
| `templates/` | Files rendered or copied into adopter repositories |
| `tests/` | Regression tests for bootstrap, validation, and audit workflows |
| `tmp/` | Scratch area for local experiments; not a canonical source of truth |
| `session_state.md` | Cross-session state for this repository's active work |
| `ROADMAP.md` | Repo-level phase and closeout targets |

## Canonical Docs

| Doc | Purpose |
|---|---|
| `README.md` | Project entry point |
| `docs/FRAMEWORK_ARCHITECTURE.md` | Agent framework layer design |
| `docs/ADOPTION_GUIDE.md` | Step-by-step adoption guide |
| `docs/DEVELOPER_TOOLCHAIN_DESIGN.md` | Formal v1 design draft for the agent-facing Developer Toolchain surface |
| `docs/DEVELOPER_TOOLCHAIN_DISCUSSION.md` | Discussion surface for how repositories should expose diagnostics, lint, build, run, and debug tooling to agents |
| `docs/TRACEABILITY_AND_RECOVERY_V1_DRAFT.md` | Formal v1 design draft for user-surface mapping, progressive failure capture, runtime evidence ownership, and root-cause closeout |
| `docs/AI_TRACEABILITY_AND_RECOVERY_DISCUSSION.md` | Discussion history and alternative viewpoints for AI-era traceability and recovery surfaces |
| `docs/DOC_FIRST_EXECUTION_GUIDELINES.md` | Repository-default doc-first planning rule and the reusable surfaces adopters should inherit |
| `docs/CLOSEOUT_SUMMARY_TEMPLATE.md` | Default final closeout-summary shape for hosts with terminal completion actions |
| `docs/PROGRESS_UPDATE_TEMPLATE.md` | Default in-progress update shape for long-running or while-style tasks |
| `docs/COMPATIBILITY.md` | Verified surfaces, intended integrations, and known limits |
| `templates/execution_contract.template.md` | Pre-execution confirmation contract for long-running tasks |
| `templates/discussion_packet.template.md` | Append-only packet template for multi-model discussion loops |
| `docs/RUNTIME_SURFACE_PROTECTION.md` | Guard-registry pattern for protecting active user-facing runtime paths |
| `docs/LEFTOVER_UNIT_CONTRACT.md` | How to classify, defer, and recover partial work truthfully |
| `docs/STRATEGY_MECHANISM_LAYERING.md` | How to separate role strategy from reusable workflow mechanisms |
| `docs/ROLE_STRATEGY_EXAMPLES.md` | Concrete reviewer and agent role examples that repositories can adapt |
| `examples/reviewer_roles/` | Ready-to-adapt starter set of first-batch and second-batch role profiles |
| `CHANGELOG.md` | Release boundary and notable changes by version |
| `VERSION` | Current framework version |
| `docs/runbooks/multi-model-discussion-loop.md` | Append-only discussion workflow for framework choice, plan review, and other open design questions |
| `docs/runbooks/resumable-git-audit-pipeline.md` | Packet / receipt / handoff workflow for resumable audit and Git closeout |
| `docs/INDEX.md` | Navigation index for all TYPE-A docs |
| `session_state.md` | Cross-session state (current goal, decisions, insights) |
| `ROADMAP.md` | Current phase plan and observable acceptance targets |

## Task Recovery Sequence

When resuming a multi-step task, recover context in this order:

1. Read this file
2. Read `docs/INDEX.md`
3. Read the canonical doc for the active topic (see triggers below)
4. Read the actual code/config files to be touched
5. If cross-session: read `session_state.md`

## Critical Topic Triggers

| Trigger keywords | Canonical doc |
|---|---|
| `architecture\|design\|layers\|service boundary` | `docs/FRAMEWORK_ARCHITECTURE.md` |
| `adoption\|setup\|onboard\|quick.start` | `docs/ADOPTION_GUIDE.md` |
| `developer toolchain design\|toolchain design\|verification status\|repro path\|scope tag` | `docs/DEVELOPER_TOOLCHAIN_DESIGN.md` |
| `language tool\|developer toolchain\|diagnostic\|diagnostics\|lint\|build\|run\|debug` | `docs/DEVELOPER_TOOLCHAIN_DISCUSSION.md` |
| `traceability\|recovery\|root cause\|incident\|failure packet\|runtime evidence\|user surface map\|security escalation` | `docs/TRACEABILITY_AND_RECOVERY_V1_DRAFT.md` |
| `ai traceability\|traceability discussion\|recovery discussion\|incident discussion` | `docs/AI_TRACEABILITY_AND_RECOVERY_DISCUSSION.md` |
| `guideline\|guidelines\|doc-first\|execution checklist\|planning mode` | `docs/DOC_FIRST_EXECUTION_GUIDELINES.md` |
| `compatibility\|supported tool\|verified\|known limits` | `docs/COMPATIBILITY.md` |
| `execution contract\|task confirmation\|long task\|while loop\|autonomous mode\|commit push policy` | `templates/execution_contract.template.md` |
| `discussion\|debate\|framework choice\|plan review\|architecture option\|second round` | `docs/runbooks/multi-model-discussion-loop.md` |
| `runtime surface\|placeholder\|mock path\|banned phrase\|live smoke` | `docs/RUNTIME_SURFACE_PROTECTION.md` |
| `leftover\|partial work\|slice classification\|scope entry` | `docs/LEFTOVER_UNIT_CONTRACT.md` |
| `release\|version\|changelog\|upgrade notes` | `CHANGELOG.md` |
| `strategy\|mechanism\|review role\|reviewer split\|codex\|claude` | `docs/STRATEGY_MECHANISM_LAYERING.md` |
| `role example\|review example\|role profile\|starter role\|runtime reviewer\|maintainability reviewer\|git reviewer\|performance reviewer` | `docs/ROLE_STRATEGY_EXAMPLES.md` |
| `audit\|handoff\|receipt\|packet\|reviewer\|git closeout` | `docs/runbooks/resumable-git-audit-pipeline.md` |
| `roadmap\|phase\|milestone\|current focus\|next phase` | `ROADMAP.md` |
| `e2e\|toolchain\|acceptance criteria\|end-to-end` | Validation Toolchain section (this file) |
| `flags\|config\|default values\|runtime override` | → check Runtime Config Locations |
| `policy audit\|framework check\|framework health\|规则检查` | Rule 27 in `.github/copilot-instructions.md` |

## Validation Toolchain

Project type: library

| Tier | Tool | Command |
|---|---|---|
| Unit | pytest | `python3 -m pytest tests/ -q` |
| Integration | structured validator | `python3 scripts/validate_template.py` |
| End-to-end | bootstrap smoke run | `python3 scripts/bootstrap_adoption.py "${TMPDIR:-/tmp}/agent-framework-template-smoke" --project-name "Smoke" --profile standard --project-type cli-tool --dry-run` |

```bash
# Run full suite (all tiers in sequence)
python3 scripts/validate_template.py \
  && python3 -m pytest tests/ -q \
  && python3 scripts/bootstrap_adoption.py "${TMPDIR:-/tmp}/agent-framework-template-smoke" --project-name "Smoke" --profile standard --project-type cli-tool --dry-run
```

## Developer Toolchain

Primary language: Python

Package manager: pip

| Surface | Command or source | Scope | Status | Fallback or stop | Notes |
|---|---|---|---|---|---|
| Diagnostics | `python3 -m compileall scripts tests examples/demo_project/src` | `module` | `verified-working` | Stop after compile blockers are cleared unless broader proof is required | Fast syntax and import diagnostics for shipped Python surfaces |
| Run | `none` | `service` | `not-applicable` | Stop at build, validation, or smoke because this repo does not ship a single live app runtime | Framework repository rather than an application runtime |
| Health or smoke | `python3 scripts/bootstrap_adoption.py "${TMPDIR:-/tmp}/agent-framework-template-smoke" --project-name "Smoke" --profile standard --project-type cli-tool --dry-run` | `module` | `verified-working` | Stop and report if bootstrap smoke cannot run honestly | Fastest runtime-adjacent smoke path for shipped adopter tooling |
| Repro path | `none` | `full-stack` | `not-applicable` | Stop after smoke because the repository does not expose a single end-user runtime path | User-visible proof lives in validation and bootstrap smoke surfaces |
| Build | `python3 -m compileall scripts tests examples/demo_project/src` | `module` | `verified-working` | Stop after build blockers are cleared when smoke is unnecessary | Required before broader smoke when syntax is in question |
| Lint | `python3 scripts/validate_template.py` | `file` | `verified-working` | Stop after lint when task scope is local and runnable proof is unnecessary | Structured repository integrity check |

### Runtime Evidence

| Evidence surface | Applies to | Priority | Status | Fallback or stop | Notes |
|---|---|---|---|---|---|
| Logs | `bootstrap smoke / validator workflows` | `first` | `verified-working` | Fall back to command stderr or stop and report missing runtime evidence | Most runtime-adjacent evidence in this repository comes from script output rather than a long-lived log sink |
| Health check | `bootstrap smoke` | `first` | `verified-working` | Stop and report if smoke cannot run honestly | `python3 scripts/bootstrap_adoption.py "${TMPDIR:-/tmp}/agent-framework-template-smoke" --project-name "Smoke" --profile standard --project-type cli-tool --dry-run` |
| Smoke path | `template bootstrap path` | `first` | `verified-working` | Stop after smoke when the repository does not expose a single app runtime | Fastest trustworthy runtime-adjacent proof for this template repo |

## User Surface Map

| Surface name | Owner path | Sensitive | Fastest repro path | Primary evidence source | Notes |
|---|---|---|---|---|---|
| `template bootstrap flow` | `scripts/bootstrap_adoption.py` | `no` | `python3 scripts/bootstrap_adoption.py "${TMPDIR:-/tmp}/agent-framework-template-smoke" --project-name "Smoke" --profile standard --project-type cli-tool --dry-run` | `Health check` | Primary user-visible workflow for adopters validating setup |
| `template validation flow` | `scripts/validate_template.py` | `no` | `python3 scripts/validate_template.py` | `Logs` | Main integrity surface for template structure and shipped assets |
| `framework governance surfaces` | `.github/` and `templates/` | `yes` | `python3 scripts/validate_template.py` plus focused doc review | `Logs` | Sensitive because changes affect future adopted repositories and enforcement behavior |

## Security-Sensitive Surfaces And Escalation

Sensitive path declarations:

| Path or surface | Why sensitive |
|---|---|
| `.github/copilot-instructions.md` | Framework governance and agent behavior boundary |
| `.github/instructions/project-context.instructions.md` | Repository truth source for future sessions |
| `templates/` | Shipped adopter-facing contract surface |
| `scripts/bootstrap_adoption.py` | Controls what adopters inherit |

Escalation rule:

1. automatically escalate failure tracking when an impacted user surface is marked `Sensitive = yes`
2. automatically escalate when a failure touches a declared sensitive path, config surface, secret surface, or trust-boundary surface
3. after escalation, require the failure artifact to record:
   impacted trust boundary, relevant config or secret surface, and at least one negative-path or misuse-path validation claim
4. human classification may upgrade severity further, but should not be the only trigger

## Build and Test Commands

```bash
# Type check
python3 -m compileall scripts tests examples/demo_project/src

# Run tests
python3 -m pytest tests/ -q

# Lint
python3 scripts/validate_template.py

# Build (if applicable)
python3 -m compileall scripts tests examples/demo_project/src

# Smoke run
python3 scripts/bootstrap_adoption.py "${TMPDIR:-/tmp}/agent-framework-template-smoke" --project-name "Smoke" --profile standard --project-type cli-tool --dry-run
```

## Protected Paths

| Path | Why protected |
|---|---|
| `session_state.md` | Active cross-session source of truth for ongoing work |
| `examples/demo_project/tmp/git_audit/` | Committed audit history used to demonstrate resumable review recovery |
| `.github/copilot-instructions.md` | Top-level framework rules; changes affect every adoption flow |

## Runtime Config Locations

| Location | What it controls |
|---|---|
| `VERSION` | Current framework release number |
| `CHANGELOG.md` | Version boundary and release notes scope |
| `.github/workflows/ci.yml` | Supported Python matrix and required CI validation steps |
| `scripts/bootstrap_adoption.py` | Bootstrap profiles, project-type presets, and copied asset surface |
| `scripts/validate_template.py` | Structural integrity rules for the repository |

## Dangerous Operations Policy

- `session_state.md` → revise deliberately when goals, hypotheses, or active work change
- `examples/demo_project/tmp/git_audit/` → preserve audit trace semantics; do not rewrite casually
- `.github/copilot-instructions.md` → treat as a public governance surface; validate docs and tests after edits

## Notes

- Use `python3` consistently in local commands to match CI and the current macOS environment.
- Keep bootstrap smoke commands in `--dry-run` mode unless intentionally testing write behavior into a disposable target.
- This template now treats executable doc-first planning as a first-class reusable surface: the source repo documents it locally, and the shipped templates let adopters turn it into their repository default for non-trivial work.
- The reusable adopter asset for that policy is `templates/doc_first_execution_guidelines.template.md`; repositories that want doc-first mode by default should copy it into `docs/DOC_FIRST_EXECUTION_GUIDELINES.md` and route future sessions to it through their project adapter.
- The discussion-loop mechanism is intentionally executor-agnostic: local repositories may standardize machine-local commands for Claude Code, Codex, Gemini, Copilot, or custom agents, but this template only standardizes the packet and synthesis workflow.
