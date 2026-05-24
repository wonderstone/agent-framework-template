# ROADMAP

> Phase planning and acceptance criteria for agent-framework-template.

---

## Phase 1 — Productize The Template

**Goal**: Turn the framework from a policy-heavy template into a more adoptable package with tooling, CI, demo assets, and reusable reviewer-role material.

**Status**: ✅ 2026-04-01

| Item | Status |
|---|---|
| Ship audit packet, receipt, and handoff tooling | ✅ 2026-04-01 |
| Add strategy/mechanism and reviewer-role example pack | ✅ 2026-04-01 |
| Add bootstrap, validator, CI, demo repo, and release assets | ✅ 2026-04-01 |

**Acceptance Criteria**:
- [x] The repository ships runnable bootstrap and validation tooling.
- [x] The repository ships a concrete demo adopted repo and starter reviewer profiles.
- [x] CI exercises the validator, tests, and bootstrap smoke paths.

---

## Phase 2 — Self-Host And Release Closeout

**Goal**: Make the repository's own metadata and hygiene match the framework it asks adopters to use.

**Status**: ✅ 2026-04-01

| Item | Status |
|---|---|
| Replace root project adapter placeholders with repo-accurate metadata | ✅ 2026-04-01 |
| Add a root roadmap and align state/release surfaces | ✅ 2026-04-01 |
| Ignore generated Python caches and clean current artifacts | ✅ 2026-04-01 |

**Acceptance Criteria**:
- [x] Root project metadata is self-hosted rather than placeholder-based.
- [x] `CHANGELOG.md` and `VERSION` define a concrete current release boundary.
- [x] Validator and test suite pass after hygiene cleanup.

---

## Phase 3 — Strengthen Developer Toolchain Contract

**Goal**: Turn Developer Toolchain from a reminder-only surface into a manifest-backed, structurally enforced contract with a richer multi-runtime reference path.

**Status**: ✅ 2026-04-03

| Item | Status |
|---|---|
| Add manifest-declared required-core Developer Toolchain contract | ✅ 2026-04-03 |
| Hard-fail malformed or missing Developer Toolchain core for new adopters | ✅ 2026-04-03 |
| Add richer multi-runtime full-stack reference example | ✅ 2026-04-03 |

**Acceptance Criteria**:
- [x] Newly bootstrapped adopters carry a manifest block that declares the Developer Toolchain required-core contract.
- [x] The copied validator hard-fails missing or malformed required-core Developer Toolchain fields for manifest-based adopters.
- [x] Multi-runtime repositories have a shipped reference example that demonstrates qualified surface labels and a full-stack repro path.
- [x] Root validation, full regression tests, and adopted-repo smoke validation all pass after the rollout.

---

## Phase 4 — Formalize SKILL Contract And Harvest Governance

**Goal**: Turn the framework-native SKILL contract and the post-task harvest loop from discussion-only surfaces into shipped design, template, validator, and bootstrap assets.

**Status**: ✅ 2026-04-05

| Item | Status |
|---|---|
| Freeze the framework-native SKILL contract and starter examples | ✅ 2026-04-05 |
| Enforce field-level SKILL governance in the validator | ✅ 2026-04-05 |
| Ship harvest-loop draft plus candidate and promotion artifact templates | ✅ 2026-04-05 |

**Acceptance Criteria**:
- [x] The repository ships a TYPE-A SKILL contract draft plus starter examples.
- [x] The validator enforces canonical SKILL matrix shape, promotion-tier constraints, and reference-path integrity.
- [x] Bootstrap and discovery surfaces expose the harvest-loop draft and artifact templates.
- [x] Root validation, regression tests, and bootstrap smoke all pass after the rollout.

---

## Phase 5 — Ship Anti-Drift Execution Control

**Goal**: Turn anti-drift from a discussion-only concern into shipped checkpoint contracts, progress receipts, sync auditing, reconciliation workflow, and rule-layer dependencies.

**Status**: ✅ 2026-04-08

| Item | Status |
|---|---|
| Freeze checkpoint contract fields across execution surfaces | ✅ 2026-04-08 |
| Add progress receipt and drift reconciliation assets | ✅ 2026-04-08 |
| Wire sync audit into hooks, validator, bootstrap, and examples | ✅ 2026-04-08 |
| Rebase execution-lifecycle rules onto the shipped anti-drift mechanisms | ✅ 2026-04-08 |

**Acceptance Criteria**:
- [x] Long-running task surfaces now declare task ID, checkpoint rule, truth surfaces, and state-sync schedule.
- [x] The repository ships receipt-bearing checkpoint and reconciliation artifacts plus helper scripts.
- [x] Hooks and validator can detect unresolved drift and block closeout honestly.
- [x] Standard-profile bootstrap includes the anti-drift docs, templates, scripts, and demo artifacts.

