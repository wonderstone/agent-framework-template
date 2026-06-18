# Huashu Design

- ID: huashu-design
- Type: workflow
- Owner: framework-maintainers
- Review Threshold: single-reviewer

## Purpose

Turn huashu-design requests into reusable, audience-scoped, channel-aware copy systems instead of one-off dense prose.

## Triggers

### Positive Triggers

- Use when a task asks for huashu, sales copy, poster wording, advisor script blocks, campaign messaging, or replaceable marketing-language modules.
- Use when a user wants the wording to stay swappable across brands, products, rates, contacts, or channels.
- Use when visual composition and copy density need to be designed together.

### Negative Triggers

- Do not use for legal approval, compliance review, or factual verification of product claims by itself.
- Do not use for backend-only, data-only, or infrastructure-only work.
- Do not use when the request is a normal documentation task with no reusable huashu or message-design component.

### Expected Effect

- The output is organized into reusable message layers rather than a single dense paragraph.
- Primary value points, optional support copy, and replaceable slots are explicitly separated.
- The resulting huashu matches the intended delivery surface such as poster, landing hero, advisor DM, QR card, or phone-share asset.

## Entry Instructions

- Capture the audience, product, channel, and required placeholders before writing.
- Keep the primary selling line short and visually compatible with the destination layout.
- Reduce supporting copy until the main offer is readable in one fast scan.
- Mark compliance, approval, or factual-claim gaps explicitly instead of pretending huashu design certifies them.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| huashu capability contract | docs/HUASHU_DESIGN_CAPABILITY.md | yes | Defines the capability boundary and reusable output shape |
| huashu runbook | docs/runbooks/huashu_design.md | yes | Supplies the step sequence and packet fields for execution |
| huashu briefing template | templates/huashu_design_brief.template.md | no | Gives a durable brief shape for repeated requests |
| skill mechanism design | docs/SKILL_MECHANISM_V1_DRAFT.md | no | Governs trigger discipline, governance, and degradation expectations |

## Governance

### Allowed Evidence

- accepted campaign or poster tasks that reuse the same huashu structure successfully
- before or after copy comparisons showing improved clarity, density, or replaceability
- operator feedback that identifies repeated message-design failure modes

### Reviewer Gate

- copy-structure refinements may use single-reviewer promotion
- any change that widens the skill into compliance signoff, claim validation, or universal product policy requires maintainer review

### Forbidden Direct Update Inputs

- one-off slogans promoted into general workflow policy without context
- legal, compliance, or approval language copied back as if huashu design owns those decisions
- channel-specific hacks promoted into universal structure without evidence

## Receipt And Review Matrix

| Field | Proposal evidence tiers | Minimum reviewer threshold | Guardrail override | Promotion tier |
|---|---|---|---|---|
| `purpose` | `1-2 only` | `single-reviewer` | `dual-reviewer` if the scope widens beyond huashu design | `human-only` |
| `triggers` | `1-3` | `single-reviewer` | `dual-reviewer` if the skill starts claiming compliance or validation authority | `human-only` |
| `entry_instructions` | `1-3` | `single-reviewer` | `single-reviewer`; keep placeholder discipline and density control intact | `delegated-reviewed` |
| `references` | `1-4` | `single-reviewer` | `single-reviewer`; reference truthfulness required | `delegated-safe` |
| `governance` | `1-2 only` | `single-reviewer` | `dual-reviewer` for reviewer-threshold changes | `human-only` |
| `degradation` | `1-3` | `single-reviewer` | `single-reviewer`; cannot hide missing approval or claim-verification surfaces | `delegated-reviewed` |

## Degradation

- If the audience or delivery surface is unclear, degrade into a brief-first mode and request or infer only the smallest missing fields.
- If the task depends on legal, compliance, or factual-claim approval, stop short of certification and mark those gaps explicitly.
- If no design preview is available for a visual asset, keep the copy shorter than normal and state the layout assumptions clearly.
- If the asset must be reusable across brands or offers, degrade into placeholder-safe copy rather than hard-coding live values.