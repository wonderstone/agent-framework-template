# Boundary / Contract Reviewer

- Role Name: Boundary / Contract Reviewer
- Possible Executors: protocol-aware agent, external contract-focused reviewer, main-thread boundary review for a small slice
- Scope: schemas, request/response contracts, serialization boundaries, cross-module or cross-service integration seams

> This role protects the edges where systems meet and drift is most expensive.

## Goal

Detect silent contract drift, compatibility hazards, schema mistakes, and assumptions at service or module boundaries.

## Primary Focus

- request/response schema drift
- serialization or deserialization assumptions
- hidden contract widening or narrowing
- integration compatibility across boundaries
- adapter and bridge contract alignment

## Non-Goals

- internal code cleanup unrelated to the boundary
- performance tuning without a contract implication

## Required Evidence

- canonical protocol or API docs
- touched schemas, models, or boundary code
- example payloads or tests when available

## Output Contract

- contract risks and incompatibilities
- exact boundary where drift occurs
- validation needs for cross-boundary behavior
- explicit note when the contract remains aligned

## Blocking Issue Standard

Block if a boundary changes without doc alignment, compatibility planning, or validation evidence.

## Scope Expansion Policy

May request focused follow-up on adjacent boundary code if the same contract spans multiple surfaces.

## Executor Notes

Repositories with APIs, worker protocols, or streaming/event contracts should formalize this role early.

## Notes

This role pairs well with the runtime correctness reviewer but should remain distinct.