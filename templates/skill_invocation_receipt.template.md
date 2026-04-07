# SKILL Invocation Receipt

- Receipt ID: [invocation-receipt-id]
- Invocation ID: [invocation-id]
- Skill ID: [skill-id]
- Trigger Class: [explicit-request | repeated-invocation-failure | repeated-manual-correction | repeated-successful-reuse | operator-forced]
- Execution Mode: [advisory-only | local-follow | delegated-run | host-runtime]
- Outcome: [success | fallback | failure | manual-override]
- Candidate Recommendation: [none | FIX | DERIVED | CAPTURED]

## Trigger Reason

- [Why this skill was invoked for this task or task phase.]

## References Loaded

| Name | Path | Loaded | Why It Was Needed |
|---|---|---|---|
| [reference] | [path] | [yes / no] | [what execution context it provided] |

## Outcome Summary

- [What happened after invocation, including any fallback, correction, or notable mismatch.]

## Evidence Links

| Evidence ID | Type | Why It Matters |
|---|---|---|
| [receipt-id] | [closeout / root-cause / invocation / task artifact] | [link from observed runtime behavior to future candidate review] |

## Follow-up Recommendation

- [State whether no change is needed or whether this invocation should propose FIX, DERIVED, or CAPTURED lineage.]

## Notes

- Invocation receipts are runtime evidence, not canonical SKILL truth.
- Do not paste raw transcripts here.