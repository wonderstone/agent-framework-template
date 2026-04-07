## Plan ready for your review

**Verdict: freeze-plan**

Based on deep codebase exploration, the enforcement gaps are mechanically identifiable and Direction E (asymmetric combination) is the right call. Here is the full response to the discussion packet:

---

### Top 3 Findings

**1. Missing mid-task enforcement point**
- Category: Mid-task state sync gap
- Why it matters: `closeout_truth_audit.py` only fires on "completed" keywords at commit time. An agent can drift through many subtasks before triggering any check. The existing `_validate_root_session_state_freshness` only catches "no active work" vs unchecked UAC — not active-work drift where Current Step diverged from files actually touched.
- Smallest honest next step: `_validate_active_session_state_coherence()` in `validate_template.py` — compare `session_state.md` last-modified commit vs most recent non-state-file commit. Advisory for adopted repos; hard-fail at framework root.

**2. Missing event-to-surface contract**
- Category: Unenforceable free-text binding
- Why it matters: Execution contract Section 7 has `Update session_state.md when: [...]` as free-text placeholders. No validator enforces them. Agents treat it as optional prose and skip it during long runs.
- Smallest honest next step: New `templates/state_sync_contract.template.md` with a structured table (event | surface | required field | enforcement level). Validator checks presence of reference — advisory for adopted repos.

**3. Missing repair path**
- Category: No structured drift recovery surface
- Why it matters: When drift is detected, agents have no templated surface to document gap → reconcile → resume without silently overwriting evidence. `docs/TRACEABILITY_AND_RECOVERY_V1_DRAFT.md` names this conceptually but ships no operational artifact.
- Smallest honest next step: `templates/state_drift_repair_packet.template.md` + `reconcile-drift` subcommand in `git_audit_pipeline.py`, parallel to `record-receipt`.

---

### Anti-Drift Mechanism Table

| Mechanism | Template Surface(s) | Enforcement Level | Why This Level Is Honest |
|---|---|---|---|
| Active-work coherence check (commit timestamp comparison) | `validate_template.py` — new `_validate_active_session_state_coherence()` | Advisory (adopted); Hard-fail (root) | File-to-state correlation is inferential |
| ROADMAP all-✅ + Active Work non-none contradiction | `validate_template.py` — new `_validate_roadmap_session_state_alignment()` | Hard-fail (root); Advisory (adopted) | Unambiguous structural contradiction at root |
| State sync event contract (structured table template) | New `templates/state_sync_contract.template.md`; extend execution contract Section 7 | Advisory (presence check) | Events are project-local |
| Drift repair packet + `reconcile-drift` CLI | New template + extend `git_audit_pipeline.py` | Repair pipeline only | Blocking recovery when state is already wrong is self-defeating |
| Checkpoint rule field in task packets | Extend `git_audit_task_packet.template.md`; new `audit_checkpoint_rule()` in `closeout_truth_audit.py` | Advisory | Hard-fail would break simple tasks |
| Receipt lineage check | `validate_template.py` — new `_validate_session_state_receipt_lineage()` | Advisory (default); Hard-fail (manifest opt-in) | Requires bootstrap guarantees |
| State-sync events runbook | New `docs/runbooks/state-sync-events.md` | Instruction layer only | Sequencing judgment can't be fully mechanized |
| Manifest opt-in: `state_sync_policy: strict` | `bootstrap_adoption.py` + `validate_repo()` adopted-repo path | Advisory → Hard-fail on opt-in | Let adopters graduate after one phase cycle |

---

### 5-Step Rollout

1. Ship `templates/state_sync_contract.template.md` + extend execution contract + validator schema check
2. Add `_validate_active_session_state_coherence()` and `_validate_roadmap_session_state_alignment()` to `validate_template.py`
3. Extend `git_audit_pipeline.py` with `reconcile-drift` + checkpoint rule; extend `closeout_truth_audit.py`
4. Ship `docs/runbooks/state-sync-events.md` + wire into all discovery surfaces
5. Manifest opt-in keys in `bootstrap_adoption.py` + `ADOPTION_GUIDE.md` section

**New files**: `templates/state_sync_contract.template.md`, `templates/state_drift_repair_packet.template.md`, `docs/runbooks/state-sync-events.md`

---

### One Thing to Avoid

