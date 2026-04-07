#!/usr/bin/env python3
"""Bootstrap this template into another repository."""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

PROJECT_TYPE_PRESETS: dict[str, dict[str, object]] = {
    "backend-api": {
        "primary_language": "Python",
        "package_manager": "pip",
        "project_map_rows": (
            "| `src/` | API implementation and domain services |",
            "| `tests/` | Unit and integration test suites |",
            "| `docs/` | Architecture, API, and runbook documentation |",
            "| `data/` | Local runtime state and fixtures (protected) |",
            "| `.github/` | Agent rules, workflows, and project adapter |",
        ),
        "validation_tool_rows": (
            "| Unit | pytest | `pytest tests/unit -q` |",
            "| Integration | pytest | `pytest tests/integration -q` |",
            "| End-to-end | curl smoke script | `./scripts/smoke.sh` |",
        ),
        "developer_tool_rows": (
            "| Diagnostics | `pyright .` | `module` | `declared-unverified` | Fall back to `python -m compileall src tests` before deeper runtime work | Type and import diagnostics |",
            "| Run | `./scripts/start.sh` | `service` | `declared-unverified` | If startup fails, inspect logs and stop unless a fallback run path is declared | Dev server entrypoint |",
            "| Health or smoke | `./scripts/smoke.sh` | `service` | `declared-unverified` | Stop and report if the service cannot be confirmed honestly | Fastest runtime confirmation path |",
            "| Repro path | `curl [primary endpoint]` | `service` | `declared-unverified` | Use `none` if no stable user-visible repro exists yet | Shortest API repro path |",
            "| Build | `python -m compileall src tests` | `module` | `declared-unverified` | Stop after build blockers are cleared when runnable proof is unnecessary | Required when runtime depends on build |",
            "| Lint | `ruff check .` | `file` | `declared-unverified` | Stop after lint when task scope is local and runnable proof is unnecessary | Recommended |",
        ),
        "full_suite": "pytest tests/ -q && ./scripts/smoke.sh",
        "build_test_commands": (
            "# Type check",
            "pyright .",
            "",
            "# Run tests",
            "pytest tests/ -q",
            "",
            "# Lint",
            "ruff check .",
            "",
            "# Build (if applicable)",
            "python -m compileall src tests",
            "",
            "# Start dev server",
            "./scripts/start.sh",
        ),
        "runtime_rows": (
            "| `.env` | Environment-level overrides |",
            "| `config/default.yaml` | API defaults and feature flags |",
        ),
        "protected_rows": (
            "| `data/` | Runtime state and local fixtures — destructive changes are irreversible |",
            "| `.env` | Secrets — append-edit preferred over wholesale overwrite |",
        ),
        "dangerous_ops": (
            "- Any path under `data/` → explicit confirmation required before destructive operations",
            "- `.env` file → prefer additive edits over wholesale replacement",
            "- Database migration scripts → require a rollback note before modification",
        ),
        "notes": (
            "- Activate your virtualenv before running validation commands.",
            "- Keep a lightweight smoke script in `scripts/smoke.sh` for UAC checks.",
        ),
        "runtime_evidence_rows": (
            "| Logs | `primary service` | `first` | `declared-unverified` | Fall back to stderr or stop and report missing runtime evidence | App log path or primary runtime output |",
            "| Health check | `primary API flow` | `first` | `declared-unverified` | Stop and report if the health path cannot be exercised honestly | `./scripts/smoke.sh` or `GET /health` |",
            "| Smoke path | `primary user flow` | `first` | `declared-unverified` | Fall back to logs plus repro and stop if neither is honest | Fastest runtime-adjacent confirmation |",
        ),
        "user_surface_rows": (
            "| `primary API flow` | `src/` | `no` | `curl [primary endpoint]` | `Health check` | Top user-visible API path |",
            "| `auth or admin API flow` | `src/` | `yes` | `curl [sensitive endpoint]` | `Logs` | Sensitive path needing stronger traceability |",
        ),
        "sensitive_rows": (
            "| `src/auth/` | auth and permission boundary |",
            "| `.env` | secrets and environment trust boundary |",
        ),
    },
    "web-frontend": {
        "primary_language": "TypeScript",
        "package_manager": "npm",
        "project_map_rows": (
            "| `src/` | UI components, routes, and client-side state |",
            "| `tests/` | Unit, integration, and browser tests |",
            "| `public/` | Static assets and HTML shell |",
            "| `docs/` | UX, architecture, and release docs |",
            "| `.github/` | Agent rules, workflows, and project adapter |",
        ),
        "validation_tool_rows": (
            "| Unit | Vitest | `npm run test:unit` |",
            "| Integration | Testing Library | `npm run test:integration` |",
            "| End-to-end | Playwright | `npm run test:e2e` |",
        ),
        "developer_tool_rows": (
            "| Diagnostics | `npm run typecheck` | `module` | `declared-unverified` | Fall back to editor diagnostics only if no CLI typecheck is available | Type diagnostics |",
            "| Run | `npm run dev` | `service` | `declared-unverified` | If startup fails, inspect logs and stop unless a fallback preview path is declared | Frontend dev server |",
            "| Health or smoke | `open primary route or run npm run test:e2e` | `service` | `declared-unverified` | Stop and report if the UI cannot be confirmed honestly | Fastest visible runtime confirmation |",
            "| Repro path | `open primary route and exercise main journey` | `full-stack` | `declared-unverified` | Use `none` only if no stable user journey exists yet | User-visible repro path |",
            "| Build | `npm run build` | `module` | `declared-unverified` | Stop after build blockers are cleared when runnable proof is unnecessary | Required when runtime depends on build |",
            "| Lint | `npm run lint` | `file` | `declared-unverified` | Stop after lint when task scope is local and runnable proof is unnecessary | Recommended |",
        ),
        "full_suite": "npm run lint && npm run test && npm run test:e2e",
        "build_test_commands": (
            "# Type check",
            "npm run typecheck",
            "",
            "# Run tests",
            "npm run test",
            "",
            "# Lint",
            "npm run lint",
            "",
            "# Build",
            "npm run build",
            "",
            "# Start dev server",
            "npm run dev",
        ),
        "runtime_rows": (
            "| `.env.local` | Local environment overrides |",
            "| `src/config.ts` | Frontend defaults and feature flags |",
        ),
        "protected_rows": (
            "| `.env.local` | API keys and local environment settings |",
            "| `public/` | User-facing static assets; deletions are high-visibility |",
        ),
        "dangerous_ops": (
            "- `.env.local` → append or patch specific keys instead of replacing the whole file",
            "- `public/` assets → confirm intent before destructive changes",
            "- Snapshot or contract fixtures → update only with corresponding UI evidence",
        ),
        "notes": (
            "- Keep at least one browser-driven E2E path for the primary user journey.",
            "- Call out responsive or accessibility validation in acceptance evidence.",
        ),
        "runtime_evidence_rows": (
            "| Logs | `frontend dev server` | `second` | `declared-unverified` | Fall back to browser console or stop and report missing evidence | Terminal output or browser console logs |",
            "| Health check | `primary route` | `first` | `declared-unverified` | Fall back to smoke path if no dedicated health path exists | Load the primary route successfully |",
            "| Smoke path | `main user journey` | `first` | `declared-unverified` | Stop and report if the journey cannot be exercised honestly | Browser path or `npm run test:e2e` |",
        ),
        "user_surface_rows": (
            "| `primary user journey` | `src/` | `no` | `open primary route and exercise main journey` | `Smoke path` | Main happy-path UI flow |",
            "| `login or billing journey` | `src/` | `yes` | `open sensitive route and validate access behavior` | `Logs` | Sensitive user-facing path needing stronger traceability |",
        ),
        "sensitive_rows": (
            "| `src/auth/` | auth and session boundary |",
            "| `.env.local` | API keys and local secret surface |",
        ),
    },
    "cli-tool": {
        "primary_language": "Python",
        "package_manager": "pip",
        "project_map_rows": (
            "| `src/` | CLI commands, parsing, and application logic |",
            "| `tests/` | Unit and command-level smoke tests |",
            "| `docs/` | Usage docs, examples, and runbooks |",
            "| `examples/` | Sample configs and command transcripts |",
            "| `.github/` | Agent rules, workflows, and project adapter |",
        ),
        "validation_tool_rows": (
            "| Unit | pytest | `pytest tests/unit -q` |",
            "| Integration | pytest | `pytest tests/integration -q` |",
            "| End-to-end | shell smoke test | `./scripts/smoke.sh` |",
        ),
        "developer_tool_rows": (
            "| Diagnostics | `pyright .` | `module` | `declared-unverified` | Fall back to `python -m compileall src tests` before deeper runtime work | Type and import diagnostics |",
            "| Run | `python -m src.main --help` | `service` | `declared-unverified` | If the entrypoint fails, inspect stderr and stop unless a fallback command is declared | Primary CLI entrypoint |",
            "| Health or smoke | `./scripts/smoke.sh` | `service` | `declared-unverified` | Stop and report if the CLI cannot be exercised honestly | Command-level smoke path |",
            "| Repro path | `run the primary user command with real arguments` | `service` | `declared-unverified` | Use `none` only if no stable user-visible flow exists yet | Shortest user-visible repro |",
            "| Build | `python -m build` | `module` | `declared-unverified` | Stop after build blockers are cleared when runnable proof is unnecessary | Required when packaging matters |",
            "| Lint | `ruff check .` | `file` | `declared-unverified` | Stop after lint when task scope is local and runnable proof is unnecessary | Recommended |",
        ),
        "full_suite": "pytest tests/ -q && ./scripts/smoke.sh",
        "build_test_commands": (
            "# Type check",
            "pyright .",
            "",
            "# Run tests",
            "pytest tests/ -q",
            "",
            "# Lint",
            "ruff check .",
            "",
            "# Build",
            "python -m build",
            "",
            "# Start",
            "python -m src.main --help",
        ),
        "runtime_rows": (
            "| `.env` | Local overrides for CLI flags and secrets |",
            "| `config/default.toml` | CLI defaults and command behavior |",
        ),
        "protected_rows": (
            "| `.env` | Secrets and developer overrides |",
            "| `examples/` | User-facing reference material; preserve intentional output |",
        ),
        "dangerous_ops": (
            "- `.env` → do not overwrite wholesale when a targeted edit is enough",
            "- `examples/` output transcripts → update only when command output intentionally changes",
            "- Packaged entrypoints → verify `--help` output after edits",
        ),
        "notes": (
            "- Keep one shell smoke test that exercises the main command exactly as a user would run it.",
            "- Prefer human-readable CLI output in UAC items, not just exit-code checks.",
        ),
        "runtime_evidence_rows": (
            "| Logs | `cli execution` | `first` | `declared-unverified` | Fall back to stderr capture or stop and report missing runtime evidence | Command stdout or stderr is usually the first evidence surface |",
            "| Health check | `main command` | `first` | `declared-unverified` | Fall back to smoke path if the direct command is not stable yet | `python -m src.main --help` or a safe command invocation |",
            "| Smoke path | `primary user command` | `first` | `declared-unverified` | Stop and report if the command cannot be exercised honestly | `./scripts/smoke.sh` |",
        ),
        "user_surface_rows": (
            "| `primary CLI command` | `src/` | `no` | `run the main command with real arguments` | `Smoke path` | Main user-visible CLI path |",
            "| `credentialed or destructive command` | `src/` | `yes` | `run the sensitive command in a safe fixture environment` | `Logs` | Sensitive because user trust or irreversible actions may be involved |",
        ),
        "sensitive_rows": (
            "| `.env` | secrets and credential surface |",
            "| `src/commands/` | command behavior that may be destructive or high-trust |",
        ),
    },
    "library": {
        "primary_language": "Python",
        "package_manager": "pip",
        "project_map_rows": (
            "| `src/` | Reusable library modules and public APIs |",
            "| `tests/` | Unit and contract tests |",
            "| `docs/` | API notes, migration guides, and architecture docs |",
            "| `benchmarks/` | Optional performance or compatibility checks |",
            "| `.github/` | Agent rules, workflows, and project adapter |",
        ),
        "validation_tool_rows": (
            "| Unit | pytest | `pytest tests/unit -q` |",
            "| Integration | contract tests | `pytest tests/contracts -q` |",
            "| End-to-end | example import smoke test | `python examples/smoke_import.py` |",
        ),
        "developer_tool_rows": (
            "| Diagnostics | `pyright .` | `module` | `declared-unverified` | Fall back to `python -m compileall src tests` before deeper work | Type and import diagnostics |",
            "| Run | `none` | `service` | `not-applicable` | Stop at build or smoke unless runnable proof is explicitly requested | No live service runtime by default |",
            "| Health or smoke | `python examples/smoke_import.py` | `module` | `declared-unverified` | Stop and report if public API smoke cannot run honestly | Public API smoke path |",
            "| Repro path | `none` | `full-stack` | `not-applicable` | Stop after smoke unless a consumer repro path is declared | Libraries may not expose a live runtime path |",
            "| Build | `python -m build` | `module` | `declared-unverified` | Stop after build blockers are cleared when smoke is unnecessary | Required when packaging matters |",
            "| Lint | `ruff check .` | `file` | `declared-unverified` | Stop after lint when task scope is local and runnable proof is unnecessary | Recommended |",
        ),
        "full_suite": "pytest tests/ -q && python examples/smoke_import.py",
        "build_test_commands": (
            "# Type check",
            "pyright .",
            "",
            "# Run tests",
            "pytest tests/ -q",
            "",
            "# Lint",
            "ruff check .",
            "",
            "# Build",
            "python -m build",
            "",
            "# Start",
            "python -c 'import src'",
        ),
        "runtime_rows": (
            "| `pyproject.toml` | Package metadata and tool configuration |",
            "| `src/config.py` | Library defaults, if applicable |",
        ),
        "protected_rows": (
            "| `pyproject.toml` | Package metadata and release-sensitive configuration |",
            "| `examples/` | Consumer-facing examples; preserve upgrade guidance |",
        ),
        "dangerous_ops": (
            "- `pyproject.toml` → confirm versioning or packaging intent before destructive edits",
            "- Public API files → require compatibility note when signatures change",
            "- Examples and migration docs → update in the same change as API behavior",
        ),
        "notes": (
            "- Track compatibility guarantees explicitly in docs and changelog entries.",
            "- Keep at least one smoke import path that uses the public API only.",
        ),
        "runtime_evidence_rows": (
            "| Logs | `import and packaging workflows` | `second` | `declared-unverified` | Fall back to command stderr or stop and report missing runtime evidence | Build and import output is often the first evidence surface |",
            "| Health check | `public API smoke` | `first` | `declared-unverified` | Stop and report if the public API cannot be exercised honestly | `python examples/smoke_import.py` |",
            "| Smoke path | `consumer import path` | `first` | `declared-unverified` | Fall back to build output if the smoke path is missing | Fastest consumer-facing confirmation |",
        ),
        "user_surface_rows": (
            "| `public API import path` | `src/` | `no` | `python examples/smoke_import.py` | `Health check` | Main consumer-visible surface for a library |",
            "| `compatibility-sensitive API path` | `src/` | `yes` | `run the public API call covered by compatibility docs` | `Logs` | Sensitive when compatibility or upgrade safety matters |",
        ),
        "sensitive_rows": (
            "| `pyproject.toml` | packaging and release trust boundary |",
            "| `src/` public API files | compatibility-sensitive surface |",
        ),
    },
    "full-stack": {
        "primary_language": "TypeScript + Python",
        "package_manager": "npm + pip",
        "project_map_rows": (
            "| `frontend/` | Browser UI and client-side state |",
            "| `backend/` | API, jobs, and domain services |",
            "| `tests/` | Cross-layer tests and E2E coverage |",
            "| `docs/` | Architecture, deployment, and release docs |",
            "| `.github/` | Agent rules, workflows, and project adapter |",
        ),
        "validation_tool_rows": (
            "| Unit | project-native test runner | `[frontend unit] + [backend unit]` |",
            "| Integration | API + UI integration tests | `[integration command]` |",
            "| End-to-end | browser or journey test | `[e2e command]` |",
        ),
        "developer_tool_rows": (
            "| Diagnostics (frontend) | `[frontend typecheck]` | `module` | `declared-unverified` | Fall back to narrower frontend diagnostics before starting the full stack | Frontend type diagnostics |",
            "| Diagnostics (backend) | `[backend typecheck]` | `module` | `declared-unverified` | Fall back to compile diagnostics before broader runtime work | Backend type diagnostics |",
            "| Run (frontend) | `[frontend dev server]` | `service` | `declared-unverified` | If startup fails, stop unless a preview fallback is declared | Frontend runtime entrypoint |",
            "| Run (backend) | `[backend api command]` | `service` | `declared-unverified` | If startup fails, stop unless a narrower backend fallback is declared | Backend runtime entrypoint |",
            "| Health or smoke (backend) | `[backend health check]` | `service` | `declared-unverified` | Stop and report if the API cannot be confirmed honestly | Fastest backend runtime confirmation |",
            "| Health or smoke (journey) | `[integration command]` | `full-stack` | `declared-unverified` | Stop and report if the user journey cannot be confirmed honestly | Cross-layer smoke path |",
            "| Repro path (primary journey) | `[primary user journey]` | `full-stack` | `declared-unverified` | Use `none` only if no stable user journey exists yet | Shortest full-stack repro path |",
            "| Build (frontend) | `[frontend build]` | `module` | `declared-unverified` | Stop after frontend build blockers are cleared when runnable proof is unnecessary | Frontend build surface |",
            "| Build (backend) | `[backend build]` | `module` | `declared-unverified` | Stop after backend build blockers are cleared when runnable proof is unnecessary | Backend build surface |",
            "| Lint (frontend) | `[frontend lint]` | `file` | `declared-unverified` | Stop after frontend lint when task scope is local | Recommended |",
            "| Lint (backend) | `[backend lint]` | `file` | `declared-unverified` | Stop after backend lint when task scope is local | Recommended |",
        ),
        "full_suite": "[unit] && [integration] && [e2e]",
        "build_test_commands": (
            "# Type check",
            "[frontend typecheck] && [backend typecheck]",
            "",
            "# Run tests",
            "[unit tests] && [integration tests]",
            "",
            "# Lint",
            "[frontend lint] && [backend lint]",
            "",
            "# Build",
            "[frontend build] && [backend build]",
            "",
            "# Start dev stack",
            "docker compose up app db",
        ),
        "runtime_rows": (
            "| `.env` | Shared environment overrides |",
            "| `frontend/src/config.ts` | UI defaults and flags |",
            "| `backend/config/default.yaml` | API/runtime defaults |",
        ),
        "protected_rows": (
            "| `.env` | Shared secrets and environment configuration |",
            "| `docker-compose.yml` | Environment orchestration; high blast radius |",
        ),
        "dangerous_ops": (
            "- `.env` → confirm secret handling before replacements",
            "- Environment orchestration files → call out blast radius before destructive edits",
            "- Cross-layer contract files → require UI + API evidence together",
        ),
        "notes": (
            "- Define one end-to-end user journey that crosses frontend and backend every time.",
            "- Keep contract drift visible in docs when frontend and backend change together.",
        ),
        "runtime_evidence_rows": (
            "| Logs | `frontend and backend runtimes` | `second` | `declared-unverified` | Fall back to the narrower service log that owns the failing surface | Record where each service emits first-line evidence |",
            "| Health check | `backend service` | `first` | `declared-unverified` | Fall back to journey smoke if the service health path is missing | `[backend health check]` |",
            "| Smoke path | `primary full-stack journey` | `first` | `declared-unverified` | Stop and report if the journey cannot be exercised honestly | `[integration command]` |",
        ),
        "user_surface_rows": (
            "| `primary full-stack journey` | `frontend/` + `backend/` | `no` | `[primary user journey]` | `Smoke path` | Cross-layer happy path |",
            "| `auth or payment journey` | `frontend/` + `backend/` | `yes` | `[sensitive user journey]` | `Logs` | Sensitive because it crosses trust boundaries |",
        ),
        "sensitive_rows": (
            "| `backend/auth/` | auth and permission boundary |",
            "| `.env` | shared secret and environment trust boundary |",
        ),
    },
}


