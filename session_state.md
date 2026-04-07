# session_state.md

> Cross-session state for agent-framework-template. Keep under ~100 lines.
> When over limit: archive old phase content to docs/archive/.

---

## Current Goal

No active implementation. The first lower-layer proof-surface tranche is complete and validated, and the five-pattern execution wave has now shipped all planned scaffold families except deferred Inversion.

---

## Working Hypothesis

Execution-scaffold-first absorption was the right path: Wrapper, Reviewer, Pipeline, and bounded Generator can be shipped honestly when each family is tied to concrete artifacts, validator-visible contracts, and adopted-repo proof, while Inversion remains deferred until a truthful host-runtime contract exists.

**Confidence**: High

**Evidence**:
- Standard bootstrap now ships the example and proof assets that the current README and adoption flow depend on.
- Validator coverage now enforces standard-profile bootstrap truth, example-level five-pattern structure, runtime-claim/degradation consistency, and structural progressive-disclosure limits.
- A narrow four-CLI round on hard-fail checks 2, 4, and 5 converged on `partial-implement`, and the implementation plus tests are green.
- The broader five-pattern execution-adoption round converged on `freeze-plan`, and the result is now externalized in `docs/SKILL_FIVE_PATTERN_EXECUTION_PLAN_V1.md` plus the archived discussion summary.
- Wrapper now has stronger structural enforcement beyond label presence: the wrapper template and example must bind to the project-context adapter and name at least one declared Developer Toolchain surface.
- Reviewer, Pipeline, and Generator now also have family-specific contract enforcement covering verdict sinks, handoff artifacts, stage checkpoints, script-plus-schema anchors, and bounded generation proof.

**Contradictions**:
- The prior state file overstated the wave as fully validated and effectively closed; the hostile acceptance round found concrete remaining desync.

---

## Plan

**Approach**: The planned execution wave is complete. Keep the canonical contract stable, preserve the shipped scaffold families, and continue treating future wording shrink or extra hard-fail promotion as evidence-driven follow-up work rather than default cleanup.

**Steps**:
1. Preserve the shipped Wrapper, Reviewer, Pipeline, and bounded Generator scaffold contracts as the current truthful execution-layer baseline.
2. Keep Inversion deferred unless a later round adds a truthful host-runtime contract and degradation story.
3. Revisit only the remaining semantic tails and adopter-specific layering questions when fresh evidence exists.

**Why this approach**: The execution-adoption round converged that pattern names alone are not useful framework progress; the completed wave proved that execution scaffolds are only worth shipping when bootstrap, validator, docs, and examples all agree.

---

## Active Work

**Current Step**: No active work.

**Next Planned Step**: None until the next scaffold-proof or wording-sync task is opened.

---

## Recent Receipts

