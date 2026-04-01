# Strategy vs Mechanism Layering

This document defines a reusable pattern for repositories that want to formalize multiple reviewer or agent roles without rewriting workflow mechanics each time.

## Goal

Separate two concerns that often get mixed together:

1. `strategy layer` — who is responsible for which kind of judgment
2. `mechanism layer` — how work is frozen, handed off, validated, and recovered

If these are fused into one prompt or one reviewer identity, the workflow becomes brittle.

## Strategy Layer

The strategy layer defines the formal responsibilities of a role first. A concrete tool or executor may implement that role, but it should not define the role.

Typical strategy-layer questions:

1. What risks is this role supposed to notice first?
2. What tradeoffs is it allowed to make?
3. What stable docs or evidence must it respect?
4. What is out of scope for this role?

Examples of strategy roles:

1. runtime correctness reviewer
2. maintainability reviewer
3. protocol boundary reviewer
4. performance reviewer
5. safe-refactor reviewer

These are role definitions, not workflow mechanics.

## Mechanism Layer

The mechanism layer defines the operational contract shared by all those roles.

Typical mechanism-layer elements:

1. task packet
2. audit receipt
3. handoff packet
4. hard gate order
5. validation evidence
6. owner review and git closeout

Examples:

1. `docs/runbooks/resumable-git-audit-pipeline.md`
2. `templates/git_audit_task_packet.template.md`
3. `templates/git_audit_receipt.template.md`
4. `templates/git_audit_handoff_packet.template.md`

This layer exists so a repository can replace an unavailable reviewer without losing workflow continuity.

## Why The Split Matters

Without the split, teams often end up encoding all of the following into one tool-specific prompt:

1. who should review what
2. how to validate it
3. how to recover when that tool stops responding

That creates a hidden single point of failure.

With the split:

1. reviewer identity can change
2. reviewer focus can change
3. packet / receipt / handoff and hard-gate behavior can stay stable

## Example Pattern

One repository may define:

1. a `runtime correctness reviewer`
2. a `maintainability reviewer`

Those are **strategy** choices.

The repository may temporarily implement them with one or more of the following:

1. an external CLI
2. a subagent
3. a main-thread review pass
4. a future custom reviewer agent

The fact that all of these implementations must consume a bounded slice, respect frozen docs, record findings, and survive session interruption is the **mechanism**.

If one executor times out, the repository should be able to switch to another implementation of the same role without inventing a new handoff method. That is the whole point of the split.

## Recommended Assets

When adopting this pattern, repositories should keep at least:

1. one TYPE-A doc that explains the strategy/mechanism split
2. one TYPE-A example set that shows several role families, not just one tool split
3. one role-profile template for formalizing reviewer roles
4. one concrete starter set for the most common first-class roles
5. one resumable workflow mechanism such as packet / receipt / handoff

See `docs/ROLE_STRATEGY_EXAMPLES.md` for a concrete example set.
See `examples/reviewer_roles/` for a ready-to-adapt starter set of 10 formal role profiles.

## Role Profile Template

Use `templates/reviewer_role_profile.template.md` to define concrete roles.

When filling the template:

1. write the role in role-language first
2. list tools or CLIs only as possible executors
3. avoid naming the role after the current tool unless the tool itself is the long-lived product concept

Examples of fields worth freezing:

1. role name
2. primary focus areas
3. non-goals
4. required evidence
5. blocking vs optional output shape
6. whether the role can propose scope expansion

## Executor Selection Policy

The strategy layer defines which role is needed. The mechanism layer defines how work is frozen and recovered. Neither layer specifies which concrete tool runs the role at runtime — that is the executor selection policy.

### Priority Order

| Priority | Executor | Use when |
|---|---|---|
| 1 — primary | CLI (external session) | Default for all bounded execution tasks |
| 2 — fallback | Subagent (internal spawn) | CLI has hit a terminal failure condition |

### When to fall back to subagent

Fall back only when one of the following is **confirmed**:

1. CLI token limit reached mid-task — context exhausted, cannot continue in the same session
2. CLI unresponsive — repeated non-recoverable errors after one retry
3. CLI session cannot be resumed and a handoff packet has been written

### Why the priority matters

CLIs run in isolated sessions with their own context windows. Using a CLI keeps bounded execution outside the main thread's context budget. Subagents share the parent context and are reserved as a fallback, not a default.

### What does not change

Role identity, judgment criteria, and blocking standards are defined in the strategy layer and do not change when the executor type changes. A runtime correctness reviewer has the same focus whether implemented by a CLI or a subagent.

This policy is enforced at runtime by Rule 19 in `.github/copilot-instructions.md`.

---

## Design Rule

When introducing a new external reviewer, internal subagent, or domain-specific agent implementation:

1. define its judgment boundary in the strategy layer
2. reuse existing packet / receipt / handoff and hard-gate logic in the mechanism layer
3. do not encode both layers into a single disposable prompt