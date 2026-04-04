# Discussion Packet First

- ID: discussion-packet-first
- Type: workflow
- Owner: framework-maintainers
- Review Threshold: single-reviewer

## Purpose

Route open design questions into one durable packet before execution begins so later rounds do not rely on chat memory.

## Triggers

### Positive Triggers

- Use when the task is primarily about choosing a direction, comparing alternatives, or reviewing a plan with real tradeoffs.

### Negative Triggers

- Do not use when the next implementation step is already obvious and the remaining work is execution, not decision-making.

### Expected Effect

- The agent creates or updates one discussion packet, asks available executors to respond against the same packet, and synthesizes the result before freezing an execution plan.

## Entry Instructions

- Freeze the decision question, current truth, constraints, candidate directions, and evaluation criteria in one packet.
- Keep feedback append-only and synthesize conflicts instead of averaging them.
- End the round once a plan can be frozen, the disagreement is narrow enough for another round, or a missing truth source blocks honest selection.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| discussion runbook | docs/runbooks/multi-model-discussion-loop.md | yes | Canonical discussion workflow and round-exit rules |
| discussion packet template | templates/discussion_packet.template.md | yes | Default packet structure |
| discussion pipeline | scripts/discussion_pipeline.py | no | Helper for packet initialization and append-only updates |

## Governance

### Allowed Evidence

- Round receipts stored in the packet.
- Human-reviewed synthesis notes.
- Repeated decision failures traced to missing or weak packet structure.

### Reviewer Gate

- Changes to triggers, entry instructions, or round-exit behavior require maintainer review.

### Forbidden Direct Update Inputs

- Raw chat transcripts copied into canonical instructions.
- Tool-specific prompting quirks promoted into the core workflow without review.

## Degradation

- If external CLIs are unavailable, fall back to repo-local agents, internal subagents, or a main-thread synthesis pass using the same packet.

## Validator Notes

- Positive and negative triggers should stay distinct.
- References should remain truthful and resolvable.