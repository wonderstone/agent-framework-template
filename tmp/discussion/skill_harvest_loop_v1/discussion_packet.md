# Discussion Packet — skill_harvest_loop_v1

- Generated at: 2026-04-05T00:00:00+00:00
- Owner: GitHub Copilot
- Current round goal: Decide whether and how the framework should turn finished task history into review-gated SKILL improvements without relying on a human to manually inspect every conversation.
- Round exit rule: Freeze a concrete mechanism direction, narrow to one sharper governance question, or stop if the proposal cannot stay truthful.

## Decision Question

How should this framework add a post-task SKILL-harvest workflow that makes the agent layer improve from real usage while minimizing direct human review and still preventing silent prompt drift?

## Why This Needs Discussion

The framework now has a formal SKILL contract, starter examples, a validator, and a field-level receipt and review matrix. What it does not yet have is the operational loop that turns finished task history into trustworthy candidate improvements. The missing mechanism is not whether agents can learn from usage in principle, but how to do so without creating automatic transcript-to-skill mutation.

## Current Truth

- The repository already distinguishes canonical framework-native skills from vendor adapters.
- The SKILL draft already forbids raw transcripts and model summaries from directly mutating canonical skill fields.
- The current review matrix still assumes human approval as the review primitive, but it does not yet say whether that review can be delegated to a role, a subagent, an external CLI, or the main thread.
- The framework already has receipts, discussion packets, handoff patterns, and truth-oriented validators that could be reused for skill promotion instead of inventing a separate mechanism.
- The user wants the workflow to become more autonomous over time and explicitly wants us to consider delegated reviewers rather than requiring a human to personally inspect every proposed skill update.

## Constraints

- The mechanism must not allow direct transcript-to-skill rewriting.
- The workflow should minimize human bottlenecks, but it still needs a real stop rule before canonical skill drift becomes invisible.
- The mechanism should fit the existing framework philosophy: stable packets, receipts, validators, delegated roles, and owner synthesis rather than free-form hidden memory.
- The system should distinguish between candidate extraction, candidate triage, patch proposal, review, and canonical promotion rather than flattening those into one opaque step.
- The design should support delegated review by role or executor, but should not assume one vendor CLI is the only reviewer.

## Candidate Directions

1. Conservative human gate: always generate skill candidates automatically, but require a human maintainer to approve every canonical change.
2. Delegated reviewer gate: automatically generate candidates and proposed patches, then delegate review to a bounded role implemented by a CLI, subagent, or main-thread owner; human escalation happens only for exception classes.
3. Confidence-tiered auto-promotion: low-risk fields such as references or gotcha appendices may promote automatically from strong receipts, while normative fields still require delegated review.
4. Full autonomous promotion: let the agent pipeline extract, review, and merge canonical skill changes end-to-end unless a validator or risk rule blocks it.

## Evaluation Criteria

- Truthfulness: does the mechanism keep candidate evidence distinguishable from approved canonical skill content?
- Autonomy: how much human bottleneck remains in the steady state?
- Drift resistance: can the workflow resist silent degradation from repeated weak proposals?
- Role compatibility: can review be delegated cleanly to a role instead of a specific person or tool?
- Validator fit: can enough of the mechanism be made mechanically checkable?
- Operational cost: can the workflow run after many tasks without becoming an administrative tax?

## Suggested Executors

- Claude Code CLI
- Codex CLI
- Gemini CLI
- GitHub Copilot CLI
- Main-thread synthesis owner

## Instructions For Participating Executors

1. Read the packet before commenting.
2. Do not rewrite the packet body unless the main thread asks for it.
3. Append feedback at the end of this file.
4. Prefer concrete workflow and governance proposals over generic warnings.
5. Assume the goal is to minimize direct human review, but not to remove all review boundaries.
6. If another round is needed, propose the narrowest next question.

## Main-Thread Decision Status

- Current status: open
- Final decision: pending

## Append-Only Discussion Log

<!-- Append feedback and synthesis entries below this line. -->

