# AI Traceability And Recovery Discussion

This document opens a framework-level discussion about a growing gap in AI-enabled software development:

when code or runtime behavior goes wrong, teams often struggle to identify the real root cause quickly enough, confidently enough, or truthfully enough.

This is becoming more important because the human development posture is changing.

In many AI application teams, humans increasingly:

1. care primarily about whether the application-level outcome works
2. no longer hold a detailed mental model of the full code path
3. may not understand the underlying framework, orchestration, prompts, tool loops, or runtime contracts in depth
4. still remain accountable for security, reliability, regression handling, and user trust

That combination creates a real framework problem, not just a documentation problem.

If the implementation stack becomes easier to change but harder to understand, then traceability, diagnosability, and recovery can no longer be optional engineering habits.

They need to become explicit framework surfaces.

This is intentionally a discussion document, not yet a frozen product contract.

Future opinions, objections, and implementation notes should be appended at the end under the feedback section rather than replacing the current summary silently.

---

## Why This Discussion Exists

AI-assisted coding changes the economics of implementation.

It becomes easier to:

1. generate code quickly
2. refactor across unfamiliar files
3. introduce new integration paths
4. ship behavior that appears correct at the surface level

It also becomes easier to:

1. lose the causal chain of why the system behaves a certain way
2. mask the true source of a failure behind several generated layers
3. fix symptoms without preserving the explanation of the failure
4. rely on an application "working now" without understanding whether it is safe or stable

That matters for at least four reasons:

1. root-cause analysis becomes slower and less reliable when nobody can reconstruct the full execution path
2. security review becomes weaker when the code path, prompt path, tool path, and config path are not tied together explicitly
3. post-incident recovery becomes more expensive when logs, repro steps, and change intent are fragmented
4. teams lose trust in AI-assisted delivery if failures cannot be explained after the fact

The framework already has pieces related to this space:

1. doc-first planning
2. session state
3. execution contracts
4. runtime surface protection
5. developer toolchain discussion
6. receipt-anchored closeout patterns

But those pieces do not yet add up to a single explicit framework stance on:

how an AI-enabled repository should preserve causal traceability from intent to change to runtime to failure to recovery.

---

## The Working Problem Statement

The problem is not only:

"AI wrote code that broke."

The deeper problem is:

when the system breaks, the repository often cannot answer these questions quickly and honestly:

1. what change introduced the behavior
2. what user-visible surface was affected
3. what code path, config path, tool call, prompt surface, or dependency path participated
4. what observable evidence first indicated the failure
5. what the shortest reliable repro path is
6. whether the issue is a correctness bug, a security issue, a state/config issue, or a hallucinated implementation path
7. what evidence supports the claimed fix
8. whether the system is actually understood now or only patched superficially

If those answers are missing, then the team does not really have operational control, even if the feature appears to work again.

---

## Framework-Level Design Goal

The goal should not be:

"make every engineer understand every generated line of code again."

That is unrealistic.

The goal should be:

make every non-trivial change and every meaningful failure reconstructable enough that a responsible human or agent can answer:

```text
what changed
→ what path it affected
→ how the system failed
→ how the failure was observed
→ how the root cause was established
→ what fix was applied
→ what evidence shows the fix is real
→ what residual risk remains
```

In other words:

the framework should optimize for operational legibility, not total human memorization.

---

## Proposed Mechanism Direction

The most reasonable way to approach this is not with one giant universal system.

It is with a small set of explicit, composable mechanisms that together create a traceability and recovery loop.

### 1. Require A Change Intent Surface For Non-Trivial Work

Before meaningful implementation, the repository should record:

1. what problem is being changed
2. what user-visible behavior is expected
3. what files or surfaces are expected to move
4. what risks are already known
5. what validation and runtime evidence will be used

This should build on the framework's existing doc-first planning rule rather than inventing a separate planning culture.

Without a written intent surface, later failure analysis starts from guesswork.

### 2. Introduce A Failure / Incident Packet Surface

When runtime behavior is broken, the framework should support a durable failure packet that records:

1. symptom summary
2. impacted surface
3. exact repro steps
4. first observed evidence
5. suspected layers involved
6. current hypothesis
7. commands, logs, traces, screenshots, or output references
8. resolution status

This is similar in spirit to task packet and handoff artifacts, but aimed at diagnosis and recovery rather than implementation fan-out.

The key idea is:

the repo should not force every debugging loop to live only in chat or terminal scrollback.

### 3. Define A Root-Cause Recording Contract

The framework should encourage teams to distinguish between:

1. symptom fixed
2. root cause identified
3. root cause only suspected

That sounds small, but it matters a lot.

Many AI-heavy teams can restore surface behavior without proving causality.

A lightweight root-cause contract could require:

1. cause statement
2. evidence for that statement
3. fix statement
4. why the fix addresses the cause rather than the symptom
5. residual unknowns

This makes postmortem quality much stronger without requiring a full formal incident process for every bug.

### 4. Make Runtime Evidence A First-Class Surface

If the framework wants agents to debug responsibly, it should explicitly record where evidence comes from.

Relevant evidence surfaces may include:

1. logs
2. health endpoints
3. smoke scripts
4. traces
5. metrics
6. audit receipts
7. browser or API repro scripts
8. security-relevant config or policy files

The framework does not need to standardize every observability tool.

It does need to standardize that a repository declares:

1. where evidence lives
2. which evidence is authoritative for which class of failure
3. what the fastest trustworthy repro path is

### 5. Create A User-Surface-To-Code-Surface Map

One of the hardest parts of AI application debugging is that people think in user journeys, but the repo is organized in modules and services.

The framework should therefore encourage a small mapping layer:

1. user-visible surface or workflow
2. primary owning code paths
3. primary runtime/config dependencies
4. primary validation or smoke checks
5. primary log or trace source

This does not need to be a giant architecture atlas.

Even a partial map for the top few user-critical paths would materially improve triage, safety review, and change confidence.

### 6. Treat Security-Relevant Traceability Separately From Generic Debugging

Not every failure is a security issue.

But when the affected path touches:

1. auth
2. permissions
3. secrets
4. external tools
5. model routing
6. prompt injection boundaries
7. data export or retention

the framework should require a stronger traceability mode.

That stronger mode could require:

1. explicit impacted trust boundary
2. config and secret surface references
3. audit log references if available
4. rollback or containment steps
5. confirmation that the fix was validated against abuse or misuse paths, not only happy-path behavior

### 7. Add Recovery-State Truthfulness As A Closeout Requirement

A common failure mode is:

the system is working again, but the repository truth does not explain why.

The framework should discourage closeout language like "resolved" or "completed" when:

1. the repro path is not captured
2. the root cause is still hypothetical
3. the runtime evidence was not preserved
4. the residual risk is not stated

This extends the same truthfulness principle already present in closeout auditing.

---

## A Possible Minimal Mechanism Set

To keep this practical, the first iteration could be very small.

A reasonable minimum set might be:

| Mechanism | Purpose |
|---|---|
| Change intent note | Freeze what was supposed to change and why |
| Failure packet | Preserve repro, evidence, and current hypothesis when behavior breaks |
| Runtime evidence map | Tell the agent where logs, health checks, smoke paths, and traces live |
| User-surface map | Connect user-visible flows to code/runtime ownership |
| Root-cause closeout note | Distinguish symptom fix from established cause |

That set is much lighter than a full incident-management platform, but much stronger than relying on chat history and memory.

---

## How This Could Land In The Framework Template

This discussion is only useful if it can be turned into reusable template surfaces.

### 1. Add A New Long-Lived Canonical Doc

The framework could eventually ship a stable companion doc such as:

`docs/TRACEABILITY_AND_RECOVERY_MODEL.md`

Its purpose would be to define:

1. expected repository traceability surfaces
2. terminology for symptom vs cause vs evidence vs recovery
3. minimum requirements for high-risk runtime paths

This current file is the discussion surface before that contract is frozen.

### 2. Extend The Project Adapter

The project adapter could gain new fields or sub-sections such as:

| Field | Meaning |
|---|---|
| Critical user surfaces | Main user-visible flows worth tracing explicitly |
| Runtime evidence sources | Logs, traces, metrics, smoke scripts, health paths |
| Failure packet location | Where diagnosis artifacts live in this repository |
| Security-sensitive paths | Auth, secrets, external tools, model/tool routing, export paths |
| Root-cause expectation | What evidence is required before a fix can be declared understood |

This would make traceability discoverable instead of tribal.

### 3. Add New Templates

Reasonable template candidates:

| Template | Purpose |
|---|---|
| `templates/failure_packet.template.md` | Debugging / incident packet for reproducible failures |
| `templates/runtime_evidence_map.template.md` | Declares where logs, health, smoke, traces, and metrics live |
| `templates/user_surface_map.template.md` | Maps user journeys to code, config, and validation surfaces |
| `templates/root_cause_note.template.md` | Records cause, evidence, fix, and residual unknowns |

These templates should stay small and operational, not bureaucratic.

### 4. Update Adoption Guidance

`docs/ADOPTION_GUIDE.md` could eventually include an adoption step asking teams to confirm:

1. what their top user-visible surfaces are
2. where runtime evidence comes from
3. how failures should be recorded
4. which paths need stronger security traceability

That would move the framework from "AI can edit here" toward "AI work remains diagnosable here."

### 5. Add Trigger Keywords

The project adapter should be able to route future sessions to these surfaces when messages include topics such as:

1. root cause
2. incident
3. failure packet
4. repro
5. traceability
6. observability
7. recovery
8. security review
9. runtime evidence

### 6. Connect With Existing Mechanisms Rather Than Replacing Them

This should not become a parallel framework.

It should integrate with:

1. doc-first execution
2. developer toolchain
3. runtime surface protection
4. closeout truth auditing
5. execution contract
6. packet / receipt / handoff mechanisms

The goal is a stronger chain of evidence, not another disconnected documentation island.

---

## Design Principles For The First Iteration

If this moves forward, I think the first version should follow these principles:

### 1. Optimize For Reconstruction, Not Exhaustiveness

The framework does not need every detail of every execution path.

It needs enough durable structure that a future human or agent can reconstruct what happened without starting from zero.

### 2. Prefer Small Honest Fields Over Large Fictional Forms

A short accurate failure packet is better than a large template full of placeholders nobody trusts.

### 3. Separate Symptom Recovery From Understanding

The framework should allow:

1. behavior restored
2. cause not yet fully proven

Those are different states and should stay different.

### 4. Make High-Risk Paths Carry Higher Requirements

Not every bug deserves the same ceremony.

Security-sensitive, user-critical, or production-default paths should have stronger traceability requirements than low-risk internal tooling.

### 5. Preserve Evidence Close To The Repository

If the key debugging truth only exists in ephemeral chat or terminal history, the framework has not solved the actual problem.

---

## Open Questions

These are the questions I think the discussion should focus on next:

1. what is the minimum traceability surface that gives real value without slowing normal development too much?
2. should failure packets be mandatory only for production or user-visible failures, or for all non-trivial runtime bugs?
3. how much of the user-surface map should live in the project adapter versus a separate canonical doc?
4. should root-cause recording be required before closeout, or only strongly recommended?
5. how should security-sensitive paths opt into stronger evidence requirements without turning the whole framework into a compliance system?
6. how do we keep the mechanism lightweight enough that teams will actually maintain it?
7. which existing framework surface should own the truth about runtime evidence sources?

---

## Recommended Next Step

The most reasonable next step is not to jump directly into hard enforcement.

A staged path looks safer:

1. agree on the problem framing and terminology first
2. define the minimum mechanism set second
3. prototype one or two small templates such as a failure packet and runtime evidence map
4. test those templates in a real AI-assisted application workflow
5. only then decide what belongs in the default framework template versus optional capability packs

That sequence gives us a better chance of landing something teams will actually use.

---

## Feedback Appendices

Append future discussion notes below this section.

---

### Feedback — 2026-04-03 — Claude Sonnet 4.6 (agent)

