---
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
| `ARCHITECTURE.md` | [System architecture — create if needed] |
| `ROADMAP.md` | Phase planning and acceptance targets |
| `session_state.md` | Cross-session state |
| `docs/INDEX.md` | TYPE-A doc navigation index |
| `docs/COMPATIBILITY.md` | [Verified tooling surface and known limits — create if useful] |
| `templates/execution_contract.template.md` | [Pre-execution confirmation contract for long tasks] |
| `docs/RUNTIME_SURFACE_PROTECTION.md` | [Guard-registry pattern for active user-facing runtime paths — create if useful] |
| `docs/LEFTOVER_UNIT_CONTRACT.md` | [How your team records and recovers partial work — create if useful] |
| `docs/STRATEGY_MECHANISM_LAYERING.md` | How to separate role strategy from workflow mechanism |
| `docs/runbooks/resumable-git-audit-pipeline.md` | Packet / receipt / handoff workflow for resumable audit and Git closeout |

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
| `compatibility\|supported tool\|verified\|known limits` | `docs/COMPATIBILITY.md` |
| `execution contract\|task confirmation\|long task\|while loop\|autonomous mode\|commit push policy` | `templates/execution_contract.template.md` |
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
