# Template Surface Rationalization Audit v1

## Goal

Identify which current agent-framework-template surfaces now look too heavy, too historical, or too weakly tiered for day-one adoption, while preserving the mechanism families that still matter.

## Summary Judgment

The template's main problem is no longer missing mechanism coverage.

The bigger product problem is tier clarity:

1. too many advanced or historical surfaces visually sit next to the true default baseline
2. adopter-facing docs still make the standard profile feel broader than most repositories really need on day one
3. several design-history documents remain valuable, but they now read like shipped obligations unless the reader already understands the framework's internal layering

## What Still Feels Right

These surfaces still look like strong defaults:

1. project adapter plus Developer Toolchain truth
2. execution contract for non-trivial work
3. resumable packet / receipt / handoff path
4. progress receipt plus drift reconciliation for long-running work
5. truthful closeout and validation audits
6. now, goal-framing contract on reusable execution artifacts

These are the mechanism-layer assets that most directly change agent behavior.

## Main Rationalization Findings

### 1. Standard profile still reads wider than its real day-one baseline

Even after adding a lean-baseline explanation, the standard profile still ships a large set of docs, templates, skills, examples, and review surfaces.

This is useful for a framework repository, but it makes adopters overestimate what is immediately required.

Recommended product stance:

1. keep shipping the richer standard profile
2. but present it in docs as `core default + optional families already included`, not as one flat required bundle

### 2. Reference-heavy docs need stronger visual downgrading

The following classes are still valuable but should read as reference or upgrade-path surfaces first:

1. `*_V1_DRAFT.md`
2. `*_DISCUSSION.md`
3. `EXECUTION_PROOF_WAVE_*`

They contain important rationale, but they are not the first surfaces most adopters should read to start using the framework honestly.

### 3. Root validator self-hosting and adopter guidance are easy to mentally conflate

The template root still validates a broad self-hosted product surface.

That is fine for this repository itself, but readers can misread the root-required file set as the required day-one set for adopters.

Recommended product stance:

1. keep strict self-hosting validation at the template root
2. but keep clarifying in adopter docs that adoption baseline is smaller than root self-hosting completeness

### 4. Some high-value mechanisms were previously under-mechanized while low-frequency rationale remained verbose

InfoWeave exposed this asymmetry clearly:

1. goal framing on reusable execution artifacts was missing as a mechanical default
2. meanwhile multiple historical rationale docs were already present and detailed

The recent fix improves this balance, but the broader lesson remains:

Mechanism-critical gaps should outrank adding more design-history prose.

## Immediate Changes Already Landed

This audit cycle already applied these corrections:

1. core reusable execution artifacts now carry `Goal`, `Phase Plan`, `Current Step`, `Step Contribution`, and `Progress State`
2. the template now ships `scripts/goal_framing_audit.py`
3. bootstrap, validator coverage, and focused tests now include the new goal-framing surfaces
4. adopter-facing docs now explicitly describe a lean baseline instead of implying that every shipped surface is equally day-one important
5. adopter-facing docs now explicitly classify `*_V1_DRAFT.md`, `*_DISCUSSION.md`, and `EXECUTION_PROOF_WAVE_*` as reference-heavy by default

## Recommended Next Cleanup Wave

### A. Re-tier docs in the index

Add explicit tags or grouped sections such as:

1. `Start here`
2. `Core default mechanisms`
3. `Advanced optional families`
4. `Reference and design history`

This is likely the highest-value next cleanup because it changes first impressions without deleting useful material.

### B. Stop listing large flat file inventories when a tiered summary would do

The adoption guide still contains long inventories that are accurate but cognitively heavy.

Recommended direction:

1. keep one small `copy these first` section
2. collapse the rest into grouped optional families
3. point to the index for the long tail instead of inlining the whole catalog repeatedly

### C. Consider downgrading some proof-wave and discussion docs from required root sections to indexed references only

This should be done carefully because the repository may still want them for self-hosted product truth.

But if they are kept, they should be visually treated as rationale/reference first.

### D. Add one explicit product statement: the framework optimizes for truthful mechanism families, not minimum file count

This would help set expectations.

The current risk is that readers interpret the template as indiscriminately large, when the real intent is to ship a broad toolbox with a smaller honest default.

## Non-Goals For This Audit

This audit does not recommend:

1. deleting major mechanism families blindly
2. collapsing all advanced execution surfaces into one generic doc
3. weakening validator or closeout truthfulness just to shorten the repo

The problem is not that the template became too strict.

The problem is that strict mechanism defaults and optional reference-heavy surfaces were not clearly separated enough.

## Recommended Product Direction

Keep the framework broad, but make its tiers much more obvious:

1. small honest default
2. advanced mechanism families by operating model
3. reference-heavy design history clearly marked as such

That direction preserves the useful parts of the template while reducing the sense that every adopter must absorb the full design archive before doing useful work.