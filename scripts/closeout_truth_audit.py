#!/usr/bin/env python3
"""Audit closeout claims for receipt-anchor evidence in the same diff."""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


CLAIM_PATTERNS = (
    re.compile(r"\bcompleted\b", re.IGNORECASE),
    re.compile(r"\baccepted\b", re.IGNORECASE),
    re.compile(r"\bstatus=passed\b", re.IGNORECASE),
    re.compile(r"\bdone\b", re.IGNORECASE),
    re.compile(r"\bverified\b", re.IGNORECASE),
    re.compile(r"\ball criteria met\b", re.IGNORECASE),
)

ANCHOR_PATTERNS = (
    re.compile(r"request_id=", re.IGNORECASE),
    re.compile(r"turn_id=", re.IGNORECASE),
    re.compile(r"session_id=", re.IGNORECASE),
    re.compile(r"stream_session_id=", re.IGNORECASE),
    re.compile(r"status=passed", re.IGNORECASE),
    re.compile(r"all tests passed", re.IGNORECASE),
    re.compile(r"live smoke passed", re.IGNORECASE),
    re.compile(r"\b\d+ passed\b", re.IGNORECASE),
)


@dataclass(frozen=True)
class DiffLine:
    path: str
    content: str


def is_truth_source(path: str) -> bool:
    normalized = path.strip()
    return (
        normalized == "session_state.md"
        or normalized == "ROADMAP.md"
        or normalized.startswith("docs/") and normalized.endswith(".md")
    )


def parse_added_lines(diff_text: str) -> list[DiffLine]:
    lines: list[DiffLine] = []
    current_path: str | None = None
    for raw_line in diff_text.splitlines():
        if raw_line.startswith("+++ b/"):
            current_path = raw_line[6:]
            continue
        if raw_line.startswith("+++ "):
            current_path = None
            continue
        if raw_line.startswith("diff --git ") or raw_line.startswith("@@"):
            continue
        if raw_line.startswith("+") and not raw_line.startswith("+++") and current_path:
            lines.append(DiffLine(path=current_path, content=raw_line[1:]))
    return lines


def find_claims(lines: list[DiffLine]) -> list[DiffLine]:
    return [
        line
        for line in lines
        if is_truth_source(line.path)
        and any(pattern.search(line.content) for pattern in CLAIM_PATTERNS)
    ]


def has_anchor(lines: list[DiffLine]) -> bool:
    return any(
        pattern.search(line.content)
        for line in lines
        for pattern in ANCHOR_PATTERNS
    )


def audit_diff(diff_text: str) -> list[str]:
    added_lines = parse_added_lines(diff_text)
    claims = find_claims(added_lines)
    if not claims or has_anchor(added_lines):
        return []

    paths = ", ".join(sorted({claim.path for claim in claims}))
    return [
        "closeout claims were added without a receipt anchor in the same diff",
        f"claim paths: {paths}",
    ]


def get_git_diff(root: Path, *, staged: bool) -> str:
    command = ["git", "-C", str(root), "diff", "--unified=0", "--no-color"]
    if staged:
        command.insert(4, "--cached")
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return completed.stdout


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit closeout claims for receipt anchors")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument("--diff-file", type=Path, help="read diff from a file instead of git")
    parser.add_argument(
        "--worktree",
        action="store_true",
        help="inspect unstaged working tree diff instead of staged diff",
    )
    args = parser.parse_args()

    if args.diff_file:
        diff_text = args.diff_file.read_text(encoding="utf-8")
    else:
        diff_text = get_git_diff(args.root.resolve(), staged=not args.worktree)

    issues = audit_diff(diff_text)
    if not issues:
        print("closeout truth audit passed")
        return 0

    print("closeout truth audit failed")
    for issue in issues:
        print(f"- {issue}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())