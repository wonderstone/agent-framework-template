# Strict Adoption And Verification

Use this document when an adopting repository wants to absorb the framework's execution-control stack honestly rather than copy a subset and later attribute the missing behavior to the template itself.

The core rule is simple:

1. do not claim full framework adoption if the target repository only copied prompt text without the checkpoint, sync, receipt, and verification mechanisms that make the rules enforceable
2. do not let the main-thread agent self-certify adoption quality without independent local CLI review when the repository expects strong process guarantees
3. if a mechanism cannot be adopted yet, record it explicitly as a gap or future upgrade path instead of silently downgrading the framework claim

## Enforcement Maturity Matrix

This matrix classifies the current template surfaces by how close they are to hard mechanical enforcement.

| Layer | Surface | Current state | Main evidence | Adoption expectation |
|---|---|---|---|---|
| A. Pipeline + tooling enforced | Dispatch runtime and checkpoint stack | Strong | `.github/copilot-instructions.md` Rules 15, 18, 20, 21; `scripts/state_sync_audit.py`; `.githooks/pre-commit`; `.githooks/pre-push` | Keep when the repository runs multi-step work, fan-out, or checkpointed execution |
| A. Pipeline + tooling enforced | Closeout truth and receipt anchoring | Very strong | Rule 25; `scripts/closeout_truth_audit.py`; `tests/test_closeout_truth_audit.py` | Keep whenever the repository writes closeout claims into truth surfaces |
| A. Pipeline + tooling enforced | State-sync and drift detection | Very strong | `scripts/state_sync_audit.py`; `tests/test_state_sync_audit.py`; hooks | Keep whenever the repository uses task packets, progress receipts, or roadmap/session truth surfaces |
| A. Pipeline + tooling enforced | Resumable git audit artifact flow | Strong | `docs/runbooks/resumable-git-audit-pipeline.md`; `scripts/git_audit_pipeline.py` | Keep whenever work may cross executors, sessions, or reviewer swaps |
| A. Pipeline + tooling enforced | Runtime surface protection | Medium-strong | `docs/RUNTIME_SURFACE_PROTECTION.md`; `scripts/runtime_surface_guardrails.py` | Keep when the repository has live user-facing runtime paths |
| B. Pipelineized but policy-guided | Planning and path selection | Medium | Rules 15 and 16 | Keep the rule layer even though plan quality still depends on executor judgment |
| B. Pipelineized but policy-guided | Decomposition and dispatch choice | Medium | Rule 15 | Keep whenever the repository expects bounded fan-out instead of ad hoc parallelism |
| B. Pipelineized but policy-guided | Reality check and goal alignment | Medium | Rule 17 | Keep whenever the repository cares about intent-to-execution alignment rather than only syntax-clean diffs |
| B. Pipelineized but policy-guided | User acceptance gate | Medium-strong | Rule 22 | Keep whenever completion claims must be tied to user-visible behavior |
| B. Pipelineized but policy-guided | Independent evaluation | Medium | Rule 26 | Keep whenever the repository wants stronger closeout integrity than self-review alone |
| C. Missing final mechanical closure | Cognitive reasoning and self-check quality | Weak-medium | Rules 11 and 12 | Keep as governance, but do not overclaim this as tool-enforced behavior |
| C. Missing final mechanical closure | Progress-line and next-actions output discipline | Medium | Rules 8 and 14 | Keep as policy unless the target repo adds a response-shape auditor |
| C. Missing final mechanical closure | Scope-entry classification and leftover discipline | Medium | Rule 24; `docs/LEFTOVER_UNIT_CONTRACT.md` | Keep as policy unless the target repo adds a leftover detection auditor |
| C. Missing final mechanical closure | Discussion quality itself | Medium | `docs/runbooks/multi-model-discussion-loop.md`; `scripts/discussion_pipeline.py` | Keep the packet workflow, but do not confuse durable discussion with guaranteed good judgment |
| C. Missing final mechanical closure | Full behavior-level validator coverage | Medium | `scripts/validate_template.py` | Treat the validator as structure and consistency enforcement, not a total execution verifier |

