# session_state.md

> Cross-session state for agent-framework-template. Keep under ~100 lines.
> When over limit: archive old phase content to docs/archive/.

---

## Current Goal

Self-host the newest governance additions so Rule 25, runtime-surface protection, and leftover-unit guidance are reflected in bootstrap, validation, and root docs.

---

## Working Hypothesis

The remaining gap is integration, not design: the new docs already exist, but adopters and maintainers need them surfaced in README, project context, bootstrap, and validator checks to prevent silent drift.

**Confidence**: High

**Evidence**: The new governance docs are now wired into the validator, bootstrap standard profile, README, and project adapters, and the focused validation suite passed after those changes.

**Contradictions**: None.

---

## Plan

**Approach**: Close the integration loop first, then leave runtime-surface automation as an explicit leftover until a real live surface exists.

**Steps**:
1. Keep validator coverage enforcing the newest TYPE-A docs and rule-range sync.
2. Keep bootstrap and project-context surfaces exposing the new docs.
3. Keep runtime-surface protection documented as reference-only in this repository.
4. Revisit concrete guard scripts only when an adopting repository has a stable live surface.

**Why this approach**: It turns the governance additions into shipped, test-backed behavior without pretending this framework repo has a live runtime path of its own.

---

## Active Work

**Current Step**: Recording the rollover and the remaining explicit leftover.

**Next Planned Step**: Monitor whether a future release should ship generic closeout/runtime guard scripts or keep them as reference patterns.

---

## Recent Receipts

- Structured validation passed via `python3 scripts/validate_template.py`.
- All tests passed via `python3 -m pytest tests/ -q`.
- `15 passed in 0.23s`, and the standard-profile bootstrap dry run succeeded via `python3 scripts/bootstrap_adoption.py /tmp/agent-framework-template-smoke --project-name "Smoke" --profile standard --project-type cli-tool --dry-run`.

---

## Phase Notes

- Wired `docs/RUNTIME_SURFACE_PROTECTION.md` and `docs/LEFTOVER_UNIT_CONTRACT.md` into the structured validator, README, root adapter, template adapter, and bootstrap standard profile.
- Added regression checks for README rule-range drift and receipt-closeout rule-number drift.
- Clarified that runtime-surface protection is a reference governance pattern in this repository, not a shipped live probe tool.

---

## Leftover Units

### runtime_surface_guardrails_template_repo

- **why_stopped**: this repository has no active default user runtime path, so a generic live guard script would be synthetic rather than truthful.
- **current_truth**: the governance pattern is documented and surfaced; validator/bootstrap now ship the docs, but no repo-local live guard script or hook installer exists.
- **missing_gate**: a real protected runtime surface plus a repeatable live validator contract.
- **next_reentry_action**: first decide whether a future template release should ship a generic skeleton guard script or keep pointing adopters to reference implementations.
- **promotion_blocker**: cannot promote to shipped runtime enforcement until there is a concrete, non-synthetic live surface definition.

---

## Blocker / Decision Needed

- (none)

---

## Mid-Session Corrections

- Corrected the earlier assumption that the rule set stopped at Rule 24; the current top-level rules run through Rule 25 and root docs must follow that numbering.

---

## User Acceptance Criteria

- [x] When a maintainer runs `python3 scripts/validate_template.py`, the newest governance docs are treated as required template surfaces.
- [x] When a maintainer runs the focused bootstrap and validator tests, the standard profile covers the new docs and README/rule-number drift is caught.
- [x] When a reader opens README or the root project context, Rule 25 and the two new governance docs are visible without searching the repo.

End-to-end scenario: a maintainer edits governance docs, runs the validator and focused tests, and sees drift detected before release.

Agent cannot verify: downstream third-party AI tools honoring every rule consistently.

---

## Phase Decisions

- Treat runtime-surface protection as a shipped governance pattern but not a repo-local executable subsystem until a real runtime surface exists.
- Treat leftover units as first-class state, not implicit TODO debt.

---

## Technical Insights

- New governance docs only become real product surface when validator, bootstrap, README, and project adapter all point at the same truth.
- Rule-number drift is cheap to introduce and worth checking automatically.
