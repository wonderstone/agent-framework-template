# session_state.md

> Cross-session state for agent-framework-template. Keep under ~100 lines.
> When over limit: archive old phase content to docs/archive/.

---

## Current Goal

Repository idle after closing the adopter-guidance and bootstrap-output hardening wave.

---

## Working Hypothesis

The highest-value follow-up after the drift audit was to make adoption guidance and bootstrap output say the same honest thing: a repository only improves with repeated use if it keeps the SKILL and harvest-governance surfaces and initializes them deliberately.

**Confidence**: High

**Evidence**:
- Four-CLI audit feedback converged on the same small set of issues: stale root state, execution-contract proof gaps, and unclear hard-versus-soft enforcement wording.
- Bootstrap, validator, tests, and prior multi-runtime or SKILL surfaces are already present and passing.
- The strongest concrete contradiction is local: the root repo was not keeping `session_state.md` aligned with completed work.

**Contradictions**: None.

---

## Plan

**Approach**: Close the guidance gap from both sides: update the README and adoption guide, then make the bootstrap next-step output repeat the same accumulation boundary for adopters at generation time.

**Steps**:
1. Upgrade the README copy-paste adoption prompt to mention SKILL and harvest surfaces explicitly.
2. Add concrete adopter guidance for safe experience accumulation in the adoption guide.
3. Update bootstrap next-step output so generated repositories surface the same accumulation guidance at the command line.
4. Run structured validation and close out the patchset.

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
- Adopter-guidance closeout passed with `python3 scripts/validate_template.py`, `python3 -m pytest tests/test_bootstrap_adoption.py -q` (`10 passed`), and the documented bootstrap smoke command showing the new SKILL or harvest next-step guidance.

---

## Completed This Phase

- Archived the previous SKILL or harvest-governance narrative to `docs/archive/Phase_4_Skill_And_Harvest_Governance_2026-04-05.md` so the root state file can return to current truth.
- Added a root-only stale-state audit to the validator and regression tests for contradictory self-hosting state.
- Added a filled execution-contract example to the demo project and wired adopter-facing docs to it.
- Clarified in root docs which surfaces are mechanically enforced versus instruction-bound.
- Completed the four-CLI drift-audit packet and validated the repository with `python3 scripts/validate_template.py` and `python3 -m pytest tests/ -q` (`56 passed`).
- Upgraded the README adoption prompt, the adoption guide, and the bootstrap next-step output so adopters are told exactly how to keep SKILL and harvest-governance surfaces aligned with real experience accumulation.

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
- [x] Adopter-facing docs explain how a repository should actually use SKILL and harvest-governance surfaces to accumulate experience.
- [x] Adopter-facing docs explain how a repository should actually use SKILL and harvest-governance surfaces to accumulate experience.
- [x] The README copy-paste adoption prompt matches the current SKILL and harvest-governance contract.
- [x] Validation for touched surfaces passes after this documentation update.

End-to-end scenario: a maintainer bootstraps a repository, reads the README or adoption guide, and sees the same practical boundary for long-term improvement: keep the SKILL and harvest-governance surfaces together, initialize at least one repository-specific skill, and promote changes through candidate packets plus promotion receipts rather than raw transcript mutation.

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