@dataclass(frozen=True)
class BootstrapResult:
    project_type: str
    capabilities: tuple[str, ...]
    created: tuple[Path, ...]
    skipped: tuple[Path, ...]
    conflicts: tuple[Path, ...]


PROFILE_COPY_PATHS: dict[str, tuple[str, ...]] = {
    "minimal": (
        ".github/copilot-instructions.md",
        "docs/INDEX.md",
        "docs/archive/.gitkeep",
    ),
    "standard": (
        ".github/RELEASE_TEMPLATE.md",
        ".github/agents/architect.agent.md",
        ".github/agents/implementer.agent.md",
        ".github/instructions/backend.instructions.md",
        ".github/instructions/docs.instructions.md",
        ".github/workflows/ci.yml",
        "CHANGELOG.md",
        "LICENSE",
        "VERSION",
        "docs/ADOPTION_GUIDE.md",
        "docs/AI_TRACEABILITY_AND_RECOVERY_DISCUSSION.md",
        "docs/CLOSEOUT_SUMMARY_TEMPLATE.md",
        "docs/COMPATIBILITY.md",
        "docs/DEVELOPER_TOOLCHAIN_DESIGN.md",
        "docs/DEVELOPER_TOOLCHAIN_DISCUSSION.md",
        "docs/DOC_FIRST_EXECUTION_GUIDELINES.md",
        "docs/FRAMEWORK_ARCHITECTURE.md",
        "docs/LEFTOVER_UNIT_CONTRACT.md",
        "docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md",
        "docs/SKILL_HARVEST_LOOP_V1_DRAFT.md",
        "docs/SKILL_MECHANISM_V1_DRAFT.md",
        "docs/runbooks/multi-model-discussion-loop.md",
        "docs/RUNTIME_SURFACE_PROTECTION.md",
        "docs/TRACEABILITY_AND_RECOVERY_V1_DRAFT.md",
        "docs/runbooks/resumable-git-audit-pipeline.md",
        "scripts/active_docs_audit.py",
        "scripts/closeout_truth_audit.py",
        "scripts/discussion_pipeline.py",
        "scripts/git_audit_pipeline.py",
        "scripts/preference_drift_audit.py",
        "scripts/skill_evolution_pipeline.py",
        "scripts/validate-template.sh",
        "scripts/validate_template.py",
        "templates/discussion_packet.template.md",
        "templates/git_audit_handoff_packet.template.md",
        "templates/git_audit_receipt.template.md",
        "templates/git_audit_task_packet.template.md",
        "templates/doc_first_execution_guidelines.template.md",
        "templates/execution_contract.template.md",
        "templates/failure_packet.template.md",
        "templates/project-context.template.md",
        "templates/root_cause_note.template.md",
        "templates/roadmap.template.md",
        "templates/session_state.template.md",
        "templates/skill_candidate_packet.template.md",
        "templates/skill_invocation_receipt.template.md",
        "templates/skill_promotion_receipt.template.md",
        "templates/skill.template.md",
        "templates/skill_tool_wrapper.template.md",
        "templates/skill_reviewer_gate.template.md",
        "templates/skill_pipeline.template.md",
        "templates/skill_artifact_generator.template.md",
        "examples/skills/01_discussion_packet_workflow.md",
        "examples/skills/02_no_placeholder_runtime_guardrail.md",
        "examples/skills/03_developer_toolchain_wrapper.md",
        "examples/skills/04_receipt_anchored_reviewer.md",
        "examples/skills/05_staged_handoff_pipeline.md",
        "examples/skills/06_bounded_artifact_generator.md",
        "examples/demo_project/README.md",
        "examples/demo_project/.github/instructions/project-context.instructions.md",
        "examples/demo_project/ROADMAP.md",
        "examples/demo_project/session_state.md",
        "examples/demo_project/docs/ARCHITECTURE.md",
        "examples/demo_project/docs/INDEX.md",
        "examples/demo_project/docs/runbooks/demo-workflow.md",
        "examples/demo_project/docs/runbooks/execution_contract_example.md",
        "examples/demo_project/src/task_tracker.py",
        "examples/demo_project/tests/test_task_tracker.py",
        "examples/demo_project/tmp/git_audit/add_task_priority/audit_receipt.md",
        "examples/demo_project/tmp/git_audit/add_task_priority/handoff_packet.md",
        "examples/demo_project/tmp/git_audit/add_task_priority/task_packet.md",
        "examples/full_stack_project/README.md",
        "examples/full_stack_project/.github/instructions/project-context.instructions.md",
        "examples/full_stack_project/.github/agent-framework-manifest.json",
        "examples/full_stack_project/docs/INDEX.md",
        "examples/full_stack_project/docs/runbooks/full-stack-workflow.md",
        "examples/full_stack_project/frontend/src/.gitkeep",
        "examples/full_stack_project/backend/app/.gitkeep",
        "examples/full_stack_project/tests/e2e/.gitkeep",
        "examples/reviewer_roles/01_goal_acceptance_owner.md",
        "examples/reviewer_roles/02_plan_checkpoint_owner.md",
        "examples/reviewer_roles/03_runtime_correctness_reviewer.md",
        "examples/reviewer_roles/04_boundary_contract_reviewer.md",
        "examples/reviewer_roles/05_git_closeout_reviewer.md",
        "examples/reviewer_roles/06_maintainability_reviewer.md",
        "examples/reviewer_roles/07_observability_failure_path_reviewer.md",
        "examples/reviewer_roles/08_performance_benchmark_reviewer.md",
        "examples/reviewer_roles/09_migration_compatibility_reviewer.md",
        "examples/reviewer_roles/10_docs_spec_drift_reviewer.md",
    ),
    "full": (
        "docs/ROLE_STRATEGY_EXAMPLES.md",
        "docs/STRATEGY_MECHANISM_LAYERING.md",
        "examples/skills/01_discussion_packet_workflow.md",
        "examples/skills/02_no_placeholder_runtime_guardrail.md",
        "examples/skills/03_developer_toolchain_wrapper.md",
        "examples/skills/04_receipt_anchored_reviewer.md",
        "examples/skills/05_staged_handoff_pipeline.md",
        "examples/skills/06_bounded_artifact_generator.md",
        "examples/demo_project/README.md",
        "examples/demo_project/.github/instructions/project-context.instructions.md",
        "examples/demo_project/ROADMAP.md",
        "examples/demo_project/session_state.md",
        "examples/demo_project/docs/ARCHITECTURE.md",
        "examples/demo_project/docs/INDEX.md",
        "examples/demo_project/docs/runbooks/demo-workflow.md",
        "examples/demo_project/src/task_tracker.py",
        "examples/demo_project/tests/test_task_tracker.py",
        "examples/demo_project/tmp/git_audit/add_task_priority/audit_receipt.md",
        "examples/demo_project/tmp/git_audit/add_task_priority/handoff_packet.md",
        "examples/demo_project/tmp/git_audit/add_task_priority/task_packet.md",
        "examples/full_stack_project/README.md",
        "examples/full_stack_project/.github/instructions/project-context.instructions.md",
        "examples/full_stack_project/.github/agent-framework-manifest.json",
        "examples/full_stack_project/docs/INDEX.md",
        "examples/full_stack_project/docs/runbooks/full-stack-workflow.md",
        "examples/full_stack_project/frontend/src/.gitkeep",
        "examples/full_stack_project/backend/app/.gitkeep",
        "examples/full_stack_project/tests/e2e/.gitkeep",
        "examples/reviewer_roles/01_goal_acceptance_owner.md",
        "examples/reviewer_roles/02_plan_checkpoint_owner.md",
        "examples/reviewer_roles/03_runtime_correctness_reviewer.md",
        "examples/reviewer_roles/04_boundary_contract_reviewer.md",
        "examples/reviewer_roles/05_git_closeout_reviewer.md",
        "examples/reviewer_roles/06_maintainability_reviewer.md",
        "examples/reviewer_roles/07_observability_failure_path_reviewer.md",
        "examples/reviewer_roles/08_performance_benchmark_reviewer.md",
        "examples/reviewer_roles/09_migration_compatibility_reviewer.md",
        "examples/reviewer_roles/10_docs_spec_drift_reviewer.md",
        "scripts/bootstrap_adoption.py",
        "templates/reviewer_role_profile.template.md",
    ),
}

