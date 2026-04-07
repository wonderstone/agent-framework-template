# Discussion Packet — skill_hard_fail_mechanicalization_v1

- Generated at: 2026-04-07T13:16:20.647678+00:00
- Owner: main-thread
- Current round goal: Obtain enough judgment to freeze a plan
- Round exit rule: Freeze a plan, narrow to a sharper second round, or stop on missing truth

## Decision Question

How should the validator mechanically implement Hard-Fail checks 2, 4, and 5 from docs/SKILL_MECHANISM_V1_DRAFT.md without creating fake semantic certainty or brittle false positives?

## Why This Needs Discussion

- The first lower-layer proof-surface patch is complete, but the remaining gap is that the docs still promise hard-fail checks for weak triggers, runtime claims without matching degradation, and entry_instructions that collapse progressive disclosure.

## Current Truth

- bootstrap, validator, tests, and standard-profile example surfaces were just strengthened and validated\n- the unresolved gap is specifically validator mechanicalization for hard-fail checks 2, 4, and 5\n- we prefer lower-layer completion over shrinking upper-layer wording by default

## Constraints

- prefer honest, bounded, validator-friendly heuristics over fake semantic judgment\n- avoid broad redesign or new DSLs\n- if a check cannot be made trustworthy, say so explicitly and recommend wording shrink only as fallback

## Candidate Directions

- implement conservative syntactic heuristics now\n- implement narrower field-specific checks tied to explicit markers\n- split some checks into hard-fail plus advisory subparts\n- conclude one or more checks cannot be made trustworthy enough yet

## Evaluation Criteria

- truthful enforcement\n- low false-positive risk\n- adopter portability\n- testability\n- alignment with existing SKILL contract

## Suggested Executors

- Claude CLI\n- Codex CLI\n- Gemini CLI\n- GitHub Copilot CLI\n- main-thread synthesis

## Instructions For Participating Executors

1. Read the packet before commenting.
2. Do not rewrite the packet body unless the main thread asks for it.
3. Append your feedback at the end of this file.
4. Prefer concrete tradeoffs, risks, and missing evidence over style opinions.
5. If another round is needed, propose the narrowest next question.

## Main-Thread Decision Status

- Current status: closed
- Final decision: partial-implement

## Append-Only Discussion Log

<!-- Append feedback and synthesis entries below this line. -->

### GitHub Copilot CLI — 2026-04-07

- **Verdict:** `PARTIAL-IMPLEMENT`

- **Check 2 — trigger conditions are too weak to be actionable**
  - **Recommended enforcement shape:** split the current idea into a hard structural floor plus an advisory specificity pass.
  - **Hard-fail portion:** require at least one bullet in each of `Positive Triggers`, `Negative Triggers`, and `Expected Effect`; require positive trigger bullets to contain an explicit condition marker such as `when`, `if`, or `unless`; require negative trigger bullets to contain a disqualifier form such as `do not`, `avoid`, `unless`, or `if not`; require positive and negative trigger bullet sets not to normalize to the same text.
  - **Advisory portion:** warn when all trigger bullets are short generic boilerplate with no scope anchors such as backticked paths, named artifacts, named stages, named surfaces, or bounded nouns already used elsewhere in the skill.
  - **Exact mechanical proxy or heuristic:** normalize bullet text to lowercase, strip punctuation, then check:
    1. each required subsection has at least one `- ` bullet
    2. at least one positive bullet matches `\b(use|invoke|apply)\b.*\b(when|if|unless)\b` or at minimum contains `when|if|unless`
    3. at least one negative bullet matches `\b(do not|don't|avoid|unless|if not)\b`
    4. normalized positive and negative bullet strings are not identical
    5. advisory only: no bullet contains any bounded-anchor token such as backticks, `/`, `.md`, `.py`, `packet`, `receipt`, `surface`, `path`, `stage`, `artifact`, `schema`, `review`, or `closeout`
  - **Biggest false-positive risk:** honest skills with terse but still real trigger prose may fail the lexical condition-marker rule, especially adopted repos that prefer different phrasing.
  - **Smallest honest next step:** add only the structural hard-fail now; keep the “weak to be actionable” wording narrowed in code comments/tests to mean “missing conditional/disqualifier form or mirrored positive/negative text,” not true semantic usefulness.

