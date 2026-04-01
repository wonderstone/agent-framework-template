# Leftover Unit Contract

This document defines the **leftover unit** — a structured representation of work that has been intentionally stopped before full completion.

---

## The Problem

Every non-trivial project has work that is started but not finished. The naive response is to pretend it doesn't exist, or to add a vague TODO comment. Both approaches create hidden debt: the next session cannot distinguish "this was never started" from "this was 60% done and stopped for a specific reason."

The leftover unit contract solves this by making "stopping partway" an explicit, auditable engineering state — not a failure to be hidden.

---

## Core Principle

A leftover is not a failure. It is not forgotten work. It is work that:

1. Has a clear record of where it stopped
2. Has a clear record of why it stopped
3. Has a clear record of what is still missing
4. Can be re-entered without reconstructing context from memory

If those four things are true, the leftover is **recoverable**. If any of them is missing, the leftover is **debt**.

---

## The Leftover Unit Fields

Every leftover unit must have these five fields:

### `slice_id`

A unique identifier for the unit of work. Typically follows the pattern `[module]_[feature]_[scope]`.

Examples: `auth_token_refresh_api`, `image_artifact_delivery_flutter`, `search_vector_indexer`

### `why_stopped`

The real reason work stopped. This should be honest, not optimistic.

Good examples:
- `no stable live probe for this path`
- `blocked by dependency on X which is not yet stable`
- `ROI insufficient to continue this sprint; costs exceed expected benefit`
- `external API not yet available in staging environment`

Bad examples:
- `TODO`
- `not done yet`
- `will finish later`

### `current_truth`

The actual state of the work right now. What exists, what works, what doesn't.

This is not a list of what you planned to do. It is a description of what you can verify is true today.

Good examples:
- `API endpoint exists and returns 200; response schema is correct; live E2E not yet run`
- `Component renders correctly with mock data; real data integration not started`
- `Unit tests pass; integration test exists but is flaky under load`

### `missing_gate`

The specific gate that is missing — the thing that would need to be true before this leftover could be promoted to complete.

Examples:
- `stable live validator that can run repeatably in CI`
- `focused integration test that covers the happy path without mocks`
- `user acceptance confirmation on the actual output format`

### `next_reentry_action`

The first concrete action to take when re-entering this leftover. This should be specific enough that a new session can start without asking questions.

Good examples:
- `First: build a repeatable live probe at scripts/validate_X_live.py`
- `First: read ARCHITECTURE.md section 3 to understand the current boundary`
- `First: run the existing flaky test 5 times to characterize the failure mode`

Bad examples:
- `Continue work`
- `Finish implementation`

### `promotion_blocker`

The specific condition that would need to change before this leftover can be promoted to `ready_for_full_execution` or declared complete.

This is different from `missing_gate` (which describes a verification step). A promotion blocker is often external:

Good examples:
- `cannot promote until live validator script exists and is repeatable`
- `cannot promote until external API is available in staging`
- `cannot promote until STT/S2S surface has a stable focused test`

Bad examples:
- `not done`
- `more work needed`

---

## Recording a Leftover Unit

Leftover units belong in `session_state.md` under a dedicated section:

```markdown
## Leftover Units

### [slice_id]

- **why_stopped**: [real reason work stopped]
- **current_truth**: [verifiable current state — what exists and works today]
- **missing_gate**: [specific verification step still needed]
- **next_reentry_action**: [first concrete action to take on re-entry]
- **promotion_blocker**: [condition that must change before this can be promoted or declared complete]
```

For long-running leftovers that survive phase rotation, promote the entry to a TYPE-A doc or a dedicated leftover registry file. Do not let leftover units disappear during `session_state.md` rollover.

---

## Allowed Leftover States

Every unit of work that enters execution must land in one of four states. If you cannot determine which state applies, the work is not ready to enter execution.

| State | Meaning |
|---|---|
| `ready_for_full_execution` | Implementation complete, all gates passed, no blockers |
| `ready_for_partial_execution` | Some gates passed; can continue on a bounded scope |
| `implementation_complete_live_blocked` | Code done; live gate cannot run yet (env/credential/dependency) |
| `do_not_enter_yet` | Slice boundary not yet stable, or minimum validation surface missing |

`implementation_complete_live_blocked` is not a failure state. It means: the implementation is done to its current boundary; the live gate is the only missing piece; this should not be called "completed" yet.

`do_not_enter_yet` is a valid state. It means: we know this exists, we know we want to do it, but we cannot do it truthfully right now. Record it as a leftover rather than starting something that cannot be closed properly.

---

## Closeout Semantics

A leftover can be closed, but only in a truthful state. Allowed closeout expressions:

- `left as validated leftover`
- `implementation complete, live gate blocked`
- `not entered yet; missing slice boundary`

Not allowed unless all gates have been met:

- `completed`
- `accepted`
- `status=passed`
- `done`

This rule connects to Rule 25 (Receipt-Anchored Closeout): any of the "not allowed" expressions require a receipt anchor proving the gates were met.

---

## Slice Classification Before Entry

Before entering any new module section or feature scope, run a **slice classification**:

1. Find the canonical rule or closest authority doc for this area
2. Identify the `slice_id` for this unit of work
3. Record `entrypoints`, `owner_files`, `minimum_validation`, `live_gate_level`
4. Determine which of the four allowed states this slice is currently in

If you cannot complete step 4, the slice is in `do_not_enter_yet`. Record it as a leftover and move on.

---

## Integration with the Resumable Audit System

The leftover unit contract and the resumable audit artifact system (Rule 18) address different scopes:

| Mechanism | Scope | Lifetime |
|---|---|---|
| Handoff packet (Rule 18) | Single task or session interruption | Until the task resumes or is abandoned |
| Leftover unit | Feature or module slice; stops for days/weeks/indefinitely | Survives phase rotations; requires explicit re-entry |

A handoff packet captures "I was doing X and had to stop." A leftover unit captures "We decided to stop at this boundary for these reasons and here is how to come back."

Use handoff packets for tactical interruptions. Use leftover units for strategic deferral.
