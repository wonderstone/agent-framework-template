from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "goal_framing_audit.py"
SPEC = importlib.util.spec_from_file_location("goal_framing_audit", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_detect_kind_does_not_misclassify_prompt_named_with_packet() -> None:
    path = REPO_ROOT / "tmp" / "fake_packet_prompt.md"
    kind = MODULE.detect_kind(path, "Prompt text only\n")

    assert kind == "unknown"


def test_goal_framing_audit_passes_on_core_templates() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "templates/git_audit_task_packet.template.md",
            "templates/git_audit_receipt.template.md",
            "templates/execution_progress_receipt.template.md",
            "templates/managed_terminal_prompt_dispatch_receipt.template.md",
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "PASS templates/git_audit_task_packet.template.md: packet" in completed.stdout
    assert "PASS templates/git_audit_receipt.template.md: receipt" in completed.stdout