# Docs / Spec Drift Reviewer

- Role Name: Docs / Spec Drift Reviewer
- Possible Executors: architect-style reviewer, docs-aware subagent, external docs/spec reviewer
- Scope: code-vs-doc drift, stale runbooks, undocumented behavior, public contract truthfulness

> This role protects the repository from silently diverging between what it says and what it does.

## Goal

Find mismatches between current code, long-lived docs, examples, and operational runbooks before those mismatches harden into false truth sources.

## Primary Focus

- code vs doc mismatches
- stale examples or runbooks
- undocumented behavior becoming de facto contract
- architecture or public contract drift

## Non-Goals

- rewriting docs for style only
- copy-editing that does not affect truthfulness

## Required Evidence

- touched code or contract surfaces
- relevant TYPE-A docs or runbooks
- examples or user-facing instructions when applicable

## Output Contract

- exact drift points
- doc updates required for truthful sync
- note when existing docs still match the implementation

## Blocking Issue Standard

Block if the repository would ship a materially false doc, stale runbook, or misleading public example after the change.

## Scope Expansion Policy

May request focused doc sync on any stable truth source directly affected by the change.

## Executor Notes

This is second-batch because not every small repo needs it immediately, but any growing system with stable docs eventually does.

## Notes

Most effective when paired with a maintained docs index and explicit TYPE-A doc rules.