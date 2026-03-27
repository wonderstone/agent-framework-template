# Adoption Guide

Step-by-step guide for adopting this agent framework in a new project.

---

## Prerequisites

- GitHub repository (new or existing)
- A coding assistant that reads `.github/copilot-instructions.md` (GitHub Copilot, Cursor, Augment, etc.)
- Bash (to run `scripts/validate-template.sh` after setup)

---

## Step 1 — Copy the Core Files

Copy these files into your new repository, preserving their paths:

```
.github/
  copilot-instructions.md          ← operating rules (Rule 0–11)
  project-context.instructions.md  ← project adapter (fill in Step 2)
  agents/
    architect.agent.md             ← analysis/planning agent
    implementer.agent.md           ← execution/validation agent
  instructions/
    backend.instructions.md        ← backend change protocol
    docs.instructions.md           ← documentation change protocol

docs/
  INDEX.md                         ← TYPE-A doc navigation index
  FRAMEWORK_ARCHITECTURE.md        ← how the layers work (optional, keep for ref)
  ADOPTION_GUIDE.md                ← this file (optional, keep for ref)
  archive/                         ← empty dir for TYPE-C docs (keep it)

templates/
  project-context.template.md      ← blank project adapter to fill in
  session_state.template.md        ← blank session state to fill in
  roadmap.template.md              ← blank ROADMAP to fill in
```

---

## Step 2 — Fill In the Project Adapter

Open `.github/project-context.instructions.md` and replace every `[placeholder]`:

| Placeholder | Replace with |
|---|---|
| `[Project Name]` | Your project name |
| Project Map rows | Your actual directory structure |
| Canonical Docs rows | Your actual key docs |
| Critical Topic Triggers | Keywords that matter in your domain |
| Build and Test Commands | Your actual build/test/lint commands |
| Protected Paths | Paths that require explicit confirmation before destructive ops |
| Runtime Config Locations | Where your config files live |

Use `templates/project-context.template.md` as a blank starting point if preferred.

---

## Step 3 — Initialize session_state.md

Copy `templates/session_state.template.md` to the project root as `session_state.md`.

Fill in:
- **Current Goal**: one sentence describing what you are working on right now
- **Working Hypothesis**: state the current working assumption (e.g., "The fix requires X" or "The root cause is Y") — even for well-understood tasks, a brief hypothesis anchors the cognitive loop
- **Confidence**: High / Medium / Low
- **Acceptance Criteria**: the observable conditions that mark your first phase complete

Leave everything else blank or with placeholder text until the first subtask is confirmed done.

---

## Step 4 — Create docs/INDEX.md

Your `docs/INDEX.md` starts with the core docs that exist. For a new project, that might be just:

```markdown
| Document | Description |
|---|---|
| `README.md` | Project entry point |
| `docs/FRAMEWORK_ARCHITECTURE.md` | Agent framework layer design |
| `docs/ADOPTION_GUIDE.md` | How to adopt this framework |
```

Update this index every time you add or remove a TYPE-A document.

---

## Step 5 — Verify docs/archive/ Exists

The `docs/archive/` directory ships with the template (it contains a `.gitkeep`). Confirm it is present after copying:

```bash
ls docs/archive/
```

If it is missing (e.g., some copy tools skip empty-ish directories), recreate it:

```bash
mkdir -p docs/archive
touch docs/archive/.gitkeep
```

All TYPE-C documents (phase reports, one-time analyses, summaries) go here.

---

## Step 6 — Initialize ROADMAP.md

Copy `templates/roadmap.template.md` to the project root as `ROADMAP.md`.

Fill in:
- **Phase 1 name and goal**: one sentence describing what the first phase achieves
- **Initial subtasks**: the work items you know about right now
- **Acceptance criteria**: observable conditions that mark Phase 1 complete

Rules 9 and 10 both write to `ROADMAP.md` (updating rows to `✅ YYYY-MM-DD`), so this file must exist before the agent starts work.

---

## Step 7 — Customize Rule 8 Footer Language (Optional)

The default footer in `copilot-instructions.md` uses English. If your team works in another language, update the footer examples in Rule 8 accordingly.

---

## Step 8 — Remove What You Don't Need

The following files are optional and can be removed for simpler projects:

| File | Remove if... |
|---|---|
| `.github/agents/architect.agent.md` | You don't use separate analysis agents |
| `.github/agents/implementer.agent.md` | Same as above |
| `.github/instructions/backend.instructions.md` | Not a backend project |
| `.github/instructions/docs.instructions.md` | Documentation is minimal |
| `docs/FRAMEWORK_ARCHITECTURE.md` | Team is familiar with the framework |
| `templates/` | All templates have been applied |

---

## Minimal Viable Setup

If you want the smallest possible setup:

