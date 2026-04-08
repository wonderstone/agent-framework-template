I’m scanning the framework docs and validator scripts now, focusing only on execution-layer gaps that would matter to downstream agents. After that I’ll distill it to the highest-leverage additions, not a broad repo review.

● Read session_state.md
  └ 101 lines read

● Search (glob)
  │ "docs/runbooks/multi-model-discussion-loop.md"
  └ 1 file found

● Search (glob)
  │ "README.md"
  └ 3 files found

● Search (glob)
  │ "docs/{ADOPTION_GUIDE.md,STRICT_ADOPTION_AND_VERIFICATION.md,SKILL_EXECUTION_LAYER_V1_DRAFT.md,D
  │ EVELOPER_TOOLCHAIN_DESIGN.md}"
  └ 4 files found

● Search (glob)
  │ "scripts/{validate_template.py,state_sync_audit.py,skill_evolution_pipeline.py}"
  └ 3 files found

I found the target docs and validator scripts. Next I’m reading the execution-layer and adoption surfaces together so the proposals are grounded in what the template already promises versus what it actually enforces.

● Read STRICT_ADOPTION_AND_VERIFICATION.md
  │ docs/STRICT_ADOPTION_AND_VERIFICATION.md
  └ L1:260 (158 lines read)

● Read ADOPTION_GUIDE.md
  │ docs/ADOPTION_GUIDE.md
  └ L1:260 (260 lines read)

● Read SKILL_EXECUTION_LAYER_V1_DRAFT.md
  │ docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md
  └ L1:260 (259 lines read)

● Read README.md
  └ L1:220 (220 lines read)

● Read multi-model-discussion-loop.md
  │ docs/runbooks/multi-model-discussion-loop.md
  └ L1:260 (143 lines read)

● Read state_sync_audit.py
  │ scripts/state_sync_audit.py
  └ L1:260 (260 lines read)

● Read DEVELOPER_TOOLCHAIN_DESIGN.md
  │ docs/DEVELOPER_TOOLCHAIN_DESIGN.md
  └ L1:260 (260 lines read)

● Read skill_evolution_pipeline.py
  │ scripts/skill_evolution_pipeline.py
  └ L1:260 (205 lines read)

● Read validate_template.py
  │ scripts/validate_template.py
  └ L1:260 (260 lines read)

● Search (grep)
  │ "verify|validator|audit|toolchain|runtime|repro|health|smoke|debug|logs|fallback"
  │ (docs/DEVELOPER_TOOLCHAIN_DESIGN.md)
  └ 55 lines found

● Search (grep)
  │ "validator|hard-fail|advisory|execution layer|host|trigger|receipt|candidate|runtime"
  │ (docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md)
  └ 70 lines found

● Search (grep)
  │ "local CLI|verification|read-only|executor|command|vendor-specific|tool"
  │ (docs/runbooks/multi-model-discussion-loop.md)
  └ 13 lines found

● Search (grep)
  │ "Developer Toolchain|required-core|Runtime Evidence|User Surface Map|skill|invocation|candidate|
  │ promotion|debug|logs|repro|health|smoke|verified-working|advisory|hard-fail"
  │ (scripts/validate_template.py)
  └ 8 lines found

The docs are pretty explicit about what *should* exist; the remaining question is which of those promises are still only partially enforced. I’m narrowing that to concrete validator/runtime gaps so the recommendations are about shipped accountability, not just nicer docs.

● Search (grep)
  │ "required-core|Developer Toolchain|User Surface Map|Runtime
  │ Evidence|verified-working|declared-unverified|known-broken|fallback|stop rule|Debug|Logs|Repro"
  │ (scripts/validate_template.py)
  └ 40 lines found

● Search (grep)
  │ "argparse|subparsers|audit|diff|staged|worktree|issue|progress receipt|drift"
  │ (scripts/state_sync_audit.py)
  └ 59 lines found

● Search (grep)
  │ "argparse|subparsers|init-|append-|audit|validate|check" (scripts/skill_evolution_pipeline.py)
  └ 7 lines found

● Search (grep)
  │ "skill_invocation_receipt|skill_candidate_packet|skill_promotion_receipt|evolution_mode|candidat
  │ e_trigger|invocation_ids|promotion receipt|invocation receipt" (scripts/validate_template.py)
  └ 18 lines found

● Search (grep)
  │ "discussion_pipeline|multi-model-discussion|discussion packet|executor"
  │ (scripts/validate_template.py)
  └ 8 lines found

