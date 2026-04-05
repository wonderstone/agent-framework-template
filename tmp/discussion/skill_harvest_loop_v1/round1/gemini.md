## Verdict
I strongly support the direction of a delegated, minimally human-gated skill-harvest loop, specifically adopting the "Confidence-tiered auto-promotion" model combined with a "Delegated reviewer gate." A fully autonomous promotion cycle for all skill aspects invites structural collapse through compounding hallucinations, while a conservative human gate becomes an immediate administrative bottleneck, guaranteeing the system will quickly atrophy. By delegating review to specialized agent roles and tiering changes by risk, the framework can evolve organically from real usage patterns while preserving the integrity of core operational directives.

## Recommended Workflow
To balance autonomy with safety, I propose the **Continuous Skill Synthesis (CSS) Pipeline**. This workflow isolates candidate generation from canonical promotion through discrete, auditable stages:

1. **Task Exhaustion & Receipt Generation:** The primary executor finishes a task, producing a standard closeout receipt that captures challenges, workarounds, and novel findings.
2. **Candidate Extraction (The Harvester):** A specialized, lightweight extraction agent parses recent task receipts. It ignores routine execution details but flags repeated workarounds or missing context as "Skill Gap Candidates."
3. **Candidate Triage & Tiering:** Candidates are mechanically classified by target field. Appendices, references, and non-binding "gotchas" are designated *Low-Risk*. Changes to preconditions, core instructions, or required tools are *High-Risk*.
4. **Delegated Review & Patch Drafting (The Synthesizer):** 
   - *Low-Risk* items are automatically drafted into a patch by a Synthesizer agent.
   - *High-Risk* items require the Synthesizer to draft a justification against the original skill mandate.
5. **Canonical Promotion Gate (The Reviewer):** A distinct Reviewer agent role evaluates the patch. 
   - *Low-Risk* patches with high confidence are merged automatically.
   - *High-Risk* patches or low-confidence assessments generate an exception packet, escalating to a human maintainer or the main-thread owner.

## Delegation Boundary
- **Fully Automated:** Task receipt generation, Candidate Extraction, and Triaging/Tiering must be fully automated background processes that require zero human interaction.
- **Delegated to Role (Agent):** Patch Drafting and Canonical Promotion for *Low-Risk* fields (e.g., adding a known error to a troubleshooting appendix) should be delegated to a dedicated Reviewer agent. The Reviewer agent operates strictly on the mechanical validation of evidence (historical receipts) against the proposed patch.
- **Human Decision Required:** Any mutation to normative execution boundaries—such as changing required inputs, security constraints, or removing existing core directives—must halt at the Canonical Promotion Gate. These require a human maintainer to explicitly approve the patch, ensuring the framework's fundamental constraints are not silently relaxed by an eager LLM.

## Risk Controls
The primary risk of an autonomous loop is **Silent Normative Drift**, where an agent iteratively dilutes strict constraints (e.g., test coverage requirements) because it encountered tasks where bypassing them was easier. 

Concrete controls:
1. **Immutable Core Directives:** Define specific blocks within the `.md` skill files (like `<critical_instructions>`) that are cryptographically or mechanically locked from autonomous modification.
2. **Evidence Traceability:** Every automated skill patch must include a `promotion_receipt.md` that permanently links the modification to the specific task receipts that justified it.
3. **Drift-Audit Cron:** A periodic script (e.g., `scripts/preference_drift_audit.py`) that strictly diffs the current skill state against a known-good baseline, explicitly flagging removed constraints or altered mandates for human review, even if they bypassed the standard gate.

## Best Contract Shape
The framework should introduce the following artifacts to manage this lifecycle:
- **`skill_gap_candidate.md`:** A raw extraction containing the proposed addition, the target skill, and pointers to the triggering task receipts.
- **`promotion_decision.md`:** A deterministic audit record created by the Reviewer agent, containing:
  - `confidence_tier`: `[Low, Medium, High]`
  - `risk_classification`: `[Normative, Additive, Ephemeral]`
  - `verdict`: `[Auto-Merged, Escalated, Rejected]`
  - `justification`: Brief rationale linking the patch to the evidence.
- **`SkillReviewer` Role Profile:** A dedicated agent instruction set isolated from task execution, focused entirely on validating structural integrity and historical evidence rather than writing code.

## Strongest Disagreement With The Current Direction
The candidate directions frame the problem too heavily around *who* does the reviewing (human vs. CLI vs. subagent). The biggest missing piece is *what* is being reviewed. The framework must treat skills not as flat markdown files, but as structured schemas where sections have inherent, differing volatility. Treating a core security constraint and a "helpful troubleshooting tip" as requiring the same review pipeline is the core flaw. The system must adopt field-level risk classification before defining the review actors.

## Narrowest Next Question
How do we mechanically differentiate and enforce the boundary between "normative instructions" (requiring human escalation) and "additive context" (safe for autonomous merge) within the existing markdown-based SKILL contract?
