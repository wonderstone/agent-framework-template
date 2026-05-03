# Managed CLI Terminal Delegation

- ID: managed-cli-terminal-delegation
- Type: workflow
- Owner: framework-maintainers
- Review Threshold: single-reviewer

## Purpose

Keep the managed CLI terminal delegation workflow honest by requiring packet-ready task boundaries, trusted-local starter commands, and a strict split between human terminal labels and machine execution IDs.

## Triggers

### Positive Triggers

- Use when a task wants to open or keep a long-lived CLI executor session.
- Use when a task mentions auto-approve CLI commands such as `ccrun`, `--dangerously-skip-permissions`, `--dangerously-bypass-approvals-and-sandbox`, or `--yolo`.
- Use when a task wants to send a long prompt through a controlled terminal rather than one-shot execution or copy-paste handoff.
- Use when a task needs guidance on how user-renamed terminal tabs relate to machine control handles.

### Negative Triggers

- Do not use for one-shot non-interactive executor calls where a managed session adds no value.
- Do not use for tasks on unknown, remote, or production-like hosts where trusted-local auto-approve starters are not acceptable.
- Do not use when the workflow assumes a terminal display name is directly machine-addressable.

### Expected Effect

- The agent keeps trusted-local managed-terminal usage bounded, recorded, and honest.
- The execution ID remains the machine control anchor even when the terminal label changes later.
- Prompt dispatch uses the repository-standard handshake, with outcomes limited to `started`, `started_after_submit`, or `degraded` and lane reuse preserved until control, readable output, or prompt-plus-enter viability is lost.

## Entry Instructions

- Read `docs/runbooks/managed_cli_terminal_delegation.md`.
- Confirm the task is packet-ready before opening a managed executor terminal.
- Choose the executor lane and use the approved trusted-local starter command from the runbook.
- Retain the execution ID as the machine control anchor.
- Immediately write `execution_id -> terminal label -> starter command -> purpose -> lane state` into a durable repo-visible truth surface.
- Run the prompt-dispatch handshake in order: pre-read, send prompt, read output immediately, send one allowed Enter only if the prompt buffered, read output again, then classify the outcome.
- Use only `started`, `started_after_submit`, or `degraded` as dispatch outcomes.
- Keep using the same lane while the execution ID is controllable, output is readable, and the prompt body plus the one allowed Enter step still makes the agent continue running.
- If the user later surfaces or renames the terminal tab, treat that name as a human anchor only.
- If the execution ID is lost or the session becomes unresponsive, restart the controlled terminal or fall back to copy-paste prompt handoff explicitly.
- Keep packet boundaries, terminal-state reporting, owner review, and focused validation unchanged.

## References

| Name | Path | Required at invocation | Purpose |
|---|---|---|---|
| managed terminal runbook | docs/runbooks/managed_cli_terminal_delegation.md | yes | Canonical trusted-local managed-terminal workflow |
| managed terminal instruction pack | .github/instructions/managed-cli-terminal-delegation.instructions.md | yes | Execution-time guideline for when to use managed sessions |
| project context adapter | .github/instructions/project-context.instructions.md | yes | Routes managed-terminal topics to the canonical runbook |
| prompt dispatch receipt template | templates/managed_terminal_prompt_dispatch_receipt.template.md | no | Reusable dispatch receipt shape for the managed-terminal handshake and final outcome |
| skill mechanism design | docs/SKILL_MECHANISM_V1_DRAFT.md | no | Governs reusable skill structure and promotion expectations |

## Governance

### Allowed Evidence

- validated repo-local command shapes
- reviewable managed-terminal experiments with observable input/output behavior
- runbook-backed and validator-backed repo documentation

### Reviewer Gate

- Workflow wording or trigger refinements may use single-reviewer promotion; any broadening of the trusted-local safety boundary remains human-reviewed.

### Forbidden Direct Update Inputs

- Do not infer that a terminal display name is machine-addressable merely because it appears in user-visible context.
- Do not broaden trusted-local auto-approve guidance to remote or production-like environments without explicit human review.

## Receipt And Review Matrix

| Field | Proposal evidence tiers | Minimum reviewer threshold | Guardrail override | Promotion tier |
|---|---|---|---|---|
| `purpose` | `1-2 only` | `single-reviewer` | `dual-reviewer` if the trusted-local boundary changes | `human-only` |
| `triggers` | `1-3` | `single-reviewer` | `dual-reviewer` if trigger wording widens host safety assumptions | `human-only` |
| `entry_instructions` | `1-3` | `single-reviewer` | `dual-reviewer` if the control-anchor rules change | `delegated-reviewed` |
| `references` | `1-4` | `single-reviewer` | `single-reviewer`; reference truthfulness required | `delegated-safe` |
| `governance` | `1-2 only` | `single-reviewer` | `dual-reviewer` for reviewer-threshold changes | `human-only` |
| `degradation` | `1-3` | `single-reviewer` | `single-reviewer`; cannot weaken stop rules silently | `delegated-reviewed` |

## Degradation

- If a controlled execution ID is unavailable, degrade to explicit copy-paste prompt handoff rather than pretending the human-visible terminal label is a control surface.
- If the host tooling cannot keep a managed executor terminal alive reliably, restart the session and rewrite the registry truth instead of reusing a stale label.
- If a prompt body was sent but the lane buffered it, use one explicit Enter step and re-read output before deciding whether the outcome is `started_after_submit` or `degraded`.
- If execution ID control is lost, output becomes unreadable, or the prompt body plus the one allowed Enter step still does not make the agent continue running, degrade or restart instead of guessing.

## Validator Notes

- Keep the execution-ID recording rule explicit whenever this skill evolves.
- Do not let display-label convenience language blur the machine-control boundary.