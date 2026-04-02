#!/usr/bin/env python3
"""Structured validator for the agent framework template."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from preference_drift_audit import audit_repo as audit_preference_drift


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    ".githooks/pre-commit",
    ".githooks/pre-push",
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
    "docs/CLOSEOUT_SUMMARY_TEMPLATE.md",
    "docs/COMPATIBILITY.md",
    "docs/DOC_FIRST_EXECUTION_GUIDELINES.md",
    "docs/FRAMEWORK_ARCHITECTURE.md",
    "docs/INDEX.md",
    "docs/LEFTOVER_UNIT_CONTRACT.md",
    "docs/PROGRESS_UPDATE_TEMPLATE.md",
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
    "scripts/closeout_truth_audit.py",
    "scripts/git_audit_pipeline.py",
    "scripts/install_git_hooks.sh",
    "scripts/preference_drift_audit.py",
    "scripts/runtime_surface_guardrails.py",
    "scripts/validate-template.sh",
    "scripts/validate_template.py",
    "templates/doc_first_execution_guidelines.template.md",
    "templates/execution_contract.template.md",
    "templates/project-context.template.md",
    "templates/reviewer_role_profile.template.md",
    "templates/roadmap.template.md",
    "templates/runtime_surface_registry.template.py",
    "templates/session_state.template.md",
    "tests/test_closeout_truth_audit.py",
    "tests/test_bootstrap_adoption.py",
    "tests/test_git_audit_pipeline.py",
    "tests/test_hook_scaffolding.py",
    "tests/test_runtime_surface_guardrails.py",
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
        "## Pre-Execution Confirmation",
        "## Example Workflow",
        "## Compatibility",
    ),
    "docs/ADOPTION_GUIDE.md": (
        "## Step 1 — Bootstrap Or Copy The Core Files",
        "## Step 3A — Confirm The Execution Contract",
        "## Minimal Viable Setup",
        "## Next Upgrade Paths",
    ),
    "docs/CLOSEOUT_SUMMARY_TEMPLATE.md": (
        "## Recommended Template",
        "## Global State Field",
        "## Default Recommendation",
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
    "docs/PROGRESS_UPDATE_TEMPLATE.md": (
        "## Recommended Template",
        "## Rules For Good Use",
        "## Default Recommendation",
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
    "docs/CLOSEOUT_SUMMARY_TEMPLATE.md",
    "docs/COMPATIBILITY.md",
    "docs/DOC_FIRST_EXECUTION_GUIDELINES.md",
    "docs/RUNTIME_SURFACE_PROTECTION.md",
    "docs/LEFTOVER_UNIT_CONTRACT.md",
    "docs/PROGRESS_UPDATE_TEMPLATE.md",
    "templates/doc_first_execution_guidelines.template.md",
    "templates/execution_contract.template.md",
    "scripts/closeout_truth_audit.py",
    "scripts/runtime_surface_guardrails.py",
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
    "docs/CLOSEOUT_SUMMARY_TEMPLATE.md",
    "docs/DOC_FIRST_EXECUTION_GUIDELINES.md",
    "docs/STRATEGY_MECHANISM_LAYERING.md",
    "docs/ROLE_STRATEGY_EXAMPLES.md",
    "docs/COMPATIBILITY.md",
    "docs/PROGRESS_UPDATE_TEMPLATE.md",
    "docs/RUNTIME_SURFACE_PROTECTION.md",
    "docs/LEFTOVER_UNIT_CONTRACT.md",
    "docs/runbooks/resumable-git-audit-pipeline.md",
)

ROOT_PROJECT_CONTEXT_REQUIRED_SNIPPETS = (
    "# agent-framework-template — Project Context",
    "Project type: library",
    "ROADMAP.md",
    "docs/DOC_FIRST_EXECUTION_GUIDELINES.md",
    "docs/CLOSEOUT_SUMMARY_TEMPLATE.md",
    "docs/PROGRESS_UPDATE_TEMPLATE.md",
    "docs/RUNTIME_SURFACE_PROTECTION.md",
    "docs/LEFTOVER_UNIT_CONTRACT.md",
    "templates/doc_first_execution_guidelines.template.md",
    "templates/execution_contract.template.md",
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

ADOPTER_MANIFEST_PATH = ".github/agent-framework-manifest.json"


@dataclass(frozen=True)
class ValidationIssue:
    kind: str
    detail: str


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_bootstrap_module(root: Path):
    import sys

    module_path = root / "scripts" / "bootstrap_adoption.py"
    spec = spec_from_file_location("bootstrap_adoption_validate", module_path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _max_rule_number(text: str) -> int:
    matches = re.findall(r"^## Rule (\d+):", text, flags=re.MULTILINE)
    return max((int(value) for value in matches), default=0)


def _rule_number_for_title(text: str, title: str) -> int | None:
    pattern = re.compile(r"^## Rule (\d+):\s+(.+)$", flags=re.MULTILINE)
    for value, found_title in pattern.findall(text):
        if found_title.strip() == title:
            return int(value)
    return None


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
    module_path = root / "scripts" / "bootstrap_adoption.py"
    module = _load_bootstrap_module(root)

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

    if "capabilities" not in _read(module_path):
        issues.append(ValidationIssue("bootstrap-feature-missing", "capability flags support"))

    return issues


def _validate_adopted_repo(root: Path) -> list[ValidationIssue]:
    manifest = json.loads(_read(root / ADOPTER_MANIFEST_PATH))
    expected_files = manifest.get("expected_files", [])

    issues: list[ValidationIssue] = []
    for relative in sorted(expected_files):
        if not (root / relative).exists():
            issues.append(ValidationIssue("missing-adopted-asset", relative))

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


def _validate_session_state_template(root: Path) -> list[ValidationIssue]:
    text = _read(root / "templates/session_state.template.md")
    issues: list[ValidationIssue] = []
    required_snippets = (
        "**Current Step**:",
        "**Next Planned Step**:",
        "**Progress Unit**:",
        "**True Closeout Boundary**:",
        "**Host Closeout Action**:",
    )
    for snippet in required_snippets:
        if snippet not in text:
            issues.append(ValidationIssue("missing-session-state-snippet", snippet))
    return issues


def _validate_execution_contract(root: Path) -> list[ValidationIssue]:
    text = _read(root / "templates/execution_contract.template.md")
    issues: list[ValidationIssue] = []
    required_snippets = (
        "## Optional Fast-Start Block",
        "Execution Boundary:",
        "Working Hypothesis:",
        "Decomposition Decision:",
        "## Long-Loop Closeout Contract",
        "Progress unit:",
        "True closeout boundary:",
        "Intermediate batch rule:",
        "Host closeout rule:",
        "Maximum file scope per dispatched subtask:",
        "Parallel ceiling:",
        "Progress unit for while-mode tasks:",
        "True closeout boundary for while-mode tasks:",
        "Intermediate batches may trigger progress updates only:",
        "Host closeout action reserved for the true boundary only:",
        "Bootstrap-mode allowance:",
        "User Acceptance Criteria (UAC):",
        "End-to-end scenario:",
        "If full E2E is not yet possible:",
        "Gap check before closeout:",
        "Host closeout action available:",
        "Platform continuation markers to ignore as completion signals:",
        "Status line rule:",
        "Final closeout summary lives in:",
        "Closeout summary template:",
        "Progress update template:",
        "Status-line / closeout-summary rule understood:",
    )
    for snippet in required_snippets:
        if snippet not in text:
            issues.append(ValidationIssue("missing-execution-contract-snippet", snippet))
    return issues


def _validate_closeout_rule_guards(root: Path) -> list[ValidationIssue]:
    text = _read(root / ".github/copilot-instructions.md")
    issues: list[ValidationIssue] = []
    required_snippets = (
        "### Closeout Irreversibility Rule (🔴 Mandatory)",
        "### Hook Repair Protocol (🔴 Mandatory)",
        "it must not emit a second closeout action",
        "add only the missing closeout action",
    )
    for snippet in required_snippets:
        if snippet not in text:
            issues.append(ValidationIssue("missing-closeout-guard-snippet", snippet))
    return issues


def _validate_receipt_closeout_references(root: Path) -> list[ValidationIssue]:
    rules_text = _read(root / ".github/copilot-instructions.md")
    rule_number = _rule_number_for_title(rules_text, "Receipt-Anchored Closeout (🔴 Mandatory)")
    expected = f"Rule {rule_number} (Receipt-Anchored Closeout)"
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


def _validate_preference_drift(root: Path) -> list[ValidationIssue]:
    return [ValidationIssue(issue.kind, issue.detail) for issue in audit_preference_drift(root)]


def validate_repo(root: Path) -> list[ValidationIssue]:
    if (root / ADOPTER_MANIFEST_PATH).is_file():
        issues = _validate_adopted_repo(root)
        issues.extend(_validate_preference_drift(root))
        return issues

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
        _validate_session_state_template,
        _validate_execution_contract,
        _validate_closeout_rule_guards,
        _validate_preference_drift,
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
