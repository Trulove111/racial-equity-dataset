# Methodology

## Equity Score Formula

The composite **Equity Score (0–100)** is a structured index of accountability quality. It measures the *strength of commitments and mechanisms* cities have adopted — not whether disparities have narrowed.

| Component | Max Points | What earns full credit |
|-----------|:----------:|------------------------|
| Plan existence & comprehensiveness | 25 | Citywide plan covering multiple agencies with goals, strategies, and measurable indicators |
| Measurable goals | 10 | Quantifiable targets with defined baselines and benchmark years |
| Implementation timelines | 15 | Specific deadlines assigned to individual goals or strategies |
| Budget commitments | 20 | Dedicated appropriations or line items explicitly tied to equity goals |
| Enforcement mechanisms | 20 | External audits, penalty structures, or independent oversight bodies with binding authority |
| Dedicated equity office | 5 | Standalone department or office with permanent staff |
| Annual public reporting | 5 | Legally or policy-mandated annual public progress reports |
| **Total** | **100** | |

### Scoring notes
- Cities with **Suspended** plans receive partial credit for elements that were in place before suspension, scaled by how recently the plan operated
- Cities with **Partial** plans are scored across all components individually — a city may score 48 despite "Partial" status if it scores well on most elements
- **Budget commitment** is the single hardest element: it requires explicit dollar amounts tied to equity goals, not general departmental budgets that overlap incidentally with equity work
- **Enforcement** requires *external* accountability — internal agency reviews do not qualify

---

## Plan Status Classification

| Status | Definition | Examples (2026) |
|--------|------------|-----------------|
| `Comprehensive` | Citywide plan covering ≥10 agencies, measurable goals, strategies, and indicators across multiple policy domains | NYC, Chicago, Philadelphia, Seattle |
| `Partial` | Formal plan exists but is missing ≥1 of: budget linkage, enforcement mechanism, or dedicated equity office | LA, San José, Austin, Charlotte |
| `Suspended` | Plan was formally adopted but subsequently suspended or de-implemented, typically citing federal executive orders | Dallas, Fort Worth |
| `None` | No formal citywide racial equity plan | Houston, Phoenix, San Antonio, Jacksonville, Nashville, Oklahoma City |

---

## Disparity Metrics

### Rent Burden
- **Definition:** Percentage of renter households spending 30% or more of gross monthly income on housing costs (rent + utilities)
- **Source:** U.S. Census Bureau ACS 2023 1-Year Estimates, Table B25140 series (A–I for racial subgroups)
- **Notes:** The 30% threshold is the federal standard for "cost-burdened." Values above 50% qualify as "severely cost-burdened" — this dataset uses the standard 30% threshold for cross-city comparability

### Wage Gap
- **Definition:** Black (or Latinx) workers' median annual earnings expressed as cents per dollar earned by white (non-Hispanic) workers
- **Formula:** `(Black median earnings / White median earnings) × 100`
- **Interpretation:** 63¢ means Black workers earn $63 for every $100 earned by white workers
- **Source:** ACS 2023 Table B20017, race-specific variants

### Commute Gap
- **Definition:** Extra minutes per week that Black workers spend commuting compared to white workers in the same metro
- **Formula:** `(Black avg one-way commute − White avg one-way commute) × 10 trips/week`
- **Source:** Federal Reserve Bank of Philadelphia racial commute disparity analysis
- **Notes:** Commute time is measured as average one-way travel time to work. 10 trips/week assumes 5 round trips

### Unemployment Gap
- **Definition:** Ratio of Black unemployment rate to white unemployment rate
- **Formula:** `Black unemployment rate / White unemployment rate`
- **Interpretation:** 2.0 means Black workers are unemployed at twice the rate of white workers
- **Source:** ACS 2023 Table B23001 and S2301

### Homeownership Gap
- **Definition:** Percentage point difference between white and Black homeownership rates
- **Formula:** `White homeownership % − Black homeownership %`
- **Source:** ACS 2023 Table B25003 series

### True Cost of Living Gap
- **Definition:** Percentage of households in a city below the threshold income needed to meet all basic needs without public assistance
- **Methodology:** Derived from a market-basket approach covering housing, food, childcare, healthcare, transportation, and taxes
- **Availability:** Only NYC has an official, published TCOL measure (NYC Office of Equity, April 2026). For all other cities, this field reflects proxy estimates derived from ACS income distribution data cross-referenced with McKinsey cost-of-living research. Treat non-NYC values as illustrative, not official
- **Source (NYC):** NYC True Cost of Living Report, April 2026

---

## Data Collection Process

1. **Plan documentation** — Each city's equity plan (or documented absence of one) was verified through official city government websites, city council legislation records, and local journalism as of April 2026

2. **Accountability flags** — Binary flags (has/lacks) for each accountability element were assigned based on plan text review. Flags required *explicit, documented evidence* — plans that mentioned goals without attached timelines were coded `hasTimelines: false`

3. **Demographic data** — All race-disaggregated statistics drawn from ACS 2023 1-Year Estimates. For cities where the 1-year ACS sample was insufficient for race-specific estimates, 5-year estimates (2019–2023) were used and noted

4. **Cross-referencing** — City-specific values were cross-checked against published city equity reports, McKinsey city-level analyses, and NLIHC state-level data. Where sources disagreed, the more conservative (less extreme) estimate was used

5. **Federal rollback tracking** — Plan suspensions and office eliminations tracked through city council records, local news, and advocacy organization databases through April 2026

---

## Limitations

| Limitation | Impact | Mitigation |
|-----------|--------|------------|
| City vs. metro-level ACS data | City boundaries exclude suburban populations; some disparities may be understated | Values use city-limit geographies consistently |
| Not all cities publish race-disaggregated data | ~4 cities required regional extrapolation | Extrapolated values noted in `Sources` column |
| Scores reflect plan quality, not outcomes | High score ≠ reduced disparity | README and docs explicitly flag this distinction |
| Federal executive order effects | EOs 14173/14218/14151 (2025) altered programs after some source dates | Suspension status captures known changes through April 2026 |
| TCOL proxy estimates | Non-NYC TCOL values lack official validation | Field notes "proxy estimate" in methodology column |
| Static snapshot | Data reflects April 2026; city plans and budgets change | Version history tracks updates; see CHANGELOG |
