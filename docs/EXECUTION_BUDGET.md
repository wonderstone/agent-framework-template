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

## Execution Modes

The budget system exposes one of three execution modes, determined entirely by
the scripts — not by freeform agent judgment:

| Mode | Meaning | Agent behavior |
|---|---|---|
| `healthy` | All budgets within limits, no platform cooldown | Full execution permitted |
| `constrained` | Some feature limits reached (heavy reasoning or reality checks) but loop not exhausted | Lightweight-only continuation; no Architect, no Rule 17 |
| `exhausted` | Loop limit hit, stagnation detected, or platform cooldown active | Stop, summarize, wait for user |

The mode is printed as `Execution Mode` in the `check_budget.sh` output and
also stored as `**Execution Mode**` in the `## Platform Constraints` section of
`session_state.md`.

### Why Degraded Mode Exists

Without a `constrained` mode, the only options are "continue as normal" or
"stop completely." A constrained mode lets the agent make forward progress on
a task while avoiding the actions most likely to consume tokens or trigger rate
limits — specifically Architect invocations and repeated reality-check passes.

This is preferable to an immediate full stop because:
- The user still gets output and progress.
- The agent avoids the high-cost operations that cause runaway behavior.
- The stop is deferred until it is actually required (budget exhausted).

### Local Budget vs Platform Constraint

The execution budget tracks local counters (loop iterations, heavy reasoning
calls, etc.) that reset per session. These prevent runaway loops within a
single session.

The `## Platform Constraints` section in `session_state.md` tracks external
signals — rate-limit responses, cooldown periods, retry-after headers — from
the platform running the agent. These are independent of local counters.

**A platform cooldown overrides local budget state.** Even if all local
counters are at 0, a `Cooldown Active: yes` flag forces `exhausted` mode.
This is enforced by `check_budget.sh` directly.

### Why Early Stopping Is Preferred Over Retry Loops

A retry loop under a platform cooldown will:
1. Consume additional requests against the rate limit.
2. Potentially trigger a longer cooldown or a harder block.
3. Produce no useful output while burning context.

Stopping cleanly and surfacing the state to the user costs nothing and
preserves the session context for a clean resume. Rule 19 in
`copilot-instructions.md` mandates this behavior.

---

## Pipeline Enforcement Model

The execution budget system is implemented as a **4-stage enforced pipeline**.
Every agent iteration must pass through all four stages. No stage may be skipped.

```
Stage 0 — Signal Capture
  └── Agent writes platform signals (rate-limit, cooldown, retry-after) to
      ## Platform Constraints in session_state.md

Stage 1 — Budget Evaluation
  └── bash scripts/execution_budget/update_budget.sh --loop (or --heavy / --reality / --stagnation)
       → increments the relevant counter in session_state.md

Stage 2 — Execution Gate (HARD STOP)
  └── bash scripts/execution_budget/check_budget.sh
       → reads both ## Execution Budget and ## Platform Constraints
       → determines Execution Mode
       → prints PIPELINE OK / DEGRADED / BLOCKED
       → exits 1 if progression must stop

Stage 3 — Controlled Execution
  └── agent applies mode behavior strictly:
       - healthy     → full execution
       - constrained → lightweight only (no Architect, no Rule 17)
       - exhausted   → STOP — summarize — ask user
```

### Mode Behavior Table

| Mode | Allowed Actions | Blocked Actions |
|---|---|---|
| `healthy` | Full execution; Architect; Rule 17 | None (individual budget fields still apply) |
| `constrained` | Direct continuation only | Architect, Rule 17, multi-step planning |
| `exhausted` | Summarize state, surface to user | Everything — agent must stop |

### Why This Is a Hard Gate

Stage 2 is not advisory — the script is the **single source of truth**. The
agent reads the pipeline status line (`PIPELINE OK / DEGRADED / BLOCKED`) and
the exit code, then applies them without interpretation. Rule 20 in
`copilot-instructions.md` mandates this and defines what constitutes an
invalid execution.

The gate exists because:
- LLM self-discipline cannot be relied on to count iterations accurately
- A file-backed counter survives across turns and context windows
- The script output is deterministic and auditable
- Platform cooldowns must override local budget state instantly

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

When a rate-limit or cooldown signal is received, the agent must:

1. Write to `## Platform Constraints` in `session_state.md`:
   - `Last Platform Event`: brief description of the signal
   - `Cooldown Active`: yes
   - `Retry After`: value if known
   - `Execution Mode`: exhausted

2. The next `check_budget.sh` run will detect `Cooldown Active: yes` and
   output `Execution Mode: exhausted`, blocking all progression.

3. The agent stops, summarizes, and waits for the user to confirm the
   cooldown has lifted before resetting `Cooldown Active` to `no`.

---

## Files

| File | Purpose |
|---|---|
| `.github/skills/execution-budget/SKILL.md` | Defines the Pipeline skill, modes, and gates |
| `scripts/execution_budget/update_budget.sh` | Increments a counter in `session_state.md` |
| `scripts/execution_budget/check_budget.sh` | Reads budget + platform state; prints enforcement report with Execution Mode |
| `templates/session_state.template.md` | Contains `## Execution Budget` and `## Platform Constraints` sections |

---

> Updated 2026-03-27: initial implementation — deterministic script-backed budget system.
> Updated 2026-03-27: added Execution Mode (healthy/constrained/exhausted), Platform Constraints section, Rule 19.
