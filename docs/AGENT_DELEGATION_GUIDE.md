# Agent Delegation Guide

> **Type:** TYPE-A design doc (framework mechanism)
> **Scope:** how to delegate, accept, and recover work across agent roles
> **Status:** draft — refine as more tranches are executed across adopted repos

This document defines how the main agent delegates work to implementation
agents, accepts or rejects output, and recovers from common failure modes.
It is derived from real multi-agent coordination problems observed across
a full A–E1 phase pipeline. Agent names (Claude Code, Codex, DeepSeeK) are
used as concrete examples; the rules apply to any comparable agent setup.

When a delegated tranche also depends on live running services, pair this guide with `docs/runbooks/runtime_alignment_and_four_lane_delegation.md` so source-level acceptance is not confused with runtime-aligned acceptance.

---

## 1. Agent Capability Matrix

**Hard rule:** Match the task type to the agent. Do not ask a code-only agent
to resolve semantic ambiguity, and do not ask a spec agent to implement from
an unresolved contract.

| Task Type | Agent Profile | Why |
|---|---|---|
| Spec, contract wording, cross-file consistency | **Claude Code** (doc/spec/review agent) | Heavy reasoning, boundary definition, test-matrix enumeration |
| Code implementation, isolated subtree, harness | **Codex** (implementer agent) | Code-heavy, low semantic ambiguity, frozen contracts |
| Real host operator evaluation, SSH execution | **DeepSeeK or Claude Code** | Windows SSH, process observation, receipt capture |
| Scope freeze, tranche dispatch, acceptance | **Main agent (human)** | Architectural authority, cross-phase consistency |
| Review of agent output before acceptance | **Main agent (human)** | Contractual judgment, owner accountability |

### When to split across agents

- **Claude first, Codex later**: shared file with unresolved semantics →
  Claude drafts spec, owner accepts, Codex implements.
- **Codex first**: isolated new subtree with frozen contract →
  Codex implements directly.
- **Parallel only on disjoint surfaces**: safe when agents edit different
  directory subtrees with zero shared files.

**Historical lesson (Phase A/B0 parallel):**
A1 (Codex: Python schema enforcement in `cli.py`) and B0.2 (Claude:
lower-plane evidence doc in `docs/`) were safe to parallelize because
they edited disjoint surfaces. A2 and A1 on the same `cli.py` would
have conflicted.

**Historical lesson (Phase B1 spec-first):**
B1 (live-host control spec) was written before any Go implementation.
This prevented Codex from encoding unresolved ambiguity about what
`backend start` means in live-host mode.

---

## 2. Parallelism Rules

**Hard rule:** If there is any doubt, serialize.

| Safe to parallelize | Must serialize |
|---|---|
| Disjoint directory subtrees | Both agents edit the same file |
| One on docs, one on CI/scripts | Both agents change the same schema |
| One on specs, one on isolated Go package | One agent depends on the other's output |
| | Shared state files are being mutated |

---

## 3. Long-Task Prompt Minimum Template

**Hard rule:** Every long-task prompt must include all mandatory fields below.
Missing fields caused real failures during the A–E1 pipeline.

```text
You are working in the <REPO> repository.

Task boundary:
- Tranche: <phase + tranche id>
- Goal: <one precise goal>
- In scope: <explicit list>
- Out of scope: <explicit list>

Accepted context you must preserve:
- <list of prior accepted tranches and their frozen decisions>

Files you may edit:
- <paths>

Files you must not edit:
- <paths>

Required behavior:
- <non-negotiable constraints>

Acceptance criteria:
1. <criterion>
2. <criterion>

Validation you must run:
- <command>
- <command>

Final response format:
1. summary of what changed
2. validation run and result
3. open risks or unresolved questions
4. updated execution-stage status table
```

### Why each mandatory field matters

| Field | Failure when omitted |
|---|---|
| `Accepted context you must preserve` | Agent reopens frozen decisions (observed: an agent proposed re-designing accepted B1 semantics during Phase D) |
| `Files you must not edit` | Scope creep into frozen surfaces (observed: docs-only task edited `cli.py`) |
| `Validation you must run` | Agent claims "done" but `go build` fails |
| `Final response format` | Inconsistent acceptance review across agents |

### Anti-patterns observed in practice

- **Vague scope**: "improve the CLI" → agent implements unrelated features.
- **Missing accepted-context**: agent reopens frozen semantics boundaries.
- **No file deny-list**: agent edits files outside the declared scope.
- **No validation commands**: agent declares completion without self-verification.

---

## 4. Agent-Specific Rules

### DeepSeeK (or equivalent replacement threads)

**Hard rule:** DeepSeeK threads start with zero conversation history. The
prompt must carry the full accepted-context handoff — every prior accepted
tranche's frozen decisions must be explicitly listed.

Required format:
```
Accepted context you must preserve:
- Phase A is complete and accepted.
- A1 accepted: <one-line summary of frozen decision>
- A2 accepted: <one-line summary of frozen decision>
...
```

Additional requirements for DeepSeeK tasks:
- Never write "based on your findings, fix the bug." The prompt must prove
  the issuer understood current state and made the synthesis decision.
- Real host evaluation tasks must include SSH details, explicit "real host
  blocker" statements, and "do not invent" rules for operator-confirmed values.
- DeepSeeK tasks must be narrowly scoped to a single tranche.

### Codex (or equivalent implementer agents)

**Hard rule:** Codex tasks require fully frozen contracts with zero semantic
ambiguity.

