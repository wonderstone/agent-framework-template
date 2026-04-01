from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "runtime_surface_guardrails.py"
SPEC = importlib.util.spec_from_file_location("runtime_surface_guardrails", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

run_guard_mode = MODULE.run_guard_mode


def write_registry(tmp_path: Path, command: str) -> Path:
    registry = tmp_path / ".github" / "runtime_surface_registry.py"
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(
        "SURFACES = [\n"
        "    {\n"
        "        'name': 'primary',\n"
        "        'exposure': 'active_default_user_path',\n"
        "        'trigger_prefixes': ('src/',),\n"
        "        'protected_source_roots': ('src/',),\n"
        "        'banned_phrases': ('PLACEHOLDER_RESPONSE_MARKER',),\n"
        f"        'focused_tests': ({command!r},),\n"
        "        'live_commands': (),\n"
        "    },\n"
        "]\n",
        encoding="utf-8",
    )
    return registry


def test_runtime_guard_finds_banned_phrase(tmp_path: Path) -> None:
    source = tmp_path / "src" / "handler.py"
    source.parent.mkdir(parents=True)
    source.write_text("PLACEHOLDER_RESPONSE_MARKER\n", encoding="utf-8")
    registry = write_registry(tmp_path, "python -c \"raise SystemExit(0)\"")

    findings = run_guard_mode(
        root=tmp_path,
        registry_path=registry,
        mode="staged-check",
        changed_paths=["src/handler.py"],
    )

    assert any("banned phrase" in finding.detail for finding in findings)
    assert any(finding.blocking for finding in findings)


def test_runtime_guard_runs_focused_commands(tmp_path: Path) -> None:
    source = tmp_path / "src" / "handler.py"
    source.parent.mkdir(parents=True)
    source.write_text("canonical output\n", encoding="utf-8")
    registry = write_registry(tmp_path, "python -c \"raise SystemExit(0)\"")

    findings = run_guard_mode(
        root=tmp_path,
        registry_path=registry,
        mode="staged-check",
        changed_paths=["src/handler.py"],
    )

    assert findings == []


def test_candidate_audit_warns_without_blocking(tmp_path: Path) -> None:
    registry = tmp_path / ".github" / "runtime_surface_registry.py"
    registry.parent.mkdir(parents=True, exist_ok=True)
    service = tmp_path / "services" / "incubator" / "worker.py"
    service.parent.mkdir(parents=True)
    service.write_text("CANDIDATE_MARKER\n", encoding="utf-8")
    registry.write_text(
        "SURFACES = [\n"
        "    {\n"
        "        'name': 'candidate',\n"
        "        'exposure': 'candidate_incubator_service',\n"
        "        'trigger_prefixes': ('services/incubator/',),\n"
        "        'protected_source_roots': ('services/incubator/',),\n"
        "        'banned_phrases': ('CANDIDATE_MARKER',),\n"
        "        'focused_tests': (),\n"
        "        'live_commands': (),\n"
        "    },\n"
        "]\n",
        encoding="utf-8",
    )

    findings = run_guard_mode(
        root=tmp_path,
        registry_path=registry,
        mode="candidate-audit",
        changed_paths=["services/incubator/worker.py"],
    )

    assert findings
    assert all(not finding.blocking for finding in findings)