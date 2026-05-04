# Frontend Design

- ID: frontend-design
- Type: workflow
- Owner: framework-maintainers
- Review Threshold: single-reviewer

## Purpose

Produce distinctive, production-grade frontend interfaces without falling back to generic AI-generated aesthetics.

## Triggers

### Positive Triggers

- Use when a task asks for a landing page, dashboard, marketing site, prototype, web component, design-system surface, or a visual polish pass on an existing UI.
- Use when a task explicitly asks for better visual design, stronger typography, more intentional motion, or a less generic frontend result.
- Use when a frontend task needs a concrete visual direction before implementation begins.

### Negative Triggers

- Do not use for backend-only, API-only, database-only, or infrastructure-only work.
- Do not use when the task is primarily about product copy, business rules, or documentation rather than the UI itself.
- Do not use to overwrite an established design system; when a repository already has a stable visual language, preserve it and apply this skill only as a quality bar.

### Expected Effect

- The agent chooses and states a visual direction before implementation.
- The resulting UI uses deliberate typography, color, spacing, layout, and motion choices instead of interchangeable defaults.
- The implementation stays real, responsive, and testable rather than stopping at decorative mockup prose.

## Entry Instructions

- Choose one explicit visual direction before implementation.
- Preserve an existing design system; improve precision and polish instead of imposing a foreign style.
- Avoid generic AI defaults and prefer a few strong design moves over weak decoration.
- Keep the output responsive and, when possible, validate the rendered result before closeout.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| external absorption guide | docs/SKILL_EXTERNAL_ABSORPTION_GUIDE.md | yes | Explains why this skill is a first-class absorbed surface rather than an imported external dependency |
| skill mechanism design | docs/SKILL_MECHANISM_V1_DRAFT.md | no | Governs trigger discipline, governance, and degradation expectations |
| repository frontend rules | .github/copilot-instructions.md | no | Supplies the repo-default frontend quality bar this skill should honor |

## Governance

### Allowed Evidence

- user-visible before or after comparisons
- accepted UI tasks that demonstrate a repeatable quality lift
- bug reports or reviews that identify generic, sloppy, or system-breaking frontend output

### Reviewer Gate

- Trigger or quality-bar refinements may use single-reviewer promotion.
- Any change that widens the skill into non-frontend work or weakens design-system preservation rules requires maintainer review.

### Forbidden Direct Update Inputs

- vague taste-only requests with no user-visible outcome
- one-off aesthetic preferences promoted into universal policy
- adapter-specific marketplace wording copied back into the canonical skill without review

## Receipt And Review Matrix

| Field | Proposal evidence tiers | Minimum reviewer threshold | Guardrail override | Promotion tier |
|---|---|---|---|---|
| `purpose` | `1-2 only` | `single-reviewer` | `dual-reviewer` if the skill broadens beyond frontend work | `human-only` |
| `triggers` | `1-3` | `single-reviewer` | `dual-reviewer` if trigger wording weakens design-system preservation | `human-only` |
| `entry_instructions` | `1-3` | `single-reviewer` | `single-reviewer`; cannot silently reintroduce generic default aesthetics | `delegated-reviewed` |
| `references` | `1-4` | `single-reviewer` | `single-reviewer`; reference truthfulness required | `delegated-safe` |
| `governance` | `1-2 only` | `single-reviewer` | `dual-reviewer` for reviewer-threshold changes | `human-only` |
| `degradation` | `1-3` | `single-reviewer` | `single-reviewer`; cannot weaken honesty about visual-proof limits | `delegated-reviewed` |

## Degradation

- If no browser, screenshot, or live preview surface is available, keep the change bounded and state the unverified visual assumptions explicitly.
- If required fonts or assets are unavailable, use the closest available substitute while preserving the declared direction.
- If the repository already enforces a design system, degrade into system-preserving mode instead of inventing a new aesthetic.
- If the task is too small for a full design pass, apply the minimum useful lift: spacing, hierarchy, typography, and responsiveness first.