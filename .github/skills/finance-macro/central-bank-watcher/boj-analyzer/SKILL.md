---
name: boj-analyzer
description: Bank of Japan policy analysis covering YCC framework, JGB purchase operations, ETF policy, and Outlook Report. Tracks BOJ normalization progress and Ueda communication style for hawk/dove signals.
category: finance-macro
domain: central-bank
allowed-tools: Bash(python3:*) Read(*)
---

# BOJ Analyzer

## Purpose

Analyze Bank of Japan monetary policy as it navigates the most delicate normalization in modern central banking history. After decades of deflation and ultra-loose policy, the BOJ is cautiously moving toward normalizing rates, unwinding YCC, and reducing JGB purchases. Every word from Governor Ueda and every basis point of rate adjustment is scrutinized by global markets due to Japan's role as the world's largest creditor nation.

## When to Use

- "What did the BOJ decide?"
- "BOJ normalization progress?"
- "YCC changes?"
- "Is the BOJ going to hike again?"
- "Ueda press conference analysis?"
- "BOJ Outlook Report review?"

## BOJ Communication Structure

### Layer 1: Policy Statement (meeting day, ~12pm JST)
- Policy rate decision
- YCC band/framework changes
- JGB purchase plan
- ETF/J-REIT purchase policy
- Voting breakdown (9 members)

### Layer 2: Outlook Report (quarterly: Jan, Apr, Jul, Oct)
- GDP and CPI forecasts for 3 fiscal years
- Risk balance assessment (upside/downside)
- Median board member forecasts + individual dots
- "Outlook for Economic Activity and Prices"

### Layer 3: Ueda Press Conference (3:30pm JST)
- Prepared remarks
- Q&A — Ueda is more technical than Kuroda, markets parse carefully

### Layer 4: Summary of Opinions (~10 days after meeting)
- Individual board member views (anonymized)
- Reveals dissent strength and direction

## BOJ Normalization Roadmap

```
Phase 1: YCC Flexibility (Done — 2022-2023)
  → Widened 10Y band from ±0.25% to ±0.50% to ±1.0% "reference"

Phase 2: YCC Abandonment + First Hike (Done — Mar 2024)
  → Ended negative rate (-0.1% → 0 to 0.1%)
  → Abandoned formal YCC, kept JGB purchase pace
  → Ended ETF/J-REIT purchases

Phase 3: Gradual Rate Normalization (Current)
  → Rate moved to 0.25% (Jul 2024)
  → Rate moved to 0.50% (?)
  → JGB purchase tapering announced

Phase 4: Full Normalization (Future)
  → Rate above 1% (neutral estimate)
  → JGB purchases minimal (balance sheet runoff)
  → QT full implementation

Phase 5: Steady State
  → Policy rate at neutral (1-2% estimated)
  → Balance sheet normalized (but still large)
  → Conventional inflation-targeting framework
```

## BOJ-Specific Hawk/Dove Framework

| Dimension | Dovish (No Normalization) | Hawkish (Normalization) |
|-----------|--------------------------|------------------------|
| Policy Rate | Hold at current level | Hike signal or hike |
| YCC | Maintain reference | Widen band / abandon |
| JGB Purchases | Maintain pace | Taper announced |
| CPI Forecast | "Below 2% medium-term" | "Above 2%, virtuous wage-price cycle" |
| Wage Growth | "Needs monitoring" | "Spring wage negotiations positive" |
| Yen Assessment | "FX should reflect fundamentals" | "Rapid FX moves undesirable" (yen weakness concern) |
| Consumption | "Moderate recovery" | "Resilient despite price rises" |

## Ueda-Specific Signals

Governor Ueda is an academic economist (MIT PhD, former BOJ board member) with a more systematic approach than Kuroda:

| Ueda Signal | Meaning |
|-------------|---------|
| "Virtuous wage-price cycle" | Confirmation of sustainable 2% inflation — key hurdle for hikes |
| "Spring wage negotiations" (春闘) | Key data point — strong Shunto = green light for hike |
| "Accommodative conditions maintained" | Even after hike, policy remains loose — don't fear tightening |
| Mentions specific data | Ueda references specific indicators — track these for hike signals |
| "Japan's neutral rate" discussion | Preparing markets for normalization end-point |
| References to 1990s/2000s | Drawing historical parallels — typically cautious |

## Output Template

```markdown
## BOJ Policy Analysis — [Meeting Date]

### Decision
- Policy Rate: X.XX% (Change: ±XXbp | Vote: X-Y)
- YCC: [10Y reference at X% / Abandoned]
- JGB Purchases: ¥X.XT/month (Change: [Maintained / Tapered to ¥XT])
- ETF/J-REIT: [No purchases / Suspended / Ended]

### Outlook Report (if quarterly meeting)
| FY | Real GDP | Core CPI (ex. fresh food) | Risk Balance |
|----|---------|--------------------------|-------------|
| FY20XX | +X.X% | +X.X% | Upside / Balanced / Downside |
| FY20XX | +X.X% | +X.X% | |
| FY20XX | +X.X% | +X.X% | |

### Hawk-Dove Score: [X] — [Label]
- Rate Signal: [Score]
- Wage Assessment: [Score]
- CPI Outlook: [Score]
- YCC Stance: [Score]

### Normalization Progress
- Current Phase: [Phase X — Label]
- Phase Progress: XX%
- Next Milestone: [e.g., 0.50% hike, JGB taper acceleration]
- Estimated Timeline: [Date]

### Market Implications
- USD/JPY: [BOJ hike supports yen / BOJ hold weighs on yen]
- JGB 10Y: [YCC ceiling, market pressure]
- Global Spillover: [JPY carry trade, JGB repatriation risk]
- Nikkei: [Yen strength headwind / Weak yen support]

### Assessment
- Normalization Path: [On track / Accelerating / Delayed]
- Key Risk: [Political pushback / Global recession / Yen overshoot]
```

## Red Flags
- BOJ has a long history of premature tightening (2000, 2006) — Ueda is hyper-aware of this
- Political pressure against normalization is strong — LDP relies on cheap funding for fiscal expansion
- MOF (Ministry of Finance) controls FX intervention separately from BOJ — contradictory signals possible
- Japanese wage data (春闘 results) is the single most important indicator for BOJ policy — track actively
- Japan's government debt (250%+ GDP) = rate normalization has severe fiscal consequences
- BOJ owns ~50% of JGB market — Japan is in uncharted territory in unwinding this
