#!/usr/bin/env python3
"""Bootstrap this template into another repository."""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

PROJECT_TYPE_PRESETS: dict[str, dict[str, object]] = {
    "backend-api": {
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
    },
    "web-frontend": {
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
    },
    "cli-tool": {
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
    },
    "library": {
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
    },
    "full-stack": {
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
    },
}


@dataclass(frozen=True)
class BootstrapResult:
    project_type: str
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
        "docs/COMPATIBILITY.md",
        "docs/FRAMEWORK_ARCHITECTURE.md",
        "docs/LEFTOVER_UNIT_CONTRACT.md",
        "docs/RUNTIME_SURFACE_PROTECTION.md",
        "docs/runbooks/resumable-git-audit-pipeline.md",
        "scripts/git_audit_pipeline.py",
        "scripts/validate-template.sh",
        "scripts/validate_template.py",
        "templates/git_audit_handoff_packet.template.md",
        "templates/git_audit_receipt.template.md",
        "templates/git_audit_task_packet.template.md",
        "templates/project-context.template.md",
        "templates/roadmap.template.md",
        "templates/session_state.template.md",
    ),
    "full": (
        "docs/ROLE_STRATEGY_EXAMPLES.md",
        "docs/STRATEGY_MECHANISM_LAYERING.md",
        "examples/demo_project/README.md",
        "examples/demo_project/.github/project-context.instructions.md",
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

RENDERED_FILES: dict[str, str] = {
    ".github/project-context.instructions.md": "templates/project-context.template.md",
    "session_state.md": "templates/session_state.template.md",
    "ROADMAP.md": "templates/roadmap.template.md",
}


def _iter_profile_paths(profile: str) -> tuple[str, ...]:
    ordered_profiles = ("minimal", "standard", "full")
    selected: list[str] = []
    for current in ordered_profiles:
        selected.extend(PROFILE_COPY_PATHS[current])
        if current == profile:
            break
    return tuple(selected)


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


def bootstrap_repo(
    *,
    target_dir: Path,
    project_name: str,
    profile: str,
    project_type: str | None = None,
    force: bool = False,
    dry_run: bool = False,
) -> BootstrapResult:
    chosen_project_type = project_type or detect_project_type(target_dir)
    created: list[Path] = []
    skipped: list[Path] = []
    conflicts: list[Path] = []

    for relative_path in _iter_profile_paths(profile):
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

    return BootstrapResult(
        project_type=chosen_project_type,
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
        force=args.force,
        dry_run=args.dry_run,
    )

    action = "Would create" if args.dry_run else "Created"
    print(f"{action} {len(result.created)} file(s) for profile '{args.profile}'.")
    print(f"Project type preset: {result.project_type}")
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

    print("Next steps:")
    print("1. Fill any remaining placeholder docs or commands for your project.")
    if args.profile == "minimal":
        print("2. Add the standard profile later if you want bundled validation tooling and CI.")
        print("3. Create your first ROADMAP and session-state entries before starting feature work.")
    else:
        print("2. Run python3 scripts/validate_template.py from the target repository.")
        print("3. Do one bootstrap smoke task before adopting the workflow broadly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