### Round 1 — Claude Code CLI

- Verdict: support direction 3 with revision; confidence-tiered promotion is viable only if tier assignment is structural and computed from the SKILL contract rather than chosen by the harvester.
- Recommended workflow: task closeout receipt -> candidate extraction -> delegated review -> conditional promotion -> promotion receipt.
- Delegation boundary: receipt emission, extraction, and tier classification may be automated; delegated reviewers may approve `appendix-safe` and `normative-delegated` candidates; `normative-human` fields stay direct-human only.
- Main risk callout: tier creep, evidence laundering, and reviewer collapse if two delegated reviewers are effectively the same reasoning system.
- Best contract shape: add per-field `promotion_tier`, `candidate_packet`, `promotion_receipt`, and reviewer-role exclusion rules.
- Strongest disagreement: the packet currently treats autonomy as a review-volume problem when the harder problem is freezing field authority classes up front.
- Narrowest next question: should `promotion_tier` be a human-authored immutable per-field annotation in the SKILL schema?

### Round 1 — Codex CLI

- Verdict: revise toward delegated, evidence-bounded promotion with explicit exception classes and periodic human audit.
- Recommended workflow: task closeout freeze -> candidate extraction -> triage and classing -> patch proposal -> delegated review -> promotion decision -> canonical promotion and audit log -> drift audit.
- Delegation boundary: automation may handle freeze, extraction, deduplication, validator checks, risk pre-classification, and audit sampling; role-based reviewers should handle routine triage and low-risk promotion; humans still own normative instructions, safety boundaries, delegation rules, validator semantics, and thin-evidence cases.
- Main risk callout: reviewer capture, evidence laundering, and risk-class gaming unless candidate truth stays separate from canonical truth.
- Best contract shape: add `candidate_packet`, `promotion_receipt`, `promotion_decision`, `reviewer_role`, `review_executor`, `confidence_tier`, `risk_class`, `exception_class`, `evidence_set`, `lineage_parent`, `promotion_scope`, and `audit_status`.
- Strongest disagreement: reviewer identity is not the design center; promotion authority classes are.
- Narrowest next question: which exact SKILL field classes are eligible for delegated auto-promotion versus permanent escalation?

### Round 1 — Gemini CLI

- Verdict: support delegated minimal-human review only if extraction stays strictly separate from promotion and structurally mutable zones are frozen in advance.
- Recommended workflow: extraction -> triage and deduplication by a `Skill Librarian` role -> patch proposal -> delegated review -> canonical promotion with promotion receipt.
- Delegation boundary: extraction, deduplication, patch formatting, and confidence-tier generation may be automated; a `Skill Librarian` and review subagent may handle low-risk append-only lanes; core instruction rewrites and contradictory candidates still require direct human approval.
- Main risk callout: prompt drift through accumulation of hyperspecific edge cases until the skill turns into a bloated transcript surrogate.
- Best contract shape: add `Candidate_Extraction_Packet.md`, `Skill_Promotion_Patch.md`, `Confidence_Tier`, `Promotion_Receipt.md`, and delegated reviewer-role definitions.
- Strongest disagreement: the current framing underweights the need for structurally immutable human-only zones inside the skill file.
- Narrowest next question: which sections of a skill are human-only edit zones versus subagent promotion zones?

### Round 1 — GitHub Copilot CLI

- Verdict: revise the direction toward autonomous evidence production plus delegated judgment plus explicit escalation, rather than equating automation with promotion.
- Recommended workflow: task closeout receipt -> harvest extraction -> candidate normalization -> mechanical screening -> delegated triage review -> patch proposal -> promotion review -> canonical promotion -> post-promotion audit sampling.
- Delegation boundary: automation may generate observations, normalize them, run schema and contradiction checks, and draft patches; delegated reviewers should own triage and most routine promotion review; direct human decisions remain required for constitutional changes such as review thresholds, validator policy, authority definitions, and provenance weakening.
- Main risk callout: false generalization, self-reinforcing reviewer drift, quiet dilution of normative guidance, and authority ambiguity.
- Best contract shape: add `candidate_packet`, `promotion_receipt`, `promotion_decision_record`, delegated reviewer role, authority source, confidence tier, risk tier, exception class, evidence set, affected canonical fields, contradiction status, escalation flag, and supersession fields.
- Strongest disagreement: the real split is constitutional change versus operational refinement, not human review versus delegated review.
- Narrowest next question: which canonical SKILL fields are informational, normative, or constitutional for promotion-governance purposes?

