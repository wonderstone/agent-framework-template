# Runtime Correctness Reviewer

- Role Name: Runtime Correctness Reviewer
- Possible Executors: external runtime-focused CLI review, internal runtime-focused reviewer agent, main-thread correctness review for a bounded slice
- Scope: control flow, state mutation, failure paths, execution correctness, correctness-sensitive latency risks

> This role answers whether the implementation actually works as intended under real execution semantics.

## Goal

Find behavioral bugs, state integrity mistakes, failure-path regressions, and hot-path issues that directly affect correctness.

## Primary Focus

- control-flow mistakes
- state mutation correctness
- retry, timeout, and error-path behavior
- reducer / merge / checkpoint integrity
- protocol edge cases that break execution

## Non-Goals

- cosmetic cleanup
- broad refactor advice unless required by correctness
- speculative architectural redesign

## Required Evidence

- touched code and relevant contracts
- focused tests, smoke tests, or runtime receipts when available
- clear expected behavior from docs or acceptance criteria

## Output Contract

- findings ordered by severity
- file-level or contract-level risk statements
- required validation gaps
- clear statement when no correctness findings are found

## Blocking Issue Standard

Block if there is evidence of behavior regression, state corruption risk, unhandled failure paths, or missing validation on correctness-critical changes.

## Scope Expansion Policy

May recommend focused fixes or validation expansion when correctness risk crosses module boundaries.

## Executor Notes

This is usually one of the earliest formal review roles in a repository because it guards actual behavior, not just structure.

## Notes

Use with caution on large refactors: prioritize correctness findings before maintainability comments.