# session_state.md

> Cross-session state for agent-framework-template. Keep under ~100 lines.
> When over limit: archive old phase content to docs/archive/.

---

## Current Goal

Repository idle after closing the template drift-audit hardening wave.

---

## Working Hypothesis

The framework architecture is mostly sound, and the highest-value remaining hardening is a narrow validator check for obviously contradictory root-state combinations rather than a broader workflow redesign.

**Confidence**: High

**Evidence**:
- Four-CLI audit feedback converged on the same small set of issues: stale root state, execution-contract proof gaps, and unclear hard-versus-soft enforcement wording.
- Bootstrap, validator, tests, and prior multi-runtime or SKILL surfaces are already present and passing.
- The strongest concrete contradiction is local: the root repo was not keeping `session_state.md` aligned with completed work.

**Contradictions**: None.

---

## Plan

**Approach**: Add a root-only stale-state audit to the validator, cover it with regression tests, then validate and close out the patchset.

**Steps**:
1. Add a root-only validator check for obvious stale-state contradictions.
2. Add regression coverage for the contradictory combinations the audit identified.
3. Re-run structured validation and the full test suite.
4. Commit and push the complete drift-audit hardening wave.

**Why this approach**: It fixes the issues the audit actually proved without reopening the larger framework design.

---

## Active Work

**Current Step**: No active work.

**Next Planned Step**: None until the next repository task is opened.

---

## Recent Receipts

- Four-CLI audit round completed for `tmp/discussion/template_framework_drift_audit_v1/` using Claude, Codex, Gemini, and Copilot.
- The shared conclusion is that the framework is mostly sound, but the root `session_state.md` had gone stale and adopter-facing docs were stronger than executable proof in a few places.
- Previous SKILL and harvest-governance rollout already closed in commit `8e700b3` with validator, tests, and bootstrap smoke passing.
- Root self-hosting now includes a validator-backed stale-state audit for obvious contradictory `session_state.md` combinations.
- Post-hardening validation passed: `python3 scripts/validate_template.py` and `python3 -m pytest tests/ -q` with `58 passed`.

---

## Completed This Phase

- Archived the previous SKILL or harvest-governance narrative to `docs/archive/Phase_4_Skill_And_Harvest_Governance_2026-04-05.md` so the root state file can return to current truth.
- Added a root-only stale-state audit to the validator and regression tests for contradictory self-hosting state.
- Added a filled execution-contract example to the demo project and wired adopter-facing docs to it.
- Clarified in root docs which surfaces are mechanically enforced versus instruction-bound.
- Completed the four-CLI drift-audit packet and validated the repository with `python3 scripts/validate_template.py` and `python3 -m pytest tests/ -q` (`56 passed`).

---

## Blocker / Decision Needed

- (none)

---

## Mid-Session Corrections

- Corrected an initial exploration claim that the SKILL validator no longer checked reference-path integrity; the current validator does check that.
- Corrected an initial exploration claim that the full-stack example project-context file was only a stub; it is already a filled reference surface.

---

## User Acceptance Criteria

- [x] Four CLI participants provide critique on whether the current framework contract is honest and operationally sound.
- [x] The shared discussion packet contains the raw round output plus a main-thread synthesis.
- [x] At least one confirmed expectation-versus-reality drift issue is fixed in the repository.
- [x] Adopter-facing docs distinguish mechanical enforcement from instruction-bound conventions where that boundary matters.
- [x] Validation for touched surfaces passes after the stale-state audit is added.

End-to-end scenario: a maintainer can inspect the discussion packet, see four-CLI critique plus synthesis, and inspect the repository surfaces to confirm the framework now describes and demonstrates its current behavior more honestly.

Agent cannot verify: how downstream adopters will operationalize the execution contract unless they add their own local workflow checks.

---

## Phase Decisions

- Treat the current round as an honesty-hardening pass, not a framework redesign pass.
- Prefer small proof-restoring fixes over abstract wording churn.
- Preserve the current git-audit and discussion-loop architecture; the audit found those mechanisms stronger than initially suspected.

---

## Technical Insights

- Self-hosting drift in the root repository damages framework trust faster than missing optional capabilities.
- A strong template surface still needs either executable proof or an explicit note that it remains instruction-bound.
- Multi-CLI critique is most useful when the packet includes concrete current truth and asks auditors to reject stale assumptions explicitly.
