# Goal Framing Contract Feedback From InfoWeave Rollout

## Summary

InfoWeave's repo-wide rollout exposed a template-level gap:

The framework ships strong execution-state and dispatch-handshake surfaces, but it does not yet make `overall goal -> current step -> step contribution -> progress state` a first-class, mechanically enforced contract across reusable execution artifacts.

That omission creates two practical problems during long, delegated, or resumed work:

1. downstream agents can keep executing with only local task text and lose the explicit relation between the current step and the overall goal
2. audit tooling can overfit filename heuristics and report false failures when artifact kinds are not classified precisely

This feedback proposes promoting goal framing into the template's default mechanism layer rather than leaving it as repo-local policy text.

## What Happened In InfoWeave

InfoWeave tightened execution governance so reusable packets, receipts, closeouts, and status snapshots explicitly carry:

1. Goal
2. Phase Plan
3. Current Step
4. Step Contribution
5. Progress State

The rollout found two repeatable lessons:

### 1. Docs-only governance was not enough

Changing docs and runbooks alone did not reliably influence later agents.

The contract only became durable after the repo also changed:

1. canonical templates
2. artifact-generation scripts
3. reusable packet assets already used as real entrypoints
4. audit tooling

This is a template concern, not just an adopter concern.

### 2. Artifact-kind audit must be precise

An early audit implementation treated any filename containing `packet` as a packet artifact.

That caused false failures for prompt files whose names also contained `packet`.

The reliable fix was to classify kinds using tighter rules such as:

1. canonical header detection
2. exact suffixes like `_packet.md`
3. explicit prompt/receipt/dispatch-receipt discrimination before fallback packet detection

This is also a template concern, because adopters will copy audit patterns if the template ships them.

## Current Template Gap

Relevant existing framework surfaces already exist, but they stop short of goal-framing enforcement.

Examples:

1. `templates/execution_progress_receipt.template.md` currently records summary, touched files, expected state effect, evidence, and notes, but not goal/phase/current-step/progress framing
2. `templates/managed_terminal_prompt_dispatch_receipt.template.md` records a strong handshake, but not the goal boundary being advanced or the current execution step inside the larger plan
3. `scripts/state_sync_audit.py` checks execution-state consistency, but the framework does not ship a dedicated goal-framing audit for packet/receipt/closeout/status artifacts

Result:

The framework helps preserve control and truthfulness, but it does not yet strongly preserve directional context during delegated execution.

## Proposed Template-Level Change

### A. Promote goal framing into reusable artifact templates

At minimum, add a first-class goal-framing block to the reusable execution artifacts most likely to be re-read by another agent or owner.

Recommended common fields:

1. `## Goal`
2. `## Phase Plan`
3. `## Current Step`
4. `## Step Contribution`
5. `## Progress State`

Recommended first targets:

1. `templates/execution_progress_receipt.template.md`
2. `templates/managed_terminal_prompt_dispatch_receipt.template.md`
3. any packet-like execution template intended for reuse or resumption

### B. Ship one framework-native goal-framing audit

Add a dedicated audit helper, separate from state-sync auditing, that validates required goal-framing markers for recognized artifact kinds.

Suggested artifact families:

1. packet
2. receipt
3. dispatch receipt
4. closeout
5. status snapshot

Suggested behavior:

1. detect kind from canonical headers first when possible
2. use exact suffix/path conventions rather than substring matches
3. skip unknown markdown by default, with optional strict mode
4. emit simple `PASS` / `FAIL` output suitable for local CLI and hook use

### C. Wire the new contract through bootstrap and validation

If the framework treats goal framing as part of the strict baseline, it should not remain a manual convention.

Recommended follow-through:

1. bootstrap copies the updated templates and helper audit
2. validator or strict-adoption audit checks the new surfaces when the relevant profile keeps execution receipts/dispatch receipts
3. docs explain that goal framing is meant to preserve directional context for later agents, not to add prose overhead

## Acceptance Bar For The Framework Change

The template-level fix is successful only if all of these become true:

1. a standard adopter inherits at least one reusable execution artifact that forces explicit goal/phase/current-step/progress framing
2. managed dispatch receipts can state not only handshake truth but also what larger step they advanced
3. the framework ships one portable audit for goal framing instead of relying on each adopter to reinvent it
4. the audit does not misclassify prompt files or other markdown merely because their filenames contain `packet`
5. adoption docs explain when this mechanism is required versus optional

## Why This Matters

Without this change, the framework preserves execution truth but still leaves a common failure mode open:

An agent may truthfully report what it just did while slowly losing why that step exists in the overall plan.

The InfoWeave rollout suggests that this missing layer is mechanical enough to belong in the template, not just in project-specific policy.

## Suggested Next Action

Treat this as a framework design issue with a small implementation slice:

1. update the two reusable templates
2. add the audit helper
3. wire validator/bootstrap exposure
4. add one focused regression proving prompt files are not misclassified as packets