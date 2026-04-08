# Execution Proof Wave 1 Plan

This document freezes the first implementation wave that turns the framework's downstream execution-support discussion into concrete shipped surfaces.

It exists to solve one specific problem:

downstream project agents should not be able to reasonably say that the template defined governance and design intent but failed to provide enough execution-layer tooling to carry that intent out honestly.

This is an executable plan, not a blue-sky discussion note.

---

## Goal

Ship the smallest first wave that materially improves downstream execution proof without weakening the framework's current governance boundary.

Wave 1 should:

1. let adopters prove what strict-adoption status they honestly reached
2. let adopters prove whether declared Developer Toolchain surfaces actually ran recently
3. avoid creating an autonomous runtime that mutates canonical truth on its own

Wave 1 should not:

1. invent a full always-on runtime scheduler
2. auto-promote canonical SKILL mutations
3. make minimal adopters carry the full strict-execution surface by default

---

## Scope

Wave 1 includes exactly these implementation surfaces:

| Surface | Status in Wave 1 | Purpose |
|---|---|---|
| `docs/EXECUTION_PROOF_WAVE_1_PLAN.md` | add | freeze the first implementation wave and its boundaries |
| `scripts/strict_adoption_audit.py` | add | generate an evidence-backed strict adoption verdict and packet |
| `templates/adoption_verification_packet.template.md` | add | canonical packet for strict-adoption proof |
| `scripts/developer_toolchain_probe.py` | add | run declared Developer Toolchain commands and record probe receipts |
| `templates/developer_toolchain_probe_receipt.template.md` | add | canonical receipt for runnable Developer Toolchain evidence |
| bootstrap manifest contract | extend | declare strict-adoption and toolchain-probe contract fields for adopters |
| `scripts/validate_template.py` | extend | validate the new scripts, templates, manifest shape, and adopter-side required files |
| tests | add and extend | lock the new execution-proof surfaces in place |

Wave 1 explicitly defers these surfaces:

| Deferred surface | Why deferred |
|---|---|
| Developer Toolchain runner | useful, but probe receipts come first and are lower-risk |
| Independent evaluation pipeline | high value, but larger surface area than Wave 1 |
| Local executor registry / review dispatcher | depends on machine-local variability and is better after strict adoption packets exist |
| Execution session initializer | useful, but downstream proof and toolchain truth are more urgent |
| SKILL runtime router | governance-sensitive and should follow execution-proof basics |

---

## Design Decisions

### 1. Strict adoption should be attested, not narrated

Wave 1 adds a dedicated strict adoption audit script and packet.

The script should:

1. read the adopter manifest
2. inspect whether the required strict-baseline mechanism files exist
3. record which validation evidence and independent review artifacts were supplied
4. output one honest status:
   - `fully-adopted`
   - `partially-adopted`
   - `design-only-upgrade-path-kept`

The script must not infer `fully-adopted` from file presence alone.

### 2. Developer Toolchain status needs receipt-bearing runtime evidence

Wave 1 adds a probe script that runs declared Developer Toolchain surfaces and writes receipts.

The probe script should:

1. parse the project adapter's Developer Toolchain table
2. select one or more declared surfaces
3. run the declared command when the surface is not `not-applicable` and not explicit `none`
4. record the outcome, timestamp, previous declared status, and any fallback or stop rule
5. write a receipt instead of silently editing canonical project-context truth

Wave 1 treats receipts as runtime evidence, not canonical status mutation.

### 3. Bootstrap should ship the proof surfaces for standard and full adopters

Wave 1 extends bootstrap output so adopters on `standard` or `full` profiles receive:

1. the strict adoption auditor
2. the strict adoption packet template
3. the Developer Toolchain probe script
4. the Developer Toolchain probe receipt template
5. manifest contract fields that describe these surfaces

`minimal` should stay light unless future evidence says otherwise.

### 4. Validation should enforce structural truth, not semantic overclaim

Wave 1 extends validation to check that:

1. the new scripts and templates exist in the template repo
2. bootstrapped adopters that claim the new contracts actually ship the expected files
3. manifest shape remains explicit and machine-checkable

Wave 1 validation should not attempt to prove that a downstream repo's command outputs are semantically correct beyond what the probe receipts actually record.

---

## Execution Plan

### Step 1 — Add canonical docs and templates

Add the design doc and the two new templates.

Acceptance target:

1. docs index includes the new TYPE-A document
2. the adoption-verification packet template exists
3. the Developer Toolchain probe receipt template exists

### Step 2 — Implement `strict_adoption_audit.py`

Add a script that:

1. reads `.github/agent-framework-manifest.json`
2. consumes a strict-adoption contract section from the manifest
3. checks required mechanism IDs against explicit file mappings
4. records supplied validation evidence and independent-review artifacts
5. writes a verification packet
6. prints the packet path and exits non-zero only when the invocation itself is malformed, not merely because the repo is partially adopted

Acceptance target:

1. it can generate a packet for a bootstrapped adopter
2. the packet includes mechanism rows, evidence rows, and a final adoption verdict
3. it does not auto-upgrade missing evidence into `fully-adopted`

### Step 3 — Implement `developer_toolchain_probe.py`

Add a script that:

1. parses Developer Toolchain entries from `.github/instructions/project-context.instructions.md`
2. supports probing one named surface or all surfaces
3. skips explicit `none` and `not-applicable` surfaces honestly
4. runs the declared command using the repository root as working directory
5. writes one probe receipt with per-surface outcomes

Acceptance target:

1. it can probe a bootstrapped adopter with a real Developer Toolchain section
2. it records success, failure, skipped, and not-applicable states distinctly
3. it never edits the project adapter directly

### Step 4 — Extend bootstrap manifest and shipped assets

Extend manifest schema and standard/full bootstrap file sets to include:

1. `strict_adoption_contract`
2. `developer_toolchain_probe_contract`
3. the new scripts and templates in `expected_files`

Acceptance target:

1. bootstrapped adopters receive the files
2. manifest contract fields describe the new proof surfaces explicitly

### Step 5 — Extend validation and tests

Extend the validator and tests so the new surfaces are locked in.

Acceptance target:

1. root validation passes with the new files present
2. bootstrap tests assert the new assets and manifest contract
3. new script tests prove packet and receipt generation
4. adopter validation catches missing expected execution-proof assets

---

## Manifest Extensions

Wave 1 adds two new manifest sections for bootstrapped adopters.

### `strict_adoption_contract`

Minimum fields:

| Field | Meaning |
|---|---|
| `version` | contract version |
| `status_values` | allowed verdicts |
| `required_mechanism_ids` | strict-baseline mechanism IDs the auditor should evaluate |
| `verification_packet_path` | canonical output path for the adoption packet |
| `require_independent_review_for` | verdicts that require external review evidence |

### `developer_toolchain_probe_contract`

Minimum fields:

| Field | Meaning |
|---|---|
| `version` | contract version |
| `receipt_output_dir` | default receipt directory |
| `allowed_surface_kinds` | surfaces the probe may target |
| `record_freshness` | whether probe receipts are expected to carry timestamps for later freshness checks |

---

## Governance Boundaries

Wave 1 must preserve these boundaries:

1. strict adoption audit may classify but must not silently rewrite manifest claims
2. Developer Toolchain probe may record runtime evidence but must not auto-edit project-context status fields
3. neither script may mutate canonical SKILL files or promotion metadata
4. validation may hard-fail structural contradictions, but must not manufacture semantic success claims

---

## User Acceptance Criteria

| ID | Criterion |
|---|---|
| UAC-1 | When a standard or full adopter is bootstrapped, the new execution-proof scripts and templates are present in the target repository and declared in the adopter manifest |
| UAC-2 | When a maintainer runs the strict adoption auditor, the repository receives a durable packet that honestly classifies adoption status based on mechanism coverage and supplied evidence |
| UAC-3 | When a maintainer runs the Developer Toolchain probe, the repository receives a durable receipt showing which declared surfaces were run, skipped, or failed |
| UAC-4 | When validation runs against the template repo or a bootstrapped adopter, missing Wave 1 execution-proof assets are detected mechanically |

End-to-end scenario:

a maintainer bootstraps a standard adopter, runs the strict adoption auditor and Developer Toolchain probe from the target repository, receives a verification packet plus probe receipt, and then runs the validator to confirm the execution-proof surfaces are structurally present.

---

## Out Of Scope

Wave 1 does not yet implement:

1. automatic freshness downgrades of `verified-working`
2. an evaluator runtime for Rule 26
3. a generic multi-CLI executor registry
4. periodic harvest or self-review scheduling
5. a SKILL runtime router

Those are valid follow-up waves, but they should build on the proof surfaces shipped here rather than replace them.