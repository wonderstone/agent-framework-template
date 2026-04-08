## Verdict: `targeted-refactor`

The file is structurally valid and the recent repair held. The issues are localized — two verbatim duplications, one misplaced bullet, one orphaned footer block, and one unresolved coexistence question between two mandatory end-of-reply requirements.

---

## Findings Table

| # | Pri | Category | Issue | Why It Matters | Recommended Fix |
|---|---|---|---|---|---|
| 1 | P1 | format | **Orphaned footer** (~line 630–634): 3 italic reference lines + `---` sitting between Rule 17 and Rule 18, outside any rule heading | Breaks the `## Rule N` + `---` separator pattern; maintainers inserting a new rule will be confused | Move to the very bottom of the file, after Rule 27 |
| 2 | P1 | overlap | **Verbatim duplicate**: checkpointed `Active Work` field list appears identically in Rule 3 (line 50) and Rule 7 (line 119) | Two copies will silently diverge on the next edit | Remove from Rule 3; add cross-ref: "For `Active Work` fields in checkpointed tasks, see Rule 7." |
| 3 | P1 | format | **Misplaced bullet in Rule 7 Context Reset Protocol** (~line 153): "The task packet must name `Progress Unit`…" is inside the context-reset trigger list but is a task-packet requirement, not a trigger | Agents will treat it as a reset trigger — wrong behavior | Move to Rule 4 or Rule 18; remove or replace with a genuine trigger |
| 4 | P1 | overlap | **Rule 4 items 4–6** ("do not trigger host closeout actions…; reserve final closeout for the declared true boundary") duplicate the Long-Loop Non-Closeout Rule in Rule 8 verbatim | Same policy in two places; one will drift | Replace Rule 4 items 4–6 with: "For checkpoint emission and closeout boundaries during long tasks, see Rule 8." |
| 5 | P2 | conflict | **Rule 8 (status line) vs Rule 14 (Next Actions)**: both mandate end-of-reply content with no coexistence statement | Agents randomly apply one or double-footer | Add one sentence to Rule 14: both are required; status line = compact machine form, Next Actions = structured decision record |
| 6 | P2 | writing | **Rule 7 is too long** (~80 lines, 4 distinct procedures): base rule + Rollover Triggers + Rollover Procedure + Context Reset Protocol | An agent parsing Rule 7 for one question must process four unrelated procedures | Extract Context Reset Protocol into a clearly separated subsection with its own `---` break |
| 7 | P2 | maintainability | **No table of contents** for 28 rules / 1200+ lines | Cross-refs like "see Rule 15" require a full-file search | Add compact ToC after the preamble blockquote: `Rule N — Title — [mandatory/on-demand]` |
| 8 | P2 | writing | **Rule 5 partial deferral to Rule 15**: Rule 5 says "see Rule 15 for full decomposition" then adds two extra checkpointed-task bullets not in Rule 15 | Reader must consult both rules for completeness | Move the two bullets into Rule 15 under "Checkpoint obligations"; leave Rule 5 as a pure pointer |
| 9 | P3 | overlap | **Rule 12 "absorbs Rule 0"** (stated inline) but Rule 0 still stands with no mutual cross-reference | Agents may apply both gates independently | Add a note in Rule 0: "The mechanical gate is in Rule 12 Step 2. Rule 0 governs challenge posture; Rule 12 governs pre-action sequence." |
| 10 | P3 | maintainability | **Rule 27 has two parallel tables** (Audit Output Format code block + Dimension Evaluation Guide table) for the same 8 dimensions | Two edits required per rule change → silent divergence | Merge into one table with `✅ / ⚠️ / ❌` condition columns; reduce the code block to a template stub |

---

## Merge Opportunities

- **Rule 3 item 4 → delete, cross-ref Rule 7** (checkpointed Active Work fields)
- **Rule 4 items 4–6 → delete, cross-ref Rule 8** (closeout boundary governance)
- **Rule 5 checkpoint bullets → move to Rule 15** (Rule 5 becomes a pure pointer)
- **Rule 27 two tables → one merged table** (same 8 dimensions, overlapping columns)
- **Rule 0 / Rule 12 → mutual cross-refs** (not a merge; audiences differ, but relationship needs documentation)

---

## Keep-As-Is

- **Rule 8 bilingual status line format** — intentional, consistent, do not change
- **Rule 20 Execution Boundary Declaration code fence** — precise and machine-readable
- **Rule 21 Terminal State Contract** (DONE/STUCK/ESCALATE) — clean, enumerated, no overlap
- **Rule 22 UAC valid/invalid table** — genuinely useful distinction, do not shorten
- **Rule 25 "what counts / does not count"** — important, keep verbatim
- **Rule 26 Three-Role Model table** — Evaluator constraint is actionable and correct
- **`🔴 Mandatory` / `🔵 On-Demand` header badges** — consistent and scannable, retain on all rules

---

## Final Recommendation

The file does not need restructuring — it needs five localized edits. The highest-value work is: (1) move the orphaned footer to the file's end, (2) remove the verbatim Rule 3/Rule 7 duplication, (3) fix the misplaced context-reset bullet in Rule 7, (4) replace the duplicated closeout governance in Rule 4 items 4–6 with a Rule 8 cross-reference, and (5) add a coexistence sentence to Rule 14 so the Rule 8 status line and Next Actions block are unambiguous. Adding a table of contents is the highest single-ROI maintainability improvement given the 28-rule span. None of these changes touch policy substance — they are structural deduplication and navigation edits only.
