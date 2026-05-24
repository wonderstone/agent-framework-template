# Git Audit Task Packet

- Generated At: 2026-05-22T23:29:19.001468+00:00
- Task ID: template-governance-sync-smoke
- Owner: main-thread
- Executor Plan: planner -> executor -> auditor -> gatekeeper

## Start Here

- Read the declared truth sources first

## Goal

Propagate canonical goal framing into template automation.

## Phase

Generate a canonical packet through the template pipeline and verify it audits cleanly.

## Current Step

1. Generate canonical packet artifacts

## Total Steps

3

## Truth Sources

- docs/DOC_FIRST_EXECUTION_GUIDELINES.md

## Allowed Files

- templates/**
- scripts/**

## Do Not Touch

- tmp/dispatch/**

## Focused Validation

- python3 scripts/governance_check.py audit tmp/git_audit/template_governance_sync_smoke

## Acceptance Boundary

- Packet renders with canonical headings and passes audit

## Checkpoint Contract

- Progress Unit: - none
- Checkpoint Rule: - none
- Truth Surfaces: - none
- State Sync Schedule: - none
- Closeout Boundary: - none

## Notes

smoke test
