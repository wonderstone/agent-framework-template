# Bounded Artifact Generator Starter

- ID: bounded-artifact-generator-starter
- Type: workflow
- Owner: framework-maintainers
- Review Threshold: single-reviewer

## Purpose

Allow narrow artifact generation only when the output contract, path, and proof surface are explicit enough to keep generation honest.

## Triggers

### Positive Triggers

- Use when the task needs a discussion packet, audit packet, receipt, candidate artifact, or other structured file with a stable schema.

### Negative Triggers

- Do not use for open-ended drafting, unconstrained content authoring, or any output that lacks a declared schema, path, and validation story.

### Expected Effect

- The skill keeps generator behavior constrained to named artifacts and stops the moment the task drifts into free-form composition without a checkable contract.

## Entry Instructions

- Artifact Contract: generate only named packets, receipts, registries, or other structured artifacts with a stable schema boundary.
- Required Inputs: gather IDs, owner fields, scope fields, and required notes before rendering.
- Output Path Rule: write to the declared repository path and keep the artifact append-only or diffable when the surrounding workflow requires it.
- Receipt Or Diff Anchor: link generated output to a receipt, command, or validation result that proves why the artifact exists.
- Stop Rule: do not expand into open-ended drafting when the artifact lacks a validator-visible contract.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| discussion pipeline | scripts/discussion_pipeline.py | no | Example generator for append-only discussion artifacts |
| git audit pipeline | scripts/git_audit_pipeline.py | no | Example generator for task packets, receipts, and handoff packets |
| skill evolution pipeline | scripts/skill_evolution_pipeline.py | no | Example generator for invocation receipts and candidate packets |
| discussion packet template | templates/discussion_packet.template.md | no | Canonical schema for one generator-backed artifact family |

## Governance

### Allowed Evidence

- Generated artifacts tied to commands, receipts, or validations that prove the contract was real.
- Maintainer-reviewed fixes for generators that drifted beyond their declared schema.

### Reviewer Gate

- Changes to artifact scope, stop rules, or evidence requirements require maintainer review.

### Forbidden Direct Update Inputs

- Rebranding unconstrained drafting as a generator.
- Generator expansions that add new artifact families without documenting the schema and proof boundary.

## Receipt And Review Matrix

| Field | Proposal evidence tiers | Minimum reviewer threshold | Guardrail override | Promotion tier |
|---|---|---|---|---|
| `purpose` | `1-2 only` | `single-reviewer` | `dual-reviewer`; no auto-proposed rewrite | `human-only` |
| `triggers` | `1-3` | `single-reviewer` | `dual-reviewer`; no auto-proposed rewrite | `human-only` |
| `entry_instructions` | `1-3` | `single-reviewer` | `dual-reviewer`; no auto-proposed rewrite | `delegated-reviewed` |
| `references` | `1-4` | `single-reviewer` | `single-reviewer`; must keep reference truthfulness | `delegated-safe` |
| `governance` | `1-2 only` | `dual-reviewer` | `dual-reviewer`; owner review required | `human-only` |
| `degradation` | `1-3` | `single-reviewer` | `dual-reviewer`; owner review required | `delegated-reviewed` |

## Degradation

- If the artifact schema, path, or validator surface is missing, stop and record the missing contract instead of pretending a broad generator is safe to invoke.

## Validator Notes

- Generator starters should point to stable artifact families, not free-form writing tasks.
- Generator text should make the stop boundary obvious to future adopters.