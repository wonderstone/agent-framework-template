# Traceability And Recovery V1 Draft

This document defines the formal v1 design draft for the framework's traceability and recovery model.

It exists to turn the discussion in `docs/AI_TRACEABILITY_AND_RECOVERY_DISCUSSION.md` into a concrete, implementable contract that later template and project-adapter changes can follow.

This is a design draft with first-pass template and adapter implications, not yet a hard-enforced framework contract.

---

## Design Status

| Field | Value |
|---|---|
| Status | Draft v1 |
| Scope | Framework-level design for repository traceability, failure capture, and recovery truth |
| Depends on | Doc-first execution, project adapter, Developer Toolchain, closeout truthfulness surfaces |
| Already changes | Design direction for future template and adapter additions |
| Does not yet change | Hard validator enforcement or required adopter completeness |

Normative note:

when this document says a field is `required in v1`, it means:

the field is part of the target v1 contract that future template and adapter work should implement.

It does not mean the current repository or adopters are already validated against it today.

---

## Purpose

AI-assisted implementation increases delivery speed, but it also makes it easier for repositories to lose causal legibility.

When a system fails, teams often cannot answer quickly enough:

1. what changed
2. what user-visible surface was affected
3. what evidence first showed the failure
4. what root cause is established versus only suspected
5. what evidence supports the claimed recovery

The purpose of this v1 design is to make those answers reconstructable without requiring every contributor to retain a complete mental model of the codebase.

The target is operational legibility, not exhaustive documentation.

---

## Core Design Decision

v1 treats traceability and recovery as a small set of connected truth surfaces rather than one large incident system.

The connected surfaces are:

| Surface | Purpose |
|---|---|
| `User Surface Map` | Maps user-visible flows to owning code paths, sensitivity, repro path, and evidence source |
| `Failure Packet` | Captures failure state progressively as investigation begins |
| `Developer Toolchain` runtime evidence sub-section | Declares where logs, health checks, smoke paths, and related runtime evidence live |
| `Root Cause Note` | Records cause status, supporting evidence, and residual uncertainty at closeout |

Design rationale:

1. the `User Surface Map` is the routing surface
2. the `Failure Packet` is the event surface
3. the `Developer Toolchain` owns runtime evidence truth
4. the `Root Cause Note` keeps symptom recovery separate from understanding

These surfaces are complementary.

They should not be merged into one giant template, and they should not be allowed to drift into separate contradictory truth sources.

---

## v1 Design Goals

The v1 contract should be:

1. small enough to adopt honestly
2. strong enough to reconstruct meaningful failures
3. explicit about which surface is authoritative for which question
4. capable of upgrading automatically for security-sensitive paths
5. usable under failure pressure, not only in calm postmortems

v1 should not require full incident-management tooling, complete service mapping, or advanced observability stacks.

---

## Authority Model

The framework should be explicit about which surface answers which question.

| Question | Authoritative surface |
|---|---|
| What user-visible flow is this? | `User Surface Map` |
| Is this flow security-sensitive? | `User Surface Map` / project adapter sensitive-surface declarations |
| Where should runtime evidence be gathered? | `Developer Toolchain` runtime evidence sub-section |
| What is broken right now? | `Failure Packet` |
| Was the cause established or only suspected? | `Root Cause Note` |
| What escalation policy applies? | Project adapter security escalation rule |

Rule:

if two surfaces try to answer the same question, one must be demoted to a reference or removed.

v1 optimizes for single-source-of-truth behavior.

---

## v1 Surface Set

### 1. User Surface Map

The `User Surface Map` is the foundational artifact in v1.

It is a decision surface, not an architecture encyclopedia.

Its job is to let a future human or agent answer:

1. what user-visible surface is being discussed
2. what code path or entry point owns it
3. whether stronger traceability rules apply
4. how to reproduce it quickly
5. where to look first for evidence

#### Minimum Required Fields

| Field | Meaning |
|---|---|
| `surface_name` | Name of the user-visible flow or entry surface |
| `owner_path` | Primary code path, entrypoint, or owning module/service |
| `sensitive` | `yes` or `no` |
| `fastest_repro_path` | Shortest trustworthy path to reproduce the flow |
| `primary_evidence_source` | First evidence source to inspect for this surface |

#### v1 Adoption Rule

The map does not need full product coverage in v1.

Minimum honest bar:

1. cover the top user-critical surfaces first
2. allow partial coverage
3. do not claim completeness unless it is actually maintained

Repositories without a live runtime path may declare `none`.

### 2. Failure Packet

The `Failure Packet` is the event artifact used when runtime behavior is broken or unexpectedly unsafe.

It must support progressive capture.

That means a packet is valid before every field is known.

#### Minimum First Save

v1 requires these fields for the first save:

| Field | Meaning |
|---|---|
| `symptom` | What is visibly wrong |
| `impacted_surface` | Which user-visible surface appears affected |
| `first_observed_evidence` | The first concrete signal that suggested failure |

If the repository genuinely does not yet have concrete evidence beyond a report, that fact must be stated explicitly rather than omitted silently.

#### Full Packet Fields

When the packet is promoted to full investigation depth, it should include:

| Field | Meaning |
|---|---|
| `symptom` | Failure summary |
| `impacted_surface` | Surface from the user-surface map |
| `severity_tier` | `lightweight` or `full` |
| `first_observed_evidence` | First concrete signal |
| `repro_steps` | Shortest known reproduction path |
| `suspected_layers` | Likely code, config, tool, prompt, or dependency layers involved |
| `current_hypothesis` | Best current causal hypothesis |
| `runtime_evidence_refs` | Links or references to logs, health checks, traces, screenshots, or scripts |
| `status` | `open`, `mitigated`, `cause-suspected`, `cause-established`, or `closed` |