CAPABILITY_COPY_PATHS: dict[str, tuple[str, ...]] = {
    "closeout-audit": (
        "scripts/closeout_truth_audit.py",
    ),
    "runtime-guards": (
        "scripts/runtime_surface_guardrails.py",
        "templates/runtime_surface_registry.template.py",
        "docs/RUNTIME_SURFACE_PROTECTION.md",
    ),
    "git-hooks": (
        ".githooks/pre-commit",
        ".githooks/pre-push",
        "scripts/install_git_hooks.sh",
    ),
}

RENDERED_FILES: dict[str, str] = {
    ".github/instructions/project-context.instructions.md": "templates/project-context.template.md",
    "session_state.md": "templates/session_state.template.md",
    "ROADMAP.md": "templates/roadmap.template.md",
}

CAPABILITY_RENDERED_FILES: dict[str, dict[str, str]] = {
    "runtime-guards": {
        ".github/runtime_surface_registry.py": "templates/runtime_surface_registry.template.py",
    }
}

MANIFEST_PATH = ".github/agent-framework-manifest.json"


def _iter_profile_paths(profile: str) -> tuple[str, ...]:
    ordered_profiles = ("minimal", "standard", "full")
    selected: list[str] = []
    for current in ordered_profiles:
        selected.extend(PROFILE_COPY_PATHS[current])
        if current == profile:
            break
    return tuple(selected)


