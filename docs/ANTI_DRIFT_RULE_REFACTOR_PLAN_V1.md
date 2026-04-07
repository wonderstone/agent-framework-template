# Anti-Drift Rule Refactor Plan V1

This document freezes the executable plan for hardening execution reliability in the template after the anti-drift design round.

It exists to turn the completed discussion in `tmp/discussion/execution_drift_enforcement_v1/discussion_packet.md` into an implementation-ready plan that can guide both mechanism work and the later rule-layer refactor.

---

## Design Status

| Field | Value |
|---|---|
| Status | Draft execution plan v1 |
| Scope | Anti-drift execution control, pipeline integration, and rule-layer refactor sequencing |
| Depends on | `docs/DOC_FIRST_EXECUTION_GUIDELINES.md`, `docs/TRACEABILITY_AND_RECOVERY_V1_DRAFT.md`, `docs/LEFTOVER_UNIT_CONTRACT.md`, `docs/runbooks/resumable-git-audit-pipeline.md`, and `tmp/discussion/execution_drift_enforcement_v1/discussion_packet.md` |
| Already changes | the implementation sequence, file-level scope, validation plan, and rule-refactor boundary for the anti-drift workstream |
| Does not yet change | the canonical wording of `.github/copilot-instructions.md` or adopter runtime behavior until the implementation waves land |

Normative note:

this is a mechanism-first refactor plan.

It does not treat rule text as the first implementation target.

The first implementation target is the missing execution-control mechanism layer. Rule text should then be rebased onto those shipped mechanism surfaces instead of trying to simulate them in prose.

---

## Goal

Reduce execution-time drift between real work and the template's truth surfaces by introducing concrete anti-drift mechanisms, then refactor execution-lifecycle rules so they rely on those mechanisms rather than relying on agent memory or prose-only discipline.

The required outcome is:

1. long-running work has explicit checkpoint and truth-sync contracts
2. execution drift becomes detectable through shipped tooling rather than only post-hoc suspicion
3. detected drift enters a standard repair loop before closeout or next-stage dispatch
4. existing rules are restructured to use the new pipeline plus anti-drift surfaces consistently

---

## Core Design Framing

The template should now treat `pipeline` and `anti-drift` as related but non-identical layers.

| Layer | Primary role |
|---|---|
| `Pipeline` | define staged execution order, handoff artifacts, checkpoint boundaries, and stop rules |
| `Anti-drift` | ensure those stage boundaries are reflected into `session_state.md`, `ROADMAP.md`, receipts, leftovers, and closeout truth before work proceeds |

Design rule:

pipeline defines the execution skeleton.

anti-drift defines the execution-integrity control layer at pipeline boundaries.

The template should not collapse them into one giant mechanism. It should make them interoperate through explicit checkpoints and shared artifacts.

---

## Current Truth And Gap Summary

### Current Truth

The template already ships:

1. `session_state.md` and `ROADMAP.md` as durable truth surfaces
2. execution contracts for long-running tasks
3. resumable git-audit packet, receipt, and handoff workflows
4. leftover-unit and receipt-anchored closeout contracts
5. staged pipeline scaffolds in the SKILL execution layer
6. validator and hook surfaces that can enforce structural claims at boundary events

### Current Gaps

The template does not yet ship:

1. a checkpoint contract that explicitly says when truth surfaces must sync during execution
2. a structured progress receipt or state-update event model
3. a contradiction-focused anti-drift auditor that compares receipts, handoffs, changed files, and truth surfaces
4. a standard drift packet and reconciliation workflow
5. a rule-layer refactor that rewrites execution-lifecycle rules to depend on those surfaces once they exist

---

## File-Level Scope

The anti-drift workstream should stay inside this file set unless the plan is revised first.

### Canonical Docs

1. `docs/TRACEABILITY_AND_RECOVERY_V1_DRAFT.md`
2. `docs/DOC_FIRST_EXECUTION_GUIDELINES.md`
3. `docs/LEFTOVER_UNIT_CONTRACT.md`
4. `docs/INDEX.md`
5. one new anti-drift runbook under `docs/runbooks/`

### Rule Surface

1. `.github/copilot-instructions.md`

### Templates

1. `templates/execution_contract.template.md`
2. `templates/session_state.template.md`
3. `templates/git_audit_task_packet.template.md`
4. one new drift packet template
5. one new execution-progress receipt template

### Tooling And Hooks

