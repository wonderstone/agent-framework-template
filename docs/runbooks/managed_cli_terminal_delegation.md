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
5. the mandatory prompt-dispatch handshake for managed executor terminals
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

## Prompt-Dispatch Handshake

Managed executor terminals now use one mandatory prompt-dispatch handshake:

1. pre-read
2. send prompt
3. read output immediately
4. if the prompt only buffered in the visible input area, send one explicit Enter
5. read output again
6. classify the outcome

Dispatch outcomes are limited to:

1. `started`: the prompt continued execution without needing the Enter step
2. `started_after_submit`: the prompt buffered first, one allowed Enter was sent, and the agent then continued running
3. `degraded`: the execution ID is no longer controllable, output is unreadable, or prompt-plus-one-allowed-Enter still does not make the agent continue

Hard rules:

1. visible prompt echo is not evidence that execution already started
2. use one explicit Enter action only when the lane buffered the prompt instead of dispatching it
3. do not classify a lane as degraded just because the one allowed Enter step was needed once
4. visible old terminal output by itself is not a reason to replace the lane
5. keep using the same lane while the execution ID remains controllable, output remains readable, and the prompt body plus the one allowed Enter step still makes the agent continue running
6. degrade or restart only when one of those hard conditions stops holding
7. once a concrete start signal confirms `started` or `started_after_submit`, stop interacting with the lane in the current turn and wait for the user to return for acceptance or a requested status check

Use `templates/managed_terminal_prompt_dispatch_receipt.template.md` when the repository wants a dedicated receipt for the handshake plus the final outcome.

## Post-Start Non-Interference

After a managed lane shows a concrete start signal, the repository-default action is to leave it alone.

Strong start signals include:

1. `Read` or `Reading` lines for the packet or repo files
2. executor reasoning banners such as `thinking`, `Whisking`, `✢ ...`, or `✶ ...`
3. `• Working (...)` status bars or close structural variants
4. packet-specific shell or tool execution lines
5. creation or overwrite of the expected packet receipt or result file

Hard rules:

1. once the lane is confirmed `started` or `started_after_submit`, do not send another task prompt, reminder, or `continue` nudge during the same packet round just because no receipt or diff is visible yet
2. after a valid start classification, the correct default action is to end the current dispatch-monitoring turn and let the user return later for acceptance or a status check
3. absence of fresh output, old transcript residue, or operator impatience are not valid reasons to re-prompt a lane that already shows a strong start signal
4. only break this non-interference rule when the executor explicitly asks for input, reports a clear terminal state such as `DONE` / `STUCK` / `ESCALATE`, or a hard failure destroys control or readability

## Standard Workflow

1. freeze the packet first
2. choose the executor lane
3. start a new controlled terminal execution with the approved trusted-local command
4. retain the returned execution ID
5. immediately record `execution_id -> terminal label -> starter command -> purpose -> creation time` in a durable repo-visible truth surface such as `session_state.md`, the active packet, or the handoff receipt
6. if the user wants, let the user manually surface that session in the terminal panel and rename it
7. pre-read the lane before dispatch so stale history is visible before new input is sent
8. send the long prompt or staged follow-up prompt body through the execution ID and read output right away
9. if the prompt only buffered, send one explicit Enter action through the same execution ID and read output again
10. classify the dispatch outcome as `started`, `started_after_submit`, or `degraded`
11. if the lane reached `started` or `started_after_submit` and is not asking for input, end the current turn and wait for the user to return later for acceptance or a status check
12. keep the session alive during the packet lifecycle unless hard-condition lane reuse fails or restart is required
13. only resume reads when the user asks for acceptance or status, or when the lane itself requests input
14. clean up the session only when the task or handoff boundary is complete

## Recording Requirement

Creating a managed executor terminal is not complete until the execution ID is written into one durable repo-visible truth surface.

Minimum required fields:

1. executor lane
2. execution ID
3. starter command
4. human-visible terminal label when known
5. task or purpose boundary
6. current lane state such as `active`, `completed`, `lost-id`, or `closed`
7. last prompt-dispatch outcome when applicable: `started`, `started_after_submit`, or `degraded`

Hard rules:

1. do not rely on the terminal panel label as the only record of a managed session
2. do not open a second managed session for the same purpose without either recording the first ID or explicitly marking the first session `lost-id` or `closed`
3. if the ID is lost before recording, mark that failure truthfully instead of pretending the visible tab remains controllable
4. if the prompt body was sent and the lane clearly started, record the dispatch outcome as `started`
5. if one explicit Enter action was needed before the lane started, record the dispatch outcome as `started_after_submit`
6. if the execution ID is no longer controllable, output is no longer readable, or the prompt body plus the one allowed Enter step still did not make the agent continue running, record the dispatch outcome as `degraded`

## Human Interaction Rules

1. the user may manually move the terminal into the terminal panel
2. the user may rename the terminal for recognition
3. the renamed label may be used in user-facing summaries as the human anchor
4. the renamed label must not replace the execution ID in machine-facing notes or control actions

## Failure And Recovery

Common failure cases:

1. the executor CLI starts but loses editor integration messaging
2. the execution ID is lost even though the user can still see a renamed terminal label
3. the prompt body is sent but the lane only buffers it in the visible input area
4. the session output becomes unreadable or stale in a way that blocks handshake classification
5. the session becomes unresponsive or needs login
6. the task changes scope while the managed terminal is still alive

Recovery rules:

1. if the execution ID is unavailable, fall back to copy-paste prompt handoff and record the downgrade explicitly
2. if the prompt body only buffered, send one explicit Enter action and re-read output before deciding whether the lane is running or degraded
3. if the session is unresponsive, kill it and open a new controlled terminal instead of assuming the renamed label is still usable
4. if login or auth is required, classify the packet as `STUCK` rather than improvising a new path silently
5. if scope changes materially, stop and return `ESCALATE` before reusing the old terminal for a broader task
6. if a visible terminal tab exists but the execution ID was never recorded or can no longer be recovered, mark that session `lost-id` and treat it as non-controllable

## Acceptance Criteria

1. The repository has one canonical runbook for trusted-local managed CLI terminal delegation.
2. The runbook defines approved starter commands for the supported executor lanes.
3. The runbook freezes the display-label versus execution-ID split.
4. The runbook defines the prompt-dispatch handshake and the only allowed outcomes: `started`, `started_after_submit`, and `degraded`.
5. The runbook requires durable recording of each managed terminal execution ID and dispatch outcome.
6. The runbook defines hard-condition lane reuse and restart rules for long-lived controlled executor sessions.
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
> Updated 2026-05-03: replaced the old staged-prompt wording with the prompt-dispatch handshake standard, the `started` / `started_after_submit` / `degraded` outcome set, and hard-condition lane reuse.
>
> Updated 2026-05-11: repositories using this template now treat `started` and `started_after_submit` as the normal stop boundary for the current dispatch turn. Once a strong start signal appears and no input is requested, the main thread should leave the lane alone and wait for the user to bring it back for acceptance rather than continuing same-turn observation or follow-up prompting.