def _iter_capability_paths(capabilities: tuple[str, ...]) -> tuple[str, ...]:
    selected: list[str] = []
    for capability in capabilities:
        selected.extend(CAPABILITY_COPY_PATHS[capability])
    return tuple(selected)


def _dedupe_paths(paths: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(paths))


def detect_project_type(target_dir: Path) -> str:
    if (target_dir / "package.json").exists():
        if (target_dir / "frontend").exists() and (target_dir / "backend").exists():
            return "full-stack"
        return "web-frontend"
    if (target_dir / "pyproject.toml").exists():
        return "backend-api"
    if (target_dir / "Cargo.toml").exists() or (target_dir / "go.mod").exists():
        return "library"
    return "cli-tool"


def _replace_project_name(contents: str, project_name: str) -> str:
    return contents.replace("[Project Name]", project_name)


def _replace_project_context_sections(contents: str, project_type: str) -> str:
    preset = PROJECT_TYPE_PRESETS[project_type]
    replacements = {
        "| `src/` | [Main application source — describe here] |\n| `docs/` | Architecture, deployment, and system docs |\n| `tests/` | Test suites |\n| `data/` | [Runtime state / user data — if applicable] |\n| `.github/` | Agent behavior rules and project adapter |": "\n".join(preset["project_map_rows"]),
        "Project type: [fill in]": f"Project type: {project_type}",
        "| Unit | [pytest / Jest / Vitest / etc.] | `[command]` |\n| Integration | [httpx / supertest / React Testing Library / etc.] | `[command]` |\n| End-to-end | [Playwright / Cypress / Newman / curl script / etc.] | `[command]` |": "\n".join(preset["validation_tool_rows"]),
        "# Run full suite (all tiers in sequence)\n# [single command or script]": f"# Run full suite (all tiers in sequence)\n{preset['full_suite']}",
        "Primary language: [fill in]\n\nPackage manager: [fill in]\n\n| Surface | Command or source | Scope | Status | Fallback or stop | Notes |\n|---|---|---|---|---|---|\n| Diagnostics | [command or source] | [file / module] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [syntax or type diagnostics] |\n| Run | [command or `none`] | [service / full-stack] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [main local execution path] |\n| Health or smoke | [command or `none`] | [service / full-stack] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [fastest reliable runtime confirmation] |\n| Repro path | [command, script, or `none`] | [service / full-stack] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [required for repos with a live runtime path] |\n| Build | [command or `none`] | [module / service] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [required when the runtime path depends on build] |\n| Lint | [command or `none`] | [file / module] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [recommended] |": f"Primary language: {preset['primary_language']}\n\nPackage manager: {preset['package_manager']}\n\n| Surface | Command or source | Scope | Status | Fallback or stop | Notes |\n|---|---|---|---|---|---|\n" + "\n".join(preset["developer_tool_rows"]),
        "| Logs | [surface / service / `none`] | [first / second / fallback] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [log path, command, or viewer] |\n| Health check | [surface / service / `none`] | [first / second / fallback] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [endpoint, script, or command] |\n| Smoke path | [surface / service / `none`] | [first / second / fallback] | [declared-unverified / verified-working / known-broken / not-applicable] | [fallback or explicit stop rule] | [fastest runtime-adjacent confirmation] |\n| [Optional additional evidence] | [surface / service] | [priority] | [status] | [fallback or stop] | [trace / metric / screenshot harness / inspection command] |": "\n".join(preset["runtime_evidence_rows"]),
        "| [surface] | [path / module / entrypoint / `none`] | [yes / no] | [command / script / route / `none`] | [logs / health / smoke / trace / user report / `none`] | [optional short context] |\n| [surface] | [path / module / entrypoint / `none`] | [yes / no] | [command / script / route / `none`] | [logs / health / smoke / trace / user report / `none`] | [optional short context] |": "\n".join(preset["user_surface_rows"]),
        "| `[path / config / flow]` | [auth / secrets / billing / export / model routing / external tool / prompt boundary] |": "\n".join(preset["sensitive_rows"]),
        "# Replace with actual project commands\n\n# Type check\n# pyright .\n\n# Run tests\n# pytest tests/\n\n# Lint\n# ruff check .\n\n# Build\n# npm run build\n\n# Start\n# ./scripts/start.sh": "\n".join(preset["build_test_commands"]),
        "| `data/` | Runtime state — irreversible if deleted |\n| `.env` | Secrets — append preferred over overwrite |\n| `[add more]` | [reason] |": "\n".join(preset["protected_rows"]),
        "| `.env` | Environment-level overrides |\n| `[config file path]` | [what it controls] |": "\n".join(preset["runtime_rows"]),
        "- `data/` → explicit confirmation required before any destructive operation\n- `.env` → do not overwrite wholesale\n- [Add project-specific entries]": "\n".join(preset["dangerous_ops"]),
        "<!-- Add environment-specific notes: venv activation, service pre-checks, etc. -->": "\n".join(preset["notes"]),
    }
    rendered = contents
    for source, target in replacements.items():
        rendered = rendered.replace(source, target)
    return rendered