● Read validate_template.py
  │ scripts/validate_template.py
  └ L1490:1865 (376 lines read)

● Read validate_template.py
  │ scripts/validate_template.py
  └ L1160:1235 (76 lines read)

● Read validate_template.py
  │ scripts/validate_template.py
  └ L430:560 (131 lines read)

● Search (grep)
  │ "SKILL_EVOLUTION_PIPELINE_REQUIRED_SNIPPETS|SKILL_INVOCATION_TEMPLATE_REQUIRED_SNIPPETS|SKILL_CA
  │ NDIDATE_TEMPLATE_REQUIRED_SNIPPETS|SKILL_PROMOTION_TEMPLATE_REQUIRED_SNIPPETS|DEVELOPER_TOOLCHAI
  │ N_REQUIRED_SURFACES|DEVELOPER_TOOLCHAIN_RECOMMENDED_SURFACES|LIVE_RUNTIME_PROJECT_TYPES"
  │ (scripts/validate_template.py)
  └ 14 lines found

● Read validate_template.py
  │ scripts/validate_template.py
  └ L296:340 (45 lines read)

● Search (grep)
  │ "active_docs_audit|preference_drift_audit|state_sync_audit|closeout_truth_audit|runtime_surface_
  │ guardrails" (scripts/validate_template.py)
  └ 18 lines found

● Search (grep)
  │ "status=passed|All tests passed|PASS|CONDITIONAL|FAIL|reviewer|independent
  │ evaluation|UAC|closeout" (scripts/validate_template.py)
  └ 50 lines found

● Search (grep)
  │ "skill invocation receipt|invocation receipt|candidate packet|promotion receipt|lineage|audit"
  │ (tests)
  └ 83 lines found

● Search (grep)
  │ "claude|codex|gemini|copilot|executor registry|executor command|availability|probe|doctor|which
  │ " in scripts/*.py
  └ 7 lines found

● Search (grep)
  │ "Developer Toolchain|verified-working|Runtime Evidence|User Surface Map|Logs or
  │ inspection|Debug" (tests)
  └ 9 lines found

● Read test_skill_evolution_pipeline.py
  │ tests/test_skill_evolution_pipeline.py
  └ L1:220 (81 lines read)

● Read test_validate_template.py
  │ tests/test_validate_template.py
  └ L650:860 (211 lines read)

● Search (grep)
  │ "executor|availability|which|probe|doctor|read-only pattern" (tests)
  └ 8 lines found

Verdict: Strong on structure and policy, but still weak on **runtime-proofing**; the main additions should make declared tool surfaces, executor availability, and evaluator paths mechanically verifiable rather than document-only.

| Priority | Proposal | Solves | Suggested surface | Governance risk |
|---|---|---|---|---|
| High | Developer Toolchain probe + freshness audit | Stops `verified-working` / `declared-unverified` from being prose-only by actually probing Diagnostics, Run, Health, Repro, Build, and Lint entries | `scripts/developer_toolchain_probe.py` plus optional `tmp/toolchain_receipts/` output and CI/hook wiring | Medium |
| High | Runtime-evidence coverage audit | Prevents live-runtime repos from declaring run paths without any usable logs/inspection, health, or user-surface evidence for debugging and repro | `scripts/runtime_evidence_audit.py` validating `Developer Toolchain`, `Runtime Evidence`, and `User Surface Map` together | Low |
| High | Executor registry + local probe | Makes multi-CLI discussion/review/evaluation support real instead of “document local commands somewhere,” so adopters can prove what Claude/Codex/Gemini/Copilot surfaces exist | `templates/executor_registry.template.*` + `scripts/executor_probe.py` | Medium |
| Medium | SKILL lineage auditor | Upgrades SKILL execution support from template rendering to real invocation→candidate→promotion integrity checks with valid IDs, links, and lineage fields | `scripts/skill_lineage_audit.py` integrated into `validate_template.py` | Low |
| Medium | Independent-evaluation receipt audit | Gives Rule 26 a concrete enforcement path so user-facing or non-trivial work cannot close without a real PASS/CONDITIONAL/FAIL evaluator artifact | `scripts/evaluation_receipt_audit.py` or an extension of `scripts/git_audit_pipeline.py` | Medium |

Recommended next move: ship the first three as one execution-support wave. They close the biggest downstream blame channels—“the toolchain entry existed but was never proven,” “the runtime had no observable debug path,” and “the template mentioned multi-executor review without a machine-checkable way to know what was installed”—then add lineage and evaluation audits as the second wave to harden SKILL and closeout integrity.

