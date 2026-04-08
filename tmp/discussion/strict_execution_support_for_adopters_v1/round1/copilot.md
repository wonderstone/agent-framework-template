Inspecting the requested framework surfaces first so I can separate design coverage from execution tooling gaps.

● Summarize target docs and scripts (shell)
  │ for f in README.md docs/ADOPTION_GUIDE.md docs/STRICT_ADOPTION_AND_VERIFICATION.md
  │ docs/SKILL_MECHANISM_V1_DRAFT.md docs/SKILL_HARVEST_LOOP_V1_DRAFT.md
  │ docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md docs/DEVELOPER_TOOLCHAIN_DESIGN.md
  │ docs/runbooks/multi-model-discussion-loop.md docs/runbooks/resumable-git-audit-pipeline.md
  │ scripts/validate_template.py scripts/state_sync_audit.py scripts/closeout_truth_audit.py …
  └ 19 lines...

I’ve got the high-level index; next I’m reading the specific sections that define adoption, toolchains, and the shipped pipelines so the recommendations land on missing execution surfaces rather than philosophy.

● Read README.md
  └ L1:220 (220 lines read)

● Read ADOPTION_GUIDE.md
  │ docs/ADOPTION_GUIDE.md
  └ L1:260 (260 lines read)

● Read STRICT_ADOPTION_AND_VERIFICATION.md
  │ docs/STRICT_ADOPTION_AND_VERIFICATION.md
  └ L1:260 (158 lines read)

● Read DEVELOPER_TOOLCHAIN_DESIGN.md
  │ docs/DEVELOPER_TOOLCHAIN_DESIGN.md
  └ L1:260 (260 lines read)

● Read SKILL_MECHANISM_V1_DRAFT.md
  │ docs/SKILL_MECHANISM_V1_DRAFT.md
  └ L1:260 (259 lines read)

● Read SKILL_HARVEST_LOOP_V1_DRAFT.md
  │ docs/SKILL_HARVEST_LOOP_V1_DRAFT.md
  └ L1:260 (156 lines read)

● Read multi-model-discussion-loop.md
  │ docs/runbooks/multi-model-discussion-loop.md
  └ L1:260 (143 lines read)

● Read SKILL_EXECUTION_LAYER_V1_DRAFT.md
  │ docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md
  └ L1:280 (279 lines read)

● Read resumable-git-audit-pipeline.md
  │ docs/runbooks/resumable-git-audit-pipeline.md
  └ L1:260 (86 lines read)

I’ve confirmed the docs already know they have some “design draft but not fully enforced yet” boundaries. Now I’m checking the shipped scripts to see exactly what execution support exists versus what’s still only described.

● Read closeout_truth_audit.py
  │ scripts/closeout_truth_audit.py
  └ L1:320 (132 lines read)

● Read git_audit_pipeline.py
  │ scripts/git_audit_pipeline.py
  └ L1:320 (274 lines read)

● Read skill_evolution_pipeline.py
  │ scripts/skill_evolution_pipeline.py
  └ L1:340 (205 lines read)

● Read discussion_pipeline.py
  │ scripts/discussion_pipeline.py
  └ L1:320 (320 lines read)

● Read state_sync_audit.py
  │ scripts/state_sync_audit.py
  └ L1:320 (297 lines read)

● Read validate_template.py
  │ scripts/validate_template.py
  └ L1:320 (320 lines read)

● Read validate_template.py
  │ scripts/validate_template.py
  └ L320:760 (441 lines read)

● Search (grep)
  │ "def audit_|class ValidationIssue|return issues|append\(|hard-fail|advisory"
  │ (scripts/validate_template.py)
  └ 129 lines found

● Search (grep)
  │ "required-core|manifest|Developer Toolchain|promotion_tier|skill|advisory|warning|runtime
  │ surface|discussion|git audit|state sync" (scripts/validate_template.py)
  └ 8 lines found

● Read validate_template.py
  │ scripts/validate_template.py
  └ L1560:1945 (385 lines read)

● Read bootstrap_adoption.py
  │ scripts/bootstrap_adoption.py
  └ L360:520 (161 lines read)

● Search (grep)
  │ "agent-framework-manifest|required_surface_kinds|required_top_level_fields|enforcement|project_t
  │ ype|capability|profile" (scripts/bootstrap_adoption.py)
  └ 54 lines found

I’ve verified the key asymmetry: the template already ships strong artifact generators and truth audits for governance, but the actual “do the work and prove the toolchain is usable” layer is thinner. I’m checking the adoption manifest and any existing downstream validator hooks so the proposals stay concrete.

