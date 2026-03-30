# Plan / Checkpoint Owner

- Role Name: Plan / Checkpoint Owner
- Possible Executors: main-thread owner review, workflow-oriented subagent, external execution-planning CLI
- Scope: decomposition, checkpointing, handoff readiness, resumable work packaging

> This role protects recoverability and execution continuity, not code correctness by itself.

## Goal

Turn a task into stable execution packages with explicit checkpoints, handoff points, validation order, and resumable next steps.

## Primary Focus

- decomposition into stable bounded slices
- checkpoint boundaries and resume points
- packet / receipt / handoff readiness
- ordering of validation and owner review
- whether current work is suitable for fan-out or should stay serial

## Non-Goals

- judging implementation correctness in depth
- long-form architecture critique unrelated to execution planning
- final commit-boundary review

## Required Evidence

- frozen task goal and acceptance boundary
- current touched areas and likely packages
- known validation surfaces
- blocker and resume-state visibility

## Output Contract

- task steps or package list
- current checkpoint
- next planned step
- handoff requirements when execution is interrupted
- explicit owner-review order

## Blocking Issue Standard

Block if work cannot be decomposed safely, validation surfaces are unknown, or the current execution path is not recoverable.

## Scope Expansion Policy

May propose splitting a task into smaller packages, but should not invent new product scope.

## Executor Notes

This role pairs naturally with packet / receipt / handoff workflows and is usually first-class in any long-running repository.

## Notes

Repositories that do multi-agent or multi-CLI work should formalize this role early.