## Hostile Acceptance Review — skill_five_pattern_acceptance_desync_v1

---

## Verdict: `CONDITIONAL`

The wave is structurally coherent and passes its own tests. It is not a FAIL. But it is not a PASS — three concrete upper/lower mismatches outrun the shipped mechanical proof surface.

---

## Findings (top 5, severity order)

---

### Finding 1 — CRITICAL
**category:** rule-execution gap / validator blind spot  
**files:** `docs/SKILL_MECHANISM_V1_DRAFT.md` lines ~288+ | `scripts/validate_template.py` | `tests/test_validate_template.py`

SKILL_MECHANISM_V1_DRAFT declares 6 conditions the validator "should hard-fail" on. The validator enforces only 3:

| Condition | Enforced? |
|---|---|
| 1. Required core fields missing | ✓ |
| 2. Trigger conditions too weak to be actionable | **✗ no check** |
| 3. Named reference does not resolve | ✓ |
| 4. Runtime behavior claimed without matching degradation | **✗ no check** |
| 5. entry_instructions inlines what should stay in references | **✗ no check** |
| 6. Receipt matrix missing promotion_tier or invalid values | ✓ |

A repo can have governance-theater triggers, undeclared runtime behavior, and fat entry_instructions — pass all tests — and the constitutional doc claims these are mechanically blocked.

**Smallest honest fix:** Downgrade SKILL_MECHANISM_V1_DRAFT.md language to explicitly split: "mechanically enforced: (1)(3)(6); reviewer-bound, not mechanically enforced: (2)(4)(5)." Or implement the three missing checks with test coverage.

---

### Finding 2 — HIGH
**category:** doc-overclaim / validator blind spot  
**files:** `templates/skill_artifact_generator.template.md` | `docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md` | `scripts/validate_template.py`

The template and execution-layer doc promise "schema backing" and say the generator "must stop if artifact lacks stable schema or **validator-visible path**." The validator's actual check: does the bullet text `Artifact Contract` appear? Nothing verifies a schema object exists, a schema path resolves, or what "validator-visible path" even means. The term is undefined anywhere in the codebase. Any free-form text under "Artifact Contract" passes.

**Smallest honest fix:** Replace "schema-backed" with "contract-backed" and drop "validator-visible path" unless a real schema-path resolution check is implemented.

---

### Finding 3 — HIGH
**category:** bootstrap mismatch / doc-overclaim  
**files:** `docs/ADOPTION_GUIDE.md` lines ~432-437 | `scripts/validate_template.py` REQUIRED_FILES | `tests/test_bootstrap_adoption.py`

ADOPTION_GUIDE tells adopters: *"run the structured validator from the repo root to confirm no required files are missing."* The validator's REQUIRED_FILES contains ~112 paths that exist only in the source template repo (`examples/reviewer_roles/`, `tests/`, multiple CI workflows, etc.). A standard-profile bootstrapped adopter repo has ~47 files. Running the validator as instructed produces a hard-failure cascade with no fault on the adopter.

**Smallest honest fix:** Add one sentence to ADOPTION_GUIDE: "validate_template.py targets the source template repository; standard/minimal profile adopter repos do not satisfy its REQUIRED_FILES check." Or add profile-aware guard logic in the validator.

---

### Finding 4 — MEDIUM
**category:** bootstrap mismatch  
**files:** `scripts/bootstrap_adoption.py` | `tests/test_bootstrap_adoption.py`

Tests show standard profile distributes examples 01-06; full profile "adds" examples 01-02 — which standard already distributed. Either a test description error, or the full profile's path list silently duplicates standard entries. Either way, the profile tier ownership of examples is undocumented and unasserted as non-overlapping.

**Smallest honest fix:** Add explicit comment block in bootstrap_adoption.py mapping each example file to exactly one profile tier. Add a test asserting no path appears in two tiers' exclusive lists.

---

### Finding 5 — MEDIUM
**category:** doc-overclaim / layer bleed  
**files:** `docs/SKILL_MECHANISM_V1_DRAFT.md` | `docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md` | `docs/ADOPTION_GUIDE.md` | `templates/` (4 files) | `examples/skills/03-06`

Upper docs consistently say "five-pattern scaffold." Lower layer ships 4 new starter templates + 4 new examples (03-06). The fifth pattern (base canonical skill) has no `skill_canonical.template.md`, does not share the four-template structural convention, and is a constitutional anchor — not a symmetric peer. An adopter expecting five symmetric patterns finds four templates and an asymmetric anchor. The asymmetry is undocumented.

**Smallest honest fix:** Change "five patterns" in docs to "four scaffold patterns plus the base canonical skill contract." Or ship a fifth starter template to make it symmetric.

---

## Residual Risks (even with fixes applied)

1. **Governance theater is never fully mechanically blocked** — the instruction-bound tier remains structurally weaker; Finding 1 gaps are the widest opening.
2. **Promotion tier enforcement has no time dimension** — the validator cannot verify that a promotion receipt existed before a canonical mutation in git history.
3. **Example drift accumulates silently** — validator checks bullet presence, not that bullets are meaningfully filled vs. left as placeholder text.
4. **Bootstrap project-type detection is brittle** — file-presence heuristics misfire on monorepos; wrong preset silently populates wrong toolchain surfaces, which pass on structure alone.
5. **Harvest loop end-to-end is untested in an adopter repo** — round-trip test confirms script behavior only; generated artifacts are not confirmed to survive validator or promotion review.

---

## Final Recommendation: `accept-with-fixes`

**Must fix before freeze:**
- Finding 1 — downgrade the false mechanical claim about conditions 2/4/5, or implement them
- Finding 3 — qualify the ADOPTION_GUIDE "run the validator" instruction to the correct scope

**Should fix:**
- Finding 2 — remove "schema-backed" overclaim or implement it

**Log and address later:**
- Findings 4 and 5 — profile layering doc + five-pattern naming alignment

Do not reroute. The fixes are targeted and require no redesign — localized wording changes and one validator scope guard.
