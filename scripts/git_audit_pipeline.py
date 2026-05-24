#!/usr/bin/env python3
"""Generate resumable git audit packet, receipt, and handoff assets."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from goal_framing_audit import audit_file


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = REPO_ROOT / "templates"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "tmp" / "git_audit"


def _slugify(value: str) -> str:
    normalized = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "git_audit_task"


def _normalize_block(value: str) -> str:
    text = value.replace("\\n", "\n").strip()
    return text or "- none"


def render_template(template_text: str, values: dict[str, str]) -> str:
    rendered = template_text
    for key, value in values.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    return rendered


def build_task_dir(task_id: str, output_root: Path) -> Path:
    return output_root / _slugify(task_id)


def load_template(template_name: str) -> str:
    return (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")


def write_rendered_file(output_path: Path, contents: str) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(contents.rstrip() + "\n", encoding="utf-8")
    return output_path


def _warn_legacy_cli_aliases(argv: list[str]) -> None:
    legacy_messages = {
        "--phase-plan": "legacy argument --phase-plan is deprecated; use --phase",
        "--step-contribution": "legacy argument --step-contribution is deprecated and ignored; fold rationale into --phase, --summary, or --notes",
        "--progress-state": "legacy argument --progress-state is deprecated and ignored; use --current-step and --total-steps",
    }
    for arg, message in legacy_messages.items():
        if arg in argv:
            print(f"warning: {message}", file=sys.stderr)


def _audit_generated_artifact(path: Path, *, canonical_only: bool) -> None:
    result = audit_file(path, canonical_only=canonical_only)
    if result.kind == "unknown":
        raise SystemExit(f"generated artifact has unknown audit kind: {path}")
    for warning in result.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    if result.missing:
        missing = ", ".join(result.missing)
        raise SystemExit(f"generated artifact failed goal-framing audit for {path}: missing {missing}")


@dataclass(frozen=True)
class TaskPacketOptions:
    task_id: str
    goal: str
    phase: str
    current_step: str
    total_steps: str
    truth_sources: str
    allowed_files: str
    do_not_touch: str
    validation: str
    acceptance_boundary: str
    owner: str
    executor_plan: str
    notes: str
    output_root: Path
    start_here: str = "- Read the declared truth sources first"
    progress_unit: str = "- none"
    checkpoint_rule: str = "- none"
    truth_surfaces: str = "- none"
    state_sync_schedule: str = "- none"
    closeout_boundary: str = "- none"


@dataclass(frozen=True)
class ReceiptOptions:
    task_id: str
    executor: str
    status: str
    goal: str
    phase: str
    current_step: str
    total_steps: str
    summary: str
    touched_files: str
    validation: str
    risks: str
    handoff_note: str
    output_root: Path


@dataclass(frozen=True)
class HandoffOptions:
    task_id: str
    next_executor: str
    goal: str
    phase: str
    current_step: str
    total_steps: str
    reason: str
    resume_point: str
    blocked_by: str
    recheck_before_continue: str
    notes: str
    output_root: Path


def create_task_packet(options: TaskPacketOptions) -> Path:
    template = load_template("git_audit_task_packet.template.md")
    output_path = build_task_dir(options.task_id, options.output_root) / "task_packet.md"
    contents = render_template(
        template,
        {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "task_id": options.task_id,
            "owner": options.owner,
            "executor_plan": options.executor_plan,
            "start_here": _normalize_block(options.start_here),
            "goal": options.goal,
            "phase": _normalize_block(options.phase),
            "current_step": _normalize_block(options.current_step),
            "total_steps": _normalize_block(options.total_steps),
            "truth_sources": _normalize_block(options.truth_sources),
            "allowed_files": _normalize_block(options.allowed_files),
            "do_not_touch": _normalize_block(options.do_not_touch),
            "validation": _normalize_block(options.validation),
            "acceptance_boundary": _normalize_block(options.acceptance_boundary),
            "progress_unit": options.progress_unit.strip() or "- none",
            "checkpoint_rule": options.checkpoint_rule.strip() or "- none",
            "truth_surfaces": options.truth_surfaces.strip() or "- none",
            "state_sync_schedule": options.state_sync_schedule.strip() or "- none",
            "closeout_boundary": options.closeout_boundary.strip() or "- none",
            "notes": _normalize_block(options.notes),
        },
    )
    return write_rendered_file(output_path, contents)


def create_receipt(options: ReceiptOptions) -> Path:
    template = load_template("git_audit_receipt.template.md")
    output_path = build_task_dir(options.task_id, options.output_root) / "audit_receipt.md"
    contents = render_template(
        template,
        {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "task_id": options.task_id,
            "executor": options.executor,
            "status": options.status,
            "goal": _normalize_block(options.goal),
            "phase": _normalize_block(options.phase),
            "current_step": _normalize_block(options.current_step),
            "total_steps": _normalize_block(options.total_steps),
            "summary": _normalize_block(options.summary),
            "touched_files": _normalize_block(options.touched_files),
            "validation": _normalize_block(options.validation),
            "risks": _normalize_block(options.risks),
            "handoff_note": _normalize_block(options.handoff_note),
        },
    )
    return write_rendered_file(output_path, contents)


def create_handoff(options: HandoffOptions) -> Path:
    template = load_template("git_audit_handoff_packet.template.md")
    output_path = build_task_dir(options.task_id, options.output_root) / "handoff_packet.md"
    contents = render_template(
        template,
        {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "task_id": options.task_id,
            "next_executor": options.next_executor,
            "goal": _normalize_block(options.goal),
            "phase": _normalize_block(options.phase),
            "current_step": _normalize_block(options.current_step),
            "total_steps": _normalize_block(options.total_steps),
            "reason": options.reason,
            "resume_point": _normalize_block(options.resume_point),
            "blocked_by": _normalize_block(options.blocked_by),
            "recheck_before_continue": _normalize_block(options.recheck_before_continue),
            "notes": _normalize_block(options.notes),
        },
    )
    return write_rendered_file(output_path, contents)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate resumable git audit packet, receipt, and handoff assets"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_task = subparsers.add_parser("init-task", help="Create a task packet")
    init_task.add_argument("--task-id", required=True)
    init_task.add_argument("--goal", required=True)
    init_task.add_argument("--phase", dest="phase")
    init_task.add_argument("--phase-plan", dest="phase")
    init_task.add_argument("--current-step", required=True)
    init_task.add_argument("--total-steps", required=True)
    init_task.add_argument("--step-contribution", default="", help=argparse.SUPPRESS)
    init_task.add_argument("--progress-state", default="", help=argparse.SUPPRESS)
    init_task.add_argument("--truth-sources", required=True)
    init_task.add_argument("--allowed-files", required=True)
    init_task.add_argument("--do-not-touch", required=True)
    init_task.add_argument("--validation", required=True)
    init_task.add_argument("--acceptance-boundary", required=True)
    init_task.add_argument("--owner", default="main-thread")
    init_task.add_argument("--executor-plan", default="planner -> executor -> auditor -> gatekeeper")
    init_task.add_argument("--start-here", default="- Read the declared truth sources first")
    init_task.add_argument("--progress-unit", default="- none")
    init_task.add_argument("--checkpoint-rule", default="- none")
    init_task.add_argument("--truth-surfaces", default="- none")
    init_task.add_argument("--state-sync-schedule", default="- none")
    init_task.add_argument("--closeout-boundary", default="- none")
    init_task.add_argument("--notes", default="- none")
    init_task.add_argument("--skip-audit", action="store_true")
    init_task.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)

    record_receipt = subparsers.add_parser("record-receipt", help="Create an audit receipt")
    record_receipt.add_argument("--task-id", required=True)
    record_receipt.add_argument("--executor", required=True)
    record_receipt.add_argument("--status", required=True)
    record_receipt.add_argument("--goal", required=True)
    record_receipt.add_argument("--phase", dest="phase")
    record_receipt.add_argument("--phase-plan", dest="phase")
    record_receipt.add_argument("--current-step", required=True)
    record_receipt.add_argument("--total-steps", required=True)
    record_receipt.add_argument("--step-contribution", default="", help=argparse.SUPPRESS)
    record_receipt.add_argument("--progress-state", default="", help=argparse.SUPPRESS)
    record_receipt.add_argument("--summary", required=True)
    record_receipt.add_argument("--touched-files", required=True)
    record_receipt.add_argument("--validation", required=True)
    record_receipt.add_argument("--risks", required=True)
    record_receipt.add_argument("--handoff-note", default="- none")
    record_receipt.add_argument("--skip-audit", action="store_true")
    record_receipt.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)

    create_handoff_parser = subparsers.add_parser(
        "create-handoff", help="Create a handoff packet"
    )
    create_handoff_parser.add_argument("--task-id", required=True)
    create_handoff_parser.add_argument("--next-executor", required=True)
    create_handoff_parser.add_argument("--goal", required=True)
    create_handoff_parser.add_argument("--phase", dest="phase")
    create_handoff_parser.add_argument("--phase-plan", dest="phase")
    create_handoff_parser.add_argument("--current-step", required=True)
    create_handoff_parser.add_argument("--total-steps", required=True)
    create_handoff_parser.add_argument("--step-contribution", default="", help=argparse.SUPPRESS)
    create_handoff_parser.add_argument("--progress-state", default="", help=argparse.SUPPRESS)
    create_handoff_parser.add_argument("--reason", required=True)
    create_handoff_parser.add_argument("--resume-point", required=True)
    create_handoff_parser.add_argument("--blocked-by", required=True)
    create_handoff_parser.add_argument("--recheck-before-continue", required=True)
    create_handoff_parser.add_argument("--notes", default="- none")
    create_handoff_parser.add_argument("--skip-audit", action="store_true")
    create_handoff_parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)

    return parser


def _require_phase(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if getattr(args, "phase", None):
        return
    parser.error("the following arguments are required: --phase")


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    _warn_legacy_cli_aliases(sys.argv[1:])

    if args.command == "init-task":
        _require_phase(args, parser)
        output_path = create_task_packet(
            TaskPacketOptions(
                task_id=args.task_id,
                goal=args.goal,
                phase=args.phase,
                current_step=args.current_step,
                total_steps=args.total_steps,
                truth_sources=args.truth_sources,
                allowed_files=args.allowed_files,
                do_not_touch=args.do_not_touch,
                validation=args.validation,
                acceptance_boundary=args.acceptance_boundary,
                owner=args.owner,
                executor_plan=args.executor_plan,
                start_here=args.start_here,
                progress_unit=args.progress_unit,
                checkpoint_rule=args.checkpoint_rule,
                truth_surfaces=args.truth_surfaces,
                state_sync_schedule=args.state_sync_schedule,
                closeout_boundary=args.closeout_boundary,
                notes=args.notes,
                output_root=args.output_root,
            )
        )
    elif args.command == "record-receipt":
        _require_phase(args, parser)
        output_path = create_receipt(
            ReceiptOptions(
                task_id=args.task_id,
                executor=args.executor,
                status=args.status,
                goal=args.goal,
                phase=args.phase,
                current_step=args.current_step,
                total_steps=args.total_steps,
                summary=args.summary,
                touched_files=args.touched_files,
                validation=args.validation,
                risks=args.risks,
                handoff_note=args.handoff_note,
                output_root=args.output_root,
            )
        )
    else:
        _require_phase(args, parser)
        output_path = create_handoff(
            HandoffOptions(
                task_id=args.task_id,
                next_executor=args.next_executor,
                goal=args.goal,
                phase=args.phase,
                current_step=args.current_step,
                total_steps=args.total_steps,
                reason=args.reason,
                resume_point=args.resume_point,
                blocked_by=args.blocked_by,
                recheck_before_continue=args.recheck_before_continue,
                notes=args.notes,
                output_root=args.output_root,
            )
        )

    if not args.skip_audit:
        _audit_generated_artifact(output_path, canonical_only=True)

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())