Do not hard-fail on `session_state.md` content drift during active work in adopted repos by default. A hard-fail blocks the agent from committing the state correction — the enforcement loop becomes self-defeating. Advisory + repair-first is correct; hard-fail belongs only at structural contradiction boundaries.

---

**Final recommendation**: Implement five steps in order, keeping all adopted-repo enforcement advisory until a repo completes one full phase cycle with the new surfaces present.
artifacts. Add a required sub-field `session_state_touched: true/false` to the handoff packet template. Validator checks presence of this field in shipped examples — it cannot verify runtime truth but enforces that the scaffold acknowledges the obligation. |
| staleness counter in pre-push audit | scripts/staleness_audit.py + .githooks/pre-push | advisory → hard-fail-on-flag | Default advisory. A per-repo env flag `DRIFT_AUDIT_STRICT=1` upgrades to hard-fail. This respects that different adopters have different commit granularity without shipping a one-size-fits-all block. |
| session_state.md format checkpoint (progress footer timestamp) | scripts/preference_drift_audit.py + session_state.md | advisory | preference_drift_audit.py already checks footer format. Extend it to warn if the footer has not changed in the last N commits. Cannot hard-fail on content, only on format absence — anything stricter would require understanding semantic intent. |

---

## Ordered Rollout Plan

**Step 1 — Add `state_sync_schedule` field to execution_contract.template.md and wire validate_template.py**
This is the cheapest prevention surface. It costs one template field, one validator check, and creates the declared baseline all other mechanisms reference. Ship this first so the absence of a sync schedule becomes a structural violation. Add it to bootstrap_adoption.py so new adopters get it automatically.

**Step 2 — Add `session_state_touched` field to git_audit_handoff_packet.template.md and validate in the pipeline scaffold example**
The pipeline scaffold (05_staged_handoff_pipeline.md) is already a shipped, validator-checked surface. Add one boolean sub-field to the handoff packet. Update the example to show `session_state_touched: true`. The validator already checks that the handoff packet references are correct — extend it to check for this field's presence. This is a hard-fail structural check with low blast radius.

**Step 3 — Ship scripts/staleness_audit.py and wire into .githooks/pre-push as advisory**
This is the first mid-execution detection mechanism. It runs at push time (not per-commit, which would be too noisy), counts the drift window, and reports which commits created divergence. Default advisory. Document the `DRIFT_AUDIT_STRICT=1` flag in the adoption guide. Add staleness_audit.py to the required-files list in validate_template.py so it ships with the template and every adopter gets it in bootstrap.

**Step 4 — Ship templates/drift_repair_packet.template.md and a runbook entry**
Add the repair artifact so there is a structured path when drift is detected. Add a corresponding `docs/runbooks/drift-repair-workflow.md` with: when to open the packet, what evidence to include, how to close it, and how the resulting packet ID becomes a valid anchor for closeout_truth_audit.py. Extend closeout_truth_audit.py to recognize `drift_repair_packet_id:` as a valid evidence anchor alongside `request_id`, `turn_id`, etc.

**Step 5 — Extend preference_drift_audit.py to warn on stale progress footer**
preference_drift_audit.py already runs, already checks the `📍 当前聚焦:` footer format. Extend it to extract the last recorded footer state and compare it against the most recent commit that touched source files. If source files changed but the footer is identical to what it was K commits ago, emit a warning. This is advisory, requires no new files, and adds one check to an existing script.

---

## One Thing the Template Must Explicitly Avoid

**Do not add a per-commit hard-fail that requires session_state.md to be updated with every commit.**

This sounds maximally strict but does not work honestly. Agents make small commits (fix a typo, add a test, bump a version) where updating session_state.md would produce noise, not signal. A per-commit hard gate would either train agents to write meaningless session_state.md updates to pass the gate (defeating the purpose) or force adopters to disable the hook entirely (losing all enforcement). The right granularity is stage boundaries and push events, not individual commits. The template must say this explicitly in the staleness_audit.py header and the adoption guide, so adopters do not accidentally tighten the threshold to per-commit and sabotage their own enforcement.

---

## Final Recommendation

Ship the five-step rollout as a single Phase 5 with staleness_audit.py in the scripts layer, `state_sync_schedule` in the execution contract, `session_state_touched` in the handoff packet, and drift_repair_packet.template.md as the repair artifact — this combination covers prevention (declared schedule), detection (push-time audit), and repair (structured packet) without pretending the template has orchestration power it does not have.
