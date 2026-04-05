# Discussion Packet — template_framework_drift_audit_v1

- Generated at: 2026-04-05T01:12:16.284700+00:00
- Owner: main-thread
- Current round goal: Obtain sharp critique on the top current framework drift risks and decide whether to patch now.
- Round exit rule: Freeze a plan, narrow to a sharper second round, or stop on missing truth

## Decision Question

Is the current template framework contract honest and operationally sound for adopters, or are there real expectation-vs-reality drift risks that should be fixed now?

## Why This Needs Discussion

The repository has accumulated several governance and contract surfaces quickly. Before adding more layers, we need a critical audit of whether the template currently promises more than it reliably enforces or demonstrates.

## Current Truth

- The repository ships bootstrap, validator, discussion-loop, SKILL, harvest-loop, developer-toolchain, and traceability surfaces.
- The validator does enforce SKILL reference-path integrity and governance-tier checks.
- The full-stack example project-context file is filled, not a stub.
- A concrete mismatch already exists: the root session_state.md still reflects the previous SKILL follow-up goal even though that work was committed and pushed, which means the framework is currently violating its own state-truth discipline.
- Another likely risk area is whether git closeout and execution-contract guidance is operationally specific enough for adopters, or still too abstract.

## Constraints

- Be critical, not polite.
- Prefer evidence-backed drift risks over speculative redesign.
- Distinguish between current bug, governance gap, doc overclaim, and acceptable known limit.
- Propose the smallest honest fix when possible.
- Assume the repository can change docs, validators, templates, examples, and tests in this round if needed.

## Candidate Directions

- Direction A: make targeted fixes only for confirmed drift bugs or overclaims.
- Direction B: soften docs/claims where the framework is intentionally design-first and not yet executable.
- Direction C: add stronger executable guardrails or examples so the framework proves the behavior it claims.

## Evaluation Criteria

- Does the finding describe a real user-visible or adopter-visible drift?
- Is the risk current and evidence-backed?
- Can the framework fix it cheaply and honestly now?
- Would leaving it unfixed mislead adopters about how the template behaves?

## Suggested Executors

- Claude CLI
- Codex CLI
- Gemini CLI
- GitHub Copilot CLI
- Main thread synthesis

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

- Timestamp: 2026-04-05T01:28:52.406588+00:00
- Stance: patch-now
- Summary: Framework is mostly sound, but stale root state plus over-strong enforcement framing create material honesty drift.

### Strengths

- Core architecture, bootstrap, validator, and examples are real.
- The git-audit and discussion-loop mechanisms are stronger than the packet initially suspected.

### Risks

- Root session_state.md had become stale.
- README phrasing was stronger than the current executable proof for some instruction-bound surfaces.

### Open Questions

- Should live state freshness eventually gain an executable repo-level audit?
- Should execution-contract instantiation stay workflow-driven or later become validator-backed?

### Recommended Next Step

- Patch the stale root state now and clarify hard-versus-soft enforcement in adopter-facing docs.

---

## Feedback — Round 1 — Codex CLI

- Timestamp: 2026-04-05T01:28:52.524435+00:00
- Stance: patch-now
- Summary: The main drift risk is self-hosting truthfulness, not missing framework architecture.

### Strengths

- The repo already ships real mechanisms for bootstrap, validation, and packetized audit.
- The discussion packet correctly focused on small honesty fixes rather than redesign.

### Risks

- Root session_state.md contradicted the actual completed work.
- Execution-contract expectations were still stronger than the proof shipped in examples.

### Open Questions

- Is a lightweight self-hosting stale-state check worth adding later?
- Which instruction-bound conventions should remain intentionally non-mechanical?

### Recommended Next Step

- Repair the self-hosting state surface and add one real execution-contract example.

---

## Feedback — Round 1 — Gemini CLI

- Timestamp: 2026-04-05T01:29:19.979033+00:00
- Stance: patch-now
- Summary: The framework is operationally reasonable, but proof boundaries should be made more explicit to adopters.

### Strengths

- The repo has concrete shipped assets rather than only policy prose.
- The current abstraction level for git closeout is acceptable.

### Risks

- Stale state weakens the framework credibility by example.
- Adopters could overestimate which rule surfaces are mechanically enforced.

### Open Questions

- Should demo artifacts continue to shoulder the proof burden for workflow surfaces?
- Would a later live-state audit be preferable to more prose disclaimers?

### Recommended Next Step

- Keep the architecture, but clarify proof boundaries and maintain a truthful root state.

---

## Feedback — Round 1 — GitHub Copilot CLI

- Timestamp: 2026-04-05T01:29:20.096060+00:00
- Stance: patch-now
- Summary: The repo needs a narrow honesty-hardening pass: current state, execution-contract example, and explicit enforcement tier wording.

### Strengths

- Resumable git-audit and discussion-loop surfaces are already backed by scripts, tests, and examples.
- The packet highest-signal concern was state truthfulness.

### Risks

- Execution contracts were described as a first-class surface without a concrete completed example.
- Instruction-bound discipline could be misread as universally hook-enforced.

### Open Questions

- Which future workflow surfaces deserve conversion from guidance to executable checks?
- Is current optional-hook posture still the right default for adopters?

### Recommended Next Step

- Land a small proof-restoring patch and stop unless new evidence appears.

---

## Main-Thread Synthesis — Round 1

- Timestamp: 2026-04-05T01:29:20.230345+00:00
- Decision: freeze-plan
- Confidence: High
- Next action: Patch the confirmed honesty gaps, run validation, and summarize residual risks without reopening the framework design.

### Summary

- All four CLI participants converged that the framework is broadly reasonable and does not need redesign.
- The most concrete current drift was the stale root session_state.md.
- The next highest-value fixes were not architectural: add one filled execution-contract example and clarify which surfaces are mechanically enforced versus instruction-bound.

### Rationale

- The packet deliberately challenged stale assumptions, and the CLIs rejected two of them: the SKILL validator still checks reference paths, and the full-stack project-context example is already real.
- Consensus was strongest on proof-restoring fixes that improve adopter honesty without widening scope.
- The git-audit and discussion-loop mechanisms were assessed as comparatively mature, so no second round is needed.

### Follow-Up Questions

- A future round can decide whether live session-state freshness deserves its own executable audit.