1. `scripts/validate_template.py`
2. `.githooks/pre-commit`
3. `.githooks/pre-push`
4. one new `scripts/state_sync_audit.py`
5. one new helper script for progress/state mutation or reconciliation

### Examples And Proof Surfaces

1. `examples/demo_project/`
2. `examples/skills/05_staged_handoff_pipeline.md`
3. tests under `tests/`

### Explicitly Out Of Scope For The First Anti-Drift Wave

1. continuous runtime orchestration or daemon-style monitoring
2. auto-rewriting `session_state.md` or `ROADMAP.md` from diffs alone
3. forcing state edits on every single commit
4. rewriting judgment-principle rules that do not interact with execution closure

---

## Ordered Implementation Phases

### Phase 1 — Freeze The Checkpoint Contract

Add the missing execution-control contract fields to the template surfaces that already govern long-running work.

Required additions:

1. `progress_unit`
2. `checkpoint_rule`
3. `truth_surfaces`
4. `state_sync_schedule`
5. `closeout_boundary` confirmation where missing or under-specified

Target files:

1. `templates/execution_contract.template.md`
2. `templates/git_audit_task_packet.template.md`
3. `templates/session_state.template.md`
4. `docs/DOC_FIRST_EXECUTION_GUIDELINES.md`

Deliverable:

every declared long task has a machine-checkable contract for when progress should be reflected into truth surfaces.

### Phase 2 — Add The Progress Event Layer

Introduce a bounded, receipt-bearing progress event model.

Required surfaces:

1. `templates/execution_progress_receipt.template.md`
2. one helper script for recording progress, blockers, completion, and leftovers
3. one example flow in the demo project or shipped examples

Minimum fields:

1. `task_id`
2. `receipt_seq`
3. `progress_unit`
4. `touched_files`
5. `status`
6. `expected_state_effect`
7. `evidence_links`

Design rule:

the helper may make state updates easier and more consistent.

it must not claim to author the full narrative truth automatically.

Deliverable:

there is now a low-friction, repeatable path from execution events into anti-drift evidence.

### Phase 3 — Add Contradiction-Focused Detection

Ship `scripts/state_sync_audit.py` and wire it into the repository's existing validation and hook surfaces.

The first wave should detect only contradiction classes that can be justified mechanically.

Initial contradiction classes:

1. declared checkpointed work with no matching progress receipt
2. `session_state.md` says no active work while receipt or handoff evidence still shows in-flight execution
3. unresolved blocker without matching leftover or handoff artifact
4. milestone or completion claims in `ROADMAP.md` without matching receipt/state reflection
5. unresolved drift present at closeout or next-stage dispatch boundary

Enforcement rule:

1. explicit contradictions become hard-fail at observable boundaries
2. staleness thresholds that are repository-tunable start advisory-first

Deliverable:

the template can now detect the most damaging execution drift without pretending to understand narrative intent automatically.

### Phase 4 — Add The Repair Loop

Ship a standard reconciliation path for when drift is detected.

Required surfaces:

1. `templates/drift_packet.template.md` or `templates/drift_reconciliation_packet.template.md`
2. `docs/runbooks/state-reconciliation.md`
3. helper command or pipeline subcommand that opens or advances reconciliation

Required packet fields:

1. `detected_by`
2. `staleness_evidence`
3. `surfaces_to_reconcile`
4. `reconciliation_steps`
5. `reconciliation_receipt_id`
6. `status`

Design rule:

the repair workflow should block closeout or next-stage dispatch until the contradiction is either resolved or explicitly converted into a leftover or handoff truth surface.

Deliverable:

drift becomes recoverable through one standard pipeline instead of ad hoc prose correction.

### Phase 5 — Rebase The Rule Layer

Only after Phases 1 through 4 ship should the major execution-lifecycle rules be refactored.

This phase should rewrite rules from “remember to keep state fresh” toward “use the declared checkpoint contract, anti-drift receipts, sync audit, and repair loop.”

Rule clusters to rebase first:

1. execution boundary and long-task autonomous execution
2. progression loop and next-actions logic
3. subtask completion and phase graduation
4. dispatch, handoff, and resumable audit rules
5. closeout and receipt-anchored completion rules
6. leftover and partial-work recovery rules

Rule clusters to review for compatibility only:

1. challenge incorrect statements
2. dangerous operations policy
3. basic read-before-act and pre-action gate rules
4. general judgment-quality rules that do not manage execution closure

Deliverable:

the rule layer is now a consumer of the mechanism layer, not a substitute for it.

---

## Rule Refactor Matrix

