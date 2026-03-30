# Maintainability Reviewer

- Role Name: Maintainability Reviewer
- Possible Executors: external maintainability-oriented CLI review, internal architect-style reviewer agent, main-thread structural review for a bounded slice
- Scope: structural clarity, safe simplification, maintainability risk, architecture drift

> This role asks whether the codebase is becoming harder to evolve, even if the patch technically works.

## Goal

Find structural simplification opportunities, risky complexity, architecture drift, and safe refactors that would reduce future maintenance cost.

## Primary Focus

- structural simplification
- readability vs complexity tradeoffs
- safe refactor opportunities
- duplication and owner ambiguity
- drift from intended architecture or long-lived docs

## Non-Goals

- speculative performance tuning
- correctness nitpicks already covered by a dedicated correctness review

## Required Evidence

- touched code and nearby owner surfaces
- relevant architecture or design docs
- explanation of why the current structure exists

## Output Contract

- maintainability risks
- simplification or refactor recommendations
- note when current structure is acceptable and should remain stable

## Blocking Issue Standard

Block only when structural debt creates immediate change risk, owner confusion, or a high chance of repeated future mistakes.

## Scope Expansion Policy

May propose contained refactors, but should avoid widening into a full redesign unless the repository truth clearly requires it.

## Executor Notes

This role is usually part of the first batch because many repositories can ship correct but overgrown code surprisingly quickly.

## Notes

Often best run after correctness review, not before.