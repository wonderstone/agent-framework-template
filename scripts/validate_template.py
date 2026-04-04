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

from active_docs_audit import audit_repo as audit_active_docs
from preference_drift_audit import audit_repo as audit_preference_drift


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    ".githooks/pre-commit",
    ".githooks/pre-push",
    ".gitignore",
    ".github/copilot-instructions.md",
    ".github/instructions/project-context.instructions.md",
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
    "docs/AI_TRACEABILITY_AND_RECOVERY_DISCUSSION.md",
    "docs/CLOSEOUT_SUMMARY_TEMPLATE.md",
    "docs/COMPATIBILITY.md",
    "docs/DEVELOPER_TOOLCHAIN_DESIGN.md",
    "docs/DEVELOPER_TOOLCHAIN_DISCUSSION.md",
    "docs/DOC_FIRST_EXECUTION_GUIDELINES.md",
    "docs/FRAMEWORK_ARCHITECTURE.md",
    "docs/INDEX.md",
    "docs/LEFTOVER_UNIT_CONTRACT.md",
    "docs/PROGRESS_UPDATE_TEMPLATE.md",
    "docs/ROLE_STRATEGY_EXAMPLES.md",
    "docs/RUNTIME_SURFACE_PROTECTION.md",
    "docs/SKILL_MECHANISM_V1_DRAFT.md",
    "docs/STRATEGY_MECHANISM_LAYERING.md",
    "docs/TRACEABILITY_AND_RECOVERY_V1_DRAFT.md",
    "docs/runbooks/multi-model-discussion-loop.md",
    "docs/runbooks/resumable-git-audit-pipeline.md",
    "examples/skills/01_discussion_packet_workflow.md",
    "examples/skills/02_no_placeholder_runtime_guardrail.md",
    "examples/demo_project/README.md",
    "examples/demo_project/.github/instructions/project-context.instructions.md",
    "examples/demo_project/docs/ARCHITECTURE.md",
    "examples/demo_project/docs/INDEX.md",
    "examples/demo_project/docs/runbooks/demo-workflow.md",
    "examples/demo_project/src/task_tracker.py",
    "examples/demo_project/tests/test_task_tracker.py",
    "scripts/active_docs_audit.py",
    "scripts/bootstrap_adoption.py",
    "scripts/closeout_truth_audit.py",
    "scripts/discussion_pipeline.py",
    "scripts/git_audit_pipeline.py",
    "scripts/install_git_hooks.sh",
    "scripts/preference_drift_audit.py",
    "scripts/runtime_surface_guardrails.py",
    "scripts/validate-template.sh",
    "scripts/validate_template.py",
    "templates/discussion_packet.template.md",
    "templates/doc_first_execution_guidelines.template.md",
    "templates/execution_contract.template.md",
    "templates/failure_packet.template.md",
    "templates/project-context.template.md",
    "templates/reviewer_role_profile.template.md",
    "templates/root_cause_note.template.md",
    "templates/roadmap.template.md",
    "templates/runtime_surface_registry.template.py",
    "templates/session_state.template.md",
    "templates/skill.template.md",
    "tests/test_active_docs_audit.py",
    "tests/test_closeout_truth_audit.py",
    "tests/test_bootstrap_adoption.py",
    "tests/test_discussion_pipeline.py",
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
    "docs/SKILL_MECHANISM_V1_DRAFT.md": (
        "## Core Design Decision",
        "## Canonical V1 Contract",
        "## Validator Contract",
        "## Portability And Honest Degradation",
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
    "docs/DEVELOPER_TOOLCHAIN_DESIGN.md",
    "docs/DEVELOPER_TOOLCHAIN_DISCUSSION.md",
    "docs/SKILL_MECHANISM_V1_DRAFT.md",
    "docs/DOC_FIRST_EXECUTION_GUIDELINES.md",
    "docs/RUNTIME_SURFACE_PROTECTION.md",
    "docs/LEFTOVER_UNIT_CONTRACT.md",
    "docs/PROGRESS_UPDATE_TEMPLATE.md",
    "docs/runbooks/multi-model-discussion-loop.md",
    "templates/doc_first_execution_guidelines.template.md",
    "templates/discussion_packet.template.md",
    "templates/execution_contract.template.md",
    "templates/skill.template.md",
    "examples/skills/",
    "scripts/closeout_truth_audit.py",
    "scripts/discussion_pipeline.py",
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
    "docs/SKILL_MECHANISM_V1_DRAFT.md",
    "docs/AI_TRACEABILITY_AND_RECOVERY_DISCUSSION.md",
    "docs/DEVELOPER_TOOLCHAIN_DESIGN.md",
    "docs/DEVELOPER_TOOLCHAIN_DISCUSSION.md",
    "docs/PROGRESS_UPDATE_TEMPLATE.md",
    "docs/runbooks/multi-model-discussion-loop.md",
    "docs/RUNTIME_SURFACE_PROTECTION.md",
    "docs/LEFTOVER_UNIT_CONTRACT.md",
    "docs/TRACEABILITY_AND_RECOVERY_V1_DRAFT.md",
    "docs/runbooks/resumable-git-audit-pipeline.md",
)

