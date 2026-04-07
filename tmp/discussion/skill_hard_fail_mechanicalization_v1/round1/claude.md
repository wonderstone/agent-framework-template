Here is my analysis and recommendation, structured to match the required output shape from the discussion packet.

---

## Verdict: PARTIAL-IMPLEMENT

---

## Check 2 — Trigger Conditions Too Weak To Be Actionable

**Current state**: The existing validator (lines 1060–1068 in `validate_template.py`) only requires that each trigger subsection has at least one `- ` bullet. A bullet reading `- Use when applicable.` passes.

**Recommended enforcement shape**: Advisory, not hard-fail.

**Whether to hard-fail, advisory, or split**: Advisory only. No syntactic proxy can reliably distinguish a genuinely concise trigger from a vacuous one without semantic reading.

**Exact mechanical proxy**:
```python
# In collect_advisories(), for each skill file:
# Extract each bullet in ### Positive Triggers and ### Negative Triggers
# If any bullet text (after stripping "- ") is shorter than 25 characters:
#   emit advisory "weak-skill-trigger-bullet"
```
The 25-char threshold catches `- Use when needed.` (18 chars) while sparing `- Use when the lint surface status is unknown.` (46 chars).

**Biggest false-positive risk**: A short but legitimately specific trigger like `- Use when the hook fires.` (26 chars) just clears the bar. Any shorter and you're into genuinely vacuous territory. Risk is low but non-zero. This is why it stays advisory.

**Smallest honest next step**: Implement as `collect_advisories` entry. After one real-world adoption cycle with zero false positives across the example set, promote to hard-fail in a follow-up patch. If it keeps firing false positives, shrink the doc wording in `SKILL_MECHANISM_V1_DRAFT.md` from "hard-fail when trigger conditions are too weak" to an advisory clause.

---

## Check 4 — Runtime-Specific Behavior Claimed Without Matching Degradation

**Recommended enforcement shape**: Hard-fail, scoped to `## Entry Instructions` only.

**Whether to hard-fail, advisory, or split**: Hard-fail. The signal is trustworthy when scoped correctly.

**Exact mechanical proxy**: Two-part check:

1. Scan only the `## Entry Instructions` section for a conservative runtime keyword set:
   ```python
   SKILL_RUNTIME_KEYWORDS = {
       "hook", "tool gating", "subagent", "context fork",
       "context isolation", "vendor-specific", "auto-trigger",
   }
   ```
2. If any keyword is found, check that `## Degradation` section contains at least one word from:
   ```python
   SKILL_DEGRADATION_VOCABULARY = {
       "fallback", "fall back", "unavailable", "absent", "block",
       "downgrade", "advisory", "refusal", "refuse", "stop",
       "cannot", "explicit",
   }
   ```
   If degradation section is absent or contains none of these → `ValidationIssue("skill-runtime-claim-without-degradation", ...)`.

All six real examples pass today: every degradation section uses at least one of these words. The template file is already gated by `is_template`.

**Biggest false-positive risk**: Scoping to `## Entry Instructions` only (not the whole document) eliminates the main risk. If "hook" appears only in a governance note ("Changes to hook behavior require review"), it won't trigger the check. The remaining risk is a skill that mentions "hook" in entry instructions but has a genuinely short, honest degradation sentence that happens to avoid the vocabulary list. The vocabulary list is broad enough (`stop`, `cannot`, `explicit`) that this is unlikely.

**Smallest honest next step**: Add `_check_skill_runtime_degradation_consistency(text, relative, is_template)` inside `_validate_skill_contract_files`, call it per skill file, add tests with a synthetic skill that has `hook` in entry_instructions but an empty degradation section.

---

## Check 5 — entry_instructions Inlines Content and Collapses Progressive Disclosure

**Recommended enforcement shape**: Split — one hard-fail, one advisory.

**Whether to hard-fail, advisory, or split**: Split.

**Exact mechanical proxies**:

**Hard-fail (high confidence)**:
```python
entry_section = _extract_markdown_section(text, "Entry Instructions")
if entry_section and "```" in entry_section and not is_template:
    issues.append(ValidationIssue("skill-entry-instructions-inlines-content", ...))
```
A fenced code block in `entry_instructions` means content that belongs in a referenced script or example has been inlined. This is definitionally wrong by the progressive disclosure rule. False-positive risk: essentially zero.

**Advisory (lower confidence)**:
If the entry_instructions section character count exceeds 600 characters, emit `"skill-entry-instructions-too-long"`. All six real examples are well under this (ranging ~150–350 chars). Eight or more bullet lines is a secondary advisory proxy.

Do NOT implement a semantic check for "this content should be in a reference." That requires NLP and is not trustworthy.

**Biggest false-positive risk**: For the hard-fail (code block): almost none. For the advisory (length): a five-pattern skill with verbose but structurally legitimate bullets could approach 600 chars. Keep the length check advisory until real adopter data firms up the threshold.

**Smallest honest next step**: Code block detection goes into `_validate_skill_contract_files` immediately. Length advisory goes into `collect_advisories`. Tests: code block → hard-fail, 10 bullets → advisory, all current examples → clean pass.

---

## Final Recommendation

**Implement partial now, keep downgrade option ready for Check 2.**

| Action | What |
|---|---|
| Ship as hard-fail now | Check 4 (`skill-runtime-claim-without-degradation`), Check 5 code-block (`skill-entry-instructions-inlines-content`) |
| Ship as advisory now | Check 2 (`weak-skill-trigger-bullet`, < 25 chars), Check 5 length (`skill-entry-instructions-too-long`, > 600 chars) |
| Do not ship yet | Any NLP scoring, full-document runtime keyword scanning, positive/negative trigger similarity check |
| Downgrade path if Check 2 fails | After one adoption cycle, if the advisory keeps false-positiving: shrink doc wording in `SKILL_MECHANISM_V1_DRAFT.md` from "hard-fail" to "advisory" for this check. That is the honest fallback — validator truth over doc theater. |

No new discussion round needed. The implementation scope is bounded, testable, and fits within the existing `_validate_skill_contract_files` + `collect_advisories` structure without redesigning the contract.
