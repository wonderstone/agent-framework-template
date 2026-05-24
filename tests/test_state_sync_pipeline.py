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
SkillEvolutionOptions = MODULE.SkillEvolutionOptions
TodoSyncOptions = MODULE.TodoSyncOptions
create_progress_receipt = MODULE.create_progress_receipt
sync_skill_evolution = MODULE.sync_skill_evolution
sync_todos = MODULE.sync_todos
upsert_drift_packet = MODULE.upsert_drift_packet


def test_create_progress_receipt_writes_structured_receipt(tmp_path: Path) -> None:
    output_path = create_progress_receipt(
        ProgressReceiptOptions(
            task_id="Template State Sync",
            status="checkpoint_reached",
            progress_unit="review-pass",
            goal="Keep execution checkpoints directional rather than summary-only.",
            phase_plan="1. Freeze task context\n2. Emit checkpoint receipts\n3. Reconcile drift before closeout",
            current_step="2. Emit checkpoint receipts",
            step_contribution="This checkpoint proves the current pass and preserves how it advances the larger task.",
            progress_state="Completed: 1. Freeze task context\nIn Progress: 1. Emit checkpoint receipts\nRemaining: 1. Reconcile drift",
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
    assert "## Goal" in contents
    assert "## Phase Plan" in contents
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


def test_sync_todos_upserts_canonical_todo_section(tmp_path: Path) -> None:
    session_state = tmp_path / "session_state.md"
    session_state.write_text("## Completed This Phase\n\n- (none)\n", encoding="utf-8")

    output_path = sync_todos(
        TodoSyncOptions(
            session_state_path=session_state,
            source_of_truth="session_state.md Todo Sync section; workspace todo list is a mirror only",
            sync_status="in_sync",
            last_synced="2026-04-24",
            todo_items=(),
        )
    )

    contents = output_path.read_text(encoding="utf-8")
    assert "## Todo Sync" in contents
    assert "workspace todo list is a mirror only" in contents


def test_sync_skill_evolution_upserts_startup_check(tmp_path: Path) -> None:
    session_state = tmp_path / "session_state.md"
    session_state.write_text("## Completed This Phase\n\n- (none)\n", encoding="utf-8")

    output_path = sync_skill_evolution(
        SkillEvolutionOptions(
            session_state_path=session_state,
            startup_check="done",
            main_thread_decision="observe_only",
            reason="No repeated pattern worth promotion in this round.",
            human_role="advisory only",
            last_evaluated="2026-04-24",
        )
    )

    contents = output_path.read_text(encoding="utf-8")
    assert "## SKILL Evolution" in contents
    assert "**Main-Thread Decision**: observe_only" in contents