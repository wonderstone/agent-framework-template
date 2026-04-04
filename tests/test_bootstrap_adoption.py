from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "bootstrap_adoption.py"
SPEC = importlib.util.spec_from_file_location("bootstrap_adoption", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

bootstrap_repo = MODULE.bootstrap_repo
detect_project_type = MODULE.detect_project_type


def test_bootstrap_minimal_creates_core_files(tmp_path: Path) -> None:
    result = bootstrap_repo(
        target_dir=tmp_path,
        project_name="Demo Project",
        profile="minimal",
    )

    assert (tmp_path / ".github" / "copilot-instructions.md").exists()
    assert (tmp_path / "docs" / "INDEX.md").exists()
    assert (tmp_path / "docs" / "archive" / ".gitkeep").exists()
    assert (tmp_path / "session_state.md").exists()
    assert (tmp_path / "ROADMAP.md").exists()
    project_context = tmp_path / ".github" / "instructions" / "project-context.instructions.md"
    assert project_context.exists()
    assert "Demo Project" in project_context.read_text(encoding="utf-8")
    assert result.skipped == ()


def test_bootstrap_standard_skips_existing_without_force(tmp_path: Path) -> None:
    existing = tmp_path / ".github" / "copilot-instructions.md"
    existing.parent.mkdir(parents=True, exist_ok=True)
    existing.write_text("keep me", encoding="utf-8")

    result = bootstrap_repo(
        target_dir=tmp_path,
        project_name="Demo Project",
        profile="standard",
    )

    assert existing.read_text(encoding="utf-8") == "keep me"
    assert existing in result.skipped
    assert (tmp_path / "docs" / "DEVELOPER_TOOLCHAIN_DESIGN.md").exists()
    assert (tmp_path / "docs" / "DEVELOPER_TOOLCHAIN_DISCUSSION.md").exists()
    assert (tmp_path / "docs" / "DOC_FIRST_EXECUTION_GUIDELINES.md").exists()
    assert (tmp_path / "docs" / "RUNTIME_SURFACE_PROTECTION.md").exists()
    assert (tmp_path / "docs" / "LEFTOVER_UNIT_CONTRACT.md").exists()
    assert (tmp_path / "docs" / "SKILL_MECHANISM_V1_DRAFT.md").exists()
    assert (tmp_path / "docs" / "runbooks" / "multi-model-discussion-loop.md").exists()
    assert (tmp_path / "templates" / "doc_first_execution_guidelines.template.md").exists()
    assert (tmp_path / "templates" / "discussion_packet.template.md").exists()
    assert (tmp_path / "templates" / "execution_contract.template.md").exists()
    assert (tmp_path / "templates" / "skill.template.md").exists()
    assert (tmp_path / "scripts" / "discussion_pipeline.py").exists()
    assert (tmp_path / "scripts" / "validate-template.sh").exists()


def test_bootstrap_capabilities_copy_opt_in_assets(tmp_path: Path) -> None:
    result = bootstrap_repo(
        target_dir=tmp_path,
        project_name="Capability Demo",
        profile="minimal",
        capabilities=("closeout-audit", "runtime-guards", "git-hooks"),
    )

    assert (tmp_path / "scripts" / "closeout_truth_audit.py").exists()
    assert (tmp_path / "scripts" / "runtime_surface_guardrails.py").exists()
    assert (tmp_path / "scripts" / "install_git_hooks.sh").exists()
    assert (tmp_path / ".githooks" / "pre-commit").exists()
    assert (tmp_path / ".githooks" / "pre-push").exists()
    assert (tmp_path / ".github" / "runtime_surface_registry.py").exists()
    manifest = json.loads(
        (tmp_path / ".github" / "agent-framework-manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["schema_version"] == 2
    assert manifest["project_name"] == "Capability Demo"
    assert manifest["profile"] == "minimal"
    assert manifest["project_type"] == "cli-tool"
    assert manifest["capabilities"] == ["closeout-audit", "runtime-guards", "git-hooks"]
    assert manifest["developer_toolchain_contract"]["version"] == "v1"
    assert manifest["developer_toolchain_contract"]["enforcement"] == "required-core"
    assert manifest["developer_toolchain_contract"]["allow_surface_qualifiers"] is True
    assert ".github/agent-framework-manifest.json" in manifest["expected_files"]
    assert "scripts/closeout_truth_audit.py" in manifest["expected_files"]
    assert ".github/runtime_surface_registry.py" in manifest["expected_files"]
    assert result.capabilities == ("closeout-audit", "runtime-guards", "git-hooks")


def test_bootstrap_full_copies_examples_and_ci(tmp_path: Path) -> None:
    bootstrap_repo(
        target_dir=tmp_path,
        project_name="Demo Project",
        profile="full",
    )

    assert (tmp_path / ".github" / "workflows" / "ci.yml").exists()
    assert (tmp_path / "examples" / "reviewer_roles" / "10_docs_spec_drift_reviewer.md").exists()
    assert (tmp_path / "examples" / "skills" / "01_discussion_packet_workflow.md").exists()
    assert (tmp_path / "examples" / "skills" / "02_no_placeholder_runtime_guardrail.md").exists()
    assert (tmp_path / "examples" / "full_stack_project" / "README.md").exists()
    assert (tmp_path / "scripts" / "bootstrap_adoption.py").exists()
    assert (tmp_path / "templates" / "reviewer_role_profile.template.md").exists()


def test_bootstrap_dry_run_does_not_write_files(tmp_path: Path) -> None:
    result = bootstrap_repo(
        target_dir=tmp_path,
        project_name="Dry Run Demo",
        profile="minimal",
        dry_run=True,
    )

    assert result.created
    assert not (tmp_path / ".github" / "copilot-instructions.md").exists()


def test_bootstrap_uses_project_type_preset_for_cli_projects(tmp_path: Path) -> None:
    result = bootstrap_repo(
        target_dir=tmp_path,
        project_name="CLI Demo",
        profile="minimal",
        project_type="cli-tool",
    )

    project_context = (tmp_path / ".github" / "instructions" / "project-context.instructions.md").read_text(
        encoding="utf-8"
    )
    assert "Project type: cli-tool" in project_context
    assert "## Developer Toolchain" in project_context
    assert "Primary language: Python" in project_context
    assert "Package manager: pip" in project_context
    assert "run the primary user command with real arguments" in project_context
    assert "python -m build" in project_context
    assert result.project_type == "cli-tool"


def test_bootstrap_uses_qualified_surface_labels_for_full_stack_projects(tmp_path: Path) -> None:
    result = bootstrap_repo(
        target_dir=tmp_path,
        project_name="Full Stack Demo",
        profile="minimal",
        project_type="full-stack",
    )

    project_context = (tmp_path / ".github" / "instructions" / "project-context.instructions.md").read_text(
        encoding="utf-8"
    )
    assert "Project type: full-stack" in project_context
    assert "| Diagnostics (frontend) |" in project_context
    assert "| Run (backend) |" in project_context
    assert "| Repro path (primary journey) |" in project_context
    assert result.project_type == "full-stack"


def test_detect_project_type_prefers_backend_for_pyproject(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")

    assert detect_project_type(tmp_path) == "backend-api"
