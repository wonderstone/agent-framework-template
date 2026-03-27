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
and prints a report in this format:

```
Execution Budget Report
- Loop Count: 4 / 5
- Heavy Reasoning Calls: 2 / 2
- Reality Checks: 1 / 3
- Stagnation Count: 1 / 2
- Budget Status: constrained

Budget Enforcement
- Autonomous progression allowed: YES
- Heavy reasoning allowed: NO
- Reality check allowed: YES
- Required action if no progress next cycle: STOP
```

The script exits with code `1` when autonomous progression must stop.

---

### Step 3 — Decision Gate

Read the Budget Enforcement section of the report and apply it **literally**:

| Report field | Hard gate behavior |
|---|---|
| `Autonomous progression allowed: NO` | **STOP.** Do not continue. Declare the blocker in `session_state.md` and surface it to the user. |
| `Heavy reasoning allowed: NO` | **Do not invoke the Architect.** Do not run any heavy analysis block. Use only what is already known. |
| `Reality check allowed: NO` | **Do not run Rule 17.** Skip the reality check this iteration. |
| `Required action: STOP` | **STOP.** Do not proceed. Surface the budget-exhausted state to the user. |

Do not interpret these gates. Apply them literally.

---

### Step 4 — Execution Permission

Only after the gate in Step 3 has been applied may the agent proceed.

- If all gates allow continuation → proceed with the next subtask.
- If any gate blocked an action → respect the block and report it.
- If progression was stopped → write the blocker to `session_state.md`
  under `## Blocker / Decision Needed` and stop.

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
- **Rule 17 (Reality Check)**: blocked by this skill when reality check budget is exhausted.
- **Architect role**: blocked by this skill when heavy reasoning budget is exhausted.
- **Rule 16 (Planning)**: planning work counts as a loop iteration; update `--loop` before planning begins.
