# Managed CLI Terminal Delegation

## Purpose

This runbook freezes the trusted-local workflow for long-lived managed CLI executor terminals.

It exists to bridge the gap between:

1. packet-ready long tasks that benefit from a persistent executor session
2. the practical need to keep one controlled terminal alive across multiple prompt turns
3. the human need to see and rename those terminals in the editor terminal panel without confusing the human label with the machine control handle

## Scope

This runbook owns:

1. when a repository may open a managed executor terminal
2. the trusted-local auto-approve starter commands for supported executor lanes
3. the lifecycle of a long-lived controlled executor session
4. the split between the human-visible terminal label and the machine control anchor
5. the mandatory two-phase prompt-dispatch rule for managed executor terminals
6. failure recovery and restart rules for managed executor terminals
7. the mandatory recording rule for execution IDs after terminal creation

## Non-Goals

This runbook does not:

1. make terminal display names machine-addressable
2. authorize uncontrolled executor terminals on unknown, remote, or production-like hosts
3. bypass packet readiness, owner review, focused validation, or closeout rules
4. replace the existing copy-paste prompt handoff path when a managed terminal cannot be controlled reliably

## Entry Conditions

Use this workflow only when all of the following are true:

1. the task is packet-ready
2. the expected execution is long enough that a persistent session is useful
3. the current host is a trusted local environment
4. the chosen executor has a validated local CLI starter command
5. the main thread can retain the execution ID returned by the terminal-control tooling

## Approved Trusted-Local Starter Commands

| Executor lane | Starter command |
|---|---|
| DeepSeek-backed Claude Code | `ccrun ds-pro claude --dangerously-skip-permissions` |
| Claude Code | `claude --dangerously-skip-permissions` |
| Codex | `codex --dangerously-bypass-approvals-and-sandbox` |
| Gemini | `gemini --yolo` or `gemini -y` |

These commands are allowed only for trusted local environments where the user explicitly wants the reduced-approval path.

## Control Anchors

Repositories using this workflow distinguish two anchors:

| Anchor | Purpose | Owner |
|---|---|---|
| Terminal display label | Human recognition anchor in the terminal panel | user-visible only |
| Execution ID | Machine control anchor for input, output, and cleanup | main thread tooling |

Hard rule:

1. the main thread must never assume a renamed terminal label is a machine-addressable control handle
2. the execution ID remains the authoritative control token for sending input, reading output, and cleanup

## Prompt Dispatch Contract

Managed executor terminals now use a mandatory two-phase prompt-dispatch contract:

1. `prompt_staged`: the main thread sends the prompt body to the controlled terminal execution ID, but execution is not yet considered started
2. `enter_sent`: the main thread sends one explicit terminal Enter action after the prompt body is staged
3. `running`: the main thread reads the next terminal output and only then treats the managed session as actively executing the prompt

Hard rules:

1. sending the prompt body is not enough to classify a managed executor terminal as running
2. the main thread must send an explicit Enter action after the prompt body whenever the executor lane requires Enter to dispatch the prompt
3. until the Enter action is sent and terminal output confirms dispatch, the session must remain recorded as `prompt_staged` rather than `running`
4. if the prompt body was staged but Enter was not sent, the session must not be summarized or accepted as an active executor run

Use `templates/managed_terminal_prompt_dispatch_receipt.template.md` when the repository wants a dedicated three-step receipt for `prompt_staged -> Enter -> post-dispatch output read`.

## Standard Workflow

1. freeze the packet first
2. choose the executor lane
3. start a new controlled terminal execution with the approved trusted-local command
4. retain the returned execution ID
5. immediately record `execution_id -> terminal label -> starter command -> purpose -> creation time` in a durable repo-visible truth surface such as `session_state.md`, the active packet, or the handoff receipt
6. if the user wants, let the user manually surface that session in the terminal panel and rename it
7. send the long prompt or staged follow-up prompt body through the execution ID and record the session as `prompt_staged` until dispatch is confirmed
8. send one explicit Enter action through the same execution ID to dispatch the staged prompt
9. read the next terminal output and only then classify the session as `running`
10. keep the session alive during the packet lifecycle unless restart is required
11. read outputs and enforce `DONE`, `STUCK`, or `ESCALATE`
12. clean up the session only when the task or handoff boundary is complete

