from __future__ import annotations

import importlib.util
import json
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


def test_parse_developer_toolchain_entries_handles_pipe_in_command() -> None:
    _, _, entries = MODULE._parse_developer_toolchain_entries(
        """## Developer Toolchain\n\nPrimary language: Python\n\nPackage manager: pip\n\n| Surface | Command or source | Scope | Status | Fallback or stop | Notes |\n|---|---|---|---|---|---|\n| Diagnostics | `python -c \"print('ok')\" | cat` | `module` | `verified-working` | `Stop` | `Pipe-safe` |\n"""
    )

    assert len(entries) == 1
    assert entries[0].command_or_source == 'python -c "print(\'ok\')" | cat'


def test_validate_repo_reports_invalid_adopter_manifest_schema_version(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    manifest_path = adopted_root / ".github" / "agent-framework-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["schema_version"] = 2
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    issues = validate_repo(adopted_root)

    assert ValidationIssue(
        "invalid-adopter-manifest-schema-version",
        ".github/agent-framework-manifest.json: expected schema_version 4",
    ) in issues


def test_validate_repo_reports_missing_strict_adoption_contract(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    manifest_path = adopted_root / ".github" / "agent-framework-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.pop("strict_adoption_contract")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    issues = validate_repo(adopted_root)

    assert ValidationIssue(
        "missing-strict-adoption-contract",
        ".github/agent-framework-manifest.json: missing strict_adoption_contract",
    ) in issues


def test_validate_repo_accepts_minimal_adopter_without_wave_2_contracts(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="minimal",
        project_type="cli-tool",
    )

    issues = validate_repo(adopted_root)

    assert not any(issue.kind.startswith("missing-strict-adoption-contract") for issue in issues)
    assert not any(issue.kind.startswith("missing-developer-toolchain-probe-contract") for issue in issues)
    assert not any(issue.kind.startswith("missing-developer-toolchain-runner-contract") for issue in issues)
    assert not any(issue.kind.startswith("missing-independent-evaluation-contract") for issue in issues)
    assert not any(issue.kind.startswith("missing-executor-review-contract") for issue in issues)


def test_validate_repo_reports_missing_developer_toolchain_probe_contract_key(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    manifest_path = adopted_root / ".github" / "agent-framework-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["developer_toolchain_probe_contract"].pop("receipt_output_dir")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    issues = validate_repo(adopted_root)

    assert ValidationIssue(
        "missing-developer-toolchain-probe-contract-key",
        ".github/agent-framework-manifest.json: developer_toolchain_probe_contract is missing key 'receipt_output_dir'",
    ) in issues


def test_validate_repo_reports_missing_executor_review_contract(tmp_path: Path) -> None:
    adopted_root = tmp_path / "adopted"
    bootstrap_repo(
        target_dir=adopted_root,
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    manifest_path = adopted_root / ".github" / "agent-framework-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.pop("executor_review_contract")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    issues = validate_repo(adopted_root)

    assert ValidationIssue(
        "missing-executor-review-contract",
        ".github/agent-framework-manifest.json: missing executor_review_contract",
    ) in issues


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


def test_validate_repo_reports_stale_root_session_state_no_active_work_with_next_step(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    session_state = repo_copy / "session_state.md"
    updated = session_state.read_text(encoding="utf-8")
    updated = updated.replace(
        "**Next Planned Step**: None until the next framework workstream is opened.",
        "**Next Planned Step**: Independent review, then git closeout.",
        1,
    )
    session_state.write_text(updated, encoding="utf-8")

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "stale-root-session-state",
        "session_state.md: 'Current Step' says no active work but 'Next Planned Step' is not none-like",
    ) in issues


def test_validate_repo_reports_stale_root_session_state_no_active_work_with_unchecked_uac(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    session_state = repo_copy / "session_state.md"
    updated = session_state.read_text(encoding="utf-8")
    updated = updated.replace(
        "- [x] When a standard or full adopter is bootstrapped, it receives the Wave 2 runner, evaluation, and executor-review assets with explicit manifest contract sections.",
        "- [ ] When a standard or full adopter is bootstrapped, it receives the Wave 2 runner, evaluation, and executor-review assets with explicit manifest contract sections.",
        1,
    )
    session_state.write_text(updated, encoding="utf-8")

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "stale-root-session-state",
        "session_state.md: 'Current Step' says no active work while User Acceptance Criteria still contain unchecked items",
    ) in issues


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


def test_validate_repo_reports_missing_task_packet_checkpoint_contract(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    task_packet_template = repo_copy / "templates" / "git_audit_task_packet.template.md"
    task_packet_template.write_text(
        task_packet_template.read_text(encoding="utf-8").replace("## Checkpoint Contract\n\n", "", 1),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "missing-task-packet-snippet",
        "templates/git_audit_task_packet.template.md: ## Checkpoint Contract",
    ) in issues


def test_validate_repo_reports_missing_state_sync_hook(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    pre_commit = repo_copy / ".githooks" / "pre-commit"
    pre_commit.write_text(
        pre_commit.read_text(encoding="utf-8").replace(
            'if [[ -f "${ROOT}/scripts/state_sync_audit.py" ]]; then\n  PYTHONDONTWRITEBYTECODE=1 python3 "${ROOT}/scripts/state_sync_audit.py" --root "${ROOT}"\nfi\n\n',
            "",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue("missing-state-sync-hook", ".githooks/pre-commit") in issues


def test_validate_repo_reports_missing_capability_asset(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)
    (repo_copy / "scripts" / "closeout_truth_audit.py").unlink()

    issues = validate_repo(repo_copy)

    assert ValidationIssue("missing-file", "scripts/closeout_truth_audit.py") in issues


def test_validate_repo_reports_missing_skill_heading(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    skill_example = repo_copy / "examples" / "skills" / "01_discussion_packet_workflow.md"
    skill_example.write_text(
        skill_example.read_text(encoding="utf-8").replace("### Negative Triggers\n", "", 1),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "missing-skill-heading",
        "examples/skills/01_discussion_packet_workflow.md: ### Negative Triggers",
    ) in issues


def test_validate_repo_reports_missing_skill_review_matrix_row(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    skill_example = repo_copy / "examples" / "skills" / "01_discussion_packet_workflow.md"
    skill_example.write_text(
        skill_example.read_text(encoding="utf-8").replace(
            "| `degradation` | `1-3` | `single-reviewer` | `dual-reviewer`; owner review required | `delegated-reviewed` |\n",
            "",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "missing-skill-review-matrix-row",
        "examples/skills/01_discussion_packet_workflow.md: receipt and review matrix is missing row 'degradation'",
    ) in issues


def test_validate_repo_reports_invalid_skill_promotion_tier(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    skill_example = repo_copy / "examples" / "skills" / "01_discussion_packet_workflow.md"
    skill_example.write_text(
        skill_example.read_text(encoding="utf-8").replace(
            "| `references` | `1-4` | `single-reviewer` | `single-reviewer`; must keep reference truthfulness | `delegated-safe` |",
            "| `references` | `1-4` | `single-reviewer` | `single-reviewer`; must keep reference truthfulness | `mystery-tier` |",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "invalid-skill-promotion-tier",
        "examples/skills/01_discussion_packet_workflow.md: row 'references' uses unsupported promotion tier 'mystery-tier'",
    ) in issues


def test_validate_repo_reports_invalid_skill_governance_promotion_tier(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    skill_example = repo_copy / "examples" / "skills" / "01_discussion_packet_workflow.md"
    skill_example.write_text(
        skill_example.read_text(encoding="utf-8").replace(
            "| `governance` | `1-2 only` | `dual-reviewer` | `dual-reviewer`; owner review required | `human-only` |",
            "| `governance` | `1-2 only` | `dual-reviewer` | `dual-reviewer`; owner review required | `delegated-reviewed` |",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "invalid-skill-governance-promotion-tier",
        "examples/skills/01_discussion_packet_workflow.md: row 'governance' must use promotion tier 'human-only'",
    ) in issues


def test_validate_repo_reports_missing_skill_reference_path(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    skill_example = repo_copy / "examples" / "skills" / "02_no_placeholder_runtime_guardrail.md"
    skill_example.write_text(
        skill_example.read_text(encoding="utf-8").replace(
            "docs/RUNTIME_SURFACE_PROTECTION.md",
            "docs/MISSING_RUNTIME_SURFACE_PROTECTION.md",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "missing-skill-reference-path",
        "examples/skills/02_no_placeholder_runtime_guardrail.md: reference path 'docs/MISSING_RUNTIME_SURFACE_PROTECTION.md' does not exist",
    ) in issues


def test_validate_repo_reports_missing_skill_invocation_template_snippet(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    invocation_template = repo_copy / "templates" / "skill_invocation_receipt.template.md"
    invocation_template.write_text(
        invocation_template.read_text(encoding="utf-8").replace("- Invocation ID: [invocation-id]\n", "", 1),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "missing-skill-invocation-template-snippet",
        "templates/skill_invocation_receipt.template.md: - Invocation ID:",
    ) in issues


def test_validate_repo_reports_missing_five_pattern_doc_snippet(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    mechanism_doc = repo_copy / "docs" / "SKILL_MECHANISM_V1_DRAFT.md"
    mechanism_doc.write_text(
        mechanism_doc.read_text(encoding="utf-8").replace(
            "2. Wrapper, Reviewer, and Pipeline may ship only as execution scaffolds or starter surfaces\n",
            "",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "missing-skill-five-pattern-doc-snippet",
        "docs/SKILL_MECHANISM_V1_DRAFT.md: Wrapper, Reviewer, and Pipeline may ship only as execution scaffolds or starter surfaces",
    ) in issues


def test_validate_repo_reports_missing_pattern_starter_snippet(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    wrapper_template = repo_copy / "templates" / "skill_tool_wrapper.template.md"
    wrapper_template.write_text(
        wrapper_template.read_text(encoding="utf-8").replace(
            "- Invocation Receipt Linkage: record the wrapper outcome in a closeout receipt or `templates/skill_invocation_receipt.template.md` derived artifact when runtime lineage matters.\n",
            "",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "missing-skill-pattern-starter-snippet",
        "templates/skill_tool_wrapper.template.md: - Invocation Receipt Linkage:",
    ) in issues


def test_validate_repo_reports_missing_pattern_example_snippet(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    wrapper_example = repo_copy / "examples" / "skills" / "03_developer_toolchain_wrapper.md"
    wrapper_example.write_text(
        wrapper_example.read_text(encoding="utf-8").replace(
            "- Invocation Receipt Linkage: when reuse evidence matters, tie the run to `templates/skill_invocation_receipt.template.md` or another receipt-bearing closeout artifact.\n",
            "",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "missing-skill-pattern-starter-snippet",
        "examples/skills/03_developer_toolchain_wrapper.md: - Invocation Receipt Linkage:",
    ) in issues


def test_validate_repo_reports_wrapper_missing_adapter_reference(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    wrapper_example = repo_copy / "examples" / "skills" / "03_developer_toolchain_wrapper.md"
    wrapper_example.write_text(
        wrapper_example.read_text(encoding="utf-8").replace(
            "| project context adapter | .github/instructions/project-context.instructions.md | yes | Declares the available surfaces, statuses, and fallback rules |\n",
            "",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "skill-wrapper-missing-reference",
        "examples/skills/03_developer_toolchain_wrapper.md: wrapper contract must reference '.github/instructions/project-context.instructions.md'",
    ) in issues


def test_validate_repo_reports_wrapper_missing_surface_binding(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    wrapper_example = repo_copy / "examples" / "skills" / "03_developer_toolchain_wrapper.md"
    wrapper_example.write_text(
        wrapper_example.read_text(encoding="utf-8").replace(
            "- Wrapper Target Surface: one row such as `Diagnostics`, `Health or smoke`, or `Repro path` from the Developer Toolchain table in `.github/instructions/project-context.instructions.md`.\n",
            "- Wrapper Target Surface: one declared row from the adapter.\n",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "skill-wrapper-missing-surface-binding",
        "examples/skills/03_developer_toolchain_wrapper.md: wrapper entry instructions must name at least one declared Developer Toolchain surface",
    ) in issues


def test_validate_repo_reports_reviewer_missing_receipt_reference(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    reviewer_example = repo_copy / "examples" / "skills" / "04_receipt_anchored_reviewer.md"
    reviewer_example.write_text(
        reviewer_example.read_text(encoding="utf-8").replace(
            "| audit receipt template | templates/git_audit_receipt.template.md | yes | Canonical sink for structured review verdicts |\n",
            "",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "skill-reviewer-missing-reference",
        "examples/skills/04_receipt_anchored_reviewer.md: reviewer contract must reference 'templates/git_audit_receipt.template.md'",
    ) in issues


def test_validate_repo_reports_reviewer_missing_verdict_contract(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    reviewer_example = repo_copy / "examples" / "skills" / "04_receipt_anchored_reviewer.md"
    reviewer_example.write_text(
        reviewer_example.read_text(encoding="utf-8").replace(
            "- Verdict Contract: require PASS, CONDITIONAL, or FAIL rather than open-ended sentiment.\n",
            "- Verdict Contract: require a structured verdict rather than open-ended sentiment.\n",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "skill-reviewer-missing-verdict-contract",
        "examples/skills/04_receipt_anchored_reviewer.md: reviewer entry instructions must name PASS, CONDITIONAL, and FAIL verdicts",
    ) in issues


def test_validate_repo_reports_pipeline_missing_handoff_reference(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    pipeline_example = repo_copy / "examples" / "skills" / "05_staged_handoff_pipeline.md"
    pipeline_example.write_text(
        pipeline_example.read_text(encoding="utf-8").replace(
            "| audit handoff template | templates/git_audit_handoff_packet.template.md | yes | Resume artifact when execution stops mid-pipeline |\n",
            "",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "skill-pipeline-missing-reference",
        "examples/skills/05_staged_handoff_pipeline.md: pipeline contract must reference 'templates/git_audit_handoff_packet.template.md'",
    ) in issues


def test_validate_repo_reports_pipeline_missing_checkpoint_rule(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    pipeline_example = repo_copy / "examples" / "skills" / "05_staged_handoff_pipeline.md"
    pipeline_example.write_text(
        pipeline_example.read_text(encoding="utf-8").replace(
            "- Checkpoint Rule: finish each stage with validation evidence or an explicit blocker.\n",
            "- Checkpoint Rule: finish each stage before the next one starts.\n",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "skill-pipeline-missing-checkpoint-rule",
        "examples/skills/05_staged_handoff_pipeline.md: pipeline entry instructions must describe stage checkpoints with validation or blocker output",
    ) in issues


def test_validate_repo_reports_generator_missing_template_reference(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    generator_example = repo_copy / "examples" / "skills" / "06_bounded_artifact_generator.md"
    generator_example.write_text(
        generator_example.read_text(encoding="utf-8").replace(
            "| skill candidate packet template | templates/skill_candidate_packet.template.md | no | Example schema for bounded generator output |\n",
            "",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "skill-generator-missing-template-reference",
        "examples/skills/06_bounded_artifact_generator.md: generator contract must reference at least one schema-backed artifact template",
    ) in issues


def test_validate_repo_reports_generator_missing_schema_boundary(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    generator_example = repo_copy / "examples" / "skills" / "06_bounded_artifact_generator.md"
    updated = generator_example.read_text(encoding="utf-8")
    updated = updated.replace(
        "- Artifact Contract: generate only artifact families already defined by stable schema surfaces such as `templates/discussion_packet.template.md`, `templates/git_audit_task_packet.template.md`, or the SKILL execution-layer templates.\n",
        "- Artifact Contract: generate only named artifact families already defined by repository surfaces.\n",
        1,
    )
    updated = updated.replace(
        "- Stop Rule: if the artifact lacks a stable schema or a validator-visible path, stop and do not treat the task as safe generator work.\n",
        "- Stop Rule: if the artifact lacks a validator-visible path, stop and do not treat the task as safe generator work.\n",
        1,
    )
    generator_example.write_text(updated, encoding="utf-8")

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "skill-generator-missing-schema-boundary",
        "examples/skills/06_bounded_artifact_generator.md: generator entry instructions must state a stable schema boundary",
    ) in issues


def test_validate_repo_reports_runtime_claim_without_degradation(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    wrapper_example = repo_copy / "examples" / "skills" / "03_developer_toolchain_wrapper.md"
    wrapper_example.write_text(
        wrapper_example.read_text(encoding="utf-8").replace(
            "- If the chosen toolchain row is missing or still design-only, block the wrapper claim and record the missing runtime contract instead of silently picking another path.\n",
            "- Runtime support is described elsewhere.\n",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "skill-runtime-claim-without-degradation",
        "examples/skills/03_developer_toolchain_wrapper.md: runtime-capability claims in entry instructions need a matching degradation path",
    ) in issues


def test_validate_repo_reports_entry_instructions_inline_code_block(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    workflow_example = repo_copy / "examples" / "skills" / "01_discussion_packet_workflow.md"
    workflow_example.write_text(
        workflow_example.read_text(encoding="utf-8").replace(
            "## References\n",
            "```text\ninline command\n```\n\n## References\n",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "skill-entry-instructions-inline-content",
        "examples/skills/01_discussion_packet_workflow.md: entry instructions must not inline fenced code blocks",
    ) in issues


def test_validate_repo_reports_standard_profile_bootstrap_drift(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    bootstrap_script = repo_copy / "scripts" / "bootstrap_adoption.py"
    bootstrap_script.write_text(
        bootstrap_script.read_text(encoding="utf-8").replace(
            '        "examples/demo_project/docs/runbooks/execution_contract_example.md",\n',
            "",
            1,
        ),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "bootstrap-profile-mismatch",
        "standard profile missing 'examples/demo_project/docs/runbooks/execution_contract_example.md'",
    ) in issues


def test_validate_repo_reports_missing_skill_candidate_template_lineage_snippet(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    candidate_template = repo_copy / "templates" / "skill_candidate_packet.template.md"
    candidate_template.write_text(
        candidate_template.read_text(encoding="utf-8").replace("- Evolution Mode: [FIX | DERIVED | CAPTURED]\n", "", 1),
        encoding="utf-8",
    )

    issues = validate_repo(repo_copy)

    assert ValidationIssue(
        "missing-skill-candidate-template-snippet",
        "templates/skill_candidate_packet.template.md: - Evolution Mode:",
    ) in issues


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


def test_validate_repo_allows_missing_optional_build_surface_for_bootstrapped_adopted_repo(
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
    ) not in issues


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


def test_collect_advisories_reports_weak_skill_trigger_bullet(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    workflow_example = repo_copy / "examples" / "skills" / "01_discussion_packet_workflow.md"
    workflow_example.write_text(
        workflow_example.read_text(encoding="utf-8").replace(
            "- Use when the task is primarily about choosing a direction, comparing alternatives, or reviewing a plan with real tradeoffs.\n",
            "- Use when needed.\n",
            1,
        ),
        encoding="utf-8",
    )

    advisories = collect_advisories(repo_copy)

    assert any(advisory.kind == "weak-skill-trigger-bullet" for advisory in advisories)


def test_collect_advisories_reports_dense_entry_instructions(tmp_path: Path) -> None:
    repo_copy = tmp_path / "repo"
    shutil.copytree(REPO_ROOT, repo_copy)

    workflow_example = repo_copy / "examples" / "skills" / "01_discussion_packet_workflow.md"
    workflow_example.write_text(
        workflow_example.read_text(encoding="utf-8").replace(
            "## References\n",
            "- Extra step one.\n- Extra step two.\n- Extra step three.\n- Extra step four.\n- Extra step five.\n- Extra step six.\n\n## References\n",
            1,
        ),
        encoding="utf-8",
    )

    advisories = collect_advisories(repo_copy)

    assert any(advisory.kind == "skill-entry-instructions-too-dense" for advisory in advisories)


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


def test_validate_repo_reports_invalid_adopted_skill_type(tmp_path: Path) -> None:
    bootstrap_repo(
        target_dir=tmp_path / "adopted",
        project_name="Adopted Demo",
        profile="standard",
        project_type="cli-tool",
    )

    skill_path = tmp_path / "adopted" / "docs" / "skills" / "SKILL.md"
    skill_path.parent.mkdir(parents=True, exist_ok=True)
    skill_path.write_text(
        """# Sample Skill\n\n- ID: sample-skill\n- Type: mystery\n- Owner: adopted-team\n- Review Threshold: single-reviewer\n\n## Purpose\n\nA sample skill.\n\n## Triggers\n\n### Positive Triggers\n\n- Use when the sample condition is present.\n\n### Negative Triggers\n\n- Do not use when the sample non-trigger is present.\n\n### Expected Effect\n\n- The agent changes behavior in a known way.\n\n## Entry Instructions\n\n- Follow the sample steps.\n\n## References\n\n| Name | Path | Required at invocation | Purpose |\n|---|---|---|---|\n| sample | README.md | no | Example only |\n\n## Governance\n\n### Allowed Evidence\n\n- Human-reviewed receipts.\n\n### Reviewer Gate\n\n- Maintainer review required.\n\n### Forbidden Direct Update Inputs\n\n- Raw transcripts.\n\n## Receipt And Review Matrix\n\n| Field | Proposal evidence tiers | Minimum reviewer threshold | Guardrail override |\n|---|---|---|---|\n| `purpose` | `1-2 only` | `single-reviewer` | `dual-reviewer`; no auto-proposed rewrite |\n| `triggers` | `1-3` | `single-reviewer` | `dual-reviewer`; no auto-proposed rewrite |\n| `entry_instructions` | `1-3` | `single-reviewer` | `dual-reviewer`; no auto-proposed rewrite |\n| `references` | `1-4` | `single-reviewer` | `single-reviewer`; must keep reference truthfulness |\n| `governance` | `1-2 only` | `dual-reviewer` | `dual-reviewer`; owner review required |\n| `degradation` | `1-3` | `single-reviewer` | `dual-reviewer`; owner review required |\n\n## Degradation\n\n- Fall back to manual execution.\n""",
        encoding="utf-8",
    )

    issues = validate_repo(tmp_path / "adopted")

    assert ValidationIssue(
        "invalid-skill-type",
        "docs/skills/SKILL.md: unsupported skill type 'mystery'",
    ) in issues
