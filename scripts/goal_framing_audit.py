#!/usr/bin/env python3
"""Audit core execution artifacts for required goal-framing sections."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

CANONICAL_GOAL_FRAMING_HEADERS = (
    ("## Goal",),
    ("## Phase",),
    ("## Current Step",),
    ("## Total Steps",),
)

LEGACY_GOAL_FRAMING_HEADERS = (
    ("## Goal",),
    ("## Phase", "## Phase Plan"),
    ("## Current Step",),
    ("## Total Steps", "## Progress State"),
)

LEGACY_MARKER_NOTES = {
    "## Phase Plan": "legacy heading tolerated during migration; prefer ## Phase",
    "## Progress State": "legacy heading tolerated during migration; prefer ## Total Steps",
    "## Step Contribution": "legacy heading no longer part of the preferred packet contract; fold rationale into Phase, Summary, or Notes",
}

PACKET_HEADERS = LEGACY_GOAL_FRAMING_HEADERS
RECEIPT_HEADERS = LEGACY_GOAL_FRAMING_HEADERS + (("## Summary",),)
DISPATCH_RECEIPT_HEADERS = LEGACY_GOAL_FRAMING_HEADERS + (("## Dispatch Contract",), ("## Result",))
HANDOFF_HEADERS = LEGACY_GOAL_FRAMING_HEADERS + (("## Reason",), ("## Resume Point",), ("## Blocked By",), ("## Recheck Before Continue",))

CANONICAL_PACKET_HEADERS = CANONICAL_GOAL_FRAMING_HEADERS
CANONICAL_RECEIPT_HEADERS = CANONICAL_GOAL_FRAMING_HEADERS + (("## Summary",),)
CANONICAL_DISPATCH_RECEIPT_HEADERS = CANONICAL_GOAL_FRAMING_HEADERS + (("## Dispatch Contract",), ("## Result",))
CANONICAL_HANDOFF_HEADERS = CANONICAL_GOAL_FRAMING_HEADERS + (("## Reason",), ("## Resume Point",), ("## Blocked By",), ("## Recheck Before Continue",))


@dataclass(frozen=True)
class AuditResult:
    path: Path
    kind: str
    missing: tuple[str, ...]
    warnings: tuple[str, ...]


def detect_kind(path: Path, contents: str) -> str:
    lowered_name = path.name.lower()
    stripped = contents.lstrip()
    if lowered_name in {
        "git_audit_task_packet.template.md",
        "task_packet.md",
        "evaluation_request.template.md",
        "adoption_verification_packet.template.md",
        "review_dispatch_packet.template.md",
    }:
        return "packet"
    if lowered_name in {"git_audit_handoff_packet.template.md", "handoff_packet.md"}:
        return "handoff"
    if lowered_name in {
        "execution_progress_receipt.template.md",
        "git_audit_receipt.template.md",
        "audit_receipt.md",
        "evaluation_report.template.md",
    }:
        return "receipt"
    if lowered_name == "managed_terminal_prompt_dispatch_receipt.template.md":
        return "dispatch_receipt"
    if stripped.startswith("# Git Audit Task Packet"):
        return "packet"
    if stripped.startswith("# Independent Evaluation Request"):
        return "packet"
    if stripped.startswith("# Strict Adoption Verification Packet"):
        return "packet"
    if stripped.startswith("# Executor Review Dispatch Packet"):
        return "packet"
    if stripped.startswith("# Git Audit Handoff Packet"):
        return "handoff"
    if stripped.startswith("# Execution Progress Receipt") or stripped.startswith("# Git Audit Receipt"):
        return "receipt"
    if stripped.startswith("# Independent Evaluation Report"):
        return "receipt"
    if stripped.startswith("# Managed Terminal Prompt Dispatch Receipt"):
        return "dispatch_receipt"
    return "unknown"


def marker_groups(kind: str, canonical_only: bool) -> tuple[tuple[str, ...], ...]:
    if kind == "packet":
        return CANONICAL_PACKET_HEADERS if canonical_only else PACKET_HEADERS
    if kind == "handoff":
        return CANONICAL_HANDOFF_HEADERS if canonical_only else HANDOFF_HEADERS
    if kind == "receipt":
        return CANONICAL_RECEIPT_HEADERS if canonical_only else RECEIPT_HEADERS
    if kind == "dispatch_receipt":
        return CANONICAL_DISPATCH_RECEIPT_HEADERS if canonical_only else DISPATCH_RECEIPT_HEADERS
    return ()


def audit_file(path: Path, canonical_only: bool = False) -> AuditResult:
    contents = path.read_text(encoding="utf-8")
    kind = detect_kind(path, contents)
    groups = marker_groups(kind, canonical_only)
    missing = tuple(" | ".join(group) for group in groups if not any(marker in contents for marker in group))
    warnings = tuple(note for marker, note in LEGACY_MARKER_NOTES.items() if marker in contents)
    return AuditResult(path=path, kind=kind, missing=missing, warnings=warnings)


def iter_targets(paths: list[Path]) -> list[Path]:
    collected: list[Path] = []
    for path in paths:
        if path.is_dir():
            collected.extend(sorted(p for p in path.rglob("*.md") if p.is_file()))
            continue
        collected.append(path)
    return collected


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit core execution artifacts for required goal-framing markers")
    parser.add_argument("paths", nargs="+", help="Files or directories to audit")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on unknown markdown kinds in addition to missing markers",
    )
    parser.add_argument(
        "--canonical-only",
        action="store_true",
        help="Require canonical goal-framing headings instead of tolerating legacy migration aliases",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    targets = iter_targets(
        [(REPO_ROOT / raw_path).resolve() if not raw_path.startswith("/") else Path(raw_path) for raw_path in args.paths]
    )

    failures: list[AuditResult] = []
    unknowns: list[Path] = []
    for path in targets:
        result = audit_file(path, canonical_only=args.canonical_only)
        relative = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        if result.kind == "unknown":
            print(f"SKIP {relative}: unknown artifact kind")
            if args.strict:
                unknowns.append(path)
            continue
        for warning in result.warnings:
            print(f"WARN {relative}: {warning}")
        if result.missing:
            print(f"FAIL {relative}: missing {', '.join(result.missing)}")
            failures.append(result)
            continue
        print(f"PASS {relative}: {result.kind}")

    if failures or unknowns:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())