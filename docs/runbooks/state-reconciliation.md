# State Reconciliation Runbook

This runbook defines how the repository repairs execution drift when `session_state.md`, `ROADMAP.md`, task packets, progress receipts, handoff packets, or closeout surfaces no longer agree.

## Goal

Turn drift from an ad hoc prose cleanup into a bounded, receipt-bearing recovery workflow.

The point is not to infer one perfect narrative automatically.

The point is to make contradictions observable, recoverable, and blocking at the right boundary.

## When To Use It

Use this runbook when any of the following is true:

1. a checkpointed task has no matching progress receipt
2. `session_state.md` says no active work while task receipts or handoff artifacts still show in-flight work
3. a blocker exists without a matching handoff packet or leftover record
4. `ROADMAP.md` and receipt-bearing task artifacts disagree about whether a boundary was reached
5. closeout or next-stage dispatch is about to continue while a contradiction remains unresolved

## Canonical Artifact

| Artifact | Purpose | Default path |
|---|---|---|
| `drift reconciliation packet` | record the detected contradiction, affected truth surfaces, repair steps, and resolution status | `tmp/git_audit/<task_slug>/drift_packet.md` |

## Minimum Flow

1. Run `python3 scripts/state_sync_audit.py --root <repo>` or the relevant hook boundary.
2. If the audit reports a contradiction, open or update `tmp/git_audit/<task_slug>/drift_packet.md`.
3. Record what evidence is stale and which surfaces must be reconciled.
4. Update the relevant truth surfaces.
5. Re-run the sync audit before closeout or dispatch continues.
6. If the work is intentionally paused rather than reconciled, convert it into a truthful handoff or leftover record.

## Required Packet Fields

Every drift packet must record:

1. `detected_by`
2. `staleness_evidence`
3. `surfaces_to_reconcile`
4. `reconciliation_steps`
5. `reconciliation_receipt_id`
6. `status`

## Status Model

| Status | Meaning |
|---|---|
| `open` | contradiction detected and not yet reconciled |
| `in_progress` | reconciliation work started but not yet confirmed |
| `resolved` | sync audit passes and the surfaces now agree |
| `converted_to_leftover` | contradiction was resolved by recording a truthful leftover boundary |

## Boundary Rule

Unresolved drift blocks:

1. final closeout
2. next-stage dispatch
3. promotion of partial work to completed

Drift does not automatically block exploratory reading or reversible local edits.

It blocks the moment the repository would otherwise freeze a false narrative into its durable truth surfaces.

## Relationship To Other Mechanisms

| Mechanism | Role |
|---|---|
| `templates/execution_contract.template.md` | declares the checkpoint and truth-sync contract up front |
| `templates/execution_progress_receipt.template.md` | records checkpoint-bearing progress events |
| `templates/git_audit_task_packet.template.md` | freezes task scope plus checkpoint contract for bounded execution |
| `templates/git_audit_handoff_packet.template.md` | records tactical interruption state |
| `docs/LEFTOVER_UNIT_CONTRACT.md` | records intentional strategic deferral after reconciliation |

## Recommended Commands

```bash
python3 scripts/state_sync_pipeline.py record-progress ...
python3 scripts/state_sync_pipeline.py upsert-drift ...
python3 scripts/state_sync_audit.py --root .
```