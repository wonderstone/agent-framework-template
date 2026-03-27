# Execution Budget Skill

> **Pattern**: Pipeline  
> **Mandatory**: YES — run at the start of every iteration before any work begins.

---

## Purpose

This skill enforces a deterministic execution budget on each agent session.
It prevents runaway loops, excessive heavy reasoning, repeated reality checks,
and rate-limit-triggering behavior by maintaining hard counters that are
checked before any work is permitted to continue.

Relying solely on LLM self-discipline is not sufficient — this skill uses
shell scripts that read and write `session_state.md` directly, making
enforcement independent of model judgment.

---

## When to Invoke

Invoke this skill **at the start of every iteration of the Rule 14
progression loop**, before any of the following:

- Starting a new subtask
- Invoking the Architect role
- Running a Reality Check (Rule 17)
- Executing any heavy reasoning block

Do **not** skip this skill. If `session_state.md` does not contain an
`## Execution Budget` section, add it from the template before proceeding.

---

## Pipeline Steps

The steps below are **sequential and mandatory**. Do not reorder, skip, or
merge steps.

---

### Step 1 — Update Budget State

Record the event type that is about to occur by running the appropriate
update script. This increments the counter **before** the work starts.

| Event | Command |
|---|---|
| Loop iteration beginning | `bash scripts/execution_budget/update_budget.sh --loop` |
| Heavy reasoning about to run | `bash scripts/execution_budget/update_budget.sh --heavy` |
| Reality check about to run | `bash scripts/execution_budget/update_budget.sh --reality` |
| No progress made last cycle | `bash scripts/execution_budget/update_budget.sh --stagnation` |

Run this script from the repository root. The script writes the updated
counter back to `session_state.md` immediately.

---

### Step 2 — Check Budget

Run the budget check script to produce a structured enforcement report:

```
bash scripts/execution_budget/check_budget.sh
```

The script reads `session_state.md`, compares all counters against limits,
checks `## Platform Constraints` for any active cooldown, and prints a report
in this format:

```
Execution Budget Report
- Loop Count: 4 / 5
- Heavy Reasoning Calls: 2 / 2
- Reality Checks: 1 / 3
- Stagnation Count: 1 / 2
- Budget Status: constrained
- Execution Mode: constrained

Budget Enforcement
- Autonomous progression allowed: YES
- Heavy reasoning allowed: NO
- Reality check allowed: YES
- Allowed mode: constrained
- Required action if no progress next cycle: STOP
```

The script exits with code `1` when autonomous progression must stop.

---

### Step 3 — Decision Gate

Read the `Execution Mode` and `Budget Enforcement` fields and apply the
corresponding mode behavior **literally**:

#### Mode: `healthy`

| Report field | Hard gate behavior |
|---|---|
| `Autonomous progression allowed: NO` | **STOP.** Declare the blocker in `session_state.md` and surface it to the user. |
| `Heavy reasoning allowed: NO` | **Do not invoke the Architect.** Use only what is already known. |
| `Reality check allowed: NO` | **Do not run Rule 17.** Skip this iteration. |

#### Mode: `constrained`

All `healthy` gates apply, plus:

- **No Architect invocation.** Heavy reasoning is blocked regardless of the
  individual `Heavy reasoning allowed` field — constrained mode means lightweight-only.
- **No additional reality-check passes.** Skip Rule 17 for this iteration.
- **Prefer lightweight continuation only.** Proceed with the next concrete
  step using already-known information. Do not expand scope.

#### Mode: `exhausted`

**Stop unconditionally.** Do not continue.

1. Write a blocker to `session_state.md` under `## Blocker / Decision Needed`.
2. Summarize the current state for the user: what was completed, what is blocked.
3. Ask for the next user-triggered action before resuming.

If `exhausted` was triggered by a platform cooldown (`Cooldown Active: yes`),
follow Rule 19 in addition to stopping.

Do not interpret these gates. Apply them literally.

---

### Step 4 — Execution Permission

Only after the gate in Step 3 has been applied may the agent proceed.

- `healthy` → proceed with the next subtask normally.
- `constrained` → proceed with lightweight continuation only; no Architect, no Rule 17.
- `exhausted` → stop; summarize; wait for user input.

**Never continue without completing Steps 1–3 first.**

---

## Constraints

- Do not skip steps.
- Do not continue without a completed budget check.
- Do not invoke the Architect when heavy reasoning is blocked.
- Do not run a reality check when reality checks are blocked.
- Do not adjust limits mid-session without explicit user instruction.
- The scripts are the source of truth — not the agent's internal count.

---

## Budget Limits (defaults)

Limits are defined in the `## Execution Budget` section of `session_state.md`.
The template defaults are:

| Counter | Default Limit | Rationale |
|---|---|---|
| Loop Count | 5 | Prevents infinite progression loops |
| Heavy Reasoning Calls | 2 | Limits expensive multi-step analysis per session |
| Reality Checks | 3 | Prevents repeated alignment checks without progress |
| Stagnation Count | 2 | Forces a stop after two consecutive no-progress cycles |

These limits may be raised for a specific session by editing `session_state.md`
with explicit user approval.

---

## Integration with Framework Rules

- **Rule 14 (Progression Loop)**: invoke this skill at the start of each loop iteration.
- **Rule 17 (Reality Check)**: blocked by this skill when reality check budget is exhausted or mode is `constrained`/`exhausted`.
- **Rule 19 (Platform Rate-Limit Response)**: platform cooldown sets `Execution Mode: exhausted`; this skill enforces the stop.
- **Architect role**: blocked by this skill when heavy reasoning budget is exhausted or mode is `constrained`/`exhausted`.
- **Rule 16 (Planning)**: planning work counts as a loop iteration; update `--loop` before planning begins.
