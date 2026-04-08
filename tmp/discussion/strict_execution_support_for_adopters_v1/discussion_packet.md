# Discussion Packet — strict_execution_support_for_adopters_v1

- Generated at: 2026-04-08T01:31:46.917612+00:00
- Owner: main-thread
- Current round goal: Obtain enough judgment to freeze a plan
- Round exit rule: Freeze a plan, narrow to a sharper second round, or stop on missing truth

## Decision Question

How should the template strengthen its execution-layer support so downstream project agents can execute the design honestly and cannot reasonably blame the template for missing tooling support?

## Why This Needs Discussion

- The template already has stronger governance and anti-drift surfaces than before, but downstream adopters may still lack concrete execution-layer support and verification tooling.
- We want the next framework wave to focus on tools and artifacts that make strict adoption executable, not only well-specified.

## Current Truth

- The repository ships anti-drift surfaces, receipt-anchored closeout auditing, state-sync auditing, resumable git-audit artifacts, discussion packets, strict adoption guidance, and SKILL governance/execution-layer design docs.
- The repository does not yet ship an always-on runtime learning loop, periodic self-review scheduler, or agent-managed canonical skill editor with governance-aware boundaries.

## Constraints

- Preserve truthful governance boundaries and do not let runtime automation bypass promotion authority.
- Prefer concrete scripts, validators, wrappers, or packetized workflows over prose-only guidance.
- Focus on what downstream repositories can actually run locally.
- Avoid requiring adopters to become a full Hermes-style always-on runtime unless the gain is clearly worth the cost.

## Candidate Directions

- Add more execution-layer tools around strict adoption verification and downstream toolchain enforcement.
- Add a bounded learning-loop surface: skill manager, periodic harvest/review loop, candidate search, and optional skills catalog.
- Strengthen downstream developer-toolchain wrappers so project agents get executable, local commands instead of relying on design interpretation.
- Add new validators and runbooks that turn current policy-guided expectations into auditable execution support.

## Evaluation Criteria

- Reduces downstream execution ambiguity
- Makes failure states auditable
- Preserves governance boundaries
- Improves strict adoption proof
- Realistic for adopters to run locally

## Suggested Executors

- claude
- codex
- gemini
- copilot

## Instructions For Participating Executors

1. Read the packet before commenting.
2. Do not rewrite the packet body unless the main thread asks for it.
3. Append your feedback at the end of this file.
4. Prefer concrete tradeoffs, risks, and missing evidence over style opinions.
5. If another round is needed, propose the narrowest next question.

## Main-Thread Decision Status

- Current status: open
- Final decision: pending

## Append-Only Discussion Log

<!-- Append feedback and synthesis entries below this line. -->

---

## Feedback — Round 1 — Claude

- Timestamp: 2026-04-08T01:47:00.749141+00:00
- Stance: conditional-support
- Summary: The biggest execution-layer gaps are self-certified strict adoption, non-enforced execution contracts, non-mechanical independent evaluation, and missing aggregated adoption proof surfaces.

### Strengths

- Proposed concrete audits: adoption status report, execution contract audit, independent evaluation gate, adoption health check.
- Strong focus on closing the specific downstream excuses that let adopters blame the template for weak execution support.
- Raw review artifact: tmp/discussion/strict_execution_support_for_adopters_v1/round1/claude.md

### Risks

- Could fragment the execution layer if each gap lands as a separate narrow script without an aggregated entrypoint.
- Needs profile-aware mandatory rules so minimal adopters are not over-constrained.

### Open Questions

- Should execution-contract and independent-evaluation audits hard-fail only for strict adopters, or for all standard/full adopters too?
- Should the aggregated adoption health surface live inside validate_template.py or stay as a dedicated script?

### Recommended Next Step

- Ship an adoption proof stack first: adoption-status audit plus stronger Developer Toolchain hard-fail checks.

---

## Feedback — Round 1 — Codex

- Timestamp: 2026-04-08T01:47:00.785566+00:00
- Stance: supportive-gap-focused
- Summary: The template already ships strong governance artifacts, but downstream repos still lack enough runnable surfaces to discover, execute, verify, and attest real toolchain support honestly.

### Strengths

- Prioritized a concrete proof stack: adoption verifier, toolchain probe, task-control wrapper, review dispatcher, skill runner, readiness/freshness/failure capture.
- Strong emphasis on auditable downstream proof rather than more philosophy.
- Raw review artifact: tmp/discussion/strict_execution_support_for_adopters_v1/round1/codex.md

### Risks

- Adding too many wrappers at once may overfit the framework before adopter evidence exists.
- A task-control wrapper could become an overly rigid orchestrator if it stops being a bounded state machine.

### Open Questions

