# Huashu Design Capability

TYPE-A: long-lived capability contract for huashu design work.

## Why This Exists

Huashu requests often arrive as loose wording tweaks, but the repeatable value is not the exact sentence. The reusable value is the structure: audience, offer, visual density, channel fit, and replaceable slots.

This capability exists to make huashu work reviewable, reusable, and safe to absorb into the framework as a first-class surface.

## Capability Boundary

This capability owns:

- huashu structure for posters, landing sections, advisor handoff copy, and campaign message blocks
- editable placeholder discipline for names, logos, rates, contacts, and offer variants
- copy-density control for visual or phone-share assets
- message layering: primary line, secondary support, optional proof, and operator-only notes

This capability does not own:

- legal approval
- compliance signoff
- factual verification of financial or market claims
- brand governance beyond what the task explicitly supplies

## Required Inputs

Minimum packet for a truthful huashu pass:

1. target audience
2. product or offer
3. delivery surface
4. required placeholders
5. must-keep constraints such as brand voice, language, or disclosure requirements

## Default Output Shape

1. primary message layer
2. secondary support line
3. optional alternative block
4. CTA block
5. contact block
6. explicit placeholder inventory

## Capability Assets

- `.github/instructions/huashu-design.instructions.md`
- `.github/skills/huashu-design/SKILL.md`
- `docs/runbooks/huashu_design.md`
- `templates/huashu_design_brief.template.md`

## Validation Standard

The capability is only considered wired when adopters can bootstrap these assets, reference them from the repository, and keep them inside manifest-backed `expected_files` truth.

## Degradation

- If the audience is unknown, keep the draft brief-first and label assumptions.
- If the channel is unknown, choose the smallest safe copy blocks and avoid over-writing long paragraphs.
- If compliance-sensitive claims appear, mark them as approval-dependent instead of final.

> Updated 2026-06-02: added the initial formal capability skeleton for huashu design.