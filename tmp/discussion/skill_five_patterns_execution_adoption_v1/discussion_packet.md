# Discussion Packet — skill_five_patterns_execution_adoption_v1

- Generated at: 2026-04-07T08:15:57.727514+00:00
- Owner: main-thread
- Current round goal: Obtain enough judgment to freeze a plan
- Round exit rule: Freeze a plan, narrow to a sharper second round, or stop on missing truth

## Decision Question

How should the template absorb Google's five SKILL design patterns while keeping the execution layer concrete, reusable, and adopter-useful rather than abstract?

## Why This Needs Discussion

The user believes the template's SKILL layer is still weak, especially when it drifts into abstraction without enough execution substance. Recent Google Cloud guidance adds five concrete SKILL design patterns that may help correct that weakness if absorbed honestly.

## Current Truth

The template now has a canonical SKILL contract, a harvest loop, and a first shipped execution layer with invocation receipts, lineage-aware candidate artifacts, bootstrap coverage, validator coverage, and adopter round-trip proof. But it still risks staying too abstract: there is not yet a clear framework-level mapping from concrete SKILL patterns such as Tool Wrapper, Generator, Reviewer, Inversion, and Pipeline into shipped template surfaces that future repositories can adopt directly.

## Constraints

Be critical, not promotional. Do not assume every pattern deserves first-class treatment. Separate pattern-level guidance from execution-layer truth. The answer must be useful to future adopted repositories, not only to this template repo. Prefer small, enforceable, and bootstrap-shippable surfaces over abstract pattern taxonomies. Preserve truthful governance boundaries and do not invent runtime power the template does not yet have.

## Candidate Directions

Direction A: document the five patterns as guidance only, without changing shipped template surfaces. Direction B: map the five patterns into new or updated canonical SKILL types, templates, examples, and validator rules. Direction C: map the five patterns into execution-layer artifacts, host-facing contracts, and workflow helpers so adopters get concrete execution scaffolding. Direction D: combine B and C in a staged way: some patterns become canonical design guidance, others become execution-side scaffolds, and some remain examples only. Direction E: reject parts of the five-pattern set that are too runtime-specific or too abstract for a reusable template.

## Evaluation Criteria

Does the proposal reduce abstraction drift? Does it give adopters concrete reusable surfaces instead of vague advice? Does it keep SKILL governance truthful? Does it strengthen execution-layer usefulness materially? Can it be bootstrapped, validated, and explained without pretending unsupported automation exists?

## Suggested Executors

Claude CLI; Codex CLI; Gemini CLI; GitHub Copilot CLI; main-thread synthesis

## Instructions For Participating Executors

1. Read the packet before commenting.
2. Do not rewrite the packet body unless the main thread asks for it.
3. Append your feedback at the end of this file.
4. Prefer concrete tradeoffs, risks, and missing evidence over style opinions.
5. If another round is needed, propose the narrowest next question.

## Main-Thread Decision Status

- Current status: closed
- Final decision: freeze-plan

## Append-Only Discussion Log

<!-- Append feedback and synthesis entries below this line. -->

### GitHub Copilot CLI — 2026-04-07

1. **Verdict**

Absorb the five patterns asymmetrically and mostly below the constitutional SKILL layer. Do **not** turn them into new first-class canonical SKILL types or a broad pattern catalog. The template should only promote patterns that can ship as concrete, bootstrapable execution surfaces with validator-visible truth. In practice that means: Tool Wrapper, Reviewer, and Pipeline are worth shipping as execution-layer scaffolds; Generator should stay example-first until the template can validate bounded input/output contracts honestly; Inversion should be rejected or deferred because the current repo does not yet have a truthful host-runtime surface for it.

2. **Top 3 findings**

