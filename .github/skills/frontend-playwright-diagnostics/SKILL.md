# Frontend Playwright Diagnostics

- ID: frontend-playwright-diagnostics
- Type: workflow
- Owner: framework-maintainers
- Review Threshold: single-reviewer

## Purpose

Turn browser-visible frontend debugging into one repo-owned Playwright smoke and receipt workflow so adopters do not depend on manual browser refresh and copied console output for routine frontend repair.

## Triggers

### Positive Triggers

- Use when a repository has a browser-visible frontend and the current debug loop depends on a human reopening the browser or pasting console logs.
- Use when Playwright is already present but the repository still lacks one canonical smoke path.
- Use when an agent needs a stable browser-runtime diagnostics seam rather than only unit or integration coverage.

### Negative Triggers

- Do not use for backend-only slices with no browser-visible surface.
- Do not use when the repository has no honest local frontend runtime path.
- Do not use when the real task is broad end-to-end acceptance instead of a bounded browser diagnostics seam.

### Expected Effect

- The repository exposes one canonical headless browser smoke command.
- Browser failures become receipt-backed and artifact-backed rather than chat-transcribed.
- Manual refresh plus copied console logs becomes fallback-only behavior.

## Entry Instructions

- Read `docs/DEVELOPER_TOOLCHAIN_DESIGN.md` and `docs/runbooks/frontend_playwright_diagnostics.md`.
- Reuse Playwright if it already exists in the repo instead of introducing a second browser framework.
- Consolidate ad hoc inspection scripts into one primary smoke entrypoint when possible.
- Capture at least browser runtime errors, request failures, first-party API failures, and critical DOM-mount failures.
- Emit one machine-readable artifact and one human-readable receipt.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| developer toolchain design | `docs/DEVELOPER_TOOLCHAIN_DESIGN.md` | yes | Framework rule for how repos should expose runnable diagnostics seams |
| frontend diagnostics runbook | `docs/runbooks/frontend_playwright_diagnostics.md` | yes | Canonical reusable workflow for Playwright-first frontend diagnostics |
| project context adapter | `.github/instructions/project-context.instructions.md` | yes | Routes frontend-diagnostics topics to the canonical runbook |
| skill mechanism design | `docs/SKILL_MECHANISM_V1_DRAFT.md` | no | Governs reusable skill structure and promotion expectations |

## Governance

### Allowed Evidence

- repo-local Playwright commands and receipts
- machine-readable browser artifacts such as JSON reports, screenshots, or traces
- frontend runtime failures captured directly from the smoke run

### Reviewer Gate

- Workflow wording or trigger refinements may use single-reviewer promotion; any weakening of the repo-owned artifact requirement remains human-reviewed.

### Forbidden Direct Update Inputs

- Do not treat paraphrased browser symptoms or pasted chat summaries as equivalent to a runnable browser smoke when the repo can carry a truthful Playwright seam.

## Receipt And Review Matrix

| Field | Proposal evidence tiers | Minimum reviewer threshold | Guardrail override | Promotion tier |
|---|---|---|---|---|
| `purpose` | `1-2 only` | `single-reviewer` | `dual-reviewer` if repo-owned artifact expectations weaken | `human-only` |
| `triggers` | `1-3` | `single-reviewer` | `dual-reviewer` if nearby non-browser tasks would start triggering it | `human-only` |
| `entry_instructions` | `1-3` | `single-reviewer` | `dual-reviewer` if manual browser transcription becomes normalized | `delegated-reviewed` |
| `references` | `1-4` | `single-reviewer` | `single-reviewer`; reference truthfulness required | `delegated-safe` |
| `governance` | `1-2 only` | `single-reviewer` | `dual-reviewer` for reviewer-threshold changes | `human-only` |
| `degradation` | `1-3` | `single-reviewer` | `single-reviewer`; fallback cannot overstate equivalence | `delegated-reviewed` |

## Degradation

- If the repository cannot run Playwright honestly yet, stop at defining or repairing the browser smoke seam rather than pretending manual refresh and copied console output are an equivalent default.

## Validator Notes

- Keep the trigger surface specific to browser-visible frontend diagnostics rather than broad testing advice.
- Keep artifact and receipt expectations explicit whenever this skill evolves.