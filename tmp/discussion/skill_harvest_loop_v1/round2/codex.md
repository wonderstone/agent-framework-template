## Verdict
- Choose A.
- A is the smallest honest contract because the framework already treats the six canonical SKILL fields as the load-bearing unit, so attaching authority directly to those fields reuses existing truth and prevents runtime actors from inventing their own classification layer.

## Why The Other Two Lose
- B loses because section zones introduce a second taxonomy beside the canonical field model, which is less portable, less mechanically checkable, and too coarse once one section contains fields with different authority weight.
- C loses because the override table becomes the real authority surface in practice, so the hybrid keeps section-level ambiguity while quietly reintroducing per-field governance anyway.

## Minimal Contract Shape
- Canonical SKILL doc: add one immutable field-classification table keyed by the six canonical fields: `purpose`, `triggers`, `entry_instructions`, `references`, `governance`, `degradation`.
- Canonical SKILL doc: for each field, record only the minimum needed governance metadata: `promotion_tier`, `minimum_evidence`, and `escalation_triggers`.
- Skill template: expose the same fixed table so every skill instance declares the authority class up front rather than inheriting ad hoc reviewer judgment.
- Validator contract: require the table to exist, require every canonical field to have exactly one classification entry, and reject unknown fields or runtime-added classes.
- Promotion receipts: record `affected_fields`, the matched canonical `promotion_tier`, evidence actually supplied, reviewer role or executor, and whether escalation was triggered.

## Validator Strategy
- Mechanically enforceable: field coverage, allowed enum values for `promotion_tier`, required evidence fields per tier, mismatch detection between proposed patch scope and declared field authority, prohibition on receipts that classify fields not present in the canonical table, and rejection of direct transcript-origin mutations into canonical fields.
- Still needs escalation or human ownership: defining the initial tier assignments, changing tier assignments later, deciding whether evidence is semantically sufficient when the validator only sees structure, and resolving contradictions or borderline cases where a proposal is formally valid but substantively overreaching.

## Drift Failure Mode
- The most likely drift is tier laundering by gradual over-permissive assignment of a normative field into a lower `promotion_tier`, after which delegated reviewers can keep making technically valid but substantively expansive edits.
- The tightest mitigation is to treat the field-classification table itself as constitutional and human-owned: no delegated actor may modify it, and any change to that table requires a separate explicit review path outside normal promotion receipts.

## Migration Path
- Keep the current v1 contract intact and add a single governance annex or table that classifies the existing six fields.
- Map the existing field-level receipt and review matrix onto that table rather than replacing it.
- Update the validator to read the new table and compare promotion receipts against it.
- Update promotion receipts to name affected canonical fields explicitly.
- Leave skill content shape unchanged; only add the fixed authority metadata and corresponding receipt checks.

## Narrowest Remaining Question
- What exact `promotion_tier` enum should the canonical table use for the six existing fields?