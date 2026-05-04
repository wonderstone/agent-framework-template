# Macroeconomic Terminology Reference

## Monetary Policy

| Term | Definition | Key Source |
|------|------------|------------|
| Federal Funds Rate | Overnight interbank lending rate set by FOMC target range | FRED: FEDFUNDS |
| Quantitative Easing (QE) | Central bank purchases of government bonds to inject liquidity | Fed balance sheet: WALCL |
| Quantitative Tightening (QT) | Central bank balance sheet reduction (runoff or active sales) | WALCL decline |
| TGA (Treasury General Account) | US government's checking account at the Fed — drains liquidity when rising | FRED: TGA |
| RRP (Reverse Repo) | Overnight facility where MMFs park cash at the Fed — absorbs excess liquidity | FRED: RRPONTSYD |
| M2 Money Supply | Broad money: M1 + savings deposits + small time deposits + retail MMFs | FRED: M2SL |
| Net Liquidity | WALCL - TGA - RRP = effective liquidity injected into the financial system | Calculated |
| Taylor Rule | Formula linking policy rate to inflation gap and output gap | `references/taylor-rule.md` |
| Hawkish | Favoring tighter policy (higher rates) to fight inflation | FOMC statements |
| Dovish | Favoring looser policy (lower rates) to support growth/employment | FOMC statements |
| MLF (Medium-term Lending Facility) | PBOC's primary policy rate tool for guiding bank lending rates | PBOC |
| LPR (Loan Prime Rate) | China's benchmark lending rate, set monthly based on MLF + bank spread | PBOC |
| YCC (Yield Curve Control) | BOJ policy targeting 10-year JGB yield at ~0% (with flexible band since 2023) | BOJ |
| Forward Guidance | Central bank communication about future policy path | Statement analysis |

## Fiscal Policy

| Term | Definition |
|------|------------|
| Fiscal Deficit | Government spending minus revenue, usually % of GDP |
| Primary Balance | Fiscal balance excluding interest payments |
| Debt-to-GDP Ratio | Total government debt / GDP — key sustainability metric |
| Debt Dynamics | How debt/GDP evolves based on primary balance, interest rate, and growth |
| Fiscal Multiplier | Change in GDP per unit change in government spending or tax cut |
| Automatic Stabilizers | Tax revenue + welfare spending that automatically respond to the cycle |
| Structural Deficit | Fiscal balance adjusted for the economic cycle |

## Growth & Output

