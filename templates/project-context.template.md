---
name: "Project Context Adapter"
applyTo: "**"
description: >
  [Project Name] project adapter. Provides the project map, critical topic triggers,
  protected paths, build/test commands, and runtime config locations. Always read
  this file before starting any multi-step task or when a critical keyword appears.
---

# [Project Name] — Project Context

## Project Map

| Path | Purpose |
|---|---|
| `src/` | [Main application source — describe here] |
| `docs/` | Architecture, deployment, and system docs |
| `tests/` | Test suites |
| `data/` | [Runtime state / user data — if applicable] |
| `.github/` | Agent behavior rules and project adapter |

## Canonical Docs

| Doc | Purpose |
|---|---|
| `README.md` | Project entry point |
| `docs/SKILL_HARVEST_LOOP_V1_DRAFT.md` | [Formal v1 design draft for post-task SKILL harvest and per-field promotion governance — keep if useful] |
| `docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md` | [Formal v1 design draft for runtime invocation evidence, bounded candidate triggers, and typed skill evolution lineage — keep if useful] |
| `docs/SKILL_MECHANISM_V1_DRAFT.md` | [Formal v1 design draft for a framework-native SKILL contract, evidence gates, and honest degradation — keep if useful] |
| `docs/DEVELOPER_TOOLCHAIN_DESIGN.md` | [Formal v1 design draft for the agent-facing Developer Toolchain surface — keep if useful] |
| `docs/DEVELOPER_TOOLCHAIN_DISCUSSION.md` | [Discussion history and alternative viewpoints for Developer Toolchain — keep if useful] |
| `docs/TRACEABILITY_AND_RECOVERY_V1_DRAFT.md` | [Formal v1 design draft for user-surface mapping, failure capture, runtime evidence ownership, and root-cause closeout — keep if useful] |
| `docs/AI_TRACEABILITY_AND_RECOVERY_DISCUSSION.md` | [Discussion history and alternative viewpoints for AI-era traceability and recovery — keep if useful] |
| `docs/ANTI_DRIFT_RULE_REFACTOR_PLAN_V1.md` | [Mechanism-first plan for checkpoint, sync-audit, repair, and rule rebase work — keep if useful] |
| `docs/DOC_FIRST_EXECUTION_GUIDELINES.md` | [Repository-default doc-first planning rule and required planning surfaces] |
| `ARCHITECTURE.md` | [System architecture — create if needed] |
| `ROADMAP.md` | Phase planning and acceptance targets |
| `session_state.md` | Cross-session state |
| `docs/INDEX.md` | TYPE-A doc navigation index |
| `docs/COMPATIBILITY.md` | [Verified tooling surface and known limits — create if useful] |
| `templates/execution_contract.template.md` | [Pre-execution confirmation contract for long tasks] |
| `templates/execution_progress_receipt.template.md` | [Checkpoint-bearing progress receipt for long-running tasks — keep if useful] |
| `templates/drift_reconciliation_packet.template.md` | [Drift packet template for execution-state reconciliation — keep if useful] |
| `templates/discussion_packet.template.md` | [Append-only packet template for multi-model discussion loops — keep if useful] |
| `templates/skill_invocation_receipt.template.md` | [Invocation receipt template for runtime skill evidence and typed evolution lineage — keep if useful] |
| `templates/skill_candidate_packet.template.md` | [Candidate packet template for post-task SKILL harvest — keep if useful] |
| `templates/skill_promotion_receipt.template.md` | [Promotion receipt template for canonical SKILL mutation decisions — keep if useful] |
| `templates/skill.template.md` | [Framework-native SKILL contract template — keep if your repository wants formal skill surfaces] |
| `docs/RUNTIME_SURFACE_PROTECTION.md` | [Guard-registry pattern for active user-facing runtime paths — create if useful] |
| `docs/LEFTOVER_UNIT_CONTRACT.md` | [How your team records and recovers partial work — create if useful] |
| `docs/STRATEGY_MECHANISM_LAYERING.md` | How to separate role strategy from workflow mechanism |
| `docs/runbooks/multi-model-discussion-loop.md` | Append-only discussion workflow for framework choice, plan review, and other open design questions |
| `docs/runbooks/resumable-git-audit-pipeline.md` | Packet / receipt / handoff workflow for resumable audit and Git closeout |
| `docs/runbooks/state-reconciliation.md` | Drift-packet workflow for reconciling `session_state.md`, `ROADMAP.md`, and task artifacts before closeout |

