# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this repository uses Semantic Versioning.

## [Unreleased]

### Changed
- Root project metadata is now self-hosted: the repository ships a real project adapter and roadmap instead of template placeholders.
- Generated Python caches are now ignored and can be cleaned without polluting the working tree.

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
