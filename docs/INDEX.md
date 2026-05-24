# Documentation Index

> This index covers all TYPE-A (long-lived) documents. Update it whenever a TYPE-A doc is added or removed.
> TYPE-C (phase reports, one-time analyses) live in `docs/archive/` and are not listed here.

---

## Core Default Mechanisms

> Start here for day-one adoption. These are the smallest honest surfaces that should stay visible before optional families or design-history material.

| Document | Description |
|---|---|
| `docs/FRAMEWORK_ARCHITECTURE.md` | How the agent framework layers work and why |
| `docs/ADOPTION_GUIDE.md` | Step-by-step guide for adopting this framework in a new project |
| `docs/CLOSEOUT_SUMMARY_TEMPLATE.md` | Stable closeout-summary format for `task_complete.summary`, including visible markers and global state fields |
| `docs/PROGRESS_UPDATE_TEMPLATE.md` | Stable progress-update format for while-style work, clearly separated from final closeout |
| `docs/COMPATIBILITY.md` | What is validated in this repository and what adopters still need to verify locally |
| `docs/DOC_FIRST_EXECUTION_GUIDELINES.md` | Repository-default doc-first planning rule plus the reusable surfaces adopters should inherit |
| `docs/STRICT_ADOPTION_AND_VERIFICATION.md` | Strict adoption mode, enforcement-maturity matrix, and local CLI verification flow for downstream repositories |
| `docs/STRATEGY_MECHANISM_LAYERING.md` | How to separate role strategy from reusable workflow mechanism |
| `docs/RUNTIME_SURFACE_PROTECTION.md` | Surface guard registry pattern: protecting user-facing runtime paths from placeholder regression |
| `docs/LEFTOVER_UNIT_CONTRACT.md` | Leftover unit contract: how to record, classify, and recover partial work truthfully |

## Advanced Optional Families

> Keep these when the repository's operating model actually uses them. They are not the smallest day-one baseline.

| Document | Description |
|---|---|
| `docs/ANTI_DRIFT_RULE_REFACTOR_PLAN_V1.md` | Executable plan for shipping anti-drift mechanisms first, then rebasing execution-lifecycle rules onto pipeline plus anti-drift surfaces |
| `docs/ROLE_STRATEGY_EXAMPLES.md` | Concrete reviewer and agent role examples spanning multiple development-stage responsibilities |
| `docs/SKILL_EXTERNAL_ABSORPTION_GUIDE.md` | Canonical boundary for turning external skill ecosystems into local skill, adapter, or mechanism surfaces without importing their host-specific assumptions |
| `docs/AGENT_DELEGATION_GUIDE.md` | Multi-agent delegation rules: capability matrix, parallelism, prompt templates, agent-specific rules, escalation policy, and acceptance gates — distilled from a real A–E1 phase pipeline |
| `templates/receipt_contract.template.md` | Receipt contract template: directory naming, file naming, supporting files, README inventory, correction protocol, and owner acceptance checklist for operator evaluations |

## Reference And Design History

> These surfaces stay valuable for framework evolution and root self-hosting, but they should be read as rationale or upgrade-path material before being treated as default adopter obligations.

| Document | Description |
|---|---|
| `docs/SKILL_HARVEST_LOOP_V1_DRAFT.md` | Formal v1 design draft for post-task SKILL harvest and per-field promotion-governance |
| `docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md` | Formal v1 design draft for runtime invocation evidence, bounded candidate triggers, and typed SKILL evolution lineage |
| `docs/SKILL_FIVE_PATTERN_EXECUTION_PLAN_V1.md` | Doc-first execution plan for absorbing Google's five SKILL patterns into concrete template surfaces |
| `docs/SKILL_MECHANISM_V1_DRAFT.md` | Formal v1 design draft for a framework-native SKILL contract, evidence gates, and honest degradation |
| `docs/DEVELOPER_TOOLCHAIN_DESIGN.md` | Formal v1 design draft for the agent-facing Developer Toolchain surface |
| `docs/DEVELOPER_TOOLCHAIN_DISCUSSION.md` | Discussion surface for making language diagnostics, lint, build, run, and debug tooling first-class agent inputs |
| `docs/EXECUTION_PROOF_WAVE_1_PLAN.md` | Executable first-wave plan for strict-adoption attestation and Developer Toolchain runtime proof surfaces |
| `docs/EXECUTION_PROOF_WAVE_2_PLAN.md` | Executable second-wave plan for toolchain runner, independent evaluation, and local executor review loop surfaces |
| `docs/AI_TRACEABILITY_AND_RECOVERY_DISCUSSION.md` | Discussion surface for making AI-era failure diagnosis, root-cause reconstruction, runtime evidence, and recovery state first-class framework inputs |
| `docs/TRACEABILITY_AND_RECOVERY_V1_DRAFT.md` | Formal v1 design draft for user-surface mapping, progressive failure capture, runtime evidence ownership, and root-cause closeout |

## Repository Root

> These root-level files exist in this repository and act as live companion surfaces beside the TYPE-A docs.

| Document | Description |
|---|---|
| `README.md` | Project entry point and quick-start guide |
| `ROADMAP.md` | Phase planning, milestones, and acceptance criteria |

## Guides and Runbooks

> Add entries here as runbooks are created under `docs/runbooks/`.

| Document | Description |
|---|---|
| `docs/runbooks/multi-model-discussion-loop.md` | Append-only discussion workflow for framework choice, plan review, and other open design questions |
| `docs/runbooks/design_gated_bounded_autonomy.md` | Concrete workflow for explicit routing, design approval, bounded keep-or-revert execution loops, and post-task learning landing |
| `docs/runbooks/frontend_playwright_diagnostics.md` | Reusable workflow for replacing manual browser transcript loops with one repo-owned Playwright smoke and receipt seam |
| `docs/runbooks/managed_cli_terminal_delegation.md` | Trusted-local managed terminal workflow for CLI executors, including the prompt-dispatch handshake, `started` / `started_after_submit` / `degraded` outcomes, execution-ID recording, and hard-condition lane reuse rules |
| `docs/runbooks/runtime_alignment_and_four_lane_delegation.md` | Generic runbook for coupling repo-vs-runtime alignment proof with honest four-lane delegated execution and owner acceptance |
| `docs/runbooks/post-task-harvest.md` | Landing-tier workflow for turning reusable post-task learning into runbooks, scripts, CI gates, or skills |
| `docs/runbooks/resumable-git-audit-pipeline.md` | Packet / receipt / handoff workflow for resumable audit, replaceable reviewers, and Git closeout recovery |
| `docs/runbooks/state-reconciliation.md` | Drift-packet workflow for reconciling `session_state.md`, `ROADMAP.md`, receipts, and handoff truth before closeout |
| `templates/managed_terminal_prompt_dispatch_receipt.template.md` | Reusable handshake receipt template for managed-terminal dispatches, including one allowed Enter step only when the prompt buffered |
| `templates/four_lane_runtime_alignment_status.template.md` | Reusable four-lane round status template that records lane labels, control state, validation, and runtime-alignment dependency honestly |

---

*Last updated: 2026-05-22 — re-tiered the index into core default, advanced optional families, and reference/design-history surfaces*
*Maintainer rule: this file is updated as part of the commit that adds or removes a TYPE-A doc.*
