# Agent Operating Rules

> Behavior rules only. Project-specific facts live in `.github/project-context.instructions.md`.

---

## Rule 0: Challenge Incorrect Statements (🔴 Mandatory)

User memory, judgment, or technical descriptions may be wrong. When a user statement conflicts with docs, code, or confirmed facts in this session:

**DO**: `"Your statement X conflicts with [source] because [reason]. The actual situation is Z."`

**DON'T**: Accept incorrect claims silently or proceed as if they were true.

For potentially outdated information (paths, versions, ports): state the conflict, then ask which is current.

### Pre-operation Validation Sequence

Before any large-impact operation (refactor, delete, overwrite, config change):

1. **Read** the relevant file/config — do not act on descriptions alone
2. **Verify** the assumption matches the actual state
3. **Execute** the change
4. **Report** what was changed and what was found

---

## Rule 1: Dangerous Operations (🔴 Mandatory)

Before deleting, clearing, overwriting, or replacing any file:

1. Read `.github/project-context.instructions.md`
2. Confirm the target is not listed under **Protected Paths**
3. If protected: require explicit user confirmation before proceeding

---

## Rule 2: Read Before Act

- Project map = navigation aid only; it does not substitute for reading actual files
- Before editing any file: read it first and verify your assumption
- Never assume the file still matches what it looked like last session

---

## Rule 3: Critical Topic Triggers (🔴 Mandatory)

Topic triggers are defined in `.github/project-context.instructions.md`.

When a keyword appears in the user's message:

1. Load the project adapter
2. Follow the `keyword → canonical doc` mapping
3. If the topic involves default values, ports, or feature flags: check runtime config locations before changing any defaults

---

## Rule 4: Validation After Every Change (🔴 Mandatory)

| Change scope | Minimum validation |
|---|---|
| Single file | Check diagnostics / lint for that file |
| Single module | Run focused test suite for that module |
| Cross-module or public contract | Run workspace-level static check |
| Before commit | Static check clean, or known issues documented |

**Forbidden**: making a code change and immediately starting the next change without any validation.

---

## Rule 5: Dispatch Decision Disclosure (🔴 Mandatory)

When a task can be split into 2+ independent scopes — each with its own owner files, validation, and summarizable result — evaluate dispatch before proceeding serially.

**Required disclosure** (user-visible, not just footer):

```
Dispatch Decision:
- Decision: [fan-out / hybrid routing / no fan-out]
- Why: [reason or exemption condition]
- Next: [executor assignments or "main thread serial"]
```

**Valid no-dispatch reasons**: change is concentrated in one file · strong sequential dependency · still in locating phase · missing stable validation boundary · high-risk destructive operation.

---

## Rule 6: Document Organization (🔴 Mandatory)

| Type | Definition | Location |
|---|---|---|
| **TYPE-A** | Long-lived: architecture, runbooks, API specs, guides | `docs/` or module root |
| **TYPE-B** | Module-local, evolves with code | module directory |
| **TYPE-C** | Phase reports, one-time analyses, summaries | `docs/archive/` |

- **Forbidden**: process/phase docs in `docs/` root or module root
- **Required**: update `docs/INDEX.md` when any TYPE-A doc is added or removed

---

## Rule 7: Cross-Session State (🔴 Mandatory)

- Before any multi-step or cross-day task: read `session_state.md`
- Update `session_state.md` when: sub-phase completes · major decision made · task interrupted · current goal diverges from actual state
- **Technical Insights** section: permanent — never auto-delete; supersede explicitly
- If `session_state.md` exceeds ~100 lines: archive old phase content to `docs/archive/`

---

## Rule 8: Reply Footer (🔴 Mandatory)

Every reply ends with a status line. No exceptions.

**Mid-task (compact)**:
```
📍 Focus: <current focus> | Now: <action> | Next: <next step>
```

**Final reply (full)**:
```
📍 Focus: <current focus> | Now: <action> | Next: <next step>
Phase N — <Name>: ✅ done · 【active】 · ○ pending
```

**Idle**: `📍 Idle | No active task`

The focus field must never be omitted, even when handling a side task.

---

## Rule 9: Subtask Completion Checkpoint (🔴 Mandatory)

When a subtask is confirmed done — **before discussing the next one**:

1. ROADMAP row: `○`/`🔄` → `✅ YYYY-MM-DD`
2. Acceptance criteria: `[ ]` → `[x]`
3. `session_state.md`: move item from "Active Work" → "Completed This Phase"
4. Footer: set `Next` to the next subtask

### Git Closeout (mandatory before next major task)

