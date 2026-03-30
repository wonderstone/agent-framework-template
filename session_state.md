# session_state.md

> Cross-session state for agent-framework-template. Keep under ~100 lines.
> When over limit: archive old phase content to docs/archive/.

---

## Current Goal

Upgrade this template so strategy-layer role definitions, example role families, and mechanism-layer recovery workflows are all first-class framework capabilities.

---

## Working Hypothesis

The best next step is not just a generic strategy/mechanism explanation, but a concrete example pack that covers multiple reviewer families so repositories can bootstrap a richer strategy layer instead of stopping at two CLIs.

**Confidence**: High

**Evidence**: Runic shows that Codex-vs-Claude responsibility split is a strategy concern, while packet/receipt/handoff and hard gates are mechanism concerns; broader examples like git closeout, protocol boundary, performance, observability, and migration review make the strategy layer more reusable.

**Contradictions**: None.

---

## Plan

**Approach**: Extend the template so it carries both the resumable mechanism layer and a formal strategy-layer model with concrete reviewer-family examples.

**Steps**:
1. Add a TYPE-A strategy/mechanism layering doc and a reviewer role profile template.
2. Add a TYPE-A example pack covering multiple reviewer families.
3. Surface the new abstraction and examples in README, architecture, adoption, index, and project adapter triggers.
4. Extend validation checks so the new framework layer cannot drift silently.
5. Re-run template validation and focused tests.

**Why this approach**: The template should not force every adopter to rediscover the difference between reviewer meaning and workflow durability on their own.

---

## Active Work

**Current Step**: Strategy/mechanism generalization and example-pack integration are complete; preparing reusable adoption guidance.

**Next Planned Step**: Reuse the generalized template in a real project and instantiate role profiles from the example pack.

---

## Completed This Phase

- Read the template's canonical rule, architecture, adoption, index, state, and validation surfaces to identify the correct upgrade points.
- Confirmed the template had no existing packet / receipt / handoff workflow, so the upgrade must add canonical assets rather than merge with a prior owner.
- Added a canonical runbook, packet templates, generator CLI, and focused tests for resumable git audit work.
- Wired the new workflow through README, framework architecture, adoption guide, project adapter triggers, agent role contracts, and template validation.
- Re-ran focused pytest and `bash scripts/validate-template.sh`; both now pass.
- Added a TYPE-A strategy/mechanism layering doc and a reviewer role profile template so domain-specific reviewer splits can reuse the same mechanism layer.
- Added a TYPE-A role strategy example pack covering runtime correctness, maintainability, git closeout, protocol boundary, state/checkpoint integrity, performance, observability, migration, and docs/spec drift reviewer families.

---

## Blocker / Decision Needed

- (none)

---

## Mid-Session Corrections

- (none)

---

## Acceptance Criteria

- [x] The template ships a canonical resumable git audit runbook, packet templates, and generator CLI.
- [x] The template also ships a strategy-layer doc and role-profile template for formal reviewer / agent role splits.
- [x] The template ships a concrete example pack that goes beyond two CLI identities and covers multiple reviewer families.
- [x] The new workflow and abstraction are surfaced in README, adoption docs, project adapter triggers, and framework architecture.
- [ ] Template validation checks and focused tests pass after the strategy/mechanism example-pack generalization.

---

## Phase Decisions

- Treat resumable git audit as a framework capability, not a project-specific recipe, so adopters inherit both the docs and the mechanism layer.
- Treat reviewer identity and reviewer workflow as separate concerns: role meaning lives in the strategy layer, packet/receipt/handoff and hard-gate durability live in the mechanism layer.

---

## Technical Insights

- Framework upgrades only stick when they are reflected in rules, docs, templates, scripts, and validation together; single-layer additions decay quickly.
- Role specialization is reusable framework material only when it is decoupled from the recovery mechanism that survives tool failure or token exhaustion.
- Concrete role families improve the strategy layer itself, because they expose judgments that would otherwise stay overloaded inside one vague "reviewer" role.
