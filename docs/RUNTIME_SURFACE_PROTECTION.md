# Runtime Surface Protection

This document explains the **surface guard registry** pattern — a mechanism for preventing placeholder or mock execution from silently re-entering user-facing runtime paths after they have been promoted to production.

---

## The Problem

Projects that develop features incrementally often use placeholder responses during incubation (e.g., a fixed template reply, a deterministic test fixture, a mock payload). This is valid during development. It becomes dangerous when a placeholder silently survives into a path that real users are hitting.

The failure mode is subtle: the feature "passes tests" (because the tests were written against the placeholder behavior), but the user experiences something wrong. The drift from "this is a temporary placeholder" to "this is the real default" happens without any visible gate.

---

## Template Status In This Repository

This framework repository documents the pattern but does not ship a generic `runtime_execution_guardrails.py`, hook installer, or live smoke probes of its own.

That is intentional: this repository is a framework package, not an application with an active default user runtime path. The concrete guard script belongs in an adopting repository once it has a real live surface to protect.

Use this document in one of two ways:

1. implement the pattern in your repository when you have a real runtime path and a repeatable live validator
2. record it as a leftover unit until the runtime surface and validation boundary are stable enough to justify enforcement

---

## The Guard Registry Pattern

A guard registry maps **source file paths** to **verification behaviors**, so that whenever a change touches a protected file, the appropriate checks run automatically.

Each entry in the registry is a **guard surface** — a named unit with the following fields:

| Field | Purpose |
|---|---|
| `name` | Unique identifier for this surface |
| `exposure` | Tier: `active_default_user_path` or `candidate_incubator_service` |
| `trigger_prefixes` | File paths that activate this guard when modified |
| `protected_source_roots` | Files scanned for banned phrases |
| `banned_phrases` | Exact strings that indicate placeholder execution |
| `focused_tests` | Test files or commands that must pass before commit |
| `live_endpoints` | Real service endpoints to probe for live smoke |
| `live_commands` | Validator scripts to run against live services |

### Two-Tier Surface Classification

| Tier | Meaning | Guard behavior |
|---|---|---|
| `active_default_user_path` | The path a real user hits without any feature flag | Enters pre-commit fail-fast; live smoke required on push |
| `candidate_incubator_service` | Accessible via internal service but not yet the default user path | Audited periodically; does not block commits |

This two-tier system prevents the "all or nothing" trap: a surface that isn't ready for production can still be registered and audited without blocking every commit.

---

## Automation Layers

### Layer 1 — Pre-Commit Guard

Before any commit that touches a protected source root:

1. Scan the source root for banned phrases
2. Run the focused test suite for that surface
3. Block the commit if either check fails

This layer must be **fast** — it runs on every commit. Avoid expensive live probes here.

### Layer 1.5 — Candidate Audit

For `candidate_incubator_service` surfaces:

1. Run a dedicated audit command that checks for promotion-blocking placeholder markers
2. Report findings but do not block commits
3. Surface the findings before the service is promoted to the default user path

### Layer 2 — Pre-Push Live Gate

When an outgoing push touches a protected active surface:

1. Probe the live endpoints (real services, not mocks)
2. Run live validator scripts
3. Assert that the response does not contain banned phrases
4. Block the push if the live smoke fails

### Layer 3 — CI Bundle

Replicate the pre-commit guard in CI, so the same check runs on every PR against the target branch. CI should call the same guard script, not a parallel implementation.

---

## Banned Phrase Detection

A banned phrase is a **concrete text string** that indicates placeholder execution. Examples:

- `"I checked in as your companion and kept the reply grounded in the current moment."`
- `"Work runtime received"`
- `"I stayed on the lightweight research path without external evidence retrieval."`

These phrases are chosen to be **false positives impossible in production**: no real response would contain them. The check is a grep, not a semantic analysis — that is intentional. Semantic checks drift; grep is stable.

When adding a new guard surface, choose banned phrases that are:

1. Specific enough that they cannot appear in legitimate output
2. Stable — they should not change as the placeholder evolves
3. Matched to the placeholder's actual output, not a hypothetical example

---

## Human Participation Nodes

The guard registry is a tool, not a replacement for human judgment. The following actions require explicit human decision:

### Promoting a surface to `active_default_user_path`

Before promoting a candidate surface:

1. Register it in the guard script with its banned phrases, focused tests, and live endpoints
2. Run the candidate audit and resolve all promotion blockers
3. Update this doc and the project adapter to reflect the new tier
4. Only then allow the surface to enter the pre-commit fail-fast

### Adding a new banned phrase

A banned phrase added incorrectly (too broad) will create false positives and destroy trust in the guard. Review each phrase against real production output before adding it.

### Removing a guard surface

A surface that is decommissioned must be explicitly removed from the registry, not just left registered. A stale guard is misleading.

---

## Adopting This Pattern

### Step 1 — Identify your default user paths

List every entry point that a real user can hit without a feature flag or internal URL. These are candidates for `active_default_user_path`.

### Step 2 — Identify placeholder markers

For each active surface, find the text or behavior that would indicate placeholder execution. Write it down as banned phrases.

### Step 3 — Write focused tests

For each surface, write at least one focused test that asserts canonical execution (not placeholder behavior). This test runs on pre-commit.

### Step 4 — Write a live validator

For each surface, write a script that probes the real running service and asserts the response is canonical. This script runs on pre-push.

### Step 5 — Register in the guard script

Create or extend a guard registry script (see `scripts/runtime_execution_guardrails.py` in Sophia-App for a reference implementation) that:

- Defines each surface as a structured data object
- Implements `staged-check`, `candidate-audit`, `live-smoke`, and `push-check` modes
- Is called from pre-commit and pre-push hooks

### Step 6 — Install hooks

Wire the guard script into `.githooks/pre-commit` and `.githooks/pre-push`. Provide an `install_git_hooks.sh` script so that any new contributor can activate the guards with a single command.

---

## Receipt-Anchored Closeout Integration

The guard registry enforces that the code is correct. Rule 25 (Receipt-Anchored Closeout) enforces that the truth source reflects that correctly. These two mechanisms are complementary:

- Guard registry: prevents placeholder from surviving in code
- Receipt-anchored closeout (Rule 25): prevents "completed" from appearing in docs without evidence

Both should be active on any project where production quality of user-facing paths matters.

---

## Reference Implementation

Sophia-App ships a reference implementation of this pattern:

- **Guard script**: `scripts/runtime_execution_guardrails.py`
- **Closeout audit**: `scripts/closeout_truth_audit.py`
- **Hook installer**: `scripts/install_git_hooks.sh`
- **Guard doc**: `docs/RUNTIME_EXECUTION_GUARDRAILS.md`

The reference implementation covers five active default user paths with banned phrase detection, focused test suites, live endpoint probes, and pre-push live gate automation.
