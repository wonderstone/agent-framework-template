# SKILL Mechanism V1 Draft

This document defines the formal v1 design draft for the framework's `SKILL` mechanism.

It exists to turn the discussion in `tmp/discussion/skill_mechanism_v1/discussion_packet.md` into a concrete framework-level contract that later template, bootstrap, validator, and adapter work can follow.

This is a design draft. It freezes the canonical framework-native contract and its governance boundaries before broader implementation or packaging work.

---

## Design Status

| Field | Value |
|---|---|
| Status | Draft v1 |
| Scope | Framework-level skill contract and governance model |
| Depends on | strategy-versus-mechanism split, discussion packets, validation surfaces, receipt-anchored closeout |
| Already changes | design expectations for future skill templates, validators, and adapter surfaces |
| Does not yet change | packaged distribution format, lockfile semantics, vendor-specific installer behavior, or a field-level receipt matrix |

Normative note:

when this document says a field is `required in v1`, it means:

the field is part of the target v1 contract that future template, bootstrap, and validation work should implement.

It does not mean every future validator or bootstrap surface is already enforced today.

---

## Purpose

The framework already has strong surfaces for discussion, validation, audit receipts, and execution recovery.

What it does not yet define formally is how a repository should model a reusable skill without collapsing into vendor-specific prompt files or unreviewed prompt drift.

`SKILL` fills that gap.

Its purpose is to give repositories a durable, reviewable mechanism for:

1. declaring when a skill should be invoked
2. separating minimal entry instructions from deeper supporting context
3. recording what evidence may improve the skill over time
4. preserving portability while being honest about runtime-specific limitations

This surface is complementary to role strategy, discussion loops, and developer-toolchain design. It is not a replacement for those surfaces.

---

## Core Design Decision

The framework freezes a hybrid direction:

1. the canonical truth is a framework-native skill contract
2. vendor-specific skill formats remain adapter layers
3. packaging and distribution remain outer layers, not the design center of v1

Decision rationale:

1. the framework should own the durable contract, not a single vendor syntax
2. adapters should consume canonical truth, not define it
3. packaging is useful, but it should follow truthful local contracts instead of substituting for them

---

## v1 Design Goals

The v1 contract should be:

1. small enough that repositories can adopt it honestly
2. strong enough that invocation is not left to vague intuition
3. explicit about review and update boundaries
4. portable across agents at the contract layer, even when runtime features differ
5. compatible with progressive disclosure instead of forcing full skill payloads into every session

The v1 contract should not require repositories to invent a marketplace, package registry, or universal hook story.

---

## Skill Types

The framework distinguishes these first-class skill types in v1:

| Type | Primary purpose |
|---|---|
| `knowledge` | Supply durable domain knowledge or reference guidance |
| `workflow` | Shape a repeatable execution sequence or working method |
| `verification` | Drive checks, validation order, or proof expectations |
| `guardrail` | Prevent specific unsafe, misleading, or policy-breaking behavior |

Design rule:

the type is not decorative metadata.

it influences how strict update policy should be, especially for `guardrail` skills.

---

## Canonical V1 Contract

### Required Core Fields

These fields are required in v1.

| Field | Meaning |
|---|---|
| `id` | Stable unique skill identifier |
| `type` | One of `knowledge`, `workflow`, `verification`, or `guardrail` |
| `purpose` | One sentence describing the behavior change the skill is meant to produce |
| `triggers` | Explicit invocation conditions, including at least one positive trigger and one negative trigger |
| `entry_instructions` | Minimal normative instructions safe to load by default |
| `references` | Named supporting artifacts used for progressive disclosure |
| `governance` | Evidence policy, reviewer threshold, and ownership metadata |
| `degradation` | Honest fallback behavior when runtime-specific features are unavailable |

Design rule:

every field after `id` and `type` is load-bearing.

`governance` and `degradation` are part of the normative contract, not advisory notes.

### Field Intent

| Field | v1 intent |
|---|---|
| `purpose` | Why the skill exists and what behavioral lift it should create |
| `triggers` | When to invoke the skill and when not to invoke it |
| `entry_instructions` | The source of truth for default invoked behavior |
| `references` | Pointers to deeper files such as scripts, examples, setup notes, gotchas, or validation details |
| `governance` | Which evidence sources may propose changes and what review threshold is required |
| `degradation` | What changes when hooks, tool gating, context forking, or other runtime affordances do not exist |

### Required Trigger Contract

The trigger contract must include:

1. at least one positive trigger
2. at least one explicit negative trigger
3. the expected effect of invocation

Design rule:

without a negative trigger, the framework cannot reason honestly about collision risk or over-invocation.

---

## Progressive Disclosure Rule

Progressive disclosure is a first-class design goal in v1.

The canonical rule is:

1. `entry_instructions` contains the minimum truthful normative payload
2. deeper examples, scripts, setup steps, and gotchas live in referenced artifacts
3. hidden details must be named explicitly when the skill depends on them

Additional rule:

a reference is not truly optional if the skill silently relies on it for correct execution.

If omitted context is mandatory, the entry surface must say so.

The framework treats silent dependency on hidden files as a design failure, not a style preference.

---

## Evidence And Update Policy

Declared skills are not automatically trustworthy forever.

The design therefore distinguishes between:

1. evidence that may propose change
2. review that may approve change
3. canonical fields that must not mutate silently

### Evidence Ranking

The default v1 evidence order is:

| Tier | Evidence source | Trust level |
|---|---|---|
| 1 | Human-authored postmortems, root-cause notes, reproducible failure analysis, closeout audits tied to receipts | Highest |
| 2 | Operator-authored gotchas with explicit provenance | High |
| 3 | Structured invocation receipts and failure-pattern aggregates | Medium |
| 4 | Auto-collected telemetry and agent-proposed observations | Low |
| 5 | Raw transcripts, transcript summaries, and frequency-only heuristics | Lowest |

