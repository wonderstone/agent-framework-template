# Demo Architecture

The demo project is intentionally small: one CLI module, one test file, and one committed audit workflow example.

## Command Flow

1. `list_tasks()` returns the in-memory task list.
2. `format_tasks()` turns tasks into human-readable output.
3. `render_demo_output()` simulates the primary user journey for acceptance checks.

## Why This Shape

- It is small enough to inspect quickly.
- It still has enough behavior to justify tests and audit artifacts.
- It gives adopters one concrete place to map framework concepts onto code.
