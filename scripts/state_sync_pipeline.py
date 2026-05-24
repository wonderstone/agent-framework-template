#!/usr/bin/env python3
"""Generate progress receipts and drift reconciliation packets for state sync."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = REPO_ROOT / "templates"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "tmp" / "git_audit"
TODO_SECTION_HEADING = "Todo Sync"
TODO_STATUS_MARKERS = {
    "pending": " ",
    "in_progress": "-",
    "completed": "x",
}
SKILL_EVOLUTION_SECTION_HEADING = "SKILL Evolution"
SKILL_EVOLUTION_STARTUP_CHECKS = {"done", "pending", "n/a"}
SKILL_EVOLUTION_DECISIONS = {
    "observe_only",
    "invocation_required",
    "candidate_review",
    "promotion_review",
    "n/a",
}


def _slugify(value: str) -> str:
    normalized = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "state_sync_task"


def _normalize_block(value: str) -> str:
    text = value.strip()
    return text or "- none"


def _today_utc_date() -> str:
    return datetime.now(timezone.utc).date().isoformat()


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


def next_receipt_seq(task_dir: Path) -> int:
    receipts_dir = task_dir / "progress_receipts"
    sequences: list[int] = []
    if receipts_dir.is_dir():
        for path in receipts_dir.glob("*.md"):
            match = re.match(r"(\d+)", path.name)
            if match:
                sequences.append(int(match.group(1)))
    return (max(sequences) + 1) if sequences else 1


def _extract_markdown_section(text: str, heading: str) -> str | None:
    heading_match = re.search(rf"^## {re.escape(heading)}\s*$", text, flags=re.MULTILINE)
    if heading_match is None:
        return None
    start = heading_match.start()
    next_heading = re.search(r"^## ", text[heading_match.end() :], flags=re.MULTILINE)
    if next_heading is None:
        return text[start:]
    return text[start : heading_match.end() + next_heading.start()]


def _upsert_markdown_section(text: str, heading: str, body: str, *, insert_before: str) -> str:
    replacement = f"## {heading}\n\n{body.strip()}\n\n---\n\n"
    existing = _extract_markdown_section(text, heading)
    if existing is not None:
        return text.replace(existing, replacement, 1)

    anchor = re.search(rf"^## {re.escape(insert_before)}\s*$", text, flags=re.MULTILINE)
    if anchor is not None:
        return text[: anchor.start()] + replacement + text[anchor.start() :]

    suffix = "" if text.endswith("\n") else "\n"
    return text + suffix + "\n" + replacement


@dataclass(frozen=True)
class ProgressReceiptOptions:
    task_id: str
    status: str
    progress_unit: str
    goal: str
    phase_plan: str
    current_step: str
    step_contribution: str
    progress_state: str
    summary: str
    touched_files: str
    expected_state_effect: str
    evidence_links: str
    notes: str
    output_root: Path
    receipt_seq: int | None = None


@dataclass(frozen=True)
class DriftPacketOptions:
    task_id: str
    detected_by: str
    staleness_evidence: str
    surfaces_to_reconcile: str
    reconciliation_steps: str
    reconciliation_receipt_id: str
    status: str
    notes: str
    output_root: Path


@dataclass(frozen=True)
class TodoItem:
    status: str
    title: str


@dataclass(frozen=True)
class TodoSyncOptions:
    session_state_path: Path
    source_of_truth: str
    sync_status: str
    last_synced: str
    todo_items: tuple[TodoItem, ...]


@dataclass(frozen=True)
class SkillEvolutionOptions:
    session_state_path: Path
    startup_check: str
    main_thread_decision: str
    reason: str
    human_role: str
    last_evaluated: str


def _render_todo_items(todo_items: tuple[TodoItem, ...]) -> str:
    if not todo_items:
        return "- (none)"

    lines: list[str] = []
    for item in todo_items:
        marker = TODO_STATUS_MARKERS[item.status]
        lines.append(f"- [{marker}] {item.title}")
    return "\n".join(lines)


def sync_todos(options: TodoSyncOptions) -> Path:
    session_state = options.session_state_path.read_text(encoding="utf-8")
    todo_body = (
        f"**Source of Truth**: {options.source_of_truth}\n\n"
        f"**Sync Status**: {options.sync_status}\n\n"
        f"**Last Synced**: {options.last_synced}\n\n"
        f"{_render_todo_items(options.todo_items)}"
    )
    updated = _upsert_markdown_section(
        session_state,
        TODO_SECTION_HEADING,
        todo_body,
        insert_before="Completed This Phase",
    )
    options.session_state_path.write_text(updated.rstrip() + "\n", encoding="utf-8")
    return options.session_state_path


def sync_skill_evolution(options: SkillEvolutionOptions) -> Path:
    session_state = options.session_state_path.read_text(encoding="utf-8")
    skill_body = (
        f"**Startup Check**: {options.startup_check}\n\n"
        f"**Main-Thread Decision**: {options.main_thread_decision}\n\n"
        f"**Reason**: {options.reason}\n\n"
        f"**Human Role**: {options.human_role}\n\n"
        f"**Last Evaluated**: {options.last_evaluated}"
    )
    updated = _upsert_markdown_section(
        session_state,
        SKILL_EVOLUTION_SECTION_HEADING,
        skill_body,
        insert_before="Completed This Phase",
    )
    options.session_state_path.write_text(updated.rstrip() + "\n", encoding="utf-8")
    return options.session_state_path


def _parse_todo_arg(raw_value: str) -> TodoItem:
    if ":" not in raw_value:
        raise argparse.ArgumentTypeError(
            "todo entries must use the format 'pending:title', 'in_progress:title', or 'completed:title'"
        )
    status, title = raw_value.split(":", 1)
    normalized_status = status.strip().lower()
    if normalized_status not in TODO_STATUS_MARKERS:
        raise argparse.ArgumentTypeError(
            "todo status must be one of: pending, in_progress, completed"
        )
    normalized_title = title.strip()
    if not normalized_title:
        raise argparse.ArgumentTypeError("todo title must not be empty")
    return TodoItem(status=normalized_status, title=normalized_title)


def create_progress_receipt(options: ProgressReceiptOptions) -> Path:
    template = load_template("execution_progress_receipt.template.md")
    task_dir = build_task_dir(options.task_id, options.output_root)
    receipt_seq = options.receipt_seq or next_receipt_seq(task_dir)
    status_slug = _slugify(options.status)
    output_path = task_dir / "progress_receipts" / f"{receipt_seq:04d}_{status_slug}.md"
    contents = render_template(
        template,
        {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "task_id": options.task_id,
            "receipt_seq": str(receipt_seq),
            "status": options.status,
            "progress_unit": options.progress_unit,
            "goal": _normalize_block(options.goal),
            "phase_plan": _normalize_block(options.phase_plan),
            "current_step": _normalize_block(options.current_step),
            "step_contribution": _normalize_block(options.step_contribution),
            "progress_state": _normalize_block(options.progress_state),
            "summary": _normalize_block(options.summary),
            "touched_files": _normalize_block(options.touched_files),
            "expected_state_effect": _normalize_block(options.expected_state_effect),
            "evidence_links": _normalize_block(options.evidence_links),
            "notes": _normalize_block(options.notes),
        },
    )
    return write_rendered_file(output_path, contents)


def upsert_drift_packet(options: DriftPacketOptions) -> Path:
    template = load_template("drift_reconciliation_packet.template.md")
    output_path = build_task_dir(options.task_id, options.output_root) / "drift_packet.md"
    contents = render_template(
        template,
        {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "task_id": options.task_id,
            "detected_by": options.detected_by,
            "reconciliation_receipt_id": options.reconciliation_receipt_id,
            "status": options.status,
            "staleness_evidence": _normalize_block(options.staleness_evidence),
            "surfaces_to_reconcile": _normalize_block(options.surfaces_to_reconcile),
            "reconciliation_steps": _normalize_block(options.reconciliation_steps),
            "notes": _normalize_block(options.notes),
        },
    )
    return write_rendered_file(output_path, contents)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate progress receipts and drift reconciliation packets"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    record_progress = subparsers.add_parser("record-progress", help="Create a progress receipt")
    record_progress.add_argument("--task-id", required=True)
    record_progress.add_argument("--status", required=True)
    record_progress.add_argument("--progress-unit", required=True)
    record_progress.add_argument("--goal", required=True)
    record_progress.add_argument("--phase-plan", required=True)
    record_progress.add_argument("--current-step", required=True)
    record_progress.add_argument("--step-contribution", required=True)
    record_progress.add_argument("--progress-state", required=True)
    record_progress.add_argument("--summary", required=True)
    record_progress.add_argument("--touched-files", required=True)
    record_progress.add_argument("--expected-state-effect", required=True)
    record_progress.add_argument("--evidence-links", required=True)
    record_progress.add_argument("--notes", default="- none")
    record_progress.add_argument("--receipt-seq", type=int)
    record_progress.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)

    upsert_drift = subparsers.add_parser("upsert-drift", help="Create or update a drift packet")
    upsert_drift.add_argument("--task-id", required=True)
    upsert_drift.add_argument("--detected-by", required=True)
    upsert_drift.add_argument("--staleness-evidence", required=True)
    upsert_drift.add_argument("--surfaces-to-reconcile", required=True)
    upsert_drift.add_argument("--reconciliation-steps", required=True)
    upsert_drift.add_argument("--reconciliation-receipt-id", default="- none")
    upsert_drift.add_argument("--status", default="open")
    upsert_drift.add_argument("--notes", default="- none")
    upsert_drift.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)

    sync_todos_parser = subparsers.add_parser(
        "sync-todos",
        help="Upsert the Todo Sync section in session_state.md",
    )
    sync_todos_parser.add_argument(
        "--session-state-path",
        type=Path,
        default=REPO_ROOT / "session_state.md",
    )
    sync_todos_parser.add_argument("--source-of-truth", required=True)
    sync_todos_parser.add_argument(
        "--sync-status",
        default="in_sync",
        choices=["in_sync", "needs_refresh", "n/a"],
    )
    sync_todos_parser.add_argument("--last-synced", default=_today_utc_date())
    sync_todos_parser.add_argument(
        "--todo",
        action="append",
        default=[],
        type=_parse_todo_arg,
        help="todo entry in the format 'status:title'",
    )

    sync_skill_parser = subparsers.add_parser(
        "sync-skill-evolution",
        help="Upsert the SKILL Evolution section in session_state.md",
    )
    sync_skill_parser.add_argument(
        "--session-state-path",
        type=Path,
        default=REPO_ROOT / "session_state.md",
    )
    sync_skill_parser.add_argument(
        "--startup-check",
        required=True,
        choices=sorted(SKILL_EVOLUTION_STARTUP_CHECKS),
    )
    sync_skill_parser.add_argument(
        "--main-thread-decision",
        required=True,
        choices=sorted(SKILL_EVOLUTION_DECISIONS),
    )
    sync_skill_parser.add_argument("--reason", required=True)
    sync_skill_parser.add_argument("--human-role", default="advisory only")
    sync_skill_parser.add_argument("--last-evaluated", default=_today_utc_date())

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "record-progress":
        output_path = create_progress_receipt(
            ProgressReceiptOptions(
                task_id=args.task_id,
                status=args.status,
                progress_unit=args.progress_unit,
                goal=args.goal,
                phase_plan=args.phase_plan,
                current_step=args.current_step,
                step_contribution=args.step_contribution,
                progress_state=args.progress_state,
                summary=args.summary,
                touched_files=args.touched_files,
                expected_state_effect=args.expected_state_effect,
                evidence_links=args.evidence_links,
                notes=args.notes,
                output_root=args.output_root,
                receipt_seq=args.receipt_seq,
            )
        )
    elif args.command == "upsert-drift":
        output_path = upsert_drift_packet(
            DriftPacketOptions(
                task_id=args.task_id,
                detected_by=args.detected_by,
                staleness_evidence=args.staleness_evidence,
                surfaces_to_reconcile=args.surfaces_to_reconcile,
                reconciliation_steps=args.reconciliation_steps,
                reconciliation_receipt_id=args.reconciliation_receipt_id,
                status=args.status,
                notes=args.notes,
                output_root=args.output_root,
            )
        )
    elif args.command == "sync-todos":
        output_path = sync_todos(
            TodoSyncOptions(
                session_state_path=args.session_state_path,
                source_of_truth=args.source_of_truth,
                sync_status=args.sync_status,
                last_synced=args.last_synced,
                todo_items=tuple(args.todo),
            )
        )
    else:
        output_path = sync_skill_evolution(
            SkillEvolutionOptions(
                session_state_path=args.session_state_path,
                startup_check=args.startup_check,
                main_thread_decision=args.main_thread_decision,
                reason=args.reason,
                human_role=args.human_role,
                last_evaluated=args.last_evaluated,
            )
        )

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())