## Recording Requirement

Creating a managed executor terminal is not complete until the execution ID is written into one durable repo-visible truth surface.

Minimum required fields:

1. executor lane
2. execution ID
3. starter command
4. human-visible terminal label when known
5. task or purpose boundary
6. current control state such as `prompt_staged`, `running`, `completed`, `lost-id`, or `closed`

Hard rules:

1. do not rely on the terminal panel label as the only record of a managed session
2. do not open a second managed session for the same purpose without either recording the first ID or explicitly marking the first session `lost-id` or `closed`
3. if the ID is lost before recording, mark that failure truthfully instead of pretending the visible tab remains controllable
4. if a prompt body has been sent but the explicit Enter action has not yet been sent, record that managed session as `prompt_staged`
5. do not upgrade a managed session from `prompt_staged` to `running` until the Enter action has been sent and a post-dispatch terminal output read has been attempted

## Human Interaction Rules

1. the user may manually move the terminal into the terminal panel
2. the user may rename the terminal for recognition
3. the renamed label may be used in user-facing summaries as the human anchor
4. the renamed label must not replace the execution ID in machine-facing notes or control actions

## Failure And Recovery

Common failure cases:

1. the executor CLI starts but loses editor integration messaging
2. the execution ID is lost even though the user can still see a renamed terminal label
3. the prompt body is staged but the explicit Enter action was never sent
4. the session becomes unresponsive or needs login
5. the task changes scope while the managed terminal is still alive

Recovery rules:

1. if the execution ID is unavailable, fall back to copy-paste prompt handoff and record the downgrade explicitly
2. if the prompt body is staged but Enter was not yet sent, send the missing Enter action explicitly or reset the session truthfully instead of pretending work already started
3. if the session is unresponsive, kill it and open a new controlled terminal instead of assuming the renamed label is still usable
4. if login or auth is required, classify the packet as `STUCK` rather than improvising a new path silently
5. if scope changes materially, stop and return `ESCALATE` before reusing the old terminal for a broader task
6. if a visible terminal tab exists but the execution ID was never recorded or can no longer be recovered, mark that session `lost-id` and treat it as non-controllable

## Acceptance Criteria

1. The repository has one canonical runbook for trusted-local managed CLI terminal delegation.
2. The runbook defines approved starter commands for the supported executor lanes.
3. The runbook freezes the display-label versus execution-ID split.
4. The runbook defines the mandatory two-phase prompt-dispatch rule and forbids treating `prompt_staged` as active execution.
5. The runbook requires durable recording of each managed terminal execution ID and dispatch control state.
6. The runbook defines lifecycle and recovery rules for long-lived controlled executor sessions.
7. The runbook stays aligned with the surrounding guidance surfaces.

## Validation Plan

1. `docs/INDEX.md` references this runbook
2. `.github/instructions/project-context.instructions.md` routes managed-terminal topics to this runbook
3. `.github/instructions/managed-cli-terminal-delegation.instructions.md` reflects the same control-anchor rules
4. `.github/skills/managed-cli-terminal-delegation/SKILL.md` stays aligned with this runbook
5. `templates/managed_terminal_prompt_dispatch_receipt.template.md` exists as the reusable dispatch receipt shape
6. `python3 scripts/validate_template.py`

> Updated 2026-05-02: added the reusable managed terminal delegation runbook, including the display-name versus execution-ID split and the requirement to record every execution ID immediately after terminal creation.
>
> Updated 2026-05-03: added the mandatory two-phase prompt-dispatch contract so managed executor sessions now distinguish `prompt_staged` from `running`, require one explicit Enter action after prompt staging, and ship a reusable three-step dispatch receipt template.