## Verdict
**Choose A — per-field `promotion_tier` column in the canonical SKILL schema.**

The six-field review matrix already exists as a per-field table enforced by the validator. Adding one column is a single additive extension to an already-truthful structure, and it anchors authority classification exactly where the validator already checks — no runtime reclassification is possible without a schema-level human-authored change.

---

## Why The Other Two Lose

- **B (section-level mutable-zone map):** `governance` alone spans three subsections with different promotion sensitivity. Section boundaries are coarser than field semantics and porous to reshuffling — content can migrate between sections to escape a restriction without changing meaning.
- **C (hybrid: sections + per-field overrides):** introduces a precedence ambiguity (which wins when they conflict?) that harvesters can use to argue their own reclassification is valid. Two overlapping models with no clear resolution rule is a larger attack surface than one model with six rows.

---

## Minimal Contract Shape

**One new column in the existing Receipt And Review Matrix table.** Current 4-column matrix becomes 5 columns:

```
Field | Proposal evidence tiers | Minimum reviewer threshold | Guardrail override | Promotion authority
```

`Promotion authority` is a **closed enum, three values only:**
- `delegated-safe` — delegated reviewer role may approve without escalation, provided evidence tier is met
- `delegated-reviewed` — delegated reviewer may approve, but must be human-accountable and distinct from the proposing system
- `human-only` — direct human approval required before any canonical mutation

**Default assignment for the six canonical fields:**

| Field | Promotion authority | Rationale |
|---|---|---|
| `purpose` | `human-only` | Defines skill identity; any rewrite is constitutional |
| `triggers` | `human-only` | Scope expansion is not safe to delegate |
| `entry_instructions` | `delegated-reviewed` | Normative; delegable with tier 1-3 evidence and a non-proposing reviewer |
| `references` | `delegated-safe` | Append-only artifact growth; low drift risk; already single-reviewer in current matrix |
| `governance` | `human-only` | Contains the reviewer rules themselves — delegating its own update is circular |
| `degradation` | `delegated-reviewed` | Fallback behavior; delegable with tier 1-3, owner-review per existing guardrail override |

**Where each piece lives:**
- **`SKILL_MECHANISM_V1_DRAFT.md`** — enum definition and default assignment table. Human-authored source of truth, not derivable at runtime.
- **`skill.template.md`** — add fifth column to the matrix skeleton.
- **`validate_template.py`** — extend column count check 4→5; hard-fail on unknown enum values; hard-fail if `governance` is classified as anything other than `human-only`.
- **Promotion receipts (new artifact type)** — must include the `promotion_tier` value, reviewer identity/role, and evidence set. Receipt is produced by the reviewer, not the proposer.

---

## Validator Strategy

**Mechanically enforceable:**
- Presence of the fifth column in every skill file's matrix
- Closed-enum check: only the three valid values pass
- Hard rule: `governance` must always be `human-only` — any other value is a hard fail
- Reviewer-proposer disjunction: a promotion receipt naming the same system as both proposer and reviewer is a hard fail
- Guardrail-type skills: no field may be classified below `delegated-reviewed` (validator can assert this from the existing `Type` metadata)

**Still needs escalation or human ownership:**
- Evidence quality disputes (is a tier-3 receipt genuinely structured, or a transcript summary relabeled?)
- Contradiction across multiple individually-valid `delegated-reviewed` patches that cumulatively rewrite normative posture
- Whether a named delegated reviewer role is actually human-accountable — this is governance policy, not static validation
- Semantic changes to `purpose`/`triggers` scope that arrive through `entry_instructions` edits

---

## Drift Failure Mode

**Compound accumulation in `entry_instructions`.** Each individual `delegated-reviewed` patch is technically valid — it meets evidence tier, uses a legitimate reviewer, and touches only a `delegated-reviewed` field. After N patches, the cumulative `entry_instructions` has been rewritten in posture and scope without any single change crossing the `human-only` threshold.

**Tightest mitigation:** require a full-skill drift audit every K=5 promotions to any `delegated-reviewed` field, anchored to a snapshot taken at the last `human-only` review. The audit compares the semantic relationship between current `entry_instructions` and the frozen `purpose`/`triggers`. The audit itself must be human-reviewed before the counter resets. The validator blocks further `delegated-reviewed` promotions once K is reached until the audit receipt is logged.

---

## Migration Path

1. Add the `promotion_tier` enum definition and default assignment table to `SKILL_MECHANISM_V1_DRAFT.md`.
2. Backfill the two existing example skills — add the fifth column to each matrix (two edits).
3. Update `skill.template.md` — add the fifth column to the skeleton.
4. Extend `validate_template.py` — increment column count check 4→5, add the closed-enum check.
5. Deploy atomically: all skill files and the validator must be updated in the same commit, since the validator currently hard-fails on anything other than exactly 4 columns.

The migration requires exactly one review gate: a dual-reviewer sign-off on the canonical doc change that introduces the default assignment table, since that table is itself a governance decision.

---

## Narrowest Remaining Question

Should the K-patch drift audit counter live inside the skill file itself as a mutable field, or outside in a separate promotion-state registry — given that a skill file tracking its own patch count can be gamed by resetting the counter through a legitimate `delegated-reviewed` edit to a non-`governance` field?