This matrix defines how the later rule rewrite should be organized.

| Rule category | Current weakness | New mechanism dependency | Refactor intent |
|---|---|---|---|
| Execution-lifecycle rules | prose-heavy freshness expectations | checkpoint contract + progress receipt + sync audit | rewrite to require declared checkpoint and sync behavior |
| Handoff / dispatch rules | artifact exists, but state reflection is weak | state-sync audit + drift packet | require truth-surface reconciliation before next-stage dispatch |
| Closeout rules | catches false completion better than mid-task drift | receipt anchor + sync audit + drift resolution | block closeout on unresolved drift contradictions |
| Leftover / partial work rules | strong on classification, weak on mid-task mismatch repair | drift packet + reconcile helper | distinguish unfinished work from drifted truth repair |
| Judgment-principle rules | usually not execution-bound | none or compatibility-only | keep unless the new mechanism creates a direct contradiction |

---

## Validation Commands

Use these commands for the anti-drift implementation waves that follow this plan:

```bash
python3 scripts/validate_template.py
python3 -m pytest tests/test_validate_template.py -q
python3 -m pytest tests/ -q
```

Add focused tests for:

1. missing checkpoint contract fields
2. progress receipt generation or parsing
3. explicit contradiction classes in `state_sync_audit.py`
4. drift repair packet happy path and unresolved-drift failure path
5. rule-layer compatibility once the rule rebase begins

If hooks are changed materially, also validate the relevant hook behavior in test coverage rather than relying only on manual shell runs.

---

## User Acceptance Criteria

- [ ] When a maintainer declares a long-running task, the execution contract makes checkpoint and state-sync expectations explicit rather than implied.
- [ ] When work progresses across stages, the template provides a receipt-bearing path that can explain what state surfaces should have changed.
- [ ] When drift occurs, the repository can detect explicit contradictions without pretending to infer the one true narrative automatically.
- [ ] When drift is detected, the repository provides a standard repair workflow before closeout or next-stage dispatch.
- [ ] When execution-lifecycle rules are later refactored, they point to real anti-drift mechanism surfaces instead of relying on prose-only reminders.

End-to-end scenario: a maintainer opens a long-running task, declares progress and checkpoint rules in the execution contract, the task emits one or more progress receipts, the repository detects any contradiction between receipts and truth surfaces at a boundary, and drift must be reconciled through the standard repair path before closeout or handoff can proceed.

Agent cannot verify yet: which exact contradiction classes should be hard-fail by default for all adopters versus advisory-first with local strictness flags, because that still depends on repository granularity and team tolerance for noisy enforcement.

---

## Progress Unit, Checkpoint, And True Closeout Boundary

Because this plan governs a multi-wave mechanism refactor, it must freeze its own execution boundaries now.

### Progress Unit

One anti-drift mechanism wave made real end-to-end.

Examples:

1. checkpoint contract fields plus validator and tests
2. progress receipt template plus helper and example
3. state sync audit plus contradiction tests and hook wiring
4. drift packet plus runbook plus boundary gate
5. rule-cluster rebase onto the new mechanism surfaces

### Progress Checkpoint

A progress update is allowed after one wave is shipped, validated, and reflected into `session_state.md`.

### True Closeout Boundary

This anti-drift workstream is only complete when:

1. the mechanism layer for prevention, detection, and repair is shipped
2. the major execution-lifecycle rules have been rebased onto those shipped mechanism surfaces
3. the repository's docs, hooks, validators, tests, and state surfaces all describe the same anti-drift truth

---

## Non-Goals And Stop Conditions

### Non-Goals

1. do not force `session_state.md` edits on every single commit
2. do not auto-generate the final narrative truth of `session_state.md` or `ROADMAP.md` from diffs alone
3. do not rewrite judgment-principle rules unless they directly conflict with the new mechanism layer
4. do not claim the template has continuous runtime orchestration or daemon-based monitoring

### Stop Conditions

Stop and reopen design discussion before implementation continues if any of these becomes true:

1. the proposed contradiction classes are too noisy to hard-fail honestly even at boundary events
2. the helper scripts start to imply automatic truth authorship rather than bounded reconciliation support
3. the planned rule rebase would require a second, parallel execution-governance system rather than reusing pipeline plus anti-drift surfaces
4. the anti-drift mechanism cannot be adopted by the demo project or a standard-profile adopter without repository-specific hidden assumptions

---

## Source Discussion

Primary design packet:

1. `tmp/discussion/execution_drift_enforcement_v1/discussion_packet.md`