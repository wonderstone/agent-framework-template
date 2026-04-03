## Verdict
- Support the current hybrid direction, but only if the framework-native contract stays small, reviewable, and clearly stricter than any adapter format.

## Canonical V1 Contract
- The canonical SKILL contract should require only seven things:
- `id`: stable, repo-local identifier.
- `type`: one of `knowledge`, `workflow`, `verification`, `guardrail`.
- `purpose`: one short statement of the behavioral lift the skill is supposed to provide.
- `triggers`: explicit conditions for invocation, phrased as observable request/context predicates rather than vague intent.
- `entry_instructions`: the minimal instructions safe to load by default.
- `references`: optional linked supporting artifacts for progressive disclosure, each labeled by role such as `setup`, `examples`, `scripts`, `gotchas`, `validation`.
- `governance`: owner, version, last-reviewed-at, and update-policy class.

That is enough to make skills addressable, triggerable, progressively disclosed, and governable. Do not put execution hooks, installer metadata, or vendor activation syntax into the core contract. Those are adapters.

## Evidence And Update Gates
- Evidence ranking should be:
- `1.` Human-reviewed validator failures tied to a concrete task outcome.
- `2.` Human-reviewed postmortems, bug reports, or closeout findings with a clear causal link to missing or wrong skill guidance.
- `3.` Repeated execution receipts showing consistent failure or costly confusion under the same trigger condition.
- `4.` Curated gotchas extracted from logs or transcripts.
- `5.` External guidance or vendor docs suggesting better patterns.

- Auto-collectable:
- Invocation receipts.
- Validator outcomes.
- Repeated failure patterns.
- Candidate gotchas extracted from transcripts or logs.

- Requires explicit human review before changing the canonical skill:
- Any modification to `purpose`, `triggers`, `entry_instructions`, or guardrail behavior.
- Any new supporting reference that changes operational behavior.
- Any update derived from external docs or model-specific recommendations.
- All guardrail-skill updates, full stop.

- Forbidden:
- Direct transcript-to-skill rewriting.
- Automatic prompt expansion based on successful runs.
- Silent edits to trigger text or entry instructions from embeddings, clustering, or model summarization alone.
- Adapter-originated changes flowing back into the canonical skill without human review.

The rule should be simple: evidence may propose; humans approve; adapters consume. Anything else creates prompt drift.

## Trigger And Validation Contract
- Minimum triggerability contract:
- A skill must declare at least one positive trigger and at least one non-trigger boundary.
- Triggers must be testable against observable context: user request shape, repo state, task phase, or failure condition.
- The skill must state whether invocation is `suggested`, `preferred`, or `mandatory`.

- Validators should check:
- Contract completeness.
- Trigger specificity: not purely tautological text like “use when helpful.”
- Separation between default entry instructions and deeper references.
- Reference integrity: linked artifacts exist and are labeled truthfully.
- Governance freshness: owner and review metadata present.
- Degradation declaration for any non-portable feature.

- Advisory only:
- Writing quality.
- Taxonomy elegance.
- Whether the skill is “good” in a broad subjective sense.
- Optimization claims not backed by receipts.

Progressive disclosure stays truthful if the top-level skill says exactly what is omitted and why. A reference is not “optional context” if the skill only works when it is loaded. In that case it is part of the required entry surface.

## Portability And Honest Degradation
- Core and portable:
- Identity, type, purpose, triggers, entry instructions, references, governance, review receipts, and validator outcomes.

- Optional adapters:
- Vendor-specific `SKILL.md` shapes.
- Packaging/install metadata.
- Hooks.
- Tool gating.
- Context-fork or subagent execution.
- Auto-install/update channels.

- Degradation behavior must be explicit:
- If hooks are unsupported, fall back to manual invocation guidance.
- If tool gating is unsupported, convert hard enforcement into a warning.
- If forked execution is unsupported, mark the workflow as single-thread degraded.
- If packaging is unsupported, allow repo-local resolution only.

## Biggest Risk
- The highest-risk failure mode is governance theater: a system that looks structured but allows unreviewed evidence to mutate trigger text and entry instructions, slowly turning skills into untraceable prompt residue.

## Narrowest Next Question
- What exact review policy matrix should apply by skill type and field, especially which fields in a `guardrail` skill are never eligible for auto-proposed updates?