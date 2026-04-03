# Discussion Packet — skill_mechanism_v1

- Generated at: 2026-04-03T23:48:35.585368+00:00
- Owner: GitHub Copilot
- Current round goal: Obtain enough judgment to freeze a plan
- Round exit rule: Freeze a plan, narrow to a sharper second round, or stop on missing truth

## Decision Question

How should this framework introduce a strong, reasonable, and continuously self-updating SKILL mechanism without collapsing into vendor-specific prompt clutter?

## Why This Needs Discussion

The framework already has strong mechanism surfaces for discussion, audit, validation, and execution, but SKILL remains comparatively thin. External guidance now treats skills as a major extension surface, and we need to decide whether this repo should productize skills as first-class framework assets rather than ad hoc tips.

## Current Truth

- The repo already has a strategy-vs-mechanism split, discussion loop runbook, packet templates, validator pipeline, and bootstrap machinery.
- The repo has only light SKILL coverage today; it does not yet define a first-class SKILL architecture, lifecycle, validator contract, or update loop.
- Anthropic guidance emphasizes SKILL.md + supporting files, trigger-oriented descriptions, progressive disclosure, invocation control, hooks, scripts, and subagent execution.
- Thariq's guidance emphasizes gotchas, progressive disclosure, not stating the obvious, setup/config handling, memory, scripts, on-demand hooks, measurement, composition, and distribution.
- Cross-agent ecosystem work suggests skills can be packaged, installed, updated, and optionally lockfile-pinned across tools instead of living only as repo-local markdown.

## Constraints

- The mechanism should stay executor-agnostic where possible and should not assume one vendor is the only runtime.
- The mechanism should be validator-friendly: avoid relying on human memory for skill quality, triggerability, or upgrade behavior.
- The mechanism should support progressive disclosure and avoid forcing full skill payloads into every session.
- The mechanism should distinguish knowledge skills, workflow skills, verification skills, and guardrail skills rather than flattening them into one template.
- The mechanism should allow controlled self-update from evidence (gotchas, logs, review findings, failed validations) without permitting silent prompt drift.

## Candidate Directions

1. Minimal path: keep skills informal and add only a TYPE-A design/discussion doc plus a few examples.
2. Framework-native path: define a repo-local SKILL contract with types, trigger semantics, supporting files, validator checks, bootstrap surfaces, and update receipts.
3. Ecosystem path: build around an open agent-skills style package model with repo-local wrappers, installer/update guidance, and lockfile/distribution support.
4. Hybrid path: standardize a framework-native contract first, but make packaging/distribution an outer layer so repos can stay local-first or publish skills later.

## Evaluation Criteria

- Triggerability: can the agent reliably decide when to use a skill?
- Behavioral lift: does the skill materially change execution quality, safety, or speed?
- Progressive disclosure: can large references/scripts/examples stay out of default context?
- Updateability: can the skill improve from evidence without unreviewed drift?
- Portability: can the mechanism survive across agents or at least degrade honestly?
- Governance: can validators, tests, hooks, and closeout artifacts keep the skill layer truthful?
- Adoption cost: can smaller repos adopt a minimal useful subset before a marketplace-scale system exists?

## Suggested Executors

- Main thread synthesis
- Architect agent for framework-shape critique
- External Codex / Claude / Gemini reviewers using the same packet if a second round is needed

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

## Feedback — Round 1 — Architect

- Timestamp: 2026-04-03T23:49:42.644248+00:00
- Stance: favor hybrid framework-native core with vendor adapters
- Summary: Use a framework-native SKILL contract as the canonical mechanism, then treat vendor-specific formats and installable packaging as adapter layers. Keep self-updating evidence-driven but review-gated.

### Strengths

- Preserves the repo's strategy-versus-mechanism split instead of binding the framework to one vendor syntax.
- Makes skill types explicit: knowledge, workflow, verification, and guardrail skills should not share one flat contract.
- Reuses existing governance primitives: discussion packets, validators, receipts, bootstrap surfaces, and doc-first planning.
- Supports progressive disclosure by keeping the entry surface short while moving references, scripts, examples, and setup into linked support files.
- Allows measurable usage and updateability through invocation receipts rather than only file existence.
- Keeps repo-local adoption cheap while leaving a clean outer path to packaged or distributed skills later.

### Risks

