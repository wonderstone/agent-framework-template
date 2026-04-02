# Developer Toolchain Design

This document defines the formal v1 design draft for the framework's `Developer Toolchain` concept.

It exists to turn the higher-level discussion in `docs/DEVELOPER_TOOLCHAIN_DISCUSSION.md` into a concrete, implementable contract that later template and bootstrap changes can follow.

This is a design draft with shipped template/bootstrap adoption, manifest-gated required-core enforcement for newly bootstrapped adopters, and reminder-level validator support for softer guidance.

---

## Design Status

| Field | Value |
|---|---|
| Status | Draft v1 |
| Scope | Framework-level design for adopter-facing project adapters |
| Depends on | `Validation Toolchain`, `Build and Test Commands`, execution contract surfaces |
| Already changes | bootstrap output, template surfaces, manifest payloads, required-core hard-fail validation for manifest-based adopters, and reminder-level validator advisories |
| Does not yet change | optional enrichment fields such as `Debug`, `Format`, log-inspection helpers, or freshness rules for `verified-working` |

Normative note:

when this document says a field is `required in v1`, it means:

the field is part of the target v1 contract that future template, bootstrap, and validation work should implement.

It does not mean every possible v1 enrichment field is already enforced today.

Current implementation boundary:

1. the required core is enforced for newly bootstrapped manifest-based adopters
2. the template root self-validates the same required core
3. optional enrichment fields remain advisory

---

## Purpose

The framework already defines how repositories declare validation tooling.

What it does not yet define cleanly is how repositories declare the development tooling an agent needs while implementing and debugging work.

`Developer Toolchain` fills that gap.

Its purpose is to give the agent a durable place to find the minimum operational information needed to:

1. collect diagnostics
2. decide which command surface to use next
3. avoid guessing about run, build, health, and debug paths
4. stop at the correct depth for the current task scope

This surface is complementary to `Validation Toolchain`, not a replacement for it.

---

## Core Design Decision

The framework keeps two separate toolchain surfaces.

| Surface | Question it answers |
|---|---|
| `Validation Toolchain` | How does the repository prove correctness and acceptance? |
| `Developer Toolchain` | How does the agent reach a runnable, diagnosable, and debuggable state during implementation? |

Decision rationale:

1. validation proves acceptability
2. developer tooling supports implementation closure
3. merging them would blur two different decision surfaces and weaken both

---

## v1 Design Goals

The v1 contract should be:

1. strong enough to support real implementation closure
2. light enough that repositories can adopt it honestly
3. explicit about scope and stop conditions
4. actionable when commands are declared but not yet trustworthy

The v1 contract should not require repositories to invent fake debugger stories or perfect runtime automation.

---

## v1 Schema

### Canonical Entry Shape

v1 freezes one canonical shape for a developer-toolchain entry.

Each entry represents one named operational surface, such as diagnostics, build, run, health, repro, lint, or debug.

v1 also allows qualified labels for multi-runtime repositories, as long as the base surface remains recognizable.

Examples:

1. `Run (frontend)`
2. `Run (backend)`
3. `Health or smoke (journey)`

| Field | Meaning |
|---|---|
| `surface` | The operational surface name, such as `diagnostics`, `build`, `run`, `health`, `repro`, `lint`, `debug` |
| `command_or_source` | The command, tool, or source the agent should use |
| `scope` | The depth at which this entry is relevant: `file`, `module`, `service`, or `full-stack` |
| `status` | Verification status: `declared-unverified`, `verified-working`, `known-broken`, or `not-applicable` |
| `fallback_or_stop` | The fallback path to use, or the explicit stop rule if no fallback exists |
| `notes` | Optional short context needed to use the entry honestly |

Design rule:

`status` and `fallback_or_stop` belong to the same entry as the command they qualify.

If a repository uses qualified labels, the framework evaluates the base surface name and treats the qualifier as runtime-specific context rather than a different contract field.

They must not be tracked in a separate free-floating section, because the agent's behavior depends on the command and its trust state being read together.

Example shape:

```text
surface: run
command_or_source: npm run dev
scope: service
status: declared-unverified
fallback_or_stop: attempt once; on failure, use npm run preview if declared, otherwise stop and report runtime path unverified
notes: local frontend dev server
```

### Required Core

