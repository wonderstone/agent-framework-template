# Staged Handoff Pipeline

- ID: staged-handoff-pipeline
- Type: workflow
- Owner: framework-maintainers
- Review Threshold: single-reviewer

## Purpose

Model multi-step execution as explicit stage transitions backed by packets, receipts, and stop rules rather than narrative workflow prose.

## Triggers

### Positive Triggers

- Use when work moves across planning, implementation, review, or closeout stages and needs a durable handoff surface between them.

### Negative Triggers

- Do not use for single-step edits that have no meaningful stage boundary or reusable handoff artifact.

### Expected Effect

- Each stage ends with a packet, receipt, or blocker note, and the next stage starts from that artifact instead of reconstructing progress from chat memory.

## Entry Instructions

- Stage Boundary: name the current stage and the next stage before work proceeds.
- Handoff Artifact: use `templates/discussion_packet.template.md`, `templates/git_audit_task_packet.template.md`, `templates/git_audit_receipt.template.md`, or `templates/git_audit_handoff_packet.template.md` as the state carrier.
- Checkpoint Rule: finish each stage with validation evidence or an explicit blocker.
- Stop Or Degrade Rule: if the stage cannot emit its artifact, stop or downgrade honestly instead of treating the pipeline as complete.
- Validator Surface: keep the runbook or template path visible so the boundary can be checked structurally.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| discussion runbook | docs/runbooks/multi-model-discussion-loop.md | no | Example of a packet-driven planning pipeline |
| git audit runbook | docs/runbooks/resumable-git-audit-pipeline.md | yes | Canonical staged execution workflow |
| audit task packet template | templates/git_audit_task_packet.template.md | yes | Planning or dispatch stage artifact |
| audit handoff template | templates/git_audit_handoff_packet.template.md | yes | Resume artifact when execution stops mid-pipeline |

## Governance

### Allowed Evidence

- Packets, receipts, and handoff notes showing whether stage boundaries held.
- Maintainer-reviewed fixes for skipped checkpoints or missing handoff artifacts.

### Reviewer Gate

- Changes to stage semantics or stop rules require maintainer review.

### Forbidden Direct Update Inputs

- Workflow claims that rely on memory instead of artifacts.
- Decorative pipeline language with no validator-visible boundary.

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

- If the workflow cannot emit a packet or receipt, stop at the current stage and record the missing handoff rather than assuming the next stage can infer state.

## Validator Notes

- Pipeline examples should identify the exact artifact family that carries state across the boundary.