- Which execution proof surfaces belong in standard profile by default versus only in strict mode?
- Should the first wave prioritize adoption verification over SKILL runtime routing?

### Recommended Next Step

- Build the downstream proof stack first: strict adoption auditor, toolchain probe receipts, and an independent evaluation pipeline.

---

## Feedback — Round 1 — Gemini

- Timestamp: 2026-04-08T01:47:00.823059+00:00
- Stance: supportive-enforcement-first
- Summary: The framework has a strong pipeline-governance baseline, but still leaves too much to agent goodwill because key execution expectations lack mechanical wrappers and stop-gates.

### Strengths

- Proposed concrete enforcement candidates: toolchain verifier, skill execution wrapper, leftover audit, independent evaluation CLI, checkpoint approval gate, discussion-resolution blocker, and strict adoption certifier.
- Especially strong on converting Layer B/C expectations into executable stop conditions.
- Raw review artifact: tmp/discussion/strict_execution_support_for_adopters_v1/round1/gemini.md

### Risks

- A checkpoint approval gate may slow autonomous flow if applied too broadly.
- Discussion blockers and evaluation gates need careful scoping so they do not create deadweight for trivial tasks.

### Open Questions

- Which policy-guided surfaces should be promoted to mandatory hard gates first: toolchain truth, independent evaluation, leftovers, or open-discussion blocking?
- Do we need a single evaluator pipeline or a narrower closeout-only gate first?

### Recommended Next Step

- Start with toolchain verification and execution wrappers that automatically produce receipts without bypassing promotion governance.

---

## Feedback — Round 1 — Copilot CLI

- Timestamp: 2026-04-08T01:47:00.859341+00:00
- Stance: partial-review-available
- Summary: Copilot CLI confirmed the core asymmetry: governance and truth-audits are strong, but execution closure is still thinner than the design contract; however the run produced only partial final output and should be treated as useful but incomplete evidence.

### Strengths

- Partial review still converged on the same core additions: strict adoption auditor, toolchain probe with freshness receipts, developer-toolchain runner, independent evaluation pipeline, local executor registry, execution-session initializer, skill runtime router, and mechanism-claim validator.
- Useful evidence that even a partial fourth review still landed on the same execution-proof theme.
- Raw review artifacts: tmp/discussion/strict_execution_support_for_adopters_v1/round1/copilot.md and tmp/discussion/strict_execution_support_for_adopters_v1/round1/copilot_retry.md

### Risks

- The partial output itself is evidence that local multi-CLI verification needs an explicit executor availability/status model, not an assumption that every configured reviewer will always return a usable packet.
- We should not over-weight the incomplete fourth review compared with the three full reviews.

### Open Questions

- Should the local executor registry and review-loop runner become part of the strict-adoption baseline?
- How should the template represent executor-unavailable versus executor-failed versus executor-returned-incomplete?

### Recommended Next Step

- Treat executor availability and review-packet completeness as first-class auditable outputs in any future review dispatcher.

---

## Main-Thread Synthesis — Round 1

- Timestamp: 2026-04-08T01:47:00.897379+00:00
- Decision: freeze-plan
- Confidence: high
- Next action: Write a concrete execution-proof upgrade plan that sequences the first-wave tools and marks which are strict-only versus standard-profile defaults.

### Summary

- All substantive reviewers converged on the same diagnosis: the template is stronger on governance truth than on runnable execution proof for downstream adopters.
- The shortest path to reducing downstream blame is not more philosophy; it is a first execution-proof wave that gives adopters concrete validators, wrappers, and attestation artifacts.
- The highest-consensus additions are: strict adoption auditor/attestation, Developer Toolchain probe receipts, a machine-facing toolchain runner, an independent evaluation pipeline, and a local executor registry plus review dispatcher.
- A second wave can extend into execution-session initialization, stricter leftover or checkpoint audits, and SKILL runtime routing, but those should follow the proof stack rather than precede it.

### Rationale

- Claude, Codex, Gemini, and the partial Copilot result all centered on the same failure mode: downstream agents can still say the template described honest execution but did not ship enough concrete execution surfaces to prove the repo could actually carry it out.
- The most defensible response is to make strict adoption machine-audited, make Developer Toolchain claims freshness-backed, and make independent review and multi-CLI verification executable rather than narrative.
- This preserves the current governance boundary because all recommended additions focus on receipts, wrappers, validators, and attestation. None of the high-consensus proposals require autonomous canonical mutation or a Hermes-style always-on runtime.

### Follow-Up Questions

- Should strict adoption auditor, toolchain probe, and independent evaluation all land in one wave, or should the first wave stop after adoption proof plus toolchain receipts?
- Which of the proposed execution-proof tools should upgrade validate_template.py versus remain standalone scripts?
