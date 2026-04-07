# Developer Toolchain Wrapper Starter

- ID: developer-toolchain-wrapper-starter
- Type: workflow
- Owner: framework-maintainers
- Review Threshold: single-reviewer

## Purpose

Bind one skill invocation to one declared Developer Toolchain surface so wrapper behavior stays explicit, inspectable, and receipt-friendly.

## Triggers

### Positive Triggers

- Use when a task should call a declared toolchain surface such as Diagnostics, Health or smoke, Repro path, or Build through a repeatable skill entrypoint.

### Negative Triggers

- Do not use when the work is exploratory and has not yet chosen a concrete toolchain surface or when the task would need hidden runtime behavior not declared in the project adapter.

### Expected Effect

- The skill invocation names one real toolchain surface, records the input boundary and evidence shape, and stops honestly when the adapter says the surface is unavailable or untrusted.

## Entry Instructions

- Bind exactly one declared Developer Toolchain row from `.github/instructions/project-context.instructions.md` before execution starts.
- Wrapper Target Surface: a named surface such as Diagnostics, Health or smoke, Repro path, or Build.
- Declared Input Boundary: the file path, module path, CLI arguments, or packet scope handed to the surface.
- Output Or Evidence Shape: exit code, log lines, generated artifact, or invocation receipt link expected from a successful run.
- Fallback Or Stop Rule: stop when the surface is `known-broken` or `not-applicable`; otherwise use the declared fallback from the project adapter.
- Invocation Receipt Linkage: record the wrapper outcome in a closeout receipt or `templates/skill_invocation_receipt.template.md` derived artifact when runtime lineage matters.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| developer toolchain design | docs/DEVELOPER_TOOLCHAIN_DESIGN.md | yes | Defines what counts as a declared toolchain surface |
| project context adapter | .github/instructions/project-context.instructions.md | yes | Provides the actual command, status, and fallback for the bound surface |
| invocation receipt template | templates/skill_invocation_receipt.template.md | no | Receipt surface when wrapper use should create execution lineage |

## Governance

### Allowed Evidence

- Receipt-bearing closeout artifacts showing wrapper success, fallback, or repeated failure.
- Maintainer-reviewed corrections when a wrapper claims runtime power the adapter does not declare.

### Reviewer Gate

- Changes to triggers, wrapper boundary labels, or fallback rules require maintainer review.

### Forbidden Direct Update Inputs

- Hidden shell conventions not declared in the adapter.
- Wrapper expansions that invent new toolchain surfaces without updating the project context.

## Receipt And Review Matrix

| Field | Proposal evidence tiers | Minimum reviewer threshold | Guardrail override | Promotion tier |
|---|---|---|---|---|
| `purpose` | `1-2 only` | `single-reviewer` | `dual-reviewer`; no auto-proposed rewrite | `human-only` |
| `triggers` | `1-3` | `single-reviewer` | `dual-reviewer`; no auto-proposed rewrite | `human-only` |
| `entry_instructions` | `1-3` | `single-reviewer` | `dual-reviewer`; no auto-proposed rewrite | `delegated-reviewed` |
| `references` | `1-4` | `single-reviewer` | `single-reviewer`; must keep reference truthfulness | `delegated-safe` |
| `governance` | `1-2 only` | `dual-reviewer` | `dual-reviewer`; owner review required | `human-only` |
| `degradation` | `1-3` | `single-reviewer` | `dual-reviewer`; owner review required | `delegated-reviewed` |

## Degradation

- If the selected toolchain surface is unavailable, marked `known-broken`, or only exists as undeclared local lore, stop and record the missing wrapper contract instead of silently substituting a different runtime path.

## Validator Notes

- Wrapper starters should name one concrete surface and one concrete fallback rule.
- Wrapper text should not imply that an undeclared tool or hidden runtime path is safe to call.