- Self-updating can degrade into silent prompt drift if evidence and approved revisions are not strictly separated.
- Weak trigger semantics would make skills optional prose blobs that agents invoke inconsistently.
- Over-classifying too early could create a heavy taxonomy that smaller repos ignore.
- Portability can be overstated because hooks, tool gating, and forked execution do not map cleanly across every agent.
- Supporting files can hide stale guidance if validators only inspect the top-level entry.
- Packaging too early could drag the framework into ecosystem mechanics before the repo-local contract is stable.

### Open Questions

- What is the minimum trigger contract that makes a skill reliably invocable without binding to one vendor activation model?
- Which evidence sources are authoritative enough to propose a skill update, and how should they be ranked?
- What is the smallest useful metric set for skill quality beyond raw invocation count?
- When should a repo-local skill be promoted into a distributed/installable artifact?
- Should guardrail skills require stricter update policy than workflow or knowledge skills?
- How should the framework express honest degradation when an agent cannot support hooks or context-fork semantics?

### Recommended Next Step

Freeze a TYPE-A design doc for a framework-native SKILL contract, then run one narrower round only on measurement and update governance before any implementation or packaging work.

---

## Main-Thread Synthesis — Round 1

- Timestamp: 2026-04-03T23:49:57.375601+00:00
- Decision: continue-discussion
- Confidence: medium-high
- Next action: Run a narrower second-round discussion focused on measurement, evidence ranking, and review gates for self-updating skills, then freeze a TYPE-A SKILL design doc if that round converges.

### Summary

Current evidence supports a hybrid path: define a framework-native SKILL mechanism first, keep vendor-specific SKILL.md or agent-specific formats as adapters, and defer package distribution mechanics until the repo-local contract is stable. The hardest unresolved boundary is not syntax but governance: what evidence is allowed to update a skill, how the update is reviewed, and how invocation quality is measured.

### Rationale

- Anthropic guidance strongly supports progressive disclosure, supporting files, trigger-oriented descriptions, scripts, hooks, and invocation control, which means the framework should treat a skill as more than a markdown blob.
- Thariq's guidance reinforces that the highest-signal skill content comes from gotchas, operational scripts, setup handling, and measurement, which aligns with this repo's evidence-first governance model.
- The repo already has reusable mechanism surfaces for discussion, validation, receipts, bootstrap, and closeout; the most coherent move is to reuse those surfaces for SKILL rather than invent a separate informal prompt layer.
- Cross-agent packaging is strategically useful, but it should be an outer layer after the local canonical contract exists, otherwise the framework risks optimizing distribution before truthfulness.

### Follow-Up Questions

- What counts as a receipt anchor for a proposed skill update?
- Which skill types may auto-accumulate gotchas, and which require stricter manual review?
- What validator contract is minimal but non-fake for triggerability and progressive disclosure?
- Should bootstrap generate repo-local skills only, or also adapter stubs for vendor-specific skill formats?

---

## Execution Receipt — Round 2 — Multi-CLI Participation

- Timestamp: 2026-04-04T04:56:00+00:00
- Goal: obtain parallel CLI judgment on the narrowed governance questions for SKILL v1
- Shared prompt: `tmp/discussion/skill_mechanism_v1/round2/prompt.txt`
- Raw outputs:
	- `tmp/discussion/skill_mechanism_v1/round2/codex.md`
	- `tmp/discussion/skill_mechanism_v1/round2/copilot.md`
	- `tmp/discussion/skill_mechanism_v1/round2/gemini.md`
	- `tmp/discussion/skill_mechanism_v1/round2/claude.md`
- Runtime notes:
	- Claude CLI was callable but not authenticated in this environment: `Not logged in · Please run /login`.
	- Gemini CLI initially failed due temporary model-capacity exhaustion, then succeeded on a clean retry.
	- Codex CLI and GitHub Copilot CLI both completed successfully in headless mode.

## Feedback — Round 2 — Codex CLI

- Stance: support hybrid, but keep the canonical contract smaller and stricter than any adapter surface.
- Strongest claims:
	- The framework-native core should stay close to `id`, `type`, `purpose`, `triggers`, `entry_instructions`, labeled `references`, and explicit `governance` metadata.
	- Evidence may propose changes, but humans must approve any change to `purpose`, `triggers`, `entry_instructions`, or guardrail behavior.
	- Validators should enforce trigger specificity, reference integrity, governance freshness, and declared degradation for non-portable capabilities.
	- Hooks, tool gating, packaging, and context-fork execution belong in adapters, not the canonical core.