- Strengthened Reviewer, Pipeline, and Generator scaffold validation so those families now require receipt or verdict sinks, explicit handoff artifacts and checkpoint rules, and script-plus-schema generator boundaries instead of decorative labels.
- Revalidated the completed family wave with `55 passed in 11.38s` across `tests/test_validate_template.py` and `tests/test_bootstrap_adoption.py`, then `81 passed in 15.06s` across the full test suite, plus `✅ All structured checks passed.`
- Strengthened Wrapper scaffold validation so `templates/skill_tool_wrapper.template.md` and `examples/skills/03_developer_toolchain_wrapper.md` must bind to `.github/instructions/project-context.instructions.md`, reference `docs/DEVELOPER_TOOLCHAIN_DESIGN.md`, and name at least one declared Developer Toolchain surface.
- Revalidated the Wrapper family with `49 passed in 9.60s` across `tests/test_validate_template.py` and `tests/test_bootstrap_adoption.py`, then `75 passed in 13.18s` across the full test suite.
- Closed `tmp/discussion/skill_five_patterns_execution_adoption_v1/discussion_packet.md` with `freeze-plan` and recorded the durable outputs in `docs/SKILL_FIVE_PATTERN_EXECUTION_PLAN_V1.md` plus `docs/archive/SKILL_Five_Pattern_Discussion_2026-04-07.md`.
- Expanded the standard bootstrap profile to ship `examples/skills/`, `examples/demo_project/`, `examples/full_stack_project/`, `examples/reviewer_roles/`, `docs/CLOSEOUT_SUMMARY_TEMPLATE.md`, and `scripts/closeout_truth_audit.py` so current docs and examples point at real shipped assets.
- Added validator checks for standard-profile bootstrap truth and extended five-pattern structural validation from starter templates to shipped examples.
- Relaxed the adopted-repo Developer Toolchain contract so `Build` is recommended rather than always required, matching the conditional wording already used in adoption guidance.
- Ran a narrow four-CLI discussion on hard-fail mechanicalization and implemented the converged partial strategy in `scripts/validate_template.py`.
- Added hard-fail checks for runtime-capability claims without degradation and structural progressive-disclosure collapse in `Entry Instructions`.
- Added advisories for weak trigger bullets and overly dense `Entry Instructions`.
- Validation passed with `43 passed in 7.41s` for `tests/test_bootstrap_adoption.py` and `tests/test_validate_template.py`, then `73 passed in 12.84s` across the full test suite, plus `✅ All structured checks passed.` and a clean standard-profile bootstrap smoke dry-run plan.
- Created `tmp/discussion/skill_five_pattern_acceptance_desync_v1/discussion_packet.md` and ran a four-CLI hostile acceptance round focused on upper-layer versus lower-layer desync.
- Collected conditional verdicts from Claude CLI, Codex CLI, Gemini CLI, and GitHub Copilot CLI, then appended the synthesis back into the packet.
- The round closed with `accept-with-fixes`: the wave is structurally coherent, but profile guidance, validator claims, and executable-proof wording still need tightening.
- Added explicit five-pattern absorption boundary text to `docs/SKILL_MECHANISM_V1_DRAFT.md`.
- Added explicit execution-layer mapping text to `docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md` covering Wrapper, Reviewer, Pipeline, bounded Generator, and deferred Inversion.
- Added starter scaffolds under `templates/skill_tool_wrapper.template.md`, `templates/skill_reviewer_gate.template.md`, `templates/skill_pipeline.template.md`, and `templates/skill_artifact_generator.template.md`.
- Added shipped examples under `examples/skills/03_developer_toolchain_wrapper.md`, `examples/skills/04_receipt_anchored_reviewer.md`, `examples/skills/05_staged_handoff_pipeline.md`, and `examples/skills/06_bounded_artifact_generator.md`.
- Wired the new scaffold surfaces into `scripts/bootstrap_adoption.py`, `scripts/validate_template.py`, `tests/test_bootstrap_adoption.py`, and `tests/test_validate_template.py`.
- Focused validation passed with `41 passed in 6.76s` across `tests/test_bootstrap_adoption.py` and `tests/test_validate_template.py` after the five-pattern scaffold wave landed.
- Structured validation passed with `✅ All structured checks passed.` after the final README and scaffold-reference fixes.

---

## Completed This Phase

- Completed the remaining five-pattern execution-wave scaffold families for Reviewer, Pipeline, and bounded Generator, including family-specific contract hardening plus validator and regression coverage.
- Completed the first five-pattern execution-wave scaffold family for Wrapper, including template/example contract hardening plus validator and regression coverage.
- Completed the five-pattern execution-adoption discussion round and froze the staged implementation direction in a TYPE-A execution plan plus a TYPE-C archive summary.
- Completed the first lower-layer proof-surface tranche for the five-pattern scaffold wave, including standard-profile bootstrap truth, validator hardening, and a partial mechanicalization of hard-fail checks 2, 4, and 5.
- Completed a four-CLI hostile acceptance round on the shipped five-pattern scaffold wave and froze the result as `accept-with-fixes` rather than a clean PASS.
- Completed a first-party OpenSpace research pass focused on skill self-evolution, execution triggers, quality monitoring, host integration, and lineage evidence.
- Created `tmp/discussion/skill_self_evolution_execution_gap_v1/discussion_packet.md` and ran a four-CLI round with Claude, Codex, Gemini, and Copilot.
- Froze the consensus direction: preserve the current governance model, add runtime invocation receipts, bounded candidate triggers, and FIX or DERIVED or CAPTURED lineage before broader automation.
- Shipped the execution-layer v1 doc, invocation receipt template, lineage-aware candidate and promotion updates, and the `scripts/skill_evolution_pipeline.py` helper.
- Wired the new execution-layer assets into bootstrap, validator, focused tests, and an adopter round-trip regression.
- Completed the multi-CLI discussion and froze the five-pattern adoption plan in both TYPE-A and TYPE-C docs.
- Completed the five-pattern scaffold wave across docs, templates, examples, bootstrap, validator, and focused tests.

