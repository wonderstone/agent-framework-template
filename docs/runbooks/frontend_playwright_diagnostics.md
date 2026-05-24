# Frontend Playwright Diagnostics

## Purpose

This runbook defines a reusable browser-debug workflow for repositories that already ship a browser-visible frontend and already have, or can honestly add, a repo-owned Playwright seam.

The purpose is not broad end-to-end product automation.

The purpose is to replace slow loops of manual browser refresh, copied console logs, and human-transcribed frontend failures with one stable headless smoke command plus receipt-backed artifacts.

## When To Use This Runbook

Use this runbook when all of the following are true:

1. the task touches a browser-visible frontend surface
2. the current debugging loop depends on a human reopening the browser or copying console output into chat
3. the repository already has Playwright, or can honestly standardize on it as the first browser smoke tool

Do not use this runbook when:

1. the slice is backend-only with no browser-visible surface
2. the repository has no reachable local frontend runtime
3. the task needs broad product acceptance rather than a bounded browser diagnostics seam

## Core Rule

When Playwright is available, the repository should expose one canonical headless smoke entrypoint for the frontend slice.

The smoke path should become the default browser diagnostics seam for future frontend repairs.

Manual refresh plus copied console logs is fallback-only behavior.

## Expected Capture Set

The first honest smoke path should capture at least:

1. `console.error`
2. `pageerror`
3. `requestfailed`
4. first-party API `4xx/5xx`
5. critical DOM-mount or route-mount failures

The exact selectors and routes may remain repository-specific.

The important contract is that the agent can review the resulting artifacts without asking the user to transcribe browser state manually.

## Recommended Artifact Set

The smoke path should emit:

1. one machine-readable artifact such as JSON report, trace, or screenshots
2. one human-readable receipt describing what the smoke found
3. one stable rerun command that later tasks can reuse directly

## Implementation Pattern

The preferred pattern is:

1. start from the browser framework already declared in the repo
2. consolidate ad hoc inspection scripts into one canonical smoke entrypoint when possible
3. keep the first version headless by default
4. scope it to the currently owned frontend surface instead of turning it into a broad product-wide E2E harness
5. treat real product bugs revealed by the smoke as a successful outcome for the diagnostics packet, not as proof that the smoke failed

## Closeout Expectation

This runbook is satisfied when:

1. the repository has one stable browser smoke command
2. the command emits artifact-backed frontend failure truth
3. later frontend repair packets can reference that same command and receipt path as the default diagnostics seam

## References

1. `docs/DEVELOPER_TOOLCHAIN_DESIGN.md`
2. `docs/DOC_FIRST_EXECUTION_GUIDELINES.md`
3. `.github/instructions/project-context.instructions.md`

> Updated 2026-05-06: added the reusable Playwright-first frontend diagnostics workflow so adopters can replace manual browser transcript loops with one repo-owned smoke seam.