---
name: hawk-dove-index
description: Cross-central bank hawk/dove scoring system with historical comparison and policy divergence detection. Tracks sentiment shifts across Fed, ECB, PBOC, and BOJ to identify convergence/divergence trade opportunities.
category: finance-macro
domain: central-bank
allowed-tools: Bash(python3:*) Read(*)
---

# Hawk-Dove Index — Cross-Bank Policy Sentiment

## Purpose

Cross-central bank hawk/dove scoring. Scores each major central bank on a -3 (strongly dovish) to +3 (strongly hawkish) scale based on their most recent policy communications. Tracks changes over time, detects policy divergence/convergence, and identifies FX and carry trade implications.

## When to Use

- "Compare Fed vs ECB hawkishness"
- "Rate differential trends?"
- "Which central bank is most hawkish right now?"
- "Policy divergence trade opportunities?"
- "Central bank sentiment tracker"

## Scoring Methodology

### Dimensions Scored

| Dimension | Weight | Source |
|-----------|--------|--------|
| Policy Rate Direction | 30% | Rate decision + forward guidance |
| Inflation Assessment | 25% | Statement language on price stability |
| Growth/Labor Assessment | 20% | Statement language on real economy |
| Balance Sheet Policy | 15% | QT/QE pace and forward guidance |
| Risk Assessment | 10% | Balance of risks language |

### Score Calculation

```
HawkDove_Score = Σ (Dimension_Score × Weight)

Dimension_Score ∈ {-3, -2, -1, 0, +1, +2, +3}
```

### Score Interpretation

| Score Range | Classification | Policy Bias |
|-------------|---------------|-------------|
| +2.0 to +3.0 | Strongly Hawkish | Tightening aggressively |
| +1.0 to +1.9 | Moderately Hawkish | Tightening, data-dependent |
| +0.4 to +0.9 | Slightly Hawkish | Hold with hawkish bias |
| -0.3 to +0.3 | Neutral | Patient, balanced risks |
| -0.9 to -0.4 | Slightly Dovish | Hold with dovish bias |
| -1.9 to -1.0 | Moderately Dovish | Easing bias, preparing cuts |
| -3.0 to -2.0 | Strongly Dovish | Easing aggressively |

## Policy Divergence Matrix

```
|              | Fed  | ECB  | PBOC | BOJ  |
|--------------|------|------|------|------|
| Fed          |  —   | Diff | Diff | Diff |
| ECB          |      |  —   | Diff | Diff |
| PBOC         |      |      |  —   | Diff |
| BOJ          |      |      |      |  —   |
```

### Divergence Interpretation

| Divergence | Score Gap | Trade Implication |
|-----------|-----------|-------------------|
| High | > 3.0 | Strong directional FX trend |
| Moderate | 1.5 - 3.0 | Range with direction bias |
| Low | < 1.5 | Range-bound, carry dominates |

## Output Template

```markdown
## Hawk-Dove Index — [Date]

### Current Scores
| Central Bank | Score | Classification | Change from Prior | Trend |
|-------------|-------|---------------|-------------------|-------|
| Fed | +X.X | [Label] | ±X.X | → |
| ECB | +X.X | [Label] | ±X.X | → |
| PBOC | -X.X | [Label] | ±X.X | → |
| BOJ | -X.X | [Label] | ±X.X | → |

### Policy Divergence Heatmap
| Divergence | Fed-ECB | Fed-PBOC | Fed-BOJ | ECB-BOJ |
|-----------|---------|---------|---------|---------|
| Score Gap | X.X | X.X | X.X | X.X |
| Intensity | [High/Mod/Low] | | | |

### Rate Differential Summary
| Pair | Policy Rate Gap | 2Y Yield Gap | Direction |
|------|----------------|-------------|-----------|
| USD-EUR | +X.XX% | +X.XX% | USD favored |
| USD-JPY | +X.XX% | +X.XX% | USD favored (carry) |
| USD-CNY | ±X.XX% | ±X.XX% | |

### Historical Context
- Current divergence level: [X] percentile over 5 years
- Trend: [Converging / Diverging / Stable]
- Peak divergence (5Y): [Date] at [Score]

### Trade Implications
- **FX**: [USD strength supported / USD weakness signal / Range-bound]
- **Carry Trade**: [JPY-funded carry attractive / at risk / neutral]
- **EM**: [Divergence supportive / headwind for EM FX]
- **Gold**: [Rate convergence bullish / hawkish Fed headwind]
```

## Red Flags
- Scoring is inherently subjective — document the basis for each score
- Central banks can pivot rapidly (ECB went from -3 to +3 in 12 months in 2022)
- Market pricing may already reflect divergence — check if priced in
- PBOC communication is less transparent — score has wider confidence interval
- BOJ score is about normalization direction, not absolute rate level
