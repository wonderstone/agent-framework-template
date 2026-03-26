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

*Project facts: `.github/project-context.instructions.md`*
*Canonical doc index: `docs/INDEX.md`*
*Cross-session state: `session_state.md`*
