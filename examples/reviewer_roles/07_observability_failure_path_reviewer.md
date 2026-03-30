# Observability / Failure-Path Reviewer

- Role Name: Observability / Failure-Path Reviewer
- Possible Executors: operations-aware reviewer agent, runtime correctness reviewer with observability scope, external failure-analysis reviewer
- Scope: request correlation, execution truth, health surfaces, diagnosability of failure

> This role becomes first-class once the repository needs reliable debugging evidence instead of ad hoc guesswork.

## Goal

Ensure the system emits enough structured evidence to diagnose failures, distinguish failure modes, and recover from broken runs.

## Primary Focus

- request IDs and trace anchors
- execution-truth surfacing
- health and memory reporting
- failure-mode distinguishability in logs, responses, or UI
- whether background or streaming paths remain debuggable

## Non-Goals

- inventing a full telemetry platform for a bounded change
- pure style cleanup in logs or dashboards

## Required Evidence

- current logging and health surfaces
- failure receipts or reproduction evidence
- event payloads or diagnostics UI when available

## Output Contract

- missing observability anchors
- failure-path blind spots
- specific surfaces that need structured evidence
- statement when failure diagnosis is already adequate

## Blocking Issue Standard

Block if a new failure path cannot be diagnosed with repository-local evidence or if important failure modes collapse into indistinguishable errors.

## Scope Expansion Policy

May request narrow instrumentation or response-metadata additions that make failure diagnosis possible.

## Executor Notes

This role is usually second-batch because not every repository needs it on day one, but mature systems need it quickly.

## Notes

Strongly complements runtime correctness work on streaming, async, or multi-service systems.