def _render_template(source: Path, project_name: str, project_type: str) -> str:
    contents = _replace_project_name(source.read_text(encoding="utf-8"), project_name)
    if source.name == "project-context.template.md":
        contents = _replace_project_context_sections(contents, project_type)
    return contents


def _copy_file(source: Path, destination: Path, *, force: bool, dry_run: bool) -> bool:
    if destination.exists() and not force:
        return False
    if dry_run:
        return True
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return True


def _write_text(destination: Path, contents: str, *, force: bool, dry_run: bool) -> bool:
    if destination.exists() and not force:
        return False
    if dry_run:
        return True
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(contents, encoding="utf-8")
    return True


def _write_manifest(
    destination: Path,
    *,
    project_name: str,
    profile: str,
    project_type: str,
    capabilities: tuple[str, ...],
    expected_files: tuple[str, ...],
    force: bool,
    dry_run: bool,
) -> bool:
    payload = {
        "schema_version": 2,
        "project_name": project_name,
        "profile": profile,
        "project_type": project_type,
        "capabilities": list(capabilities),
        "expected_files": list(expected_files),
        "developer_toolchain_contract": {
            "version": "v1",
            "enforcement": "required-core",
            "required_top_level_fields": ["Primary language", "Package manager"],
            "required_surface_kinds": [
                "Diagnostics",
                "Run",
                "Health or smoke",
                "Repro path",
            ],
            "recommended_surface_kinds": ["Build", "Lint"],
            "allow_surface_qualifiers": True,
        },
    }
    return _write_text(
        destination,
        json.dumps(payload, indent=2) + "\n",
        force=force,
        dry_run=dry_run,
    )