These fields are required in v1 when the corresponding surface exists.

| Field | Requirement | Notes |
|---|---|---|
| Primary language | Required | Dominant language for the touched runtime or module surface |
| Diagnostics source or command | Required | Language server, compiler, checker, or equivalent syntax or type diagnostic source |
| Package manager | Required | The package or environment manager the agent is expected to use |
| Run entrypoint | Required, or explicit `none` | Main local execution path for the relevant runtime surface |
| Health check or smoke path | Required, or explicit `none` | Fastest reliable runtime confirmation path |
| Repro path | Required for repos with a live runtime path, otherwise explicit `none` | Shortest user-visible reproduction path |

Additional rule:

`Build` becomes required when the relevant runtime path depends on a build step before it can run honestly.

Additional clarification:

required fields in this section describe the target contract for the future implemented surface.

They do not imply that today's bootstrap output or validator already enforces them.

### Recommended Fields

These fields are recommended in v1 and should normally be present when the repository has the surface.

| Field | Why recommended |
|---|---|
| Lint | Helps catch policy and quality failures before deeper execution |
| Build | Clarifies compile or packaging boundaries even when not always needed |
| Logs or inspection command | Gives the agent a repeatable runtime observation surface |
| Scope tag on non-core entries | Lets the agent apply the same stop-rule logic to lint, debug, logs, and related helper entries |

Supported scope tags in v1:

1. `file`
2. `module`
3. `service`
4. `full-stack`

Scope model rule:

1. scope is attached per entry, not once for the whole section
2. a repository may declare multiple runtime entries with different scopes
3. the agent selects the minimum viable entry whose scope matches the task and user-visible acceptance target

This keeps scope actionable for mixed repositories instead of making it a decorative label.

### Optional Fields

These fields remain optional in v1.

| Field | Why optional in v1 |
|---|---|
| Format | Helpful but not essential to execution closure |
| Debug entry or attach path | Some repositories still rely on run-plus-logs rather than a formal debugger |
| Output priority override | Useful for advanced repos, but not required for the default policy |
| Environment or bootstrap notes | Helpful context, but not a base contract field |

---

## Verification Status Model

Declared commands are not automatically trustworthy.

The design therefore distinguishes between declared surfaces and verification status.

### Status Values

| Status | Meaning |
|---|---|
| `declared-unverified` | Intended command exists but has not yet been confirmed in a relevant context |
| `verified-working` | Command succeeded at least once in a relevant recent context |
| `known-broken` | Command is known to fail for current repository reasons |
| `not-applicable` | Surface does not exist for this repository or scope |

### Required Agent Behavior

Verification status is not decorative. It must change behavior.

| Status | Required agent behavior |
|---|---|
| `declared-unverified` | Agent may attempt it if it is the minimum next step; failure is recoverable and must be recorded honestly |
| `verified-working` | Agent should prefer this path over alternative commands at the same scope |
| `known-broken` | Agent must not rely on it as the primary path; use the declared fallback or stop if none exists |
| `not-applicable` | Agent skips the surface without penalty |

Additional policy:

every non-working status must pair with one of these outcomes:

1. explicit fallback path
2. explicit stop rule
3. explicit `none`

Without one of those outcomes, the status does not form a usable decision surface.

---

## Default Execution Ladder

The framework defines a default consumption order for developer-toolchain surfaces.

```text
diagnostics
→ lint
→ build
→ run
→ health or smoke
→ repro path
```

This is a default ladder, not a command to always run every layer.

The agent should climb only as far as the task scope and acceptance target require.

Selection rule:

1. choose the narrowest relevant entry first
2. if that entry succeeds and satisfies the stop rule, do not escalate to a broader scope
3. only move to a broader scope when the narrower scope cannot satisfy the declared acceptance target or explicitly declares a broader fallback

### Scope-Aware Stop Rules

| Task scope | Default ladder | Default stop rule |
|---|---|---|
| `file` | diagnostics → lint | Stop after local static blockers are cleared unless runnable proof was explicitly requested |
| `module` | diagnostics → lint → build when applicable | Stop after module-level validation succeeds |
| `service` | diagnostics → lint → build → run → health or smoke | Stop when the declared service entrypoint is running and the health path passes |
| `full-stack` | diagnostics → lint → build → run → health or smoke → repro path | Stop when the declared user-visible repro path is exercised or explicitly blocked |

