# Discussion Packet — copilot_instructions_format_review_v1

- Generated at: 2026-04-07T22:22:50.936754+00:00
- Owner: main-thread
- Current round goal: Obtain an implementation-ready review of .github/copilot-instructions.md itself
- Round exit rule: Freeze a plan, narrow to a sharper second round, or stop on missing truth

## Decision Question

How should this repository improve .github/copilot-instructions.md with respect to file-format correctness, writing quality, rule overlap or conflict, and overall maintainability?

## Why This Needs Discussion

The Rule 4-7 region in .github/copilot-instructions.md was recently repaired after a structural corruption. Before making further edits, we want a fresh 4-CLI review of the file as it exists now: whether the markdown format is still problematic, whether the writing is规范 and internally consistent, whether some rules conflict or can be merged, and what concrete improvements would raise clarity and maintainability.

## Current Truth

- The file now has continuous Rule headings from Rule 0 through Rule 27.
- The previously corrupted Rule 4-7 region was repaired: Rule 6 was restored, malformed tables were fixed, and list structure is valid again.
- The file is intentionally long and now includes anti-drift additions such as progress receipts, drift packets, and state-sync rules.
- The current review target is the file itself, not the whole framework.

## Constraints

- Focus on the current file content, not hypothetical future repos.
- Distinguish formatting or markdown-structure issues from content or policy issues.
- Be specific about any conflicts, redundancy, merge opportunities, naming issues, or readability problems.
- Do not suggest deleting important governance just to make the file shorter.
- Prefer concrete, shippable edits over vague style advice.

## Candidate Directions

1. Keep the file mostly as-is and only do minor cleanup.
2. Refactor specific overlapping rules or duplicated clauses while preserving intent.
3. Split some content into referenced docs or appendices while keeping the top-level rule set authoritative.
4. Reorganize sections for readability without changing policy substance.
5. Combine 2, 3, and 4 asymmetrically where useful.

## Evaluation Criteria

1. Is the markdown structure valid and resilient?
2. Is the writing style internally consistent and easy to follow?
3. Are any rules redundant, conflicting, or awkwardly split?
4. Would a new agent misread or overlook important obligations because of file shape?
5. What is the smallest high-value improvement set?

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

## Feedback — Round 1 — Codex CLI

- Timestamp: 2026-04-07T22:28:57.675055+00:00
- Stance: targeted-refactor
- Summary: The file is no longer structurally broken, but response-shape rules, checkpoint-task rules, and acceptance/closeout rules are fragmented across too many sections.

### Strengths

- Continuous Rule 0-27 headings and repaired markdown structure are stable.
- Rule 20, Rule 22, Rule 25, and Rule 27 remain high-value governance anchors.

### Risks

- Rule 8 vs Rule 14 overlap on reply-ending requirements.
- Checkpoint-task obligations are duplicated across Rules 3, 4, 5, 7, 18, 20, and 21.
- Rule 21 says "five conditions" while listing four.

### Open Questions

- Should reply-shape obligations live in one rule or stay split between status formatting and decision logic?
- Should checkpoint mechanics be centralized in Rule 18 or Rule 20?

### Recommended Next Step

- Fix concrete integrity issues first.
- Then centralize the checkpoint contract and reply-shape contract.

---

## Feedback — Round 1 — Gemini CLI

- Timestamp: 2026-04-07T22:28:57.786467+00:00
- Stance: targeted-refactor
- Summary: The markdown format is mostly stable now, but anti-drift clauses were copy-pasted across multiple rules, creating redundancy and navigation cost.

### Strengths

- Rule 8 closeout formatting is crisp and unambiguous.
- Rule 22 remains strong on observable acceptance criteria.
- The tables are generally easy to parse.

### Risks

- Checkpointed long-task clauses are repeated across Rules 3, 4, 5, 7, and 8.
- Rules 1, 2, and 12 overlap around pre-action safety checks.
- Rule 27 references EC §1 without a clear in-file definition.
- Rule 7 still has a visually awkward floating paragraph.

### Open Questions

- Should the safety gate be collapsed into one rule?
- Should the checkpoint and drift clauses move under Rule 18 or Rule 20?

### Recommended Next Step

- Consolidate repeated anti-drift/checkpoint requirements into one authoritative section.
- Align audit terminology with the execution boundary concept.

---

## Feedback — Round 1 — GitHub Copilot CLI

- Timestamp: 2026-04-07T22:28:57.895266+00:00
- Stance: targeted-refactor
- Summary: The current file shape is serviceable, but there are still real conflicts around autonomy vs ask-before-proceed, plus the dispatch and closeout lifecycle is spread too widely.

### Strengths

- Rule numbering continuity is now strong.
- Rule 15 decomposition logic and Rule 25 receipt anchoring are especially solid.
- The document can be improved without a wholesale rewrite.

### Risks

- Rule 22 asks the agent to stop for missing success conditions, which conflicts with Rule 20 autonomous execution posture.
- Rule 11 low-confidence wording is not fully aligned with Rule 20.
- Completion and closeout obligations are fragmented across Rules 8, 9, 14, 17, 22, 25, and 26.
- Rule 6 mixes document classes and execution artifacts in one taxonomy table.

### Open Questions

- Should completion, alignment, and closeout be regrouped into a single lifecycle cluster?
- Should Rule 7 be narrowed to session_state and reset semantics only?

### Recommended Next Step

- Fix the explicit contradictions and count mismatch first.
- Then regroup dispatch and closeout rules into cleaner clusters.

---

## Feedback — Round 1 — Claude CLI

- Timestamp: 2026-04-07T22:28:58.005851+00:00
- Stance: no-output
- Summary: The Claude CLI command exited without producing stdout or stderr content, so this round has no usable Claude opinion.

### Strengths

- none

### Risks

- The round effectively contains three substantive external reviews and one empty result.
- Any claimed 4-CLI consensus should be described as 3 convergent reviews plus 1 no-output run.

### Open Questions

- none

### Recommended Next Step

- Proceed with synthesis using the three convergent reviews and record the empty Claude run as a workflow note.

---

## Main-Thread Synthesis — Round 1

- Timestamp: 2026-04-07T22:28:58.115757+00:00
- Decision: targeted-refactor
- Confidence: high
- Next action: If the repository wants a follow-up edit pass, apply a narrow cleanup patch: fix the explicit contradictions first, then centralize repeated checkpoint and response-shape clauses.

### Summary

- Consensus from Codex, Gemini, and Copilot is strong: the file is no longer structurally broken, but it remains overly fragmented.
- The highest-value work is not a rewrite; it is a consolidation pass over duplicated checkpoint, reply-shape, dispatch, and closeout rules.
- Three concrete defects surfaced repeatedly: Rule 21 count mismatch, terminology drift around execution boundary / execution contract, and autonomy wording conflicts across Rules 20, 22, and 11.

### Rationale

- All three substantive reviewers independently landed on targeted-refactor rather than freeze-as-is or full restructure.
- They converged on the same risk pattern: policy fragmentation now matters more than raw markdown validity.
- Preserving the current governance depth while reducing duplication is the lowest-risk path because the repaired structure is already usable.

### Follow-Up Questions

- Should checkpoint mechanics be centralized under Rule 18 or Rule 20?
- Should progress/alignment/closeout rules stay separate or be regrouped into one lifecycle cluster?
