# Task Packet

- Task ID: add_task_priority
- Goal: preserve task priority labels across list output and review handoff
- Owner: demo-main-thread
- Executor Plan: planner -> executor -> reviewer -> owner closeout

## Start Here

- Read `examples/demo_project/src/task_tracker.py` and `examples/demo_project/tests/test_task_tracker.py`.
- Keep the checkpoint contract in sync with `examples/demo_project/session_state.md` before handoff or closeout.

- Truth sources:
  - `examples/demo_project/src/task_tracker.py`
  - `examples/demo_project/tests/test_task_tracker.py`
  - `examples/demo_project/docs/ARCHITECTURE.md`
- Allowed files:
  - `examples/demo_project/src/task_tracker.py`
  - `examples/demo_project/tests/test_task_tracker.py`
- Validation:
  - `pytest examples/demo_project/tests/test_task_tracker.py -q`
- Acceptance boundary:
  - The rendered task list visibly includes priority labels.

## Checkpoint Contract

- Progress Unit: review-pass
- Checkpoint Rule: each meaningful review checkpoint emits one progress receipt and syncs `examples/demo_project/session_state.md` before another executor resumes.
- Truth Surfaces: `examples/demo_project/session_state.md`, `examples/demo_project/ROADMAP.md`, `tmp/git_audit/add_task_priority/task_packet.md`, progress receipts, audit receipt, handoff packet, and drift packet.
- State Sync Schedule: checkpoint -> progress receipt + session state, handoff -> handoff packet + session state, closeout -> receipt trail + roadmap and state sync.
- Closeout Boundary: focused test passes, output remains visibly correct, and no drift packet is open.
