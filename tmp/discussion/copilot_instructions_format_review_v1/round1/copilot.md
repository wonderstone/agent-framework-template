● Read discussion_packet.md
  │ tmp/discussion/copilot_instructions_format_review_v1/discussion_packet.md
  └ 66 lines read

● Read session_state.md
  └ 122 lines read

● Inspect instruction file size and headings (shell)
  │ wc -l .github/copilot-instructions.md && rg -n '^## |^---$|^## Rule '
  │ .github/copilot-instructions.md | sed -n '1,220p'
  └ 62 lines...

I’ve got the packet and the current file shape. Next I’m reading the instruction file in chunks so I can separate actual format issues from policy overlap and navigation problems.

● Read copilot-instructions.md
  │ .github/copilot-instructions.md
  └ L1:220 (220 lines read)

● Read copilot-instructions.md
  │ .github/copilot-instructions.md
  └ L221:450 (230 lines read)

● Read copilot-instructions.md
  │ .github/copilot-instructions.md
  └ L701:950 (249 lines read)

● Read copilot-instructions.md
  │ .github/copilot-instructions.md
  └ L951:1235 (285 lines read)

● Read copilot-instructions.md
  │ .github/copilot-instructions.md
  └ L451:700 (250 lines read)

The file is structurally much better than a broken draft, but I’m seeing a few concrete consistency issues now rather than raw markdown corruption. I’m checking repetition hot spots so I can rank the refactors by payoff instead of just calling it “too long.”

● Search (grep)
  │ "task packet|handoff packet|drift packet|progress receipt|Execution Boundary|Next
  │ Actions|UAC|closeout|session_state\.md" (.github/copilot-instructions.md)
  └ 1 file found

● Search (grep)
  │ "verify all five conditions|At task intake|ask before proceeding|Low-confidence rule|Inside a
  │ declared execution boundary|do not trigger host closeout actions at internal batch boundaries"
  │ (.github/copilot-instructions.md)
  └ 9 lines found

● Search (grep)
  │ "main thread|main-thread|main thread owner review|main-thread owner review"
  │ (.github/copilot-instructions.md)
  └ 16 lines found

● Search (grep)
  │ "^### " (.github/copilot-instructions.md)
  └ 1 file found

Verdict: targeted-refactor

Findings

