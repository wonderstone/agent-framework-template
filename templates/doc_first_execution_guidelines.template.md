# Doc-First Execution Guidelines

This document freezes the default execution mode for this repository.

It exists to remove ambiguity about how non-trivial implementation work should start, how detailed planning artifacts must be, and whether doc-first execution is optional.

It is the default unless the user explicitly overrides it.

## Default Execution Mode

For this repository, the default mode is:

1. document first
2. validate the plan against current truth sources
3. execute against the written plan
4. update the plan or checklist before changing direction

This means non-trivial work should begin from executable documentation, not from chat memory alone.

## What Counts As Non-Trivial

Treat a task as non-trivial when it has one or more of these properties:

1. touches more than one file
2. changes behavior rather than only wording or formatting
3. introduces a new module, package, subsystem, workflow, or contract
4. affects user-visible behavior
5. requires multi-step validation, staged rollout, or cross-session continuity

For those tasks, the planning artifact must exist before meaningful implementation begins.

## Required Detail Level

Planning artifacts must be executable rather than aspirational.

At minimum, the planning artifact must include:

1. goal and boundary
2. current truth and gap summary
3. file-level scope
4. ordered implementation steps
5. validation commands
6. user-visible acceptance criteria
7. stop conditions, non-goals, or explicit deferrals

If those elements are absent, the plan is not implementation-ready.

## Required Planning Surfaces

The expected planning stack for non-trivial work is:

1. repository-level roadmap or design doc
2. file-level execution checklist or implementation checklist
3. validation commands recorded in a durable validation doc or equivalent
4. current state reflected in `session_state.md` or the repository's state-tracking equivalent

## Default Agent Behavior

When the user asks for a new phase, subsystem, or meaningful behavior change, the default behavior is:

1. update or create the roadmap or design truth first
2. create or update the execution checklist next
3. sync validation commands and entry docs
4. update current state tracking
5. begin implementation only after those planning surfaces exist

Do not ask the user to choose between doc-first and code-first for non-trivial work unless they explicitly request a lighter-weight path.

## Document Update Rule

If implementation reveals that the plan is incomplete or wrong, update the relevant doc before continuing down the new path.

Do not silently diverge from the documented plan.

## Minimum Acceptance For Adoption

This rule is active only when all of these are true:

- [ ] the repository's global instructions or policy surface state that doc-first execution is the default for non-trivial work
- [ ] the project adapter or repo-local instruction file points future sessions to this document
- [ ] the repository has an active roadmap or design doc plus a checklist surface
- [ ] entry documentation points to the planning artifacts before implementation starts

## Local Customization

Replace the generic references in this template with the actual local surfaces used by your repository.

Suggested replacements:

1. active roadmap/design doc path
2. execution checklist path
3. validation doc path
4. state-tracking doc path

> Updated [YYYY-MM-DD]: adopt doc-first execution as the repository default for non-trivial work.