Rule:

full runtime startup is not the default for leaf edits.

The ladder is meant to reduce guesswork, not create unnecessary execution overhead.

For multi-runtime repositories:

1. each runtime path should be represented by its own entry set
2. the framework does not require a single universal run command in v1; qualified surface labels are valid
3. the agent should use the entry set that matches the touched surface and declared repro path

---

## Repro Path Policy

For repositories with a live runtime path, the repro path is a first-class field in v1.

This is because the most expensive agent recovery failures usually happen when the user-visible path cannot be reproduced reliably.

Allowed v1 values:

1. a concrete repro path
2. `none`, when the repository truthfully does not yet have one

Disallowed v1 behavior:

inventing a placeholder repro path just to satisfy the schema.

---

## Debug Policy

v1 does not require every repository to provide a formal debugger entry.

Repos without a debugger surface are still valid if they provide an honest runtime loop such as:

```text
run command
→ observe logs
→ hit health endpoint or smoke path
→ reproduce issue
→ iterate
```

This keeps the framework strict about closure while avoiding debugger fiction.

---

## Integration Points

When the design moves from draft to implementation, these framework surfaces are expected to change.

| Surface | Planned change |
|---|---|
| `templates/project-context.template.md` | Add a `Developer Toolchain` section with v1 fields |
| `scripts/bootstrap_adoption.py` | Render first-pass `Developer Toolchain` placeholders and preset defaults |
| `docs/ADOPTION_GUIDE.md` | Add an adoption step covering language plus developer-toolchain confirmation |
| `templates/execution_contract.template.md` | Add a short execution-ladder and stop-rule policy section |
| `.github/project-context.instructions.md` | Add formal trigger language for developer-toolchain design and usage |

Reminder-level validator advisories are already part of this design draft.

Manifest-gated hard-fail validation for the required core is now part of the implementation path for newly bootstrapped adopters.

Rollout rule:

1. the template root still emits advisories for soft guidance and also self-validates the required core
2. newly bootstrapped adopters receive a manifest that declares the v1 required-core contract
3. adopted repos only hard-fail against the contract they actually carry in their manifest

This keeps the rollout forward-moving without retroactively breaking older adopters that have not refreshed their framework assets yet.

---

## Explicit v1 Non-Goals

v1 does not attempt to do the following:

1. auto-discover the correct tooling for every ecosystem
2. mandate an IDE launch configuration for every repository
3. guarantee that all AI executors can drive every debugger identically
4. define a permanent freshness contract for `verified-working`
5. hard-fail optional enrichment fields such as `Debug`, `Format`, or log-inspection helpers

---

## Risks And Open Questions

These remain intentionally unresolved in v1.

| Topic | Why unresolved |
|---|---|
| Verification freshness | `verified-working` is useful, but v1 does not yet define how long that status remains trustworthy |
| Multi-runtime repositories | Some repositories expose several valid run paths; v1 does not yet define a canonical selection model |
| Scope-tag drift | Scope tags help execution stop correctly, but they can decay if repositories use them inconsistently |
| Enforcement strength for optional fields | The framework still has not decided when optional enrichments such as `Debug`, `Format`, or log-inspection helpers should graduate from advisories into hard validation failures |

These are tracked as design follow-ups, not blockers for publishing the v1 draft.

---

## Adoption Guidance For The Current Draft

While v1 is still a draft rather than a frozen long-term standard:

1. use this document as the source of truth for field names and behavior policy
2. keep the discussion doc for argument history and alternative viewpoints
3. describe enforcement precisely: required-core enforcement is live for manifest-based adopters, while optional enrichment remains advisory

This keeps the draft honest while still allowing future implementation work to converge around a stable long-term contract.

---

## Decision Summary

| Decision | Outcome |
|---|---|
| Separate `Developer Toolchain` from `Validation Toolchain` | Accepted for v1 |
| Use a progressive contract rather than a heavy required schema | Accepted for v1 |
| Make verification status actionable rather than descriptive | Accepted for v1 |
| Require repro path only for repos with a live runtime path | Accepted for v1 |
| Require a formal debugger surface | Rejected for v1 |

> Updated 2026-04-03: first formal design draft created from the discussion record and appended feedback.