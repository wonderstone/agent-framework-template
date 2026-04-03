---
applyTo: "**"
description: >
  Reference project-context file for a multi-runtime adopted repository.
---

# Full Stack Reference Project — Project Context

## Project Map

| Path | Purpose |
|---|---|
| `frontend/` | Browser UI and route-level flows |
| `backend/` | API, jobs, and domain services |
| `tests/e2e/` | Browser or cross-service journeys |
| `docs/` | Architecture and runbook docs |
| `.github/` | Agent rules, manifest, and project adapter |

Project type: full-stack

## Developer Toolchain

Primary language: TypeScript + Python

Package manager: npm + pip

| Surface | Command or source | Scope | Status | Fallback or stop | Notes |
|---|---|---|---|---|---|
| Diagnostics (frontend) | `npm run typecheck:web` | `module` | `declared-unverified` | Fall back to editor diagnostics only if the CLI checker is temporarily unavailable | Frontend type diagnostics |
| Diagnostics (backend) | `pyright backend` | `module` | `declared-unverified` | Fall back to `python -m compileall backend tests` before deeper runtime work | Backend type diagnostics |
| Run (frontend) | `npm run dev:web` | `service` | `declared-unverified` | If startup fails, stop unless a preview fallback is declared | Frontend runtime entrypoint |
| Run (backend) | `uvicorn backend.app.main:app --reload` | `service` | `declared-unverified` | If startup fails, stop unless a narrower backend fallback is declared | Backend runtime entrypoint |
| Health or smoke (backend) | `curl http://localhost:8000/health` | `service` | `declared-unverified` | Stop and report if the API cannot be confirmed honestly | Fast backend confirmation |
| Health or smoke (journey) | `npm run test:smoke` | `full-stack` | `declared-unverified` | Stop and report if the journey smoke fails before full repro | Cross-layer smoke path |
| Repro path (primary journey) | `open /login -> create record -> verify dashboard summary` | `full-stack` | `declared-unverified` | Use `none` only if no stable user-visible journey exists yet | Shortest full-stack repro |
| Build (frontend) | `npm run build:web` | `module` | `declared-unverified` | Stop after frontend build blockers are cleared when runnable proof is unnecessary | Frontend build surface |
| Build (backend) | `python -m build backend` | `module` | `declared-unverified` | Stop after backend build blockers are cleared when runnable proof is unnecessary | Backend build surface |
| Lint (frontend) | `npm run lint:web` | `file` | `declared-unverified` | Stop after frontend lint when task scope is local | Recommended |
| Lint (backend) | `ruff check backend tests` | `file` | `declared-unverified` | Stop after backend lint when task scope is local | Recommended |

### Runtime Evidence

| Evidence surface | Applies to | Priority | Status | Fallback or stop | Notes |
|---|---|---|---|---|---|
| Logs | `frontend and backend runtimes` | `second` | `declared-unverified` | Fall back to the narrower service log that owns the failing surface | Keep service-specific evidence discoverable without duplicating the whole map |
| Health check | `backend service` | `first` | `declared-unverified` | Fall back to journey smoke if the service health path is missing | `curl http://localhost:8000/health` |
| Smoke path | `primary full-stack journey` | `first` | `declared-unverified` | Stop and report if the journey cannot be exercised honestly | `npm run test:smoke` |

## User Surface Map

| Surface name | Owner path | Sensitive | Fastest repro path | Primary evidence source | Notes |
|---|---|---|---|---|---|
| `primary full-stack journey` | `frontend/` + `backend/` | `no` | `open /login -> create record -> verify dashboard summary` | `Smoke path` | Cross-layer happy path |
| `auth or payment journey` | `frontend/` + `backend/` | `yes` | `[sensitive user journey]` | `Logs` | Sensitive because it crosses trust boundaries and user data surfaces |

## Security-Sensitive Surfaces And Escalation

Sensitive path declarations:

| Path or surface | Why sensitive |
|---|---|
| `backend/auth/` | auth and permission boundary |
| `.env` | shared secret and environment trust boundary |
| `frontend/src/routes/login*` | sensitive entry path for authentication-related journeys |

Escalation rule:

1. automatically escalate failure tracking when an impacted user surface is marked `Sensitive = yes`
2. automatically escalate when a failure touches a declared sensitive path, config surface, secret surface, or trust-boundary surface
3. after escalation, require the failure artifact to record:
   impacted trust boundary, relevant config or secret surface, and at least one negative-path or misuse-path validation claim
4. human classification may upgrade severity further, but should not be the only trigger

## Build and Test Commands

```bash
# Type check
npm run typecheck:web && pyright backend

# Run tests
npm run test:web && pytest backend/tests -q

# Lint
npm run lint:web && ruff check backend tests

# Build
npm run build:web && python -m build backend

# Start
npm run dev:web
uvicorn backend.app.main:app --reload
```
