## Verdict

**Support with revision.** Direction 3 (confidence-tiered auto-promotion) is correct in principle but under-specified in a dangerous way: "low-risk fields" is not a mechanical predicate, it is a judgment call that will silently expand over time. Support the delegated-reviewer model only if the confidence tier is defined structurally — by field name and evidence threshold in the SKILL contract itself — not by whoever runs the harvest agent at promotion time.

---

## Recommended Workflow

**Stage 1 — Task Closeout Receipt.** At task end, the executor emits a structured receipt: task ID, skill(s) invoked, outcome signal (success/fail/partial), and any fields that were exercised or hit a gap. No free text. Receipts are append-only.

**Stage 2 — Candidate Extraction.** A harvest agent reads N receipts above a configurable threshold and produces a `candidate_packet`: proposed field diffs, evidence pointers (receipt IDs, not transcripts), and a confidence tier label (`appendix-safe`, `normative-delegated`, `normative-human`). The agent may not set its own tier — the tier is computed from the field's tier classification in the SKILL contract.

**Stage 3 — Delegated Review.** A bounded reviewer role (any capable CLI or subagent) validates the candidate packet against the existing SKILL contract and review matrix. Its only outputs are: `approve`, `reject`, or `escalate`. It cannot edit the candidate packet.

**Stage 4 — Conditional Promotion.** `appendix-safe` candidates approved by delegated review auto-promote. `normative-delegated` candidates require a second delegated reviewer (different executor, same role). `normative-human` candidates are queued for direct human decision and cannot auto-promote under any condition.

**Stage 5 — Promotion Receipt.** Every promotion — including auto-promotions — writes a promotion receipt: what changed, who approved, which tier, which evidence. This is the audit trail that makes drift visible.

---

## Delegation Boundary

- **Fully automated:** Stage 1 (receipt emission), Stage 2 (candidate extraction), tier classification.
- **Delegated to role:** Stage 3 review for `appendix-safe` and `normative-delegated` tiers. Any capable executor may fill the role; the role is defined by the contract, not the vendor.
- **Must remain human:** Stage 4 for `normative-human` tier — specifically: `steps`, `trigger_when`, `do_not_trigger_when`, and `contract` fields. These define behavioral identity. Silent mutation here is indistinguishable from prompt injection.

---

## Risk Controls

**Top risks:** (1) Tier creep — fields gradually reclassified as `appendix-safe` to avoid bottlenecks. (2) Evidence laundering — receipts accumulate from a single repeated failure pattern, creating false consensus. (3) Reviewer collapse — two delegated reviewers from the same model family effectively constitute one opinion.

**Controls:** Lock tier classification behind a human-authored schema change, not runtime logic. Require candidate packets to show receipt diversity (minimum distinct task types). Require delegated reviewers to be from different executor families where two are needed.

---

## Best Contract Shape

Add to the SKILL contract:
- `promotion_tier` per field (enum: `appendix-safe | normative-delegated | normative-human`)
- `candidate_packet` artifact: `{ receipts[], proposed_diff, tier_label, confidence_score, harvest_agent_id }`
- `promotion_receipt` artifact: `{ candidate_id, reviewer_role, executor_id, decision, timestamp }`
- `reviewer_role` definition block: role name, required capabilities, exclusion rules (e.g., "not same executor as harvest agent")

Do not add a free-form `notes` field to the candidate packet — it will become a transcript smuggling vector.

---

## Strongest Disagreement With The Current Direction

The packet frames autonomy as a dial between Direction 1 and Direction 4, as if the only question is how much human review to remove. The harder problem is that **the harvest agent's tier judgment is itself a normative decision** and the current framing allows it to self-classify. Field-level tier must be frozen in the SKILL contract by a human and validated mechanically at harvest time — not inferred by the agent. Without this, Direction 3 degrades into Direction 4 in practice.

---

## Narrowest Next Question

Should `promotion_tier` be a per-field annotation on the SKILL schema itself — immutable except by direct human edit — or can it be overridden by a delegated reviewer on a per-candidate basis with escalation logged?
