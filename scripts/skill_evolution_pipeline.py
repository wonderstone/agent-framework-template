#!/usr/bin/env python3
"""Generate SKILL execution-layer artifacts from runtime evidence."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _read_template(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _normalize_block(value: str) -> str:
    text = value.strip()
    return text or "- none"


def _write(output_path: Path, contents: str) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(contents.rstrip() + "\n", encoding="utf-8")
    return output_path


def _replace_exact(text: str, mapping: dict[str, str]) -> str:
    rendered = text
    for source, target in mapping.items():
        rendered = rendered.replace(source, target)
    return rendered


@dataclass(frozen=True)
class InvocationReceiptOptions:
    receipt_id: str
    invocation_id: str
    skill_id: str
    trigger_class: str
    execution_mode: str
    outcome: str
    candidate_recommendation: str
    trigger_reason: str
    references_loaded: str
    outcome_summary: str
    evidence_links: str
    follow_up_recommendation: str
    output_path: Path


@dataclass(frozen=True)
class CandidatePacketOptions:
    candidate_id: str
    source_skill: str
    harvest_source: str
    proposed_by: str
    confidence_tier: str
    evolution_mode: str
    candidate_trigger: str
    invocation_ids: str
    parent_lineage: str
    target_fields: str
    proposed_delta: str
    evidence_bundle: str
    escalation_triggers: str
    notes: str
    output_path: Path


def create_invocation_receipt(options: InvocationReceiptOptions) -> Path:
    template = _read_template("templates/skill_invocation_receipt.template.md")
    rendered = _replace_exact(
        template,
        {
            "[invocation-receipt-id]": options.receipt_id,
            "[invocation-id]": options.invocation_id,
            "[skill-id]": options.skill_id,
            "[explicit-request | repeated-invocation-failure | repeated-manual-correction | repeated-successful-reuse | operator-forced]": options.trigger_class,
            "[advisory-only | local-follow | delegated-run | host-runtime]": options.execution_mode,
            "[success | fallback | failure | manual-override]": options.outcome,
            "[none | FIX | DERIVED | CAPTURED]": options.candidate_recommendation,
            "[Why this skill was invoked for this task or task phase.]": _normalize_block(options.trigger_reason),
            "| [reference] | [path] | [yes / no] | [what execution context it provided] |": options.references_loaded.strip() or "| runtime evidence | docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md | no | Placeholder row to be replaced by real invocation context |",
            "[What happened after invocation, including any fallback, correction, or notable mismatch.]": _normalize_block(options.outcome_summary),
            "| [receipt-id] | [closeout / root-cause / invocation / task artifact] | [link from observed runtime behavior to future candidate review] |": options.evidence_links.strip() or "| none | invocation | No linked evidence yet |",
            "[State whether no change is needed or whether this invocation should propose FIX, DERIVED, or CAPTURED lineage.]": _normalize_block(options.follow_up_recommendation),
        },
    )
    return _write(options.output_path, rendered)


def create_candidate_packet(options: CandidatePacketOptions) -> Path:
    template = _read_template("templates/skill_candidate_packet.template.md")
    rendered = _replace_exact(
        template,
        {
            "[candidate-id]": options.candidate_id,
            "[skill-id]": options.source_skill,
            "[closeout receipt / root-cause note / invocation receipt]": options.harvest_source,
            "[harvester role or executor]": options.proposed_by,
            "[low / medium / high]": options.confidence_tier,
            "[FIX | DERIVED | CAPTURED]": options.evolution_mode,
            "[explicit-request | repeated-invocation-failure | repeated-manual-correction | repeated-successful-reuse | operator-forced]": options.candidate_trigger,
            "[invocation-id or comma-separated ids]": options.invocation_ids,
            "[none / skill-id / candidate-id / promotion-receipt-id]": options.parent_lineage,
            "[List the canonical SKILL fields this candidate wants to affect.]": _normalize_block(options.target_fields),
            "[Describe the smallest candidate change in field-scoped terms, not free-form transcript summary.]": _normalize_block(options.proposed_delta),
            "| [receipt-id] | [closeout / root-cause / invocation] | [link from observed condition to proposed change] |": options.evidence_bundle.strip() or "| none | invocation | No evidence bundle provided yet |",
            "[List any reasons this candidate must escalate instead of staying in a delegated lane.]": _normalize_block(options.escalation_triggers),
            "Candidate packets are not canonical truth.\n- Do not paste raw transcripts here.\n- Invocation receipts may justify a candidate, but they still do not authorize canonical mutation by themselves.": f"Candidate packets are not canonical truth.\n- Do not paste raw transcripts here.\n- Invocation receipts may justify a candidate, but they still do not authorize canonical mutation by themselves.\n- {_normalize_block(options.notes).lstrip('- ')}",
        },
    )
    return _write(options.output_path, rendered)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate SKILL execution-layer artifacts")
    subparsers = parser.add_subparsers(dest="command", required=True)

    invocation = subparsers.add_parser("init-invocation", help="Create a skill invocation receipt")
    invocation.add_argument("--receipt-id", required=True)
    invocation.add_argument("--invocation-id", required=True)
    invocation.add_argument("--skill-id", required=True)
    invocation.add_argument("--trigger-class", required=True)
    invocation.add_argument("--execution-mode", required=True)
    invocation.add_argument("--outcome", required=True)
    invocation.add_argument("--candidate-recommendation", required=True)
    invocation.add_argument("--trigger-reason", default="- none")
    invocation.add_argument("--references-loaded", default="")
    invocation.add_argument("--outcome-summary", default="- none")
    invocation.add_argument("--evidence-links", default="")
    invocation.add_argument("--follow-up-recommendation", default="- none")
    invocation.add_argument("--output", type=Path, required=True)

    candidate = subparsers.add_parser("init-candidate", help="Create a skill candidate packet")
    candidate.add_argument("--candidate-id", required=True)
    candidate.add_argument("--source-skill", required=True)
    candidate.add_argument("--harvest-source", required=True)
    candidate.add_argument("--proposed-by", required=True)
    candidate.add_argument("--confidence-tier", required=True)
    candidate.add_argument("--evolution-mode", required=True)
    candidate.add_argument("--candidate-trigger", required=True)
    candidate.add_argument("--invocation-ids", required=True)
    candidate.add_argument("--parent-lineage", required=True)
    candidate.add_argument("--target-fields", default="- none")
    candidate.add_argument("--proposed-delta", default="- none")
    candidate.add_argument("--evidence-bundle", default="")
    candidate.add_argument("--escalation-triggers", default="- none")
    candidate.add_argument("--notes", default="- none")
    candidate.add_argument("--output", type=Path, required=True)

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "init-invocation":
        output_path = create_invocation_receipt(
            InvocationReceiptOptions(
                receipt_id=args.receipt_id,
                invocation_id=args.invocation_id,
                skill_id=args.skill_id,
                trigger_class=args.trigger_class,
                execution_mode=args.execution_mode,
                outcome=args.outcome,
                candidate_recommendation=args.candidate_recommendation,
                trigger_reason=args.trigger_reason,
                references_loaded=args.references_loaded,
                outcome_summary=args.outcome_summary,
                evidence_links=args.evidence_links,
                follow_up_recommendation=args.follow_up_recommendation,
                output_path=args.output,
            )
        )
    else:
        output_path = create_candidate_packet(
            CandidatePacketOptions(
                candidate_id=args.candidate_id,
                source_skill=args.source_skill,
                harvest_source=args.harvest_source,
                proposed_by=args.proposed_by,
                confidence_tier=args.confidence_tier,
                evolution_mode=args.evolution_mode,
                candidate_trigger=args.candidate_trigger,
                invocation_ids=args.invocation_ids,
                parent_lineage=args.parent_lineage,
                target_fields=args.target_fields,
                proposed_delta=args.proposed_delta,
                evidence_bundle=args.evidence_bundle,
                escalation_triggers=args.escalation_triggers,
                notes=args.notes,
                output_path=args.output,
            )
        )

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())