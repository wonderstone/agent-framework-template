#!/usr/bin/env python3
"""Unified governance audit and goal-framing migration helpers for the template repo."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from goal_framing_audit import REPO_ROOT, audit_file, iter_targets
from boundary_report_audit import audit_file as audit_boundary, iter_targets as iter_boundary_targets


LEGACY_HEADING_PHASE = "## Phase Plan"
LEGACY_HEADING_PROGRESS = "## Progress State"
LEGACY_HEADING_STEP_CONTRIBUTION = "## Step Contribution"
CANONICAL_HEADING_PHASE = "## Phase"
CANONICAL_HEADING_TOTAL_STEPS = "## Total Steps"
NOTES_HEADING = "## Notes"


@dataclass(frozen=True)
class MigrationResult:
    path: Path
    changed: bool
    warnings: tuple[str, ...]


def _count_ordered_items(section_body: str) -> int | None:
    count = len(re.findall(r"(?m)^\d+\.\s+", section_body))
    return count or None


def _extract_section(contents: str, heading: str) -> tuple[str | None, int, int]:
    pattern = re.compile(rf"(?ms)^({re.escape(heading)}\n\n)(.*?)(?=^##\s|\Z)")
    match = pattern.search(contents)
    if not match:
        return None, -1, -1
    return match.group(2).rstrip(), match.start(), match.end()


def _normalize_glued_legacy_headings(contents: str) -> str:
    return re.sub(
        r"([^\n])(##\s+(?:Phase Plan|Progress State|Step Contribution))",
        r"\1\n\n\2",
        contents,
    )


def _replace_section(contents: str, old_heading: str, new_heading: str) -> str:
    return contents.replace(old_heading, new_heading, 1)


def _append_or_merge_notes(contents: str, title: str, body: str) -> str:
    block = f"{title}:\n\n{body.strip()}" if body.strip() else title
    notes_body, start, end = _extract_section(contents, NOTES_HEADING)
    if notes_body is None:
        return contents.rstrip() + f"\n\n{NOTES_HEADING}\n\n{block}\n"
    merged = notes_body.rstrip()
    if merged:
        merged = merged + "\n\n"
    merged += block
    return contents[:start] + f"{NOTES_HEADING}\n\n{merged}\n" + contents[end:]


def _remove_section(contents: str, heading: str) -> tuple[str, str | None]:
    body, start, end = _extract_section(contents, heading)
    if body is None:
        return contents, None
    while start > 0 and contents[start - 1] == "\n":
        start -= 1
        if start > 0 and contents[start - 1] == "\n":
            continue
        break
    return contents[:start] + contents[end:].lstrip("\n"), body


def _derive_total_steps(contents: str) -> str | None:
    match = re.search(r"Step\s+\d+\s+of\s+(\d+)", contents, re.IGNORECASE)
    if match:
        return match.group(1)
    phase_body, _, _ = _extract_section(contents, CANONICAL_HEADING_PHASE)
    if phase_body is None:
        phase_body, _, _ = _extract_section(contents, LEGACY_HEADING_PHASE)
    if phase_body:
        count = _count_ordered_items(phase_body)
        if count:
            return str(count)
    return None


def _insert_total_steps(contents: str, total_steps: str) -> str:
    current_step_body, _, end = _extract_section(contents, "## Current Step")
    if current_step_body is None:
        return contents
    insertion = f"\n\n{CANONICAL_HEADING_TOTAL_STEPS}\n\n{total_steps}\n\n"
    return contents[:end].rstrip() + insertion + contents[end:].lstrip("\n")


def migrate_goal_framing_file(path: Path) -> MigrationResult:
    original = path.read_text(encoding="utf-8")
    updated = _normalize_glued_legacy_headings(original)
    warnings: list[str] = []

    if LEGACY_HEADING_PHASE in updated:
        updated = _replace_section(updated, LEGACY_HEADING_PHASE, CANONICAL_HEADING_PHASE)

    if CANONICAL_HEADING_TOTAL_STEPS not in updated:
        total_steps = _derive_total_steps(updated)
        if total_steps:
            updated = _insert_total_steps(updated, total_steps)
        else:
            warnings.append("could not derive Total Steps automatically")

    updated, step_contribution = _remove_section(updated, LEGACY_HEADING_STEP_CONTRIBUTION)
    if step_contribution is not None:
        updated = _append_or_merge_notes(updated, "Legacy step contribution", step_contribution)

    updated, progress_state = _remove_section(updated, LEGACY_HEADING_PROGRESS)
    if progress_state is not None:
        updated = _append_or_merge_notes(updated, "Legacy progress state", progress_state)

    changed = updated != original
    if changed:
        path.write_text(updated.rstrip() + "\n", encoding="utf-8")
    return MigrationResult(path=path, changed=changed, warnings=tuple(warnings))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Unified template governance audit and migration helpers")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="Run goal-framing audit through one repo-local entrypoint")
    audit_parser.add_argument("paths", nargs="+", help="Files or directories to audit")
    audit_parser.add_argument("--allow-legacy", action="store_true", help="Allow legacy migration aliases instead of canonical-only headings")
    audit_parser.add_argument("--strict", action="store_true", help="Fail on unknown markdown kinds")

    migrate_parser = subparsers.add_parser("migrate-goal-framing", help="Migrate legacy packet headings toward canonical goal framing")
    migrate_parser.add_argument("paths", nargs="+", help="Markdown files or directories to migrate")
    migrate_parser.add_argument("--include-unknown", action="store_true", help="Also migrate markdown files whose artifact kind is unknown to the audit helper")

    boundary_parser = subparsers.add_parser("boundary-report-audit", help="Validate goal-step boundary reporting shape (4+1 Execution Assurance Stack)")
    boundary_parser.add_argument("paths", nargs="+", help="Files or directories to audit")
    boundary_parser.add_argument("--strict", action="store_true", help="Fail on files that lack goal-step markers entirely")
    return parser


def run_audit(args: argparse.Namespace) -> int:
    targets = iter_targets([(REPO_ROOT / raw).resolve() if not raw.startswith("/") else Path(raw) for raw in args.paths])
    failures = 0
    for path in targets:
        result = audit_file(path, canonical_only=not args.allow_legacy)
        relative = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        if result.kind == "unknown":
            print(f"SKIP {relative}: unknown artifact kind")
            if args.strict:
                failures += 1
            continue
        for warning in result.warnings:
            print(f"WARN {relative}: {warning}")
        if result.missing:
            print(f"FAIL {relative}: missing {', '.join(result.missing)}")
            failures += 1
            continue
        print(f"PASS {relative}: {result.kind}")
    return 1 if failures else 0


def run_migration(args: argparse.Namespace) -> int:
    targets = iter_targets([(REPO_ROOT / raw).resolve() if not raw.startswith("/") else Path(raw) for raw in args.paths])
    failures = 0
    for path in targets:
        kind = audit_file(path, canonical_only=False).kind
        relative = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        if kind == "unknown" and not args.include_unknown:
            print(f"SKIP {relative}: unknown artifact kind")
            continue
        result = migrate_goal_framing_file(path)
        for warning in result.warnings:
            print(f"WARN {relative}: {warning}")
        state = "UPDATED" if result.changed else "UNCHANGED"
        print(f"{state} {relative}")
        if result.warnings:
            failures += 1
    return 1 if failures else 0


def run_boundary_report_audit(args: argparse.Namespace) -> int:
    targets = iter_boundary_targets([
        (REPO_ROOT / raw).resolve() if not raw.startswith("/") else Path(raw)
        for raw in args.paths
    ])
    failures = 0
    for path in targets:
        result = audit_boundary(path)
        from boundary_report_audit import format_result
        print(format_result(result))
        if result.has_framing and (
            result.missing_headings or result.empty_sections
            or not result.total_steps_has_breakdown
            or not result.current_step_has_step_of
        ):
            failures += 1
    return 1 if failures else 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "audit":
        return run_audit(args)
    if args.command == "migrate-goal-framing":
        return run_migration(args)
    if args.command == "boundary-report-audit":
        return run_boundary_report_audit(args)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())