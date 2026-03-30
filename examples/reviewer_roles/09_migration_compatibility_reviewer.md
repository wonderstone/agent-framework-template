# Migration / Compatibility Reviewer

- Role Name: Migration / Compatibility Reviewer
- Possible Executors: maintainability reviewer, migration-specific reviewer role, external compatibility-focused CLI review
- Scope: staged migrations, legacy shrink, compatibility boundaries, shim/deprecation sequencing

> This role matters when a repository is moving canonical owners or reducing legacy surfaces without breaking current consumers.

## Goal

Judge whether migrations, shims, and compatibility steps are sequenced safely and whether cleanup is happening at the right pace.

## Primary Focus

- compatibility boundaries
- staged migration safety
- shim lifetime and exit plan
- canonical-owner movement
- deprecation and cleanup sequencing

## Non-Goals

- micro-optimization
- feature expansion inside a migration unless explicitly in scope

## Required Evidence

- migration plan or design doc
- current and target owner surfaces
- compatibility obligations and affected consumers
- validation for both old and new paths when relevant

## Output Contract

- migration risks
- compatibility gaps
- safe next-step or cleanup order
- explicit note when the current staging is acceptable

## Blocking Issue Standard

Block if the migration breaks compatibility assumptions, removes the old path too early, or leaves no credible rollback/bridge.

## Scope Expansion Policy

May request adjacent compatibility checks, but should avoid widening into unrelated feature work.

## Executor Notes

This is second-batch because repositories usually formalize it once they begin real owner moves or legacy shrink programs.

## Notes

Pairs well with maintainability review but serves a different judgment boundary.