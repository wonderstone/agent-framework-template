# Root Cause Note

## Cause Status

- Cause status: established
- Related failure packet: `examples/demo_project/tmp/failure_recovery/demo_cli_output_regression/failure_packet.md`
- Impacted surface: `demo task listing flow`

## Cause Statement

- Cause statement: the demo code path rendered the task list before the seeded demo task was created, so the visible output looked empty even though the command itself still exited successfully
- Supporting evidence:
  - the repro output was empty before the fix
  - after restoring seed-before-render ordering, the expected task appeared again

## Fix Statement

- Fix statement: restore the seed-before-render order in the demo CLI path
- Why this fix addresses cause rather than symptom alone: it repairs the ordering bug that created the empty output instead of patching the transcript or masking the missing data

## Residual Risk

- What could still go wrong: another future refactor could preserve command success while silently changing visible CLI output again
- What would likely be observed first if it does: the demo transcript or smoke output would stop showing the seeded task name

## Validation Summary

- Positive-path validation:
  - `python -m src.task_tracker --demo`
  - `pytest tests/ -q`
- Negative-path or misuse-path validation:
  - not required for this issue

## Closeout Truthfulness

- Safe to say `closed`: yes
- If `no`, preferred wording: none
