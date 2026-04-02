# Demo Workflow

This walkthrough shows one realistic way to use the framework in a small repository.

## Bootstrap

```bash
python scripts/bootstrap_adoption.py ../demo-task-tracker \
  --project-name "Demo Task Tracker" \
  --profile standard \
  --project-type cli-tool
```

## Customize

1. Replace the generated project context with repo-specific paths and commands.
2. Fill the Developer Toolchain section honestly, using explicit `none` where a surface does not exist.
3. Add a tiny code surface and at least one test.
4. Fill `ROADMAP.md` and `session_state.md` with the first real phase.

## Audit Flow

1. Generate a task packet before external review.
2. Record an audit receipt after one bounded execution pass.
3. Write a handoff packet if the session stops before closeout.

The committed files under `tmp/git_audit/add_task_priority/` illustrate that flow.