### Main-Thread Synthesis — Round 1

- Convergence: all four participants reject direct transcript-to-skill mutation and converge on the same core ladder: closeout receipt -> candidate extraction -> classification or normalization -> delegated review -> promotion receipt -> audit.
- Strongest shared correction: the design center should shift away from reviewer identity and toward authority classes. The key question is not "human or delegated" in the abstract; it is which field classes may be changed by which authority under which evidence threshold.
- Shared governance boundary: candidate truth must remain distinct from canonical truth. Receipts and candidate packets may accumulate aggressively; canonical mutation must stay explicit, typed, and reversible.
- Likely stable direction: adopt a tiered promotion model rather than a single global review rule. A working vocabulary is emerging across the four responses: appendix-safe or descriptive lanes, delegated normative lanes, and escalation-only or constitutional lanes.
- Most reusable mechanism pieces already exist in-framework: closeout receipts, reviewer roles, validators, audit logs, and append-only packets. The missing layer is a promotion-governance contract that binds field class -> allowed authority -> minimum evidence -> escalation triggers.
- Main unresolved choice: whether the framework should encode this as a per-field `promotion_tier` table in the canonical SKILL contract, a section-level mutable-zone map, or a hybrid of both. The round strongly suggests that runtime reviewers should not be allowed to improvise that classification.
- Provisional direction freeze: do not pursue full autonomous promotion. Move toward delegated, evidence-bounded promotion with explicit exception classes, periodic human audit sampling, and a human-owned schema for field authority.
- Narrowed next question for round 2: what is the minimal canonical field-classification model that can support delegated promotion honestly without letting the harvester self-classify its own authority?

### Round 2 Kickoff — Main Thread

- Question freeze: choose the minimal canonical field-classification model for SKILL promotion governance.
- Option A: per-field `promotion_tier` table attached directly to the canonical SKILL schema.
- Option B: section-level mutable-zone map, where entire sections are marked delegated-safe, delegated-reviewed, or human-only.
- Option C: hybrid model, with section zones as the primary boundary plus per-field overrides for a small number of special fields.
- Existing truth to reuse: the canonical v1 contract already exposes six load-bearing fields (`purpose`, `triggers`, `entry_instructions`, `references`, `governance`, `degradation`) and a field-level receipt/review matrix. The new mechanism should extend that truth rather than invent a parallel taxonomy.
- Decision criteria for round 2: smallest truthful schema surface, lowest risk of authority drift, easiest validator enforcement, and clearest portability across executor types.
- Out-of-scope for round 2: package distribution, installer behavior, lockfiles, or vendor-specific prompt file shapes.

### Round 2 — Claude Code CLI

- Verdict: choose A, adding a `Promotion authority` column directly to the existing field matrix.
- Why A wins: one additive column on an already-validator-enforced six-row table is smaller and safer than introducing section zones or precedence rules.
- Minimal contract shape: extend the existing matrix with a closed enum for field authority; Claude proposed `delegated-safe`, `delegated-reviewed`, and `human-only`, with `purpose`, `triggers`, and `governance` frozen as `human-only`.
- Validator focus: enforce closed-enum values, keep `governance` permanently `human-only`, reject reviewer-proposer identity collapse, and add stronger guardrail-type minima.
- Drift warning: repeated valid edits to `entry_instructions` can accumulate into semantic posture change even when each patch is individually legal.
- Narrowest remaining question: should the drift-audit counter live in the skill itself or in an external promotion-state registry?