- **Finding 1**
  - **category:** execution gap
  - **why it matters:** The repo's current weakness is not lack of SKILL vocabulary; it is lack of pattern-specific execution scaffolding that adopted repos can actually run. If these five patterns land only as docs, enums, or example names, the template gets more abstract while adopters still get the same thin execution layer.
  - **smallest honest next step:** Pick at most three patterns with immediate shipped value — Tool Wrapper, Reviewer, Pipeline — and require each one to earn template status only if it ships with all four surfaces: a starter template or helper, an adoption-guide path, a validator check, and one adopter-round-trip example.

- **Finding 2**
  - **category:** governance fit
  - **why it matters:** The canonical SKILL contract is already load-bearing around `purpose`, `triggers`, `entry_instructions`, `references`, `governance`, and `degradation`, with per-field promotion authority. Recasting the five patterns as new canonical SKILL types or normative control fields would blur the existing authority model and create a second taxonomy that is easier to gesture at than to govern truthfully.
  - **smallest honest next step:** Keep the canonical contract unchanged in v1. If pattern identity is needed at all, treat it as non-authoritative example labeling or optional execution metadata outside the constitutional field set, not as a new required canonical field.

- **Finding 3**
  - **category:** bootstrapability
  - **why it matters:** The five patterns do not deserve equal framework weight. Tool Wrapper, Reviewer, and Pipeline already map onto repo surfaces the template can ship honestly: Developer Toolchain commands, evaluator or audit roles, and packet or receipt workflows. Generator and especially Inversion do not yet have equivalent bounded, validator-friendly template surfaces, so elevating them now would over-promise runtime power and weaken adopter trust.
  - **smallest honest next step:** Stage the adoption explicitly: Wrapper around declared toolchain commands first; Reviewer around independent evaluation receipts second; Pipeline around bounded multi-step helpers third; Generator only as one tightly scoped example backed by a real artifact template; Inversion deferred until the repo can name a concrete host-facing contract and fallback behavior.

3. **Pattern mapping table**

| Pattern | Mapping | Reason |
|---|---|---|
| Tool Wrapper | execution scaffold | Best fit for the repo's existing Developer Toolchain surface: ship wrappers that bind a skill to declared commands, evidence, fallback, and validation rather than inventing a new canonical type. |
| Generator | example only | Useful in bounded cases, but too easy to make vague; keep it tied to concrete artifact generation examples until the template can validate declared input/output contracts honestly. |
| Reviewer | execution scaffold | Already aligned with the repo's independent-evaluation, audit-receipt, and reviewer-role machinery, so this can become a real reusable execution surface. |
| Inversion | reject | Too runtime- and host-specific for the current template; adopting it now would imply orchestration power and control inversion surfaces the repo does not actually ship. |
| Pipeline | execution scaffold | The repo already has packet, receipt, and helper-script patterns that can become a bounded staged-execution scaffold without pretending to be a general workflow engine. |

4. **One thing this template must not do**

It must not add a five-pattern catalog to the canonical SKILL contract and call that "adoption" while shipping no new helper, validator, or bootstrap surface for the chosen patterns.

5. **Final recommendation**

`freeze-plan`

### GitHub Copilot CLI — 2026-04-07 (fresh pass)

1. **Verdict**

Absorb the five patterns unevenly and mostly as shipped execution scaffolding, not as new canonical SKILL law. The template should only promote a pattern when it can ship a bootstrapable helper surface, validator-visible truth, and an adopter-useful execution path. On that test, Tool Wrapper, Reviewer, and Pipeline are worth absorbing into the execution layer; Generator should stay example-only for now; Inversion should be deferred or rejected until the framework has a truthful host-runtime contract for it.

2. **Top 3 findings**

- **Finding 1**
  - **category:** execution gap
  - **why it matters:** The current weakness is not that the template lacks pattern names. It is that adopters still do not get enough concrete execution scaffolding from the SKILL layer. If the five patterns become mostly documentation or taxonomy, the template gets broader while the execution layer stays thin.
  - **smallest honest next step:** Treat Tool Wrapper, Reviewer, and Pipeline as opt-in execution-layer scaffolds only if each ships with a concrete template/helper surface, validator coverage, bootstrap wiring, and one adopter round-trip example.

