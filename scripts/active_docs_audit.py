#!/usr/bin/env python3
"""Audit active documentation for portability and stale framework assertions."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ActiveDocIssue:
    kind: str
    detail: str


ACTIVE_DOC_GLOBS: tuple[str, ...] = (
    "README.md",
    ".github/**/*.md",
    ".github/**/*.instructions.md",
    "docs/**/*.md",
    "examples/**/*.md",
    "examples/**/*.instructions.md",
    "templates/**/*.md",
)

EXCLUDED_PARTS = ("docs/archive/", "tmp/", ".venv/", "node_modules/")

ABSOLUTE_LOCAL_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?:^|[\s`\"'(])(/Users/[^\s`\"')]+)"),
    re.compile(r"(?:^|[\s`\"'(])(/var/folders/[^\s`\"')]+)"),
    re.compile(r"(?:^|[\s`\"'(])(/private/var/folders/[^\s`\"')]+)"),
    re.compile(r"(?:^|[\s`\"'(])([A-Za-z]:\\[^\s`\"')]+)"),
    re.compile(r"(?:^|[\s`\"'(])(file://[^\s`\"')]+)"),
    re.compile(r"(?:^|[\s`\"'(])(/tmp/[A-Za-z0-9._-][^\s`\"')]+)"),
)

REPO_ENTRYPOINT_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "nonportable-python-entrypoint",
        re.compile(
            r"(?<!python3 )python\s+scripts/(?:bootstrap_adoption|validate_template|git_audit_pipeline|closeout_truth_audit|preference_drift_audit|active_docs_audit|runtime_surface_guardrails)\.py"
        ),
    ),
    (
        "nonportable-python-entrypoint",
        re.compile(r"(?<!python3 -m )python\s+-m\s+pytest\s+tests/\s+-q"),
    ),
)

REQUIRED_SNIPPETS: dict[str, tuple[str, ...]] = {
    "README.md": (
        "rules are loaded on-demand, not all at once",
        ".github/instructions/project-context.instructions.md",
    ),
    "docs/FRAMEWORK_ARCHITECTURE.md": (
        "Layer 1 — Operating Rules",
        "Layer 2 — Project Adapter",
        ".github/instructions/project-context.instructions.md",
    ),
}

FORBIDDEN_SNIPPETS: dict[str, tuple[str, ...]] = {
    "README.md": (
        "  project-context.instructions.md  ← project adapter (fill in for your project)",
    ),
    "docs/ADOPTION_GUIDE.md": (
        "  project-context.instructions.md  ← project adapter (fill in Step 2)",
    ),
    "docs/INDEX.md": (
        "## Project (create these for your project)",
        "| `ARCHITECTURE.md` | System architecture, module map, and service boundaries |",
    ),
}


def _iter_active_doc_paths(root: Path) -> list[Path]:
    seen: dict[str, Path] = {}
    for pattern in ACTIVE_DOC_GLOBS:
        for path in root.glob(pattern):
            if not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            if any(part in relative for part in EXCLUDED_PARTS):
                continue
            seen[relative] = path
    return [seen[key] for key in sorted(seen)]


def audit_repo(root: Path) -> list[ActiveDocIssue]:
    issues: list[ActiveDocIssue] = []

    for path in _iter_active_doc_paths(root):
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")

        for pattern in ABSOLUTE_LOCAL_PATTERNS:
            for match in pattern.finditer(text):
                issues.append(
                    ActiveDocIssue(
                        "nonportable-active-doc-path",
                        f"{relative}: {match.group(1)}",
                    )
                )

        for kind, pattern in REPO_ENTRYPOINT_PATTERNS:
            for match in pattern.finditer(text):
                issues.append(ActiveDocIssue(kind, f"{relative}: {match.group(0)}"))

    for relative, snippets in REQUIRED_SNIPPETS.items():
        path = root / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in text:
                issues.append(ActiveDocIssue("missing-active-doc-snippet", f"{relative}: {snippet}"))

    for relative, snippets in FORBIDDEN_SNIPPETS.items():
        path = root / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet in text:
                issues.append(ActiveDocIssue("stale-active-doc-assertion", f"{relative}: {snippet}"))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit active docs for portability and stale assertions")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="Repository root to audit")
    args = parser.parse_args()
    root = args.root.resolve()

    issues = audit_repo(root)

    print("=== Active Docs Audit ===")
    if not issues:
        print("✅  Active documentation checks passed.")
        return 0

    for issue in issues:
        print(f"❌  {issue.kind}: {issue.detail}")
    print("")
    print(f"Found {len(issues)} issue(s).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())