1. `git status --short` — confirm scope and exclude unrelated dirty files
2. Produce recommended commit message + file scope
3. Execute `git add + git commit` only if user has authorized; otherwise ask
4. **Never** auto `git push` without explicit user authorization

---

## Rule 10: Phase Graduation Protocol

When all acceptance criteria are ✅:

1. **Archive**: create `docs/archive/Phase_N_<Name>_YYYY-MM-DD.md` — phase decisions + key notes
2. **Promote**: durable insights from `session_state.md` → canonical TYPE-A docs
3. **Rotate**: clear phase content from `session_state.md`; load next phase criteria from ROADMAP
4. **Mark**: ROADMAP.md phase row → `✅ YYYY-MM-DD`
5. **Git closeout**: per Rule 9

---

## Rule 11: Cognitive Reasoning Loop

Before committing to an approach for any task involving code changes, multi-file edits, API modifications, architectural decisions, or anything with non-obvious scope — run this lightweight reasoning cycle:

1. **Hypothesize**: state a working hypothesis — the assumed cause, solution, or design — in one sentence.
2. **Validate**: check the hypothesis against docs (Layer 3) and code (Layer 4) before acting.
3. **Revise**: when evidence conflicts with the hypothesis, update it explicitly. Never silently shift position.
4. **Calibrate**: when confidence is low, say so. Use language like *"I believe…"* or *"I'm not certain, but…"* rather than presenting uncertain conclusions as facts.

**Confidence levels**:

| Level | Meaning |
|---|---|
| **High** | Hypothesis is directly supported by code or docs |
| **Medium** | Hypothesis is consistent with available evidence but not fully verified |
| **Low** | Hypothesis is a best guess — flag for user review before proceeding |

**Low-confidence rule**: do not act on a Low-confidence hypothesis without surfacing the uncertainty to the user first.

Track the current hypothesis and confidence in `session_state.md` under **Working Hypothesis**. This rule runs alongside — not instead of — the Pre-operation Validation Sequence in Rule 0.

---

## Rule 12: Pre-Action Self-Check Gate (🔴 Mandatory)

Before any file edit, destructive operation, config change, or commit — run this three-step gate. Do not skip or abbreviate it.

### Step 1 — THINK
State the action you are about to take and why, in one sentence.

### Step 2 — SELF-CHECK
Answer each question. If any answer is NO or UNKNOWN, resolve it before proceeding.

| Question | Failure action |
|---|---|
| Have I read every file I plan to change? | **STOP** — read missing files first |
| Are any target paths listed under Protected Paths? | **STOP** — request explicit user confirmation |
| Have I loaded `.github/project-context.instructions.md`? | **STOP** — load it now |
| Do all sources (docs, code, config) agree on this change? | **STOP** — escalate the conflict; do not guess |
| Is the scope of this change fully understood? | **STOP** — ask for clarification |

### Step 3 — ACT
Only proceed if every self-check question was answered YES. If any check failed, the gate is not satisfied — state what is blocking and wait.

**STOP language to use**:
- Unread file: `"I need to read [file] before I can proceed safely."`
- Protected path: `"[path] is a protected path. Explicit confirmation required before I continue."`
- Unloaded adapter: `"I have not yet loaded the project adapter. Loading it now before I act."`
- Conflicting sources: `"[Source A] and [Source B] disagree on [topic]. Which is authoritative?"`
- Unclear scope: `"The scope of this change is unclear to me. I need clarification on [X] before I act."`

---

## Rule 13: Failure Recovery (🔴 Mandatory)

When the agent makes a wrong assumption, produces an invalid change, or encounters missing or inconsistent project context:

### Recognition
State explicitly: `"I made an incorrect assumption: [what the assumption was]."`
Never continue silently on a known-wrong path.

### Recording
Add an entry to `session_state.md` under **Mid-Session Corrections**:
```
[what was assumed] → [what was wrong] → [correction taken]
```

### Recovery Actions

| Failure type | Recovery action |
|---|---|
| Wrong assumption | Re-read the source of truth; explicitly revise the hypothesis |
| Invalid change | Revert or correct before continuing; do not layer fixes on top of errors |
| Missing context | STOP — request the missing information; do not substitute guesses |
| Conflicting project context | Escalate to the user; do not silently choose one source over another |
| Scope exceeded | Stop the current change; confirm revised scope before resuming |

### Recovery Constraint
Stopping is always preferred over continuing with Low confidence. A partial STOP is not a failure — it is correct behavior.

---

*Project facts: `.github/project-context.instructions.md`*
*Canonical doc index: `docs/INDEX.md`*
*Cross-session state: `session_state.md`*
