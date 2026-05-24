---
description: "Use when a packet-ready long task should run through a trusted-local managed CLI executor terminal instead of one-shot execution or copy-paste-only handoff."
applyTo: "**"
---

# Managed CLI Terminal Delegation

Use this instruction when a task is packet-ready, long-running, and a persistent executor terminal is more useful than a one-shot CLI call.

## Core Rule

Managed executor terminals are allowed only for trusted local environments and only after the packet boundary is already frozen.

## Required Behavior

1. open the terminal through a controlled execution surface and keep the returned execution ID
2. treat the execution ID as the machine control anchor for input, output, and cleanup
3. immediately record `execution_id -> label -> command -> purpose -> lane state` in a durable repo-visible truth surface
4. if the user manually surfaces or renames the terminal in the editor, treat that terminal label as a human recognition anchor only
5. use the approved trusted-local starter commands from `docs/runbooks/managed_cli_terminal_delegation.md`
6. run the prompt-dispatch handshake in order: pre-read, send prompt, read output immediately, send one allowed Enter only if the prompt buffered, read output again, then classify the outcome
7. classify the dispatch outcome only as `started`, `started_after_submit`, or `degraded`
8. once the lane reaches `started` or `started_after_submit` and is not asking for input, stop interacting with it in the current turn and wait for the user to bring it back for acceptance or status
9. keep using the same lane while the execution ID is controllable, output is readable, and the prompt body plus the one allowed Enter step still makes the agent continue running
10. keep the session open during the long task unless restart or cleanup is required

## Hard Rules

1. do not assume a terminal display name is machine-addressable
2. do not use trusted-local auto-approve starter commands for unknown, remote, or production-like hosts
3. do not open a managed terminal before the task is packet-ready
4. do not treat a visible prompt echo as proof that execution already started
5. do not treat visible old terminal output as a reason to replace the lane by itself
6. do not treat the one allowed Enter step as a downgrade signal when the prompt buffered
7. if the execution ID is lost, explicitly downgrade to copy-paste prompt handoff or restart the terminal; do not pretend the renamed tab is still controllable
8. if output is no longer readable, or the prompt body plus the one allowed Enter step still does not make the agent continue running, classify the lane as degraded and restart or downgrade instead of guessing
9. once a strong start signal has appeared, do not send another task instruction in the same packet round just because a receipt, diff, or result file is not visible yet

## References

1. `docs/runbooks/managed_cli_terminal_delegation.md`
2. `.github/skills/managed-cli-terminal-delegation/SKILL.md`
3. `.github/instructions/project-context.instructions.md`