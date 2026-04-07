from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "state_sync_pipeline.py"
SPEC = importlib.util.spec_from_file_location("state_sync_pipeline", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

DriftPacketOptions = MODULE.DriftPacketOptions
ProgressReceiptOptions = MODULE.ProgressReceiptOptions
create_progress_receipt = MODULE.create_progress_receipt
upsert_drift_packet = MODULE.upsert_drift_packet


def test_create_progress_receipt_writes_structured_receipt(tmp_path: Path) -> None:
    output_path = create_progress_receipt(
        ProgressReceiptOptions(
            task_id="Template State Sync",
            status="checkpoint_reached",
            progress_unit="review-pass",
            summary="Reached the first checkpoint",
            touched_files="- session_state.md",
            expected_state_effect="- session_state.md: current step updated",
            evidence_links="- pytest tests/test_state_sync_pipeline.py -q",
            notes="- none",
            output_root=tmp_path,
        )
    )

    contents = output_path.read_text(encoding="utf-8")
    assert output_path.name.startswith("0001_")
    assert "checkpoint_reached" in contents
    assert "current step updated" in contents


def test_upsert_drift_packet_writes_reconciliation_fields(tmp_path: Path) -> None:
    output_path = upsert_drift_packet(
        DriftPacketOptions(
            task_id="Template State Sync",
            detected_by="state_sync_audit.py",
            staleness_evidence="- session_state.md lagged behind the receipt",
            surfaces_to_reconcile="- session_state.md\n- ROADMAP.md",
            reconciliation_steps="- update session_state.md\n- rerun the audit",
            reconciliation_receipt_id="receipt-1",
            status="open",
            notes="- keep closeout blocked until resolved",
            output_root=tmp_path,
        )
    )

    contents = output_path.read_text(encoding="utf-8")
    assert output_path.name == "drift_packet.md"
    assert "receipt-1" in contents
    assert "session_state.md" in contents