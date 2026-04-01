# Task Packet

- Task ID: add_task_priority
- Goal: preserve task priority labels across list output and review handoff
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
