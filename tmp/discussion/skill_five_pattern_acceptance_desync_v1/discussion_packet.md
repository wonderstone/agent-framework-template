# Discussion Packet — skill_five_pattern_acceptance_desync_v1

- Generated at: 2026-04-07T10:30:13.616652+00:00
- Owner: main-thread
- Current round goal: Obtain enough judgment to freeze a plan
- Round exit rule: Freeze a plan, narrow to a sharper second round, or stop on missing truth

## Decision Question

After the five-pattern scaffold implementation wave, where do upper-layer rules, docs, validator claims, or governance surfaces still drift away from lower-layer starter surfaces, bootstrap output, examples, or executable proof?

## Why This Needs Discussion

The implementation wave is complete and validated, but the user explicitly wants a hostile acceptance round focused on upper-layer versus lower-layer desynchronization before treating the wave as truly solid.

## Current Truth

The repository now ships five-pattern boundary text in the canonical SKILL docs, new starter scaffold templates for Wrapper/Reviewer/Pipeline/bounded Generator, new examples under examples/skills, bootstrap wiring, validator rules, focused tests, full tests, and a successful standard-profile bootstrap smoke dry-run. The risk is not obvious breakage; it is hidden desync between what upper-layer rules claim and what lower-layer executable surfaces really guarantee.

## Constraints

Be adversarial. Prefer finding mismatches, overclaims, validator blind spots, profile-distribution mistakes, example/template drift, rule/execution gaps, or fake confidence. Do not redesign the whole framework. Judge the shipped wave as it exists. Distinguish clearly between constitutional rule surfaces, validator-enforced truth, bootstrap-distributed assets, and lower-layer starter/example execution semantics.

## Candidate Directions

Direction A: no material desync remains; only minor wording polish. Direction B: there are doc or rule claims not fully grounded in bootstrap/validator/example reality. Direction C: there are validator or bootstrap blind spots that allow upper-layer claims to drift. Direction D: reviewer/pipeline/wrapper/generator placement still has unresolved layer bleed between governance and execution. Direction E: one or more shipped surfaces should be downgraded, tightened, or explicitly scoped to remove false confidence.

## Evaluation Criteria

Does the critique find concrete upper/lower mismatch with file-level evidence? Does it separate rule-layer concerns from execution-layer concerns? Does it avoid asking for unsupported runtime power? Does it focus on acceptance-risk rather than open-ended redesign?

## Suggested Executors

Claude CLI; Codex CLI; Gemini CLI; GitHub Copilot CLI; main-thread synthesis

## Instructions For Participating Executors

1. Read the packet before commenting.
2. Do not rewrite the packet body unless the main thread asks for it.
3. Append your feedback at the end of this file.
4. Prefer concrete tradeoffs, risks, and missing evidence over style opinions.
5. If another round is needed, propose the narrowest next question.

## Main-Thread Decision Status

- Current status: closed
- Final decision: accept-with-fixes

## Append-Only Discussion Log

<!-- Append feedback and synthesis entries below this line. -->

## Feedback — Round 1 — Claude CLI

- Stance: conditional
- Summary: The wave is coherent, but the rule layer still overstates what the validator and adopter validation surfaces actually enforce.

### Strengths

- Identified a concrete constitutional-to-validator mismatch in the SKILL mechanism hard-fail claims.
- Distinguished structural presence checks from real executable or profile-aware proof.

### Risks

- The current doc wording can create false confidence about mechanical enforcement.
- The adoption guide still overreaches on where the structured validator is safe to run.

### Open Questions

- Whether to downgrade the SKILL mechanism wording or implement the missing validator checks.
- Whether to narrow five-pattern naming to four scaffolds plus the canonical base contract.

### Recommended Next Step

- Tighten the overstated rule and validator claims before treating the five-pattern wave as fully closed.

---

## Feedback — Round 1 — Codex CLI

- Stance: conditional
- Summary: The main desync is profile-level and contract-level: standard-profile adopters inherit docs that still point at full-only example surfaces, and the adoption guide understates the Build contract enforced by the adopter manifest.