---

## Phase 6 — Expand Execution-Proof Runtime Surfaces

**Goal**: Turn the execution-proof follow-on surfaces into shipped runtime helpers so adopters can run, review, and audit the next layer mechanically rather than relying on policy text alone.

**Status**: ✅ 2026-04-08

| Item | Status |
|---|---|
| Ship a machine-facing Developer Toolchain runner with durable receipts | ✅ 2026-04-08 |
| Ship a bounded independent-evaluation request/report pipeline | ✅ 2026-04-08 |
| Ship a packetized local executor review loop with registry-driven dispatch | ✅ 2026-04-08 |

**Acceptance Criteria**:
- [x] Standard and full adopters inherit the Wave 2 runner, evaluator, and local-review assets with explicit manifest schema 4 contracts.
- [x] The validator and strict-adoption auditor mechanically reject missing or malformed Wave 2 surfaces.

---

## Phase 7 — Ship Frontend Diagnostics Asset

**Goal**: Turn the Playwright-first frontend diagnostics workflow into a shipped template asset so frontend-capable adopters inherit one browser-smoke seam with bootstrap and validator backing.

**Status**: ✅ 2026-05-11

| Item | Status |
|---|---|
| Add reusable frontend diagnostics runbook and skill | ✅ 2026-05-06 |
| Copy the new assets through standard/full bootstrap | 🔄 in progress |
| Mechanically require the assets through validator and focused tests | 🔄 in progress |

**Acceptance Criteria**:
- [ ] Standard and full adopters inherit `docs/runbooks/frontend_playwright_diagnostics.md` and `.github/skills/frontend-playwright-diagnostics/SKILL.md` through bootstrap.
- [ ] The root validator reports the new runbook and skill as required framework assets.
- [ ] `README.md`, `docs/INDEX.md`, and `.github/instructions/project-context.instructions.md` all expose the new frontend diagnostics surface clearly enough for adopters to discover it.
- [ ] Focused bootstrap and validator regression tests fail if the new asset family is missing.
- [x] Focused regressions, full repository tests, and bootstrap smoke all pass after the rollout.

---

## Phase 8 — Extract Runtime Alignment And Four-Lane Delegation Assets

**Goal**: Turn the observed `repo target vs running services` acceptance pattern and honest four-lane delegated-execution reporting into generic template assets rather than repo-local folklore.

**Status**: 🔄 active

| Item | Status |
|---|---|
| Add a generic runbook for runtime alignment plus four-lane delegation | ✅ 2026-05-11 |
| Add a reusable four-lane runtime-alignment status template | ✅ 2026-05-11 |
| Wire the new assets through docs index, delegation guidance, and project-context topic routing | ✅ 2026-05-11 |
| Copy the new assets through standard/full bootstrap | ✅ 2026-05-11 |
| Mechanically require the new assets through validator and focused tests | ✅ 2026-05-11 |
| Expose the new asset family in adopter-facing setup guidance | 🔄 in progress |

**Acceptance Criteria**:
- [x] The template ships one canonical runbook for coupling runtime alignment with four-lane delegation.
- [x] The template ships one reusable four-lane status template that records lane labels, control state, validation, and runtime dependency.
- [x] `docs/INDEX.md`, `docs/AGENT_DELEGATION_GUIDE.md`, and `.github/instructions/project-context.instructions.md` all expose the new asset family clearly enough for adopters to discover it.
- [x] Standard and full adopters inherit `docs/runbooks/runtime_alignment_and_four_lane_delegation.md` and `templates/four_lane_runtime_alignment_status.template.md` through bootstrap.
- [x] The root validator reports the new runbook and template as required framework assets.
- [x] Focused bootstrap and validator regression tests fail if the new asset family is missing.
- [x] The structured validator reports no new failures attributable to the doc-only extraction slice; current root-validator failures remain the pre-existing unrelated skill-hygiene blockers already present in the repository.
- [ ] `docs/ADOPTION_GUIDE.md` exposes when adopters should keep the runtime-alignment runbook and four-lane status template during bootstrap or manual adoption.

---

## Completed Phases

| Phase | Completed |
|---|---|
| Phase 1 — Productize The Template | 2026-04-01 |
| Phase 2 — Self-Host And Release Closeout | 2026-04-01 |
| Phase 3 — Strengthen Developer Toolchain Contract | 2026-04-03 |
| Phase 4 — Formalize SKILL Contract And Harvest Governance | 2026-04-05 |
| Phase 5 — Ship Anti-Drift Execution Control | 2026-04-08 |
| Phase 6 — Expand Execution-Proof Runtime Surfaces | 2026-04-08 |