```
.github/
  copilot-instructions.md          ← keep (core rules)
  project-context.instructions.md  ← keep (fill in)

docs/
  INDEX.md                         ← keep (update as docs grow)
  archive/                         ← keep (ships empty)

session_state.md                   ← create from templates/session_state.template.md
ROADMAP.md                         ← create from templates/roadmap.template.md
```

Everything else is additive.

After setup, run `bash scripts/validate-template.sh` from the repo root to confirm no required files are missing.

---

## Ongoing Maintenance

| Trigger | Action |
|---|---|
| New TYPE-A doc added | Update `docs/INDEX.md` |
| Phase complete | Archive to `docs/archive/`, rotate `session_state.md`, mark ROADMAP |
| Protected path changes | Update `project-context.instructions.md` |
| New topic trigger needed | Add row to Critical Topic Triggers in adapter |
| `session_state.md` exceeds ~100 lines | Archive old phase content; keep current phase + insights |

---

## Pipeline Enforcement at Runtime

The framework includes a deterministic pipeline enforcement system that prevents
runaway loops and rate-limit storms. Every agent iteration must pass through a
4-stage pipeline before any task is permitted to execute.

### How it works

```
Stage 0 — Signal Capture
  Agent writes platform events (rate-limit, cooldown) to
  ## Platform Constraints in session_state.md

Stage 1+2 — Enforcement (sole valid runtime command)
  bash scripts/execution_budget/enforce_pipeline.sh --loop
    (or --heavy, --reality, --stagnation)

Stage 3 — Hard Gate
  Script outputs PIPELINE OK / DEGRADED / BLOCKED
  Exit 1 on BLOCKED — agent must not continue

Stage 4 — Controlled Execution
  healthy     → full execution
  constrained → lightweight only (no Architect, no Rule 17)
  exhausted   → STOP — summarize — wait for user
```

`enforce_pipeline.sh` is the **sole valid runtime command**. `update_budget.sh`
and `check_budget.sh` are internal implementation details — they are called by
the wrapper, never directly by the agent during task execution.

### What happens when PIPELINE BLOCKED appears

When `check_budget.sh` or `enforce_pipeline.sh` outputs `PIPELINE BLOCKED: exhausted`
and exits with code `1`, the agent **must**:

1. Stop all task execution immediately.
2. Write a blocker entry to `session_state.md` under `## Blocker / Decision Needed`.
3. Surface a human-readable summary: what was completed, what is blocked, why.
4. Wait for the user to take action before resuming.

The agent must **not**:
- Start a new subtask
- Call the Architect
- Run a reality check (Rule 17)
- Make any file edits except `session_state.md`

### Why bypass is impossible

The enforcement guarantee rests on three mutually reinforcing layers:

| Layer | Mechanism |
|---|---|
| **Script exit code** | `check_budget.sh` exits `1` when exhausted; any shell pipeline that checks `$?` will fail |
| **Pipeline status line** | `PIPELINE BLOCKED: exhausted` is the last line of output — easily grep-able; agents read it literally |
| **Rule 20 (copilot-instructions.md)** | Defines any deviation as an *invalid execution* — the agent instruction set treats skipping the pipeline the same as violating a hard safety rule |

None of these can be bypassed without explicitly overriding the scripts or the
instructions. The counters live in `session_state.md` as plain text that
persists across turns and context windows — the model's internal state has no
bearing on what the file contains.

### Verifying the pipeline is working

Run the edge-case test suite to confirm all enforcement behaviors work:

```bash
bash scripts/execution_budget/test_pipeline.sh
```

Expected output: 11 assertions, all passing (✅).

---

## Troubleshooting

**Agent ignores the rules**: confirm `.github/copilot-instructions.md` is being loaded by your AI assistant. Some tools require explicit activation.

**Agent doesn't load the right doc**: check the Critical Topic Triggers in your project adapter — ensure the keyword matches what appears in typical user messages.

**session_state.md is out of sync**: treat the actual code as truth; update session_state.md to match, not the other way around.

**`PIPELINE BLOCKED` appears unexpectedly**: check `session_state.md` → `## Platform Constraints`. If `Cooldown Active: yes`, a platform rate-limit was received. Reset it to `no` only after confirming the cooldown has lifted, then re-run the budget check.

**Agent continues after PIPELINE BLOCKED**: this is a Rule 20 violation. The agent's instruction set explicitly defines this as invalid. Verify that `copilot-instructions.md` contains Rule 20 and that it is being loaded. Run `bash scripts/validate-template.sh` to check integrity.

**Budget counters seem wrong**: counters in `session_state.md` accumulate across a session and are never auto-reset. To start a fresh session, reset the counters to `0` manually or copy from `templates/session_state.template.md`. Only do this between sessions, not mid-task.

**validate-template.sh fails with missing checks**: re-run after copying the latest `copilot-instructions.md` and `scripts/` from this template repository.
