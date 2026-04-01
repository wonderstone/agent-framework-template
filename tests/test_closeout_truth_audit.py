from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "closeout_truth_audit.py"
SPEC = importlib.util.spec_from_file_location("closeout_truth_audit", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

audit_diff = MODULE.audit_diff


def test_closeout_audit_passes_when_no_claims_are_added() -> None:
    diff_text = """diff --git a/README.md b/README.md\n+++ b/README.md\n@@ -1 +1 @@\n+plain documentation update\n"""

    assert audit_diff(diff_text) == []


def test_closeout_audit_fails_without_receipt_anchor() -> None:
    diff_text = """diff --git a/session_state.md b/session_state.md\n+++ b/session_state.md\n@@ -1 +1 @@\n+- task completed\n"""

    issues = audit_diff(diff_text)

    assert issues
    assert "receipt anchor" in issues[0]


def test_closeout_audit_passes_with_receipt_anchor_in_same_diff() -> None:
    diff_text = """diff --git a/session_state.md b/session_state.md\n+++ b/session_state.md\n@@ -1 +1,2 @@\n+- task completed\n+- 15 passed in 0.23s\n"""

    assert audit_diff(diff_text) == []