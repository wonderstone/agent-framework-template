---
name: central-bank-watcher
description: Central bank policy analysis — FOMC, ECB, PBOC, BOJ. Hawk-dove scoring (-3 to +3), cross-bank policy divergence, rate path expectations.
category: finance-macro
domain: central-bank
allowed-tools: Bash(python3:*) Read(*)
---

# Central Bank Policy Watcher

## Purpose

Systematic analysis of major central bank communications. Instead of reading every statement manually, this domain parses policy signals to generate hawk-dove scores, detect shifts in tone, and quantify cross-bank policy divergence/convergence.

## How to Use

```bash
python3 central-bank-watcher/scripts/hawk_dove_scorer.py
```

## Hawk-Dove Framework

Every policy communication is scored -3 (very dovish) to +3 (very hawkish):

| Score | Label | Rate Implication |
|-------|-------|-----------------|
| +3 | Strongly Hawkish | +50bp+, inflation fighting priority |
| +2 | Hawkish | +25bp, further tightening likely |
| +1 | Slightly Hawkish | Hold with hawkish bias |
| 0 | Neutral | Hold, balanced risks |
| -1 | Slightly Dovish | Hold with dovish bias |
| -2 | Dovish | -25bp, ready to ease soon |
| -3 | Strongly Dovish | -50bp+, crisis response |

**Cross-bank divergence** = average absolute difference between central banks' hawk-dove scores. High divergence → FX volatility, carry trade opportunities. Low divergence → synchronized cycle, range-bound FX.

## Red Flags
- Hawk-dove scoring is subjective — always note the basis for the score
- Market pricing ≠ actual outcome — Fed funds futures can be wrong by 100bp+
- Dot plots aren't commitments — SEP projections change meeting to meeting
- PBOC doesn't use forward guidance the way Fed/ECB do — less signal from statements
- BOJ communication is deliberately ambiguous — read between the lines
