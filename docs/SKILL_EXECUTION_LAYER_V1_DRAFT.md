# SKILL Execution Layer V1 Draft

This document defines the formal v1 design draft for the framework's SKILL execution layer.

It exists to close the gap between the canonical SKILL contract and real task execution so repositories can make skills improve through use without collapsing canonical truth into runtime drift.

---

## Design Status

| Field | Value |
|---|---|
| Status | Draft v1 |
| Scope | Runtime invocation evidence, bounded candidate triggers, lineage metadata, and execution-side artifact surfaces for SKILL evolution |
| Depends on | `docs/SKILL_MECHANISM_V1_DRAFT.md`, `docs/SKILL_HARVEST_LOOP_V1_DRAFT.md`, receipt-anchored closeout, and discussion-backed design decisions |
| Already changes | template surfaces, bootstrap assets, validator expectations, and future runtime evidence packaging for SKILL use |
| Does not yet change | autonomous canonical mutation, cloud skill sharing, telemetry-backed promotion authority, or a fully automated host executor |

Normative note:

when this document says a surface is part of the execution layer, it means:

the surface may be generated automatically from real task execution evidence, but it does not become canonical SKILL truth unless the existing promotion boundary approves it.

---

## Purpose

The framework already has a strong canonical contract for SKILL files and a governance loop for candidate extraction and promotion.

What it has been missing is the thin execution plane that lets repositories answer these questions honestly:

1. was a skill actually invoked
2. why was it invoked
3. what references were loaded
4. what happened during execution
5. should that execution create a candidate for `FIX`, `DERIVED`, or `CAPTURED` evolution

This document defines that missing layer.

Its purpose is to:

1. give runtime use of skills a receipt-bearing evidence surface
2. let repeated task execution generate bounded candidate signals
3. preserve lineage between invocation, candidate, and promotion
4. keep canonical mutation governance strict even when runtime execution becomes more automatic

---

## Core Decision

The framework should add a thin execution layer, not a self-rewriting canonical skill engine.

That means:

1. invocation evidence becomes first-class
2. bounded triggers may create candidate packets
3. typed evolution lineage becomes explicit
4. canonical SKILL files remain constitutionally governed by the existing field-level authority model

The framework should not allow:

1. raw transcripts to rewrite canonical SKILL fields
2. runtime frequency alone to authorize canonical mutation
3. metrics or heuristic summaries to bypass `promotion_tier`

---

## Relationship To Existing SKILL Surfaces

| Surface | Role |
|---|---|
| `docs/SKILL_MECHANISM_V1_DRAFT.md` | canonical skill contract and constitutional field authority |
| `docs/SKILL_HARVEST_LOOP_V1_DRAFT.md` | candidate extraction versus canonical promotion boundary |
| this document | runtime invocation evidence and execution-side evolution inputs |

Design rule:

the execution layer complements the canonical SKILL contract.

it does not replace it.

## Five-Pattern Execution Scaffold Mapping

The execution layer is the main place where the template currently absorbs the usable parts of Google's five skill patterns.

The mapping is intentionally asymmetric:

| Pattern | Execution-layer stance |
|---|---|
| `Tool Wrapper` | execution scaffold that binds a skill to one declared Developer Toolchain surface |
| `Reviewer` | receipt-anchored evaluation scaffold tied to independent review, audit, or closeout evidence |
| `Pipeline` | staged execution scaffold with explicit handoff artifacts, checkpoints, and stop rules |
| `Generator` | bounded artifact generation only when output schema, path, and proof surface are explicit |
| `Inversion` | deferred until a truthful host-runtime contract and degradation story exist |

Design rule:

the execution layer does not turn these patterns into new constitutional skill fields.

It turns selected patterns into concrete scaffolds that repositories can ship, validate, and reuse without overclaiming runtime power.

---

## Canonical Execution-Layer Artifacts

The v1 execution layer adds these artifacts:

| Artifact | Canonical? | Purpose |
|---|---|---|
| skill invocation receipt | no | proves that a skill was invoked for a real task, with trigger reason, references loaded, and execution outcome |
| skill candidate packet | no | proposes a bounded change from invocation, closeout, or root-cause evidence |
| skill promotion receipt | yes | records which canonical fields changed and under which authority |

Design rule:

invocation receipts are runtime evidence.

candidate packets are non-canonical proposals.

promotion receipts remain the canonical evidence of approved mutation.

---

## Invocation Lifecycle

The minimal v1 lifecycle is:

1. a host or executor evaluates whether a skill should apply
2. if the skill is used, an invocation receipt is written
3. the receipt records the skill, trigger class, references loaded, outcome, and evidence links
4. bounded trigger rules decide whether a candidate packet should be created
5. the candidate packet carries `FIX`, `DERIVED`, or `CAPTURED` lineage metadata
6. the existing promotion governance decides whether canonical mutation happens

