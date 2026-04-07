# Developer Toolchain Wrapper

- ID: developer-toolchain-wrapper
- Type: workflow
- Owner: framework-maintainers
- Review Threshold: single-reviewer

## Purpose

Bind a task to one declared Developer Toolchain surface so wrapper behavior stays truthful, auditable, and easy for adopters to reuse.

## Triggers

### Positive Triggers

- Use when the task should invoke a declared surface from `.github/instructions/project-context.instructions.md`, such as `Diagnostics`, `Health or smoke`, or `Repro path`.

### Negative Triggers

- Do not use when the repository has not declared the target surface yet or when the task is still deciding which runtime or module path is authoritative.

### Expected Effect

- The agent names the toolchain surface first, carries the exact scope into the command, and records the result as receipt-bearing execution evidence when the run matters to later closeout.

## Entry Instructions

- Wrapper Target Surface: one row such as `Diagnostics`, `Health or smoke`, or `Repro path` from the Developer Toolchain table in `.github/instructions/project-context.instructions.md`.
- Declared Input Boundary: the file set, module path, or runtime arguments handed to that row.
- Output Or Evidence Shape: the expected command output, log surface, or receipt path that proves the wrapper completed honestly.
- Fallback Or Stop Rule: if the row says `known-broken` or `not-applicable`, stop or follow the adapter's declared fallback instead of improvising.
- Invocation Receipt Linkage: when reuse evidence matters, tie the run to `templates/skill_invocation_receipt.template.md` or another receipt-bearing closeout artifact.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| project context adapter | .github/instructions/project-context.instructions.md | yes | Declares the available surfaces, statuses, and fallback rules |
| developer toolchain design | docs/DEVELOPER_TOOLCHAIN_DESIGN.md | yes | Explains why wrappers must stay tied to declared surfaces |
| invocation receipt template | templates/skill_invocation_receipt.template.md | no | Runtime evidence sink for repeated wrapper usage |

## Governance

### Allowed Evidence

- Closeout receipts tied to successful or failed wrapper runs.
- Maintainer-reviewed fixes when the wrapper points at a stale or misleading surface.

### Reviewer Gate

- Changes to wrapper semantics or fallback behavior require maintainer review.

### Forbidden Direct Update Inputs

- Hidden local shell habits promoted into the wrapper without adapter updates.
- Decorative pattern labels that are not tied to a real toolchain row.

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

- If the chosen toolchain row is missing or still design-only, block the wrapper claim and record the missing runtime contract instead of silently picking another path.

## Validator Notes

- Wrapper examples should mention a real adapter path and a real evidence sink.