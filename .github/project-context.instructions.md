---
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
| `docs/COMPATIBILITY.md` | Verified surfaces, intended integrations, and known limits |
| `templates/execution_contract.template.md` | Pre-execution confirmation contract for long-running tasks |
| `docs/RUNTIME_SURFACE_PROTECTION.md` | Guard-registry pattern for protecting active user-facing runtime paths |
| `docs/LEFTOVER_UNIT_CONTRACT.md` | How to classify, defer, and recover partial work truthfully |
| `docs/STRATEGY_MECHANISM_LAYERING.md` | How to separate role strategy from reusable workflow mechanisms |
| `docs/ROLE_STRATEGY_EXAMPLES.md` | Concrete reviewer and agent role examples that repositories can adapt |
| `examples/reviewer_roles/` | Ready-to-adapt starter set of first-batch and second-batch role profiles |
| `CHANGELOG.md` | Release boundary and notable changes by version |
| `VERSION` | Current framework version |
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
| `compatibility\|supported tool\|verified\|known limits` | `docs/COMPATIBILITY.md` |
| `execution contract\|task confirmation\|long task\|while loop\|autonomous mode\|commit push policy` | `templates/execution_contract.template.md` |
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
| End-to-end | bootstrap smoke run | `python3 scripts/bootstrap_adoption.py /tmp/agent-framework-template-smoke --project-name "Smoke" --profile standard --project-type cli-tool --dry-run` |

```bash
# Run full suite (all tiers in sequence)
python3 scripts/validate_template.py \
  && python3 -m pytest tests/ -q \
  && python3 scripts/bootstrap_adoption.py /tmp/agent-framework-template-smoke --project-name "Smoke" --profile standard --project-type cli-tool --dry-run
```

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
python3 scripts/bootstrap_adoption.py /tmp/agent-framework-template-smoke --project-name "Smoke" --profile minimal --project-type cli-tool --dry-run
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
