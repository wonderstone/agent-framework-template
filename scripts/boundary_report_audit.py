#!/usr/bin/env python3
"""Audit markdown files for truthful goal-step boundary reporting.

Validates the canonical 4+1 Execution Assurance Stack reporting shape:

    Goal:       <large target only>
    Phase:      <stage purpose>
    Current Step: Step X of Y — <active step summary>
    Total Steps: 1. <step 1 summary> 2. <step 2 summary> ...

This audit runs at closeout boundaries so goal-step framing drift
is caught mechanically rather than relying on self-check memory.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_HEADINGS = ("## Goal", "## Phase", "## Current Step", "## Total Steps")

# Pattern: "Step X of Y" with optional trailing text
STEP_OF_PATTERN = re.compile(r"Step\s+\d+\s+of\s+\d+", re.IGNORECASE)

# Pattern: numbered list items like "1. ", "2. ", "3. " at line start
NUMBERED_ITEM_PATTERN = re.compile(r"(?m)^\d+\.\s+\S")


@dataclass(frozen=True)
class AuditResult:
    path: Path
    has_framing: bool  # whether the file carries goal-step markers at all
    missing_headings: tuple[str, ...]  # required headings not found
    empty_sections: tuple[str, ...]  # headings found but with no content
    total_steps_has_breakdown: bool  # Total Steps contains numbered items
    current_step_has_step_of: bool  # Current Step mentions "Step X of Y"
    warnings: tuple[str, ...]


def _extract_section_text(contents: str, heading: str) -> str | None:
    """Return the text body after a ## heading, up to the next ## or EOF."""
    pattern = re.compile(
        rf"(?ms)^({re.escape(heading)})\s*$"
        rf"\n+(.*?)"
        rf"(?=^##\s|\Z)"
    )
    match = pattern.search(contents)
    if not match:
        return None
    body = match.group(2).strip()
    return body if body else None


def audit_file(path: Path) -> AuditResult:
    """Audit one markdown file for boundary-report requirements."""
    contents = path.read_text(encoding="utf-8")

    # Quick check: does this file carry goal-step markers at all?
    has_framing = any(
        marker in contents for marker in REQUIRED_HEADINGS
    )
    if not has_framing:
        return AuditResult(
            path=path,
            has_framing=False,
            missing_headings=(),
            empty_sections=(),
            total_steps_has_breakdown=False,
            current_step_has_step_of=False,
            warnings=(),
        )

    missing: list[str] = []
    empty: list[str] = []
    total_steps_breakdown = False
    current_step_step_of = False
    warnings: list[str] = []

    for heading in REQUIRED_HEADINGS:
        body = _extract_section_text(contents, heading)
        if body is None:
            missing.append(heading)
            continue

        if not body:
            empty.append(heading)
            continue

        # Heading-specific deep checks
        if heading == "## Total Steps":
            total_steps_breakdown = bool(NUMBERED_ITEM_PATTERN.search(body))
            if not total_steps_breakdown:
                warnings.append(
                    "Total Steps section lacks numbered breakdown "
                    '(expected lines like "1. <summary> 2. <summary> ...")'
                )

        if heading == "## Current Step":
            current_step_step_of = bool(STEP_OF_PATTERN.search(body))
            if not current_step_step_of:
                warnings.append(
                    'Current Step does not contain "Step X of Y" pattern'
                )

    return AuditResult(
        path=path,
        has_framing=True,
        missing_headings=tuple(missing),
        empty_sections=tuple(empty),
        total_steps_has_breakdown=total_steps_breakdown,
        current_step_has_step_of=current_step_step_of,
        warnings=tuple(warnings),
    )


def iter_targets(paths: list[Path]) -> list[Path]:
    """Collect .md files from paths, recursing into directories."""
    collected: list[Path] = []
    for path in paths:
        if path.is_dir():
            collected.extend(sorted(p for p in path.rglob("*.md") if p.is_file()))
        elif path.suffix == ".md":
            collected.append(path)
    return collected


def format_result(result: AuditResult) -> str:
    """Format one audit result into a human-readable line."""
    if not result.has_framing:
        return f"SKIP {_rel(result.path)}: no goal-step framing markers"

    label = "PASS"
    reasons: list[str] = []

    if result.missing_headings:
        label = "FAIL"
        reasons.append(f"missing: {', '.join(result.missing_headings)}")
    if result.empty_sections:
        label = "FAIL"
        reasons.append(f"empty: {', '.join(result.empty_sections)}")
    if not result.total_steps_has_breakdown and "## Total Steps" not in result.missing_headings:
        label = "FAIL"
        reasons.append("Total Steps missing numbered breakdown")
    if not result.current_step_has_step_of and "## Current Step" not in result.missing_headings:
        label = "FAIL"
        reasons.append("Current Step missing 'Step X of Y'")
    for warning in result.warnings:
        reasons.append(f"WARN: {warning}")

    detail = "; ".join(reasons) if reasons else "canonical shape verified"
    return f"{label} {_rel(result.path)}: {detail}"


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit markdown files for canonical goal-step boundary reporting shape"
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Files or directories to audit (recursively scans .md files)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero even when files lack goal-step markers entirely",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    targets = iter_targets(
        [(REPO_ROOT / p).resolve() if not p.startswith("/") else Path(p) for p in args.paths]
    )

    failures = 0
    strict_failures = 0

    for path in targets:
        result = audit_file(path)
        print(format_result(result))
        if result.has_framing and (
            result.missing_headings or result.empty_sections
            or not result.total_steps_has_breakdown
            or not result.current_step_has_step_of
        ):
            failures += 1
        if args.strict and not result.has_framing:
            strict_failures += 1

    if strict_failures:
        print(f"\nStrict mode: {strict_failures} file(s) skipped because they lack goal-step framing.")
    if failures:
        print(f"\n{_rel(Path('.'))}: {failures} file(s) with boundary-report defects.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
