# No Placeholder Runtime Claims

- ID: no-placeholder-runtime-claims
- Type: guardrail
- Owner: framework-maintainers
- Review Threshold: dual-reviewer

## Purpose

Prevent agents from shipping placeholder runtime paths, fake smoke claims, or misleading live-surface assertions into active docs and user-facing closeout artifacts.

## Triggers

### Positive Triggers

- Use when the task edits runtime guidance, health checks, smoke paths, user-surface maps, or other docs that describe what currently works in a live or runtime-adjacent flow.

### Negative Triggers

- Do not use for pure discussion artifacts, historical archives, or speculative design notes that are explicitly not active runtime truth.

### Expected Effect

- The agent verifies that active docs only claim live behavior backed by real commands, receipts, or declared runtime evidence, and blocks placeholder wording from being treated as current truth.

## Entry Instructions

- Prefer explicit `none`, declared stop rules, or scoped caveats over invented runtime stories.
- Treat active runtime docs as truth sources, not brainstorming space.
- If a runtime path cannot be verified honestly, record the blocker instead of upgrading the claim.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| runtime surface protection | docs/RUNTIME_SURFACE_PROTECTION.md | yes | Guard-registry pattern and placeholder regression policy |
| active docs audit | scripts/active_docs_audit.py | yes | Executable checks for nonportable or stale active-doc assertions |
| closeout truth audit | scripts/closeout_truth_audit.py | no | Receipt-anchor enforcement for truth-source closeout claims |

## Governance

### Allowed Evidence

- Reproducible audit failures.
- Human-reviewed root-cause notes tied to false runtime claims.
- Closeout receipts showing mismatch between claimed and verified runtime behavior.

### Reviewer Gate

- All normative changes require explicit maintainer review because this is a guardrail skill.

### Forbidden Direct Update Inputs

- Auto-rewriting the skill from successful runs alone.
- Frequency-only heuristics that weaken the guardrail because a phrase appears often.
- Adapter-specific behavior redefining what counts as live proof.

## Degradation

- If a runtime cannot be exercised in the current environment, the skill falls back to blocking the claim, recording the blocker, and preserving explicit uncertainty in the user-facing truth source.

## Validator Notes

- This skill should never imply that missing runtime evidence can be replaced by stylistic confidence.