---
name: pboc-analyzer
description: PBOC monetary policy analysis covering MLF/LPR rate setting, RRR adjustments, PSL operations, and Q4 Monetary Policy Report. Tracks China's multi-rate framework and detects policy stance shifts from official communications.
category: finance-macro
domain: central-bank
allowed-tools: Bash(python3:*) Read(*)
---

# PBOC Analyzer

## Purpose

Analyze People's Bank of China monetary policy — unique among major central banks for its multi-rate, multi-tool framework. The PBOC uses quantity-based tools (RRR, PSL, window guidance) alongside price-based tools (MLF, LPR, 7D reverse repo), making policy stance interpretation more complex than single-rate central banks. Also tracks the quarterly Monetary Policy Report for formal policy signals.

## When to Use

- "What's PBOC doing?"
- "Did PBOC cut MLF?"
- "Analyze PBOC monetary policy stance"
- "China monetary policy direction?"
- "PBOC Q4 report signals?"

## PBOC Policy Tools Hierarchy

```
Tier 1 (Strategic — Monthly/Quarterly):
  MLF Rate (1Y): Core policy rate signal — most watched
  RRR: Reserve requirement — major liquidity injection tool
  LPR (1Y, 5Y+): Benchmark lending rates — derived from MLF

Tier 2 (Tactical — Daily/Weekly):
  7-Day Reverse Repo: Daily OMO — liquidity fine-tuning
  14-Day Reverse Repo: Pre-holiday liquidity management
  PSL: Directed infrastructure/housing lending

Tier 3 (Structural):
  Window Guidance: Informal lending quotas (not published)
  Relending Facilities: Targeted sector support (green, tech, agri)
  Macro-Prudential Assessments (MPA): Bank compliance framework
```

## PBOC Communication Sources

| Source | Frequency | Content | Reliability |
|--------|----------|---------|------------|
| MLF Operation Announcement | Monthly (15th) | Rate, amount | High |
| LPR Fixing | Monthly (20th) | 1Y and 5Y+ LPR | High |
| Monetary Policy Report | Quarterly | Full policy review, outlook | High (formal) |
| Governor Pan speeches | Irregular | Policy signals | Medium-High |
| Financial News (央行主管报纸) | Daily | Unofficial guidance, trial balloons | Medium |
| State Council meeting readouts | Irregular | Top-level policy direction | Highest |

## PBOC-Specific Hawk/Dove Framework

| Dimension | Easing Signal | Tightening Signal |
|-----------|-------------|-------------------|
| MLF Rate | Cut | Hike |
| RRR | Cut | Hike |
| LPR (especially 5Y) | Cut (property support) | Hold or hike |
| Aggregate Financing Growth | Accelerating | Decelerating |
| 7D Reverse Repo Volume | Large injections | Draining |
| PSL Issuance | New quota announced | No new quota |
| Report Language | "flexible and appropriate" (灵活适度) | "prudent" (稳健) |
| Property Language | "support reasonable demand" | "housing is for living, not speculation" |

## The PBOC Lexicon

PBOC communication uses codified phrases that signal policy shifts:

| Phrase (Chinese) | Translation | Policy Signal |
|-----------------|-------------|---------------|
| 稳健的货币政策 | "Prudent monetary policy" | Neutral (default) |
| 灵活适度 | "Flexible and appropriate" | Moderate easing |
| 精准有力 | "Targeted and forceful" | Active easing |
| 合理充裕 | "Reasonably ample" liquidity | Liquidity injection |
| 不搞大水漫灌 | "No flood irrigation" | No massive stimulus (yet) |
| 保持定力 | "Maintain resolve" | Resisting easing pressure |
| 以我为主 | "Self-oriented" (independent policy) | Decoupling from Fed |

## Output Template

```markdown
## PBOC Policy Analysis — [Date]

### Current Policy Settings
| Instrument | Rate/Level | Last Change | Direction |
|-----------|-----------|-------------|-----------|
| MLF (1Y) | X.XX% | [Date] ±XXbp | |
| RRR (large banks) | X.X% | [Date] | |
| LPR (1Y) | X.XX% | [Date] | |
| LPR (5Y+) | X.XX% | [Date] | |
| 7D Reverse Repo | X.XX% | [Date] | |

### Policy Stance Assessment
- Hawk-Dove Score: [X] — [Label]
- Liquidity Stance: [Injecting / Neutral / Draining]
- Credit Impulse: +X.X — [Expansion / Contraction]
- Key Phrase Shift: [Old → New | Signal]

### Key Constraints
- CNY Stability: [PBOC defending / Stable / Depreciation pressure]
- Capital Outflows: [Accelerating / Stable / Reversing]
- Property Sector: [Stabilizing / Still declining]
- Fed Divergence: [Following / Decoupling / Opposing]

### Assessment
- Primary Policy Direction: [Easing / Neutral / Tightening]
- Next Expected Move: [MLF cut / RRR cut / LPR cut / Hold]
- Probability of Additional Stimulus: XX% in [timeframe]
```

## Red Flags
- PBOC can cut RRR without cutting MLF — quantity vs price easing are independent
- Window guidance (informal lending quotas) is invisible to outsiders — always assume hidden policy
- The 5Y LPR is specifically for mortgages — PBOC can cut 5Y without cutting 1Y to target property
- Chinese media trial balloons often precede official policy — watch 金融时报 (Financial News)
- "Self-oriented" (以我为主) language = PBOC will ease even if Fed is hiking (decisive signal)
