# Racial Equity Dataset — 20 Largest U.S. Cities

[![Dataset Version](https://img.shields.io/badge/version-1.0.0-blue)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-CC%20BY%204.0-green)](LICENSE)
[![Cities](https://img.shields.io/badge/cities-20-orange)]()
[![Last Updated](https://img.shields.io/badge/updated-April%202026-lightgrey)]()

A structured, open research dataset comparing racial equity plans, accountability mechanisms, cost-of-living disparities, housing burden, wage gaps, and commute inequities across the **20 largest U.S. cities by population** (2024 Census estimates).

Anchored by **New York City's first-ever Preliminary Citywide Racial Equity Plan** (April 2026) and the inaugural **NYC True Cost of Living Measure**, this dataset enables city-by-city comparison of both plan quality and real-world racial disparities.

---

## 🗂 Dataset Files

| File | Format | Description |
|------|--------|-------------|
| [`data/racial_equity_20_cities.csv`](data/racial_equity_20_cities.csv) | CSV | Primary dataset — 20 cities × 40 columns |
| [`data/racial_equity_20_cities.tsv`](data/racial_equity_20_cities.tsv) | TSV | Tab-separated variant for shell/pandas use |
| [`docs/methodology.md`](docs/methodology.md) | Markdown | Equity score formula, metric definitions, limitations |
| [`docs/sources.md`](docs/sources.md) | Markdown | Full primary source list with URLs |
| [`docs/column_definitions.md`](docs/column_definitions.md) | Markdown | Field-by-field data dictionary |

---

## 🔑 Key Findings (April 2026)

- **Only 3 of 20 cities** (Chicago, Philadelphia, Seattle) have equity plans with *both* budget commitments *and* enforcement mechanisms
- **Dallas and Fort Worth** formally suspended equity plans in 2025 under federal executive orders (EOs 14173, 14218, 14151)
- **Los Angeles** defunded its Office of Race and Equity in FY2025–26; **San Diego** proposed eliminating its Department of Race & Equity
- NYC's True Cost of Living Measure found **62% of New Yorkers** cannot meet basic needs — with rates of 43.7% (white) vs. 77.6% (Hispanic)
- Black renters average **58% cost-burdened** across the 20 cities vs. ~41% for white renters
- Black workers spend an average of **19 extra minutes per week** commuting compared to white workers (Federal Reserve Philadelphia)
- The average equity score across all 20 cities is **35/100**

---

## 📊 Coverage

### Cities Included

| Rank | City | State | Equity Score | Plan Status |
|------|------|-------|:---:|---|
| 1 | New York City | NY | 73 | Comprehensive |
| 2 | Los Angeles | CA | 42 | Partial (office defunded) |
| 3 | Chicago | IL | 81 | Comprehensive |
| 4 | Houston | TX | 12 | None |
| 5 | Phoenix | AZ | 14 | None |
| 6 | Philadelphia | PA | 84 | Comprehensive |
| 7 | San Antonio | TX | 8 | None |
| 8 | San Diego | CA | 36 | Partial (dept. being eliminated) |
| 9 | Dallas | TX | 10 | Suspended |
| 10 | San José | CA | 44 | Partial |
| 11 | Austin | TX | 38 | Partial |
| 12 | Jacksonville | FL | 6 | None |
| 13 | Fort Worth | TX | 5 | Suspended |
| 14 | Columbus | OH | 34 | Partial |
| 15 | Charlotte | NC | 48 | Partial |
| 16 | Indianapolis | IN | 22 | Partial |
| 17 | Seattle | WA | 89 | Comprehensive |
| 18 | Denver | CO | 41 | Partial |
| 19 | Nashville | TN | 9 | None |
| 20 | Oklahoma City | OK | 8 | None |

### Metric Categories

| Category | Fields |
|----------|--------|
| **Accountability** | Equity plan existence, measurable goals, timelines, budget linkage, enforcement, equity office, annual reporting, composite score |
| **Poverty & Income** | Official poverty rate, Black/Latinx/White poverty rates, median household income by race, True COL gap |
| **Housing** | Median rent, Black/Latinx/White rent burden (%), homeownership rates, rent burden gap (pp) |
| **Wages** | Black/Latinx wage gap (¢ per $1 white), Black/White unemployment rates, unemployment gap ratio |
| **Commute** | Black/White average commute (min), commute gap (extra min/week) |
| **Qualitative** | Accountability gap descriptions, primary sources per city |

---

## ⚖️ Equity Score Methodology

The composite **Equity Score (0–100)** measures the *strength of accountability structures*, not outcomes:

| Component | Points | Criteria |
|-----------|:------:|----------|
| Plan existence & comprehensiveness | 25 | Citywide plan covering multiple agencies |
| Measurable goals | 10 | Quantifiable targets with baselines |
| Implementation timelines | 15 | Specific deadlines for goal completion |
| Budget commitments | 20 | Dedicated funding tied to equity goals |
| Enforcement mechanisms | 20 | External audits, penalties, or oversight bodies |
| Dedicated equity office | 5 | Standalone office or department |
| Annual public reporting | 5 | Required annual progress reports |
| **Total** | **100** | |

> **Important:** A high score means strong accountability commitments — not that disparities have been reduced. Cities with suspended plans receive partial credit only for elements in place before suspension.

### Plan Status Definitions

| Status | Definition |
|--------|------------|
| `Comprehensive` | Citywide plan covering multiple agencies with goals, strategies, and indicators |
| `Partial` | Plan exists but lacks one or more critical elements (budget, enforcement, or dedicated office) |
| `Suspended` | Plan was formally adopted but suspended or de-implemented (often citing federal executive orders) |
| `None` | No formal citywide racial equity plan |

---

## 📐 Disparity Metrics

| Metric | Definition | Source |
|--------|------------|--------|
| **Rent burden** | % of renters spending ≥30% of gross income on housing | ACS 2023 Table B25140 |
| **Wage gap** | Black workers' median earnings as cents per $1 earned by white workers | ACS 2023 Table B20017 |
| **Commute gap** | Extra minutes per week Black workers commute vs. white workers | Fed Reserve Philadelphia |
| **Unemployment gap** | Ratio of Black to white unemployment rates (2.0 = twice as high) | ACS 2023 |
| **True COL gap** | % of households below threshold needed to meet all basic needs | NYC official TCOL measure; proxy estimates elsewhere |

---

## 🏛 Primary Sources

| Source | URL |
|--------|-----|
| NYC Preliminary Citywide Racial Equity Plan (April 2026) | [nyc.gov](https://www.nyc.gov/assets/equity/downloads/pdf/FINAL_PUBLISH_Preliminary%20REP_4%206%2026.pdf) |
| NYC True Cost of Living Measure (April 2026) | [nyc.gov](https://www.nyc.gov/assets/equity/downloads/pdf/2026-NYC-TcoL-Report.pdf) |
| U.S. Census Bureau ACS 2023 1-Year Estimates | [data.census.gov](https://data.census.gov/) |
| Chicago CPD Racial Equity Action Plan (2024) | [chicagopolice.org](https://www.chicagopolice.org/wp-content/uploads/Chicago-Police-Departments-Equity-Action-Plan.pdf) |
| Philadelphia Budgeting for Racial Equity FY2024 | [phila.gov](https://www.phila.gov/media/20230301185113/budgeting-for-racial-equity-FY2024.pdf) |
| Seattle RSJI 2025–26 Budget | [seattle.gov](https://www.seattle.gov/documents/departments/financedepartment/2526proposedbudget/2526_rsji.pdf) |
| McKinsey — Mapping Road to Prosperity & Parity (2024) | [mckinsey.com](https://www.mckinsey.com/institute-for-economic-mobility/our-insights/mapping-the-road-to-prosperity-and-parity-for-black-and-latino-residents-across-america) |
| NLIHC Housing Gap Report 2025 | [nlihc.org](https://nlihc.org/sites/default/files/gap/2025/gap-report_2025_english.pdf) |
| Federal Reserve Philadelphia — Racial Commute Study | [philadelphiafed.org](https://www.philadelphiafed.org/) |
| Dallas equity plan suspension (Resolution 25-2552A) | Dallas City Council, August 2025 |
| San Diego equity dept. elimination | [inewsource.org](https://inewsource.org/2025/05/13/san-diego-budget-deficit-race-equity-cuts/) |

See [`docs/sources.md`](docs/sources.md) for per-city source citations.

---

## ⚠️ Data Limitations

1. **City vs. metro-level data** — Estimates derived from ACS 2023 city-level tables; may differ from state or metro figures
2. **Extrapolated fields** — Not all cities publish race-disaggregated data; some values extrapolated from regional ACS tables and adjusted for city cost context
3. **Scores reflect plan quality, not outcomes** — A score of 89 (Seattle) means strong accountability structures, not that disparities are resolved
4. **Federal rollback context** — EOs 14173, 14218, and 14151 (2025) altered equity programs between source publication dates and this dataset
5. **True COL gap** — Only NYC has an official TCOL measure; all other city values are proxy estimates

---

## 🔄 Versioning

This dataset follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version: structural changes (columns added/removed, methodology change)
- **MINOR** version: new cities or time periods added
- **PATCH** version: data corrections or source updates

See [CHANGELOG.md](CHANGELOG.md) for full version history.

---

## 🤝 Contributing

Corrections, updated city plans, and additional metrics are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

This dataset is released under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).  
You are free to share and adapt it for any purpose, including commercial, with attribution.

**Citation:**
```
Racial Equity Dataset: 20 Largest U.S. Cities (v1.0.0, April 2026).
Compiled from publicly available government reports, U.S. Census ACS 2023,
McKinsey, NLIHC, and Federal Reserve research.
GitHub: https://github.com/Trulove111/racial-equity-dataset
Dashboard: https://www.perplexity.ai/computer/a/racial-equity-dashboard-20-lar-E1EJiRZlSCyupQX84K_bqw
```

---

## 🔗 Related

- **Interactive Dashboard** — [perplexity.ai/computer/…](https://www.perplexity.ai/computer/a/racial-equity-dashboard-20-lar-E1EJiRZlSCyupQX84K_bqw)
- **Google Sheet with pivot tables** — [docs.google.com/spreadsheets/…](https://docs.google.com/spreadsheets/d/1pfLTMQv-s9mYtj94st0_vwqkSOAAJB3L/edit)
