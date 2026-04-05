## Verdict
- **Revise** the overall direction: support a delegated, minimally human-gated harvest loop, but reject any framing that treats “automation” and “promotion” as the same step.
- The right model is **autonomous evidence production + delegated judgment + explicit escalation**, not full autonomous canonical mutation.
- Direct human inspection should become **exception-based**, but the framework still needs one clearly named authority that can overrule, freeze, or ratify boundary changes when the proposal touches normative skill behavior.

## Recommended Workflow
- **Stage 1 — Task Closeout Receipt:** every finished task emits a closeout receipt with outcome, evidence references, failure modes, operator notes, and confidence.
- **Stage 2 — Harvest Extraction:** a bounded extractor generates **candidate observations** only, never canonical edits. It should pull repeated patterns, gotchas, tool constraints, review failures, and missing contract coverage from receipts and artifacts.
- **Stage 3 — Candidate Normalization:** observations are converted into a **candidate packet** with typed claims, supporting evidence, affected skill fields, estimated blast radius, and proposed review lane.
- **Stage 4 — Mechanical Screening:** validator checks schema, evidence sufficiency, provenance, duplicate detection, contradiction against canonical text, and whether the candidate is even eligible for promotion.
- **Stage 5 — Delegated Triage Review:** a delegated reviewer role decides: reject, merge into backlog, request stronger evidence, or advance to patch proposal. This is governance, not editing.
- **Stage 6 — Patch Proposal:** only approved candidates produce a proposed canonical delta, with a field-by-field rationale linked back to evidence.
- **Stage 7 — Promotion Review:** delegated reviewer or owner evaluates the proposed delta against the canonical contract, drift rules, and exception policy.
- **Stage 8 — Canonical Promotion:** accepted changes are promoted with a **promotion receipt** recording who reviewed, under what authority, and why the evidence crossed the threshold.
- **Stage 9 — Post-Promotion Audit Sampling:** periodic spot audits inspect promoted changes for false generalization and reviewer drift.

## Delegation Boundary
- **Can be automated:** task closeout receipt generation, candidate extraction, normalization, duplicate clustering, evidence linking, contradiction checks, confidence scoring, and patch drafting.
- **Should be delegated to a role rather than a human by default:** triage review and most promotion review. The reviewer should be defined as a **role contract**—for example, “skill-governance reviewer”—that may be executed by a CLI, subagent, or main-thread owner.
- **Must still require a direct human decision:** changes to normative or high-blast-radius fields. Specifically: changes to the canonical SKILL contract itself, promotion thresholds, validator policy, exception taxonomy, review authority definitions, or any proposal that weakens provenance requirements. Those are constitutional changes, not routine skill maintenance.

## Risk Controls
- The top risks are **false generalization from a few tasks**, **self-reinforcing reviewer drift**, **quiet dilution of normative guidance**, and **authority ambiguity** where “review happened” but nobody can say by whom or under what standard.
- Concrete controls:
  1. **Typed evidence classes**: no candidate without linked receipts and cited artifacts.
  2. **Field risk tiers**: informative fields can move faster; normative fields require stricter review.
  3. **Separation of claims from edits**: extractors propose observations, not truth.
  4. **Explicit exception classes**: contradiction, weak evidence, policy touch, cross-skill spillover, and validator ambiguity must escalate.
  5. **Promotion ledger**: every canonical change needs durable provenance, reviewer identity/role, threshold used, and supersession history.
  6. **Audit sampling and rollback path**: autonomy without periodic falsification will drift.

## Best Contract Shape
- Add these artifacts and fields:
  - **Candidate packet**
  - **Promotion receipt**
  - **Promotion decision record**
  - **Delegated reviewer role**
  - **Authority source** (CLI, subagent, owner, human maintainer)
  - **Confidence tier**
  - **Risk tier / blast radius**
  - **Exception class**
  - **Evidence set** with minimum count and diversity
  - **Affected canonical fields**
  - **Contradiction status**
  - **Escalation required**
  - **Supersedes / superseded-by**
- Most important addition: a **two-threshold model**—one threshold for “worthy of review,” another for “worthy of promotion.” That keeps the loop autonomous without making promotion cheap.

## Strongest Disagreement With The Current Direction
- The biggest thing I would change is the implicit framing that the key choice is **human review vs delegated review**. That is too shallow. The real boundary is **constitutional change vs operational refinement**. If you classify proposals by governance impact instead of reviewer identity, the workflow gets cleaner: most operational refinements can be delegated, while constitutional changes stay explicitly owned.

## Narrowest Next Question
- **Which canonical SKILL fields are informational, which are normative, and which are constitutional for promotion-governance purposes?**

