# SKILL Five-Pattern Execution Plan V1

This document freezes the doc-first execution plan for the next SKILL implementation wave.

It exists to turn the completed discussion in `tmp/discussion/skill_five_patterns_execution_adoption_v1/discussion_packet.md` into an implementation-ready plan that future work can execute against without drifting back into abstract pattern language.

---

## Design Status

| Field | Value |
|---|---|
| Status | Draft execution plan v1 |
| Scope | How the template should absorb Google's five SKILL design patterns into durable framework surfaces |
| Depends on | `docs/SKILL_MECHANISM_V1_DRAFT.md`, `docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md`, `docs/DOC_FIRST_EXECUTION_GUIDELINES.md`, and `tmp/discussion/skill_five_patterns_execution_adoption_v1/discussion_packet.md` |
| Already changes | the intended file scope, validation plan, adoption boundary, and non-goals for the next implementation wave |
| Does not yet change | runtime behavior, validator enforcement, bootstrap output, or shipped helper surfaces until the implementation wave starts |

Normative note:

this plan is executable guidance, not a conceptual survey.

Any future implementation claiming to follow this plan must preserve its staging rules and non-goals unless this document is updated first.

> Updated 2026-04-08: the planned execution wave has now shipped contract-hardened Wrapper, Reviewer, Pipeline, and bounded Generator scaffold families with validator-visible enforcement. Inversion remains deferred.

---

## Goal

Absorb the useful parts of Google's five SKILL design patterns into the template without turning them into a decorative taxonomy.

The required outcome is:

1. future adopted repositories receive concrete execution scaffolding rather than abstract pattern advice
2. the canonical SKILL contract remains governance-safe and does not gain fake pattern metadata
3. any absorbed pattern is bootstrap-shippable, validator-visible, and tied to a real adopter use path

---

## Frozen Direction

The completed discussion froze this staged direction:

| Pattern | Direction |
|---|---|
| `Tool Wrapper` | absorb as execution scaffold |
| `Reviewer` | absorb as execution scaffold candidate, with care not to blur role strategy and SKILL mechanism |
| `Pipeline` | absorb as execution scaffold |
| `Generator` | keep bounded; example-first unless it is tied to explicit artifact generation with validator-visible contracts |
| `Inversion` | defer until the template has a truthful host-runtime contract and degradation story |

Framework rule:

no pattern becomes a shipped template surface unless it earns all of these:

1. a concrete artifact or helper surface
2. bootstrap or adoption-guide integration
3. validator-visible truth checks
4. at least one adopter-useful example or round-trip proof

---

## Current Truth And Gap Summary

### Current Truth

The template already ships:

1. a canonical SKILL contract with governance, degradation, evidence ranking, and field-level promotion authority
2. a harvest loop for candidate extraction and promotion review
3. a first SKILL execution layer with invocation receipts, candidate lineage, promotion lineage, bootstrap coverage, validator coverage, and an adopter round-trip
4. reviewer-role examples, resumable packet or receipt workflows, and developer-toolchain surfaces that can anchor Wrapper, Reviewer, and Pipeline patterns truthfully

### Current Gaps

The template does not yet ship:

1. an explicit mapping from the five patterns into reusable framework surfaces
2. a wrapper contract that binds skills to Developer Toolchain commands with evidence and fallback semantics
3. a reviewer scaffold that connects SKILL execution to the repository's existing evaluation and audit machinery without blurring governance layers
4. a bounded pipeline scaffold that future adopters can reuse for staged execution beyond broad prose guidance
5. a clear boundary stating that Generator is only safe when tied to narrow artifact generation and that Inversion is deferred

---

## File-Level Scope

The next implementation wave should stay inside this file set unless the plan is revised first.

### Canonical Docs

1. `docs/SKILL_MECHANISM_V1_DRAFT.md`
2. `docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md`
3. `docs/ADOPTION_GUIDE.md`
4. `README.md`
5. `docs/INDEX.md`

### Template Surfaces

1. `templates/skill.template.md`
2. one or more new pattern-specific starter templates only if they are real execution scaffolds
3. `templates/project-context.template.md` if the adopter-facing project adapter must route to new pattern-aware execution surfaces

### Shipped Examples

1. `examples/skills/` for bounded Wrapper, Reviewer, Pipeline, and possibly Generator examples
2. `examples/reviewer_roles/` only if Reviewer absorption requires tighter strategy-mechanism linking

### Tooling And Validation

1. `scripts/bootstrap_adoption.py`
2. `scripts/validate_template.py`
3. focused tests under `tests/`

### Explicitly Out Of Scope For The First Wave

1. cloud skill sharing
2. automatic host-side inversion flows
3. broad runtime orchestration beyond what the template can validate honestly
4. adding a required `pattern` field to the canonical SKILL contract

---

## Ordered Implementation Steps

### Step 1 — Freeze The Absorption Boundary In Canonical Docs

Update the SKILL mechanism and execution-layer docs so they say explicitly:

1. the five patterns are not a new constitutional taxonomy
2. Wrapper, Reviewer, and Pipeline are the primary execution-scaffold candidates
3. Generator is safe only in a narrow artifact-generation form unless stronger contracts exist
4. Inversion is deferred until a truthful host-runtime contract exists

Deliverable:

the docs state both what the template will absorb and what it will refuse to overclaim.

### Step 2 — Define The Minimum Wrapper Scaffold

Ship one thin execution-scaffold contract for Tool Wrapper.

Minimum contract:

1. wrapper target surface or command
2. declared input boundary
3. output or evidence shape
4. fallback or stop rule
5. invocation receipt linkage

Deliverable:

future adopters can bind a skill to a real Developer Toolchain surface without inventing hidden runtime behavior.

### Step 3 — Decide Reviewer Placement And Ship The Smallest Honest Surface

Reviewer needs a narrower implementation choice before code starts.

Allowed options:

1. execution scaffold anchored to evaluator or audit receipts
2. strategy-adjacent example layer anchored to reviewer roles and audit machinery

Forbidden option:

1. redefining Reviewer as a new canonical SKILL type or law-bearing field

Deliverable:

one honest reviewer surface that can be shipped, bootstrapped, and validated.

### Step 4 — Ship A Bounded Pipeline Scaffold

Pipeline should be implemented as staged execution scaffolding, not a generic workflow slogan.

Minimum surface:

1. stage boundary
2. artifact handoff or state handoff
3. checkpoint rule
4. stop or degrade rule
5. validator-visible truth surface

Deliverable:

future adopters can reuse a packet or receipt backed pipeline instead of reconstructing staged execution from prose.

### Step 5 — Keep Generator Narrow

Generator may ship only if it is tied to bounded artifact generation already consistent with the template.

Valid early examples:

1. packet generation
2. receipt generation
3. candidate artifact initialization

Invalid early examples:

1. open-ended content generation with no output contract
2. vague “document generator” labels with no validator or receipt surface

Deliverable:

Generator remains useful without turning into a catch-all abstraction bucket.

### Step 6 — Wire Bootstrap, Validator, And Tests Together

No absorbed pattern counts as shipped until the bootstrap and validation surfaces move with it.

Required proof for each shipped scaffold:

1. copied or rendered by bootstrap where appropriate
2. referenced in adopter-facing docs
3. checked structurally by validator
4. covered by focused tests
5. covered by at least one adopter-useful example or round-trip where feasible

Deliverable:

the framework does not regress into docs-only pattern adoption.

---

## Validation Commands

Use these commands for the implementation wave that follows this plan:

```bash
python3 scripts/validate_template.py
python3 -m pytest tests/test_bootstrap_adoption.py tests/test_validate_template.py -q
```

Add focused tests for any new helper script or template surface.

If a new scaffold changes bootstrap output materially, also re-run the bootstrap smoke command recorded in `.github/instructions/project-context.instructions.md`.

---

## User Acceptance Criteria

- [x] When a maintainer reads the SKILL docs, the five-pattern adoption boundary is explicit and does not overclaim pattern support.
- [x] When a maintainer bootstraps the standard profile, the absorbed patterns that were approved for shipping are present as real execution scaffolds, not only prose references.
- [x] When the validator runs, it can distinguish shipped scaffold truth from decorative pattern labels.
- [x] When an adopter inspects the shipped examples, they can see how Wrapper, Reviewer, or Pipeline map into concrete repository surfaces.

End-to-end scenario: a maintainer adopts the template, sees a real wrapper or reviewer or pipeline scaffold in the shipped assets, can trace its execution boundary through docs plus validator rules, and does not mistake deferred patterns like Inversion for supported runtime power.

Agent cannot verify yet: whether future adopters will keep Reviewer as a starter scaffold or pull parts of it upward into repository-specific role strategy, because that still depends on local review architecture.

---

## Progress Unit, Checkpoint, And Closeout Boundary

Because the next wave is a while-style multi-file implementation task, the execution plan must freeze these boundaries now.

### Progress Unit

One absorbed scaffold family made real end-to-end.

Examples:

1. Wrapper contract plus template plus validator plus test
2. Reviewer scaffold plus example plus validator plus test
3. Pipeline scaffold plus helper plus validator plus test

### Progress Checkpoint

A progress update is allowed after one scaffold family is fully documented, wired, and validated.

### True Closeout Boundary

The implementation wave is only complete when:

1. the selected scaffold families are shipped
2. Generator and Inversion boundaries are documented honestly
3. bootstrap, validator, tests, and adopter-facing docs all agree on the same truth

---

## Non-Goals And Stop Conditions

### Non-Goals

1. do not create a new required `pattern` field in the canonical SKILL contract
2. do not claim support for Inversion without a host-runtime contract and degradation path
3. do not ship Generator as an unbounded content-authoring abstraction
4. do not treat discussion consensus as proof until bootstrap, validator, and tests agree

### Stop Conditions

Stop and re-open design discussion before implementation if any of these becomes true:

1. Reviewer cannot be placed honestly without collapsing strategy and mechanism into one surface
2. Wrapper requires runtime power the template still cannot describe truthfully
3. Generator pressure expands beyond bounded artifact generation before validator-backed contracts exist
4. the implementation wave needs a broader workflow engine rather than bounded staged scaffolds

---

## Source Discussion

Primary design packet:

1. `tmp/discussion/skill_five_patterns_execution_adoption_v1/discussion_packet.md`

Local summary doc:

1. `docs/archive/SKILL_Five_Pattern_Discussion_2026-04-07.md`