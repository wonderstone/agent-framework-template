# Windows Host Evaluation

- ID: windows-host-evaluation
- Type: workflow
- Owner: framework-maintainers
- Review Threshold: single-reviewer

## Purpose

Turn repository-specific Windows host evaluation packaging into a repeatable operator workflow for truthful host discovery, native Windows build policy, receipt capture, and receipt review.

## Triggers

### Positive Triggers

- Use when a task needs real Windows host onboarding before trusting a lifecycle or observation lane.
- Use when a repository already has runbooks, helper scripts, or receipt directories for Windows evaluation and the agent needs to turn them into one operator flow.
- Use when the task needs a truthful split between operator-confirmed values and agent-driven steps.
- Use when the agent must review operator receipts for naming/content honesty, blocker evidence, or historical-vs-active behavior.
- Use when the task needs to package Windows-native build policy together with prereq registration and receipt capture.

### Negative Triggers

- Do not use for pure runtime code changes with no Windows host evaluation surface.
- Do not use to invent service names, scheduled task names, watchdog script paths, working directories, or other operator-confirmed values.
- Do not use when the repository has no Windows evaluation surfaces to package and the task is only abstract architecture discussion.

### Expected Effect

- The repository ends up with one truthful Windows operator entry point, narrow helper-script boundaries, explicit operator-confirmed gates, and receipt-backed acceptance evidence.

## Entry Instructions

- Read the repository adapter first and locate any existing Windows runbooks, helper scripts, receipt directories, and operator metadata files.
- Keep the default execution path truthful for the target host; if a copied binary is not trusted, prefer a native Windows build path or `go run` until a verified `.exe` exists.
- Build one top-level operator entry point that explains what to read first, which helper script handles each lane, where receipts go, and what blocks execution.
- Preserve the distinction between readonly, observation, and lifecycle lanes.
- Treat historical receipts as time-scoped evidence; do not present them as the default behavior for future runs.
- Stop and report blockers instead of mutating the contract when operator-confirmed values or host prerequisites are missing.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| project context adapter | .github/instructions/project-context.instructions.md | yes | Routes Windows evaluation topics to the right framework surfaces |
| windows ssh automation skill | .github/skills/windows-ssh-automation/SKILL.md | no | Remote Windows control patterns when the host is driven over SSH |
| receipt contract template | templates/receipt_contract.template.md | yes | Canonical receipt naming, inventory, correction, and acceptance rules |
| agent delegation guide | docs/AGENT_DELEGATION_GUIDE.md | no | Main-agent delegation, acceptance, and blocker-reporting rules |
| developer toolchain design | docs/DEVELOPER_TOOLCHAIN_DESIGN.md | no | How build, smoke, and verification surfaces should be exposed to agents |

## Governance

### Allowed Evidence

- Receipt-bearing operator runs and helper-script outputs.
- Human-reviewed runbooks and operator onboarding docs.
- Verified build and smoke paths on real Windows hosts.
- Root-cause notes that distinguish observation from proof.

### Reviewer Gate

- Changes to purpose, triggers, entry instructions, or degradation require maintainer review because they redefine when the framework should trust Windows host evaluation packaging.

### Forbidden Direct Update Inputs

- Raw chat transcripts promoted directly into the skill.
- One-off host quirks presented as framework-wide rules.
- Repository-specific task names or paths promoted into portable hard rules unless the skill clearly labels them as examples.

## Receipt And Review Matrix

| Field | Proposal evidence tiers | Minimum reviewer threshold | Guardrail override | Promotion tier |
|---|---|---|---|---|
| `purpose` | `1-2 only` | `single-reviewer` | `dual-reviewer` if the workflow boundary changes | `human-only` |
| `triggers` | `1-3` | `single-reviewer` | `single-reviewer`; must preserve negative triggers | `delegated-reviewed` |
| `entry_instructions` | `1-3` | `single-reviewer` | `single-reviewer`; cannot silently remove operator-confirmed gates | `delegated-reviewed` |
| `references` | `1-4` | `single-reviewer` | `single-reviewer`; reference truthfulness required | `delegated-safe` |
| `governance` | `1-2 only` | `single-reviewer` | `dual-reviewer` for reviewer-threshold changes | `human-only` |
| `degradation` | `1-3` | `single-reviewer` | `single-reviewer`; must preserve blocker honesty | `delegated-reviewed` |

## Degradation

- If the repository has no top-level operator entry point yet, degrade to identifying the real Windows runbook, helper scripts, and receipt root first, then propose the entry point rather than guessing one.
- If Windows-native build cannot be verified, degrade to truthful `go run` or repository-local fallback instructions rather than claiming a distributable binary path exists.
- If the repository has historical receipts but no contract doc, use the receipt contract template as the review baseline and record the gap explicitly.
- If operator-confirmed values are missing, stop and surface them as blockers instead of inventing host facts.

## Validator Notes

- Keep repository-specific names, paths, and host IDs in examples or references, not in the portable hard rules.
- The skill should stay focused on packaging and executing Windows host evaluation workflows, not on redefining runtime semantics.