- Specify exact file paths, expected behavior, and validation commands.
- Do not ask Codex to choose between approaches — resolve the choice first.
- Codex output must be reviewed by Claude or the main agent before acceptance
  when the change touches cross-cutting contract surfaces.

### Claude Code (or equivalent spec/review agents)

**Hard rule:** Claude is the first choice for cross-file consistency reasoning,
contract wording, and test-matrix enumeration.

- Claude tasks benefit from explicit "do not widen into" boundaries.
- Claude is also effective at post-implementation review: auditing Codex
  output for contract violations.

---

## 5. Agent Response Format

**Hard rule:** Every agent closeout must use this exact structure:

```
1. summary of what changed
2. validation run and result
3. open risks or unresolved questions
4. updated execution-stage status table
```

The stage-status table is non-negotiable. If the agent cannot produce it,
the tranche is not complete.

**Stage-status table format:**

| Phase | Tranche | Owner | Execution agent | Goal | Status | Evidence | Next gate |
|---|---|---|---|---|---|---|---|

Status values: `not started`, `in progress`, `ready to dispatch`,
`completed and accepted`, `blocked`.

Evidence column must list specific files and validation commands, not
vague descriptions.

---

## 6. Escalation Policy

**Hard rule:** Agents must escalate (not silently work around) these blockers:

| Blocker | Required Action |
|---|---|
| Frozen semantics are ambiguous | Stop, ask main agent for clarification |
| Required file is locked or missing | Stop, report exact path |
| Existing test contradicts task spec | Stop, report the contradiction |
| Host prerequisite is missing | Stop, document the gap as a receipt asset |
| Binary crashes on target host | Stop, report observation; do not claim root cause without discriminating evidence |

### Escalation anti-pattern (observed)

**Over-attribution of root cause:** An agent correctly observed that a
macOS-cross-compiled Windows binary crashes with access violation on a
real Windows host, and that a native Windows build works. It incorrectly
claimed the root cause was a "Go 1.23.5 toolchain bug." The correct
escalation was: "observed incompatibility confirmed; cause not yet
isolated." Do not upgrade observation to root cause without additional
discriminating evidence.

---

## 7. Acceptance Gate

**Hard rule:** Before the main agent accepts any tranche, verify all of:

| Check | Pass condition |
|---|---|
| Scope | Edits stayed inside tranche boundary |
| Tests | Tranche-specific and existing regressions pass |
| Runtime alignment | When live runtime matters, the running service or equivalent runtime surface is aligned closely enough with the intended target to support acceptance |
| Contract | Caller-visible nouns and envelope shape remain coherent |
| Docs | Docs reflect real implementation state |
| Drift | No hidden widening into out-of-scope behavior |
| Naming | No filename/content mismatch in receipt or test assets |
| Attribution | No root-cause claims unsupported by discriminating evidence |

---

## 8. Spec-First Rule

**Hard rule:** Implementation agents must not resolve semantic ambiguity.

- If a surface is still ambiguous, a spec agent drafts the specification first.
- Implementer agents execute only after the owner accepts the spec.
- If an implementer encounters undefined behavior, it must surface it as a
  blocker — not silently choose an interpretation.

---

## 9. Recovery and Handoff

**Hard rule:** When work spans multiple sessions or agents:

1. Every session writes its state to a shared truth file (e.g., `session_state.md`).
2. Handoff between agents includes:
   - The accepted-context list
   - The exact state of all in-progress files
   - The validation commands last run and their results
3. If a replacement thread takes over, the full accepted-context handoff
   (§4) is mandatory — replacement threads start with zero history.
4. If an agent discovers a wrong assumption mid-execution, it writes a
   correction entry and resumes from the corrected state.

---

## 10. Stage-Status Table (Canonical Reference)

Every tranche closeout appends a row to the master stage-status table.
This table is the single source of truth for what is accepted and pending.

**Hard rule:** No tranche is complete until its row is updated.

Example rows (from `remote-win-runtime`):

| Phase | Tranche | Owner | Agent | Goal | Status | Evidence | Next gate |
|---|---|---|---|---|---|---|---|
| Phase A | A1 | Main | Codex | schema enforcement | completed and accepted | `cli.py`, `test_cli.py`, `scripts/validate_artifacts.py` | A2 dispatch |
| Phase B | B1 | Main | Claude | live-host control spec | completed and accepted | `docs/live-host-control-spec.md` | B2 dispatch |
| Phase C | C2 | Main | Claude | parity fixture harness | completed and accepted | `go-runtime/fixtures/`, `internal/parity/`, `cmd/parity-check/` | C3 dispatch |
| Phase D | D2 | Main | DeepSeeK | live proof parity | completed and accepted | `host/probe.go`, `health/health.go`, `doctor/doctor.go`, `repair/repair.go` | subsequent dispatch |
| Phase E | E1 | Main | DeepSeeK | ACE integration path | completed and accepted | `internal/integration/aceflow/` | subsequent dispatch |

---

## 11. Adopter Customization

When adopting this guide for a specific repository:

1. Replace agent names (Claude Code, Codex, DeepSeeK) with your actual
   agent profiles. The capability matrix should reflect your agents'
   strengths.
2. Add repo-specific "Files you must not edit" examples that are always
   in the deny-list for that project.
3. Replace the example stage-status table rows with your actual tranches.
4. Add repo-specific escalation triggers (e.g., protected paths, sensitive
   config surfaces).
5. Link this guide from your project-context adapter under the
   `delegation\|agent\|tranche\|dispatch` trigger.
6. If your repository depends on live services for acceptance, also link `docs/runbooks/runtime_alignment_and_four_lane_delegation.md` from your project-context adapter under runtime-alignment or multi-lane topics.