- **Check 4 — runtime-specific behavior is claimed without a matching degradation declaration**
  - **Recommended enforcement shape:** implement a conservative hard-fail for claim-family presence plus degradation-family presence, and keep finer “matching” judgment advisory unless a claim family can be mirrored syntactically.
  - **Hard-fail portion:** if skill text outside `## Degradation` contains runtime-capability family tokens, then `## Degradation` must contain both an unavailability/degrade marker and either the same family token or an approved fallback outcome.
  - **Exact mechanical proxy or heuristic:** scan non-template skills and examples for claim families in `Purpose`, `Triggers`, `Entry Instructions`, and `Validator Notes`:
    - executor/runtime families: `external cli`, `subagent`, `main-thread`, `host-runtime`, `hook`, `tool gating`, `context isolation`
    - runtime-path families: `runtime`, `health`, `smoke`, `repro path`, `toolchain surface`, `independent reviewer path`
    Then require the `Degradation` section to include:
    1. an unavailable/degrade marker: `if .* unavailable`, `if no`, `if .* missing`, `downgrade`, `fallback`, `fall back`, `stop`, `block`, `refus`, or `manual`
    2. either one token from the same detected family or one approved fallback outcome phrase such as `advisory-only`, `explicit refusal`, `owner checkpoint`, `record the missing`, `stop`
  - **Biggest false-positive risk:** general discussion of runtime concepts in a skill may trip the claim-family detector even when the prose is descriptive rather than a normative runtime claim.
  - **Smallest honest next step:** implement family-based detection only for the already-shipped starter/example surfaces first, then generalize to adopted `SKILL.md` files once the family list survives a few real examples.

- **Check 5 — `entry_instructions` inlines what should remain in referenced artifacts and collapses progressive disclosure**
  - **Recommended enforcement shape:** split into hard-fail for obvious structural collapse and advisory for density/bloat.
  - **Hard-fail portion:** reject `Entry Instructions` sections that contain fenced code blocks, markdown tables, or nested subheadings before the next top-level section. Those are strong structural signs that deep material was inlined instead of referenced.
  - **Advisory portion:** warn when `Entry Instructions` exceeds a conservative bullet or length budget, or when it repeats many explicit reference paths already listed in `References`.
  - **Exact mechanical proxy or heuristic:** extract the `Entry Instructions` section and:
    1. hard-fail if it contains ``````, a table header like `| ... |`, or headings `### ` / `#### `
    2. advisory if it has more than 5 top-level bullets, more than ~900 characters, or mentions 3+ reference paths that also appear in the `References` table
  - **Biggest false-positive risk:** some honest compact skills may legitimately need 6 short bullets or a longer-than-average entry surface without actually collapsing progressive disclosure.
  - **Smallest honest next step:** implement only the structural hard-fail now; keep the density thresholds advisory until at least a few adopter-owned skills exist outside the shipped examples.

- **Final recommendation:** implement partial + keep partial wording downgrade ready.
  - Hard-fail now:
    1. stronger structural trigger checks for check 2
    2. conservative runtime-claim/degradation-family checks for check 4
    3. obvious progressive-disclosure collapse checks for check 5
  - Keep advisory for:
    1. true trigger usefulness/specificity scoring
    2. deep semantic matching between runtime claim and degradation text
    3. entry-instruction density judgments
  - If the doc wants the stronger original wording to remain literal hard-fail truth, another narrow round is still needed; otherwise the doc should be ready to downgrade those semantic tails to advisory language.

---

## Main-Thread Synthesis — Round 1

- Decision: partial-implement
- Confidence: High
- Next action: keep the implemented structural subset, observe it through real usage, and only shrink the remaining semantic wording if later evidence shows the unresolved tail cannot be made trustworthy.

### Summary

This round converged on a bounded implementation plan rather than a second broad redesign. The honest move was not “hard-fail everything the doc says” and not “give up and shrink immediately”. The usable outputs converged on a middle path: hard-fail the structural subset of checks 4 and 5 now, add advisory coverage for check 2 and entry-instruction density, and keep the semantic tail available for future narrowing only if real usage proves the remaining promises cannot be mechanized honestly.

### Rationale

The newly implemented validator path now reflects the strongest overlap across the executors: runtime-capability claims in `Entry Instructions` must carry a matching degradation path; `Entry Instructions` may not inline fenced code, markdown tables, or nested subheadings; short trigger bullets and over-dense entry surfaces are warned on rather than overclaimed as semantic hard-fails. Codex and GitHub Copilot CLI both supported this partial-implement route directly. Claude aligned on advisory-only for check 2 and a hard structural subset for checks 4 and 5. Gemini was more conservative on checks 2 and 4, but still aligned that only a bounded structural subset is trustworthy today.

### Follow-Up Questions

- After at least one adopter cycle, does the weak-trigger advisory produce clean enough signal to promote any subset into hard-fail?
- Do future skill surfaces need an explicit structured runtime-dependency field, or is the current entry-instructions-plus-degradation check sufficient?
