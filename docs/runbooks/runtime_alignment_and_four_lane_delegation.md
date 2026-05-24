# Runtime Alignment And Four-Lane Delegation

## Purpose

This runbook freezes one reusable framework pattern for repositories that both:

1. delegate bounded implementation work across multiple CLI executor lanes
2. depend on live running services or other runtime surfaces for acceptance truth

The goal is to keep two truths coupled instead of treating them as separate cleanup steps:

1. `repo target` versus `running services` alignment
2. four-lane delegated execution with owner validation and honest lane-state reporting

This runbook exists because repositories can otherwise make two recurring mistakes.

1. accept delegated output against stale running services
2. narrate a four-lane operating model as if four lanes were always simultaneously controllable

## Scope

This runbook owns:

1. the runtime-alignment loop between source truth, deploy truth, and running-service truth
2. the reusable four-lane delegation model for bounded long tasks
3. the distinction between `logical lane model` and `currently controllable lane count`
4. the owner-review rules for accepting live-runtime-dependent work
5. the summary and template surfaces that make the pattern reusable

## Non-Goals

This runbook does not:

1. require every repository to use four lanes at all times
2. replace the narrower managed-terminal handshake runbook
3. replace repo-specific capability matrices or executor-choice rules
4. treat runtime alignment as a substitute for focused product validation
5. let delegated executors own roadmap, state, or closeout truth

## Core Model

Repositories using this pattern distinguish two independent dimensions.

### A. Runtime Alignment

`Runtime alignment` means the repository can compare:

1. intended repo target
2. deployed bundle or runtime payload
3. actually running service or user-facing runtime

The comparison does not need one universal implementation shape.

It does need one honest operator-visible or maintainer-visible proof surface.

### B. Four-Lane Delegation

`Four-lane delegation` means the repository tracks four logical execution seats for bounded work.

Those four lanes may map to:

1. four different CLIs
2. four profiles on fewer underlying CLIs
3. four role-labeled seats in a mixed human-plus-tool workflow

Hard rule:

1. the logical four-lane model does not imply that four controllable execution IDs always exist right now
2. summaries must report the current controllable lane count honestly

## Responsibilities

| Responsibility | Owner | Meaning |
|---|---|---|
| Packet freeze | main thread or owner | freeze scope, validation, and do-not-touch boundary before dispatch |
| Lane execution | delegated lane | run one bounded packet to `DONE`, `STUCK`, or `ESCALATE` |
| Runtime alignment | owner plus live runtime surfaces | prove that live runtime truth matches the intended target closely enough for acceptance |
| Acceptance | main thread or owner | validate, decide acceptance, sync docs or state, and close out truthfully |

## Runtime Alignment Loop

Repositories should keep the runtime loop explicit.

1. identify the repo target to which the acceptance claim refers
2. sync or rebuild the deploy or runtime bundle if the repository has that layer
3. restart or refresh the affected runtime through the repository's canonical control surface
4. verify lightweight liveness separately from heavier runtime-consistency truth when both surfaces exist
5. compare repo target versus running runtime using the repository's chosen evidence surface
6. only then accept user-visible or live-runtime-dependent outcomes

Hard rule:

1. if the task depends on live runtime truth, `tests passed in source` is not enough by itself when the running service may still be stale

## Four-Lane Model

The reusable model is role-first rather than tool-first.

| Lane | Meaning | Typical ownership |
|---|---|---|
| Lane A | broad reasoning, spec, or cross-file review work | reasoning-oriented executor or reviewer |
| Lane B | implementation-heavy bounded work | implementer executor |
| Lane C | independent review or alternative implementation seat | reviewer or second implementation executor |
| Lane D | display-surface, observability, or cross-cutting presentation work when separated from domain logic | dedicated display or observability executor when the repository wants one |

Repositories may rename these lanes to concrete agent labels.

Examples:

1. `Claude Code`, `Codex`, `Gemini`, `Copilot`
2. `Spec`, `Implementer`, `Reviewer`, `Display`
3. `Claude`, `Codex`, `DeepSeek`, `Frontend/Backend`

The framework-level rule is the same in every case:

1. keep the logical seat stable for summary and packet interpretation
2. keep the current machine-controllable lane count honest

## Dispatch Rules

Before dispatching a lane packet under this pattern, require all of the following.

1. the task is packet-ready
2. the packet has a bounded file or module scope
3. the packet names focused validation or a review-only acceptance boundary
4. the packet says whether live runtime alignment is part of the acceptance claim
5. the owner can state the lane role clearly enough that the end-of-round summary remains interpretable

## Active-Lane Honesty Rule

This rule is mandatory.

1. do not summarize all four lanes as active when fewer are actually controllable
2. if one or more lanes are only logical placeholders for the current round, label them as `planned`, `idle`, `not currently controllable`, or an equivalent honest state
3. if a lane lost its control anchor, keep the lane identity but downgrade the state rather than silently claiming full activity

## Acceptance Rules

When live runtime matters, acceptance requires both:

1. the delegated packet evidence
2. the runtime-alignment evidence relevant to the affected user or operator surface

Acceptance is incomplete if either of the following is true.

1. the delegated lane returned `DONE` but the running service still exposes stale truth
2. the runtime surface looks healthy but the delegated packet never produced bounded task evidence

## Failure Modes And Recovery

| Failure mode | Meaning | Recovery |
|---|---|---|
| `repo fixed / live stale` | source change exists but runtime still serves older behavior | rerun the repository's deploy-sync or restart path and re-check runtime truth |
| `four-lane fiction` | status surface claims four active lanes without four controllable seats | downgrade the summary to the truthful active count and record missing seats explicitly |
| `runtime truth overloaded into liveness` | one heavy consistency route makes the lightweight health route misleading or slow | split liveness from heavy comparison again |
| `packet-done without runtime proof` | delegated success was accepted too early | reject acceptance and run the runtime loop |

## Observability

This pattern is strongest when repositories ship:

1. one lightweight liveness surface or equivalent cheap health check
2. one heavier runtime-consistency or repo-versus-runtime comparison surface when live runtime matters
3. one per-round four-lane status table or equivalent summary artifact

Use `templates/four_lane_runtime_alignment_status.template.md` as the default starter when the repository wants a reusable four-lane summary that also records runtime dependency.

## Adopter Guidance

Repositories adopting this runbook should customize only these parts.

1. lane names
2. runtime entrypoints
3. deploy-sync or rebuild commands
4. validation commands

They should keep these invariants unchanged.

1. live-runtime-dependent acceptance requires runtime proof
2. four logical lanes do not imply four active control anchors
3. owner review remains the acceptance boundary

## Acceptance Criteria

1. The repository has one canonical runbook for coupling runtime alignment with four-lane delegation.
2. The runbook distinguishes logical lane model from current controllable lane count.
3. The runbook states that live-runtime-dependent acceptance needs runtime proof, not source-only validation.
4. The runbook points to one reusable status template for four-lane summaries.

## Validation Plan

1. `docs/INDEX.md` references this runbook.
2. `.github/instructions/project-context.instructions.md` routes runtime-alignment or multi-lane delegation topics to this runbook.
3. `templates/four_lane_runtime_alignment_status.template.md` exists.
4. `python3 scripts/validate_template.py`

> Updated 2026-05-11: Added as the generic framework runbook for repositories that need both runtime-alignment proof and honest four-lane delegated execution summaries.