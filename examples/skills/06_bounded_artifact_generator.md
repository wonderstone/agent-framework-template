# Bounded Artifact Generator

- ID: bounded-artifact-generator
- Type: workflow
- Owner: framework-maintainers
- Review Threshold: single-reviewer

## Purpose

Keep generator behavior limited to schema-backed artifact creation so generated output remains diffable, reusable, and validator-visible.

## Triggers

### Positive Triggers

- Use when the task needs a discussion packet, git audit packet, skill invocation receipt, or candidate packet generated from known inputs.

### Negative Triggers

- Do not use for unconstrained prose generation, broad drafting, or any output with no stable schema or repository path.

### Expected Effect

- The generator produces one named artifact family, writes it to the expected path, and leaves a receipt or command trace explaining why that artifact was created.

## Entry Instructions

- Artifact Contract: generate only artifact families already defined by stable schema surfaces such as `templates/discussion_packet.template.md`, `templates/git_audit_task_packet.template.md`, or the SKILL execution-layer templates.
- Required Inputs: collect the IDs, owner fields, scope notes, and evidence references before rendering.
- Output Path Rule: write the artifact into its canonical repository location and preserve append-only or diff-friendly behavior where required.
- Receipt Or Diff Anchor: tie the generated artifact to a command, validation result, or receipt-bearing closeout artifact.
- Stop Rule: if the artifact lacks a stable schema or a validator-visible path, stop and do not treat the task as safe generator work.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| discussion pipeline | scripts/discussion_pipeline.py | no | Generator for discussion packet artifacts |
| git audit pipeline | scripts/git_audit_pipeline.py | no | Generator for task, receipt, and handoff artifacts |
| skill evolution pipeline | scripts/skill_evolution_pipeline.py | no | Generator for invocation receipts and candidate packets |
| skill candidate packet template | templates/skill_candidate_packet.template.md | no | Example schema for bounded generator output |

## Governance

### Allowed Evidence

- Generated artifacts tied to explicit commands or receipts.
- Maintainer-reviewed fixes when a generator drifted beyond its declared artifact family.

### Reviewer Gate

- Changes to artifact scope or stop rules require maintainer review.

### Forbidden Direct Update Inputs

- Rebranding free-form drafting as a generator.
- New artifact families added without a template or validator-visible contract.

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

- If the output contract or path cannot be named precisely, block generator use and fall back to a normal planning or writing path instead of pretending generation is safe.

## Validator Notes

- Generator examples should show a real script or template backing the artifact family.