ROOT_PROJECT_CONTEXT_REQUIRED_SNIPPETS = (
    "# agent-framework-template — Project Context",
    "Project type: library",
    "ROADMAP.md",
    "docs/DOC_FIRST_EXECUTION_GUIDELINES.md",
    "docs/DEVELOPER_TOOLCHAIN_DESIGN.md",
    "docs/DEVELOPER_TOOLCHAIN_DISCUSSION.md",
    "docs/SKILL_MECHANISM_V1_DRAFT.md",
    "docs/TRACEABILITY_AND_RECOVERY_V1_DRAFT.md",
    "docs/CLOSEOUT_SUMMARY_TEMPLATE.md",
    "docs/PROGRESS_UPDATE_TEMPLATE.md",
    "## Developer Toolchain",
    "Primary language: Python",
    "docs/runbooks/multi-model-discussion-loop.md",
    "docs/RUNTIME_SURFACE_PROTECTION.md",
    "docs/LEFTOVER_UNIT_CONTRACT.md",
    "templates/doc_first_execution_guidelines.template.md",
    "templates/discussion_packet.template.md",
    "templates/execution_contract.template.md",
    "python3 -m pytest tests/ -q",
    '${TMPDIR:-/tmp}/agent-framework-template-smoke',
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


@dataclass(frozen=True)
class ValidationAdvisory:
    kind: str
    detail: str


@dataclass(frozen=True)
class DeveloperToolchainEntry:
    surface: str
    surface_kind: str
    command_or_source: str
    scope: str
    status: str
    fallback_or_stop: str
    notes: str


DEVELOPER_TOOLCHAIN_ALLOWED_SCOPES = {"file", "module", "service", "full-stack"}
DEVELOPER_TOOLCHAIN_ALLOWED_STATUSES = {
    "declared-unverified",
    "verified-working",
    "known-broken",
    "not-applicable",
}
DEVELOPER_TOOLCHAIN_ALLOWED_SURFACE_KINDS = {
    "Diagnostics",
    "Run",
    "Health or smoke",
    "Repro path",
    "Build",
    "Lint",
    "Format",
    "Logs or inspection",
    "Debug",
}
DEVELOPER_TOOLCHAIN_REQUIRED_SURFACES = (
    "Diagnostics",
    "Run",
    "Health or smoke",
    "Repro path",
)
DEVELOPER_TOOLCHAIN_RECOMMENDED_SURFACES = (
    "Build",
    "Lint",
)
LIVE_RUNTIME_PROJECT_TYPES = {"backend-api", "web-frontend", "cli-tool", "full-stack"}
DEFAULT_DEVELOPER_TOOLCHAIN_CONTRACT = {
    "version": "v1",
    "enforcement": "required-core",
    "required_top_level_fields": ["Primary language", "Package manager"],
    "required_surface_kinds": [
        "Diagnostics",
        "Run",
        "Health or smoke",
        "Repro path",
        "Build",
    ],
    "recommended_surface_kinds": ["Lint"],
    "allow_surface_qualifiers": True,
}

SKILL_ALLOWED_TYPES = {"knowledge", "workflow", "verification", "guardrail"}
SKILL_REQUIRED_HEADINGS = (
    "## Purpose",
    "## Triggers",
    "### Positive Triggers",
    "### Negative Triggers",
    "### Expected Effect",
    "## Entry Instructions",
    "## References",
    "## Governance",
    "### Allowed Evidence",
    "### Reviewer Gate",
    "### Forbidden Direct Update Inputs",
    "## Degradation",
)
SKILL_REQUIRED_METADATA_LABELS = (
    "ID",
    "Type",
    "Owner",
    "Review Threshold",
)
SKILL_RUNTIME_IGNORE_PARTS = {".git", ".venv", "node_modules", "tmp", "__pycache__"}


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


def _extract_markdown_section(text: str, heading: str) -> str | None:
    heading_match = re.search(rf"^## {re.escape(heading)}\s*$", text, flags=re.MULTILINE)
    if heading_match is None:
        return None

    start = heading_match.end()
    next_heading = re.search(r"^## ", text[start:], flags=re.MULTILINE)
    if next_heading is None:
        return text[start:]
    return text[start : start + next_heading.start()]


def _extract_project_type(text: str) -> str | None:
    match = re.search(r"^Project type:\s*(.+)$", text, flags=re.MULTILINE)
    if match is None:
        return None
    return match.group(1).strip()


def _extract_markdown_subsection(text: str, heading: str) -> str | None:
    heading_match = re.search(rf"^### {re.escape(heading)}\s*$", text, flags=re.MULTILINE)
    if heading_match is None:
        return None

    start = heading_match.end()
    next_heading = re.search(r"^(## |### )", text[start:], flags=re.MULTILINE)
    if next_heading is None:
        return text[start:]
    return text[start : start + next_heading.start()]


def _clean_table_cell(value: str) -> str:
    return value.strip().strip("`")


def _canonical_surface_kind(value: str) -> str:
    return re.sub(r"\s*\([^)]*\)\s*$", "", value.strip())


def _surface_is_qualified(value: str) -> bool:
    return _canonical_surface_kind(value) != value.strip()


def _parse_developer_toolchain_entries(text: str) -> tuple[str | None, str | None, list[DeveloperToolchainEntry]]:
    section = _extract_markdown_section(text, "Developer Toolchain")
    if section is None:
        return None, None, []

    primary_language_match = re.search(r"^Primary language:\s*(.+)$", section, flags=re.MULTILINE)
    package_manager_match = re.search(r"^Package manager:\s*(.+)$", section, flags=re.MULTILINE)
    primary_language = primary_language_match.group(1).strip() if primary_language_match else None
    package_manager = package_manager_match.group(1).strip() if package_manager_match else None

    entries: list[DeveloperToolchainEntry] = []
    lines = section.splitlines()
    table_lines: list[str] = []
    collecting = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|"):
            table_lines.append(line)
            collecting = True
            continue
        if collecting:
            break

    for line in table_lines[2:]:
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) != 6:
            continue
        entries.append(
            DeveloperToolchainEntry(
                surface=_clean_table_cell(parts[0]),
                surface_kind=_canonical_surface_kind(_clean_table_cell(parts[0])),
                command_or_source=_clean_table_cell(parts[1]),
                scope=_clean_table_cell(parts[2]),
                status=_clean_table_cell(parts[3]),
                fallback_or_stop=_clean_table_cell(parts[4]),
                notes=_clean_table_cell(parts[5]),
            )
        )

    return primary_language, package_manager, entries


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
        "python3 scripts/validate_template.py",
        "python3 -m pytest tests/ -q",
        "scripts/bootstrap_adoption.py",
        '${RUNNER_TEMP}/template-smoke-minimal',
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
    text = _read(root / ".github/instructions/project-context.instructions.md")
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


