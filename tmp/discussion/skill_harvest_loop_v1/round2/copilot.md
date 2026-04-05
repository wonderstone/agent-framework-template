I’m pulling the discussion packet sections you pointed to and grounding the answer in the existing v1 contract rather than reopening the larger workflow.

## Verdict
- **Choose A.**
- A per-field `promotion_tier` table is the smallest honest extension because the contract already treats these six fields as the canonical unit of review, so authority stays human-authored at the same granularity the framework already understands.

## Why The Other Two Lose
- **B:** section zones are too coarse and too shape-dependent; they introduce authority ambiguity whenever a section contains mixed semantics or is rendered differently across templates and vendor adapters.
- **C:** the hybrid solves edge cases by adding a second authority system, which is unnecessary with only six load-bearing fields and creates its own drift risk between zones and overrides.

## Minimal Contract Shape
- **Canonical SKILL doc:** add a fixed `promotion_tier` table keyed by the six existing canonical fields: `purpose`, `triggers`, `entry_instructions`, `references`, `governance`, `degradation`.
- **Canonical SKILL doc:** define `promotion_tier` as human-owned governance metadata; harvesters, triagers, and delegated reviewers may read it but may not propose or apply tier changes through the normal promotion path.
- **Skill template:** render the same six fields unchanged; add only the `promotion_tier` block so every skill instance carries its field authority map explicitly.
- **Validator contract:** require that every promotion candidate declares `affected_fields`, and reject any candidate whose requested action is not allowed by the target field’s `promotion_tier`.
- **Promotion receipts:** record `affected_fields`, resolved `promotion_tier` for each field, evidence references, reviewer role/executor, and whether escalation was required.
- **Do not** add a parallel section taxonomy or mutable-zone map.

## Validator Strategy
- **Mechanically enforceable:** presence and completeness of the six-field `promotion_tier` table; candidate/patch/receipt field targeting; prohibition on edits outside declared fields; prohibition on tier changes via harvest promotion; evidence attachment requirements; rejection of transcript-derived direct canonical edits.
- **Still needs escalation or human ownership:** initial tier assignment, any later changes to tier definitions or thresholds, borderline cases where evidence supports a field update but the proposed wording changes normative meaning, and contradictions between receipts that the validator can detect but not resolve semantically.

## Drift Failure Mode
- **Most likely drift:** delegated reviewers keep making “allowed” updates inside a delegated field until that field slowly accumulates normative behavior the tier did not intend.
- **Tightest mitigation:** require every promotion receipt to bind evidence to explicit `affected_fields`, and make tier changes or repeated semantic broadening of the same field escalate automatically instead of remaining in the delegated lane.

## Migration Path
- Start from the existing field-level receipt/review matrix and convert it directly into a six-row `promotion_tier` table with no restructuring of the SKILL body.
- Update the validator to read that table and compare it against `affected_fields` in candidate packets and promotion receipts.
- Update the skill template once so all new and existing skills carry the same explicit table.
- Leave the current six canonical fields, receipts, and review flow intact; this is a governance annotation layer, not a rewrite of the contract.

## Narrowest Remaining Question
- What is the smallest fixed enum for `promotion_tier` that covers the six canonical fields without introducing a second taxonomy?

