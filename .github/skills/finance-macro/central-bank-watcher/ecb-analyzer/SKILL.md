---
name: ecb-analyzer
description: ECB policy decision, Lagarde press conference, and Monetary Policy Account analysis. Extracts policy signals, tracks PEPP/APP reinvestment policy, and detects Governing Council hawk/dove shifts.
category: finance-macro
domain: central-bank
allowed-tools: Bash(python3:*) Read(*)
---

# ECB Analyzer

## Purpose

Systematic analysis of European Central Bank monetary policy communications. The ECB's Governing Council represents 20 national economies with divergent conditions — making ECB analysis inherently more complex than single-country central banks. Tracks policy rate decisions, PEPP/APP reinvestment policy, TLTRO operations, and the Lagarde press conference for hawk/dove signals.

## When to Use

- "What did the ECB decide?"
- "Analyze the ECB statement"
- "Is the ECB hawkish or dovish?"
- "ECB rate path expectations?"
- "Lagarde press conference signals?"

## ECB Communication Structure

### Layer 1: Monetary Policy Statement (2:15pm CET, decision day)
- Policy rate decision (deposit facility, MRO, marginal lending)
- APP/PEPP reinvestment guidance
- TLTRO terms
- Economic assessment paragraph

### Layer 2: Press Conference (2:45pm CET)
- Lagarde prepared statement
- Q&A session — often contains stronger signals than the statement

### Layer 3: Monetary Policy Account (4 weeks after meeting)
- Detailed Governing Council discussion
- Dissenting views (not attributed by name, but described)
- Policy alternatives discussed

## Key ECB-Specific Metrics

| Indicator | Source | Signal |
|-----------|--------|--------|
| Deposit Facility Rate | ECB decision | Key policy rate |
| PEPP Reinvestment Pace | ECB statement | QT/QE direction |
| TLTRO Outstanding | ECB SDW | Bank funding reliance |
| Transmission Protection Instrument (TPI) | ECB statement | Anti-fragmentation tool availability |
| Eurozone Inflation (HICP) | Eurostat | Price stability assessment |
| Negotiated Wage Growth | ECB watcher surveys | Lagarde's key metric for policy |

## ECB Hawk-Dove Scoring

ECB policy stance is scored on the same -3 to +3 scale with these ECB-specific considerations:

| Dimension | Dovish Signal (-) | Hawkish Signal (+) |
|-----------|------------------|-------------------|
| Rate Guidance | "Restrictiveness can be reduced" | "Rates will stay sufficiently restrictive" |
| Inflation | "Well on track to 2%" | "Domestic inflation still elevated" |
| Growth | "Risks tilted to downside" | "Recovery gaining momentum" |
| Wages | "Moderating as expected" | "Wage growth remains high" |
| Fragmentation | TPI activation mentioned | "Spreads contained" |
| Balance Sheet | "PEPP reinvestments continue" | "APP runoff accelerated" |

## Country Divergence Monitor

Unlike the Fed, ECB policy must serve 20 economies with divergent conditions. Key fault lines:

| Dimension | Hawkish Countries (North) | Dovish Countries (South) |
|-----------|--------------------------|-------------------------|
| Growth | Germany, Netherlands (at/near potential) | Italy, Spain (slack) |
| Inflation | Baltics (higher CPI) | Greece, Portugal (lower) |
| Debt | Germany (~65% GDP) | Italy (~140%), Greece (~170%) |
| Banking | Netherlands, Germany (strong) | Italy, Greece (NPL legacy) |

**Implication**: ECB decisions often reflect compromise between these blocs. A "hawkish" decision may actually represent a compromise where doves conceded.

## Output Template

```markdown
## ECB Analysis — [Meeting Date]

### Decision
- Deposit Facility Rate: X.XX% (Change: ±XXbp)
- MRO Rate: X.XX% | Marginal Lending: X.XX%
- APP Reinvestment: [Full / Partial / None]
- PEPP Reinvestment: [Continuing / Partial / Ended]
- Vote: Consensus / Divided

### Key Language Changes
| Topic | Prior Statement | Current | Δ Signal |
|-------|----------------|---------|----------|
| Inflation | | | |
| Growth | | | |
| Wages | | | |
| Balance Sheet | | | |

### Lagarde Presser Signals
- Prepared Remarks Tone: [Confident / Concerned / Data-dependent]
- Q&A Highlights: [Key quote + interpretation]
- Hawk-Dove Score: [X] — [Label]

### Rate Path
| Timeline | Market Pricing | ECB Forward Guidance | Gap |
|----------|---------------|---------------------|-----|
| Next Meeting | XX% chance ±XXbp | — | |

### Country Divergence Note
- Key tension: [North vs South dimension]
- Compromise signal: [What was traded off]

### Assessment
- Policy Bias: [Easing / Hold / Tightening]
- Next Move: [Cut / Hold / Hike], likely [Date]
- EUR/USD Implication: [Supportive / Neutral / Headwind]
```

## Red Flags
- ECB Governing Council has 26 members — consensus is hard, surprises happen
- National central bank governors often speak before ECB meetings — causing market confusion
- Lagarde is a former politician (not PhD economist) — her communication style is less technical and sometimes ambiguous
- "Whatever it takes" (Draghi 2012) showed ECB can shift entire regime with one phrase — watch for Lagarde equivalent
- Fragmentation risk (BTP-Bund spread) can override inflation concerns — the ECB has a de facto sovereign backstop role
