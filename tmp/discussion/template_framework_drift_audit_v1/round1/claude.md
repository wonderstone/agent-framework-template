## Audit: Template Framework Drift Assessment

### Verdict

**Material drift risk exists — but it's a framing problem, not an architectural one.** The framework's design surfaces are mostly sound and the examples (demo project, full-stack reference) are genuinely complete. Three concrete gaps exist where the docs make claims that are stale, unqualified, or aspirationally framed as enforcement guarantees.

---

### Top 3 Findings

#### 1. Current Bug — `session_state.md` violates the framework's own state-truth discipline
**Category:** Current bug

Commit `8e700b3` (harvest-loop contract, Apr 5) happened after the last `session_state.md` update. The file still says "No active work / Next: Independent review, then git closeout." The harvest-loop design freeze is simply not recorded.

**Why it matters:** This is the clearest signal that state-truth discipline is hard to maintain in practice. If the template repo itself violates Rule 7, adopters using it as a behavioral example will replicate the lapse — and the framework's credibility on "resumable, truthful state" collapses immediately on inspection.

**Smallest honest fix:** Update `session_state.md` to record harvest-loop v1 as completed, clear the stale SKILL follow-up goal, and set an accurate next step. 5-line edit.

---

#### 2. Doc Overclaim — Validator enforcement is qualified but documented as universal
**Category:** Doc overclaim

`session_state.md` line 52: *"The validator now hard-fails missing review-matrix rows, invalid matrix thresholds in real skills, and nonexistent reference paths."* True — but only for **manifest-based adopters**. Non-manifest adopters get advisory warnings that CI passes through (`validate_template.py` `collect_advisories()`, lines 1030+). This two-tier model (manifest opt-in = strict; no manifest = advisory) is architecturally intentional but is completely undocumented at the adopter-facing layer.

**Why it matters:** An adopter bootstrapping without a manifest will believe their Developer Toolchain contract is enforced when it is only structurally checked. False CI confidence is the drift risk.

**Smallest honest fix:** One sentence in README: *"Developer Toolchain field validation is hard-enforced for manifest-based adopters; for all others, violations are advisory and do not block CI."* No code change.

---

#### 3. Governance Gap — Rules 0–27 are presented as behavioral guarantees; only Rule 25 is actually hooked
**Category:** Governance gap (acceptable known limit, framing problem)

`README.md` line 265: *"When a required pre-condition is not met, the agent states why it is blocked and waits — it does not guess, skip, or proceed with Low confidence."*

Reality: Only Rule 25 (Receipt-Anchored Closeout) is enforced via `scripts/closeout_truth_audit.py` hooked to pre-commit. Rules 1, 7, 11, 12, 13, 23 are documented behavioral expectations. No pre-edit hook validates the Rule 12 self-check gate. No hook blocks edits to protected paths (Rule 1).

**Why it matters:** Adopters who read the README language as enforcement will not implement their own team discipline around the self-check gate and state tracking — because they think the framework already enforces it.

**Smallest honest fix:** One callout in README: *"Rule 25 is enforced by a pre-commit hook. Rules 0–24 and 26–27 are behavioral conventions enforced by team discipline, not automated hooks."*

---

### One Thing the Packet Is Over-Worried About

**The execution contract being "too abstract" for adopters.**

`templates/execution_contract.template.md` is actually quite operationally specific — it defines git policy (force-push/rebase require explicit confirmation), dispatch rules, long-task autonomous mode, scope boundaries, and escalation. The real gap is not vagueness but *presence enforcement*: the validator doesn't check whether a project carries an execution contract at all. The packet diagnoses this as a specificity problem; it is a presence-enforcement problem. Different fix required.

---

### Final Recommendation

**Patch now** for Finding 1 (`session_state.md` — trivial, makes the framework honest about its own state).

**Document only** for Findings 2 and 3 — both are framing/qualification issues. Two honest sentences in README eliminate the overclaims without softening the design intent or requiring redesign.

The advisory-broad + hard-enforced-for-opt-in + one universal hook model is reasonable for a bootstrap template. The only unreasonable thing is presenting it as more uniform than it is.
