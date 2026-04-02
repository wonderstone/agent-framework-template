#!/usr/bin/env python3
"""Audit framework surfaces for preference-alignment drift."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class DriftIssue:
    kind: str
    detail: str


REQUIRED_SNIPPETS: dict[str, tuple[str, ...]] = {
    ".github/copilot-instructions.md": (
        "• 当前在做: <action> | 下一步: <next step>",
        "• 当前聚焦: <focus> | 正在做: <action> | 下一步: <next step>",
        "📍 当前聚焦: <final focus> | 已完成: <delivered outcome> | 下一步: <none / next / blocker>",
    ),
    "templates/execution_contract.template.md": (
        "- Routine in-progress replies use: `• 当前在做: <action> | 下一步: <next step>`",
        "- Use the longer focus-bearing variant only when ambiguity exists: `• 当前聚焦: <focus> | 正在做: <action> | 下一步: <next step>`",
        "- Final closeout may use exactly one footer and must place `---` immediately before it: `📍 当前聚焦: <final focus> | 已完成: <outcome> | 下一步: <none / next / blocker>`",
    ),
    "docs/PROGRESS_UPDATE_TEMPLATE.md": (
        "• 当前在做: [current action or batch summary] | 下一步: [next concrete action]",
        "- use the final closeout marker `📍`",
    ),
    "docs/CLOSEOUT_SUMMARY_TEMPLATE.md": (
        "---\n📍 当前聚焦: [final focus] | 已完成: [delivered outcome] | 下一步: [none / next / blocker]",
        "keep exactly one final `📍` footer and place `---` immediately before it",
    ),
    "README.md": (
        "- routine in-progress replies use `• 当前在做: ... | 下一步: ...`",
        "- use `• 当前聚焦: ... | 正在做: ... | 下一步: ...` only when the focus needs to be explicit",
        "- final closeout keeps exactly one `📍` footer and places `---` immediately before it",
    ),
    "docs/ADOPTION_GUIDE.md": (
        "- routine in-progress replies use `• 当前在做: ... | 下一步: ...`",
        "- the longer focus-bearing variant is only for ambiguous cases",
        "- final closeout uses exactly one `📍` footer and places `---` immediately before it",
    ),
}


FORBIDDEN_SNIPPETS: dict[str, tuple[str, ...]] = {
    ".github/copilot-instructions.md": (
        "📍 Focus: <current focus> | Now: <action> | Next: <next step>",
    ),
    "templates/execution_contract.template.md": (
        "- Every in-progress reply status line must be: `📍 Focus: <focus> | Now: <action> | Next: <next step>`",
    ),
}


def audit_repo(root: Path) -> list[DriftIssue]:
    issues: list[DriftIssue] = []

    for relative_path, snippets in REQUIRED_SNIPPETS.items():
        path = root / relative_path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in text:
                issues.append(DriftIssue("missing-preference-snippet", f"{relative_path}: {snippet}"))

    for relative_path, snippets in FORBIDDEN_SNIPPETS.items():
        path = root / relative_path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet in text:
                issues.append(DriftIssue("forbidden-preference-snippet", f"{relative_path}: {snippet}"))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit framework preference-alignment drift")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="Repository root to audit")
    args = parser.parse_args()
    root = args.root.resolve()

    issues = audit_repo(root)

    print("=== Preference Drift Audit ===")
    if not issues:
        print("✅  Preference-alignment checks passed.")
        return 0

    for issue in issues:
        print(f"❌  {issue.kind}: {issue.detail}")
    print("")
    print(f"Found {len(issues)} issue(s).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())