- **Perspective:** The document is asking the right question but may be proposing the wrong unit of work — the failure packet and root-cause note are structurally sound, but the user-surface-to-code-surface map is where the most return on investment lies.
- **Agreement:** The core framing is correct. The shift from "AI wrote broken code" to "the repository cannot reconstruct what happened" is the real problem worth solving. The principle of separating *symptom fixed* from *root cause identified* is operationally important and easy to lose in practice — the framework making that distinction explicit is one of the highest-value things it can do. The staged path in the next step section is also right; skipping directly to enforcement would create compliance theater.
- **Concern 1 — The failure packet may see selective usage:** Failure packets are most likely to be filled out when people are already methodical. They are least likely to be filled out under pressure during actual incidents — which is exactly when they matter most. The mechanism design should account for this asymmetry. If filling out a failure packet requires assembling all eight fields before it is useful, adoption will be poor. A better model might be a *progressive packet*: even a two-field entry (symptom + repro steps) is better than nothing, and the agent can prompt for additional fields as the investigation develops. The framework should make partial packets valid, not treat incomplete packets as non-conformant.
- **Concern 2 — The user-surface map is undervalued in the proposal:** It is currently listed as one of five mechanisms at roughly equal weight. I would argue it is the foundational mechanism the other four depend on. Without knowing which user surface a failure touches, the agent cannot determine whether the failure packet warrants full security-level traceability or a lightweight root-cause note. The map is also the most stable artifact — user surfaces change more slowly than code paths — which makes it the most cost-effective thing to maintain. I would recommend elevating it.
- **Concern 3 — "Residual risk" is listed as a field but has no acceptance criteria:** The root-cause closeout note requires a *residual unknowns* field. That is good. But without a definition of what an acceptable residual risk statement looks like, agents and humans will write it as a disclaimer rather than a decision surface. A residual risk statement should at minimum answer: *what could still go wrong, and what would we observe first if it does?* That framing converts the field from a liability disclaimer into an early-warning specification.
- **Suggestion 1 — Introduce a failure severity tier at packet creation time:** Not every failure needs the same packet depth. The framework should define at minimum two tiers — *lightweight* (single user, non-production, no security surface) and *full* (production-visible, security-sensitive, or regression of a previously closed issue). The tier should be declared at packet creation, not retrospectively. This gives agents a clear branching rule and prevents the full packet format from discouraging usage on low-stakes bugs.
- **Suggestion 2 — Bind the runtime evidence map to the Developer Toolchain, not a separate template:** The developer toolchain discussion already proposed recording where logs, health checks, and smoke paths live. Creating a separate `runtime_evidence_map.template.md` risks duplicating that surface and eventually diverging from it. The better design is to make the runtime evidence map a sub-section of the developer toolchain entry in the project adapter, with a promotion path to a standalone doc only for complex multi-service repositories. Single-source-of-truth here is more important than organizational tidiness.
- **Suggestion 3 — The security traceability mode needs a trip wire, not just a higher-bar checklist:** The current proposal says that when a failure touches auth, secrets, or prompt injection boundaries, a stronger traceability mode is required. That is the right policy. But "required" without a trigger mechanism means it only activates when someone remembers to apply it. The project adapter's security-sensitive path list should function as a trip wire: when any file path, config key, or runtime log in the failure packet matches a declared security surface, the agent should automatically escalate to the full security traceability mode rather than waiting for human judgment to apply the upgrade. This is the kind of mechanical enforcement that actually changes behavior under pressure.

---

## Round 1 Summary

After the first discussion pass, I think several points are now strong enough to treat as provisional consensus:

1. the problem is real and framework-shaped, not merely a team education issue
2. the target is operational legibility and reconstruction, not full human understanding of every generated detail
3. the framework should distinguish symptom recovery from root-cause understanding
4. the solution should be mechanism-oriented and lightweight, not a heavyweight compliance layer
5. this work should integrate with existing framework surfaces rather than becoming a parallel documentation system

Round 1 also surfaced several likely design pivots:

1. the `user-surface-to-code-surface map` may be more foundational than originally framed
2. the `failure packet` likely needs to be progressive rather than all-or-nothing
3. `runtime evidence` may belong inside the `Developer Toolchain` surface unless complexity justifies promotion
4. security-sensitive traceability probably needs an automatic escalation trigger, not only policy language

That means the discussion has moved far enough that the next round should not stay broad.

The next round should focus on narrowing the mechanism set and assigning ownership of each truth surface.

---

## Round 2 Focus

This second round is intentionally narrower.

The goal is to decide which mechanisms belong in the minimum framework contract and how they should connect to existing template surfaces.

Comments appended in this round should try to answer one or more of the questions below directly.

### Question 1 — What Is The True Foundation?

Which mechanism should be treated as foundational in v1?

Candidates:

1. `user-surface-to-code-surface map`
2. `failure packet`
3. `root-cause closeout note`
4. `developer toolchain` plus runtime evidence sub-section

What we need from feedback:

1. which artifact should be required first
2. which other artifacts depend on it
3. what the minimum viable contents of that artifact are

### Question 2 — Should Failure Capture Be Progressive By Design?

Should the framework explicitly allow a partial failure packet such as:

1. symptom
2. impacted surface
3. repro steps if known

with the rest filled in later as the investigation matures?

What we need from feedback:

1. whether progressive packets should be first-class
2. what the minimum acceptable first save is
3. what event should require promotion from lightweight to full packet

### Question 3 — Where Should Runtime Evidence Live?

Should runtime evidence be:

1. a sub-section of `Developer Toolchain`
2. a separate reusable template
3. recorded in both places with one acting as a promoted detailed surface

What we need from feedback:

1. what should be the single source of truth
2. when a repository is complex enough to justify a dedicated runtime evidence doc
3. how to avoid duplicated maintenance

### Question 4 — How Should Security Escalation Actually Trigger?

If a failure touches a security-sensitive path, what mechanism should upgrade traceability requirements?

Candidate triggers:

1. path match against declared sensitive files or directories
2. config key or secret surface match
3. affected user surface marked as sensitive
4. explicit human classification
5. some combination of the above

What we need from feedback:

1. which trigger should be automatic
2. which trigger should remain human-reviewed
3. what extra evidence becomes mandatory after escalation

### Question 5 — What Can Realistically Become Default Template Surface?

Not every good mechanism should ship as a default required template.

For each proposed artifact, feedback should state whether it belongs as:

1. default template surface
2. optional capability pack
3. advanced repository-only extension

The artifacts currently under consideration are:

1. `failure_packet.template.md`
2. `user_surface_map.template.md`
3. `root_cause_note.template.md`
4. runtime evidence as a dedicated template or a `Developer Toolchain` sub-section

---

## Round 2 Suggested Feedback Format

To keep the discussion comparable across contributors, append feedback in this shape when possible:

```markdown
### Feedback — YYYY-MM-DD — [name or agent]

- Perspective:
- Strong agreement:
- Main concern:
- Recommendation for v1:
- What should be deferred:
- Proposed ownership:
```

This is a suggested format, not a hard requirement.

The important thing is that appended feedback should stay concrete and decision-oriented.

---

## Round 2 Decision Target

If this round goes well, the desired outcome is not a full final contract yet.

The desired outcome is a narrower implementation target:

1. one foundational traceability artifact
2. one failure-capture artifact
3. one clear owner for runtime evidence truth
4. one security escalation rule
5. a recommendation about which surfaces ship by default versus optional capability

If those five things become clear, the framework is ready to move from discussion into a small v1 mechanism draft.

---

### Feedback — 2026-04-03 — Claude Sonnet 4.6 (agent) — Round 2

- **Perspective:** The five decision targets at the end of this section are the right frame. I will try to give a direct answer to each rather than reopening earlier debates.

- **Strong agreement:** The Round 1 summary correctly identifies the pivots. The progressive packet and the automatic security escalation trigger both deserve to land in v1, not deferred to later. Deferring either one would leave the framework with the same gap it already has: policies that only activate when someone remembers to apply them.

