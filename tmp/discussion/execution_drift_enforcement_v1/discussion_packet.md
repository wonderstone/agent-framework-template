# Discussion Packet — execution_drift_enforcement_v1

- Generated at: 2026-04-08T00:00:00+00:00
- Owner: main-thread
- Current round goal: Obtain an implementation-ready anti-drift plan
- Round exit rule: Freeze a concrete plan, narrow to a sharper second round, or stop on missing truth

## Decision Question

How should the template harden its execution layer so adopted-project agents stop drifting away from `session_state.md`, `ROADMAP.md`, and other plan or progress truth surfaces during long-running implementation?

## Why This Needs Discussion

Adopted repositories are reporting a repeated failure mode: the planning and governance layer is strong on paper, but execution often drifts. Agents start from a good `session_state.md`, `ROADMAP.md`, or execution contract, then proceed for a while and stop updating those truth surfaces. The result is a stale plan, false progress visibility, and recovery surfaces that no longer describe the real project state.

This is not a wording problem. It is an execution-control problem. The user wants implementable mechanisms: more tools, stronger validators, better repair loops, and pipeline constraints that can materially reduce or eliminate this drift rather than merely reminding agents to behave better.

## Current Truth

The template already ships strong planning and governance surfaces:

1. `session_state.md`
2. `ROADMAP.md`
3. execution contracts and doc-first execution guidance
4. receipt-anchored closeout and git-audit artifacts
5. Developer Toolchain and validation surfaces
6. discussion-loop and resumable handoff workflows

But the current weakness is execution-time freshness and synchronization. The template mostly relies on instruction-following plus lightweight validator checks. It does not yet have a strong always-on enforcement path that says:

1. which state surfaces must change after which execution events
2. how those updates are detected mechanically
3. what repair path runs when drift is detected mid-task rather than at closeout only
4. how long-running tasks keep state surfaces honest without depending on agent memory alone

## Constraints

Be concrete, critical, and implementation-minded. Do not answer with “train the agent better” or “write clearer rules” alone. Prefer mechanisms that can actually ship in this template repo: helper scripts, validator rules, task-packet requirements, receipt-driven state updates, execution pipeline hooks, state reconciliation tools, and bounded stop rules. Distinguish between what can hard-fail, what should stay advisory, and what needs a repair workflow instead of a prohibition.

Do not assume we can fully eliminate all drift with one validator pass at closeout. The better answer may combine:

1. stronger runtime instrumentation or receipts
2. mid-task synchronization checkpoints
3. diff-aware or state-aware auditing tools
4. explicit leftover-unit or repair pipelines
5. narrower scope declarations that reduce opportunities for state divergence

The answer must be useful to repositories that adopt this template, not only to this template repo itself.

## Candidate Directions

Direction A: Add a state-sync auditor that compares `session_state.md`, `ROADMAP.md`, receipts, and changed files, then fails when truth surfaces are stale or contradictory.

Direction B: Add an execution-progress pipeline where every subtask or batch emits a receipt that must be reflected into state surfaces before the next stage can proceed.

Direction C: Add a repair-first workflow for drift: detect stale state, open a drift packet, reconcile the truth surfaces, and only then allow closeout or next-stage execution.

Direction D: Add more tool support inside the template for state mutation itself, such as scripts that update `session_state.md` / `ROADMAP.md` from a structured event model rather than relying on free-form prose edits.

Direction E: Combine A, B, C, and D asymmetrically: some pieces hard-fail, some stay advisory, and some become explicit repair loops.

## Evaluation Criteria

Judge proposals against these questions:

1. Does the plan reduce execution-time drift rather than only improving post-hoc reporting?
2. Can the plan ship as concrete template surfaces: scripts, validators, templates, examples, or runbooks?
3. Does the plan preserve honest governance boundaries instead of pretending the template has full orchestration power it does not have?
4. Can adopters actually use it across different repository types?
5. Does it define what hard-fails, what stays advisory, and what enters a repair pipeline?
6. Does it improve recovery when drift still happens rather than assuming perfect prevention?

## Requested Output Shape

Do not just recommend a direction. Return an implementation-shaped answer with:

1. a top-line verdict
2. the smallest set of new template surfaces to add
3. which pieces should be hard-fail validator rules
4. which pieces should be advisory only
5. which pieces should become repair workflows or pipelines
6. an ordered rollout plan for this repository
7. at least one thing we should explicitly avoid because it sounds strict but would not work honestly

## Suggested Executors

Claude CLI; Codex CLI; Gemini CLI; GitHub Copilot CLI; main-thread synthesis

## Instructions For Participating Executors

1. Read the packet before commenting.
2. Do not rewrite the packet body unless the main thread asks for it.
3. Append your feedback at the end of this file.
4. Prefer tradeoffs, missing enforcement paths, and implementation surfaces over policy slogans.
5. If another round is needed, propose the narrowest next question.

## Main-Thread Decision Status

- Current status: closed
- Final decision: freeze-plan

## Append-Only Discussion Log

<!-- Append feedback and synthesis entries below this line. -->

### Claude CLI — 2026-04-08

1. Verdict

`freeze-plan`

2. Top findings

- Detection gap: the template lacks a staleness signal between commits, so state drift can accumulate silently for many commits before closeout.
- Prevention gap: execution contracts do not currently declare a state-sync schedule, so there is no explicit contract violation to detect mid-task.
- Repair gap: drift has no structured repair artifact today, so reconciliation falls back to free-form prose edits.

3. Proposed surfaces

