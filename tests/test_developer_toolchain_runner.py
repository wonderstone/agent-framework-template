from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
import json

REPO_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_MODULE_PATH = REPO_ROOT / "scripts" / "bootstrap_adoption.py"
BOOTSTRAP_SPEC = importlib.util.spec_from_file_location("bootstrap_adoption_for_runner", BOOTSTRAP_MODULE_PATH)
assert BOOTSTRAP_SPEC is not None
assert BOOTSTRAP_SPEC.loader is not None
BOOTSTRAP_MODULE = importlib.util.module_from_spec(BOOTSTRAP_SPEC)
sys.modules[BOOTSTRAP_SPEC.name] = BOOTSTRAP_MODULE
BOOTSTRAP_SPEC.loader.exec_module(BOOTSTRAP_MODULE)

bootstrap_repo = BOOTSTRAP_MODULE.bootstrap_repo


def _write_runner_context(project_context_path: Path) -> None:
    project_context_path.write_text(
        """# Runner Context\n\n## Developer Toolchain\n\n| Surface | Command or source | Scope | Status | Fallback or stop | Notes |\n|---|---|---|---|---|---|\n| Diagnostics | `python -c \"print('diag ok')\"` | `module` | `verified-working` | Stop after diagnostics | Smoke diagnostics |\n| Lint | `python -c \"print('lint blocked')\"` | `file` | `known-broken` | Use diagnostics instead | Explicitly broken |\n| Build | `python -c \"print('build ok')\"` | `module` | `declared-unverified` | Stop | Build path |\n""",
        encoding="utf-8",
    )


def test_developer_toolchain_runner_lists_and_runs_surface(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )
    _write_runner_context(adopted_root / ".github" / "instructions" / "project-context.instructions.md")

    list_result = subprocess.run(
        [
            sys.executable,
            str(adopted_root / "scripts" / "developer_toolchain_runner.py"),
            "--root",
            str(adopted_root),
            "list-surfaces",
        ],
        cwd=adopted_root,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "| Diagnostics | module | verified-working |" in list_result.stdout

    output_path = adopted_root / "tmp" / "toolchain_run_receipts" / "runner.md"
    run_result = subprocess.run(
        [
            sys.executable,
            str(adopted_root / "scripts" / "developer_toolchain_runner.py"),
            "--root",
            str(adopted_root),
            "run-surface",
            "--surface",
            "Diagnostics",
            "--output",
            str(output_path),
        ],
        cwd=adopted_root,
        check=True,
        capture_output=True,
        text=True,
    )

    assert run_result.stdout.strip() == str(output_path)
    rendered = output_path.read_text(encoding="utf-8")
    assert "- Surface: Diagnostics" in rendered
    assert "- Outcome: success" in rendered


def test_developer_toolchain_runner_skips_known_broken_without_override(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )
    _write_runner_context(adopted_root / ".github" / "instructions" / "project-context.instructions.md")

    output_path = adopted_root / "tmp" / "toolchain_run_receipts" / "runner.md"
    subprocess.run(
        [
            sys.executable,
            str(adopted_root / "scripts" / "developer_toolchain_runner.py"),
            "--root",
            str(adopted_root),
            "run-surface",
            "--surface",
            "Lint",
            "--output",
            str(output_path),
        ],
        cwd=adopted_root,
        check=True,
        capture_output=True,
        text=True,
    )

    rendered = output_path.read_text(encoding="utf-8")
    assert "- Outcome: skipped-known-broken" in rendered


def test_developer_toolchain_runner_rejects_ambiguous_surface_kind(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="standard",
        project_type="full-stack",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(adopted_root / "scripts" / "developer_toolchain_runner.py"),
            "--root",
            str(adopted_root),
            "show-surface",
            "--surface",
            "Diagnostics",
        ],
        cwd=adopted_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "is ambiguous" in result.stderr


def test_developer_toolchain_runner_respects_manifest_override_policy(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )
    _write_runner_context(adopted_root / ".github" / "instructions" / "project-context.instructions.md")

    manifest_path = adopted_root / ".github" / "agent-framework-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["developer_toolchain_runner_contract"]["allow_known_broken_override"] = False
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(adopted_root / "scripts" / "developer_toolchain_runner.py"),
            "--root",
            str(adopted_root),
            "run-surface",
            "--surface",
            "Lint",
            "--allow-known-broken",
        ],
        cwd=adopted_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "disallows known-broken overrides" in result.stderr