#### Promotion Rules

A packet must be promoted from `lightweight` to `full` when any of these are true:

1. the impacted surface is marked `sensitive`
2. the issue survives one attempted fix
3. the issue recurs after previous closeout
4. the issue becomes shared beyond a single local executor

Promotion should be agent-driven when the trigger is observable.

It should not rely only on human memory.

### 3. Runtime Evidence Ownership

v1 assigns runtime evidence truth to the `Developer Toolchain` surface.

It should not default to a separate required template.

The runtime evidence sub-section should declare:

| Field | Meaning |
|---|---|
| `evidence_surface` | Log, health, smoke, trace, metric, or inspection command |
| `applies_to` | Surface or runtime scope this evidence applies to |
| `priority` | Whether this is the first, second, or fallback evidence source |
| `status` | `declared-unverified`, `verified-working`, `known-broken`, or `not-applicable` |
| `fallback_or_stop` | What to do if this evidence source is unavailable |

#### Promotion To Standalone Doc

Runtime evidence may be promoted to a standalone canonical doc when one table or section can no longer tell an agent where to look first without branching into service-specific prose.

This is a functional threshold, not a numeric one.

### 4. Root Cause Note

The `Root Cause Note` is the closeout artifact that records whether the repository actually understands the failure.

Its main role is to preserve the distinction between:

1. symptom fixed
2. cause suspected
3. cause established

#### Required Fields

| Field | Meaning |
|---|---|
| `cause_status` | `suspected` or `established` |
| `cause_statement` | What the repository believes caused the issue |
| `supporting_evidence` | Evidence supporting that statement |
| `fix_statement` | What changed |
| `why_fix_addresses_cause` | Why this fix targets cause rather than symptom alone |
| `residual_risk` | What could still go wrong and what would likely be observed first |

#### v1 Requirement Rule

The `Root Cause Note` is required in v1 when:

1. a `Failure Packet` exists
2. the issue was user-visible
3. the issue touched a sensitive surface
4. the issue is being closed with cause still `suspected`

It is not required for every low-severity defect with no failure artifact.

---

## Severity Model

v1 defines two failure tiers.

| Tier | Meaning |
|---|---|
| `lightweight` | Single-path, low-risk, non-sensitive failure with limited spread |
| `full` | Sensitive, recurring, user-visible, or cross-executor failure requiring deeper traceability |

The tier is set at packet creation time and may be upgraded later.

Downgrading should be rare and should be explained explicitly if it happens.

---

## Security Escalation Rule

Security-sensitive traceability requirements must not depend only on someone remembering to apply them.

v1 therefore requires automatic escalation when either of these is true:

1. the impacted surface is marked `sensitive` in the `User Surface Map`
2. the failure touches a declared sensitive path, config surface, secret surface, or trust-boundary surface in the project adapter

Human classification remains a manual override path, not the primary trigger.

### Required Additions After Escalation

After escalation, the repository must record at minimum:

1. impacted trust boundary
2. relevant config, secret, or policy surface
3. at least one negative-path or misuse-path validation claim

Recommended but not required in v1:

1. rollback or containment note
2. audit log reference
3. abuse-case repro detail

---

## Ownership Model

v1 keeps ownership aligned with truth type.

| Surface | Owner |
|---|---|
| `User Surface Map` | Project adapter / long-lived repository truth |
| Sensitive surface declarations and escalation rule | Project adapter / long-lived repository truth |
| Runtime evidence sub-section | `Developer Toolchain` / execution truth |
| `Failure Packet` | Task or incident artifact / event truth |
| `Root Cause Note` | Closeout artifact / recovery truth |

This separation is deliberate:

1. repository truths should not be recreated per incident
2. incident truths should not be frozen into adoption-time docs
3. runtime evidence should stay near execution surfaces rather than incident narratives

---

## Template Implications

If v1 is adopted, the framework should eventually add or update these surfaces:

| Area | Suggested change |
|---|---|
| `templates/project-context.template.md` | Add `User Surface Map` and sensitive-surface declarations |
| `templates/failure_packet.template.md` | Add progressive failure packet template |
| `templates/root_cause_note.template.md` | Add closeout artifact for cause and residual risk |
| `docs/DEVELOPER_TOOLCHAIN_DESIGN.md` and related template surfaces | Add runtime evidence ownership and cross-linking |
| `docs/ADOPTION_GUIDE.md` | Add adoption step for user-surface map and sensitive-surface declarations |

v1 does not require a default standalone `runtime_evidence_map.template.md`.

That surface may emerge later if repeated real-world use shows it is needed.

---

## Boundaries And Non-Goals

v1 is intentionally limited.

Non-goals:

1. full incident management
2. mandatory tracing or metrics infrastructure
3. exhaustive mapping of every product surface before adoption can begin
4. replacing repository-specific judgment with a giant universal taxonomy
5. forcing all low-severity defects through heavyweight closeout

The near-term goal is narrower:

create enough durable structure that failures, recovery, and residual uncertainty remain reconstructable.

---

## Open Provisional Choices

The following choices are provisionally set in this draft and should be validated during template prototyping:

1. minimum `Failure Packet` first save uses three fields, not two
2. runtime evidence remains a `Developer Toolchain` sub-section by default
3. `Root Cause Note` is mandatory only when a failure artifact or higher-risk closeout exists
4. the `User Surface Map` is partial-first, not exhaustive-first

If template trials show these choices are too heavy or too weak, the draft should be revised before enforcement is considered.
