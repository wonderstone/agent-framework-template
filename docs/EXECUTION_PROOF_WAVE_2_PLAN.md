# Execution Proof Wave 2 Plan

This document freezes the second implementation wave for downstream execution support.

Wave 1 proved strict adoption status and Developer Toolchain runtime evidence.

Wave 2 closes the next three gaps that still let downstream agents say the template defined the right behavior but did not ship enough execution surfaces to carry it out directly.

---

## Goal

Ship the smallest second wave that makes three execution-layer promises real:

1. a declared Developer Toolchain surface can be selected and run through one machine-facing entrypoint
2. independent evaluation can produce bounded request and verdict artifacts instead of relying on prose-only policy
3. local multi-executor review can be configured, probed, and dispatched through a durable packet rather than ad hoc shell memory

Wave 2 must preserve the same governance boundary as Wave 1:

1. do not auto-upgrade canonical truth from runtime artifacts
2. do not let the implementing executor self-certify independent evaluation
3. do not let local executor automation silently erase unavailable, failed, or partial review states

---

## Scope

Wave 2 includes exactly these surfaces:

| Surface | Status in Wave 2 | Purpose |
|---|---|---|
| `docs/EXECUTION_PROOF_WAVE_2_PLAN.md` | add | freeze the second execution-proof wave and its boundaries |
| `scripts/developer_toolchain_runner.py` | add | give agents one machine-facing surface to list, inspect, and run declared Developer Toolchain entries |
| `templates/developer_toolchain_run_receipt.template.md` | add | canonical receipt for one executed Developer Toolchain run |
| `scripts/evaluation_pipeline.py` | add | generate independent-evaluation request and report artifacts |
| `templates/evaluation_request.template.md` | add | canonical evaluator request artifact |
| `templates/evaluation_report.template.md` | add | canonical evaluator verdict artifact |
| `scripts/review_dispatch.py` | add | probe and dispatch local executor reviews into durable packetized outputs |
| `templates/local_executor_registry.template.json` | add | machine-local registry for declared review executors |
| `templates/review_dispatch_packet.template.md` | add | canonical packet for executor availability and review dispatch outputs |
| bootstrap manifest contract | extend | declare runner, evaluator, and executor-review-loop contracts for adopters |
| `scripts/validate_template.py` | extend | validate the new scripts, templates, manifest shape, and example adopter surfaces |
| tests | add and extend | lock the new execution surfaces in place |

Wave 2 explicitly defers these surfaces:

| Deferred surface | Why deferred |
|---|---|
| task-control state machine | larger behavioral surface than this wave needs |
| execution readiness audit | easier to add after runner and executor registry exist |
| freshness downgrade audit | depends on real receipt cadence first |
| SKILL runtime router | governance-sensitive and still downstream-optional |

---

## Design Decisions

### 1. Developer Toolchain should become machine-consumable, not only human-readable

Wave 2 adds a runner that reads the same adapter table as the probe script.

The runner should:

1. list declared surfaces
2. show one surface with its status, scope, and stop rule
3. run one surface through a stable command entrypoint
4. emit a run receipt instead of mutating canonical status
5. refuse `known-broken` surfaces unless the operator explicitly overrides that guard

### 2. Independent evaluation needs a bounded artifact pair

Wave 2 adds an evaluation pipeline that creates exactly two artifacts:

1. evaluator request
2. evaluator report

The pipeline should make Rule 26 executable without pretending it can prove actual evaluator independence from shell metadata alone.

The artifacts should therefore record:

1. generator identity
2. evaluator identity
3. UAC focus
4. allowed review scope
5. PASS / CONDITIONAL / FAIL verdict
6. gap check and evidence anchors

### 3. Local CLI review should become a configured runtime surface

Wave 2 adds a local executor registry plus a dispatch script.

The dispatch layer should:

1. probe executor availability
2. dispatch the same prompt to each available executor through a declared command template
3. capture stdout and stderr in raw artifacts
4. record `available`, `unavailable`, `dispatch-failed`, and `completed` distinctly
5. preserve append-only packet truth instead of hiding incomplete review state

---

## Execution Plan

### Step 1 — Add Wave 2 docs and templates

Acceptance target:

1. docs index includes the new TYPE-A document
2. the new runner, evaluator, and review-dispatch templates exist

### Step 2 — Implement `developer_toolchain_runner.py`

Acceptance target:

1. it can list and inspect surfaces from the project adapter
2. it can run a declared surface and write a run receipt
3. it does not silently ignore `known-broken` status

### Step 3 — Implement `evaluation_pipeline.py`

Acceptance target:

1. it can generate an evaluator request artifact
2. it can generate an evaluator report artifact with PASS / CONDITIONAL / FAIL
3. it records UAC coverage and gap-check fields explicitly

### Step 4 — Implement `review_dispatch.py`

Acceptance target:

1. it can read a local executor registry
2. it can probe executor availability honestly
3. it can dispatch a review prompt and capture raw stdout or stderr per executor
4. it can write one durable packet describing the run

### Step 5 — Extend bootstrap, manifest, validator, and tests

Acceptance target:

1. bootstrapped standard and full adopters receive the new scripts, templates, and registry file
2. the adopter manifest exposes explicit contract sections for the new Wave 2 surfaces
3. validation catches missing or malformed Wave 2 assets mechanically
4. tests cover runner, evaluation pipeline, review dispatch, bootstrap, and validator regressions

---

## Manifest Extensions

Wave 2 adds three new manifest sections.

| Section | Minimum fields |
|---|---|
| `developer_toolchain_runner_contract` | `version`, `receipt_output_dir`, `allow_known_broken_override` |
| `independent_evaluation_contract` | `version`, `request_template`, `report_template`, `allowed_verdicts` |
| `executor_review_contract` | `version`, `registry_path`, `packet_output_dir`, `require_raw_outputs` |

Wave 2 also extends `strict_adoption_contract.required_mechanism_ids` so strict adopters must ship the runner, independent-evaluation pipeline, and local executor review loop when they claim the full strict baseline.

---

## User Acceptance Criteria

| ID | Criterion |
|---|---|
| UAC-1 | When a standard or full adopter is bootstrapped, it receives the runner, evaluation, and executor-review-loop assets plus manifest contract sections for each |
| UAC-2 | When a maintainer runs the Developer Toolchain runner, the repository receives a durable run receipt for the selected surface |
| UAC-3 | When a maintainer initializes and records an independent evaluation, the repository receives bounded request and report artifacts with explicit verdict fields |
| UAC-4 | When a maintainer probes and dispatches local executor review, the repository receives a durable packet that records availability and raw output paths honestly |
| UAC-5 | When validation runs against the template repo or a bootstrapped adopter, missing Wave 2 execution assets are detected mechanically |

End-to-end scenario:

a maintainer bootstraps a standard adopter, runs the Developer Toolchain runner for one surface, opens an evaluation request and report for non-trivial work, dispatches one local review loop through the executor registry, and then runs the validator to confirm the Wave 2 surfaces are structurally present.

---

## Governance Boundaries

Wave 2 must keep these boundaries intact:

1. runner receipts and probe receipts do not rewrite project-context status automatically
2. evaluation artifacts do not prove independence by fiat; they expose identities and verdicts for later audit
3. review dispatch packets must preserve unavailable and failed executor states rather than collapsing them into success
4. none of the new scripts may mutate canonical SKILL truth or promotion receipts