## Strict Adoption Baseline

If a project wants to say that it adopted this framework's strict operating model, it should keep the full Layer A baseline unless a repository-specific constraint makes one item honestly inapplicable.

| Mechanism | Why it is baseline | Minimum carried surface |
|---|---|---|
| Truthful project adapter | The rest of the framework depends on real repo-specific commands and protected paths | `.github/instructions/project-context.instructions.md` |
| Execution contract | Long-running work should not run on implicit assumptions | `templates/execution_contract.template.md` or repo-local equivalent |
| Checkpoint and state-sync stack | Prevents execution state from drifting back into chat-only memory | `templates/execution_progress_receipt.template.md`, `templates/drift_reconciliation_packet.template.md`, `scripts/state_sync_pipeline.py`, `scripts/state_sync_audit.py` |
| Receipt-anchored closeout | Prevents paper-complete truth surfaces | `scripts/closeout_truth_audit.py` plus the Rule 25 closeout boundary |
| User acceptance and toolchain honesty | Prevents `tests passed` from replacing user-visible validation | Rule 22 and Rule 23 surfaces in `.github/copilot-instructions.md` and the project adapter |
| Independent evaluation path | Prevents the implementing agent from acting as sole acceptance authority | Rule 26 plus a real evaluator path |
| Resumable packet and handoff flow | Prevents multi-executor work from depending on chat memory | `docs/runbooks/resumable-git-audit-pipeline.md`, `scripts/git_audit_pipeline.py` |
| Discussion packet workflow | Prevents major design decisions from living only in ephemeral chat | `docs/runbooks/multi-model-discussion-loop.md`, `templates/discussion_packet.template.md`, `scripts/discussion_pipeline.py` |

If one of these is skipped, the adopter should say one of the following explicitly:

| Honest status | Meaning |
|---|---|
| `fully adopted` | All applicable Layer A mechanisms are present and verified locally |
| `partially adopted` | Some Layer A or Layer B surfaces were intentionally skipped or downgraded |
| `design-only upgrade path kept` | The repository kept future upgrade docs or templates but did not wire the mechanism into current execution |

## Strict Adoption Prompt

Use the prompt below when you want another agent to absorb the framework into a target repository without silently weakening the mechanism stack.

