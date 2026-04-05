## Verdict
- Choose A: Per-field `promotion_tier` table attached directly to the canonical SKILL schema.
- Extending the existing field-level receipt and review matrix with a strict per-field tier is the simplest, most mechanically verifiable way to freeze authority without inventing a new taxonomy.

## Why The Other Two Lose
- Option B (Section-level mutable-zone map): It introduces a parallel spatial taxonomy (sections) that misaligns with the already established semantic truth of the six load-bearing field contracts.
- Option C (Hybrid): It unnecessarily bloats the schema with two competing layers of authority resolution, making mechanical validation significantly harder and increasing the risk of edge-case exploits.

## Minimal Contract Shape
- Add a strict `promotion_tier` property (e.g., `human-only`, `delegated-normative`, `auto-append`) explicitly mapping to the six existing load-bearing fields (`purpose`, `triggers`, `entry_instructions`, `references`, `governance`, `degradation`).
- This addition belongs directly in the canonical SKILL doc schema and its corresponding validator contract to ensure the rules are structurally bound to the fields they govern.

## Validator Strategy
- The validator can mechanically block any automated patch proposal that attempts to mutate a field whose `promotion_tier` exceeds the authenticated runtime authority (e.g., instantly rejecting a delegated subagent's edit to a `human-only` field).
- Any proposed changes to `human-only` fields (like `purpose` or `governance`), as well as patches containing contradictory evidence or failing schema checks, must automatically halt the delegated workflow and escalate for direct human ownership.

## Drift Failure Mode
- The most likely failure mode is prompt bloat, where harvesters repeatedly submit low-quality, hyperspecific micro-optimizations to `auto-append` or `delegated-normative` fields (like `references` or `entry_instructions`) until the core intent is diluted.
- The tightest mitigation is enforcing a mechanical distinctness threshold and rate limit in the validator, silently dropping candidates that merely rephrase existing field data or exceed a maximum patch frequency.

## Migration Path
- The current v1 contract can adopt this with zero disruption by updating the validator to parse a new `promotion_tier` mapping, treating any unannotated or legacy SKILL document as implicitly defaulting all six fields to `human-only`.

## Narrowest Remaining Question
- What exact threshold of distinct, accumulated evidence must a candidate packet present to successfully clear the validation gate for a `delegated-normative` field without triggering an escalation?
