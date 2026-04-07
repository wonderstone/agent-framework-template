# Discussion Packet — skill_self_evolution_execution_gap_v1

- Generated at: 2026-04-07T03:48:03.140710+00:00
- Owner: main-thread
- Current round goal: Decide what the template should absorb from OpenSpace next, especially around execution-layer strengthening for SKILL self-evolution.
- Round exit rule: Freeze a plan, narrow to a sharper second round, or stop on missing truth

## Decision Question

How should the template absorb OpenSpace-style SKILL self-evolution while fixing its weak execution layer without losing governance truthfulness?

## Why This Needs Discussion

OpenSpace provides a concrete self-evolving-skill model, the user strongly agrees with that direction, and recent feedback says this template's SKILL execution layer is too weak and detached from actual task loops.

## Current Truth

The template already has a canonical SKILL contract, a harvest-loop governance model, candidate and promotion artifacts, validators, examples, and adoption guidance. It is stronger on governance than execution. OpenSpace explicitly adds FIX/DERIVED/CAPTURED evolution, metric-driven triggers, host-skill integration, lineage tracking, and a shared skill community. The user wants a four-CLI discussion specifically about absorbing the right OpenSpace ideas and closing the execution gap in this template.

## Constraints

Be critical, not promotional. Do not assume OpenSpace should be copied wholesale. Separate execution-layer gaps from governance-layer strengths. Prefer the smallest honest design move that materially improves execution. Preserve truthful mutation boundaries; do not collapse into transcript-to-skill auto-rewrite. Assume docs, templates, validators, examples, and runtime execution surfaces can all change in a later implementation wave.

## Candidate Directions

Direction A: keep the current governance model and only add stronger examples or docs. Direction B: add an execution layer for SKILL invocation and evolution triggers while preserving the current governance and promotion boundary. Direction C: adopt a more automated OpenSpace-style self-evolution engine with stronger runtime metrics and lineage, but keep explicit human authority for canonical mutation. Direction D: split SKILL into two planes: executable runtime skill assets and canonical governance skill contracts.

## Evaluation Criteria

Does the proposed direction make skills actually improve through use? Does it close the execution-layer weakness reported by users? Does it preserve or improve governance truthfulness? Can it be implemented incrementally in this template without pretending unsupported automation already exists?

## Suggested Executors

Claude CLI; Codex CLI; Gemini CLI; GitHub Copilot CLI; main-thread synthesis

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

## Feedback — Round 1 — Claude CLI

- Timestamp: 2026-04-07T00:00:00+00:00
- Stance: freeze-plan
- Summary: The template should not copy OpenSpace wholesale; it should add a thin execution-side evidence plane so skills can improve through use without breaking the current governance boundary.

### Strengths

- The existing SKILL governance model is already strong and should remain the constitutional layer.
- OpenSpace contributes a useful execution-side taxonomy rather than a replacement governance model.

### Risks

- Skills still lack a real invocation evidence loop.
- Metric-driven autonomous promotion would create a false authority chain before the template has trustworthy runtime telemetry.

### Open Questions

- How small can the first execution artifact be while still proving invocation, outcome, and lineage?

### Recommended Next Step

- Add invocation receipts, lineage anchors, and typed evolution metadata before attempting broader automation.

---

## Feedback — Round 1 — Codex CLI

- Timestamp: 2026-04-07T00:00:00+00:00
- Stance: freeze-plan
- Summary: The next honest step is a non-canonical runtime path linking trigger, invocation, receipt, candidate, and review rather than a full self-evolution engine.

### Strengths

- The framework already separates canonical mutation from candidate evidence.
- The current six-field SKILL contract is the right thing to preserve.

### Risks

- Without structured invocation evidence, skills cannot honestly become smarter through use.
- Triggerability and metric-driven evolution remain theoretical until a host-facing runtime contract exists.

### Open Questions

- Should the first runtime layer be a receipt schema only, or schema plus one stubbed adapter path?

### Recommended Next Step

- Add one host-facing trigger-eval plus invocation logging contract and typed evolution modes on candidate and promotion artifacts.

---

## Feedback — Round 1 — Gemini CLI

- Timestamp: 2026-04-07T00:00:00+00:00
- Stance: continue-discussion
- Summary: OpenSpace's direction is valuable, but the template still needs one narrower design step on runtime receipts and invocation protocol before freezing implementation details.

### Strengths

- OpenSpace-style lineage tracking and metric-driven triggers are directionally strong.
- The current harvest boundary is a valuable protection against contextual pollution.

### Risks

- The current framework has no structural bridge from ad-hoc runtime adaptation to candidate generation.
- Over-automation could let single-session hacks leak into canonical truth.

### Open Questions

- What exact runtime receipt or delta artifact should feed the candidate packet?

### Recommended Next Step

- Narrow the next step to defining the runtime receipt or delta schema and the FIX, DERIVED, or CAPTURED injection path.

---

## Feedback — Round 1 — GitHub Copilot CLI

- Timestamp: 2026-04-07T00:00:00+00:00
- Stance: freeze-plan
- Summary: The template should add a thin execution plane for skill use, outcome classes, candidate generation triggers, and lineage while keeping canonical skills human-bounded.

### Strengths

- Receipt anchoring, field-level authority, and the ban on transcript-to-canonical mutation are already the framework's strongest assets.
- OpenSpace's FIX, DERIVED, CAPTURED split is a high-value import if treated as evidence metadata rather than mutation authority.

### Risks

