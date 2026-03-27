# Execution Budget

This document explains why the execution budget system exists, how it works,
and how it prevents rate-limit-triggering runaway agent behavior.

---

## Why It Exists

An LLM-based agent is subject to several failure modes that purely
instruction-based rules cannot prevent reliably:

| Failure mode | Effect |
|---|---|
| Infinite progression loops | Agent runs Rule 14 indefinitely without user input |
| Heavy reasoning overuse | Architect invocations or deep analysis chains consume excessive tokens |
| Repeated reality checks | Rule 17 runs on every micro-step rather than per loop cycle |
| Stagnation loops | Agent produces no real output across multiple cycles and still continues |

All of these can trigger API rate limits, exhaust context windows, and produce
outputs that are more expensive and less useful than a clean stop.

Relying on the model to count its own iterations is insufficient — the model
has no reliable long-term memory of how many loops it has completed. A
deterministic, script-backed counter that reads and writes `session_state.md`
directly is required.

---

## Why Scripts Instead of Rules Alone

Framework rules (like Rule 14 and Rule 17) describe what the agent *should*
do. They do not enforce a hard stop when the agent is in a loop.

Scripts provide:

- **Determinism** — a counter in `session_state.md` is authoritative. The
  script increments it and checks it; the model's internal count is irrelevant.
- **Persistence** — `session_state.md` survives across turns. The budget
  carries forward even if the model loses context.
- **Auditability** — the exact state of the budget is visible in the file at
  any point.
- **Enforcement independence** — the gate logic lives in the script, not in
  the model. The model reads the output and applies it literally.

---

## How the Pipeline Works

The execution budget system is implemented as a **Pipeline skill** located at
`.github/skills/execution-budget/SKILL.md`.

Every iteration of the Rule 14 progression loop must run the pipeline before
any work begins:

```
Step 1 — Update Budget State
  └── bash scripts/execution_budget/update_budget.sh --loop   (or --heavy / --reality / --stagnation)

Step 2 — Check Budget
  └── bash scripts/execution_budget/check_budget.sh
       → prints Execution Budget Report + Budget Enforcement block

Step 3 — Decision Gate
  └── agent reads enforcement output and applies hard gates:
       - Autonomous progression allowed: NO  → STOP
       - Heavy reasoning allowed: NO         → skip Architect
       - Reality check allowed: NO           → skip Rule 17

Step 4 — Execution Permission
  └── agent may proceed only after gates are applied
```

The scripts read and write `session_state.md`. The counter fields live under
`## Execution Budget` in that file.

---

## How It Prevents Rate-Limit-Triggering Behavior

| Runaway pattern | Budget mechanism that stops it |
|---|---|
| 10+ progression loop iterations | `Loop Count` limit (default: 5) — autonomous progression blocked at limit |
| Multiple Architect invocations per session | `Heavy Reasoning Calls` limit (default: 2) — Architect blocked after limit |
| Reality check on every micro-step | `Reality Checks` limit (default: 3) — Rule 17 skipped after limit |
| Agent spinning with no output | `Stagnation Count` limit (default: 2) — progression stopped after 2 no-progress cycles |

When any hard limit is reached, the agent stops, writes a blocker to
`session_state.md`, and surfaces it to the user. This produces a clean,
observable stop instead of a runaway degradation.

---

## Budget Limits

Default limits are defined in `templates/session_state.template.md`:

```
**Loop Count**: 0 / 5
**Heavy Reasoning Calls**: 0 / 2
**Reality Checks**: 0 / 3
**Stagnation Count**: 0 / 2
**Budget Status**: healthy
```

These defaults are intentionally conservative. A user may raise specific
limits for a long-running task by editing `session_state.md` directly.
The scripts will respect whatever limit is written in the file.

---

## Files

| File | Purpose |
|---|---|
| `.github/skills/execution-budget/SKILL.md` | Defines the Pipeline skill and gates |
| `scripts/execution_budget/update_budget.sh` | Increments a counter in `session_state.md` |
| `scripts/execution_budget/check_budget.sh` | Reads budget state and prints enforcement report |
| `templates/session_state.template.md` | Contains the `## Execution Budget` section template |

---

> Updated 2026-03-27: initial implementation — deterministic script-backed budget system.
