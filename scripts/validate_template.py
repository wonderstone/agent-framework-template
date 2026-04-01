#!/usr/bin/env python3
"""Structured validator for the agent framework template."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    ".gitignore",
    ".github/copilot-instructions.md",
    ".github/project-context.instructions.md",
    ".github/agents/architect.agent.md",
    ".github/agents/implementer.agent.md",
    ".github/instructions/backend.instructions.md",
    ".github/instructions/docs.instructions.md",
    ".github/RELEASE_TEMPLATE.md",
    ".github/workflows/ci.yml",
    "README.md",
    "ROADMAP.md",
    "CHANGELOG.md",
    "LICENSE",
    "VERSION",
    "docs/ADOPTION_GUIDE.md",
    "docs/COMPATIBILITY.md",
    "docs/FRAMEWORK_ARCHITECTURE.md",
    "docs/INDEX.md",
    "docs/LEFTOVER_UNIT_CONTRACT.md",
    "docs/ROLE_STRATEGY_EXAMPLES.md",
    "docs/RUNTIME_SURFACE_PROTECTION.md",
    "docs/STRATEGY_MECHANISM_LAYERING.md",
    "docs/runbooks/resumable-git-audit-pipeline.md",
    "examples/demo_project/README.md",
    "examples/demo_project/.github/project-context.instructions.md",
    "examples/demo_project/docs/ARCHITECTURE.md",
    "examples/demo_project/docs/INDEX.md",
    "examples/demo_project/docs/runbooks/demo-workflow.md",
    "examples/demo_project/src/task_tracker.py",
    "examples/demo_project/tests/test_task_tracker.py",
    "scripts/bootstrap_adoption.py",
    "scripts/git_audit_pipeline.py",
    "scripts/validate-template.sh",
    "scripts/validate_template.py",
    "templates/project-context.template.md",
    "templates/reviewer_role_profile.template.md",
    "templates/roadmap.template.md",
    "templates/session_state.template.md",
    "tests/test_bootstrap_adoption.py",
    "tests/test_git_audit_pipeline.py",
    "tests/test_validate_template.py",
)

REQUIRED_DIRS = (
    ".github/workflows",
    "docs/archive",
    "examples/demo_project",
)

REQUIRED_SECTIONS = {
    "README.md": (
        "## Why This Exists",
        "## Quick Start",
        "## Example Workflow",
        "## Compatibility",
    ),
    "docs/ADOPTION_GUIDE.md": (
        "## Step 1 — Bootstrap Or Copy The Core Files",
        "## Minimal Viable Setup",
        "## Next Upgrade Paths",
    ),
    "docs/FRAMEWORK_ARCHITECTURE.md": (
        "## State Model",
        "## Resumable Audit Artifacts",
        "## Strategy vs Mechanism Layering",
        "## User Acceptance Gate",
    ),
    "docs/COMPATIBILITY.md": (
        "## Verified In This Repository",
        "## Integration Notes",
        "## Known Limits",
    ),
    "examples/demo_project/README.md": (
        "## Scenario",
        "## Demo Layout",
        "## Walkthrough",
    ),
}

README_REQUIRED_REFERENCES = (
    "scripts/bootstrap_adoption.py",
    "examples/demo_project/",
    "docs/COMPATIBILITY.md",
    "docs/RUNTIME_SURFACE_PROTECTION.md",
    "docs/LEFTOVER_UNIT_CONTRACT.md",
)

DOC_LINK_PATHS = {
    "README.md",
    "docs/ADOPTION_GUIDE.md",
    "docs/FRAMEWORK_ARCHITECTURE.md",
    "docs/INDEX.md",
    "docs/COMPATIBILITY.md",
    "examples/demo_project/README.md",
}

INDEX_REQUIRED_ROWS = (
    "docs/FRAMEWORK_ARCHITECTURE.md",
    "docs/ADOPTION_GUIDE.md",
    "docs/STRATEGY_MECHANISM_LAYERING.md",
    "docs/ROLE_STRATEGY_EXAMPLES.md",
    "docs/COMPATIBILITY.md",
    "docs/RUNTIME_SURFACE_PROTECTION.md",
    "docs/LEFTOVER_UNIT_CONTRACT.md",
    "docs/runbooks/resumable-git-audit-pipeline.md",
)

ROOT_PROJECT_CONTEXT_REQUIRED_SNIPPETS = (
    "# agent-framework-template — Project Context",
    "Project type: library",
    "ROADMAP.md",
    "docs/RUNTIME_SURFACE_PROTECTION.md",
    "docs/LEFTOVER_UNIT_CONTRACT.md",
    "python3 -m pytest tests/ -q",
    "examples/demo_project/tmp/git_audit/",
)

ROOT_PROJECT_CONTEXT_FORBIDDEN_SNIPPETS = (
    "[Project Name]",
    "Main application source",
    "Add project-specific entries here as the project evolves",
    "npm run build",
    "./scripts/start.sh",
)


@dataclass(frozen=True)
class ValidationIssue:
    kind: str
    detail: str


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _max_rule_number(text: str) -> int:
    matches = re.findall(r"^## Rule (\d+):", text, flags=re.MULTILINE)
    return max((int(value) for value in matches), default=0)


def _markdown_links(text: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)", text)


def _validate_required_paths(root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            issues.append(ValidationIssue("missing-file", relative))
    for relative in REQUIRED_DIRS:
        if not (root / relative).is_dir():
            issues.append(ValidationIssue("missing-dir", relative))
    return issues


def _validate_sections(root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for relative_path, sections in REQUIRED_SECTIONS.items():
        text = _read(root / relative_path)
        for section in sections:
            if section not in text:
                issues.append(ValidationIssue("missing-section", f"{relative_path}: {section}"))
    return issues


def _validate_readme_references(root: Path) -> list[ValidationIssue]:
    text = _read(root / "README.md")
    issues: list[ValidationIssue] = []
    for required in README_REQUIRED_REFERENCES:
        if required not in text:
            issues.append(ValidationIssue("missing-readme-reference", required))
    return issues


def _validate_doc_links(root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for relative_path in DOC_LINK_PATHS:
        text = _read(root / relative_path)
        for link in _markdown_links(text):
            if link.startswith("/") or re.match(r"^[A-Za-z]:/", link):
                issues.append(
                    ValidationIssue("absolute-local-link", f"{relative_path}: {link}")
                )
                continue
            if "[" in link:
                continue
            target = (root / relative_path).parent / link
            if not target.exists():
                issues.append(
                    ValidationIssue("broken-link", f"{relative_path}: {link}")
                )
    return issues


def _validate_index(root: Path) -> list[ValidationIssue]:
    text = _read(root / "docs/INDEX.md")
    issues: list[ValidationIssue] = []
    for required in INDEX_REQUIRED_ROWS:
        if required not in text:
            issues.append(ValidationIssue("missing-index-row", required))
    return issues


def _validate_ci(root: Path) -> list[ValidationIssue]:
    text = _read(root / ".github/workflows/ci.yml")
    required_snippets = (
        "python-version:",
        "scripts/validate_template.py",
        "python -m pytest tests/ -q",
        "scripts/bootstrap_adoption.py",
    )
    issues: list[ValidationIssue] = []
    for snippet in required_snippets:
        if snippet not in text:
            issues.append(ValidationIssue("missing-ci-step", snippet))
    return issues


def _validate_bootstrap(root: Path) -> list[ValidationIssue]:
    from importlib.util import module_from_spec, spec_from_file_location
    import sys

    module_path = root / "scripts" / "bootstrap_adoption.py"
    spec = spec_from_file_location("bootstrap_adoption_validate", module_path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    issues: list[ValidationIssue] = []
    seen: set[str] = set()
    for profile in ("minimal", "standard", "full"):
        paths = module._iter_profile_paths(profile)
        for relative in paths:
            if relative in seen:
                continue
            seen.add(relative)
            if not (root / relative).exists():
                issues.append(ValidationIssue("missing-bootstrap-asset", relative))

    if "project_type" not in _read(module_path):
        issues.append(ValidationIssue("bootstrap-feature-missing", "project_type support"))

    return issues


def _validate_root_project_context(root: Path) -> list[ValidationIssue]:
    text = _read(root / ".github/project-context.instructions.md")
    issues: list[ValidationIssue] = []

    for snippet in ROOT_PROJECT_CONTEXT_REQUIRED_SNIPPETS:
        if snippet not in text:
            issues.append(ValidationIssue("missing-root-context-snippet", snippet))

    for snippet in ROOT_PROJECT_CONTEXT_FORBIDDEN_SNIPPETS:
        if snippet in text:
            issues.append(ValidationIssue("root-context-placeholder", snippet))

    return issues


def _validate_rule_sync(root: Path) -> list[ValidationIssue]:
    rules_text = _read(root / ".github/copilot-instructions.md")
    max_rule = _max_rule_number(rules_text)
    readme_text = _read(root / "README.md")
    issues: list[ValidationIssue] = []

    for expected in (f"Rule 0–{max_rule}", f"rules 0–{max_rule}"):
        if expected not in readme_text:
            issues.append(ValidationIssue("readme-rule-range-mismatch", expected))

    return issues


def _validate_receipt_closeout_references(root: Path) -> list[ValidationIssue]:
    max_rule = _max_rule_number(_read(root / ".github/copilot-instructions.md"))
    expected = f"Rule {max_rule} (Receipt-Anchored Closeout)"
    issues: list[ValidationIssue] = []

    for relative_path in (
        "docs/RUNTIME_SURFACE_PROTECTION.md",
        "docs/LEFTOVER_UNIT_CONTRACT.md",
    ):
        text = _read(root / relative_path)
        if "Receipt-Anchored Closeout" in text and expected not in text:
            issues.append(
                ValidationIssue("receipt-closeout-rule-mismatch", relative_path)
            )

    return issues


def validate_repo(root: Path) -> list[ValidationIssue]:
    checks = (
        _validate_required_paths,
        _validate_sections,
        _validate_readme_references,
        _validate_doc_links,
        _validate_index,
        _validate_ci,
        _validate_bootstrap,
        _validate_root_project_context,
        _validate_rule_sync,
        _validate_receipt_closeout_references,
    )
    issues: list[ValidationIssue] = []
    for check in checks:
        issues.extend(check(root))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the agent framework template")
    parser.add_argument(
        "--root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root to validate",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    issues = validate_repo(root)

    print("=== Agent Framework Template — Structured Validation ===")
    print("")
    if not issues:
        print("✅  All structured checks passed.")
        return 0

    for issue in issues:
        print(f"❌  {issue.kind}: {issue.detail}")
    print("")
    print(f"Found {len(issues)} issue(s).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
