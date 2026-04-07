# Documentation Index

> This index covers all TYPE-A (long-lived) documents. Update it whenever a TYPE-A doc is added or removed.
> TYPE-C (phase reports, one-time analyses) live in `docs/archive/` and are not listed here.

---

## Framework (included with this template)

| Document | Description |
|---|---|
| `docs/FRAMEWORK_ARCHITECTURE.md` | How the agent framework layers work and why |
| `docs/ADOPTION_GUIDE.md` | Step-by-step guide for adopting this framework in a new project |
| `docs/CLOSEOUT_SUMMARY_TEMPLATE.md` | Stable closeout-summary format for `task_complete.summary`, including visible markers and global state fields |
| `docs/PROGRESS_UPDATE_TEMPLATE.md` | Stable progress-update format for while-style work, clearly separated from final closeout |
| `docs/STRATEGY_MECHANISM_LAYERING.md` | How to separate role strategy from reusable workflow mechanism |
| `docs/ROLE_STRATEGY_EXAMPLES.md` | Concrete reviewer and agent role examples spanning multiple development-stage responsibilities |
| `docs/COMPATIBILITY.md` | What is validated in this repository and what adopters still need to verify locally |
| `docs/SKILL_HARVEST_LOOP_V1_DRAFT.md` | Formal v1 design draft for post-task SKILL harvest and per-field promotion-governance |
| `docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md` | Formal v1 design draft for runtime invocation evidence, bounded candidate triggers, and typed SKILL evolution lineage |
| `docs/SKILL_MECHANISM_V1_DRAFT.md` | Formal v1 design draft for a framework-native SKILL contract, evidence gates, and honest degradation |
| `docs/DEVELOPER_TOOLCHAIN_DESIGN.md` | Formal v1 design draft for the agent-facing Developer Toolchain surface |
| `docs/DEVELOPER_TOOLCHAIN_DISCUSSION.md` | Discussion surface for making language diagnostics, lint, build, run, and debug tooling first-class agent inputs |
| `docs/AI_TRACEABILITY_AND_RECOVERY_DISCUSSION.md` | Discussion surface for making AI-era failure diagnosis, root-cause reconstruction, runtime evidence, and recovery state first-class framework inputs |
| `docs/TRACEABILITY_AND_RECOVERY_V1_DRAFT.md` | Formal v1 design draft for user-surface mapping, progressive failure capture, runtime evidence ownership, and root-cause closeout |
| `docs/DOC_FIRST_EXECUTION_GUIDELINES.md` | Repository-default doc-first planning rule plus the reusable surfaces adopters should inherit |
| `docs/RUNTIME_SURFACE_PROTECTION.md` | Surface guard registry pattern: protecting user-facing runtime paths from placeholder regression |
| `docs/LEFTOVER_UNIT_CONTRACT.md` | Leftover unit contract: how to record, classify, and recover partial work truthfully |

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
| `docs/runbooks/resumable-git-audit-pipeline.md` | Packet / receipt / handoff workflow for resumable audit, replaceable reviewers, and Git closeout recovery |

---

*Last updated: 2026-04-07 — added the SKILL execution layer v1 design draft*
*Maintainer rule: this file is updated as part of the commit that adds or removes a TYPE-A doc.*
