# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this repository uses Semantic Versioning.

## [Unreleased]

### Added
- Stable closeout and progress formatting docs at `docs/CLOSEOUT_SUMMARY_TEMPLATE.md` and `docs/PROGRESS_UPDATE_TEMPLATE.md`.
- While-loop closeout state fields in `templates/session_state.template.md` for progress unit, true closeout boundary, and host closeout action.
- Optional fast-start execution block in `templates/execution_contract.template.md` to freeze planning surfaces, execution boundary, UAC, decomposition, and long-loop closeout rules at task start.
- Rule 8 closeout guardrails for irreversible host closeout and hook-only repair paths.
- Developer Toolchain discussion and formal design docs at `docs/DEVELOPER_TOOLCHAIN_DISCUSSION.md` and `docs/DEVELOPER_TOOLCHAIN_DESIGN.md`.

### Changed
- Root project metadata is now self-hosted: the repository ships a real project adapter and roadmap instead of template placeholders.
- Generated Python caches are now ignored and can be cleaned without polluting the working tree.
- Rule 8 now separates in-progress status lines from final closeout behavior and treats host closeout actions such as `task_complete` as the machine-facing completion signal.
- Doc-first planning guidance now requires while-style tasks to declare progress checkpoints separately from the true closeout boundary.
- `templates/execution_contract.template.md` now carries explicit long-loop closeout, validation, host-closeout, and status-line fields.
- `scripts/validate_template.py` now checks closeout/progress template docs, session-state long-loop fields, execution-contract long-loop declarations, and Rule 8 closeout guard snippets.
- `templates/project-context.template.md` and `scripts/bootstrap_adoption.py` now surface a first-pass Developer Toolchain contract including language, package manager, runtime ladder surfaces, and verification-state placeholders.
- `docs/ADOPTION_GUIDE.md` now asks adopters to confirm language plus Developer Toolchain surfaces rather than only validation commands.
- `scripts/validate_template.py` now parses Developer Toolchain sections structurally and emits reminder-level advisories for missing core surfaces, invalid statuses or scopes, and weak live-runtime repro declarations.
- Bootstrapped adopters now receive a manifest-declared Developer Toolchain `required-core` contract, and the copied validator hard-fails missing or malformed core Developer Toolchain fields against that manifest.
- Developer Toolchain surface labels now support runtime qualifiers such as `Run (frontend)` or `Run (backend)` so multi-runtime repositories can stay explicit without collapsing into one fake command.
- The repository now ships `examples/full_stack_project/` as a richer reference for multi-runtime Developer Toolchain structure and repro-path modeling.

### Migration Notes
- Repositories adopting this update should re-render or manually update `templates/execution_contract.template.md`, `templates/session_state.template.md`, and any local Rule 8 customization to match the new status-line versus closeout-summary model.
- If your host exposes a terminal closeout action such as `task_complete`, move final visible closeout content into the final response body or the host closeout payload rather than relying on a standalone footer.
- Repositories adopting this update should re-render or manually update `.github/project-context.instructions.md` to add the Developer Toolchain section and fill explicit `none` values where a runtime, repro path, or debugger surface does not exist.
- Repositories that refresh their bootstrap manifest now opt into hard-fail validation of the Developer Toolchain required core; legacy adopters without the new manifest block remain on the older softer path until they refresh.

## [0.3.0] - 2026-04-01

### Added
- Structured validator at `scripts/validate_template.py`.
- Bootstrap project-type presets, conflict reporting, and next-step summary.
- Demo project under `examples/demo_project/`.
- CI smoke tests for `minimal`, `standard`, and `full` bootstrap profiles.
- Compatibility guidance, release metadata, and a root ROADMAP for self-hosting.

### Changed
- `scripts/validate-template.sh` is now a thin wrapper over the structured validator.
- Git closeout guidance now defaults to main-thread commit/push with exception-based escalation.

## [0.2.0] - 2026-04-01

### Added
- Resumable git audit packet, receipt, and handoff workflow.
- Reviewer role examples and role profile template.
- Bootstrap-based adoption flow and CI validation.

## [0.1.0] - 2026-03-31

### Added
- Initial layered agent framework template with session state and roadmap support.
