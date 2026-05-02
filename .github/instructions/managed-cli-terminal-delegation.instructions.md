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
3. immediately record `execution_id -> label -> command -> purpose -> control state` in a durable repo-visible truth surface
4. if the user manually surfaces or renames the terminal in the editor, treat that terminal label as a human recognition anchor only
5. use the approved trusted-local starter commands from `docs/runbooks/managed_cli_terminal_delegation.md`
6. stage the prompt body first and send one explicit Enter action when the executor lane requires Enter to dispatch the prompt
7. do not classify the managed session as running until the Enter step has been sent and a follow-up terminal output read has been attempted
8. keep the session open during the long task unless restart or cleanup is required

## Hard Rules

1. do not assume a terminal display name is machine-addressable
2. do not use trusted-local auto-approve starter commands for unknown, remote, or production-like hosts
3. do not open a managed terminal before the task is packet-ready
4. do not treat a staged prompt as active execution before the explicit Enter dispatch step
5. if the execution ID is lost, explicitly downgrade to copy-paste prompt handoff or restart the terminal; do not pretend the renamed tab is still controllable

## References

1. `docs/runbooks/managed_cli_terminal_delegation.md`
2. `.github/skills/managed-cli-terminal-delegation/SKILL.md`
3. `.github/instructions/project-context.instructions.md`