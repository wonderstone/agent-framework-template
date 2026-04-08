#!/usr/bin/env python3
"""Generate a strict-adoption verification packet for a bootstrapped repository."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_MANIFEST_PATH = ".github/agent-framework-manifest.json"
DEFAULT_AUDIT_VERSION = "v1"
PROJECT_CONTEXT_PLACEHOLDER_PATTERN = re.compile(
    r"\[(?:[^\]]*(?:fill in|describe here|if useful|if needed|if applicable|your topic|project-specific|config file path|what it controls|optional additional evidence|path / module / entrypoint|surface / service|auth / secrets|single command or script|command or source|command or `none`)[^\]]*)\]",
    re.IGNORECASE,
)
VALIDATION_PASS_MARKERS = (
    re.compile(r"status=passed", re.IGNORECASE),
    re.compile(r"validator passed", re.IGNORECASE),
    re.compile(r"all structured checks passed", re.IGNORECASE),
    re.compile(r"all tests passed", re.IGNORECASE),
    re.compile(r"\b\d+ passed\b", re.IGNORECASE),
    re.compile(r"live smoke passed", re.IGNORECASE),
)
REVIEW_PASS_MARKERS = (
    re.compile(r"verdict:\s*pass", re.IGNORECASE),
    re.compile(r"review passed", re.IGNORECASE),
    re.compile(r"stance:\s*accept", re.IGNORECASE),
    re.compile(r"no material findings", re.IGNORECASE),
    re.compile(r"no findings", re.IGNORECASE),
    re.compile(r"passed in substance", re.IGNORECASE),
)
FAIL_MARKERS = (
    re.compile(r"\b(fail|failed|blocker|rejected|partially-adopted|design-only-upgrade-path-kept)\b", re.IGNORECASE),
    re.compile(r"(?<!0\s)(?<!no\s)\berrors?\b", re.IGNORECASE),
)


@dataclass(frozen=True)
class MechanismDefinition:
    id: str
    required_paths: tuple[str, ...]
    design_only_paths: tuple[str, ...]
    required_manifest_sections: tuple[str, ...]
    note: str


MECHANISM_DEFINITIONS: dict[str, MechanismDefinition] = {
    "project-context-adapter": MechanismDefinition(
        id="project-context-adapter",
        required_paths=(".github/instructions/project-context.instructions.md",),
        design_only_paths=(),
        required_manifest_sections=(),
        note="Truthful project adapter with repo-local commands and protected paths.",
    ),
    "execution-contract-surface": MechanismDefinition(
        id="execution-contract-surface",
        required_paths=("templates/execution_contract.template.md",),
        design_only_paths=(),
        required_manifest_sections=(),
        note="Long-task execution contract surface is shipped.",
    ),
    "developer-toolchain-contract": MechanismDefinition(
        id="developer-toolchain-contract",
        required_paths=(
            ".github/instructions/project-context.instructions.md",
            ".github/agent-framework-manifest.json",
        ),
        design_only_paths=("docs/DEVELOPER_TOOLCHAIN_DESIGN.md",),
        required_manifest_sections=("developer_toolchain_contract",),
        note="Developer Toolchain contract is declared in the adapter and manifest.",
    ),
    "developer-toolchain-probe": MechanismDefinition(
        id="developer-toolchain-probe",
        required_paths=(
            "scripts/developer_toolchain_probe.py",
            "templates/developer_toolchain_probe_receipt.template.md",
        ),
        design_only_paths=("docs/DEVELOPER_TOOLCHAIN_DESIGN.md",),
        required_manifest_sections=("developer_toolchain_probe_contract",),
        note="Receipt-bearing runtime probe for declared Developer Toolchain surfaces.",
    ),
    "developer-toolchain-runner": MechanismDefinition(
        id="developer-toolchain-runner",
        required_paths=(
            "scripts/developer_toolchain_runner.py",
            "templates/developer_toolchain_run_receipt.template.md",
        ),
        design_only_paths=("docs/DEVELOPER_TOOLCHAIN_DESIGN.md",),
        required_manifest_sections=("developer_toolchain_runner_contract",),
        note="Machine-facing runner for declared Developer Toolchain surfaces.",
    ),
    "closeout-truth-audit": MechanismDefinition(
        id="closeout-truth-audit",
        required_paths=("scripts/closeout_truth_audit.py",),
        design_only_paths=(),
        required_manifest_sections=(),
        note="Receipt-anchored closeout enforcement is shipped.",
    ),
    "state-sync-stack": MechanismDefinition(
        id="state-sync-stack",
        required_paths=(
            "scripts/state_sync_audit.py",
            "scripts/state_sync_pipeline.py",
            "templates/execution_progress_receipt.template.md",
            "templates/drift_reconciliation_packet.template.md",
        ),
        design_only_paths=("docs/runbooks/state-reconciliation.md",),
        required_manifest_sections=(),
        note="Checkpoint, receipt, and drift-reconciliation stack is shipped.",
    ),
    "git-audit-pipeline": MechanismDefinition(
        id="git-audit-pipeline",
        required_paths=(
            "scripts/git_audit_pipeline.py",
            "templates/git_audit_task_packet.template.md",
            "templates/git_audit_receipt.template.md",
            "templates/git_audit_handoff_packet.template.md",
        ),
        design_only_paths=("docs/runbooks/resumable-git-audit-pipeline.md",),
        required_manifest_sections=(),
        note="Resumable git-audit packet and handoff workflow is shipped.",
    ),
    "discussion-packet-workflow": MechanismDefinition(
        id="discussion-packet-workflow",
        required_paths=(
            "scripts/discussion_pipeline.py",
            "templates/discussion_packet.template.md",
        ),
        design_only_paths=("docs/runbooks/multi-model-discussion-loop.md",),
        required_manifest_sections=(),
        note="Append-only design discussion packet workflow is shipped.",
    ),
    "independent-evaluation-pipeline": MechanismDefinition(
        id="independent-evaluation-pipeline",
        required_paths=(
            "scripts/evaluation_pipeline.py",
            "templates/evaluation_request.template.md",
            "templates/evaluation_report.template.md",
        ),
        design_only_paths=(),
        required_manifest_sections=("independent_evaluation_contract",),
        note="Independent evaluation request and report pipeline is shipped.",
    ),
    "local-executor-review-loop": MechanismDefinition(
        id="local-executor-review-loop",
        required_paths=(
            "scripts/review_dispatch.py",
            ".github/local_executor_registry.json",
            "templates/review_dispatch_packet.template.md",
        ),
        design_only_paths=("docs/runbooks/multi-model-discussion-loop.md",),
        required_manifest_sections=("executor_review_contract",),
        note="Machine-local executor registry and packetized review dispatch loop are shipped.",
    ),
}


def _parse_named_path(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("expected NAME=PATH")
    name, path = value.split("=", 1)
    name = name.strip()
    path = path.strip()
    if not name or not path:
        raise argparse.ArgumentTypeError("expected non-empty NAME=PATH")
    return name, path


def _load_manifest(root: Path, manifest_path: str) -> dict[str, object]:
    return json.loads((root / manifest_path).read_text(encoding="utf-8"))


def _status_for_mechanism(
    root: Path,
    definition: MechanismDefinition,
    manifest: dict[str, object],
) -> tuple[str, int, int, list[str], str]:
    present_required = [path for path in definition.required_paths if (root / path).exists()]
    missing_required = [path for path in definition.required_paths if not (root / path).exists()]
    present_design_only = [path for path in definition.design_only_paths if (root / path).exists()]
    missing_manifest_sections = [
        f"manifest:{section}"
        for section in definition.required_manifest_sections
        if not isinstance(manifest.get(section), dict)
    ]
    missing_required = [*missing_required, *missing_manifest_sections]

    if definition.id == "project-context-adapter":
        project_context = root / ".github" / "instructions" / "project-context.instructions.md"
        if not project_context.is_file():
            missing_required.append("truthful-project-context")
        else:
            project_context_text = project_context.read_text(encoding="utf-8")
            if PROJECT_CONTEXT_PLACEHOLDER_PATTERN.search(project_context_text):
                missing_required.append("truthful-project-context")

    if missing_required == []:
        return "kept", len(present_required), len(definition.required_paths), [], definition.note
    if present_required:
        return (
            "downgraded",
            len(present_required),
            len(definition.required_paths),
            missing_required,
            "Some required execution assets are present, but the mechanism is incomplete.",
        )
    if present_design_only:
        return (
            "design-only-upgrade-path-kept",
            0,
            len(definition.required_paths),
            missing_required,
            "Only the design or runbook surface is present; runnable execution assets are missing.",
        )
    return (
        "missing",
        0,
        len(definition.required_paths),
        missing_required,
        "No shipped design or execution surface was found for this mechanism.",
    )


def _default_output_path(root: Path, contract: dict[str, object]) -> Path:
    configured = contract.get("verification_packet_path")
    if isinstance(configured, str) and configured.strip():
        return root / configured
    return root / "tmp" / "adoption_verification" / "adoption_verification_packet.md"


def _evidence_note(path: Path, *, kind: str) -> tuple[bool, str]:
    if not path.exists():
        return False, f"{kind.capitalize()} evidence file is missing."
    text = path.read_text(encoding="utf-8")
    markers = VALIDATION_PASS_MARKERS if kind == "validation" else REVIEW_PASS_MARKERS
    has_pass = any(marker.search(text) for marker in markers)
    has_fail = any(marker.search(text) for marker in FAIL_MARKERS)
    if has_pass and not has_fail:
        return True, f"{kind.capitalize()} evidence includes recognized pass markers."
    if has_pass and has_fail:
        return False, f"{kind.capitalize()} evidence mixes pass and fail markers; review manually."
    if has_fail:
        return False, f"{kind.capitalize()} evidence includes non-passing markers."
    return False, f"{kind.capitalize()} evidence has no recognized pass markers."


def _compute_verdict(
    mechanism_statuses: list[str],
    *,
    has_validation_evidence: bool,
    has_independent_review: bool,
    independent_review_required: bool,
) -> tuple[str, str]:
    if any(status in {"missing", "downgraded", "unknown-mechanism"} for status in mechanism_statuses):
        return "partially-adopted", "At least one required mechanism is missing, incomplete, or unknown."

    if any(status == "design-only-upgrade-path-kept" for status in mechanism_statuses):
        return (
            "design-only-upgrade-path-kept",
            "Only design-level upgrade paths remain for at least one required mechanism.",
        )

    if not has_validation_evidence:
        return "partially-adopted", "Required mechanism files exist, but no validation evidence was supplied."

    if independent_review_required and not has_independent_review:
        return "partially-adopted", "Required independent review evidence was not supplied."

    return "fully-adopted", "All required mechanisms are present and the declared evidence gates were satisfied."


def _render_packet(
    template: str,
    *,
    generated_at: str,
    repository_root: Path,
    manifest_schema_version: object,
    audit_version: str,
    verdict: str,
    verdict_summary: str,
    mechanism_rows: str,
    validation_rows: str,
    review_rows: str,
    required_mechanism_ids: list[str],
    require_independent_review_for: list[str],
    verification_packet_path: Path,
) -> str:
    rendered = template
    replacements = {
        "[generated-at]": generated_at,
        "[repository-root]": str(repository_root),
        "[manifest-schema-version]": str(manifest_schema_version),
        "[audit-version]": audit_version,
        "[fully-adopted | partially-adopted | design-only-upgrade-path-kept]": verdict,
        "[Short summary of why this verdict was reached.]": verdict_summary,
        "| [mechanism-id] | [kept | downgraded | design-only-upgrade-path-kept | missing | unknown-mechanism] | [N/M paths present] | [missing paths or `none`] | [short note] |": mechanism_rows,
        "| [validation-label] | [path] | [yes / no] | [what this evidence proves] |": validation_rows,
        "| [reviewer-name] | [path] | [yes / no] | [what this review contributes] |": review_rows,
        "[comma-separated mechanism ids]": ", ".join(required_mechanism_ids) or "none",
        "[comma-separated verdicts or `none`]": ", ".join(require_independent_review_for) or "none",
        "[verification-packet-path]": str(verification_packet_path.relative_to(repository_root)),
    }
    for source, target in replacements.items():
        rendered = rendered.replace(source, target)
    return rendered.rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a strict-adoption verification packet")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root to audit")
    parser.add_argument(
        "--manifest-path",
        default=DEFAULT_MANIFEST_PATH,
        help="Path to the adopter manifest relative to the repository root",
    )
    parser.add_argument(
        "--validation-evidence",
        action="append",
        default=[],
        type=_parse_named_path,
        help="Validation evidence in NAME=PATH form; may be repeated",
    )
    parser.add_argument(
        "--review-artifact",
        action="append",
        default=[],
        type=_parse_named_path,
        help="Independent review artifact in REVIEWER=PATH form; may be repeated",
    )
    parser.add_argument("--output", type=Path, help="Override packet output path")
    args = parser.parse_args()

    root = args.root.resolve()
    manifest = _load_manifest(root, args.manifest_path)
    contract = manifest.get("strict_adoption_contract")
    if not isinstance(contract, dict):
        raise SystemExit("manifest is missing strict_adoption_contract")

    required_mechanism_ids = [
        str(value) for value in contract.get("required_mechanism_ids", []) if str(value).strip()
    ]
    require_independent_review_for = [
        str(value) for value in contract.get("require_independent_review_for", []) if str(value).strip()
    ]
    output_path = args.output.resolve() if args.output else _default_output_path(root, contract)

    mechanism_statuses: list[str] = []
    mechanism_rows: list[str] = []
    for mechanism_id in required_mechanism_ids:
        definition = MECHANISM_DEFINITIONS.get(mechanism_id)
        if definition is None:
            mechanism_statuses.append("unknown-mechanism")
            mechanism_rows.append(
                f"| {mechanism_id} | unknown-mechanism | 0/0 paths present | none | No built-in definition exists for this mechanism id. |"
            )
            continue
        status, present_count, total_count, missing_required, note = _status_for_mechanism(
            root, definition, manifest
        )
        mechanism_statuses.append(status)
        missing_display = ", ".join(missing_required) if missing_required else "none"
        mechanism_rows.append(
            f"| {mechanism_id} | {status} | {present_count}/{total_count} paths present | {missing_display} | {note} |"
        )

    validation_rows: list[str] = []
    valid_validation_evidence = 0
    for label, relative_path in args.validation_evidence:
        path = root / relative_path
        passed, note = _evidence_note(path, kind="validation")
        if passed:
            valid_validation_evidence += 1
        validation_rows.append(
            f"| {label} | {relative_path} | {'yes' if path.exists() else 'no'} | {note} |"
        )
    if not validation_rows:
        validation_rows.append("| none | none | no | No validation evidence was supplied to the audit. |")

    review_rows: list[str] = []
    valid_review_artifacts = 0
    for reviewer, relative_path in args.review_artifact:
        path = root / relative_path
        passed, note = _evidence_note(path, kind="review")
        if passed:
            valid_review_artifacts += 1
        review_rows.append(
            f"| {reviewer} | {relative_path} | {'yes' if path.exists() else 'no'} | {note} |"
        )
    if not review_rows:
        review_rows.append("| none | none | no | No independent review artifacts were supplied to the audit. |")

    independent_review_required = "fully-adopted" in require_independent_review_for
    verdict, verdict_summary = _compute_verdict(
        mechanism_statuses,
        has_validation_evidence=valid_validation_evidence > 0,
        has_independent_review=valid_review_artifacts > 0,
        independent_review_required=independent_review_required,
    )

    template = (root / "templates" / "adoption_verification_packet.template.md").read_text(encoding="utf-8")
    rendered = _render_packet(
        template,
        generated_at=datetime.now(timezone.utc).isoformat(),
        repository_root=root,
        manifest_schema_version=manifest.get("schema_version", "unknown"),
        audit_version=DEFAULT_AUDIT_VERSION,
        verdict=verdict,
        verdict_summary=verdict_summary,
        mechanism_rows="\n".join(mechanism_rows),
        validation_rows="\n".join(validation_rows),
        review_rows="\n".join(review_rows),
        required_mechanism_ids=required_mechanism_ids,
        require_independent_review_for=require_independent_review_for,
        verification_packet_path=output_path,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())