```text
You are working in my application repository at <TARGET_REPO_PATH>.

Template source of truth:
https://github.com/wonderstone/agent-framework-template

Adopt the framework in strict mode. Do not treat the template as a bag of optional prompt text.

Required outcome:
- absorb the framework's real execution-control mechanisms, not only the wording of `.github/copilot-instructions.md`
- keep the repository honest about which surfaces are mechanically enforced, policy-guided, or still design-only
- do not later attribute missing behavior to the template when the target repo skipped the mechanism that made that behavior real

Strict baseline:
- keep the truthful project adapter
- keep the execution contract for long-running work
- keep the checkpoint, receipt, drift-reconciliation, and state-sync surfaces for multi-step execution
- keep receipt-anchored closeout enforcement
- keep the user-acceptance and validation-toolchain surfaces honest
- keep an independent evaluation path for non-trivial or user-facing work
- keep the resumable packet and handoff flow when multi-executor work is possible
- keep the discussion-packet workflow when design ambiguity exists

Allowed downgrade rule:
- only downgrade a baseline mechanism when it is honestly inapplicable to the target repository
- if you downgrade one, record it explicitly as `partially adopted` or `design-only upgrade path kept`
- do not claim `fully adopted` unless all applicable baseline mechanisms are present and verified

Execution requirements:
1. Read the real template files before changing the target repo.
2. Inspect the target repo and map each strict baseline mechanism to a concrete file, script, runbook, or local equivalent.
3. Bootstrap or copy files as needed, but preserve the framework paths unless a repo-specific reason requires a different location.
4. Fill the generated project adapter with real commands, protected paths, truth surfaces, and user-surface evidence sources.
5. Do not invent fake runtime paths, fake E2E coverage, fake enforcement, or fake independent evaluation.
6. If the repo is not yet ready for one baseline mechanism, leave an explicit upgrade path and report the gap.

Required local verification flow:
1. Run the target repo's mechanical validation commands from its own root.
2. If the repo keeps the discussion workflow, create a verification packet for this adoption decision.
3. Use the same verification prompt against all locally available CLI executors, such as Claude, Codex, Gemini, and Copilot.
4. Each CLI review must be read-only and must answer whether the repo truly kept the strict baseline mechanisms, whether any mechanism was silently downgraded, and whether any adoption claim overstates enforcement.
5. Record or append all review outputs into one durable packet or adjacent review artifacts.
6. Resolve critical or major gaps exposed by the CLI reviews.
7. Re-run the target repo's mechanical validation after fixes.
8. Do not declare adoption complete until both conditions hold:
   - mechanical validation is clean
   - independent local CLI review no longer reports unresolved critical gaps in the strict baseline

Report at the end:
- whether the repo is `fully adopted`, `partially adopted`, or `design-only upgrade path kept`
- which strict baseline mechanisms were kept, downgraded, or skipped
- which local CLI executors were used for independent verification
- what validation commands ran and whether they passed
- which surfaces remain policy-guided rather than mechanically enforced
```

## Local CLI Verification Flow

Use this workflow when the target repository wants stronger proof than a single main-thread agent judgment.

| Step | Action | Expected artifact |
|---|---|---|
| 1 | Freeze the adoption scope and baseline mechanisms to be verified | verification prompt or discussion packet |
| 2 | Run the repository's mechanical validators locally | validator output, test output, audit output |
| 3 | Dispatch the same verification question to all locally available CLI executors | one output per CLI executor |
| 4 | Require each CLI to stay read-only and to classify missing or downgraded mechanisms explicitly | appended feedback or saved review note |
| 5 | Synthesize the CLI findings and fix any critical or major gaps | synthesis note plus follow-up edits |
| 6 | Re-run the local validators after remediation | final validator output |
| 7 | Declare the adoption status honestly: `fully adopted`, `partially adopted`, or `design-only upgrade path kept` | final report or closeout summary |

Recommended review questions for each CLI executor:

1. Did the target repository keep every applicable Layer A mechanism?
2. Did the target repository overclaim any Layer B or Layer C surface as if it were tool-enforced?
3. Is the project adapter truthful about diagnostics, build, run, health, repro, and user-surface evidence?
4. Can the repository honestly say that the framework was absorbed, or is it only carrying a partial imitation?

## What Not To Claim

Do not claim any of the following unless the target repository has actually wired the corresponding mechanism:

| Overclaim | Why it is invalid without the mechanism |
|---|---|
| `the framework guarantees checkpoint integrity` | invalid without receipts, drift reconciliation, and sync audit |
| `the framework guarantees truthful closeout` | invalid without receipt-anchored closeout enforcement |
| `the framework guarantees acceptance integrity` | invalid without real UAC plus independent evaluation |
| `the framework guarantees discussion-backed design decisions` | invalid without a durable discussion packet workflow |
| `the framework guarantees resumable multi-executor work` | invalid without packet, receipt, and handoff artifacts |

## Adoption Decision Rule

When a downstream repository asks whether it has really absorbed the framework, use this sequence:

1. check whether the Layer A baseline is present and locally verified
2. check whether any downgraded mechanism was reported explicitly rather than silently skipped
3. check whether the repo's own local CLI reviewers agree that the adoption claim is honest
4. only then say the framework was absorbed in strict mode

If these checks fail, the right answer is not that the template underperformed. The right answer is that the repository only performed a partial adoption and should report that boundary honestly.