### Round 2 — Codex CLI

- Verdict: choose A.
- Why A wins: the canonical contract already reasons at the field level, so per-field authority reuse is the smallest honest extension and prevents runtime actors from inventing their own classification layer.
- Minimal contract shape: add an immutable field-classification table keyed by the six canonical fields with `promotion_tier`, `minimum_evidence`, and `escalation_triggers`; propagate that table into the template, validator, and promotion receipts.
- Validator focus: require total field coverage, enforce enum validity, compare patch scope against field authority, and reject transcript-origin canonical mutation.
- Drift warning: tier laundering through gradually over-permissive field assignments.
- Narrowest remaining question: what exact `promotion_tier` enum should the canonical table use for the six existing fields?

### Round 2 — Gemini CLI

- Verdict: choose A.
- Why A wins: extending the existing field-level receipt and review matrix is simpler and more mechanically verifiable than adding section zones or a hybrid override model.
- Minimal contract shape: add a strict `promotion_tier` property mapped to the six existing canonical fields and bind it directly into the canonical SKILL doc plus validator contract.
- Validator focus: block any patch whose requested mutation exceeds the runtime authority implied by the target field's `promotion_tier`; escalate `human-only` fields automatically.
- Drift warning: prompt bloat via repeated low-quality micro-updates to lower-tier fields.
- Narrowest remaining question: what evidence threshold is sufficient for `delegated-normative` style fields without forcing escalation every time?

### Round 2 — GitHub Copilot CLI

- Verdict: choose A.
- Why A wins: authority should stay at the same granularity as the current six-field contract, rather than adding a coarser section taxonomy or a dual-layer override system.
- Minimal contract shape: add a fixed `promotion_tier` table keyed by the six canonical fields, treat that table as human-owned governance metadata, require every candidate to declare `affected_fields`, and bind receipts to the resolved tier for each field.
- Validator focus: ensure six-field table completeness, prohibit tier changes through normal promotion, require evidence attachment, and reject edits outside declared fields.
- Drift warning: delegated reviewers may repeatedly broaden a delegated field until it carries more normative weight than intended.
- Narrowest remaining question: what is the smallest fixed enum for `promotion_tier` that covers the six canonical fields without introducing a second taxonomy?

### Main-Thread Synthesis — Round 2

- Outcome: round 2 resolves decisively in favor of Option A. All four participants rejected section-level mutable zones and rejected the hybrid as unnecessary schema bloat for a contract that currently has only six load-bearing fields.
- Stable design direction: extend the existing field-level receipt and review matrix rather than inventing a second authority model. The governance surface should remain field-native.
- Strongest shared rationale: the framework already treats `purpose`, `triggers`, `entry_instructions`, `references`, `governance`, and `degradation` as the canonical unit of truth. Authority classification should live at that exact unit so validator enforcement, receipts, and review behavior all bind to the same object.
- Strongest shared rejection of B and C: section boundaries are too coarse and too easy to game through content reshuffling, while the hybrid quietly recreates per-field governance anyway and adds precedence ambiguity on top.
- Provisional field-authority freeze: `purpose`, `triggers`, and `governance` are the clearest `human-only` candidates; `references` is the clearest delegated-safe or lowest-risk delegated lane; `entry_instructions` and `degradation` sit in the delegated-reviewed middle and need explicit anti-accumulation controls.
- Validator consequence: the next implementation should likely add one new closed-enum column to the existing matrix, require exact six-field coverage, forbid runtime tier mutation, and require every candidate or promotion receipt to bind `affected_fields` to the canonical field-authority table.
- Remaining disagreement is narrow and implementable: not whether to choose A, but what the smallest honest enum should be and whether cumulative drift on delegated-reviewed fields is controlled by evidence thresholds alone or also by an external promotion-state or audit registry.
- Direction freeze after round 2: the framework should model SKILL promotion authority as a human-authored per-field table attached to the existing canonical contract, not as section zones and not as a mixed dual-authority system.