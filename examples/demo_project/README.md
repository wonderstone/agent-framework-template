# Demo Project

This example shows what an adopted repository can look like after using the framework with a small Python CLI task tracker.

---

## Scenario

The demo project simulates a team that adopted the template with the `standard` profile, then added project-specific context, tests, and a resumable audit trail for a small feature.

The feature in the committed audit artifacts is: adding task priority labels without losing the ability to resume review in a new CLI session.

---

## Demo Layout

```
examples/demo_project/
  .github/instructions/project-context.instructions.md
  docs/
    ARCHITECTURE.md
    INDEX.md
    runbooks/demo-workflow.md
  src/task_tracker.py
  tests/test_task_tracker.py
  ROADMAP.md
  session_state.md
  tmp/git_audit/add_task_priority/
    task_packet.md
    audit_receipt.md
    handoff_packet.md
```

---

## Walkthrough

1. Read [demo-workflow.md](docs/runbooks/demo-workflow.md) to see the exact bootstrap and audit sequence.
2. Open [project-context.instructions.md](.github/instructions/project-context.instructions.md) to see what adopters customize first, including the Developer Toolchain section.
3. Inspect [task_tracker.py](src/task_tracker.py) and [test_task_tracker.py](tests/test_task_tracker.py) for a minimal code surface.
4. Review the committed packet, receipt, and handoff files under `tmp/git_audit/` to see how work survives interruption.