| Term | Definition | Key Indicator |
|------|------------|--------------|
| GDP (Gross Domestic Product) | Total value of goods and services produced | FRED: GDP, World Bank: NY.GDP.MKTP.CD |
| Real GDP | GDP adjusted for inflation (constant prices) | FRED: GDPC1 |
| GDP per Capita | GDP / population — rough living standard proxy | World Bank: NY.GDP.PCAP.CD |
| Potential Output | Maximum sustainable GDP without inflationary pressure | CBO estimate |
| Output Gap | (Actual - Potential) / Potential — negative = slack, positive = overheating | Calculated |
| PMI (Purchasing Managers' Index) | Survey of manufacturing/service sector — >50 = expansion, <50 = contraction | ISM, Markit |
| Industrial Production | Output of factories, mines, utilities | FRED: INDPRO |
| Capacity Utilization | % of industrial capacity being used — inflationary signal when >82% | FRED: TCU |
| Retail Sales | Consumer spending at retail level | FRED: RSAFS |

## Employment & Labor

| Term | Definition | Key Indicator |
|------|------------|--------------|
| Unemployment Rate | % of labor force actively seeking work | FRED: UNRATE |
| Labor Force Participation Rate | % of working-age population in the labor force | FRED: CIVPART |
| Nonfarm Payrolls | Monthly change in employment (ex. farms) | FRED: PAYEMS |
| Initial Jobless Claims | Weekly new unemployment benefit filings | FRED: ICSA |
| JOLTS Job Openings | Number of unfilled jobs — labor demand proxy | FRED: JTSJOL |
| Wage Growth | Average hourly earnings YoY change | FRED: CES0500000003 |
| NAIRU | Non-Accelerating Inflation Rate of Unemployment | CBO estimate |
| Underemployment (U-6) | Broader measure including part-time for economic reasons | FRED: U6RATE |

## Inflation & Prices

| Term | Definition | Key Indicator |
|------|------------|--------------|
| CPI (Consumer Price Index) | Urban consumer basket price change | FRED: CPIAUCSL |
| Core CPI | CPI ex. food and energy (less volatile) | FRED: CPILFESL |
| PCE (Personal Consumption Expenditures) | Fed's preferred inflation measure | FRED: PCEPI |
| Core PCE | PCE ex. food and energy — Fed's 2% target metric | FRED: PCEPILFE |
| PPI (Producer Price Index) | Wholesale/producer prices — leading indicator for CPI | FRED: PPIACO |
| Inflation Expectations | Market/survey expectations of future inflation | FRED: T5YIFR (5y breakeven) |
| Disinflation | Slowing inflation rate (still positive) | — |
| Deflation | Negative inflation rate (falling prices) | — |
| Stagflation | High inflation + low growth + high unemployment | — |

## Trade & Balance of Payments

| Term | Definition | Key Indicator |
|------|------------|--------------|
| Current Account | Trade balance + net income + net transfers | World Bank: BN.CAB.XOKA.GD.ZS |
| Trade Balance | Exports minus imports of goods and services | FRED: NETEXP (GDP component) |
| Terms of Trade | Export prices / import prices | National sources |
| Foreign Direct Investment (FDI) | Cross-border investment in productive assets | World Bank: BX.KLT.DINV.WD.GD.ZS |
| Exchange Rate (Spot) | Current market rate for currency pair | FRED: DEX+{CC}US series |
| Real Effective Exchange Rate (REER) | Trade-weighted, inflation-adjusted exchange rate | BIS |
| Foreign Exchange Reserves | Central bank holdings of foreign currency | IMF IFS |
| Capital Flight | Large-scale capital outflow, often during crisis | — |

## Financial Markets

| Term | Definition | Key Indicator |
|------|------------|--------------|
| Yield Curve | Term structure of interest rates across maturities | FRED: DGS{2,5,10,30} |
| 10Y-2Y Spread | DGS10 - DGS2 — negative = recession signal | FRED: T10Y2Y |
| 10Y-3M Spread | DGS10 - DTB3 — Fed's preferred recession indicator | FRED: T10Y3M |
| Credit Spread | Corporate bond yield - Treasury yield (same maturity) | FRED: BAA10Y |
| VIX | S&P 500 implied volatility — "fear index" | FRED: VIXCLS |
| Real Yield | Nominal yield - inflation expectations (TIPS breakeven) | FRED: DFII10 |
| Financial Conditions Index | Composite measure of financial tightness/ease | Chicago Fed NFCI |

## Property & Housing

| Term | Definition | Key Indicator |
|------|------------|--------------|
| House Price Index | Repeat-sales or hedonic house price measure | FRED: CSUSHPISA (Case-Shiller) |
| Housing Affordability Index | Median income / qualifying income × 100 | NAR |
| Price-to-Income Ratio | Median house price / median household income | OECD |
| Price-to-Rent Ratio | House price / annual rent — like P/E for housing | Calculated |
| Housing Starts | New residential construction begun | FRED: HOUST |
| Building Permits | Authorizations for new construction — leading indicator | FRED: PERMIT |
| Mortgage Rate | Average 30-year fixed rate | FRED: MORTGAGE30US |
| Mortgage Debt Service Ratio | Mortgage payments / disposable income | FRED: MDSP |
| Loan-to-Value Ratio (LTV) | Mortgage loan / property value | Bank surveys |
| Credit Impulse | Change in new credit / GDP — leading property cycle indicator | BIS, national sources |

## Cycle Terminology

| Term | Definition |
|------|------------|
| Business Cycle | Expansion → Peak → Contraction → Trough → Expansion |
| Leading Indicator | Indicator that changes before the economy (PMI, building permits, yield curve) |
| Coincident Indicator | Indicator that changes with the economy (employment, industrial production) |
| Lagging Indicator | Indicator that changes after the economy (unemployment rate, CPI) |
| Soft Landing | Tightening cycle ends without causing recession |
| Hard Landing | Tightening cycle triggers recession |
| Recession | Significant decline in economic activity across the economy (2+ quarters of negative GDP) |
| Depression | Prolonged, severe recession (no formal definition) |
| Property Cycle | Typically 18-year cycle (Harrison): Recovery → Boom → Bust → Stabilization |
| Commodity Supercycle | Multi-decade demand-driven commodity price upswing (often China/industrialization-led) |
| Liquidity Cycle | Expansion/contraction of central bank balance sheets and global money supply |
| Credit Cycle | Expansion/contraction of bank lending and private sector leverage |
