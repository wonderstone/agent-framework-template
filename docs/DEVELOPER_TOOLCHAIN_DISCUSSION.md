# Developer Toolchain Discussion

This document is the long-lived discussion surface for one framework gap:

how an agent-enabled repository should define, expose, and use language-specific developer tooling so the agent can reliably:

1. detect syntax and type errors early
2. run lint and compile steps in the right order
3. start or attach to the correct runtime entrypoint
4. use tool output to choose the next corrective action
5. reach a real execution or debug loop rather than stopping at static validation

This is intentionally a discussion and direction-setting document, not yet a committed product contract.

Future opinions, counterarguments, and implementation notes should be appended at the end under the feedback section rather than replacing the current summary silently.

---

## Why This Discussion Exists

The current framework already treats validation as a first-class concept.

That part is real and should not be understated:

1. the project adapter has a `Validation Toolchain` section
2. bootstrap presets prefill test, lint, build, and basic run commands for several project types
3. the architecture doc explicitly states that toolchain setup is a prerequisite for non-trivial implementation work

However, validation coverage is not the same as execution closure.

Today the framework is stronger at answering:

1. what checks should exist before a task can be considered correct
2. what commands a repository should record for tests and structural validation

It is weaker at answering:

1. how the agent should discover and consume language diagnostics during active implementation
2. how the agent should organize compile or start workflows after making a change
3. how the agent should move from a failing run into a repeatable debug loop
4. what tool outputs are authoritative for the next decision when multiple tools disagree

That gap matters because many real tasks fail in the space between edit and acceptance:

1. syntax errors appear before tests can even run
2. a service cannot start because build or env setup is incomplete
3. lint or type errors point to the real issue earlier than runtime tests do
4. a user-visible bug requires a reproducible run or debug loop, not just a passing static check

The framework currently recognizes pieces of that problem, but it does not yet productize the whole loop as a named, reusable surface.

---

## Current Framework State

### What Already Exists

The current template already provides these foundations:

| Surface | Current state | Notes |
|---|---|---|
| Validation Toolchain | Present | Unit / integration / E2E are recorded in the project adapter |
| Build and Test Commands | Present | Typecheck, test, lint, build, and start placeholders exist |
| Bootstrap presets | Present | Project-type presets prefill common commands |
| Runtime guard workflow | Present for opt-in runtime surfaces | Helps protect production-facing execution paths |
| Execution contract | Present | Can already ask for bootstrap-mode allowance and validation gates |

### What Is Still Missing Or Underspecified

| Gap | Why it matters |
|---|---|
| No explicit `Developer Toolchain` section | The agent lacks a canonical place to find diagnostics, run, debug, and task-entry tooling |
| No formal diagnostic priority model | The agent may guess whether to trust language server diagnostics, compiler output, lint, or runtime logs first |
| No debug surface contract | Repro, launch, attach, and log-inspection paths are not first-class adoption inputs |
| No language-tool onboarding checklist | Repositories can confirm the language without confirming the minimum developer tooling required for closure |
| No standard output-consumption loop | The framework does not yet encode how agents should react to tool output in a consistent sequence |

### Working Assessment

The framework is not missing tool awareness entirely.

The more accurate statement is:

the framework already has a validation toolchain model, but it does not yet have a complete developer execution toolchain model.

That distinction is important because the solution should build on the existing validation model rather than replacing it.

---

## Goal

The target capability is not merely:

"record the repository's lint command"

The target capability is:

the framework should let a repository declare enough language-appropriate tooling that an agent can move through this loop with minimal guessing:

```text
edit
→ collect diagnostics
→ fix parse/type/lint failures in the right order
→ build or start the program correctly
→ observe runtime or debug feedback
→ choose the next correction
→ verify the user-visible path
```

In other words, the framework should support a real implementation closure loop, not only a validation checklist.

---

## Proposed Direction

### 1. Keep `Validation Toolchain`, Add `Developer Toolchain`

Do not overload the existing validation section with everything.

Instead, keep two neighboring surfaces in the project adapter:

| Section | Purpose |
|---|---|
| Validation Toolchain | Proves correctness across unit, integration, and E2E tiers |
| Developer Toolchain | Tells the agent how to detect errors, compile, run, inspect, and debug during implementation |

This split keeps the existing architecture honest:

1. validation answers whether the work is acceptable
2. developer tooling answers how the agent reaches a runnable, debuggable state in the first place

### 2. Define A Minimum Developer Toolchain Contract

At adoption time, repositories should confirm at least these fields:

| Field | Meaning |
|---|---|
| Primary language | The dominant implementation language for the touched area |
| Diagnostics | Language server, compiler, or checker used to surface syntax/type errors |
| Lint | Static style and policy checks |
| Format | Formatter used when relevant |
| Build | Compile or packaging command |
| Run | Main dev or local execution command |
| Debug | Launch profile, attach path, or debug entry command |
| Logs or health checks | The fastest reliable runtime feedback loop |
| Package manager | How tool installation and script execution are expected to happen |
| Tool output priority | Which tool output the agent should treat as authoritative first |