---

## Blocker / Decision Needed

- No blocker for repository operation. The remaining open design question is whether future adopter evidence is strong enough to promote more of the semantic tail of hard-fail checks 2 and 5 into hard-fail rather than advisory, and whether any adopter wants to move parts of Reviewer upward into repository-specific role strategy.

---

## Mid-Session Corrections

- Corrected the earlier assumption that the five-pattern scaffold wave could already be treated as fully closed; hostile acceptance found remaining desync at the docs and proof boundary.
- Corrected an initial exploration claim that the SKILL validator no longer checked reference-path integrity; the current validator does check that.
- Corrected an initial exploration claim that the full-stack example project-context file was only a stub; it is already a filled reference surface.
- Corrected the first reviewer starter draft to avoid referencing a doc that the standard bootstrap profile does not ship.

---

## User Acceptance Criteria

- [x] When a maintainer reads the SKILL docs, the five-pattern adoption boundary is explicit and does not overclaim pattern support.
- [x] When a maintainer bootstraps the standard profile, the absorbed patterns that were approved for shipping are present as real execution scaffolds, not only prose references.
- [x] When the validator runs, it can distinguish shipped scaffold truth from decorative pattern labels.
- [x] When an adopter inspects the shipped examples, they can see how Wrapper, Reviewer, or Pipeline map into concrete repository surfaces.

End-to-end scenario: a framework maintainer bootstraps the template, sees concrete wrapper or reviewer or pipeline starter surfaces in the shipped assets, traces their boundaries through docs plus validator checks, and does not confuse deferred patterns like Inversion with supported runtime power.

Agent cannot verify: whether future adopters will want Reviewer to stay as a starter scaffold or elevate parts of it into repository-specific role strategy, because that still depends on local review architecture.

---

## Phase Decisions

- Treat the current round as an honesty-hardening pass, not a framework redesign pass.
- Prefer small proof-restoring fixes over abstract wording churn.
- Preserve the current git-audit and discussion-loop architecture; the audit found those mechanisms stronger than initially suspected.
- Absorb the five Google patterns asymmetrically: Wrapper, Reviewer, and Pipeline as shipped scaffolds; Generator as bounded artifact generation only; Inversion deferred.
- Treat the current five-pattern wave as conditionally accepted until the hostile acceptance findings are addressed.
- For hard-fail checks 2, 4, and 5, implement only the bounded structural subset now; keep semantic usefulness/density judgment advisory until real adopter evidence justifies more.

---

## Technical Insights

- Self-hosting drift in the root repository damages framework trust faster than missing optional capabilities.
- A strong template surface still needs either executable proof or an explicit note that it remains instruction-bound.
- Multi-CLI critique is most useful when the packet includes concrete current truth and asks auditors to reject stale assumptions explicitly.
- Pattern adoption stays honest when templates, bootstrap output, validator checks, and examples all describe the same limited runtime claim.
- Hostile acceptance is useful after a green validation pass because it catches profile-local guidance drift and proof-language inflation that structural checks miss.
- A narrow 4-CLI round is effective for validator design when the question is reduced to “which structural subset is trustworthy enough to mechanize now?” rather than broad framework direction.
