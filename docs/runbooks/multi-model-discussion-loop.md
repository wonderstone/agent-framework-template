# Multi-Model Discussion Loop

This runbook turns open design questions into a recoverable discussion workflow instead of a chat-only brainstorm.

## Goal

Use this workflow when the task is not "implement the obvious next step" but "decide what the right next step should be".

Typical cases:

1. framework or library selection
2. architecture or migration direction
3. plan review with real tradeoffs
4. sequencing disputes
5. design gaps that should be discussed before code is written

## Core Principle

The mechanism is executor-agnostic.

The framework should not hardcode one vendor CLI as the truth source for design judgment. Instead:

1. freeze the question and constraints in one Markdown packet
2. send that same packet to the available executors
3. require each executor to append feedback to the same document
4. let the main thread synthesize, narrow, and decide
5. only then freeze the execution plan and start implementation

Possible executors include:

1. external CLIs such as Claude Code, Codex, Gemini, or Copilot when installed locally
2. repo-local custom agents
3. internal subagents when external CLIs are unavailable or intentionally skipped
4. the main thread for the final synthesis pass

## Canonical Artifact

| Artifact | Purpose | Default path |
|---|---|---|
| `discussion packet` | Freeze the question, context, options, criteria, round goal, and append-only feedback log | `tmp/discussion/<topic_slug>/discussion_packet.md` |

This workflow deliberately keeps one canonical packet per topic so later rounds can append to the same file instead of scattering reasoning across multiple chats.

## Minimum Flow

1. Create a discussion packet before broad design debate starts.
2. Dispatch the packet to the available executors.
3. Require each executor to append its feedback at the end of the same Markdown file.
4. Let the main thread append a synthesis block after reviewing all feedback.
5. Decide one of three outcomes:
   - freeze a plan and move to execution
   - run a narrower second round
   - stop and escalate because the decision still lacks required truth
6. Before coding, promote the winning direction into the repository's execution surfaces such as roadmap, design doc, checklist, execution contract, or `session_state.md`.

## Round Exit Rule

Do not keep a discussion loop open just because more opinions are available.

Freeze the round when one of these is true:

1. one option is clearly best against the stated criteria
2. the disagreement is now narrow enough for a second focused round
3. a missing truth source blocks honest selection
4. the user asked for a checkpoint instead of a final decision

## When To Run A Second Round

Run another round only when it meaningfully narrows uncertainty.

Good reasons:

1. two top options remain close and the tradeoff is still material
2. an executor exposed a missing constraint or hidden assumption
3. the first round mixed multiple questions that should be split
4. the main thread cannot yet write a trustworthy execution plan

Bad reasons:

1. collecting opinions without a sharper next question
2. asking more tools because one answer was merely inconvenient
3. restarting broad discussion after the decision is already implementation-ready

## Main-Thread Responsibility

The main thread owns:

1. writing the initial packet
2. choosing which executors to involve
3. checking that appended feedback actually answers the packet
4. synthesizing conflicts rather than averaging them blindly
5. deciding whether the next action is `freeze-plan`, `continue-discussion`, or `stop`

The main thread is the decision owner even when many tools participate.

## Executor Rules

Every participating executor should:

1. read the packet before commenting
2. avoid rewriting earlier packet sections
3. append feedback at the end of the file
4. focus on tradeoffs, risks, missing evidence, and recommended direction
5. suggest the narrowest useful next question when another round is needed

## Recommended CLI

Use the bundled generator script:

```bash
python3 scripts/discussion_pipeline.py init-topic ...
python3 scripts/discussion_pipeline.py append-feedback ...
python3 scripts/discussion_pipeline.py append-synthesis ...
```

The framework intentionally does not hardcode vendor-specific command names or flags for Claude Code, Codex, Gemini, or Copilot because local installations differ. Record machine-local executor commands in the repository adapter, local runbooks, or the task packet when your team standardizes them.

## Relationship To The Rest Of The Framework

This runbook complements the rest of the framework like this:

1. `.github/copilot-instructions.md` decides when discussion must happen before implementation
2. `.github/instructions/project-context.instructions.md` routes `discussion|debate|framework choice|plan review` topics here
3. `docs/DOC_FIRST_EXECUTION_GUIDELINES.md` requires a durable discussion surface when a task has real design ambiguity
4. `scripts/discussion_pipeline.py` and `templates/discussion_packet.template.md` make the workflow operational
