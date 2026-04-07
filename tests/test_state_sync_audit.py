from __future__ import annotations

import importlib.util
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "state_sync_audit.py"
SPEC = importlib.util.spec_from_file_location("state_sync_audit", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

StateSyncIssue = MODULE.StateSyncIssue
audit_diff = MODULE.audit_diff
audit_repo = MODULE.audit_repo


def test_audit_repo_reports_missing_progress_receipt_for_active_task(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    session_state = repo_copy / "session_state.md"
    session_state.write_text(
        session_state.read_text(encoding="utf-8").replace(
            "**Active Task ID**: none",
            "**Active Task ID**: demo_state_sync_task",
        ).replace(
            "**Current Step**: No active work.",
            "**Current Step**: Implement the checkpoint contract.",
        ),
        encoding="utf-8",
    )

    issues = audit_repo(repo_copy)

    assert any(issue.kind == "missing-progress-receipt" for issue in issues)


def test_audit_repo_reports_unresolved_drift_packet(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    packet = repo_copy / "tmp" / "git_audit" / "demo_state_sync_task" / "drift_packet.md"
    packet.parent.mkdir(parents=True, exist_ok=True)
    packet.write_text(
        "# Drift Reconciliation Packet\n\n- Status: open\n",
        encoding="utf-8",
    )

    issues = audit_repo(repo_copy)

    assert StateSyncIssue(
        "unresolved-drift-packet",
        "tmp/git_audit/demo_state_sync_task/drift_packet.md: unresolved drift must be reconciled before closeout or next-stage dispatch",
    ) in issues


def test_audit_diff_reports_unsynced_progress_receipt() -> None:
    diff_text = """diff --git a/tmp/git_audit/demo_task/progress_receipts/0001_started.md b/tmp/git_audit/demo_task/progress_receipts/0001_started.md
+++ b/tmp/git_audit/demo_task/progress_receipts/0001_started.md
@@
+- Status: checkpoint_reached
"""

    issues = audit_diff(diff_text)

    assert any(issue.kind == "unsynced-progress-receipt" for issue in issues)


def test_audit_diff_reports_roadmap_completion_without_artifact() -> None:
    diff_text = """diff --git a/ROADMAP.md b/ROADMAP.md
+++ b/ROADMAP.md
@@
+| Ship anti-drift sync audit | ✅ 2026-04-08 |
"""

    issues = audit_diff(diff_text)

    assert any(issue.kind == "roadmap-completion-without-artifact" for issue in issues)