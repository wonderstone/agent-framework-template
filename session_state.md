# session_state.md

> Cross-session state for agent-framework-template. Keep under ~100 lines.
> When over limit: archive old phase content to docs/archive/.

---

## Current Goal

Remove the execution-budget and platform-constraints workflow from this template repository.

---

## Working Hypothesis

The budget workflow is causing more friction than protection, so the cleanest fix is to remove its files and all repository references in one pass.

**Confidence**: High

**Evidence**: The workflow is spread across rules, docs, template state, validation, scripts, and a skill file; partial deletion would leave the template inconsistent.

**Contradictions**: None.

---

## Plan

**Approach**: Remove the execution-budget artifacts and update the remaining framework docs and checks to match the simplified model.

**Steps**:
1. Delete the execution-budget skill, scripts, and dedicated doc.
2. Remove budget and platform-constraint references from templates, docs, and operating rules.
3. Re-run repository validation and search for stale references.

**Why this approach**: It removes the overhead at the source and keeps the repository internally consistent.

---

## Active Work

**Current Step**: Removing the budget workflow and repairing the template references it touched.

**Next Planned Step**: Validate the simplified template and clean up any stale references.

---

## Completed This Phase

- Identified all execution-budget and platform-constraints integration points across rules, docs, templates, scripts, and validation.
- Removed the execution-budget skill, scripts, dedicated doc, and all template/runtime references.
- Re-ran template validation after the removal and confirmed the simplified repository still passes.

---

## Blocker / Decision Needed

- (none)

---

## Mid-Session Corrections

- (none)

---

## Acceptance Criteria

- [x] Execution-budget files and skill are removed from the repository.
- [x] No template, doc, or rule still references Execution Budget or Platform Constraints.
- [x] `bash scripts/validate-template.sh` passes after the removal.

---

## Phase Decisions

- Keep `session_state.md` in the repository root, but reduce it to durable workflow state only.

---

## Technical Insights

- Skill files in `.github/skills/<name>/SKILL.md` require YAML frontmatter with a `name` field.
- Workflow scaffolding that depends on self-reported agent state tends to spread quickly across docs, rules, and validation, so full removal needs one-pass consistency cleanup.
