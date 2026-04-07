# SKILL Promotion Receipt

- Receipt ID: [promotion-receipt-id]
- Candidate ID: [candidate-id]
- Source Skill: [skill-id]
- Evolution Mode: [FIX | DERIVED | CAPTURED]
- Invocation IDs: [invocation-id or comma-separated ids]
- Parent Lineage: [none / skill-id / candidate-id / promotion-receipt-id]
- Decision: [approve / reject / defer / escalate]
- Reviewer Role: [role name]
- Review Executor: [cli / subagent / owner / human]

## Affected Fields

| Field | Promotion Tier | Evidence Used | Escalation Required |
|---|---|---|---|
| [canonical-field] | [delegated-safe / delegated-reviewed / human-only] | [receipt ids] | [yes / no] |

## Decision Rationale

- [Why the change was accepted, rejected, deferred, or escalated.]

## Canonical Result

- [Describe the canonical mutation that occurred, or state that no canonical mutation occurred.]

## Follow-up

- [Name any audit, rollback, or human review that still must happen.]

## Notes

- Promotion receipts are canonical evidence of the decision, not proof that runtime observations may bypass the declared promotion path.