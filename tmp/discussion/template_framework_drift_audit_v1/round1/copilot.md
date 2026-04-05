I’ve got the packet and I’m pulling the repo surfaces that actually define the adopter contract now. Next I’m checking where the framework claims enforcement versus where it only gestures at it.

I’ve already found one hard truth bug the packet called out: the root `session_state.md` is stale by its own standard. Now I’m checking whether the higher-level claims are actually backed by shipped enforcement or just described as policy.

Baseline proof is decent: validator, tests, and active-doc audit all pass. That shifts this away from “mostly fictional framework” and toward “real framework with a few truth/governance blind spots.”

The execution-contract concern looks narrower than the packet suggests. The template itself is quite specific; the gap is that nothing proves or requires an adopter to actually instantiate it in live work.

The validator confirms the contract template exists and contains the right fields, but it never checks any live `session_state.md` truthfulness and it never proves an execution contract got instantiated in actual workflow. That’s the main expectation gap.

The repo does have concrete proof for the resumable git-audit story: templates, generator, docs, tests, and committed demo artifacts all line up. So that part looks stronger than the packet implies.

1. **Verdict:** The framework is **reasonable but currently has material drift risk**. It is not vaporware: bootstrap, validator, hooks, audit pipeline, demo repo, and CI all exist and pass. But the source repo already violates its own state-truth contract, and two key “operational” surfaces still rely too much on agent obedience rather than executable proof.

2. **Top 3 findings**
   1. **Stale root state is a real contract break**
      - **category:** current bug
      - **why it matters to adopters:** `session_state.md` is presented as a live truth source, but the root file still says the current goal is SKILL follow-up work and “Next Planned Step: Independent review, then git closeout” even though that wave is clearly no longer the active state. If the template repo itself cannot keep `session_state.md` truthful, adopters should distrust the contract.
      - **smallest honest fix now:** Update `session_state.md` immediately to the repository’s actual current state, or explicitly mark it idle/completed instead of leaving a finished wave as “current.”

   2. **Truthfulness governance does not catch the failure it claims to prevent**
      - **category:** governance gap
      - **why it matters to adopters:** The repo has executable guards, but they stop short of live state truth. `scripts/validate_template.py` checks the **template** shape of `session_state` and the execution contract, not the truthfulness of the live root `session_state.md`; `scripts/closeout_truth_audit.py` only looks for broad claim words plus any anchor-like line in the same diff. That means proof-vs-claim discipline is real for some staged closeout cases, but weak for the actual “state doc must stay true” promise.
      - **smallest honest fix now:** Add one repo-level audit that fails stale or contradictory root `session_state.md`, and tighten closeout auditing so the proof is tied to the same file/claim block rather than “any anchor anywhere in the diff.”

   3. **The execution contract is well-written but not yet operationally proven**
      - **category:** doc overclaim
      - **why it matters to adopters:** README, adoption docs, architecture, and agent instructions all frame the execution contract as the precondition for long-task autonomy and git closeout policy, but the repo does not show one completed execution-contract artifact in the demo path and does not enforce that it gets instantiated in real work. So adopters can easily mistake a strong template for an enforced workflow.
      - **smallest honest fix now:** Either ship one filled execution-contract example in `examples/demo_project/` and reference it from the walkthrough, or soften the wording from “should produce before any long-running task” to “recommended unless your host/repo enforces it.”

3. **One thing the packet is over-worried about:** The git closeout / resumable audit side is **not** too abstract anymore. That surface is comparatively strong: `scripts/git_audit_pipeline.py`, `scripts/closeout_truth_audit.py`, optional hooks, tests for both, the runbook, and committed demo packet/receipt/handoff artifacts all exist. The weakness is not lack of mechanism there; it is uneven enforcement of live truth and execution-contract instantiation.

4. **Final recommendation:** **patch now**. Not a redesign—just a targeted honesty pass: fix the stale root state, add one executable live-state truth check, and either prove or soften the execution-contract claim.