def _skill_accumulation_assets_included(profile: str) -> bool:
    return profile in {"standard", "full"}


def _print_next_steps(*, profile: str, capabilities: tuple[str, ...]) -> None:
    print("Next steps:")
    print("1. Fill any remaining placeholder docs or commands for your project.")
    if profile == "minimal":
        print("2. Add the standard profile later if you want bundled validation tooling and CI.")
        print("3. Fill the Developer Toolchain section honestly, using explicit 'none' where needed.")
        print("4. Create your first ROADMAP and session-state entries before starting feature work.")
        print(
            "5. If long-term agent improvement matters, add the standard profile before rollout so the SKILL and harvest-governance surfaces ship together."
        )
    else:
        print("2. Run python3 scripts/validate_template.py from the target repository.")
        print("3. Fill the Developer Toolchain section honestly, using explicit 'none' where needed.")
        print("4. Do one bootstrap smoke task before adopting the workflow broadly.")
        if _skill_accumulation_assets_included(profile):
            print(
                "5. If you want long-term agent improvement, keep the shipped SKILL and harvest-governance docs or templates, then initialize at least one repository-specific skill before broad rollout."
            )
            print(
                "6. Do not promote raw transcript excerpts straight into canonical skills; use candidate packets and promotion receipts as the mutation boundary."
            )
    if capabilities:
        print("7. Review any opt-in capability scaffolding before enabling it in production.")


