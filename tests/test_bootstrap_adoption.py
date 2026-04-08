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
    assert (tmp_path / "docs" / "EXECUTION_PROOF_WAVE_1_PLAN.md").exists()
    assert (tmp_path / "docs" / "EXECUTION_PROOF_WAVE_2_PLAN.md").exists()
    assert (tmp_path / "docs" / "ANTI_DRIFT_RULE_REFACTOR_PLAN_V1.md").exists()
    assert (tmp_path / "docs" / "RUNTIME_SURFACE_PROTECTION.md").exists()
    assert (tmp_path / "docs" / "LEFTOVER_UNIT_CONTRACT.md").exists()
    assert (tmp_path / "docs" / "STRICT_ADOPTION_AND_VERIFICATION.md").exists()
    assert (tmp_path / "docs" / "SKILL_EXECUTION_LAYER_V1_DRAFT.md").exists()
    assert (tmp_path / "docs" / "SKILL_HARVEST_LOOP_V1_DRAFT.md").exists()
    assert (tmp_path / "docs" / "SKILL_MECHANISM_V1_DRAFT.md").exists()
    assert (tmp_path / "docs" / "runbooks" / "multi-model-discussion-loop.md").exists()
    assert (tmp_path / "docs" / "runbooks" / "state-reconciliation.md").exists()
    assert (tmp_path / "templates" / "doc_first_execution_guidelines.template.md").exists()
    assert (tmp_path / "templates" / "discussion_packet.template.md").exists()
    assert (tmp_path / "templates" / "drift_reconciliation_packet.template.md").exists()
    assert (tmp_path / "templates" / "execution_contract.template.md").exists()
    assert (tmp_path / "templates" / "execution_progress_receipt.template.md").exists()
    assert (tmp_path / "templates" / "skill_invocation_receipt.template.md").exists()
    assert (tmp_path / "templates" / "skill_candidate_packet.template.md").exists()
    assert (tmp_path / "templates" / "skill_promotion_receipt.template.md").exists()
    assert (tmp_path / "templates" / "skill.template.md").exists()
    assert (tmp_path / "templates" / "skill_tool_wrapper.template.md").exists()
    assert (tmp_path / "templates" / "skill_reviewer_gate.template.md").exists()
    assert (tmp_path / "templates" / "skill_pipeline.template.md").exists()
    assert (tmp_path / "templates" / "skill_artifact_generator.template.md").exists()
    assert (tmp_path / "examples" / "skills" / "01_discussion_packet_workflow.md").exists()
    assert (tmp_path / "examples" / "skills" / "06_bounded_artifact_generator.md").exists()
    assert (tmp_path / "examples" / "demo_project" / "README.md").exists()
    assert (
        tmp_path / "examples" / "demo_project" / "docs" / "runbooks" / "execution_contract_example.md"
    ).exists()
    assert (
        tmp_path
        / "examples"
        / "demo_project"
        / "tmp"
        / "git_audit"
        / "add_task_priority"
        / "progress_receipts"
        / "0001_priority_review_started.md"
    ).exists()
    assert (
        tmp_path / "examples" / "demo_project" / "tmp" / "git_audit" / "add_task_priority" / "drift_packet.md"
    ).exists()
    assert (tmp_path / "examples" / "full_stack_project" / "README.md").exists()
    assert (tmp_path / "examples" / "reviewer_roles" / "10_docs_spec_drift_reviewer.md").exists()
    assert (tmp_path / "scripts" / "closeout_truth_audit.py").exists()
    assert (tmp_path / "scripts" / "developer_toolchain_probe.py").exists()
    assert (tmp_path / "scripts" / "developer_toolchain_runner.py").exists()
    assert (tmp_path / "scripts" / "discussion_pipeline.py").exists()
    assert (tmp_path / "scripts" / "evaluation_pipeline.py").exists()
    assert (tmp_path / "scripts" / "review_dispatch.py").exists()
    assert (tmp_path / "scripts" / "state_sync_audit.py").exists()
    assert (tmp_path / "scripts" / "state_sync_pipeline.py").exists()
    assert (tmp_path / "scripts" / "strict_adoption_audit.py").exists()
    assert (tmp_path / "scripts" / "skill_evolution_pipeline.py").exists()
    assert (tmp_path / "scripts" / "validate-template.sh").exists()
    assert (tmp_path / "templates" / "adoption_verification_packet.template.md").exists()
    assert (tmp_path / "templates" / "developer_toolchain_probe_receipt.template.md").exists()
    assert (tmp_path / "templates" / "developer_toolchain_run_receipt.template.md").exists()
    assert (tmp_path / "templates" / "evaluation_request.template.md").exists()
    assert (tmp_path / "templates" / "evaluation_report.template.md").exists()
    assert (tmp_path / "templates" / "local_executor_registry.template.json").exists()
    assert (tmp_path / "templates" / "review_dispatch_packet.template.md").exists()
    assert (tmp_path / ".github" / "local_executor_registry.json").exists()


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
    assert manifest["schema_version"] == 4
    assert manifest["project_name"] == "Capability Demo"
    assert manifest["profile"] == "minimal"
    assert manifest["project_type"] == "cli-tool"
    assert manifest["capabilities"] == ["closeout-audit", "runtime-guards", "git-hooks"]
    assert manifest["developer_toolchain_contract"]["version"] == "v1"
    assert manifest["developer_toolchain_contract"]["enforcement"] == "required-core"
    assert manifest["developer_toolchain_contract"]["allow_surface_qualifiers"] is True
    assert "strict_adoption_contract" not in manifest
    assert "developer_toolchain_probe_contract" not in manifest
    assert "developer_toolchain_runner_contract" not in manifest
    assert "independent_evaluation_contract" not in manifest
    assert "executor_review_contract" not in manifest
    assert ".github/agent-framework-manifest.json" in manifest["expected_files"]
    assert "scripts/closeout_truth_audit.py" in manifest["expected_files"]
    assert ".github/runtime_surface_registry.py" in manifest["expected_files"]
    assert ".github/local_executor_registry.json" not in manifest["expected_files"]
    assert not (tmp_path / ".github" / "local_executor_registry.json").exists()
    assert result.capabilities == ("closeout-audit", "runtime-guards", "git-hooks")