| priority | category | issue | why it matters | recommended fix |
|---|---|---|---|---|
| P1 | conflict | Rule 22 says “If the user has not specified success conditions: ask before proceeding,” but Rule 20 makes autonomous multi-step execution the default and treats interruption as a last resort. | This is a real behavioral conflict, not just style. Different agents could legitimately choose opposite actions on the same task. | Rewrite Rule 22 so missing UAC defaults to “derive provisional UAC from the request, mark assumptions explicitly, and only stop when the gap is material or irreversible.” |
| P2 | maintainability | The dispatch/executor workflow is spread across Rules 5, 15, 18, 19, 21, and 26. | The policy is understandable only after hopping across six rules. That increases misreads and makes future edits risky because one change can silently desync the rest. | Keep Rule 15 as the strategy layer, but create one contiguous “dispatch pipeline” block or checklist that covers packet -> executor selection -> terminal states -> evaluation, then reduce the other rules to short, non-repetitive references. |
| P3 | maintainability | Completion/closeout obligations are fragmented across Rules 8, 9, 14, 17, 22, 25, and 26. | The file repeats the same lifecycle idea in slightly different words: don’t close out early, show status, prove acceptance, anchor completion, get evaluation. The repetition makes the file feel heavier than it is and makes conflicts harder to spot. | Build a single “definition of done / closeout ladder” subsection and let the surrounding rules reference it instead of restating closeout conditions. |
| P4 | format | Rule 21 says “verify all five conditions,” but the readiness table contains only four conditions. | This is a concrete integrity bug in the current file. It undermines trust because readers cannot tell whether a condition is missing or the count is wrong. | Either change “five” to “four” or add the missing fifth condition. |
| P5 | overlap | Rule 7 carries session-state rules, rollover, context reset, receipts, handoff behavior, drift behavior, hard gates, and Git closeout handoff. | Rule 7 no longer reads like one rule; it reads like a mini-manual. Its scope overlaps materially with Rules 9, 18, 20, 24, and 25. | Narrow Rule 7 to cross-session state and context reset only. Move receipt/handoff/drift/Git-closeout obligations to their owning rules and leave short cross-references here. |
| P6 | writing | Rule 11 says low-confidence action must be surfaced “to the user first,” but the same rule and Rule 20 allow proceeding inside the execution boundary with `Alignment: uncertain`. | The intent is recoverable, but the wording is not internally clean. “Surface first” and “proceed, then flag” are different operational orders. | Change the wording to something like “must be surfaced at the next allowed progress boundary; irreversible low-confidence decisions still hard-stop.” |
| P7 | format | Rule 6’s table mixes document classes with execution artifacts, and the “Location” column is not semantically consistent. | TYPE-A/B/C are document-placement concepts, while progress receipts and drift packets are workflow artifacts with timing semantics. That makes the table harder to scan and maintain. | Split Rule 6 into two tables: “Document types” and “Execution artifacts.” |
| P8 | writing | Rule 8’s output templates switch abruptly into mixed Chinese/English labels without an explicit convention note. | It is technically valid, but readers may not know whether bilingual output is required, preferred, or just an example. That hurts predictability for future maintainers. | Add one sentence explaining that the labels are intentional built-in markers, or standardize the templates to one language and say localized equivalents are allowed. |
| P9 | maintainability | The standalone italic reference block between Rules 17 and 18 interrupts the rule flow. | It is not wrong, but it looks like a floating appendix fragment rather than part of the main structure. That makes navigation feel less disciplined than the rest of the file. | Move those three lines to the top preamble, a short “Core truth surfaces” note, or an appendix-style footer. |

Merge opportunities

- Rules 5 + 15 + 19 + 21 + 26: merge into a clearer “Dispatch and execution pipeline” structure. Keep strategy decisions separate from runtime mechanics, but place them adjacently so the reader can follow one flow.
- Rules 8 + 14 + 17 + the closeout parts of 9/25: consolidate into a single “Progress, alignment, and closeout” flow. Right now the same end-of-task logic is repeated in multiple voices.
- Rules 4 + 22 + 23: treat these as one stack: technical validation -> user acceptance -> toolchain prerequisite. They already form a dependency chain and would read better as one sequence.
- Rule 7 + parts of 18 + 24: reduce duplication by making Rule 7 own `session_state.md` and context reset, while Rule 18 owns task/audit/handoff packets and Rule 24 owns leftovers.

Keep-as-is

- The file’s top-level rule numbering and section continuity from Rule 0 to Rule 27 are now strong and should not be casually rearranged.
- Rule 15’s decomposition test and serial-exemption framing are clear and operationally useful.
- Rule 22’s concrete UAC examples, especially for doc/config/template work, are high-value and should stay.
- Rule 25’s receipt-anchor concept is sharp, memorable, and materially improves truthfulness.
- Rule 27’s policy-audit table is a good summary surface and should remain as a compact audit entry point.

Final recommendation

The file no longer looks structurally broken; the main problems are now policy overlap, a few real inconsistencies, and lifecycle rules being split across too many sections. I would not freeze it as-is, but I also would not do a wholesale rewrite: the highest-value move is a targeted refactor that preserves the rule set while regrouping related obligations and fixing the explicit contradictions. Start with the concrete integrity fixes first: Rule 21’s count mismatch, Rule 22 vs Rule 20, and Rule 11 vs Rule 20. After that, collapse the dispatch cluster and the closeout cluster into cleaner flows, because that will improve readability more than line-by-line copyediting.

