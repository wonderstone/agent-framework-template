I’m reading the packet first, then I’ll give you a tight contract-level review focused on the remaining governance choices.

## Verdict
- **Support** the hybrid direction, but only if the framework-native SKILL contract is kept narrow, validator-enforced, and review-gated so adapters cannot become a backdoor for silent behavior drift.

## Canonical V1 Contract
- Minimum required sections:
  1. **id** — stable identifier, never inferred from filename alone.
  2. **kind** — one of `knowledge`, `workflow`, `verification`, `guardrail`.
  3. **purpose** — one short statement of the behavior change this skill is meant to produce.
  4. **triggers** — explicit “use when / do not use when” conditions in observable terms.
  5. **entry_instructions** — the minimal instructions needed at invocation time.
  6. **dependencies** — referenced support artifacts by role: examples, scripts, docs, checks.
  7. **capabilities_required** — what runtime features are assumed: hooks, subagents, script execution, structured outputs, etc.
  8. **degradation_policy** — what to do when those capabilities are absent.
  9. **evidence_basis** — the approved sources that justify the current content.
  10. **update_policy** — who may propose updates, who must review, and whether the skill is auto-suggest-only or human-approved.
  11. **validator_expectations** — what can be mechanically checked for this skill.
- Do **not** put metrics, packaging, marketplace metadata, or vendor prompt syntax into the canonical core. Those belong in adapters or receipts.

## Evidence And Update Gates
- Evidence ranking, strongest to weakest:
  1. **Failed validations / reproducible breakages**
  2. **Human review findings tied to receipts**
  3. **Postmortems or closeout notes with concrete failure patterns**
  4. **Invocation receipts showing repeated success/failure patterns**
  5. **User-authored gotchas with examples**
  6. **Raw logs / traces**
  7. **Model-synthesized summaries of logs**
- Auto-collect is acceptable for: invocation counts, validation failures, tool errors, missing-capability events, and linked receipts.
- Human review should be mandatory for: any change to `purpose`, `triggers`, `entry_instructions`, `guardrail` content, or `degradation_policy`.
- Human review can be lighter for: adding examples, adding non-normative references, or tightening validator metadata.
- Forbidden because it creates silent prompt drift:
  1. Directly mutating skill instructions from conversation transcripts or raw model outputs
  2. Auto-promoting “successful one-off workaround” into normative instructions
  3. Updating guardrail skills from usage frequency rather than failure evidence
  4. Letting adapter-layer files diverge semantically from the canonical skill without explicit review

## Trigger And Validation Contract
- Minimum triggerability contract:
  1. A skill must declare **positive triggers** (“use when X”)
  2. It must declare **negative triggers** (“do not use when Y”)
  3. It must name the **expected effect** (“this changes planning / execution / verification in Z way”)
- Validators should check:
  1. Required fields exist and are non-empty
  2. Triggers are specific enough to be falsifiable, not vague slogans
  3. Every dependency path resolves
  4. Claimed capabilities match actual adapter/runtime requirements
  5. Degradation policy exists for every non-portable capability
  6. Evidence and update policy are present and internally consistent
- Validators should **not** pretend to prove usefulness, readability, or trigger quality from static checks alone. Those should stay advisory, backed by receipts and review.
- Progressive disclosure stays truthful if the top-level skill contains the full normative contract and linked artifacts contain only supporting detail, examples, or procedures. A hidden file must never contain obligations not named in the entry surface.

## Portability And Honest Degradation
- Core and portable:
  1. Identity
  2. Kind
  3. Purpose
  4. Trigger semantics
  5. Entry instructions
  6. Dependency references
  7. Evidence/update governance
- Optional adapter features:
  1. Vendor-specific skill manifests
  2. Hooks
  3. Subagent dispatch
  4. Tool gating
  5. Installable packaging / lockfiles
  6. Context-fork execution
- Degradation must be explicit: “cannot enforce hook, fall back to advisory reminder”; “cannot fork context, inline condensed procedure”; “cannot gate tools, require manual review step.” Never claim equivalent behavior when it is only approximate.

## Biggest Risk
- The highest-risk failure mode is **governance-shaped prompt drift**: a skill layer that looks validated and portable, but is actually accumulating unreviewed behavioral instructions through logs, adapters, and hidden support files.

## Narrowest Next Question
- **What exact receipt schema is sufficient to justify a skill update without allowing narrative-only evidence to modify normative instructions?**

