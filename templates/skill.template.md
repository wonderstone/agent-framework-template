# Skill Contract Template

- ID: [skill-id]
- Type: [knowledge | workflow | verification | guardrail]
- Owner: [team or role]
- Review Threshold: [single-reviewer | dual-reviewer | owner-only]

> This template freezes the framework-native v1 SKILL contract. Keep the entry surface small, put deep detail in references, and do not let adapter-specific behavior redefine the canonical truth.

## Purpose

[One sentence describing the behavior change this skill should produce.]

## Triggers

### Positive Triggers

- [Use when this specific request, task phase, repo state, or failure mode is present.]

### Negative Triggers

- [Do not use when this nearby but different condition is present.]

### Expected Effect

- [What changes in planning, execution, or verification once this skill is invoked.]

## Entry Instructions

- [Minimal normative instructions safe to load by default.]
- [Keep this short and move setup, examples, scripts, and gotchas into references.]

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| [setup] | [path] | [yes / no] | [what deeper context this file provides] |

## Governance

### Allowed Evidence

- [Root-cause notes, receipts, or other approved evidence sources.]

### Reviewer Gate

- [Who must approve changes to purpose, triggers, entry instructions, governance, or degradation.]

### Forbidden Direct Update Inputs

- [Raw transcripts, model summaries, frequency-only heuristics, or other blocked sources.]

## Receipt And Review Matrix

| Field | Proposal evidence tiers | Minimum reviewer threshold | Guardrail override |
|---|---|---|---|
| `purpose` | [for example: 1-2 only] | [single-reviewer / dual-reviewer / owner-only] | [stricter rule for guardrail skills] |
| `triggers` | [for example: 1-3] | [single-reviewer / dual-reviewer / owner-only] | [stricter rule for guardrail skills] |
| `entry_instructions` | [for example: 1-3] | [single-reviewer / dual-reviewer / owner-only] | [stricter rule for guardrail skills] |
| `references` | [for example: 1-4] | [single-reviewer / dual-reviewer / owner-only] | [guardrail-specific reference rule] |
| `governance` | [for example: 1-2 only] | [single-reviewer / dual-reviewer / owner-only] | [stricter rule for guardrail skills] |
| `degradation` | [for example: 1-3] | [single-reviewer / dual-reviewer / owner-only] | [stricter rule for guardrail skills] |

## Degradation

- If [hook / tool gating / subagent / context isolation] is unavailable, [fallback or explicit refusal].

## Validator Notes

- Triggers should remain specific enough to distinguish nearby non-triggers.
- Entry instructions should not inline the full content of referenced files.
- If a reference is required for correct invocation, say so explicitly.