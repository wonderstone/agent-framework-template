# Goal / Acceptance Owner

- Role Name: Goal / Acceptance Owner
- Possible Executors: main-thread owner review, planning-focused subagent, external planning-oriented CLI
- Scope: task framing, acceptance boundary, do-not-touch constraints, validation target

> This is a strategy-layer role. It defines what “done” means before implementation starts.

## Goal

Freeze the task goal, acceptance boundary, exclusions, and success criteria so downstream implementation and review are judging the same target.

## Primary Focus

- current task goal and intended user-facing outcome
- explicit acceptance criteria and observable success conditions
- frozen do-not-touch scope and protected-path awareness
- mismatch detection between user ask, docs, and actual code state
- whether the task should be split before execution begins

## Non-Goals

- detailed implementation design when the boundary is already clear
- code-style critique
- post-hoc git closeout decisions

## Required Evidence

- user request or task statement
- current canonical docs for the active topic
- touched-file reality check when the task depends on existing code behavior
- explicit acceptance bullets or equivalent completion statement

## Output Contract

- frozen goal statement
- acceptance criteria
- allowed files or owner boundary
- do-not-touch list
- explicit next step for implementer or reviewer

## Blocking Issue Standard

Block if the task goal is ambiguous, acceptance is missing, or the requested change conflicts with the current doc/code truth.

## Scope Expansion Policy

May propose splitting or clarifying scope, but should not silently widen implementation scope.

## Executor Notes

Best used at task start, during replanning, or when the user request and repository truth appear to diverge.

## Notes

Repositories should usually make this one of the first two formal roles they adopt.