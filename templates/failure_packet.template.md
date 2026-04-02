# Failure Packet

> Use this when runtime behavior is broken, unexpectedly unsafe, or no longer trustworthy.
> This packet is progressive: save early with the minimum fields, then extend it as investigation matures.

---

## Packet Status

- Severity tier: [lightweight / full]
- Status: [open / mitigated / cause-suspected / cause-established / closed]
- Created on: [YYYY-MM-DD]
- Updated on: [YYYY-MM-DD]
- Owner: [person / agent / team]

## Minimum First Save

- Symptom: [what is visibly wrong]
- Impacted surface: [must match a `User Surface Map` entry when one exists]
- First observed evidence: [log line / screenshot / failing command / user report / explicit `report-only so far`]

Rule:

- If the packet exists, these three fields must exist.
- If there is no concrete evidence yet, say so explicitly rather than leaving the field blank.

---

## Expanded Investigation

- Fastest repro path: [shortest trustworthy reproduction path]
- Repro status: [not-attempted / reproduced / not-reproduced / intermittent]
- Suspected layers: [code / config / prompt / tool / dependency / runtime / external service]
- Current hypothesis: [best current explanation]
- Runtime evidence refs:
  - [log path / command / health endpoint / screenshot / trace / smoke script]
- Fix attempted so far:
  - [change]
- Outcome of attempted fix:
  - [result]

## Escalation Check

- Impacted surface marked sensitive: [yes / no]
- Sensitive path or config touched: [yes / no]
- Survived one attempted fix: [yes / no]
- Recurred after previous closeout: [yes / no]
- Shared beyond one local executor: [yes / no]

Rule:

- If any answer above is `yes`, promote to `full` unless there is a documented reason not to.

## Full Investigation Additions

- Impacted trust boundary: [auth / secrets / model routing / external tool / export path / none]
- Relevant config or secret surface: [path / env / setting / none]
- Negative-path or misuse-path validation claim: [what was checked beyond happy path]
- Containment or rollback note: [optional in v1]
- Residual unknowns: [what is still not proven]

## Closeout Linkage

- Root cause note required: [yes / no]
- Root cause note path: [path or `none yet`]
- Closeout evidence summary: [what evidence would justify `closed`]