def bootstrap_repo(
    *,
    target_dir: Path,
    project_name: str,
    profile: str,
    project_type: str | None = None,
    capabilities: tuple[str, ...] = (),
    force: bool = False,
    dry_run: bool = False,
) -> BootstrapResult:
    chosen_project_type = project_type or detect_project_type(target_dir)
    selected_capabilities = tuple(dict.fromkeys(capabilities))
    created: list[Path] = []
    skipped: list[Path] = []
    conflicts: list[Path] = []

    planned_paths = _dedupe_paths(
        (*_iter_profile_paths(profile), *_iter_capability_paths(selected_capabilities))
    )

    for relative_path in planned_paths:
        source = REPO_ROOT / relative_path
        destination = target_dir / relative_path
        copied = _copy_file(source, destination, force=force, dry_run=dry_run)
        if copied:
            created.append(destination)
        else:
            skipped.append(destination)
            if destination.exists():
                conflicts.append(destination)

    for destination_rel, source_rel in RENDERED_FILES.items():
        source = REPO_ROOT / source_rel
        destination = target_dir / destination_rel
        contents = _render_template(source, project_name, chosen_project_type)
        rendered = _write_text(destination, contents, force=force, dry_run=dry_run)
        if rendered:
            created.append(destination)
        else:
            skipped.append(destination)
            if destination.exists():
                conflicts.append(destination)

    for capability in selected_capabilities:
        for destination_rel, source_rel in CAPABILITY_RENDERED_FILES.get(capability, {}).items():
            source = REPO_ROOT / source_rel
            destination = target_dir / destination_rel
            contents = _render_template(source, project_name, chosen_project_type)
            rendered = _write_text(destination, contents, force=force, dry_run=dry_run)
            if rendered:
                created.append(destination)
            else:
                skipped.append(destination)
                if destination.exists():
                    conflicts.append(destination)

    manifest_destination = target_dir / MANIFEST_PATH
    manifest_written = _write_manifest(
        manifest_destination,
        project_name=project_name,
        profile=profile,
        project_type=chosen_project_type,
        capabilities=selected_capabilities,
        expected_files=tuple(
            dict.fromkeys(
                [
                    *planned_paths,
                    *RENDERED_FILES.keys(),
                    *[
                        destination_rel
                        for capability in selected_capabilities
                        for destination_rel in CAPABILITY_RENDERED_FILES.get(capability, {}).keys()
                    ],
                    MANIFEST_PATH,
                ]
            )
        ),
        force=force,
        dry_run=dry_run,
    )
    if manifest_written:
        created.append(manifest_destination)
    else:
        skipped.append(manifest_destination)
        if manifest_destination.exists():
            conflicts.append(manifest_destination)

    return BootstrapResult(
        project_type=chosen_project_type,
        capabilities=selected_capabilities,
        created=tuple(created),
        skipped=tuple(skipped),
        conflicts=tuple(conflicts),
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bootstrap the agent framework template into another repository"
    )
    parser.add_argument("target_dir", type=Path, help="Repository root to populate")
    parser.add_argument("--project-name", required=True, help="Project name used in rendered files")
    parser.add_argument(
        "--profile",
        choices=("minimal", "standard", "full"),
        default="standard",
        help="Amount of framework material to copy",
    )
    parser.add_argument(
        "--project-type",
        choices=tuple(PROJECT_TYPE_PRESETS),
        help="Project preset to use for the rendered project-context file",
    )
    parser.add_argument(
        "--capability",
        dest="capabilities",
        action="append",
        choices=tuple(CAPABILITY_COPY_PATHS),
        default=[],
        help="Optional executable capability to include in addition to the selected profile",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files instead of skipping them",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be created without writing files",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    target_dir = args.target_dir.resolve()
    result = bootstrap_repo(
        target_dir=target_dir,
        project_name=args.project_name,
        profile=args.profile,
        project_type=args.project_type,
        capabilities=tuple(args.capabilities),
        force=args.force,
        dry_run=args.dry_run,
    )

    action = "Would create" if args.dry_run else "Created"
    print(f"{action} {len(result.created)} file(s) for profile '{args.profile}'.")
    print(f"Project type preset: {result.project_type}")
    if result.capabilities:
        print(f"Capabilities: {', '.join(result.capabilities)}")
    print(f"Target repository: {target_dir}")
    for path in result.created:
        print(f"+ {path}")

    if result.skipped:
        print(f"Skipped {len(result.skipped)} existing file(s).")
        for path in result.skipped:
            print(f"= {path}")

    if result.conflicts:
        print("Conflict report:")
        for path in result.conflicts:
            print(f"! {path}")

    _print_next_steps(profile=args.profile, capabilities=result.capabilities)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
