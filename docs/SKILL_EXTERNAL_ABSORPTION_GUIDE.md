# External Skill Absorption Guide

This document defines how the framework should absorb useful external skill ecosystems without importing their host-specific assumptions wholesale.

It exists because external projects are now influencing the framework's own SKILL direction, but the framework still needs a clear rule for what becomes canonical, what becomes an adapter, and what stays outside the core contract.

---

## Design Status

| Field | Value |
|---|---|
| Status | Draft v1 |
| Scope | How the framework absorbs external skill and workflow ideas into canonical local surfaces |
| Depends on | `docs/SKILL_MECHANISM_V1_DRAFT.md`, `docs/SKILL_FIVE_PATTERN_EXECUTION_PLAN_V1.md`, and `docs/STRATEGY_MECHANISM_LAYERING.md` |
| Already changes | which external ideas are now treated as first-class local surfaces versus inspiration only |
| Does not yet change | validator enforcement, bootstrap output, or installer behavior beyond the assets added in this repository |

Normative note:

external inspiration does not become framework truth by popularity alone.

It becomes framework truth only when the repository can restate it as a local contract with honest triggers, references, governance, and degradation.

---

## Purpose

The framework already defines a canonical SKILL contract and a strategy-versus-mechanism split.

What it needed next was a rule for external ecosystems that are clearly useful but arrive with very different packaging models:

1. standalone skills
2. MCP-backed tool adapters
3. full workflow plugins
4. host-specific orchestration stacks
5. narrow autonomous experiment harnesses

This guide freezes the absorption rule so future work does not confuse inspiration, adapter integration, and canonical skill surfaces.

---

## Core Rule

Absorb behavior, not brands.

The framework should import only the reusable behavior change that can be expressed honestly in local contract form.

It should not import:

1. host-specific installation assumptions as framework law
2. product packaging as if it were the skill contract itself
3. a second truth surface that duplicates session state, packets, receipts, or validator ownership

---

## Absorption Tiers

| Tier | Meaning | Examples |
|---|---|---|
| `first-class skill` | The behavior can be restated as a local skill with stable triggers and honest degradation | `frontend-design` |
| `adapter-backed skill` | The behavior depends on an external tool or MCP surface, but the invocation rule can still be local | `context7-docs` |
| `mechanism extraction` | The external project is too broad to import directly, but specific workflow patterns should be absorbed into local runbooks or future skills | `Superpowers`, `gstack`, `autoresearch` |
| `explicitly excluded` | The external system conflicts with the framework's truth surfaces or would duplicate existing state machinery | `Task Master AI` |

---

## Adoption Decisions

### 1. Frontend Design

Decision: absorb as a first-class skill.

Why:

1. its behavior is local and reusable
2. its triggers are clear and bounded to frontend work
3. it strengthens user-visible output quality without requiring a host-specific runtime

Local surface shipped now:

1. `.github/skills/frontend-design/SKILL.md`

Framework rule:

the absorbed skill must preserve an existing design system when one exists; its job is to improve quality, not to force arbitrary redesign.

### 2. Context7

Decision: absorb as an adapter-backed skill, not as a pure prompt skill.

Why:

1. the valuable behavior is version-sensitive documentation retrieval
2. the underlying capability is external and tool-backed
3. the local framework still needs a canonical rule telling agents when to prefer fresh docs over memory

Local surface shipped now:

1. `.github/skills/context7-docs/SKILL.md`

Framework rule:

Context7-backed guidance is authority for upstream APIs, not for repository-local behavior.

### 3. Superpowers

Decision: absorb selected workflow guardrails only.

Absorbed ideas:

1. plan or design approval can be a real hard gate before implementation
2. implementation plans should contain concrete validation steps rather than vague intent
3. independent review after execution is a first-class workflow stage, not optional polish

Do not absorb directly:

1. Claude-specific packaging
2. plugin-specific slash-command taxonomy
3. any assumption that its workflow is the framework's only planning model

Landing tier:

1. mechanism extraction into future runbook and skill refinements

### 4. gstack

Decision: absorb selected methodology patterns only.

Absorbed ideas:

1. skill routing should be explicit rather than magical
2. per-project learnings are useful when they stay bounded and attributable
3. global install versus repo-vendoring is an architectural choice that should stay outside the canonical skill contract

Do not absorb directly:

1. gstack's host-install paths as framework law
2. its session directories or state layout as canonical framework truth
3. its complete startup-operating-system as a drop-in framework replacement

Landing tier:

1. mechanism extraction into future routing, memory, and installer discussions

### 5. autoresearch

Decision: absorb the bounded autonomous-loop pattern, not the research harness.

Absorbed ideas:

1. one mutable surface is often safer than open-ended file editing
2. a fixed metric and keep-or-revert loop can make long-running autonomy honest
3. explicit stop, timeout, and revert rules are more reusable than domain-specific ML content

Do not absorb directly:

1. the single-GPU LLM training harness itself
2. domain-specific assumptions about `train.py`, `prepare.py`, or `val_bpb`
3. indefinite execution claims unless the host and validation surfaces can support them honestly

Landing tier:

1. mechanism extraction into future autonomous-loop runbooks or bounded workflow skills

### 6. Task Master AI

Decision: explicitly excluded from the current framework core.

Why:

1. it is a separate task system, not a narrow skill contract
2. it would duplicate the framework's existing truth surfaces for state, packets, receipts, and closeout
3. adopting it into the core now would create competing task authorities

Framework rule:

Task Master AI may be evaluated later as an optional external integration, but it is not part of the current canonical skill layer.

---

## Mapping To Framework Layers

| External source | Local landing layer | Current state |
|---|---|---|
| `frontend-design` | canonical skill | shipped |
| `Context7` | adapter-backed skill | shipped |
| `Superpowers` | workflow guardrail extraction | documented |
| `gstack` | routing and learnings extraction | documented |
| `autoresearch` | bounded autonomous-loop extraction | documented |
| `Task Master AI` | excluded from core | documented |

---

## Design Rules For Future External Inputs

When evaluating a future external skill, plugin, or orchestration stack:

1. identify whether it is a skill, adapter, mechanism bundle, or independent product
2. map it to one absorption tier before adding any files
3. refuse any integration that creates a second canonical truth surface without an explicit adapter boundary
4. prefer a thin local restatement over vendoring external branding and host-path assumptions
5. require honest degradation whenever the external capability is not guaranteed in the local host

---

## Current Deliverables

This absorption round ships these concrete local surfaces:

1. `.github/skills/frontend-design/SKILL.md`
2. `.github/skills/context7-docs/SKILL.md`
3. `docs/runbooks/design_gated_bounded_autonomy.md`
4. `templates/design_gated_bounded_autonomy_packet.template.md`
5. this TYPE-A guide as the canonical boundary for future external skill absorption

> Updated 2026-05-04: froze the current external adoption boundary. `frontend-design` and `Context7` are now first-class absorbed local surfaces; the extracted `Superpowers`, `gstack`, and `autoresearch` patterns now land in a shipped runbook plus reusable packet template; `Task Master AI` remains excluded from the framework core.