- Missing execution substrate keeps self-evolution mostly theoretical.
- Metrics without declared runtime evidence would create fake certainty and prompt churn.

### Open Questions

- Which minimal trigger set should the first execution plane support?

### Recommended Next Step

- Start with repeated invocation failure, repeated manual correction, and repeated successful reuse as bounded candidate triggers.

---

## Main-Thread Synthesis — Round 1

- Timestamp: 2026-04-07T00:00:00+00:00
- Decision: freeze-plan
- Confidence: High
- Next action: Freeze the next design wave around a thin SKILL execution plane, typed evolution lineage, and bounded runtime evidence artifacts before broader automation.

### Summary

- All four CLI participants agreed on the same core diagnosis: the template is stronger on SKILL governance than on SKILL execution.
- The highest-value OpenSpace ideas are not "self-rewriting canonical skills" but FIX, DERIVED, CAPTURED lineage, runtime invocation evidence, and a host-facing execution contract.
- The disagreement was only about sequencing: three executors thought the direction is already clear enough to freeze now, while Gemini wanted one narrower schema pass first.

### Rationale

- The packet asked whether the template should absorb OpenSpace's self-evolution direction while fixing its execution weakness, and all four outputs converged on a thin execution-side layer as the missing piece.
- No executor recommended weakening the current promotion boundary; the consensus was to preserve canonical mutation authority and make runtime observations feed candidate packets rather than directly rewrite SKILL truth.
- The strongest common import from OpenSpace was its FIX, DERIVED, CAPTURED split and lineage mindset. The strongest common rejection was autonomous metric-driven canonical mutation without a trustworthy runtime evidence substrate.
- Gemini's request for a narrower schema pass does not materially conflict with freeze-plan because the next implementation wave can start by freezing those schemas first.

### Follow-Up Questions

- The first implementation wave should answer three concrete design questions:
	1. What is the minimal `skill_invocation_receipt` shape?
	2. Which bounded runtime triggers can create candidate packets honestly?
	3. Where should typed evolution lineage live: candidate packets only, or candidate packets plus promotion receipts?

## GitHub Copilot CLI Feedback — 2026-04-07

1. **Verdict: what should the template absorb next?**

Add a thin execution plane for SKILL use, not a self-rewriting skill engine. Concretely: introduce structured skill invocation receipts, outcome classes, metric-triggered candidate creation, and lineage links between `CAPTURED` runtime observations, `DERIVED` candidate packets, and `FIX` canonical promotions. Keep canonical SKILL fields human-governed and receipt-anchored.

2. **Top 3 findings**

### 1. Execution receipts are missing, so the self-evolution loop has no trustworthy runtime substrate.

- **category:** execution gap
- **why it matters:** The template already knows how a skill may change, but it does not yet know when a skill was invoked, whether it helped, what failed, or which evidence should generate a candidate. That makes the current harvest loop governance-rich but execution-thin: it can review mutations honestly, but it cannot reliably discover them through actual use.
- **smallest honest next step:** Add a non-canonical `skill_invocation_receipt` artifact with fields for skill id, trigger matched, task context, outcome class, evidence links, and candidate recommendation. Wire it to candidate packet generation only for bounded fields such as `references` and draft `entry_instructions` suggestions.

### 2. The template has the right constitutional boundaries already; weakening them to copy OpenSpace wholesale would damage trust.

- **category:** governance strength
- **why it matters:** The existing SKILL contract, per-field promotion tiers, receipt-anchor rule, and explicit ban on transcript-to-canonical mutation are the strongest parts of the current design. If OpenSpace-style evolution is copied naively, runtime frequency and agent summaries will start acting like constitutional authority, and the framework will overstate what it actually knows.
- **smallest honest next step:** Preserve the current human-only boundary for `purpose`, `triggers`, and `governance`, and explicitly classify any new FIX/DERIVED/CAPTURED surfaces as evidence planes rather than mutation authority.

### 3. Metric-driven triggers are valuable, but dangerous unless paired with a declared runtime surface and lineage model.

- **category:** over-automation risk
- **why it matters:** OpenSpace is directionally right that repeated failure, repeated manual correction, or repeated successful reuse should trigger learning work. But without a declared runtime observation surface, those metrics become hand-wavy heuristics; without lineage, reviewers cannot tell whether a proposal came from a real failure pattern, a tooling artifact, or prompt drift.
- **smallest honest next step:** Define a minimal trigger set such as repeated invocation failure, repeated operator override, and repeated successful reference usage, but require each trigger to point to invocation receipts plus a lineage chain (`CAPTURED` observation -> `DERIVED` candidate -> `FIX` promotion receipt) before any canonical review starts.

3. **One OpenSpace idea that is high-value for this template**

Treat skill evolution as a typed pipeline rather than a monolithic rewrite loop. The FIX/DERIVED/CAPTURED split is useful because it gives the template a truthful place for runtime observations and agent-derived proposals without pretending they are already canonical truth.

4. **One OpenSpace idea that this template should resist or heavily constrain**

Do not allow raw usage traces or transcript-like history to flow directly into canonical skill mutation. If the template adopts auto-rewrite behavior for normative fields, especially `purpose`, `triggers`, or guardrail skills, it will erase the main thing it currently gets right: explicit governance truth.

5. **Final recommendation**

- **freeze-plan**
- Freeze on Direction B plus a narrow slice of Direction C: add execution receipts, metric-triggered candidate creation, host/runtime integration points, and lineage tracking, while keeping canonical mutation human-governed and receipt-anchored.
