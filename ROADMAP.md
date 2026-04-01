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

## Completed Phases

| Phase | Completed |
|---|---|
| Phase 1 — Productize The Template | 2026-04-01 |
| Phase 2 — Self-Host And Release Closeout | 2026-04-01 |