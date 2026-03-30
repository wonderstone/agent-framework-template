from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "git_audit_pipeline.py"
SPEC = importlib.util.spec_from_file_location("git_audit_pipeline", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

HandoffOptions = MODULE.HandoffOptions
ReceiptOptions = MODULE.ReceiptOptions
TaskPacketOptions = MODULE.TaskPacketOptions
build_task_dir = MODULE.build_task_dir
create_handoff = MODULE.create_handoff
create_receipt = MODULE.create_receipt
create_task_packet = MODULE.create_task_packet
render_template = MODULE.render_template


def test_render_template_replaces_known_placeholders() -> None:
    template = "Task {{task_id}} owned by {{owner}}"

    rendered = render_template(template, {"task_id": "audit-1", "owner": "main-thread"})

    assert rendered == "Task audit-1 owned by main-thread"


def test_create_task_packet_writes_markdown_from_template(tmp_path: Path) -> None:
    output_path = create_task_packet(
        TaskPacketOptions(
            task_id="Template Audit 01",
            goal="Freeze scope before external review",
            truth_sources="- docs/runbooks/resumable-git-audit-pipeline.md",
            allowed_files="- docs/**\n- scripts/git_audit_pipeline.py",
            do_not_touch="- .env",
            validation="- bash scripts/validate-template.sh",
            acceptance_boundary="- task packet exists",
            owner="main-thread",
            executor_plan="planner -> executor -> auditor -> gatekeeper",
            notes="- start with canonical docs",
            output_root=tmp_path,
        )
    )

    assert output_path == build_task_dir("Template Audit 01", tmp_path) / "task_packet.md"
    contents = output_path.read_text(encoding="utf-8")
    assert "Template Audit 01" in contents
    assert "Freeze scope before external review" in contents


def test_create_receipt_writes_summary_validation_and_risks(tmp_path: Path) -> None:
    output_path = create_receipt(
        ReceiptOptions(
            task_id="Template Audit 01",
            executor="external-codex",
            status="completed",
            summary="Added runbook and script",
            touched_files="- docs/runbooks/resumable-git-audit-pipeline.md",
            validation="- pytest tests/test_git_audit_pipeline.py -q",
            risks="- main thread still needs owner review",
            handoff_note="- do not close out without hard gates",
            output_root=tmp_path,
        )
    )

    contents = output_path.read_text(encoding="utf-8")
    assert "external-codex" in contents
    assert "Added runbook and script" in contents
    assert "main thread still needs owner review" in contents


def test_create_handoff_writes_resume_point_and_recheck_list(tmp_path: Path) -> None:
    output_path = create_handoff(
        HandoffOptions(
            task_id="Template Audit 01",
            next_executor="main-thread",
            reason="CLI session ended",
            resume_point="- review packet\n- rerun focused validation",
            blocked_by="- external reviewer token exhaustion",
            recheck_before_continue="- confirm validate-template.sh still passes",
            notes="- keep allowed-files scope frozen",
            output_root=tmp_path,
        )
    )

    contents = output_path.read_text(encoding="utf-8")
    assert "CLI session ended" in contents
    assert "confirm validate-template.sh still passes" in contents
    assert "keep allowed-files scope frozen" in contents