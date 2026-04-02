# Failure Packet

## Packet Status

- Severity tier: lightweight
- Status: cause-established
- Created on: 2026-04-03
- Updated on: 2026-04-03
- Owner: demo maintainer

## Minimum First Save

- Symptom: `python -m src.task_tracker --demo` printed an empty task list after adding the seeded demo item
- Impacted surface: `demo task listing flow`
- First observed evidence: visible CLI output no longer contained the seeded task name in the demo transcript

## Expanded Investigation

- Fastest repro path: `python -m src.task_tracker --demo`
- Repro status: reproduced
- Suspected layers: code / runtime
- Current hypothesis: the demo path stopped seeding the default task before rendering the list
- Runtime evidence refs:
  - demo command stdout from `python -m src.task_tracker --demo`
- Fix attempted so far:
  - restored the seed-before-render step in the demo path
- Outcome of attempted fix:
  - demo output once again showed the seeded task and tests stayed green

## Escalation Check

- Impacted surface marked sensitive: no
- Sensitive path or config touched: no
- Survived one attempted fix: no
- Recurred after previous closeout: no
- Shared beyond one local executor: no

## Closeout Linkage

- Root cause note required: yes
- Root cause note path: `examples/demo_project/tmp/failure_recovery/demo_cli_output_regression/root_cause_note.md`
- Closeout evidence summary: demo command output restored and `pytest tests/ -q` still passes