● Read bootstrap_adoption.py
  │ scripts/bootstrap_adoption.py
  └ L660:720 (61 lines read)

● Search (grep)
  │ "verification packet|independent evaluation|evaluator|PASS|CONDITIONAL|FAIL|adoption
  │ status|fully adopted|partially adopted|design-only upgrade path kept" in **/*.{md,py,json}
  └ 5 lines found

● Get file or directory contents (MCP: github-mcp-server) · examples/full_stack_project/.github/age…
  └ successfully downloaded text file (SHA: b01d75a05520ba873878863803fe4ec605d3c...

● Read state_sync_pipeline.py
  │ scripts/state_sync_pipeline.py
  └ L1:320 (204 lines read)

● Read execution_contract.template.md
  │ templates/execution_contract.template.md
  └ L1:220 (170 lines read)

● Search (grep)
  │ "execution_contract|execution progress
  │ receipt|progress_receipt|drift_reconciliation|state_sync_pipeline|verification packet|strict
  │ adoption|agent-framework-manifest|independent evaluation" in **/*.{py,md,json}
  └ 7 lines found

Verdict: **The template is already strong on governance artifacts, truth-audits, and adoption philosophy, but still only medium-strength on execution closure for downstream repos: it ships many packet/receipt generators and validators, yet too few runnable surfaces that help an agent discover, execute, verify, and attest the real toolchain honestly.**

| Priority | Proposal | Solves | Why current support is insufficient | Suggested surface | Adoption tier | Governance risk |
|---|---|---|---|---|---|---|
| 1 | **Strict adoption auditor + attestation packet** | Lets a downstream repo prove **which baseline mechanisms are actually present, validated, and independently reviewed** before claiming `fully adopted`. | `docs/STRICT_ADOPTION_AND_VERIFICATION.md` requires honest adoption status and local CLI review, but there is **no dedicated script** that turns that into a standard artifact. `bootstrap_adoption.py` writes a manifest, but it only records profile/project type/expected files/toolchain contract, not mechanism claims or verification evidence. | Add `scripts/strict_adoption_audit.py`, `templates/adoption_verification_packet.template.md`, and extend `.github/agent-framework-manifest.json` with `mechanism_claims`, `verification_commands`, `independent_reviewers`, `adoption_status`, `last_verified_at`, `unresolved_gaps`. Validator should reconcile manifest + packet + repo state. | **Mandatory** for repos claiming **strict** adoption; optional for minimal profile. | Must **classify and evidence** adoption, not auto-upgrade a repo to `fully adopted` from file presence alone. |
| 2 | **Developer toolchain probe + freshness receipts** | Makes `verified-working` and `known-broken` statuses **provable and time-bounded**, so agents stop guessing whether declared commands still work. | `docs/DEVELOPER_TOOLCHAIN_DESIGN.md` explicitly says freshness rules for `verified-working` are not yet implemented, and `validate_template.py` mostly checks structure, not recent proof. A downstream agent can still say “the template told me to use this surface, but didn’t prove it was runnable.” | Add `scripts/developer_toolchain_probe.py` plus `templates/toolchain_probe_receipt.template.md`; write receipts under `tmp/toolchain_receipts/`. Validator should flag `verified-working` entries with no recent receipt, or impossible statuses for declared project type. | **Mandatory** for standard/full adopters; **profile-gated** for live-runtime surfaces (`Run`, `Health`, `Repro`). | Do **not** let probes silently rewrite project-context truth; they should produce receipts and proposed status changes only. |
| 3 | **Developer toolchain query/runner wrapper** | Gives agents a **machine-facing execution surface** for “what should I run next?” instead of forcing them to parse Markdown by convention. | The Developer Toolchain contract is well-defined, but it is still mostly a **human-readable table**. The template ships wrapper-style SKILL examples, but no general runner that consumes the adapter and enforces the ladder/stop rules. | Add `scripts/developer_toolchain_runner.py` with commands like `list-surfaces`, `select-surface`, `run-surface`, `explain-stop-rule`; optionally emit a normalized JSON snapshot from the project adapter. | **Mandatory** for strict/full adopters; optional for minimal. | Must refuse undeclared commands and honor fallback/stop rules, or it becomes a governance bypass. |
| 4 | **Independent evaluation pipeline** | Turns Rule 26 into a real executable path: **request evaluation, record verdict, tie it to UAC evidence, and gate closeout**. | Today the repo has `git_audit_pipeline.py` for task/receipt/handoff and reviewer-style templates, but no standard evaluator artifact with explicit `PASS / CONDITIONAL / FAIL` tied to user acceptance. That leaves independent evaluation partly policy-shaped. | Add `scripts/evaluation_pipeline.py` or extend `git_audit_pipeline.py` with `init-eval` and `record-verdict`; add `templates/evaluation_request.template.md` and `templates/evaluation_report.template.md`; validator/hook should require evaluator receipts for user-facing or multi-file completion claims. | **Mandatory** for user-facing or non-trivial work; optional for small internal refactors. | Highest risk is fake independence; the same executor must not be able to self-issue a passing verdict without explicit override. |
| 5 | **Local executor registry + review-loop runner** | Makes multi-CLI verification and discussion loops **actually runnable and repeatable** on downstream machines, with auditable failures when a local executor is unavailable. | `docs/runbooks/multi-model-discussion-loop.md` and strict adoption both rely on sending the same question to local CLIs, but the template intentionally stops at packet generation and avoids executor wiring. That preserves portability, but leaves adopters to invent the runtime loop themselves. | Add `templates/local_executor_registry.template.json` and `scripts/executor_review_loop.py` to read machine-local commands, dispatch read-only prompts, capture outputs, and append them into discussion/verification packets with explicit `available / unavailable / failed` states. | **Optional / profile-gated** by local CLI availability; **mandatory** only if the repo claims independent local CLI verification. | Must never treat “executor unavailable” as implicit approval; blocked review is evidence, not success. |
| 6 | **Execution-session initializer and checkpoint scheduler** | Reduces long-task drift by making it easy to **start a task with one coherent contract**, emit first receipts, and keep packet/state surfaces aligned. | The repo ships `execution_contract.template.md`, `state_sync_pipeline.py`, and `git_audit_pipeline.py`, but no single downstream command that initializes the execution contract, task packet, first checkpoint, and sync cadence together. Agents still hand-stitch those surfaces. | Add `scripts/execution_session.py` or extend `state_sync_pipeline.py` with `init-execution`, `checkpoint`, `record-blocker`, `close-phase`; validator can detect checkpointed tasks that have receipts but no execution contract or task packet. | **Mandatory** for long-task/checkpointed workflows; optional for small tasks. | Should scaffold and audit; it must not “bless” execution when UAC, scope, or protected-path checks are unresolved. |
| 7 | **SKILL runtime router / trigger evaluator** | If adopters keep the SKILL path, this provides the missing **invoke/skip/load references/emit receipt** execution layer so skills are not just governed documents. | `docs/SKILL_EXECUTION_LAYER_V1_DRAFT.md` explicitly says the framework currently standardizes the decision shape and receipt fields, but repos may implement runtime behavior however they want. `skill_evolution_pipeline.py` generates artifacts from supplied data; it does not perform trigger evaluation or runtime binding. | Add `scripts/skill_runtime.py` with `evaluate-trigger`, `start-invocation`, `complete-invocation`; add a lightweight skill registry surface mapping `skill_id -> references -> wrapper target`. Validator should require at least one executable skill surface before a repo claims “execution-backed SKILL accumulation.” | **Optional / profile-gated**; **mandatory** only for repos that claim skill accumulation through execution evidence. | This is the most governance-sensitive area: the router must never mutate canonical SKILL truth or auto-promote candidates. |
| 8 | **Mechanism-claim validator for downstream manifests** | Prevents downstream repos from hiding behind vague “we adopted the framework” language by forcing them to make **explicit, auditable mechanism claims**. | Current manifests mostly describe profile and toolchain contract. They do not declare whether a repo actually kept execution contracts, state-sync stack, independent evaluation, discussion workflow, runtime guards, or SKILL execution surfaces. | Extend manifest schema with per-mechanism claim rows: `kept`, `downgraded`, `inapplicable`, `design-only`; add validator checks that every strong claim has a concrete file/script/receipt mapping and that downgraded items are reported honestly. | **Mandatory** for strict adoption; optional otherwise. | Risk is over-bureaucratizing minimal repos; keep the claim set focused on strict-baseline mechanisms only. |

Recommended next move: **Build the downstream proof stack first, not more philosophy**: start with (1) a strict adoption auditor, (2) toolchain probe receipts, and (3) an independent evaluation pipeline. Those three additions would most directly remove the downstream agent’s strongest excuse today—“the template described honest execution, but didn’t give me enough runnable surfaces to prove the repo could actually do it.”