- **Main concern:** The five decision targets are listed as parallel deliverables with no ordering dependency stated. In practice they are not parallel. The user-surface map has to exist before the security escalation trigger is useful, because path-matching and surface-marking both require knowing what the sensitive surfaces are. If escalation is specified before the map is defined, the trigger has nothing to evaluate against. This ordering dependency should be made explicit in v1 scoping, not left to implementers to discover.

- **Recommendation for v1 — answering each question directly:**

  **Q1 — Foundation:** The `user-surface-to-code-surface map` is the correct foundational artifact. All four other mechanisms depend on it in some way — failure severity tiering needs to know what surface was hit, security escalation needs the sensitive-surface list, runtime evidence needs to know which surfaces are production-critical. Minimum viable contents for v1: (a) surface name, (b) primary code path or entry point, (c) sensitive yes/no, (d) fastest repro path, (e) primary runtime evidence source. Nothing else is required in the first pass. The map does not need to be complete at adoption — partial coverage of the top two or three user-critical paths is enough to make the other mechanisms functional.

  **Q2 — Progressive packets:** Yes, progressive packets should be first-class. The minimum acceptable first save is two fields: *symptom* and *impacted surface*. These two fields are almost always knowable immediately and together they let the agent determine severity tier and check the user-surface map. Promotion from lightweight to full packet should be required when: (a) the failure is reproduced on a sensitive surface, (b) a fix has been applied but root cause is still suspected rather than proven, or (c) the issue recurs after a previous closeout. Promotion should not require human initiation — the agent should prompt for it when any of the three conditions are met.

  **Q3 — Runtime evidence ownership:** Single source of truth is `Developer Toolchain` as a sub-section. The promotion threshold to a standalone doc should be explicit: a repository with three or more independently-operated services, each with distinct log pipelines and health surfaces, is complex enough to justify promotion. Below that threshold, a sub-section is sufficient and a separate template creates maintenance drag. The `Developer Toolchain` cross-link from Q3 in the DEVELOPER_TOOLCHAIN_DISCUSSION is also consistent with Copilot's Round 1 suggestion there — these two documents are now aligned on this point and v1 should close it.

  **Q4 — Security escalation trigger:** The right v1 answer is a combination of path match (automatic) and affected surface marked sensitive in the user-surface map (automatic), with explicit human classification as an override path only. The trigger should be automatic when either condition is met independently — it should not require both. What becomes mandatory after escalation: (a) impacted trust boundary named explicitly, (b) config or secret surface referenced, (c) at minimum one negative-path validation stated (not only happy-path). Audit log references and rollback steps should be strongly recommended but not required in v1 to avoid blocking teams without formal audit infrastructure.

  **Q5 — Default vs optional:**

  | Artifact | Recommendation |
  |---|---|
  | `user_surface_map.template.md` | Default template surface — required for any repository with a live runtime path |
  | `failure_packet.template.md` | Default template surface — progressive, two-field minimum |
  | `root_cause_note.template.md` | Default template surface — required at closeout when cause is still suspected |
  | Runtime evidence as `Developer Toolchain` sub-section | Default template surface — sub-section first, standalone promotion explicit |

  No proposed artifact belongs in optional-only. Pushing all four to optional would reproduce the current state where teams only use these surfaces when they are already methodical.

- **What should be deferred:** Metrics and traces as first-class evidence sources. They belong in the runtime evidence surface eventually, but requiring them in v1 would exclude most repositories that have logs and health endpoints but no structured tracing. Logs plus health plus repro path is the right v1 bar. Traces and metrics are v2 enrichment.

- **Proposed ownership:** The `user-surface-to-code-surface map` should be owned by the project adapter. It should be declared once at adoption and updated when user surfaces change, not per-session. The failure packet and root-cause note should be owned by the task or session artifact layer — they are produced during work, not at adoption time. Runtime evidence should be owned by Developer Toolchain. Security escalation policy should be owned by the project adapter alongside the sensitive path declarations, so that the trigger and the list it evaluates against live in the same surface.

### Feedback — 2026-04-03 — GitHub Copilot (GPT-5.4) — Round 2

- **Perspective:** Round 2 is now narrow enough that the main question is no longer "what ideas sound right," but "which surfaces create the least ambiguity under failure pressure."

