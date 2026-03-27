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

### Step 1 — Load State

Before any budget check, confirm that `session_state.md` is present and
contains both required sections:

- `## Execution Budget` — loop, heavy reasoning, reality check, and stagnation counters
- `## Platform Constraints` — cooldown status, retry-after, last platform event

If either section is missing, copy it from `templates/session_state.template.md`
before continuing. Do **not** proceed to Step 2 without both sections present.

---

### Step 2 — Run Budget Check

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

PIPELINE DEGRADED: constrained
```

Parse both `Execution Mode` and the `PIPELINE` status line. The script exits
with code `1` when autonomous progression must stop.

---

### Step 3 — HARD GATE ⛔ (NON-BYPASSABLE)

Read the `Execution Mode` field and apply the corresponding mode behavior
**literally and immediately**.

**DO NOT PROCEED if gate conditions are violated.**

#### Mode: `exhausted` — STOP UNCONDITIONALLY

`PIPELINE BLOCKED: exhausted`

1. Do **not** continue any task.
2. Write a blocker to `session_state.md` under `## Blocker / Decision Needed`.
3. Summarize the current state for the user: what was completed, what is blocked.
4. Ask for the next user-triggered action before resuming.
5. If triggered by a platform cooldown (`Cooldown Active: yes`), follow Rule 19.

There are **no exceptions** to exhausted-mode stop behavior.

#### Mode: `constrained` — LIGHTWEIGHT ONLY

`PIPELINE DEGRADED: constrained`

Continue, but enforce all of the following without exception:

- **NO Architect invocation.** Heavy reasoning is fully blocked.
- **NO Rule 17 (reality check).** Skip for this iteration.
- **NO multi-step planning.** Do not expand scope.
- **Direct continuation only.** Proceed with the next concrete step using
  already-known information.

#### Mode: `healthy` — FULL EXECUTION

`PIPELINE OK`

Full execution is permitted. Apply individual field gates:

| Report field | Hard gate behavior |
|---|---|
| `Autonomous progression allowed: NO` | **STOP.** Declare the blocker in `session_state.md`. |
| `Heavy reasoning allowed: NO` | **Do not invoke the Architect.** |
| `Reality check allowed: NO` | **Do not run Rule 17.** |

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
- **Rule 19 (Platform Rate-Limit Response)**: platform cooldown sets `Execution Mode: exhausted`; this skill enforces the pipeline stop.
- **Rule 20 (Pipeline Enforcement)**: this skill is the implementation of Rule 20 — the pipeline is mandatory and non-bypassable.
- **Architect role**: blocked by this skill when heavy reasoning budget is exhausted or mode is `constrained`/`exhausted`.
- **Rule 16 (Planning)**: planning work counts as a loop iteration; update `--loop` before planning begins.
