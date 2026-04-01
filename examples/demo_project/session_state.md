# session_state.md

> Cross-session state for Demo Task Tracker.

---

## Current Goal

Demonstrate how the framework looks inside a small adopted repository with resumable audit artifacts.

---

## Working Hypothesis

If the demo stays intentionally small, adopters will understand the customization points faster than they would from generic prose alone.

**Confidence**: High

**Evidence**: The project context, roadmap, code, tests, and packet examples all point at the same feature slice.

**Contradictions**: None.

---

## Plan

**Approach**: Keep the feature small and make the recovery artifacts visible.

**Steps**:
1. Show the customized project adapter.
2. Show a tiny but real code/test surface.
3. Show packet, receipt, and handoff artifacts for one feature.

**Why this approach**: The framework is easier to trust when structure and execution evidence are side by side.

---

## Active Work

**Current Step**: Keep the demo aligned with the productized template.

**Next Planned Step**: Use the demo as the first walkthrough for new adopters.

---

## Completed This Phase

- Added a project-specific adapter and document index.
- Added a minimal CLI implementation and tests.
- Added a committed audit packet, receipt, and handoff set for one feature.

---

## Blocker / Decision Needed

- (none)

---

## Mid-Session Corrections

- (none)

---

## Acceptance Criteria

- [x] The demo reads like an adopted repo, not a toy folder of placeholders.
- [x] The code and the audit docs reference the same feature.

---

## Phase Decisions

- Keep the demo file-based and local to reduce cognitive load.

---

## Technical Insights

- Small concrete examples teach this framework faster than more policy text.