def _iter_skill_contract_paths(root: Path) -> tuple[Path, ...]:
    paths: list[Path] = []
    explicit_paths = (
        root / "templates" / "skill.template.md",
        root / "examples" / "skills" / "01_discussion_packet_workflow.md",
        root / "examples" / "skills" / "02_no_placeholder_runtime_guardrail.md",
    )
    for path in explicit_paths:
        if path.is_file():
            paths.append(path)

    for path in root.rglob("SKILL.md"):
        if any(part in SKILL_RUNTIME_IGNORE_PARTS for part in path.parts):
            continue
        if path not in paths:
            paths.append(path)

    return tuple(paths)


def _skill_path_label(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _validate_skill_contract_files(root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in _iter_skill_contract_paths(root):
        relative = _skill_path_label(root, path)
        text = _read(path)
        is_template = relative == "templates/skill.template.md"

        for heading in SKILL_REQUIRED_HEADINGS:
            if heading not in text:
                issues.append(ValidationIssue("missing-skill-heading", f"{relative}: {heading}"))

        for label in SKILL_REQUIRED_METADATA_LABELS:
            if re.search(rf"^- {re.escape(label)}:\s*(.+)$", text, flags=re.MULTILINE) is None:
                issues.append(ValidationIssue("missing-skill-metadata", f"{relative}: {label}"))

        if "| Name | Path | Required at invocation | Purpose |" not in text:
            issues.append(
                ValidationIssue(
                    "missing-skill-reference-table",
                    f"{relative}: references table must use the canonical columns Name / Path / Required at invocation / Purpose",
                )
            )

        for subsection in ("Positive Triggers", "Negative Triggers", "Expected Effect"):
            section = _extract_markdown_subsection(text, subsection)
            if section is not None and "- " not in section:
                issues.append(
                    ValidationIssue(
                        "empty-skill-trigger-section",
                        f"{relative}: subsection '{subsection}' needs at least one bullet",
                    )
                )

        if not is_template:
            type_match = re.search(r"^- Type:\s*(.+)$", text, flags=re.MULTILINE)
            if type_match is not None:
                skill_type = type_match.group(1).strip().strip("`")
                if skill_type not in SKILL_ALLOWED_TYPES:
                    issues.append(
                        ValidationIssue(
                            "invalid-skill-type",
                            f"{relative}: unsupported skill type '{skill_type}'",
                        )
                    )

            if "[" in text or "{{" in text:
                issues.append(
                    ValidationIssue(
                        "skill-placeholder-leftover",
                        f"{relative}: replace placeholder text before treating this as a real skill surface",
                    )
                )

    return issues


def _validate_preference_drift(root: Path) -> list[ValidationIssue]:
    return [ValidationIssue(issue.kind, issue.detail) for issue in audit_preference_drift(root)]


def _validate_active_docs(root: Path) -> list[ValidationIssue]:
    return [ValidationIssue(issue.kind, issue.detail) for issue in audit_active_docs(root)]


def _group_developer_toolchain_entries(
    entries: list[DeveloperToolchainEntry],
) -> dict[str, list[DeveloperToolchainEntry]]:
    grouped: dict[str, list[DeveloperToolchainEntry]] = {}
    for entry in entries:
        grouped.setdefault(entry.surface_kind, []).append(entry)
    return grouped


def _build_contract_issues(
    *,
    primary_language: str | None,
    package_manager: str | None,
    entries: list[DeveloperToolchainEntry],
    contract: dict[str, object],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    required_top_level_fields = set(contract.get("required_top_level_fields", []))
    required_surface_kinds = set(contract.get("required_surface_kinds", []))
    allow_surface_qualifiers = bool(contract.get("allow_surface_qualifiers", False))

    if "Primary language" in required_top_level_fields and not primary_language:
        issues.append(
            ValidationIssue(
                "missing-developer-toolchain-primary-language",
                ".github/instructions/project-context.instructions.md: Developer Toolchain is missing Primary language",
            )
        )

    if "Package manager" in required_top_level_fields and not package_manager:
        issues.append(
            ValidationIssue(
                "missing-developer-toolchain-package-manager",
                ".github/instructions/project-context.instructions.md: Developer Toolchain is missing Package manager",
            )
        )

    if not entries:
        issues.append(
            ValidationIssue(
                "missing-developer-toolchain-table",
                ".github/instructions/project-context.instructions.md: Developer Toolchain needs a structured table of surfaces",
            )
        )
        return issues

    grouped = _group_developer_toolchain_entries(entries)
    for surface_kind in sorted(required_surface_kinds):
        if surface_kind not in grouped:
            issues.append(
                ValidationIssue(
                    "missing-developer-toolchain-surface",
                    f".github/instructions/project-context.instructions.md: Developer Toolchain is missing required surface '{surface_kind}'",
                )
            )

    for entry in entries:
        if _surface_is_qualified(entry.surface) and not allow_surface_qualifiers:
            issues.append(
                ValidationIssue(
                    "developer-toolchain-qualifier-disallowed",
                    f".github/instructions/project-context.instructions.md: surface '{entry.surface}' uses a qualifier but the manifest contract forbids qualified labels",
                )
            )

        if entry.scope not in DEVELOPER_TOOLCHAIN_ALLOWED_SCOPES:
            issues.append(
                ValidationIssue(
                    "invalid-developer-toolchain-scope",
                    f".github/instructions/project-context.instructions.md: surface '{entry.surface}' uses unsupported scope '{entry.scope}'",
                )
            )

        if entry.status not in DEVELOPER_TOOLCHAIN_ALLOWED_STATUSES:
            issues.append(
                ValidationIssue(
                    "invalid-developer-toolchain-status",
                    f".github/instructions/project-context.instructions.md: surface '{entry.surface}' uses unsupported status '{entry.status}'",
                )
            )

        if entry.status in {"declared-unverified", "known-broken"} and not entry.fallback_or_stop:
            issues.append(
                ValidationIssue(
                    "missing-developer-toolchain-fallback",
                    f".github/instructions/project-context.instructions.md: surface '{entry.surface}' needs a fallback or explicit stop rule for status '{entry.status}'",
                )
            )

        if entry.status == "not-applicable" and entry.command_or_source.lower() != "none":
            issues.append(
                ValidationIssue(
                    "invalid-developer-toolchain-none",
                    f".github/instructions/project-context.instructions.md: surface '{entry.surface}' is marked not-applicable but does not use explicit 'none'",
                )
            )

    return issues


def _validate_developer_toolchain_contract(
    project_context_path: Path,
    *,
    project_type: str | None,
    contract: dict[str, object],
) -> list[ValidationIssue]:
    if not project_context_path.is_file():
        return [
            ValidationIssue(
                "missing-developer-toolchain-context",
                ".github/instructions/project-context.instructions.md: missing project context file for Developer Toolchain validation",
            )
        ]

    text = _read(project_context_path)
    if _extract_markdown_section(text, "Developer Toolchain") is None:
        return [
            ValidationIssue(
                "missing-developer-toolchain-section",
                ".github/instructions/project-context.instructions.md: add a Developer Toolchain section",
            )
        ]

    primary_language, package_manager, entries = _parse_developer_toolchain_entries(text)
    issues = _build_contract_issues(
        primary_language=primary_language,
        package_manager=package_manager,
        entries=entries,
        contract=contract,
    )
    return issues


def collect_advisories(root: Path) -> list[ValidationAdvisory]:
    advisories: list[ValidationAdvisory] = []
    project_context = root / ".github/instructions/project-context.instructions.md"
    if not project_context.is_file():
        return advisories

    text = _read(project_context)
    project_type = _extract_project_type(text)
    primary_language, package_manager, entries = _parse_developer_toolchain_entries(text)
    if _extract_markdown_section(text, "Developer Toolchain") is None:
        advisories.append(
            ValidationAdvisory(
                "developer-toolchain-reminder",
                ".github/instructions/project-context.instructions.md: add a Developer Toolchain section so agents can discover diagnostics, run, health, and repro surfaces",
            )
        )
        return advisories

    if not primary_language:
        advisories.append(
            ValidationAdvisory(
                "developer-toolchain-reminder",
                ".github/instructions/project-context.instructions.md: missing Primary language in the Developer Toolchain section",
            )
        )

    if not package_manager:
        advisories.append(
            ValidationAdvisory(
                "developer-toolchain-reminder",
                ".github/instructions/project-context.instructions.md: missing Package manager in the Developer Toolchain section",
            )
        )

    if not entries:
        advisories.append(
            ValidationAdvisory(
                "developer-toolchain-reminder",
                ".github/instructions/project-context.instructions.md: add a Developer Toolchain table with structured surfaces rather than keeping the section empty",
            )
        )
        return advisories

    grouped = _group_developer_toolchain_entries(entries)

    for surface in DEVELOPER_TOOLCHAIN_REQUIRED_SURFACES:
        if surface not in grouped:
            advisories.append(
                ValidationAdvisory(
                    "developer-toolchain-reminder",
                    f".github/instructions/project-context.instructions.md: add the required Developer Toolchain surface '{surface}'",
                )
            )

    for surface in DEVELOPER_TOOLCHAIN_RECOMMENDED_SURFACES:
        if surface not in grouped:
            advisories.append(
                ValidationAdvisory(
                    "developer-toolchain-reminder",
                    f".github/instructions/project-context.instructions.md: consider adding the recommended Developer Toolchain surface '{surface}' or set it explicitly to none",
                )
            )

    for entry in entries:
        if entry.surface_kind not in DEVELOPER_TOOLCHAIN_ALLOWED_SURFACE_KINDS:
            advisories.append(
                ValidationAdvisory(
                    "developer-toolchain-reminder",
                    f".github/instructions/project-context.instructions.md: surface '{entry.surface}' uses unknown base surface '{entry.surface_kind}'; prefer canonical names such as Diagnostics, Run, or Debug",
                )
            )

        if entry.scope not in DEVELOPER_TOOLCHAIN_ALLOWED_SCOPES:
            advisories.append(
                ValidationAdvisory(
                    "developer-toolchain-reminder",
                    f".github/instructions/project-context.instructions.md: surface '{entry.surface}' uses unsupported scope '{entry.scope}'",
                )
            )

        if entry.status not in DEVELOPER_TOOLCHAIN_ALLOWED_STATUSES:
            advisories.append(
                ValidationAdvisory(
                    "developer-toolchain-reminder",
                    f".github/instructions/project-context.instructions.md: surface '{entry.surface}' uses unsupported status '{entry.status}'",
                )
            )

        if entry.status in {"declared-unverified", "known-broken"} and not entry.fallback_or_stop:
            advisories.append(
                ValidationAdvisory(
                    "developer-toolchain-reminder",
                    f".github/instructions/project-context.instructions.md: surface '{entry.surface}' needs a fallback or explicit stop rule for status '{entry.status}'",
                )
            )

        if entry.status == "not-applicable" and entry.command_or_source.lower() != "none":
            advisories.append(
                ValidationAdvisory(
                    "developer-toolchain-reminder",
                    f".github/instructions/project-context.instructions.md: surface '{entry.surface}' is marked not-applicable but does not use explicit 'none'",
                )
            )

    if not any(entry.status in DEVELOPER_TOOLCHAIN_ALLOWED_STATUSES for entry in entries):
        advisories.append(
            ValidationAdvisory(
                "developer-toolchain-reminder",
                ".github/instructions/project-context.instructions.md: add verification status values so declared commands become an actionable decision surface",
            )
        )

    if project_type in LIVE_RUNTIME_PROJECT_TYPES:
        repro_entries = grouped.get("Repro path", [])
        if repro_entries and all(entry.command_or_source.lower() == "none" for entry in repro_entries):
            advisories.append(
                ValidationAdvisory(
                    "developer-toolchain-reminder",
                    ".github/instructions/project-context.instructions.md: live-runtime project types should prefer a concrete Repro path when one is stable; keep 'none' only when that is the honest current state",
                )
            )

        run_entries = grouped.get("Run", [])
        if run_entries and all(entry.command_or_source.lower() == "none" for entry in run_entries):
            advisories.append(
                ValidationAdvisory(
                    "developer-toolchain-reminder",
                    ".github/instructions/project-context.instructions.md: live-runtime project types should normally declare a concrete Run entrypoint rather than 'none'",
                )
            )

    return advisories


def validate_repo(root: Path) -> list[ValidationIssue]:
    if (root / ADOPTER_MANIFEST_PATH).is_file():
        issues = _validate_adopted_repo(root)
        manifest = json.loads(_read(root / ADOPTER_MANIFEST_PATH))
        contract = manifest.get("developer_toolchain_contract")
        if isinstance(contract, dict):
            issues.extend(
                _validate_developer_toolchain_contract(
                    root / ".github/instructions/project-context.instructions.md",
                    project_type=manifest.get("project_type"),
                    contract=contract,
                )
            )
        issues.extend(_validate_preference_drift(root))
        issues.extend(_validate_active_docs(root))
        issues.extend(_validate_skill_contract_files(root))
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
        _validate_active_docs,
        _validate_receipt_closeout_references,
        _validate_skill_contract_files,
    )
    issues: list[ValidationIssue] = []
    for check in checks:
        issues.extend(check(root))
    issues.extend(
        _validate_developer_toolchain_contract(
            root / ".github/instructions/project-context.instructions.md",
            project_type=_extract_project_type(_read(root / ".github/instructions/project-context.instructions.md")),
            contract=DEFAULT_DEVELOPER_TOOLCHAIN_CONTRACT,
        )
    )
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
    advisories = collect_advisories(root)

    print("=== Agent Framework Template — Structured Validation ===")
    print("")
    if not issues:
        for advisory in advisories:
            print(f"⚠️  {advisory.kind}: {advisory.detail}")
        if advisories:
            print("")
        print("✅  All structured checks passed.")
        return 0

    for issue in issues:
        print(f"❌  {issue.kind}: {issue.detail}")
    print("")
    print(f"Found {len(issues)} issue(s).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
