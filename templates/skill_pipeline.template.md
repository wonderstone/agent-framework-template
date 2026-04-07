# Staged Handoff Pipeline Starter

- ID: staged-handoff-pipeline-starter
- Type: workflow
- Owner: framework-maintainers
- Review Threshold: single-reviewer

## Purpose

Make staged execution explicit by requiring named boundaries, handoff artifacts, checkpoint proof, and an honest stop rule between stages.

## Triggers

### Positive Triggers

- Use when a task crosses multiple bounded stages such as planning, implementation, review, closeout, or any packet or receipt driven workflow.

### Negative Triggers

- Do not use when the work is a single local step with no meaningful stage boundary or when no artifact changes hands between stages.

### Expected Effect

- The skill turns broad workflow prose into explicit stage boundaries and keeps later stages from pretending earlier artifacts or proof already exist.

## Entry Instructions

- Stage Boundary: name each stage before work moves, such as plan, generate, review, or closeout.
- Handoff Artifact: choose the packet, receipt, handoff note, or candidate file that carries state across the boundary.
- Checkpoint Rule: end each stage with validation, receipt output, or an explicit blocker before the next stage starts.
- Stop Or Degrade Rule: if a stage cannot emit its artifact or proof, stop or downgrade honestly instead of skipping the boundary.
- Validator Surface: keep at least one doc, template, or script that makes the pipeline checkable by bootstrap or validator logic.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| discussion runbook | docs/runbooks/multi-model-discussion-loop.md | no | Example of packet-backed multi-stage decision flow |
| git audit runbook | docs/runbooks/resumable-git-audit-pipeline.md | yes | Canonical staged packet or receipt workflow |
| audit handoff template | templates/git_audit_handoff_packet.template.md | yes | Standard handoff artifact shape |
| audit receipt template | templates/git_audit_receipt.template.md | yes | Standard stage-exit proof surface |

## Governance

### Allowed Evidence

- Handoff packets, audit receipts, and closeout artifacts showing where stage boundaries held or broke.
- Maintainer-reviewed fixes for pipelines that skipped proof or lost state across boundaries.

### Reviewer Gate

- Changes to stage semantics, handoff requirements, or degrade behavior require maintainer review.

### Forbidden Direct Update Inputs

- Pipeline descriptions that rely only on chat memory.
- New stage names that have no artifact or proof surface behind them.

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

- If the repository cannot emit a real handoff artifact yet, keep the pipeline boundary documented as a stop point and do not claim the stage transition is automated or durable.

## Validator Notes

- Pipeline starters should name at least one concrete handoff artifact.
- Pipeline text should never imply that a later stage can reconstruct state from memory alone.