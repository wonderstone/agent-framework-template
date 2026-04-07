# Independent Reviewer Gate Starter

- ID: independent-reviewer-gate-starter
- Type: verification
- Owner: framework-maintainers
- Review Threshold: single-reviewer

## Purpose

Route completed implementation through one receipt-anchored independent evaluation path before closeout so review is explicit instead of implied.

## Triggers

### Positive Triggers

- Use when a task has crossed from generation into evaluation and the repository wants one reviewer, audit pass, or owner verdict recorded against the finished scope.

### Negative Triggers

- Do not use when the work is still being generated, when no bounded review artifact exists yet, or when the task is a trivial local change with no declared review lane.

### Expected Effect

- The skill freezes the review artifact, expects a structured verdict, records the evidence sink, and blocks closeout when independent evaluation cannot be completed honestly.

## Entry Instructions

- Review Artifact: freeze a task packet, diff, build log, runnable path, or closeout bundle before handoff.
- Verdict Contract: the reviewer must return PASS, CONDITIONAL, or FAIL against explicit acceptance criteria.
- Evidence Sink: record the verdict in an audit receipt, review comment, or closeout summary tied to the changed scope.
- Escalation Or Stop Rule: stop the lane when the reviewer finds scope drift, missing proof, or an unverifiable user-visible claim.
- Independence Rule: the generator of the change does not self-certify the final closeout when an independent reviewer path is available.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| git audit runbook | docs/runbooks/resumable-git-audit-pipeline.md | yes | Defines packet, receipt, and handoff expectations for replaceable review passes |
| audit task packet template | templates/git_audit_task_packet.template.md | no | Freezes what the reviewer is allowed to inspect |
| audit receipt template | templates/git_audit_receipt.template.md | yes | Canonical receipt surface for structured verdicts |
| execution contract template | templates/execution_contract.template.md | no | Optional upstream boundary that defines when review should fire |

## Governance

### Allowed Evidence

- Audit receipts, reviewer verdicts, and closeout artifacts tied to the evaluated scope.
- Maintainer-reviewed examples showing a repeated gap in review handoff or verdict recording.

### Reviewer Gate

- Changes to verdict semantics, independence rules, or escalation boundaries require maintainer review.

### Forbidden Direct Update Inputs

- Treating author self-review as independent proof.
- Expanding the reviewer gate into a new constitutional skill type or mandatory runtime law.

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

- If no independent reviewer path exists in the current repository, downgrade this starter to a documented owner checkpoint and record that the closeout still lacks independent evaluation.

## Validator Notes

- Reviewer starters should describe a real verdict sink, not just say “have someone review this.”
- Reviewer text should stay tied to receipts, checkpoints, or closeout evidence rather than vague taste-based critique.