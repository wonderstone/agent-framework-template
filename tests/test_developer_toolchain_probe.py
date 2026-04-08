from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_MODULE_PATH = REPO_ROOT / "scripts" / "bootstrap_adoption.py"
BOOTSTRAP_SPEC = importlib.util.spec_from_file_location("bootstrap_adoption_for_probe", BOOTSTRAP_MODULE_PATH)
assert BOOTSTRAP_SPEC is not None
assert BOOTSTRAP_SPEC.loader is not None
BOOTSTRAP_MODULE = importlib.util.module_from_spec(BOOTSTRAP_SPEC)
sys.modules[BOOTSTRAP_SPEC.name] = BOOTSTRAP_MODULE
BOOTSTRAP_SPEC.loader.exec_module(BOOTSTRAP_MODULE)

bootstrap_repo = BOOTSTRAP_MODULE.bootstrap_repo


def _write_probe_context(project_context_path: Path) -> None:
    project_context_path.write_text(
        """# Probe Context\n\n## Developer Toolchain\n\n| Surface | Command or source | Scope | Status | Fallback or stop | Notes |\n|---|---|---|---|---|---|\n| Diagnostics | `python -c \"print('diag ok')\"` | `module` | `verified-working` | Stop | Smoke diagnostics |\n| Build | `python -c \"import sys; sys.exit(2)\"` | `module` | `verified-working` | Stop | Intentional failure |\n| Health or smoke | `none` | `service` | `not-applicable` | Stop | No smoke command |\n| Lint | `python -c \"print('known broken')\"` | `file` | `known-broken` | Stop | Explicitly broken |\n""",
        encoding="utf-8",
    )


def test_developer_toolchain_probe_records_success_failure_and_skip(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )
    _write_probe_context(adopted_root / ".github" / "instructions" / "project-context.instructions.md")

    output_path = adopted_root / "tmp" / "probe" / "receipt.md"
    result = subprocess.run(
        [
            sys.executable,
            str(adopted_root / "scripts" / "developer_toolchain_probe.py"),
            "--root",
            str(adopted_root),
            "--output",
            str(output_path),
        ],
        cwd=adopted_root,
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.strip() == str(output_path)
    rendered = output_path.read_text(encoding="utf-8")
    assert "| Diagnostics | module | verified-working | success | 0 |" in rendered
    assert "| Build | module | verified-working | failure | 2 |" in rendered
    assert "| Health or smoke | service | not-applicable | not-applicable | n/a |" in rendered
    assert "| Lint | file | known-broken | skipped-known-broken | n/a |" in rendered


def test_developer_toolchain_probe_respects_surface_selection(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )
    _write_probe_context(adopted_root / ".github" / "instructions" / "project-context.instructions.md")

    output_path = adopted_root / "tmp" / "probe" / "receipt.md"
    subprocess.run(
        [
            sys.executable,
            str(adopted_root / "scripts" / "developer_toolchain_probe.py"),
            "--root",
            str(adopted_root),
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

    rendered = output_path.read_text(encoding="utf-8")
    assert "| Diagnostics | module | verified-working | success | 0 |" in rendered
    assert "| Build |" not in rendered
