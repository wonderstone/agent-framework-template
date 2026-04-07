# Receipt-Anchored Reviewer

- ID: receipt-anchored-reviewer
- Type: verification
- Owner: framework-maintainers
- Review Threshold: single-reviewer

## Purpose

Turn review into a receipt-bearing evaluation step so implementation closeout does not rely on implied approval.

## Triggers

### Positive Triggers

- Use when a task has a bounded review artifact and the repository wants an explicit PASS, CONDITIONAL, or FAIL verdict before closeout.

### Negative Triggers

- Do not use while the generator is still changing files or when no packet, diff, or runnable path exists for an independent evaluator to inspect.

### Expected Effect

- The reviewer receives one frozen artifact bundle, returns a structured verdict, and records that verdict in a receipt or closeout surface that later sessions can trust.

## Entry Instructions

- Review Artifact: freeze the diff, task packet, runnable path, or validation output before asking for review.
- Verdict Contract: require PASS, CONDITIONAL, or FAIL rather than open-ended sentiment.
- Evidence Sink: store the verdict in `templates/git_audit_receipt.template.md`, a pull request comment, or a closeout summary tied to the reviewed scope.
- Escalation Or Stop Rule: stop closeout if the reviewer finds scope drift, missing proof, or a user-visible claim that cannot be verified.
- Independence Rule: prefer an evaluator path that did not generate the change when one is available.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| git audit runbook | docs/runbooks/resumable-git-audit-pipeline.md | yes | Defines the replaceable reviewer and receipt workflow |
| audit receipt template | templates/git_audit_receipt.template.md | yes | Canonical sink for structured review verdicts |
| closeout summary template | docs/CLOSEOUT_SUMMARY_TEMPLATE.md | no | Final summary sink for review outcomes |

## Governance

### Allowed Evidence

- Audit receipts or review comments tied to the evaluated scope.
- Maintainer-reviewed examples where review failed because the artifact boundary was weak.

### Reviewer Gate

- Changes to verdict semantics or independence rules require maintainer review.

### Forbidden Direct Update Inputs

- Treating author self-review as independent proof.
- Recasting reviewer strategy as a new canonical SKILL law instead of a narrow evaluation scaffold.

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

- If no independent reviewer path exists, downgrade to an explicit owner checkpoint and record that the final closeout still lacks independent evaluation.

## Validator Notes

- Reviewer examples should point to a real verdict sink rather than vague advice to review carefully.