- **Finding 2**
  - **category:** governance fit
  - **why it matters:** The canonical SKILL contract is already carrying real governance load through required fields and field-level promotion authority. Adding the five patterns as new canonical classes or required metadata would create a second control vocabulary without improving truthfulness, and would make it easier for adopters to claim pattern support without shipping any real execution surface.
  - **smallest honest next step:** Keep the canonical contract unchanged in v1. If pattern identity is recorded at all, keep it outside the constitutional field set as optional execution metadata or example labeling.

- **Finding 3**
  - **category:** adopter utility
  - **why it matters:** The patterns are not equally portable. Tool Wrapper maps cleanly to declared Developer Toolchain surfaces. Reviewer maps to the repo's existing evaluator and audit machinery. Pipeline maps to bounded helper-driven staged execution. Generator and Inversion are much easier to oversell than to validate, so promoting them too early would weaken adopter trust.
  - **smallest honest next step:** Freeze a staged plan: Wrapper first, Reviewer second, Pipeline third; keep Generator in examples until bounded input/output contracts are shippable; defer Inversion until the host-facing contract and degradation path are explicit.

3. **Pattern mapping table**

| Pattern | Mapping | Reason |
|---|---|---|
| Tool Wrapper | execution scaffold | Strongest fit for the existing Developer Toolchain and execution-receipt model; can ship as a real wrapper around declared commands, evidence, and fallback. |
| Generator | example only | Still too easy to make abstract; keep it confined to bounded artifact-generation examples until the template can validate input/output truth honestly. |
| Reviewer | execution scaffold | Already fits independent evaluation, audit receipts, and reviewer-role machinery, so it can become a concrete reusable execution surface. |
| Inversion | reject | The template does not yet ship a truthful host-runtime control surface for inversion; promoting it now would imply orchestration power the framework does not have. |
| Pipeline | execution scaffold | Best treated as a bounded staged-execution helper built from packets, receipts, and validator-aware step boundaries, not as a generic workflow engine. |

4. **One thing this template must not do**

It must not turn the five patterns into a canonical pattern catalog or required SKILL metadata while leaving adopters with no new helper, validator, or bootstrap surface they can actually use.

5. **Final recommendation**

`freeze-plan`

---

## Feedback — Round 1 — Gemini CLI

- Timestamp: 2026-04-07T08:29:34.597369+00:00
- Stance: freeze-plan
- Summary: Absorb the five patterns mainly as concrete execution scaffolds rather than enlarging the canonical SKILL contract; ship only the patterns that can be validated and immediately useful to adopters.

### Strengths

- Pushes the template toward tangible adopter utility rather than abstract taxonomy.\n- Strongly protects the canonical SKILL contract from decorative pattern inflation.

### Risks

- Deferring Inversion may leave one Google pattern unabsorbed for now.\n- Keeping Generator example-only may feel conservative unless later rounds add bounded I/O validation.

### Open Questions

- Whether Generator should later graduate from example-only to execution scaffold once the template can validate bounded artifact contracts.

### Recommended Next Step

- Promote Tool Wrapper, Reviewer, and Pipeline only if each ships with a helper surface, bootstrap path, validator coverage, and adopter proof.

---

## Feedback — Round 1 — Codex CLI

- Timestamp: 2026-04-07T08:29:35.184705+00:00
- Stance: freeze-plan
- Summary: Do not absorb the five patterns as new canonical SKILL taxonomy; only Tool Wrapper, Generator-in-a-narrow-form, and Pipeline should become execution scaffolds, while Reviewer stays example-only or governance-adjacent and Inversion is rejected for now.

### Strengths

- Sharp focus on bootstrapability and validator-visible truth.\n- Rejects decorative pattern catalogs with no shipped executors or helpers.

### Risks

- Places Reviewer closer to role or governance surfaces than other executors did, which may create a sequencing dispute.\n- Narrowing Generator to artifact generation may under-fit broader authoring use cases.

### Open Questions