def test_bootstrap_standard_ships_execution_proof_round_trip(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    project_context = adopted_root / ".github" / "instructions" / "project-context.instructions.md"
    project_context.write_text(
        """# Adopted Demo — Project Context\n\n## Project Map\n\n| Path | Purpose |\n|---|---|\n| `src/` | CLI implementation |\n| `docs/` | Project docs |\n| `tests/` | Regression tests |\n| `.github/` | Agent policy and adapter |\n\n## Canonical Docs\n\n| Doc | Purpose |\n|---|---|\n| `README.md` | Project entry point |\n| `docs/INDEX.md` | Canonical doc index |\n| `ROADMAP.md` | Planned milestones |\n| `session_state.md` | Cross-session state |\n\n## Validation Toolchain\n\nProject type: cli-tool\n\n| Tier | Tool | Command |\n|---|---|---|\n| Unit | pytest | `python -m pytest tests/ -q` |\n| Integration | bootstrap | `python scripts/bootstrap_adoption.py --help` |\n| End-to-end | smoke | `python -c \"print('smoke ok')\"` |\n\n## Developer Toolchain\n\nPrimary language: Python\n\nPackage manager: pip\n\n| Surface | Command or source | Scope | Status | Fallback or stop | Notes |\n|---|---|---|---|---|---|\n| Diagnostics | `python -c \"print('diag ok')\"` | `module` | `declared-unverified` | `Stop after diagnostics` | `Syntax smoke` |\n| Run | `python -c \"print('run ok')\"` | `service` | `declared-unverified` | `Use diagnostics if run is unavailable` | `Main run path` |\n| Health or smoke | `python -c \"print('smoke ok')\"` | `service` | `declared-unverified` | `Stop after smoke` | `Fast runtime proof` |\n| Repro path | `python -c \"print('repro ok')\"` | `service` | `declared-unverified` | `Stop after repro` | `User repro path` |\n| Build | `python -c \"print('build ok')\"` | `module` | `declared-unverified` | `Stop after build` | `Build path` |\n| Lint | `python -c \"print('lint ok')\"` | `module` | `declared-unverified` | `Stop after lint` | `Lint path` |\n""",
        encoding="utf-8",
    )

    validation_evidence = adopted_root / "tmp" / "adoption_verification" / "validation.txt"
    review_artifact = adopted_root / "tmp" / "adoption_verification" / "review.md"
    validation_evidence.parent.mkdir(parents=True, exist_ok=True)
    validation_evidence.write_text("status=passed\nAll tests passed\n", encoding="utf-8")
    review_artifact.write_text("Verdict: PASS\nIndependent review accepted.\n", encoding="utf-8")

    adoption_output = adopted_root / "tmp" / "adoption_verification" / "packet.md"
    adoption_script = adopted_root / "scripts" / "strict_adoption_audit.py"
    adoption = subprocess.run(
        [
            sys.executable,
            str(adoption_script),
            "--root",
            str(adopted_root),
            "--validation-evidence",
            f"validator={validation_evidence.relative_to(adopted_root)}",
            "--review-artifact",
            f"cli-review={review_artifact.relative_to(adopted_root)}",
            "--output",
            str(adoption_output),
        ],
        cwd=adopted_root,
        check=True,
        capture_output=True,
        text=True,
    )

    probe_output = adopted_root / "tmp" / "toolchain_probe_receipts" / "probe.md"
    probe_script = adopted_root / "scripts" / "developer_toolchain_probe.py"
    probe = subprocess.run(
        [
            sys.executable,
            str(probe_script),
            "--root",
            str(adopted_root),
            "--surface",
            "Diagnostics",
            "--surface",
            "Build",
            "--output",
            str(probe_output),
        ],
        cwd=adopted_root,
        check=True,
        capture_output=True,
        text=True,
    )

    assert adoption.stdout.strip() == str(adoption_output)
    assert probe.stdout.strip() == str(probe_output)

    adoption_text = adoption_output.read_text(encoding="utf-8")
    probe_text = probe_output.read_text(encoding="utf-8")
    assert "- Adoption verdict: fully-adopted" in adoption_text
    assert "project-context-adapter" in adoption_text
    assert "developer-toolchain-probe" in adoption_text
    assert "| Diagnostics | module | declared-unverified | success | 0 |" in probe_text
    assert "| Build | module | declared-unverified | success | 0 |" in probe_text


def test_bootstrap_standard_ships_wave_2_round_trip(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    project_context = adopted_root / ".github" / "instructions" / "project-context.instructions.md"
    updated = project_context.read_text(encoding="utf-8")
    updated = updated.replace("`pyright .`", "`python -c \"print('diag ok')\"`")
    project_context.write_text(updated, encoding="utf-8")

    runner_output = adopted_root / "tmp" / "toolchain_run_receipts" / "runner.md"
    runner = subprocess.run(
        [
            sys.executable,
            str(adopted_root / "scripts" / "developer_toolchain_runner.py"),
            "--root",
            str(adopted_root),
            "run-surface",
            "--surface",
            "Diagnostics",
            "--output",
            str(runner_output),
        ],
        cwd=adopted_root,
        check=True,
        capture_output=True,
        text=True,
    )

    evaluation_request = subprocess.run(
        [
            sys.executable,
            str(adopted_root / "scripts" / "evaluation_pipeline.py"),
            "init-request",
            "--task-id",
            "task-1",
            "--generator",
            "implementer",
            "--evaluator",
            "auditor",
            "--review-scope",
            "user-facing",
            "--goal",
            "Review the generated output.",
            "--uac-focus",
            "- [x] output rendered",
            "--evidence-to-review",
            "- receipt",
            "--allowed-files",
            "- src/example.py",
            "--do-not-touch",
            "- docs/archive/",
            "--output-root",
            str(adopted_root / "tmp" / "evaluation"),
        ],
        cwd=adopted_root,
        check=True,
        capture_output=True,
        text=True,
    )
    evaluation_report = subprocess.run(
        [
            sys.executable,
            str(adopted_root / "scripts" / "evaluation_pipeline.py"),
            "record-report",
            "--task-id",
            "task-1",
            "--evaluator",
            "auditor",
            "--verdict",
            "PASS",
            "--uac-coverage",
            "- [x] output rendered",
            "--gap-check",
            "No additional user-visible gaps found.",
            "--evidence-anchors",
            "- receipt",
            "--output-root",
            str(adopted_root / "tmp" / "evaluation"),
        ],
        cwd=adopted_root,
        check=True,
        capture_output=True,
        text=True,
    )

    registry_path = adopted_root / ".github" / "local_executor_registry.json"
    registry_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "executors": [
                    {
                        "name": "alpha",
                        "probe_command": f"{sys.executable} -c \"import sys; sys.exit(0)\"",
                        "review_command": f"{sys.executable} -c \"from pathlib import Path; print(Path(r'{'{prompt_file}'}').read_text(encoding='utf-8').strip())\"",
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    prompt_file = adopted_root / "tmp" / "review_prompt.txt"
    prompt_file.write_text("wave 2 review", encoding="utf-8")
    review_packet = subprocess.run(
        [
            sys.executable,
            str(adopted_root / "scripts" / "review_dispatch.py"),
            "--root",
            str(adopted_root),
            "--review-id",
            "review-1",
            "dispatch",
            "--prompt-file",
            str(prompt_file),
        ],
        cwd=adopted_root,
        check=True,
        capture_output=True,
        text=True,
    )

    assert runner.stdout.strip() == str(runner_output)
    assert "- Outcome: success" in runner_output.read_text(encoding="utf-8")
    assert "evaluation_request.md" in evaluation_request.stdout
    assert "evaluation_report.md" in evaluation_report.stdout
    assert "- Verdict: PASS" in Path(evaluation_report.stdout.strip()).read_text(encoding="utf-8")
    packet_path = Path(review_packet.stdout.strip())
    assert "| alpha | available | completed |" in packet_path.read_text(encoding="utf-8")


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
    assert (tmp_path / "examples" / "skills" / "03_developer_toolchain_wrapper.md").exists()
    assert (tmp_path / "examples" / "skills" / "04_receipt_anchored_reviewer.md").exists()
    assert (tmp_path / "examples" / "skills" / "05_staged_handoff_pipeline.md").exists()
    assert (tmp_path / "examples" / "skills" / "06_bounded_artifact_generator.md").exists()
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
