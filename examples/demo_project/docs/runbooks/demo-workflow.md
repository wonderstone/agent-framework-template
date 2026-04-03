# Demo Workflow

This walkthrough shows one realistic way to use the framework in a small repository.

## Bootstrap

```bash
python3 scripts/bootstrap_adoption.py ../demo-task-tracker \
  --project-name "Demo Task Tracker" \
  --profile standard \
  --project-type cli-tool
```

## Customize

1. Replace the generated project context with repo-specific paths and commands.
2. Fill the Developer Toolchain section honestly, using explicit `none` where a surface does not exist.
3. Keep `Runtime Evidence` inside the Developer Toolchain section so future agents know where logs, smoke paths, and health checks actually live.
4. Fill `User Surface Map` with only the top user-visible flows first; do not pretend the map is complete if it is not.
5. Mark security-sensitive flows honestly and keep the escalation rule close to those declarations.
6. Add a tiny code surface and at least one test.
7. Fill `ROADMAP.md` and `session_state.md` with the first real phase.

## Audit Flow

1. Generate a task packet before external review.
2. Record an audit receipt after one bounded execution pass.
3. Write a handoff packet if the session stops before closeout.

The committed files under `tmp/git_audit/add_task_priority/` illustrate that flow.

## Failure And Recovery Flow

When runtime behavior is broken or no longer trustworthy:

1. open a `failure_packet.md` using `templates/failure_packet.template.md`
2. save the minimum fields immediately: symptom, impacted surface, and first observed evidence
3. promote the packet to `full` if the issue touches a sensitive surface, survives one attempted fix, or becomes shared beyond one executor
4. at closeout, write a `root_cause_note.md` if the issue was user-visible, sensitive, or still only partially understood

The key rule is:

do not let the explanation of the failure live only in chat or terminal scrollback.

Example committed artifacts:

1. `examples/demo_project/tmp/failure_recovery/demo_cli_output_regression/failure_packet.md`
2. `examples/demo_project/tmp/failure_recovery/demo_cli_output_regression/root_cause_note.md`

## Recommended Layout

For a small repository like this demo, a practical layout is:

1. keep long-lived truth in `.github/instructions/project-context.instructions.md`
2. keep event truth in task-local artifacts such as `failure_packet.md`
3. keep recovery truth in `root_cause_note.md`
4. keep audit recovery truth in `tmp/git_audit/`

That split helps future agents answer:

1. what surface was affected
2. where evidence should come from
3. whether stronger escalation rules apply
4. whether the cause is understood or only mitigated
