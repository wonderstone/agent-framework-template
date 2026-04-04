## Verdict

Support the hybrid direction without revision — the three-CLI convergence is unusually clean, and the remaining disagreements are about implementation gates, not architecture shape.

## Canonical V1 Contract

Minimum viable fields, nothing aspirational:

- `id` — stable, unique, slug-format identifier
- `type` — one of `knowledge | workflow | verification | guardrail`
- `purpose` — one sentence, written for the invoking agent, not documentation readers
- `triggers` — at minimum one positive condition and one explicit negative exclusion
- `entry_instructions` — the normative behavior body; the field that validators and reviewers treat as the source of truth
- `references` — named pointers to supporting files, never inlined content
- `governance` — evidence policy and reviewer threshold, not boilerplate
- `degradation` — what the skill declares it cannot do when hooks, tool gating, or forked execution are absent

Every field after `id` and `type` is load-bearing. Drop nothing. Add nothing in V1.

## Evidence And Update Gates

**Ranked highest to lowest trust:**
1. Human-authored postmortems and root-cause notes from reproducible failures
2. Closeout audits attached to completed receipts
3. Operator-authored gotchas with explicit provenance
4. Invocation receipts (structured, schema-bound, not free-form)
5. Agent-proposed observations or auto-collected telemetry

**Auto-collection may proceed without review:** gotcha candidates, reference-file additions, invocation frequency signals.

**Human review is required before any change to:** `purpose`, `triggers`, `entry_instructions`, `governance`, `degradation`. This list is non-negotiable regardless of skill type.

**Forbidden as direct update evidence:** raw transcripts, model-generated summaries of transcripts, frequency-based heuristics without failure evidence. These create exactly the silent prompt drift that multiple CLIs identified as the primary risk. They may inform a human reviewer but must never trigger an automated rewrite.

**Guardrail skills require stricter policy:** no auto-proposed updates to normative fields at all; all changes require an explicit reviewer sign-off in the receipt.

## Trigger And Validation Contract

**Minimum triggerability contract:** one positive trigger (when to invoke), one negative trigger (when not to invoke even if conditions partially match), and a declared expected effect. Without the negative trigger, validators cannot detect collision risk, and agents will over-invoke.

**Validators must enforce (hard failures):**
- Required fields present and non-empty
- Trigger specificity: no trigger that is just a noun or a broad category without an activation condition
- Reference integrity: every named reference resolves to an existing file
- Degradation coverage: if `entry_instructions` mention hooks, scripts, or tool gating, a degradation entry must exist
- No progressive disclosure collapse: `entry_instructions` must not inline the full content of any referenced file

**Advisory only (warnings, not blocking):**
- Prose quality and tone
- Whether the purpose is user-friendly
- Gotcha count or coverage breadth

Progressive disclosure is only truthful when the omitted detail is named. A reference that says "see setup.md" is honest. An instruction that silently relies on setup.md without naming it is not.

## Portability And Honest Degradation

**Core and portable:** `id`, `type`, `purpose`, `triggers`, `entry_instructions`, `references`, `governance`. These carry zero runtime assumptions.

**Adapter-layer only (explicit degradation required):** hooks, tool gating, subagent forking, context isolation, package install/update behavior. Each of these must be declared in `degradation`, not assumed present. An agent that cannot execute hooks must know what the skill falls back to — or must refuse to invoke the skill entirely. Implied parity across runtimes is the failure mode.

## Biggest Risk

**Governance theater:** the review gate exists in the schema but becomes a rubber stamp. Evidence accumulates, a human approves a batch of low-scrutiny updates, and trigger conditions and entry instructions drift in small increments that no single reviewer flags as significant. The damage is invisible until invocation quality collapses and there is no receipt trail to explain why. Strict field-level review attribution — who approved what change from what evidence — is the only defense.

## Narrowest Next Question

Define the receipt and review matrix: for each canonical field, which evidence tier may propose an update, what reviewer threshold is required, and what additional constraints apply when the skill type is `guardrail`?