### Receipt Anchor Rule

Any proposal to change a canonical skill field must point to at least one receipt-bearing artifact.

Valid first-pass receipt anchors include:

1. root-cause notes tied to a reproducible failure
2. closeout audits tied to a concrete batch of work
3. structured invocation receipts with explicit provenance

The receipt does not need to approve the change by itself.

It does need to prove that the proposal came from a real observed condition rather than free-form preference drift.

### Default Review Rule

Evidence may propose.

Humans approve.

Adapters consume.

### Normative Update Boundary

Human review is required before any change to:

1. `purpose`
2. `triggers`
3. `entry_instructions`
4. `governance`
5. `degradation`

Additional rule:

`guardrail` skills require the strictest policy in v1.

No automatic proposal path may directly rewrite their normative fields.

### Forbidden Direct Update Inputs

These must not directly update the canonical skill:

1. raw transcripts
2. model-generated transcript summaries
3. frequency-only heuristics without failure evidence
4. adapter-layer drift flowing back into the core contract without explicit review

These inputs may inform a reviewer, but they must not become self-executing rewrite sources.

## Field-Level Receipt And Review Matrix

The canonical v1 follow-up question is now frozen into the design itself.

Each canonical field uses the following default matrix:

| Field | Proposal evidence tiers | Minimum reviewer threshold | Guardrail override |
|---|---|---|---|
| `purpose` | 1-2 only | `single-reviewer` | `dual-reviewer`; no auto-proposed rewrite |
| `triggers` | 1-3 | `single-reviewer` | `dual-reviewer`; no auto-proposed rewrite |
| `entry_instructions` | 1-3 | `single-reviewer` | `dual-reviewer`; no auto-proposed rewrite |
| `references` | 1-4 | `single-reviewer` | `single-reviewer`; must keep reference truthfulness |
| `governance` | 1-2 only | `dual-reviewer` | `dual-reviewer`; owner review required |
| `degradation` | 1-3 | `single-reviewer` | `dual-reviewer`; owner review required |

Matrix rule:

1. a lower-trust evidence tier may add a candidate note, but it may not directly justify a canonical field change beyond the row's allowed tier range
2. `references` is the most flexible field because it often grows through examples or support files, but even there the reference must remain truthful and reviewable
3. `governance` and `degradation` are not metadata-only fields; they use stricter review because they change how the skill can evolve and how it behaves under capability gaps
4. every `guardrail` skill applies its override column even when a repository uses a looser default elsewhere

---

## Validator Contract

Validators should enforce the truthful mechanical layer, not pretend to score semantic elegance.

### Hard-Fail Checks

The v1 validator contract should hard-fail when:

1. required core fields are missing or empty
2. trigger conditions are too weak to be actionable
3. a named reference does not resolve to an existing artifact
4. runtime-specific behavior is claimed without a matching degradation declaration
5. `entry_instructions` inlines what should remain in referenced artifacts and collapses progressive disclosure

### Advisory Checks

The v1 validator contract should keep these advisory:

1. prose quality
2. style or tone preferences
3. taxonomy elegance
4. gotcha breadth or example richness
5. broad usefulness claims that cannot yet be proven mechanically

Design rule:

the validator should prove contract truthfulness, not fake deep semantic certainty.

---

## Portability And Honest Degradation

The framework distinguishes between core portable semantics and adapter-only capabilities.

### Core Portable Layer

These should remain portable at the contract layer:

1. identity
2. type
3. purpose
4. trigger semantics
5. entry instructions
6. reference structure
7. governance policy

### Adapter Layer

These remain adapter-specific in v1:

1. vendor-native skill manifest formats
2. hook execution
3. tool gating
4. subagent or context-fork execution
5. package install or update channels
6. lockfile or publish semantics

### Degradation Rule

If an adapter capability is absent, the skill must declare one of these outcomes:

1. manual fallback behavior
2. advisory-only execution
3. explicit refusal to invoke

Implied parity across runtimes is not allowed.

---

## Implementation Boundary

This design draft freezes the framework-level contract now, but it does not yet require every downstream implementation layer to ship at once.

The next likely implementation steps are:

1. a canonical skill template surface
2. validator support for the hard-fail and advisory checks defined here
3. one or more repository-local starter examples covering at least two skill types
4. a later follow-up on the field-level receipt and review matrix

That receipt and review matrix is now defined at the design level, but downstream templates and validators still need to consume it consistently.

Open follow-up boundary:

the remaining implementation work is no longer deciding the matrix. It is making sure future templates, validators, and adapter surfaces enforce it consistently.

---

## Biggest Risk To Avoid

The primary failure mode is governance theater:

a repository can appear to have a formal skill system while actually allowing low-scrutiny evidence, adapter drift, or hidden support files to mutate normative behavior over time.

The purpose of this design is to make that drift visible, reviewable, and stoppable.

---

## Relationship To The Rest Of The Framework

This document complements the rest of the framework like this:

1. `docs/STRATEGY_MECHANISM_LAYERING.md` keeps role strategy separate from skill mechanism
2. `docs/runbooks/multi-model-discussion-loop.md` provides the durable discussion path that produced this design draft
3. `docs/DOC_FIRST_EXECUTION_GUIDELINES.md` explains when repositories should freeze a durable design surface before implementation
4. future validators, templates, and bootstrap surfaces should consume this draft rather than inventing vendor-first skill rules

---

## Current Decision Summary

The v1 framework should standardize a small framework-native skill contract, keep vendor syntax and package mechanics outside the canonical core, require human review for all normative field changes, and make honest degradation mandatory whenever runtime features differ.