- `scripts/staleness_audit.py` wired to pre-push, advisory-first with optional strict mode.
- `state_sync_schedule` field added to `templates/execution_contract.template.md` as a hard-fail structural requirement.
- `templates/drift_repair_packet.template.md` plus a dedicated runbook and closeout-audit integration.

4. Main warning

- Do not hard-fail on every commit if `session_state.md` was not edited; that would create noise and train meaningless state churn.

### Codex CLI — 2026-04-08

1. Verdict

`freeze-plan`

2. Top findings

- The template lacks a mechanical execution unit and checkpoint contract, so drift is inevitable on long tasks.
- Current enforcement is mostly closeout-time and misses mid-task divergence.
- Drift needs a standard repair loop, not just a validator failure.

3. Proposed surfaces

- Add `progress_unit`, `checkpoint_rule`, `truth_surfaces`, and `closeout_boundary` to execution contracts and task packets.
- Ship `scripts/state_sync_audit.py` plus `templates/drift_packet.template.md` and a state-reconciliation runbook.
- Keep roadmap sync hard-fail only for explicit milestone or completion claims, not every code diff.

4. Main warning

- Do not pretend the template can continuously orchestrate agent behavior or infer “fresh enough” state from diffs alone.

### Gemini CLI — 2026-04-08

1. Verdict

`freeze-plan`

2. Top findings

- Detection and enforcement are too loosely coupled; if drift is only checked late, the repair cost becomes high.
- Hard-fail enforcement needs a paired repair path or teams will bypass it.
- The template must stay honest about its boundary: hooks, scripts, and CI are real; continuous orchestration is not.

3. Proposed surfaces

- `scripts/state_sync_audit.py` in hooks and CI.
- `docs/runbooks/drift-repair.md` plus `templates/drift_reconciliation_packet.template.md`.
- Optional state-mutation helper such as `scripts/update_session_state.py`.

4. Main warning

- Do not assume a continuously monitoring runtime daemon; all enforcement should stay discrete and stateless.

### GitHub Copilot CLI — 2026-04-08

1. Verdict

`freeze-plan`

2. Top findings

- Prevention is missing a low-friction event path from execution into state surfaces.
- Detection should compare receipts, handoffs, leftovers, and truth surfaces for contradictions rather than guessing one perfect fix.
- Repair should use a mandatory drift packet and reconcile command before closeout or next-stage dispatch.

3. Proposed surfaces

- Structured progress receipt schema with fields like `task_id`, `receipt_seq`, `progress_unit`, `touched_files`, `status`, and `expected_state_effect`.
- A state-mutation helper with `record-progress`, `record-blocker`, `record-complete`, and `record-leftover` subcommands.
- `scripts/state_sync_audit.py` plus drift packet workflow and closeout/dispatch gates.

4. Main warning

- Do not auto-overwrite the “correct” `session_state.md` or `ROADMAP.md` narrative from diffs; reconciliation must stay explicit.

### Main-Thread Synthesis — Round 1

- Timestamp: 2026-04-08T00:00:00+00:00
- Decision: freeze-plan
- Confidence: High
- Next action: turn the consensus into a concrete anti-drift implementation plan with phased surfaces for prevention, detection, and repair.

#### Summary

All four usable outputs converged on the same underlying answer: drift cannot be rooted out by stronger prose rules alone. The template needs an execution-event model plus explicit anti-drift tooling. The honest solution is asymmetric, not monolithic:

1. prevention through declared checkpoint contracts and optional structured progress receipts
2. detection through contradiction-focused sync auditing at observable boundaries such as handoff, closeout, push, or CI
3. repair through a mandatory drift packet or reconciliation workflow when contradiction is detected

No executor argued for “just prompt the agent better.” No executor supported pretending the template can continuously orchestrate runtime behavior. The consensus was that enforcement should land in scripts, hooks, validators, and packet workflows the template can actually ship.

#### Frozen Plan Shape

The converged implementation shape is:

1. extend `templates/execution_contract.template.md` with checkpoint and state-sync fields such as `progress_unit`, `checkpoint_rule`, `truth_surfaces`, and `state_sync_schedule`
2. add a structured progress-receipt path plus optional state-mutation helper so state updates have a low-friction, receipt-bearing input surface
3. ship `scripts/state_sync_audit.py` that checks contradiction classes, not vague freshness feelings
4. add a repair artifact and runbook such as `templates/drift_packet.template.md` or `templates/drift_reconciliation_packet.template.md` plus a `docs/runbooks/state-reconciliation.md`
5. hard-fail only at observable boundaries the template can honestly police: dispatch, handoff, closeout, push, and explicit roadmap/session-state claims

#### What Should Be Hard-Fail vs Advisory vs Repair

- Hard-fail:
	- missing checkpoint or state-sync fields in execution contracts or task packets
	- explicit contradiction classes from `state_sync_audit.py`
	- milestone or completion claims in `ROADMAP.md` without matching evidence and state reflection
	- unresolved drift at closeout or next-stage dispatch boundaries
- Advisory:
	- helper commands for updating state surfaces
	- staleness thresholds that are useful but repository-dependent
	- roadmap nudges outside explicit milestone or completion transitions
- Repair-loop:
	- any detected drift where the auditor can prove contradiction but cannot know which truth surface should win

#### Main Risk To Avoid

Do not over-tighten the template into per-commit mandatory `session_state.md` edits or automatic narrative rewriting from diffs. That would create noisy fake updates and encourage bypassing the system instead of making state more truthful.