# SKILL Five-Pattern Discussion

Date: 2026-04-07
Scope: archive the completed multi-CLI discussion on how the template should absorb Google's five SKILL design patterns without regressing into abstraction drift.

---

## Summary

- The discussion concluded that the template should not absorb the five patterns as a new canonical SKILL taxonomy.
- The strongest candidates for absorption are `Tool Wrapper`, `Reviewer`, and `Pipeline`, and they should be absorbed as execution scaffolds only if they become bootstrap-shippable, validator-visible, and adopter-useful.
- `Generator` should remain bounded: either example-only or limited to narrow artifact-generation scaffolds such as packet or receipt generation.
- `Inversion` should remain deferred until the template can name a truthful host-runtime contract and degradation story.

---

## Source Packet

- Discussion packet: `tmp/discussion/skill_five_patterns_execution_adoption_v1/discussion_packet.md`

---

## Usable Executor Outcomes

| Executor | Result | Main stance |
|---|---|---|
| GitHub Copilot CLI | usable | absorb patterns asymmetrically; Wrapper, Reviewer, Pipeline as execution scaffolds; Generator bounded; Inversion deferred |
| Gemini CLI | usable | execution scaffolds only where they can be validated and immediately useful to adopters |
| Codex CLI | usable | reject new canonical taxonomy; Wrapper and Pipeline strongest; Generator narrow; Reviewer placement still debatable |
| Claude CLI | blocked | invoked twice but did not return a trustworthy non-interactive answer for this round |

---

## Convergence

All usable feedback converged on these points:

1. the current failure mode is abstraction drift, not missing pattern names
2. the canonical SKILL contract should stay constitutional rather than becoming a pattern catalog
3. pattern absorption should happen mostly below the canonical layer through helpers, wrappers, templates, validators, receipts, and examples
4. `Tool Wrapper` and `Pipeline` are the clearest first absorption targets
5. `Inversion` is not honest to ship yet

---

## Main Disagreements

The discussion only left two narrow disagreements:

1. whether `Reviewer` should become a first-class execution scaffold or remain attached to reviewer-role strategy plus audit machinery
2. whether `Generator` should remain example-only or be allowed to ship in a narrow artifact-generation form

These disagreements were judged small enough to freeze a staged plan without another broad discussion round.

---

## Frozen Direction

| Pattern | Frozen direction |
|---|---|
| `Tool Wrapper` | execution scaffold |
| `Reviewer` | execution scaffold candidate; narrower boundary still needed |
| `Pipeline` | execution scaffold |
| `Generator` | bounded and example-first |
| `Inversion` | defer |

Framework rule frozen by this round:

no pattern becomes a shipped template surface unless it has:

1. a concrete artifact or helper
2. a bootstrap or adoption path
3. validator-visible truth
4. an adopter-useful example or proof surface

---

## Durable Decisions

- Do not add a required pattern catalog or `pattern` field to the canonical SKILL contract.
- Treat pattern absorption as an execution-layer and adoption-surface problem before treating it as a governance-taxonomy problem.
- Require any absorbed pattern to become real in docs, templates, bootstrap, validator, and tests together.
- Record blocked executors honestly instead of treating missing output as consensus.

---

## Recommended Next Step

- Start a doc-first implementation wave that turns the frozen direction into a staged execution plan for Wrapper, Reviewer, Pipeline, bounded Generator, and deferred Inversion.