- Whether Reviewer belongs as an execution scaffold because the repo already has reviewer-role and evaluation machinery, or should stay example-only to avoid contract blur.

### Recommended Next Step

- Freeze a rule that no pattern becomes template-canonical unless it ships a bootstrap artifact, an execution scaffold, and a validator-visible truth surface.

---

## Feedback — Round 1 — Claude CLI

- Timestamp: 2026-04-07T08:30:00+00:00
- Stance: stop
- Summary: Claude CLI was invoked twice in non-interactive mode for this round but did not return a usable answer before timing out or blocking on interactive input, so this executor did not provide a trustworthy design judgment.

### Strengths

- The repo's local Claude installation and account login were confirmed before execution.

### Risks

- Treating a timed-out or interaction-blocked run as real design feedback would pollute the round with fake consensus.

### Open Questions

- Whether this repository should standardize a more robust machine-local Claude discussion wrapper before the next multi-CLI round.

### Recommended Next Step

- Record the failed executor honestly and proceed with synthesis from the usable executor outputs.

---

## Main-Thread Synthesis — Round 1

- Timestamp: 2026-04-07T08:33:25.137961+00:00
- Decision: freeze-plan
- Confidence: High
- Next action: Freeze the next implementation wave around Wrapper, Reviewer, and Pipeline as candidate execution-layer scaffolds; keep Generator bounded and defer Inversion until a host-runtime contract exists.

### Summary

The usable round-one feedback converged on one core point: the template should not absorb Google's five SKILL patterns as a new canonical taxonomy. Instead, it should absorb them asymmetrically and only where they can become concrete, bootstrap-shippable, validator-visible execution scaffolds for adopted repositories. Tool Wrapper and Pipeline are the strongest candidates for direct execution-layer adoption. Reviewer also has strong support as an execution scaffold because the repo already ships reviewer roles, independent evaluation, and audit receipts, though one executor argued it should stay governance-adjacent. Generator should stay bounded: either example-only or a narrow artifact-generation scaffold. Inversion should be deferred or rejected until the template has a truthful host-runtime control contract and degradation path.

### Rationale

The repo's known failure mode is abstraction drift: adding pattern vocabulary without adding real execution substance. All usable feedback rejected that failure mode directly. No executor argued for adding a required pattern catalog or new canonical SKILL metadata. The consensus was that the existing canonical SKILL contract should remain constitutional, while pattern absorption should happen mostly underneath it through helper scripts, wrappers, validator-backed scaffolds, examples, and execution receipts. The main disagreement was only degree: whether Reviewer belongs as a first-class execution scaffold and whether Generator is merely example-only or can survive as a narrow artifact-generation scaffold. That disagreement is small enough to freeze a staged plan without another broad round. Claude CLI was invoked but did not return a usable non-interactive response in this round, so the synthesis is based on the three usable executor outputs plus the independent Copilot CLI pass already appended to the packet.

### Follow-Up Questions

- Should Reviewer be formalized as an execution scaffold in the SKILL layer, or remain attached to role strategy plus audit machinery?\n- Can Generator graduate from example-only to a narrow artifact-generation scaffold if tied to packet or receipt generators and validator-backed output contracts?\n- What is the smallest truthful wrapper contract that lets adopted repos bind skills to Developer Toolchain commands without inventing fake host automation?

### Main-Thread Closeout

- Timestamp: 2026-04-08T00:00:00+00:00
- Status: closed
- Final decision: freeze-plan
- Durable output: `docs/SKILL_FIVE_PATTERN_EXECUTION_PLAN_V1.md` and `docs/archive/SKILL_Five_Pattern_Discussion_2026-04-07.md`

Round 1 produced enough usable judgment to freeze the next execution wave without opening a narrower second round. The durable outcome of this discussion is a doc-first implementation plan that keeps the canonical SKILL contract free of decorative pattern metadata, stages Wrapper, Reviewer, and Pipeline as concrete scaffold candidates, keeps Generator bounded, and defers Inversion until a truthful host-runtime contract exists.