- Highest-risk failure mode: governance theater, where unreviewed evidence slowly mutates triggers and instructions into untraceable prompt residue.
- Narrowest next question proposed: define a field-by-field review matrix, especially what guardrail-skill fields are never eligible for auto-proposed updates.

## Feedback — Round 2 — GitHub Copilot CLI

- Stance: support hybrid, but make the canonical contract the only normative truth and prevent adapters from becoming a backdoor for silent drift.
- Strongest claims:
	- V1 should include explicit sections for identity, type, purpose, triggers, entry instructions, resources, constraints, evidence policy, and degradation policy.
	- Evidence ranking should start with human-reviewed postmortems and reproducible failures, then invocation receipts and operator-authored gotchas, with raw transcripts at the bottom.
	- Validators should require positive triggers, negative triggers, expected effect, dependency resolution, capability alignment, and degradation coverage.
	- Progressive disclosure is only honest when omitted detail is named explicitly and hidden files do not introduce new obligations.
- Highest-risk failure mode: silent prompt drift disguised as continuous improvement.
- Narrowest next question proposed: define the smallest receipt schema that can justify a skill-update proposal without exposing raw transcript content.

## Feedback — Round 2 — Gemini CLI

- Stance: strongly support hybrid because it keeps skills anchored in repo truth rather than vendor syntax.
- Strongest claims:
	- The core contract should stay minimal and deterministic: skill identity and type, trigger condition, execution boundary, progressive-disclosure references, and empirically proven gotchas.
	- Evidence should be ranked with root-cause notes and failure packets first, then closeout audits, telemetry, and finally agent-proposed observations.
	- Auto-collection may draft gotchas or reference-file additions, but any structural change to trigger conditions, execution boundaries, or workflow directives must remain human-reviewed.
	- Validators should check trigger collision risk, referenced file existence, and that the top-level skill does not collapse progressive disclosure by inlining heavy scripts or context dumps.
- Highest-risk failure mode: trigger bloat, where overlapping skills defeat the whole progressive-disclosure model.
- Narrowest next question proposed: how to enforce mutually exclusive or hierarchical triggers across skills without a central human router.

## Feedback — Round 2 — Claude CLI Runtime Blocker

- Status: callable binary confirmed, but this environment could not complete review because the CLI is not logged in.
- Evidence: `tmp/discussion/skill_mechanism_v1/round2/claude.md` contains `Not logged in · Please run /login`.
- Implication: the claim that all four CLIs can currently participate directly conflicts with the observed runtime state. Three CLIs produced usable feedback in this round; Claude remains a recoverable environment blocker rather than a design blocker.

## Main-Thread Synthesis — Round 2

- Timestamp: 2026-04-04T04:58:00+00:00
- Decision: freeze-plan
- Confidence: high
- Next action: promote the converged contract into a TYPE-A SKILL design doc when implementation work is requested.

### Convergence

- The hybrid direction is now strongly converged across the available CLIs: the canonical truth should be framework-native, while vendor formats, packaging, hooks, tool gating, and subagent/fork behavior remain adapter layers.
- All three successful CLIs independently converged on the same governance boundary: evidence may propose, but human review must gate any change to normative instructions, trigger conditions, execution boundaries, or guardrail behavior.
- There is broad agreement that the canonical v1 contract must stay small. The stable center is: identity, type, purpose, triggers, entry instructions, references/resources, governance or evidence/update policy, and explicit degradation semantics for non-portable features.
- There is also broad agreement that validators should enforce only the truthful mechanical layer: required fields, trigger specificity, reference integrity, capability/degradation declarations, and the separation between entry instructions and deeper supporting artifacts. Usefulness, elegance, and broad prose quality should remain advisory.

### Decisions To Carry Forward

- Freeze a framework-native SKILL contract that is smaller than any vendor adapter and explicitly prohibits adapter-to-core backflow without review.
- Make `guardrail` skills stricter than the other skill types for update policy; no CLI argued for relaxed automatic mutation here.
- Treat raw transcripts, model summaries, and frequency-based heuristics as low-trust evidence. They can propose candidate gotchas or receipts, but they must not directly rewrite canonical instructions.
- Make honest degradation a first-class field rather than an undocumented side effect. If hooks, tool gating, or forked execution are unavailable, the skill must declare the fallback behavior rather than implying parity.

### Remaining Narrow Question

- If another discussion round is needed, it no longer needs to be broad. The narrowest unresolved design question is now the receipt and review matrix: which fields may be updated from which evidence sources, under what reviewer threshold, and with what stricter rules for guardrail skills.
