---
description: >
  [Project Name] project adapter. Provides the project map, critical topic triggers,
  protected paths, build/test commands, and runtime config locations. Always read
  this file before starting any multi-step task or when a critical keyword appears.
---

# [Project Name] — Project Context

## Project Map

<!-- Update these paths to match your actual project structure -->

| Path | Purpose |
|---|---|
| `src/` | Main application source |
| `docs/` | Architecture, deployment, and system docs |
| `tests/` | Test suites |
| `data/` | Runtime state and user data (protected) |
| `.github/` | Agent behavior rules and project adapter |

## Canonical Docs

| Doc | Purpose |
|---|---|
| `README.md` | Project entry point |
| `docs/FRAMEWORK_ARCHITECTURE.md` | Agent framework layer design |
| `docs/ADOPTION_GUIDE.md` | Step-by-step adoption guide |
| `docs/INDEX.md` | Navigation index for all TYPE-A docs |
| `session_state.md` | Cross-session state (current goal, decisions, insights) |

## Task Recovery Sequence

When resuming a multi-step task, recover context in this order:

1. Read this file
2. Read `docs/INDEX.md`
3. Read the canonical doc for the active topic (see triggers below)
4. Read the actual code/config files to be touched
5. If cross-session: read `session_state.md`

## Critical Topic Triggers

<!-- keyword pattern (regex) → canonical doc to load -->
<!-- Customize: add/remove rows to match your project's topic surface -->

| Trigger keywords | Canonical doc |
|---|---|
| `architecture\|design\|layers\|service boundary` | `docs/FRAMEWORK_ARCHITECTURE.md` |
| `adoption\|setup\|onboard\|quick.start` | `docs/ADOPTION_GUIDE.md` |
| `roadmap\|phase\|milestone\|current focus\|next phase` | `ROADMAP.md` |
| `flags\|config\|default values\|runtime override` | → check Runtime Config Locations |

## Build and Test Commands

<!-- Replace with actual commands for this project -->

```bash
# Type check
pyright .

# Run tests
pytest tests/

# Lint
ruff check .

# Build (if applicable)
npm run build

# Start dev server
./scripts/start.sh
```

## Protected Paths

<!-- Explicit user confirmation required before: delete, clear, overwrite, replace -->

| Path | Why protected |
|---|---|
| `data/` | Runtime state and user data — destructive changes are irreversible |
| `.env` | Secrets — append-edit preferred over wholesale overwrite |

## Runtime Config Locations

<!-- Where to look before changing any default value, port, or feature flag in code -->

| Location | What it controls |
|---|---|
| `.env` | Environment-level overrides |
| `config/default.yaml` | Application defaults (overridden by `.env`) |

## Dangerous Operations Policy

- Any path under `data/` → explicit confirmation required before any destructive operation
- `.env` file → do not overwrite wholesale when additive edit is sufficient
- Add project-specific entries here as the project evolves

## Notes

<!-- Add environment-specific operational notes here -->
<!-- Example: venv activation, service pre-checks, port conflicts -->
