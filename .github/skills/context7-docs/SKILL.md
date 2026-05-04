# Context7 Docs

- ID: context7-docs
- Type: knowledge
- Owner: framework-maintainers
- Review Threshold: single-reviewer

## Purpose

Retrieve fresh, version-sensitive third-party library documentation before code generation or configuration guidance relies on stale model memory.

## Triggers

### Positive Triggers

- Use when a task depends on external library or framework APIs, setup steps, migration details, or configuration syntax.
- Use when the user asks for help with a specific package and version-sensitive correctness matters.
- Use when the agent would otherwise rely on remembered docs for React, Next.js, FastAPI, Tailwind, SDKs, or similar third-party surfaces.

### Negative Triggers

- Do not use for repository-local behavior that should be learned from the checked-out codebase.
- Do not use for pure architecture, product, or business-logic questions that do not require third-party API truth.
- Do not use when the task already names a local canonical doc or source file that is the correct authority.

### Expected Effect

- The agent resolves the exact library or framework it is discussing.
- External API guidance becomes version-aware and documentation-backed.
- The agent distinguishes upstream library truth from repository-local conventions instead of mixing them together.

## Entry Instructions

- Prefer Context7 or an equivalent version-specific doc source before answering third-party API, setup, or configuration questions from memory.
- Resolve the library identity first, then fetch only the topic needed for the current task.
- Keep documentation retrieval narrow and progressive rather than dumping broad manuals into context.
- Treat upstream docs as authority for external APIs, but keep repository-local files as authority for local behavior.
- If Context7 is unavailable, fall back to official upstream docs or repo-pinned vendor docs and state the degradation honestly.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| external absorption guide | docs/SKILL_EXTERNAL_ABSORPTION_GUIDE.md | yes | Explains why Context7 is absorbed as an adapter-backed documentation surface |
| skill mechanism design | docs/SKILL_MECHANISM_V1_DRAFT.md | no | Governs canonical skill boundaries and degradation rules |
| developer toolchain discussion | docs/DEVELOPER_TOOLCHAIN_DISCUSSION.md | no | Frames documentation and diagnostics as first-class agent inputs |

## Governance

### Allowed Evidence

- reproducible cases where stale model memory caused wrong setup or API guidance
- successful version-sensitive doc lookups that improved task correctness
- maintainer-reviewed adapter notes for supported documentation backends

### Reviewer Gate

- Query-shaping and fallback refinements may use single-reviewer promotion.
- Any change that turns this skill into a general web-search skill or weakens the distinction between upstream docs and local source requires maintainer review.

### Forbidden Direct Update Inputs

- generic web search results treated as canonical without source discrimination
- repository-local facts rewritten from upstream docs
- marketplace copy pasted into the canonical skill without maintainer review

## Receipt And Review Matrix

| Field | Proposal evidence tiers | Minimum reviewer threshold | Guardrail override | Promotion tier |
|---|---|---|---|---|
| `purpose` | `1-2 only` | `single-reviewer` | `dual-reviewer` if the skill broadens beyond external docs retrieval | `human-only` |
| `triggers` | `1-3` | `single-reviewer` | `dual-reviewer` if trigger wording blurs local-vs-upstream authority | `human-only` |
| `entry_instructions` | `1-3` | `single-reviewer` | `single-reviewer`; cannot silently replace version-aware docs with memory-only guidance | `delegated-reviewed` |
| `references` | `1-4` | `single-reviewer` | `single-reviewer`; reference truthfulness required | `delegated-safe` |
| `governance` | `1-2 only` | `single-reviewer` | `dual-reviewer` for reviewer-threshold changes | `human-only` |
| `degradation` | `1-3` | `single-reviewer` | `single-reviewer`; cannot hide loss of version-sensitive truth | `delegated-reviewed` |

## Degradation

- If Context7 or an equivalent documentation adapter is unavailable, use official upstream docs or repo-pinned vendor docs and say that the answer was not Context7-backed.
- If the exact library version is unknown, state the version uncertainty instead of pretending the syntax is universal.
- If no trustworthy upstream documentation is reachable, stop at bounded guidance and label any remaining advice as unverified.