### 3. Encode The Consumption Order

The framework should explicitly recommend an output-consumption sequence such as:

```text
language parse or type diagnostics
→ lint
→ build
→ start or attach
→ health or smoke
→ end-to-end acceptance path
```

This does not mean every repository must run every step on every edit.

It means the framework should define the default order in which the agent resolves blockers when multiple tool surfaces are available.

### 4. Treat Debug As A First-Class Adoption Input

Many repositories record test and build commands but never define how debugging is actually entered.

That leaves agents improvising with ad hoc terminal commands or skipping the debug loop entirely.

A reasonable baseline is:

1. identify the default launch or attach path
2. identify the runtime log or health probe that confirms the process is alive
3. identify the shortest repro path for the primary user journey

Even if a project has no formal IDE launch configuration yet, the adapter should still record the canonical debug entry strategy.

### 5. Make Bootstrap Ask For More Than Project Type

Current bootstrap presets infer a lot from project type.

That is useful, but still too coarse for strong closure.

The next iteration should ask or render placeholders for:

1. package manager
2. language diagnostic tool
3. lint tool
4. build tool
5. local run command
6. debug entry path
7. fastest health check or smoke path

This turns language confirmation into toolchain confirmation, which is the actual operational need.

---

## Suggested Template Changes

The following changes appear reasonable without overcomplicating the framework:

| Area | Suggested change |
|---|---|
| `templates/project-context.template.md` | Add a `Developer Toolchain` section next to `Validation Toolchain` |
| `scripts/bootstrap_adoption.py` | Render first-pass developer tooling fields per preset, not only validation and build commands |
| `docs/ADOPTION_GUIDE.md` | Add an adoption step that confirms language plus minimum developer toolchain |
| `templates/execution_contract.template.md` | Add a short tool-output consumption policy for implementation closure |
| `docs/FRAMEWORK_ARCHITECTURE.md` | Clarify the distinction between validation closure and developer execution closure |
| Project adapter triggers | Add trigger keywords for language tooling, diagnostics, lint, build, run, and debug surfaces |

---

## Boundaries And Non-Goals

This proposal should stay disciplined.

Non-goals for the first iteration:

1. building a universal auto-discovery engine for every ecosystem
2. forcing every repository to adopt a full IDE launch configuration on day one
3. guaranteeing that every AI executor can operate every debugger identically
4. replacing repository-specific engineering judgment with a giant generic matrix

The near-term goal is narrower:

give agents a durable, explicit place to find the minimum toolchain information needed to close the loop responsibly.

---

## Open Questions

These questions should be debated before implementation is frozen:

1. should `Developer Toolchain` be mandatory for every project type, or only for repositories with a live runtime path?
2. should debug entry be a required field, or can a reproducible run plus log path satisfy the first iteration?
3. should the framework standardize a single default consumption order, or allow per-project override only?
4. how much language specificity belongs in bootstrap presets versus the final repository adapter?
5. should language-server diagnostics be called out explicitly when the host already exposes diagnostics via editor APIs?
6. should runtime guardrails and developer toolchain guidance stay separate, or cross-link more strongly?

---

## Recommended Next Step

The most reasonable follow-up is a staged change set:

1. add the discussion-backed `Developer Toolchain` concept to docs and templates first
2. add bootstrap placeholders and preset defaults second
3. only after that, consider stronger validation or policy enforcement around missing developer-tool fields

That sequencing keeps the framework understandable while still moving the missing capability into a first-class surface.

---

## Feedback Appendices

Append future discussion notes below this section.

---

### Additional Opinion: Prefer A Progressive Contract Over A Heavy Required Schema

I broadly agree with the direction in this document.

In particular, separating `Validation Toolchain` from `Developer Toolchain` feels like the right abstraction boundary because it distinguishes:

1. proof that work is acceptable
2. the operational path the agent uses to reach that acceptable state

That said, I think the first implementation should be careful not to make `Developer Toolchain` feel like a large mandatory questionnaire that slows adoption.

My current opinion is:

the framework should introduce `Developer Toolchain` as a progressive contract with a small required core and a larger optional enrichment layer.

A reasonable first-pass split might be:

#### Required Core

1. primary language
2. diagnostics command or source
3. build command if applicable
4. run command or runtime entrypoint
5. fastest health check, smoke path, or "none"
6. package manager

#### Optional But Strongly Recommended

1. lint
2. format
3. debug entry
4. log locations or inspection command
5. tool output priority
6. shortest repro path for the main user-visible flow

Why this matters:

1. many repositories can supply a useful run, build, and diagnostics loop quickly
2. fewer repositories have a clean debug story on day one
3. forcing the full schema too early may create placeholder noise rather than usable guidance

I also think the framework should distinguish between:

1. declared tools
2. verified tools

For example, a repository may declare `npm run dev` as the intended run command, but that does not mean the command is currently healthy in the local environment.

That suggests a useful future extension:

the adapter or bootstrap output could record both the intended command and an optional verification status such as `unverified`, `verified once`, or `known broken`.

This would help agents reason more honestly about whether they are following a trusted path or attempting recovery on a partially configured repository.

Finally, I would recommend that the first version explicitly support repositories with no true "debugger" surface.

For many teams, the real debug loop is:

```text
run command
→ observe logs
→ hit health endpoint or smoke script
→ reproduce issue
→ iterate
```

If the framework requires a formal debug configuration too early, it may exclude otherwise well-structured projects that still provide enough runtime observability for effective agent work.

So my preferred implementation principle is:

make the contract strong enough to support implementation closure, but light enough that repositories can adopt it honestly without fiction.

Recommended append format:

```markdown
### Feedback — YYYY-MM-DD — [name or role]

- Perspective: [one-line summary]
- Agreement: [what parts seem right]
- Concern: [what may be over- or under-scoped]
- Suggestion: [specific adjustment]
```

Do not rewrite the earlier sections silently when adding feedback. Add new feedback entries at the end so the discussion history remains inspectable.

---

### Feedback — 2026-04-03 — Claude Sonnet 4.6 (agent)

- **Perspective:** The consumption order and verification status ideas are the most practically impactful additions in this document.
- **Agreement:** The progressive contract framing is correct. Forcing a complete schema before repositories have a working debug story will generate exactly the kind of placeholder fiction the framework should resist. The `Validation Toolchain` / `Developer Toolchain` split is clean and worth keeping — it prevents the two concerns from conflating in ways that make both harder to reason about.
- **Concern:** The proposed consumption order (`parse/type → lint → build → start → health → E2E`) is reasonable as a default, but the framework currently has no mechanism to record *when to stop* in that sequence. An agent following the order on a task that only touches a leaf utility function may end up attempting a full service start unnecessarily. Without a concept of task scope, the sequence becomes overhead rather than guidance. Similarly, the `verified once` / `unverified` / `known broken` status idea is the right direction, but if it is only advisory and never triggers a behavior change in the agent, it will drift out of sync quickly and become noise.
- **Suggestion 1 — Scope hint on Developer Toolchain entries:** Each toolchain entry should carry an optional `scope` tag, e.g. `file`, `module`, `service`, `full-stack`. The agent can then select the minimum viable sequence for the task at hand rather than running the full ladder every time. This does not require inference — the repository registers the scope explicitly at adoption time.
- **Suggestion 2 — Make verification status actionable, not decorative:** The adapter should not just record `unverified` passively. It should specify what the agent is expected to do when it encounters an unverified command: skip it and log, attempt it and treat failure as recoverable, or halt and prompt the user. Without an associated behavior policy, the status is documentation rather than a decision surface.
- **Suggestion 3 — Treat the repro path as the diagnostic entry point, not the exit:** The shortest repro path for the main user-visible flow is currently placed in the "optional but strongly recommended" tier. I would promote it to required for any repository with a live runtime path. The agent's most expensive recoveries happen when the repro path is missing or wrong — not when lint configuration is incomplete. If a repository cannot yet state a repro path, `none` is a valid and honest value, but the field should be present so the gap is visible rather than assumed.

### Feedback — 2026-04-03 — GitHub Copilot (GPT-5.4)

- **Perspective:** The highest-value evolution is to make `Developer Toolchain` a truthful decision surface, not just a registry of commands.
- **Agreement:** The separation from `Validation Toolchain` is correct, and the newer direction around scope tags, repro paths, and actionable verification status makes the proposal materially stronger. Those additions move the document away from passive documentation and toward operational guidance an agent can actually follow.
- **Concern:** The remaining risk is drift between declared tooling and real repository behavior. A repository can truthfully record `run`, `build`, and `health` commands once, then gradually lose confidence as environments, scripts, or startup assumptions change. If the framework only records intended commands, agents may still follow a stale path and waste time on recoveries that look legitimate on paper. There is also some risk of duplicating adjacent framework surfaces if `logs`, `health`, and `repro` are described here without clearly pointing to the repository's broader runtime-evidence story.
- **Suggestion 1 — Add a lightweight receipt hook for toolchain truthfulness:** For commands that matter to closure, allow an optional last-known receipt such as a date, validation note, or command result summary. The goal is not heavy auditing, just enough evidence to distinguish "declared" from "recently exercised." That would make toolchain entries more resilient against silent drift.
- **Suggestion 2 — Define explicit stop semantics per row:** Each important entry should be able to say whether failure means `stop`, `fallback`, or `continue with warning`. That gives the agent a direct policy surface when a command is missing, flaky, or intentionally non-authoritative for the current task.
- **Suggestion 3 — Cross-link Developer Toolchain with runtime evidence rather than duplicating it:** This document should stay focused on how the agent enters the implementation loop. When a repository already has a stronger source of truth for logs, health probes, smoke paths, or incident evidence, the `Developer Toolchain` section should reference that surface rather than restating it inconsistently.
