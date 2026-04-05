# Phase 4 — SKILL And Harvest Governance

Date: 2026-04-05
Scope: archive the completed SKILL contract, harvest-governance, and related bootstrap or validator rollout that previously lingered in `session_state.md`.

---

## Summary

- Froze the framework-native SKILL contract as a TYPE-A design surface and shipped the first reusable template plus starter examples.
- Added field-level receipt and review governance, including `promotion_tier`, to the canonical SKILL surface, starter examples, and validator.
- Added the SKILL harvest loop draft plus reusable candidate-packet and promotion-receipt templates.
- Exposed the new SKILL and harvest surfaces through bootstrap, project-context discovery, adoption docs, compatibility notes, and repository validation.

---

## Receipt Window

- `python3 scripts/validate_template.py` passed after the SKILL and harvest-governance rollout.
- `python3 -m pytest tests/ -q` passed with `56 passed` during the closeout wave.
- `python3 scripts/bootstrap_adoption.py "${TMPDIR:-/tmp}/agent-framework-template-smoke" --project-name "Smoke" --profile standard --project-type cli-tool --dry-run` rendered the SKILL and harvest assets in the shipped standard profile.
- Git closeout completed in commit `8e700b3` (`skills: add harvest loop contract and artifacts`).

---

## Durable Decisions

- Keep the canonical SKILL contract framework-native and treat vendor-specific skill formats as adapter layers.
- Attach promotion authority directly to the six canonical SKILL fields instead of inventing a second governance taxonomy.
- Keep candidate truth and canonical truth separate: post-task harvest may propose, but canonical mutation still requires typed review and receipts.
- Treat `governance` as permanently `human-only` and enforce that in the validator.

---

## Promoted Insights

- The framework becomes trustworthy only when docs, templates, bootstrap, validator, and examples move together.
- Multi-CLI discussion is most useful when the packet freezes concrete current truth and asks for the smallest honest fix rather than broad redesign.
- Self-hosting drift in state and closeout surfaces is more damaging than missing optional features, because adopters inspect the root repo as proof.
