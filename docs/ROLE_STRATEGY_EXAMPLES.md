# Role Strategy Examples

This document provides concrete examples of strategy-layer role definitions that repositories can adapt.

These examples are intentionally broader than a single `Codex vs Claude` split. The goal is to help teams think in role families, not tool names.

Rule of thumb:

1. name the role by the judgment it provides
2. treat CLIs, subagents, or custom agents as replaceable executors of that role
3. only mention a tool name as an example implementation, never as the role's identity

Each example below should be read together with the mechanism layer:

1. task packet
2. audit receipt
3. handoff packet
4. hard-gate order
5. owner review

The role decides **what to judge**. The mechanism decides **how the judgment participates in a recoverable workflow**.

The template also ships a concrete starter pack under `examples/reviewer_roles/`. Those files turn the role families below into ready-to-adapt profiles instead of leaving them only as prose examples.

If you want to see how these roles fit into a repository instead of reading them in isolation, inspect `examples/demo_project/`. The demo does not implement every role, but it shows the surrounding assets those roles expect: project context, roadmap, session state, code, tests, and audit artifacts.

Recommended adoption order:

1. first batch: goal/acceptance owner, plan/checkpoint owner, runtime correctness reviewer, boundary/contract reviewer, git closeout reviewer, maintainability reviewer
2. second batch: observability/failure-path reviewer, performance/benchmark reviewer, migration/compatibility reviewer, docs/spec drift reviewer

## 1. Runtime Correctness Reviewer

Possible executors:

1. external runtime-focused CLI review
2. internal runtime-focused reviewer agent
3. main-thread correctness review for a very small bounded slice

Primary focus:

1. control-flow mistakes
2. state mutation correctness
3. protocol and contract edge cases
4. failure-path correctness
5. hot-path inefficiencies that directly affect correctness or latency

Non-goals:

1. broad code-style cleanup
2. cosmetic refactors
3. architecture redesign unless it directly fixes a correctness risk

Best used for:

1. checkpoint logic
2. transport boundaries
3. reducer / merge logic
4. retry and timeout paths

## 2. Maintainability Reviewer

Possible executors:

1. external maintainability-oriented CLI review
2. internal architect-style reviewer agent
3. main-thread structural review for a very small bounded slice

Primary focus:

1. structural simplification
2. safe refactor opportunities
3. readability vs complexity tradeoffs
4. drift from stable docs and intended architecture

Non-goals:

1. speculative performance tuning with no evidence
2. protocol-lawyering when the contract is already explicit and validated

Best used for:

1. large slices that work but feel overgrown
2. cross-module edits with maintainability risk
3. post-fix cleanup after a correctness patch

## 3. Git Closeout Reviewer

Possible executors:

1. main-thread reviewer
2. external reviewer with bounded diff-only scope

Authority boundary:

1. this role reviews closeout readiness and commit boundary quality
2. main-thread owner normally executes final commit and normal push after this role reports readiness
3. this role should escalate only when closeout is not ready or a higher-risk Git action is requested

Primary focus:

1. whether the diff still matches the frozen packet
2. whether unrelated dirt is leaking into the closeout
3. whether validation evidence matches what is being committed
4. whether the commit boundary is coherent

Non-goals:

1. redesigning the already accepted implementation
2. broad feature brainstorming

Best used for:

1. pre-commit inspection
2. selective staging decisions
3. phase closeout checks
4. deciding whether the main thread can safely proceed to commit/push without further cleanup

Release-adjacent assets that pair well with this role:

1. `CHANGELOG.md`
2. `VERSION`
3. `.github/RELEASE_TEMPLATE.md`

## 4. Protocol Boundary Reviewer

Possible executors:

1. protocol-aware agent
2. external reviewer with contract focus

Primary focus:

1. request/response schema drift
2. serialization and deserialization assumptions
3. compatibility hazards across boundaries
4. silent contract widening or narrowing

Non-goals:

1. internal code organization unrelated to the boundary

Best used for:

1. API slices
2. worker protocol changes
3. event model edits
4. gateway / client contract work

## 5. State And Checkpoint Integrity Reviewer

Possible executors:

1. runtime correctness reviewer
2. dedicated checkpoint/state agent

Primary focus:

1. snapshot correctness
2. merge/reducer invariants
3. replay / resume semantics
4. state contamination across sessions or branches

Non-goals:

1. generic refactor advice unless it protects state invariants

Best used for:

1. durable resume work
2. memory persistence changes
3. graph state mutation logic

## 6. Performance And Benchmark Reviewer

Possible executors:

1. performance-focused reviewer agent
2. external benchmark-aware reviewer

Primary focus:

1. hot-path inefficiencies
2. unnecessary allocations or copies
3. benchmark regressions
4. abstractions that distort a performance-sensitive path

Non-goals:

1. subjective “this feels slow” claims with no repository evidence
2. refactors that reduce readability with no measured gain

Best used for:

1. allocation-sensitive code
2. serializers and event writers
3. reducers on large state
4. inner-loop transforms

## 7. Observability And Failure-Path Reviewer

Possible executors:

1. operations-aware reviewer agent
2. runtime correctness reviewer with observability scope

Primary focus:

1. whether the system emits enough evidence to debug failure
2. whether request IDs, execution truth, checkpoints, or state transitions are visible
3. whether failure modes are distinguishable in logs or outputs

Non-goals:

1. inventing a full telemetry platform for a bounded slice

Best used for:

1. failed-turn diagnostics
2. stream event contracts
3. health and memory reporting
4. background job tracing

## 8. Safe Refactor / Migration Reviewer

Possible executors:

1. maintainability reviewer
2. migration-specific reviewer role

Primary focus:

1. compatibility boundaries
2. staged migration safety
3. shim lifetime and deprecation plan
4. whether cleanup is sequenced safely

Non-goals:

1. runtime micro-optimization
2. feature expansion during migration

Best used for:

1. moving canonical owners
2. shrinking legacy surfaces
3. replacing adapters or shims
4. package or module reorganizations

## 9. Docs And Spec Drift Reviewer

Possible executors:

1. architect-style reviewer
2. docs-aware subagent

Primary focus:

1. code vs doc mismatches
2. stale examples or runbooks
3. undocumented behavior entering the repository
4. whether stable docs still match the current implementation slice

Non-goals:

1. rewriting docs for style only

Best used for:
1. keeping architecture docs aligned after framework upgrades
2. checking adoption docs after bootstrap changes
3. reviewing runbooks and demo artifacts after workflow changes
4. catching stale release or compatibility guidance

1. public contract changes
2. architecture shifts
3. process workflow changes

## Brainstorming Rule

When designing reviewer or agent splits for a repository, do not stop at the first two obvious roles.

Do not ask only:

1. which CLI should review this

Also ask:

1. which judgment boundaries must be explicit before implementation starts
2. which judgments are needed to keep work resumable and auditable
3. which judgments can wait until the repository reaches a higher maturity level

1. what judgment role is actually needed here
2. can that role be fulfilled by more than one executor if the current tool fails

At minimum, ask whether the repository would benefit from examples in these families:

1. correctness
2. maintainability
3. git closeout
4. protocol boundary
5. state/checkpoint integrity
6. performance
7. observability/failure-path
8. safe migration/refactor
9. docs/spec drift

Not every repository needs all of them. But thinking through the list usually improves the strategy layer, because it exposes what judgments are currently overloaded into one vague “reviewer” role.
