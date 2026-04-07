# SKILL Harvest Loop V1 Draft

This document defines the formal v1 design draft for the framework's post-task SKILL harvest and promotion-governance loop.

It exists to turn the discussion in `tmp/discussion/skill_harvest_loop_v1/discussion_packet.md` into a concrete contract that templates, validators, and future promotion receipts can implement without reopening the whole workflow question each time.

---

## Design Status

| Field | Value |
|---|---|
| Status | Draft v1 |
| Scope | Post-task candidate extraction, delegated review boundaries, and canonical promotion authority for SKILL files |
| Depends on | `docs/SKILL_MECHANISM_V1_DRAFT.md`, `docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md`, discussion packets, receipt-anchored closeout, and validator surfaces |
| Already changes | field-authority expectations for skill templates, examples, validators, and future promotion receipts |
| Does not yet change | packaged distribution format, installer behavior, lockfile semantics, or a fully implemented promotion-state registry |

Normative note:

when this document says a field authority is `human-only`, `delegated-reviewed`, or `delegated-safe`, it means the canonical SKILL contract must declare that authority in a human-authored schema surface rather than letting the harvester, reviewer, or adapter infer it at runtime.

---

## Purpose

The framework already has a canonical SKILL contract and a field-level receipt and review matrix.

What it still needs is a trustworthy mechanism for turning finished-task and execution-side evidence into candidate skill improvements without collapsing into direct transcript-to-skill mutation.

This design defines that mechanism.

Its purpose is to:

1. separate candidate extraction from canonical promotion
2. freeze field-level promotion authority in a human-authored contract
3. allow delegated review for bounded classes of change
4. make silent prompt drift visible, auditable, and stoppable

---

## Core Decision

The v1 framework should use a per-field `promotion_tier` table attached directly to the canonical SKILL contract.

The framework should not use:

1. section-level mutable zones as the primary authority model
2. a hybrid section-plus-override model as the default authority surface

Decision rationale:

1. the existing SKILL contract already treats six canonical fields as the load-bearing unit of truth
2. validator checks, receipts, and review rules already bind naturally to those fields
3. section-level authority is easier to game through content reshuffling and creates a second taxonomy the framework does not need

---

## Promotion Authority Model

The authority model is intentionally small.

It uses one closed enum:

| `promotion_tier` | Meaning |
|---|---|
| `delegated-safe` | delegated review may approve the change without human escalation when the field's evidence and review rules are satisfied |
| `delegated-reviewed` | delegated review may review and recommend, but cumulative drift controls and stricter evidence checks apply |
| `human-only` | direct human approval is required before canonical mutation |

The initial default assignment for the six canonical fields is:

| Field | Default `promotion_tier` | Why |
|---|---|---|
| `purpose` | `human-only` | it defines skill identity and intent |
| `triggers` | `human-only` | trigger expansion silently changes invocation scope |
| `entry_instructions` | `delegated-reviewed` | normative behavior can be tuned, but only with stronger review and drift checks |
| `references` | `delegated-safe` | support artifacts can grow faster if truthfulness remains intact |
| `governance` | `human-only` | the system must not delegate edits to its own authority rules |
| `degradation` | `delegated-reviewed` | fallback behavior is important but can evolve under explicit evidence and review |

Design rule:

the `promotion_tier` table itself is a constitutional surface.

Normal harvest or promotion flows may consume it, but they must not mutate it.

---

## Canonical Artifacts

The v1 loop keeps artifacts separate by authority level.

| Artifact | Purpose | Canonical? |
|---|---|---|
| closeout receipt | proves the task ended in a real observed condition with receipt-bearing evidence | no |
| candidate packet | proposes a field-scoped change from receipt-bearing evidence | no |
| promotion receipt | records which canonical fields changed, under which authority, and why | yes |

Candidate packets are not canonical truth.

Promotion receipts are canonical evidence that a canonical mutation was explicitly approved.

---

## Validator Contract

The validator should hard-fail the structural truth layer first.

### Hard-Fail Checks

The first implementation layer should hard-fail when:

1. a skill file's receipt and review matrix omits the `promotion_tier` column
2. a skill file omits one of the six canonical field rows from that matrix
3. a non-template skill row uses an unsupported `promotion_tier` value
4. a non-template skill classifies `governance` as anything other than `human-only`
5. a promotion-oriented artifact claims canonical mutation without naming its affected canonical fields

### Advisory Checks

The first implementation layer may keep these advisory until a later phase:

1. cumulative drift across many individually valid `delegated-reviewed` updates
2. evidence-quality disputes where structure is valid but the claim remains semantically weak
3. rate-limit or anti-bloat heuristics for delegated-safe lanes
4. whether a repository wants an external promotion-state registry rather than a purely receipt-driven history

Design rule:

the validator should not pretend to solve semantic governance by itself.

Its job is to keep the authority model explicit and mechanically queryable.

---

## Migration Boundary

The minimal migration from the current v1 SKILL surface is:

1. add `promotion_tier` to the existing receipt and review matrix rather than creating a new governance section
2. update the canonical skill draft and the template to expose that column
3. update examples and validators to consume the same six-field authority map
4. defer richer promotion-state registries or drift counters to a later follow-up once the field authority table is stable in real use

This keeps the first implementation wave additive.

It changes the governance contract without forcing repositories to redesign the shape of their skill files.

---

## Current Decision Summary

The framework should model SKILL promotion authority as a human-authored per-field table attached to the existing canonical SKILL contract.

It should allow delegated review for bounded fields, require direct human approval for constitutional fields, and keep candidate extraction separate from canonical mutation.