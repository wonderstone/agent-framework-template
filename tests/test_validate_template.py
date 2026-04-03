from __future__ import annotations

import importlib.util
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "validate_template.py"
SPEC = importlib.util.spec_from_file_location("validate_template", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

ValidationIssue = MODULE.ValidationIssue
validate_repo = MODULE.validate_repo
collect_advisories = MODULE.collect_advisories

BOOTSTRAP_MODULE_PATH = REPO_ROOT / "scripts" / "bootstrap_adoption.py"
BOOTSTRAP_SPEC = importlib.util.spec_from_file_location("bootstrap_adoption_for_validation", BOOTSTRAP_MODULE_PATH)
assert BOOTSTRAP_SPEC is not None
assert BOOTSTRAP_SPEC.loader is not None
BOOTSTRAP_MODULE = importlib.util.module_from_spec(BOOTSTRAP_SPEC)
sys.modules[BOOTSTRAP_SPEC.name] = BOOTSTRAP_MODULE
BOOTSTRAP_SPEC.loader.exec_module(BOOTSTRAP_MODULE)

bootstrap_repo = BOOTSTRAP_MODULE.bootstrap_repo


def test_validate_repo_passes_for_current_repository() -> None:
    issues = validate_repo(REPO_ROOT)

    assert issues == []


def test_validate_repo_reports_preference_drift(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    readme = repo_copy / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8").replace(
            "- routine in-progress replies use `• 当前在做: ... | 下一步: ...`",
            "- routine in-progress replies use `📍 Focus: ... | Now: ... | Next: ...`",
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "missing-preference-snippet",
        "README.md: - routine in-progress replies use `• 当前在做: ... | 下一步: ...`",
    ) in issues


def test_validate_repo_reports_active_doc_portability_drift(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    project_context = repo_copy / ".github" / "instructions" / "project-context.instructions.md"
    project_context.write_text(
        project_context.read_text(encoding="utf-8").replace(
            '${TMPDIR:-/tmp}/agent-framework-template-smoke',
            '/tmp/agent-framework-template-smoke',
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "nonportable-active-doc-path",
        ".github/instructions/project-context.instructions.md: /tmp/agent-framework-template-smoke",
    ) in issues


def test_validate_repo_reports_missing_required_file(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)
    (repo_copy / "LICENSE").unlink()

    issues = validate_repo(repo_copy)

    assert ValidationIssue("missing-file", "LICENSE") in issues


def test_validate_repo_reports_root_project_context_placeholder(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    project_context = repo_copy / ".github" / "instructions" / "project-context.instructions.md"
    original = project_context.read_text(encoding="utf-8")
    project_context.write_text(
        original.replace("# agent-framework-template — Project Context", "# [Project Name] — Project Context", 1),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue("root-context-placeholder", "[Project Name]") in issues


def test_validate_repo_reports_readme_rule_range_mismatch(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    readme = repo_copy / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8").replace("Rule 0–27", "Rule 0–26"),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue("readme-rule-range-mismatch", "Rule 0–27") in issues


def test_validate_repo_reports_receipt_closeout_rule_mismatch(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    runtime_doc = repo_copy / "docs" / "RUNTIME_SURFACE_PROTECTION.md"
    runtime_doc.write_text(
        runtime_doc.read_text(encoding="utf-8").replace(
            "Rule 25 (Receipt-Anchored Closeout)",
            "Rule 24 (Receipt-Anchored Closeout)",
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "receipt-closeout-rule-mismatch", "docs/RUNTIME_SURFACE_PROTECTION.md"
    ) in issues


def test_validate_repo_reports_missing_capability_asset(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)
    (repo_copy / "scripts" / "closeout_truth_audit.py").unlink()

    issues = validate_repo(repo_copy)

    assert ValidationIssue("missing-file", "scripts/closeout_truth_audit.py") in issues


def test_validate_repo_passes_for_bootstrapped_adopted_repo(tmp_path: Path) -> None:
    bootstrap_repo(
        target_dir=tmp_path / "adopted",
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    issues = validate_repo(tmp_path / "adopted")

    assert issues == []


def test_validate_repo_reports_missing_developer_toolchain_section_for_bootstrapped_adopted_repo(
    tmp_path: Path,
) -> None:
    bootstrap_repo(
        target_dir=tmp_path / "adopted",
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    project_context = tmp_path / "adopted" / ".github" / "instructions" / "project-context.instructions.md"
    text = project_context.read_text(encoding="utf-8")
    start = text.index("## Developer Toolchain")
    end = text.index("## Build and Test Commands")
    project_context.write_text(text[:start] + text[end:], encoding="utf-8")

    issues = validate_repo(tmp_path / "adopted")

    assert ValidationIssue(
        "missing-developer-toolchain-section",
        ".github/instructions/project-context.instructions.md: add a Developer Toolchain section",
    ) in issues


def test_validate_repo_reports_invalid_developer_toolchain_status_for_bootstrapped_adopted_repo(
    tmp_path: Path,
) -> None:
    bootstrap_repo(
        target_dir=tmp_path / "adopted",
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    project_context = tmp_path / "adopted" / ".github" / "instructions" / "project-context.instructions.md"
    project_context.write_text(
        project_context.read_text(encoding="utf-8").replace(
            "| `declared-unverified` |", "| `mystery-status` |", 1
        ),
        encoding="utf-8",
    )

    issues = validate_repo(tmp_path / "adopted")

    assert ValidationIssue(
        "invalid-developer-toolchain-status",
        ".github/instructions/project-context.instructions.md: surface 'Diagnostics' uses unsupported status 'mystery-status'",
    ) in issues


def test_validate_repo_reports_missing_primary_language_for_bootstrapped_adopted_repo(
    tmp_path: Path,
) -> None:
    bootstrap_repo(
        target_dir=tmp_path / "adopted",
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    project_context = tmp_path / "adopted" / ".github" / "instructions" / "project-context.instructions.md"
    project_context.write_text(
        project_context.read_text(encoding="utf-8").replace(
            "Primary language: Python\n\n", ""
        ),
        encoding="utf-8",
    )

    issues = validate_repo(tmp_path / "adopted")

    assert ValidationIssue(
        "missing-developer-toolchain-primary-language",
        ".github/instructions/project-context.instructions.md: Developer Toolchain is missing Primary language",
    ) in issues


def test_validate_repo_reports_missing_required_surface_for_bootstrapped_adopted_repo(
    tmp_path: Path,
) -> None:
    bootstrap_repo(
        target_dir=tmp_path / "adopted",
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    project_context = tmp_path / "adopted" / ".github" / "instructions" / "project-context.instructions.md"
    project_context.write_text(
        project_context.read_text(encoding="utf-8").replace(
            "| Build | `python -m build` | `module` | `declared-unverified` | Stop after build blockers are cleared when runnable proof is unnecessary | Required when packaging matters |\n",
            "",
        ),
        encoding="utf-8",
    )

    issues = validate_repo(tmp_path / "adopted")

    assert ValidationIssue(
        "missing-developer-toolchain-surface",
        ".github/instructions/project-context.instructions.md: Developer Toolchain is missing required surface 'Build'",
    ) in issues


def test_collect_advisories_reports_missing_developer_toolchain_section(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    project_context = repo_copy / ".github" / "instructions" / "project-context.instructions.md"
    text = project_context.read_text(encoding="utf-8")
    start = text.index("## Developer Toolchain")
    end = text.index("## Build and Test Commands")
    project_context.write_text(text[:start] + text[end:], encoding="utf-8")

    advisories = collect_advisories(repo_copy)

    assert any(advisory.kind == "developer-toolchain-reminder" for advisory in advisories)


def test_collect_advisories_reports_invalid_developer_toolchain_status(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    project_context = repo_copy / ".github" / "instructions" / "project-context.instructions.md"
    project_context.write_text(
        project_context.read_text(encoding="utf-8").replace("| `verified-working` |", "| `mystery-status` |", 1),
        encoding="utf-8",
    )

    advisories = collect_advisories(repo_copy)

    assert any("unsupported status 'mystery-status'" in advisory.detail for advisory in advisories)


def test_collect_advisories_reports_live_runtime_repro_none(tmp_path: Path) -> None:
    bootstrap_repo(
        target_dir=tmp_path / "adopted",
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    project_context = tmp_path / "adopted" / ".github" / "instructions" / "project-context.instructions.md"
    project_context.write_text(
        project_context.read_text(encoding="utf-8").replace(
            "| Repro path | `run the primary user command with real arguments` | `service` | `declared-unverified` | Use `none` only if no stable user-visible flow exists yet | Shortest user-visible repro |",
            "| Repro path | `none` | `service` | `not-applicable` | Stop after smoke because no stable repro exists yet | Shortest user-visible repro |",
        ),
        encoding="utf-8",
    )

    advisories = collect_advisories(tmp_path / "adopted")

    assert any("live-runtime project types should prefer a concrete Repro path" in advisory.detail for advisory in advisories)


def test_collect_advisories_accepts_qualified_surface_labels(tmp_path: Path) -> None:
    bootstrap_repo(
        target_dir=tmp_path / "adopted",
        project_name="Adopted Demo",
        profile="standard",
        project_type="full-stack",
    )

    advisories = collect_advisories(tmp_path / "adopted")

    assert not any("unknown base surface" in advisory.detail for advisory in advisories)


def test_collect_advisories_passes_for_bootstrapped_adopted_repo(tmp_path: Path) -> None:
    bootstrap_repo(
        target_dir=tmp_path / "adopted",
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    advisories = collect_advisories(tmp_path / "adopted")

    assert advisories == []