## Task Recovery Sequence

1. Read this file
2. Read `docs/INDEX.md`
3. Read the canonical doc for the active topic (see triggers below)
4. Read the actual code/config files to be touched
5. If cross-session: read `session_state.md`

## Critical Topic Triggers

<!-- Add rows matching your project's topic surface -->
<!-- Pattern: keyword (partial match is fine) → doc to load -->

| Trigger keywords | Canonical doc |
|---|---|
| `network\|port\|proxy\|connectivity` | `docs/NETWORK_GUIDE.md` |
| `architecture\|design\|service boundary` | `ARCHITECTURE.md` |
| `skill\|skills\|skill design\|skill mechanism\|triggerability\|progressive disclosure\|guardrail skill` | `docs/SKILL_MECHANISM_V1_DRAFT.md` |
| `skill harvest\|promotion tier\|promotion authority\|candidate packet\|promotion receipt` | `docs/SKILL_HARVEST_LOOP_V1_DRAFT.md` |
| `skill execution\|invocation receipt\|evolution mode\|fix\|derived\|captured` | `docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md` |
| `developer toolchain design\|toolchain design\|verification status\|repro path\|scope tag` | `docs/DEVELOPER_TOOLCHAIN_DESIGN.md` |
| `language tool\|developer toolchain\|diagnostic\|diagnostics\|lint\|build\|run\|debug` | `docs/DEVELOPER_TOOLCHAIN_DISCUSSION.md` |
| `traceability\|recovery\|root cause\|incident\|failure packet\|runtime evidence\|user surface map\|security escalation` | `docs/TRACEABILITY_AND_RECOVERY_V1_DRAFT.md` |
| `ai traceability\|traceability discussion\|recovery discussion\|incident discussion` | `docs/AI_TRACEABILITY_AND_RECOVERY_DISCUSSION.md` |
| `guideline\|guidelines\|doc-first\|execution checklist\|planning mode` | `docs/DOC_FIRST_EXECUTION_GUIDELINES.md` |
| `compatibility\|supported tool\|verified\|known limits` | `docs/COMPATIBILITY.md` |
| `execution contract\|task confirmation\|long task\|while loop\|autonomous mode\|commit push policy` | `templates/execution_contract.template.md` |
| `discussion\|debate\|framework choice\|plan review\|architecture option\|second round` | `docs/runbooks/multi-model-discussion-loop.md` |
| `checkpoint\|state sync\|drift\|reconciliation\|progress receipt` | `docs/runbooks/state-reconciliation.md` |
| `runtime surface\|placeholder\|mock path\|banned phrase\|live smoke` | `docs/RUNTIME_SURFACE_PROTECTION.md` |
| `leftover\|partial work\|slice classification\|scope entry` | `docs/LEFTOVER_UNIT_CONTRACT.md` |
| `strategy\|mechanism\|review role\|reviewer split\|codex\|claude` | `docs/STRATEGY_MECHANISM_LAYERING.md` |
| `audit\|handoff\|receipt\|packet\|reviewer\|git closeout` | `docs/runbooks/resumable-git-audit-pipeline.md` |
| `roadmap\|phase\|milestone` | `ROADMAP.md` |
| `e2e\|toolchain\|acceptance criteria\|end-to-end` | Validation Toolchain section (this file) |
| `[your topic]` | `[your doc path]` |

## Validation Toolchain

<!-- Required by Rule 23. Fill before any feature work begins.            -->
<!-- Project type: web-frontend / backend-api / cli-tool / library / full-stack -->

Project type: [fill in]

| Tier | Tool | Command |
|---|---|---|
| Unit | [pytest / Jest / Vitest / etc.] | `[command]` |
| Integration | [httpx / supertest / React Testing Library / etc.] | `[command]` |
| End-to-end | [Playwright / Cypress / Newman / curl script / etc.] | `[command]` |

```bash
# Run full suite (all tiers in sequence)
# [single command or script]
```

<!-- If any tier is missing, declare a toolchain setup task before feature work. -->

## Developer Toolchain

<!-- Progressive contract. Use explicit `none` when a surface does not exist. -->
<!-- Qualify the surface label with parentheses when multiple runtimes exist, e.g. `Run (frontend)` and `Run (backend)`. -->

Primary language: [fill in]

Package manager: [fill in]

