---
name: ecb-watcher
description: Monitor European Central Bank balance sheet, APP/PEPP portfolios, TLTRO operations, and Eurosystem liquidity. Track ECB policy rate, balance sheet runoff, and net liquidity contribution to global conditions.
category: finance-macro
domain: liquidity
allowed-tools: Bash(python3:*) Read(*)
---

# ECB Watcher — European Central Bank Liquidity Analysis

## Purpose

Track ECB monetary policy operations and balance sheet evolution. Monitor APP (Asset Purchase Programme) and PEPP (Pandemic Emergency Purchase Programme) reinvestment/runoff, TLTRO (Targeted Longer-Term Refinancing Operations) repayments, and Eurosystem net liquidity. The ECB began QT later than the Fed (March 2023) and uses a different approach — partial reinvestment rather than passive runoff caps.

## When to Use

- "What's the ECB balance sheet?"
- "How fast is ECB QT running?"
- "What's happening with TLTRO repayments?"
- "ECB vs Fed liquidity comparison"
- "European liquidity conditions"

## Key Indicators

| Indicator | Source | Frequency | What It Tells Us |
|-----------|--------|-----------|-----------------|
| ECB Total Assets | ECB SDW | Weekly | Total balance sheet size |
| APP Portfolio | ECB SDW | Monthly | Asset Purchase Programme holdings |
| PEPP Portfolio | ECB SDW | Monthly | Pandemic QE portfolio |
| TLTRO Outstanding | ECB SDW | Monthly | Bank borrowing from ECB |
| ECB Policy Rate (Deposit Facility) | ECB | Per meeting | Key policy rate |
| Excess Liquidity | ECB SDW | Weekly | Banking system liquidity buffer |
| Government Deposits | ECB SDW | Weekly | Fiscal factor — drains liquidity |

## ECB QT Mechanics

Unlike the Fed, the ECB doesn't use caps:
- **APP**: Full reinvestment ended July 2023. Passive runoff ~€25B/month.
- **PEPP**: Partial reinvestment ended December 2024. Passive runoff ~€7.5B/month.
- **TLTRO**: Loans maturing — banks repaying. Outstanding declining naturally.
- **Total QT pace**: ~€30-35B/month balance sheet reduction.

## ECB vs Fed Liquidity

| Dimension | Fed | ECB |
|-----------|-----|-----|
| QT Start | June 2022 | March 2023 |
| QT Method | Monthly caps (Treasury + MBS) | Passive runoff, no caps |
| Monthly Runoff | ~$60B (often below cap) | ~€30-35B |
| Balance Sheet Peak | $8.96T (April 2022) | €8.84T (June 2022) |
| RRP Equivalent | RRP facility (~$100B+) | Excess liquidity (€3T+) — still massive |
| Key Difference | RRP → 0 means QT bites directly | Excess liquidity abundant — no near-term scarcity |

## Process

```bash
# ECB data via API
python3 mcp-servers/ecb-mcp/server.py get_series '{"series_id":"ILM.W.U2.C.A052.U2.EUR"}'
python3 scripts/fetch_ecb.py --balance-sheet
```

## Output Template

```markdown
## ECB Liquidity Dashboard — [Date]

### Balance Sheet
| Metric | Value | Monthly Change | YoY Change |
|--------|-------|---------------|------------|
| ECB Total Assets | €X.XXT | -€XXB | -€XXXB |
| APP Portfolio | €X.XXT | -€XXB | |
| PEPP Portfolio | €X.XXT | -€XB | |
| TLTRO Outstanding | €XXXB | -€XXB | |
| Excess Liquidity | €X.XXT | | |

### Policy Stance
- Deposit Facility Rate: X.XX%
- Next Meeting: [Date]
- Market Pricing: [XXbp cut/hike/hold]
- QT Pace: €XXB/month

### Assessment
- Liquidity Contribution: [Positive / Neutral / Draining]
- Banking System: [Abundant / Ample / Scarce] reserves
- EUR Impact: Liquidity conditions [supportive / neutral / headwind] for EUR
```

## Red Flags
- ECB data is in euros — currency-adjusted comparison to Fed needs EUR/USD FX rate
- Excess liquidity (€3T+) means QT won't cause reserve scarcity for years
- TLTROs are repaid at maturity — concentrated repayment dates can cause volatility
- National central bank (NCB) operations differ across Eurosystem
- Italian sovereign-bank nexus means BTP spread widening can trigger emergency measures
