# Git Closeout Reviewer

- Role Name: Git Closeout Reviewer
- Possible Executors: main-thread reviewer, external reviewer with bounded diff-only scope
- Scope: diff coherence, staged boundary, validation-to-diff alignment, closeout hygiene

> This role does not redesign the work. It verifies that the closeout is coherent and auditable.

## Goal

Ensure the final diff, staged set, validation evidence, and commit boundary still match the frozen task packet.

The role is a reviewer, not the default Git operator: its normal output is a readiness judgment for the main thread, which normally performs commit and push after hard gates pass.

## Primary Focus

- whether the diff matches the frozen scope
- whether unrelated dirt leaked into the closeout
- whether stated validation actually covers the touched changes
- whether the commit boundary is coherent and reviewable

## Non-Goals

- broad feature brainstorming
- reopening already accepted design decisions without a concrete risk

## Required Evidence

- current git status or changed-files view
- task packet or equivalent frozen scope
- validation receipts or test outputs
- intended commit boundary
- changelog / version / release note context when the closeout is part of a framework release

## Output Contract

- include/exclude recommendation for changed files
- closeout risks
- recommended commit boundary
- statement of readiness or non-readiness for main-thread commit/push

## Blocking Issue Standard

Block if unrelated changes are mixed in, validation is insufficient for the diff, or the commit boundary is not coherent.

## Scope Expansion Policy

Should avoid scope expansion; it may only request narrow cleanup needed for a safe closeout.

## Executor Notes

This role becomes essential once work is split across multiple agents, worktrees, or CLI sessions.

By default, use this role to review and prepare closeout, then let the main thread perform the actual commit and normal push path unless an exception condition requires escalation.

When the change is release-facing, this role should also check that `CHANGELOG.md`, `VERSION`, and any release note draft stay aligned with the shipped diff.

## Notes

Use after implementation and focused validation, not before.
