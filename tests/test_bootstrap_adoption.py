from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from contextlib import redirect_stdout
from io import StringIO
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
main = MODULE.main


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
    assert (tmp_path / "docs" / "SKILL_EXECUTION_LAYER_V1_DRAFT.md").exists()
    assert (tmp_path / "docs" / "SKILL_HARVEST_LOOP_V1_DRAFT.md").exists()
    assert (tmp_path / "docs" / "SKILL_MECHANISM_V1_DRAFT.md").exists()
    assert (tmp_path / "docs" / "runbooks" / "multi-model-discussion-loop.md").exists()
    assert (tmp_path / "templates" / "doc_first_execution_guidelines.template.md").exists()
    assert (tmp_path / "templates" / "discussion_packet.template.md").exists()
    assert (tmp_path / "templates" / "execution_contract.template.md").exists()
    assert (tmp_path / "templates" / "skill_invocation_receipt.template.md").exists()
    assert (tmp_path / "templates" / "skill_candidate_packet.template.md").exists()
    assert (tmp_path / "templates" / "skill_promotion_receipt.template.md").exists()
    assert (tmp_path / "templates" / "skill.template.md").exists()
    assert (tmp_path / "scripts" / "discussion_pipeline.py").exists()
    assert (tmp_path / "scripts" / "skill_evolution_pipeline.py").exists()
    assert (tmp_path / "scripts" / "validate-template.sh").exists()


def test_bootstrap_standard_ships_runnable_skill_execution_round_trip(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    invocation_output = adopted_root / "tmp" / "skill_execution" / "invocation.md"
    candidate_output = adopted_root / "tmp" / "skill_execution" / "candidate.md"
    script_path = adopted_root / "scripts" / "skill_evolution_pipeline.py"

    invocation = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "init-invocation",
            "--receipt-id",
            "receipt-1",
            "--invocation-id",
            "invoke-1",
            "--skill-id",
            "discussion-packet-first",
            "--trigger-class",
            "explicit-request",
            "--execution-mode",
            "host-runtime",
            "--outcome",
            "success",
            "--candidate-recommendation",
            "CAPTURED",
            "--trigger-reason",
            "- The host requested the discussion workflow.",
            "--references-loaded",
            "| discussion runbook | docs/runbooks/multi-model-discussion-loop.md | yes | Needed for the canonical round flow |",
            "--outcome-summary",
            "- The invocation produced a durable discussion packet.",
            "--evidence-links",
            "| packet-1 | task artifact | Links runtime execution back to the packet artifact |",
            "--follow-up-recommendation",
            "- Capture this as reusable runtime evidence.",
            "--output",
            str(invocation_output),
        ],
        cwd=adopted_root,
        check=True,
        capture_output=True,
        text=True,
    )

    candidate = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "init-candidate",
            "--candidate-id",
            "candidate-1",
            "--source-skill",
            "discussion-packet-first",
            "--harvest-source",
            "invocation receipt",
            "--proposed-by",
            "skill-harvester",
            "--confidence-tier",
            "high",
            "--evolution-mode",
            "DERIVED",
            "--candidate-trigger",
            "repeated-successful-reuse",
            "--invocation-ids",
            "invoke-1",
            "--parent-lineage",
            "discussion-packet-first",
            "--target-fields",
            "- references\n- entry_instructions",
            "--proposed-delta",
            "- Strengthen the runtime packet append workflow.",
            "--evidence-bundle",
            "| receipt-1 | invocation | Shows the runtime path completed successfully |",
            "--escalation-triggers",
            "- Escalate if canonical trigger scope needs widening.",
            "--notes",
            "- Keep canonical mutation behind promotion review.",
            "--output",
            str(candidate_output),
        ],
        cwd=adopted_root,
        check=True,
        capture_output=True,
        text=True,
    )

    assert invocation.stdout.strip() == str(invocation_output)
    assert candidate.stdout.strip() == str(candidate_output)

    invocation_text = invocation_output.read_text(encoding="utf-8")
    candidate_text = candidate_output.read_text(encoding="utf-8")

    assert "- Execution Mode: host-runtime" in invocation_text
    assert "discussion runbook" in invocation_text
    assert "packet-1" in invocation_text
    assert "- Evolution Mode: DERIVED" in candidate_text
    assert "- Invocation IDs: invoke-1" in candidate_text
    assert "receipt-1" in candidate_text


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


def test_main_prints_skill_accumulation_guidance_for_standard_profile(tmp_path: Path, monkeypatch) -> None:
    output = StringIO()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "bootstrap_adoption.py",
            str(tmp_path),
            "--project-name",
            "Std Demo",
            "--profile",
            "standard",
            "--dry-run",
        ],
    )

    with redirect_stdout(output):
        exit_code = main()

    rendered = output.getvalue()
    assert exit_code == 0
    assert "initialize at least one repository-specific skill before broad rollout" in rendered
    assert "Do not promote raw transcript excerpts straight into canonical skills" in rendered


def test_main_tells_minimal_profile_users_to_add_standard_for_skill_governance(
    tmp_path: Path, monkeypatch
) -> None:
    output = StringIO()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "bootstrap_adoption.py",
            str(tmp_path),
            "--project-name",
            "Min Demo",
            "--profile",
            "minimal",
            "--dry-run",
        ],
    )

    with redirect_stdout(output):
        exit_code = main()

    rendered = output.getvalue()
    assert exit_code == 0
    assert "add the standard profile before rollout so the SKILL and harvest-governance surfaces ship together" in rendered
