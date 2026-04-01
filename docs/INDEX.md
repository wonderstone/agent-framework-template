# Documentation Index

> This index covers all TYPE-A (long-lived) documents. Update it whenever a TYPE-A doc is added or removed.
> TYPE-C (phase reports, one-time analyses) live in `docs/archive/` and are not listed here.

---

## Framework (included with this template)

| Document | Description |
|---|---|
| `docs/FRAMEWORK_ARCHITECTURE.md` | How the agent framework layers work and why |
| `docs/ADOPTION_GUIDE.md` | Step-by-step guide for adopting this framework in a new project |
| `docs/STRATEGY_MECHANISM_LAYERING.md` | How to separate role strategy from reusable workflow mechanism |
| `docs/ROLE_STRATEGY_EXAMPLES.md` | Concrete reviewer and agent role examples spanning multiple development-stage responsibilities |
| `docs/COMPATIBILITY.md` | What is validated in this repository and what adopters still need to verify locally |
| `docs/RUNTIME_SURFACE_PROTECTION.md` | Surface guard registry pattern: protecting user-facing runtime paths from placeholder regression |
| `docs/LEFTOVER_UNIT_CONTRACT.md` | Leftover unit contract: how to record, classify, and recover partial work truthfully |

## Project (create these for your project)

> These entries are placeholders. Replace them with the actual docs for your project.
> Remove any entry that does not apply; add new rows as your project's docs grow.

| Document | Description |
|---|---|
| `README.md` | Project entry point and quick-start guide |
| `ARCHITECTURE.md` | System architecture, module map, and service boundaries |
| `ROADMAP.md` | Phase planning, milestones, and acceptance criteria |

## Guides and Runbooks

> Add entries here as runbooks are created under `docs/runbooks/`.

| Document | Description |
|---|---|
| `docs/runbooks/resumable-git-audit-pipeline.md` | Packet / receipt / handoff workflow for resumable audit, replaceable reviewers, and Git closeout recovery |

---

*Last updated: 2026-04-01 — added RUNTIME_SURFACE_PROTECTION.md, LEFTOVER_UNIT_CONTRACT.md*
*Maintainer rule: this file is updated as part of the commit that adds or removes a TYPE-A doc.*