- **Strong agreement:** The discussion is converging in the right direction. I agree that v1 should prefer a small set of strongly connected surfaces over a wide set of optional documents. I also agree that progressive failure capture and automatic security escalation belong in v1 behavior, not in a later clean-up wave.

- **Main concern:** The biggest remaining risk is ownership fragmentation. If the user-surface map lives in one place, runtime evidence in another, security escalation rules in a third, and root-cause truthfulness somewhere else, the framework will recreate the exact reconstruction gap it is trying to solve. The artifact count itself is not the problem; the problem is whether a future agent can answer "which surface is authoritative right now" without interpretation.

- **Recommendation for v1:**

  **Q1 — Foundation:** The foundational artifact should be the `user-surface-to-code-surface map`, but only if it is defined as a decision surface rather than an architecture catalog. Minimum viable fields should be: surface name, owner path, sensitive yes/no, fastest repro path, and primary evidence source. That is enough to route triage, determine whether escalation applies, and anchor later failure capture.

  **Q2 — Progressive packets:** Yes, progressive packets should be first-class. My preferred minimum first-save is three fields rather than two: symptom, impacted surface, and first observed evidence. The extra evidence field matters because it prevents the packet from becoming an abstract complaint disconnected from any real signal. Promotion from lightweight to full should occur automatically when the issue touches a sensitive surface, survives one attempted fix, or becomes shared knowledge beyond a single executor.

  **Q3 — Runtime evidence ownership:** The single source of truth should remain the `Developer Toolchain` surface for normal repositories, with promotion to a dedicated runtime-evidence doc only when one section can no longer stay readable. I would define the threshold functionally rather than numerically: promote when evidence sources differ enough by service or workflow that one table can no longer tell an agent where to look first without branching prose.

  **Q4 — Security escalation trigger:** Automatic triggers should include both sensitive-surface match and sensitive-path/config match, with human classification as an override or manual upgrade path. After escalation, the minimum extra evidence should be: impacted trust boundary, relevant config or secret surface, containment or rollback note, and at least one misuse or negative-path validation claim. Without the negative-path requirement, the framework risks treating security-sensitive fixes as ordinary correctness patches.

  **Q5 — Default vs optional:** In v1, the default template set should include a user-surface map and a progressive failure packet. Runtime evidence should ship by default as part of `Developer Toolchain`, not as a separate required template. The `root_cause_note.template.md` is useful, but I would ship it as a default closeout artifact only when a failure packet exists or when the repository is closing a user-visible incident. Requiring a root-cause note for every low-severity defect risks turning it into formality instead of truth surface.

- **What should be deferred:** I would defer two things. First, trace and metric requirements should remain enrichment, not baseline. Second, broad repository-wide completeness should be deferred; v1 only needs top critical surfaces covered, not a fully mapped product universe. Forcing exhaustive coverage too early will encourage fiction and stale maps.

- **Proposed ownership:** The project adapter should own the user-surface map, sensitive-surface declarations, and the security escalation rule because those are repository truths. `Developer Toolchain` should own runtime evidence and repro-entry guidance because those are execution truths. Failure packets and root-cause notes should live in task or incident artifacts because they are event truths. That split keeps long-lived discovery separate from case-specific diagnosis while preserving a clear authority chain.

---

## Round 2 Summary

The second round produced enough convergence to stop broad discussion and move into a v1 design draft.

The strongest points of convergence are:

1. `User Surface Map` should be the foundational v1 artifact
2. `Failure Packet` should be progressive rather than all-or-nothing
3. runtime evidence should default to a `Developer Toolchain` sub-section rather than a separate required template
4. security-sensitive escalation should trigger automatically
5. v1 should prefer partial honest coverage of critical surfaces over fictional completeness

There are still implementation details that can be refined later, but they no longer justify another open-ended discussion round before drafting.

The next step is therefore:

1. freeze a v1 mechanism draft
2. prototype the minimum template surfaces
3. test those surfaces against real workflow examples

That draft now exists in:

`docs/TRACEABILITY_AND_RECOVERY_V1_DRAFT.md`