### Strengths

- Found an adopter-facing profile mismatch that can survive green validation.
- Isolated a concrete doc-to-manifest mismatch around the required Build surface.

### Risks

- Standard adopters can receive broken local guidance without the validator catching it.
- Profile drift is likely to recur until the docs are validated against shipped profile surfaces.

### Open Questions

- Whether the docs should be marked full-only for example-heavy guidance or the standard profile should ship more example surfaces.

### Recommended Next Step

- Make profile scoping explicit in README and ADOPTION_GUIDE and add profile-aware doc integrity checks.

---

## Feedback — Round 1 — Gemini CLI

- Stance: conditional
- Summary: The new scaffold wave is still partly invisible to automated adoption and validation because the adoption prompt, example count language, and template classification logic lag the shipped starter set.

### Strengths

- Flagged automated-adoption invisibility rather than only validator wording gaps.
- Surfaced a concrete validator issue around treating only templates/skill.template.md as a true template.

### Risks

- Future adopters can discard or misclassify the new starter templates while still believing they preserved SKILL support.
- Pattern templates remain more concrete-skill-like than reusable-template-like under current validation logic.

### Open Questions

- Whether all .template.md skill files should be treated as reusable templates by the validator.
- Whether reviewer and pipeline starters should loosen their git-audit-specific required references.

### Recommended Next Step

- Update adoption-facing keep lists and align validator template classification with the shipped starter-template family.

---

## Feedback — Round 1 — GitHub Copilot CLI

- Stance: conditional
- Summary: The wave passes structural checks, but the lower layer only proves snippet integrity and file presence, not the stronger executable-proof and profile-truth claims now implied by the upper docs.

### Strengths

- Cross-checked docs, bootstrap, validator, tests, and examples in one pass.
- Cleanly separated structural validation from adopter-useful proof.

### Risks

- The current wording makes scaffold shipment sound stronger than the real proof surface.
- Example and profile drift can persist because narrative claims are not validator-checked.

### Open Questions

- Whether to add runnable smoke paths for the new scaffold families or downgrade the “proof” language.

### Recommended Next Step

- Reframe the wave as structurally shipped scaffolds unless or until executable pattern-family proof exists.

---

## Main-Thread Synthesis — Round 1

- Decision: accept-with-fixes
- Confidence: High
- Next action: tighten the adopter-facing docs and validator claims before treating the five-pattern scaffold wave as fully accepted.

### Summary

The four-CLI hostile acceptance round converged on the same broad judgment: the five-pattern scaffold wave is not broken, but it is not yet honest enough to count as a clean PASS. All usable outputs landed on conditional acceptance and found desync at the boundary between upper-layer claims and lower-layer proof. The most repeated problems were profile mismatch in standard-profile docs, validator blind spots around narrative and pattern-specific promises, stale example-count language, and overclaiming what is mechanically enforced or executable today.

### Rationale

The lower layer currently proves that the new scaffold files exist, that bootstrap copies selected surfaces, and that some required snippets are present. It does not yet prove every stronger claim now implied by the docs: that standard-profile adopters receive all referenced examples, that all five-pattern starter surfaces are visible to automated adoption flows, that the validator mechanically enforces the full SKILL mechanism hard-fail list, or that wrapper or reviewer or pipeline or generator families have executable proof beyond structural presence. That makes the right closeout a focused honesty-hardening pass, not a redesign and not a rubber-stamp acceptance.

### Required Fix Set Before Clean PASS

1. Align README and ADOPTION_GUIDE profile guidance with what standard versus full actually bootstrap.
2. Fix or downgrade upper-layer wording that currently overstates validator enforcement or executable proof.
3. Update stale adoption/example inventory language so the shipped scaffold wave is accurately described.

### Follow-Up Questions

- Should the next patch favor wording downgrades, stronger validator checks, or both?
- Which of the new scaffold families deserves a real runnable smoke path first?