| Surface | Command or source | Scope | Status | Fallback or stop | Notes |
|---|---|---|---|---|---|
| Diagnostics | [command or source] | [file / module] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [syntax or type diagnostics] |
| Run | [command or `none`] | [service / full-stack] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [main local execution path] |
| Health or smoke | [command or `none`] | [service / full-stack] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [fastest reliable runtime confirmation] |
| Repro path | [command, script, or `none`] | [service / full-stack] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [required for repos with a live runtime path] |
| Build | [command or `none`] | [module / service] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [required when the runtime path depends on build] |
| Lint | [command or `none`] | [file / module] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [recommended] |

Default policy:

1. climb only as far as the task scope and user-visible acceptance target require
2. treat `declared-unverified` as recoverable, not trustworthy by default
3. never leave `known-broken` without either a fallback path or an explicit stop rule

### Runtime Evidence

<!-- Keep this as the single source of truth for normal repositories. -->
<!-- Promote to a dedicated doc only when one section can no longer tell the agent where to look first. -->

| Evidence surface | Applies to | Priority | Status | Fallback or stop | Notes |
|---|---|---|---|---|---|
| Logs | [surface / service / `none`] | [first / second / fallback] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [log path, command, or viewer] |
| Health check | [surface / service / `none`] | [first / second / fallback] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [endpoint, script, or command] |
| Smoke path | [surface / service / `none`] | [first / second / fallback] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [fastest runtime-adjacent confirmation] |
| [Optional additional evidence] | [surface / service] | [priority] | [status] | [fallback or stop] | [trace / metric / screenshot harness / inspection command] |

## User Surface Map

<!-- This is a decision surface, not a full architecture atlas. -->
<!-- Cover the top user-critical flows first. Use explicit `none` when the repository has no live runtime path. -->

| Surface name | Owner path | Sensitive | Fastest repro path | Primary evidence source | Notes |
|---|---|---|---|---|---|
| [surface] | [path / module / entrypoint / `none`] | [yes / no] | [command / script / route / `none`] | [logs / health / smoke / trace / user report / `none`] | [optional short context] |
| [surface] | [path / module / entrypoint / `none`] | [yes / no] | [command / script / route / `none`] | [logs / health / smoke / trace / user report / `none`] | [optional short context] |

## Security-Sensitive Surfaces And Escalation

<!-- Keep this near the user-surface map so automatic escalation can evaluate against a durable source. -->

Sensitive path declarations:

| Path or surface | Why sensitive |
|---|---|
| `[path / config / flow]` | [auth / secrets / billing / export / model routing / external tool / prompt boundary] |

Escalation rule:

1. automatically escalate failure tracking when an impacted user surface is marked `Sensitive = yes`
2. automatically escalate when a failure touches a declared sensitive path, config surface, secret surface, or trust-boundary surface
3. after escalation, require the failure artifact to record:
   impacted trust boundary, relevant config or secret surface, and at least one negative-path or misuse-path validation claim
4. human classification may upgrade severity further, but should not be the only trigger

## Build and Test Commands

```bash
# Replace with actual project commands

# Type check
# pyright .

# Run tests
# pytest tests/

# Lint
# ruff check .

# Build
# npm run build

# Start
# ./scripts/start.sh
```

## Protected Paths

<!-- Explicit user confirmation required before: delete, clear, overwrite, replace -->

| Path | Why protected |
|---|---|
| `data/` | Runtime state — irreversible if deleted |
| `.env` | Secrets — append preferred over overwrite |
| `[add more]` | [reason] |

## Runtime Config Locations

| Location | What it controls |
|---|---|
| `.env` | Environment-level overrides |
| `[config file path]` | [what it controls] |

## Dangerous Operations Policy

- `data/` → explicit confirmation required before any destructive operation
- `.env` → do not overwrite wholesale
- [Add project-specific entries]

## Notes

<!-- Add environment-specific notes: venv activation, service pre-checks, etc. -->
<!-- If your repository adopts doc-first execution as the default, say so explicitly here so future sessions do not treat it as optional. -->
<!-- If your repository standardizes machine-local discussion executors such as Claude Code, Codex, Gemini, Copilot, or custom agents, record those commands in this file or in a nearby runbook instead of relying on chat memory. -->
<!-- If your repository has live runtime paths, point future sessions to `templates/failure_packet.template.md` and `templates/root_cause_note.template.md` or your repo-local copies of them. -->