This is intentionally smaller than a full OpenSpace-style autonomous evolution engine.

It gives repositories a truthful first execution plane without pretending they already have full telemetry, cloud sharing, or self-healing runtimes.

---

## Invocation Receipt Contract

The minimal v1 invocation receipt should record:

| Field | Meaning |
|---|---|
| `receipt_id` | stable identifier for the invocation receipt |
| `invocation_id` | stable identifier for the skill use instance |
| `skill_id` | canonical skill being invoked |
| `trigger_class` | why the skill fired |
| `execution_mode` | how the skill was applied at runtime |
| `outcome` | whether the invocation succeeded, fell back, failed, or was overridden |
| `candidate_recommendation` | whether the invocation should propose no change, `FIX`, `DERIVED`, or `CAPTURED` |
| `references_loaded` | which skill references were actually loaded |
| `evidence_links` | closeout, root-cause, or invocation evidence anchors tied to the outcome |

The v1 receipt does not need deep telemetry.

It does need enough structure that later candidate creation can point to something more truthful than a vague session summary.

---

## Trigger Classes

The execution layer uses a small set of bounded trigger classes in v1:

| Trigger class | When it applies |
|---|---|
| `explicit-request` | the user or task packet explicitly asked for the skill |
| `repeated-invocation-failure` | the same or closely related invocation failed repeatedly |
| `repeated-manual-correction` | the agent or operator repeatedly repaired the same gap after skill use |
| `repeated-successful-reuse` | a workflow or guardrail repeatedly worked and now looks reusable |
| `operator-forced` | a human or owner explicitly forced invocation for a known case |

Design rule:

trigger classes may create candidates.

they do not authorize canonical mutation by themselves.

---

## Evolution Modes

The execution layer adopts this typed lineage model:

| Mode | Meaning |
|---|---|
| `FIX` | repair a broken, stale, or misleading skill path |
| `DERIVED` | create a specialized or enhanced branch from an existing skill |
| `CAPTURED` | extract a new reusable pattern from successful execution |

Design rule:

`FIX`, `DERIVED`, and `CAPTURED` describe the origin and lineage of a proposal.

they do not define the authority level of the resulting canonical change.

Authority still comes from the existing `promotion_tier` table in the canonical SKILL contract.

---

## Host Integration Contract

The v1 execution layer standardizes one minimal host-facing decision surface:

### Trigger Evaluation Input

1. requested task or task phase
2. candidate skill id
3. reason the host believes the skill might apply
4. nearby non-trigger or uncertainty notes

### Trigger Evaluation Output

1. invoke or skip decision
2. trigger class
3. required references to load
4. invocation id if invoked

This contract is intentionally narrow.

Repositories may implement it through prompts, wrappers, MCP tools, or local executors.

The framework only standardizes the decision shape and receipt fields in v1.

---

## Validator Contract

The validator should enforce the truthful structural layer first.

### Hard-Fail Checks

The first implementation layer should hard-fail when:

1. the template repository is missing the invocation receipt template
2. candidate packets omit execution-lineage fields such as `evolution_mode`, `candidate_trigger`, or `invocation_ids`
3. promotion receipts omit lineage fields needed to explain where an approved mutation came from
4. the execution-layer doc or shipped docs reference a runtime self-evolution path that the template does not actually provide

### Advisory Checks

The first implementation layer may keep these advisory:

1. whether a repository has enough runtime coverage to generate high-quality invocation receipts automatically
2. whether trigger classes are too broad for a given adopter repo
3. whether lineage naming is elegant enough for dashboards or analytics

Design rule:

the validator should prove that the execution layer exists structurally and truthfully.

it should not pretend to validate the semantic quality of every future evolved skill.

---

## Migration Boundary

The minimum implementation wave from this draft is:

1. add this TYPE-A doc
2. add a `skill_invocation_receipt` template
3. extend candidate and promotion artifacts with typed evolution lineage fields
4. ship a helper script that can initialize invocation and candidate artifacts from real evidence
5. update bootstrap, README, adoption docs, and validator surfaces accordingly

This gives adopters an execution path they can actually use.

It still stops short of autonomous canonical mutation, cloud sync, or full runtime telemetry.

---

## Current Decision Summary

The template should move toward OpenSpace's self-evolution direction by making skill execution observable, lineage-aware, and candidate-producing.

It should not move toward self-rewriting canonical truth.

The next implementation wave should therefore make invocation evidence, bounded candidate triggers, and `FIX / DERIVED / CAPTURED` lineage real shipped surfaces for adopters.