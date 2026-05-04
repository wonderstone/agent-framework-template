---
name: fomc-analyzer
description: Systematic FOMC statement, minutes, dot plot, and Powell press conference analysis. Extracts policy signals, sentiment shifts, and generates rate path scenarios with hawk/dove classification.
category: finance-macro
domain: central-bank
allowed-tools: Bash(python3:*) Read(*)
---

# FOMC Analyzer

## Purpose

Systematic analysis of Federal Open Market Committee communications. Parses statements, minutes, Summary of Economic Projections (SEP / dot plot), and Powell's press conferences to extract policy signals. Tracks changes in Fed language over time and generates forward-looking rate path scenarios.

## When to Use

- "What did the FOMC decide?"
- "Analyze the FOMC statement"
- "What changed in the dot plot?"
- "Is Powell hawkish or dovish?"
- "What's the rate path pricing?"
- "What's the Fed's reaction function right now?"

## FOMC Communication Layers

### Layer 1: Statement (Immediate — 2pm release day)
- Rate decision (hike/cut/hold)
- Balance sheet policy (QT pace)
- Economic assessment paragraph
- Voting breakdown (unanimous/dissents)
- Key phrase shifts from prior statement

### Layer 2: SEP / Dot Plot (Quarterly — Mar/Jun/Sep/Dec)
- Fed funds rate projections (current year, next 2 years, longer run)
- GDP, unemployment, PCE, core PCE projections
- Dot distribution: median, mean, range, clustering
- "Longer run" dot = neutral rate estimate

### Layer 3: Press Conference (30 min after release)
- Prepared remarks: context for decision
- Q&A: unscripted policy signals
- Tone: confidence, concern, uncertainty

### Layer 4: Minutes (3 weeks after meeting)
- Detailed discussion of economic outlook
- Risk assessment details
- Dissent reasoning
- Balance sheet discussion

## Statement Language Tracking

Key phrase shifts to monitor:

| Topic | Dovish Signal | Neutral | Hawkish Signal |
|-------|-------------|---------|---------------|
| Inflation | "making progress toward 2%" | "remains elevated" | "lack of further progress" |
| Labor | "come into better balance" | "strong" | "extremely tight" |
| Risks | "balanced" | "moving into better balance" | "weighted to upside" |
| Forward | "adjusting policy" (cut signal) | "data-dependent" | "further tightening" |
| Confidence | "gained greater confidence" | "needs greater confidence" | "highly attentive to inflation" |

## Dot Plot Analysis

```
Median dot = central tendency of rate projections
Dot dispersion = degree of committee uncertainty

Key to watch:
- Median dot vs market pricing (gap = surprise potential)
- Shifts in "longer run" dot (neutral rate estimate)
- Clustering: are dots concentrated or widely dispersed?
- Hawks (high dots) vs Doves (low dots) count
```

## Process

For each FOMC event:
1. Fetch statement text
2. Compare to prior statement — identify changed language
3. Score hawk/dove: -3 to +3
4. If SEP release: analyze dot plot shifts
5. Compare to market pricing — identify gap
6. Generate 3 scenarios (base, hawkish, dovish)

## Output Template

```markdown
## FOMC Analysis — [Meeting Date]

### Decision
- Rate: [Held at / Increased to / Cut to] X.XX%
- Vote: [Unanimous / X-Y with [Name] dissenting]
- QT: [Continuing at $XXB/mo / Tapering / Ended]

### Language Changes
| Topic | Prior Statement | Current Statement | Δ Signal |
|-------|----------------|-------------------|----------|
| Inflation | "elevated" | "making progress" | +1 dovish |
| Labor | "strong" | "strong but moderating" | +1 dovish |
| ... | | | |

### Dot Plot (If SEP)
| Year | Median Projection | Prior Median | Change |
|------|------------------|-------------|--------|
| 20XX | X.XX% | X.XX% | ±XXbp |
| 20XX | X.XX% | X.XX% | ±XXbp |
| Long-Run | X.XX% | X.XX% | ±XXbp |

### Hawk-Dove Score: [X] — [Label]
- Inflation tone: [Score]
- Labor tone: [Score]
- Forward guidance: [Score]
- Risk assessment: [Score]
- **Composite: [Score]**

### Rate Path Scenarios
| Scenario | 3M | 6M | 12M | Probability |
|----------|----|----|-----|------------|
| Base Case | X.XX% | X.XX% | X.XX% | XX% |
| Hawkish | X.XX% | X.XX% | X.XX% | XX% |
| Dovish | X.XX% | X.XX% | X.XX% | XX% |

### Key Takeaway
[2-3 sentence synthesis of the most important signal from this meeting]
```

## Red Flags
- FOMC dots are individual views, not commitments — members change views
- Dissents matter — the first dissent in a direction often precedes a policy shift
- "Transitory" and "patient" were both retired after being proven wrong — watch for word retirement
- Powell's Q&A often contains stronger signals than the statement
- Market reaction (first 30 min) often reverses by next day — don't over-interpret initial moves
