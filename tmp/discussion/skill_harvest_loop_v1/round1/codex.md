## Verdict
- Revise the overall direction.
- The right target is not full autonomy and not mandatory human approval; it is delegated, evidence-bounded promotion with explicit exception classes and periodic human audit.
- I support a delegated, minimally human-gated harvest loop only if the system treats extraction, proposal, review, and promotion as separate accountable acts with receipts at each boundary. Without that, “delegated review” becomes silent prompt drift with better branding.

## Recommended Workflow
- **Stage 1: Task Closeout Freeze**
  - At task completion, freeze a task-closeout packet containing only approved artifacts: outcome summary, validator results, cited evidence, failure notes, and reusable heuristics. No raw transcript becomes canonical input.
- **Stage 2: Candidate Extraction**
  - A harvester role converts the closeout packet into one or more skill candidates. Each candidate must point to exact evidence slices and declare the target field, claim type, novelty, and confidence tier.
- **Stage 3: Triage And Classing**
  - A triage role classifies each candidate by risk: descriptive, procedural, normative, safety-relevant, or contract-changing. This is the key governance split, because not all skill changes deserve the same path.
- **Stage 4: Patch Proposal**
  - A proposer role generates a bounded patch proposal against the canonical skill contract, plus a promotion receipt explaining why the change is justified and what evidence is still missing.
- **Stage 5: Delegated Review**
  - A reviewer role checks the proposal against the validator, receipt matrix, source sufficiency rules, and anti-drift constraints. Review should be role-based, not person-based: CLI, subagent, or main-thread owner are all valid executors if they implement the same review contract.
- **Stage 6: Promotion Decision**
  - Low-risk classes may be promoted by delegated approval alone. Higher-risk classes require explicit escalation and a direct maintainer decision.
- **Stage 7: Canonical Promotion And Audit Log**
  - Promotion writes the canonical change plus immutable promotion metadata: who reviewed, by what role, from which evidence packet, under what confidence tier, and under which exception policy.
- **Stage 8: Drift Audit**
  - Run periodic audits over promoted changes to detect repeated weak edits, style creep, or expansion of normative language without commensurate evidence.

## Delegation Boundary
- Can be automated:
  - Task closeout freeze, candidate extraction, de-duplication, evidence linking, validator checks, risk pre-classification, patch formatting, and audit sampling.
- Should be delegated to a role rather than a human:
  - Triage, proposal review, and routine promotion for low-risk fields. The framework should define reviewer behavior once and let any conforming executor perform it.
- Must still require a direct human decision:
  - Any change to normative instructions, safety boundaries, delegation rules, escalation policy, validator semantics, or exception handling. Also any promotion where evidence is thin, conflicting, or based on single-task anecdote.

## Risk Controls
- Top risks:
  - Repeated low-grade proposals slowly rewriting intent.
  - Reviewer capture, where the same reasoning pattern extracts and approves its own drift.
  - Evidence laundering, where transcript-derived impressions are repackaged as “receipts.”
  - Risk-class gaming, where substantive changes are mislabeled as low-risk appendices.
- Concrete controls:
  - Require evidence-addressable candidate packets, not free-form summaries.
  - Separate extractor and reviewer roles by contract, ideally by executor class when feasible.
  - Use field-level promotion rules with hard bans on auto-promotion for normative fields.
  - Record promotion lineage and make drift queryable over time.
  - Add mandatory periodic human audit by sample, not by every change.
  - Trigger escalation on repeated edits to the same field, low evidence density, or disagreement between reviewer roles.

## Best Contract Shape
- Add:
  - `candidate_packet`
  - `promotion_receipt`
  - `promotion_decision`
  - `reviewer_role`
  - `review_executor`
  - `confidence_tier`
  - `risk_class`
  - `exception_class`
  - `evidence_set`
  - `lineage_parent`
  - `promotion_scope`
  - `audit_status`
- Most important distinction:
  - Separate “candidate truth” from “canonical truth.” A candidate can be well-supported and still not be canonical until a promotion decision says so.

## Strongest Disagreement With The Current Direction
- The current framing is still too centered on “who reviews” instead of “what authority each stage has.”
- I would change the design center from reviewer identity to promotion authority classes. If that is not explicit, swapping human review for delegated review just hides the same ambiguity behind tooling.

## Narrowest Next Question
- Which exact SKILL field classes are eligible for delegated auto-promotion, and which are permanently escalation-only?