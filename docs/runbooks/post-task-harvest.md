# Post-Task Harvest

This runbook turns post-task "experience summary" into a real execution layer.

It exists for one purpose:

> if a completed task changes how future work should be prioritized, validated, or closed out, that learning must land somewhere durable instead of living only in chat history.

## When To Use

Use this runbook after any task, phase, or recovery round that produced at least one of the following:

- a repeated failure mode
- a repeated sequencing rule
- a new definition of "done"
- a new validation path or regression command
- a durable priority rule for what to do next

Do not use it for one-off trivia, temporary environment noise, or preferences that do not change future behavior.

## Landing Ladder

Choose the highest truthful landing tier that the lesson actually deserves.

| Tier | Landing surface | Use when |
|---|---|---|
| 0 | No durable landing | The lesson is one-off or does not change future behavior |
| 1 | Repo memory / session state equivalent | The lesson should bias future decisions but is still repository-local and small |
| 2 | Runbook / policy doc | The lesson should be visible to future operators and repeated over months |
| 3 | Script / validator / regression entry | The lesson can be enforced or checked mechanically |
| 4 | CI / hook / audit gate | The lesson must become merge- or closeout-blocking |
| 5 | Skill / reusable template surface | The lesson is portable across tasks or repositories and benefits from a reusable invocation contract |

Design rule:

If a lesson can honestly become a script or validator, prefer that over leaving it as prose.

## Required Questions

Every harvest decision must answer these questions:

1. What changed future behavior?
2. Why is this not a one-off observation?
3. What is the lightest truthful landing tier?
4. Is there already an existing doc, script, or skill that should be updated instead of creating a new surface?
5. What future trigger should cause revalidation or promotion to a stronger tier?

## Required Packet Shape

Use `templates/experience_harvest_packet.template.md` as the default packet shape.

At minimum, the packet must include:

- trigger
- evidence
- decision
- landing tier
- enforcement level
- revalidation trigger

The packet is the durable explanation surface. The script, doc, or skill is the durable behavior surface.

## Promotion Rules

Use these default promotion rules:

| From | To | Promote when |
|---|---|---|
| Tier 1 | Tier 2 | The same lesson affects multiple future tasks or phases |
| Tier 2 | Tier 3 | The lesson can be validated mechanically |
| Tier 3 | Tier 4 | Failing to enforce it would cause user-facing, closeout, or trust regressions |
| Tier 2-4 | Tier 5 | The lesson is portable across repositories or repeated task families |

## Closeout Rule

Post-task harvest is part of closeout, not an optional appendix.

A task closeout is incomplete when:

- a real reusable lesson exists
- and no landing decision was recorded
- or the recorded landing decision contradicts the chosen enforcement level

## Minimal Operating Pattern

1. Fill one harvest packet.
2. Choose the landing tier.
3. Land it in the lightest truthful surface.
4. If applicable, add or update a script/check.
5. Record the revalidation trigger.

That is enough for v1.