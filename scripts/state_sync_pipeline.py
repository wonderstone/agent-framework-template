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


def _slugify(value: str) -> str:
    normalized = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "state_sync_task"


def _normalize_block(value: str) -> str:
    text = value.strip()
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


def next_receipt_seq(task_dir: Path) -> int:
    receipts_dir = task_dir / "progress_receipts"
    sequences: list[int] = []
    if receipts_dir.is_dir():
        for path in receipts_dir.glob("*.md"):
            match = re.match(r"(\d+)", path.name)
            if match:
                sequences.append(int(match.group(1)))
    return (max(sequences) + 1) if sequences else 1


@dataclass(frozen=True)
class ProgressReceiptOptions:
    task_id: str
    status: str
    progress_unit: str
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
                summary=args.summary,
                touched_files=args.touched_files,
                expected_state_effect=args.expected_state_effect,
                evidence_links=args.evidence_links,
                notes=args.notes,
                output_root=args.output_root,
                receipt_seq=args.receipt_seq,
            )
        )
    else:
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

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())