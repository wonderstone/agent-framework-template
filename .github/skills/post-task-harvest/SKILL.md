# Post-Task Harvest

- ID: post-task-harvest
- Type: workflow
- Owner: framework-maintainers
- Review Threshold: single-reviewer

## Purpose

Turn reusable post-task learning into a durable mechanism instead of leaving it in chat history.

## Triggers

### Positive Triggers

- Use when a task, phase, or recovery round changed how future work should be prioritized, validated, or closed out.
- Use when a repeated failure mode, regression rule, or new definition of done was discovered.

### Negative Triggers

- Do not use for one-off trivia, temporary environment noise, or observations that do not change future behavior.

### Expected Effect

- The agent records one harvest packet, chooses a landing tier, and updates the correct durable surface (memory, runbook, script, CI gate, or skill).

## Entry Instructions

- Ask whether the lesson changes future behavior.
- If not, do not create a durable surface.
- If yes, choose the lightest truthful landing tier from the landing ladder.
- Prefer scripts and validators over prose when the rule can be checked mechanically.
- Record the revalidation trigger so the lesson can be promoted, revised, or removed later.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| post-task harvest runbook | docs/runbooks/post-task-harvest.md | yes | Canonical landing-tier and promotion rules |
| experience harvest packet template | templates/experience_harvest_packet.template.md | yes | Default durable packet shape |

## Governance

### Allowed Evidence

- Closeout docs
- Receipt-bearing regressions or audits
- Repeated decision failures traced to the same missing mechanism

### Reviewer Gate

- Changes to the landing ladder, promotion rules, or required questions require maintainer review.

### Forbidden Direct Update Inputs

- Raw transcript summaries with no task-level evidence
- One-off preferences promoted into reusable policy without repeated proof

## Degradation

- If the host does not support durable memory, land the lesson in a runbook or packet doc instead.
- If no script or CI layer exists yet, record the next-promotion trigger in the packet.