**Verdict**

`PARTIAL-IMPLEMENT`

**Check 2: trigger conditions are too weak to be actionable**

- Recommended enforcement shape: split into a very small hard-fail floor plus an advisory vagueness lint.
- Enforcement level: split.
- Exact mechanical proxy or heuristic: hard-fail only on obvious structural non-actionability in `### Positive Triggers` and `### Negative Triggers`:
  `1.` no bullets
  `2.` any bullet is placeholder-like (`[... ]`, `TBD`, `todo`, `example`, `sample`)
  `3.` any bullet lacks a conditional marker such as `when`, `if`, or `unless`
  `4.` positive and negative bullets normalize to the same text after lowercasing and stripping `use/do not use/not`
  `5.` any bullet is trivially short, e.g. fewer than 5 words
  Keep broader “too vague” detection advisory only, using a denylist like `appropriate`, `helpful`, `useful`, `relevant`, `as needed`, `best judgment`, `sometimes`.
- Biggest false-positive risk: domain-specific but valid triggers can be concise or use unusual phrasing without `when/if/unless`.
- Smallest honest next step: add only the placeholder/conditional/collision/short-bullet hard-fails first and phrase the rest as advisory.

**Check 4: runtime-specific behavior is claimed without a matching degradation declaration**

- Recommended enforcement shape: implement for an explicit capability-family list, not for all “runtime-ish” prose.
- Enforcement level: split, with a real hard-fail subset.
- Exact mechanical proxy or heuristic: scan all sections except `## Degradation` and `## References` for capability-family markers derived from the doc itself:
  `hook`, `tool gating`, `subagent` / `sub-agent`, `context fork` / `context isolation`, `package install`, `update channel`, `lockfile`, `publish`.
  If any family is claimed outside degradation, hard-fail unless `## Degradation` contains:
  `1.` an unavailability marker such as `if`, `when unavailable`, `absent`, `missing`, `cannot`
  `2.` an outcome marker such as `fallback`, `manual`, `advisory-only`, `refuse`, `stop`, `downgrade`, or `block`
  `3.` ideally the same capability family token or mapped alias.
  Missing `1` or `2` should be hard-fail. Missing `3` should be advisory unless the family vocabulary is tightly controlled.
- Biggest false-positive risk: a skill may mention a capability only to forbid it, or may have a truthful generic degradation that does not repeat the same token family.
- Smallest honest next step: start with the explicit portability/degradation vocabulary already named in `docs/SKILL_MECHANISM_V1_DRAFT.md` and add tests around one positive and one negative case per family.

**Check 5: `entry_instructions` inlines what should remain in referenced artifacts and collapses progressive disclosure**

- Recommended enforcement shape: enforce only structural collapse, not semantic “this belongs in references” judgment.
- Enforcement level: split.
- Exact mechanical proxy or heuristic: hard-fail `## Entry Instructions` only when it clearly stops being a minimal entry surface:
  `1.` contains a table
  `2.` contains fenced code
  `3.` contains nested headings
  `4.` exceeds a conservative size cap, e.g. more than 5 bullets or more than 220 words
  `5.` contains numbered procedural steps across many lines, e.g. 6+ `1.` / `2.` style items
  Keep “too much detail relative to references” advisory-only, for example when entry instructions are much larger than the references block or repeat many reference-path details.
- Biggest false-positive risk: some honest skills may need 6 concise bullets or a slightly longer entry surface without actually collapsing disclosure.
- Smallest honest next step: implement only the structural caps that all shipped examples already satisfy, and tune the thresholds from current examples before widening.

**Final recommendation**

Implement partial + keep partial wording downgrade ready.

Check 4 has a trustworthy hard-fail subset now. Check 5 has a trustworthy structural hard-fail subset now. Check 2 does not support a truthful full hard-fail without pretending to understand prose quality, so it should be split and documented that way unless the contract wording is narrowed to the structural floor.
