# Column Definitions

Data dictionary for `data/racial_equity_20_cities.csv` (40 columns).

---

## Identifiers

| Column | Type | Description |
|--------|------|-------------|
| `Rank` | integer | Population rank among 20 cities (1 = largest, per 2024 Census estimates) |
| `City` | string | City name |
| `State` | string | Two-letter state abbreviation |

---

## Accountability & Plan Quality

| Column | Type | Values | Description |
|--------|------|--------|-------------|
| `Equity Score (0-100)` | integer | 0–100 | Composite accountability index (see [methodology.md](methodology.md)) |
| `Plan Status` | string | Comprehensive, Partial, Suspended, None | Classification of racial equity plan quality |
| `Plan Year` | integer | Year or blank | Year the most recent equity plan was formally adopted |
| `Has Equity Plan` | boolean | true / false | Whether any formal citywide racial equity plan exists |
| `Measurable Goals` | boolean | true / false | Plan includes quantifiable targets with defined baselines |
| `Has Timelines` | boolean | true / false | Goals have specific implementation deadlines |
| `Has Budget Commitment` | boolean | true / false | Dedicated funding explicitly tied to equity goals |
| `Has Enforcement` | boolean | true / false | External audit, penalty, or independent oversight mechanism exists |
| `Equity Office Exists` | boolean | true / false | Standalone equity office or department with permanent staff |
| `Annual Reporting` | boolean | true / false | Annual public progress reports required by policy or law |
| `Agency Count` | integer | Number or blank | Number of city agencies with documented equity commitments in the plan |

---

## Poverty & Income

| Column | Type | Unit | Description |
|--------|------|------|-------------|
| `Official Poverty Rate (%)` | float | % | Share of all residents below the Federal Poverty Level (ACS 2023 S1701) |
| `Black Poverty Rate (%)` | float | % | Share of Black residents below FPL |
| `Latinx Poverty Rate (%)` | float | % | Share of Latinx/Hispanic residents below FPL |
| `White Poverty Rate (%)` | float | % | Share of white (non-Hispanic) residents below FPL |
| `Median Household Income ($)` | integer | USD | Overall city median household income (ACS 2023 B19013) |
| `Black Median Income ($)` | integer | USD | Median household income for Black households |
| `Latinx Median Income ($)` | integer | USD | Median household income for Latinx/Hispanic households |
| `White Median Income ($)` | integer | USD | Median household income for white (non-Hispanic) households |
| `True COL Gap (% below)` | float | % | % of households below the True Cost of Living threshold. **NYC only** has an official measure; other cities use proxy estimates — treat non-NYC values as illustrative |

---

## Housing & Rent Burden

| Column | Type | Unit | Description |
|--------|------|------|-------------|
| `Median Rent ($/mo)` | integer | USD/month | Median gross rent, all units (ACS 2023 B25064) |
| `Black Rent Burden (%)` | float | % | Share of Black renters spending ≥30% of income on housing (ACS 2023 B25140B) |
| `Latinx Rent Burden (%)` | float | % | Share of Latinx renters spending ≥30% of income on housing (ACS 2023 B25140I) |
| `White Rent Burden (%)` | float | % | Share of white renters spending ≥30% of income on housing (ACS 2023 B25140A) |
| `Black Homeownership (%)` | float | % | Black homeownership rate (ACS 2023 B25003B) |
| `White Homeownership (%)` | float | % | White homeownership rate (ACS 2023 B25003A) |
| `Rent Burden Gap (pp Black-White)` | float | percentage points | Black rent burden % minus White rent burden % |

---

## Wages & Employment

| Column | Type | Unit | Description |
|--------|------|------|-------------|
| `Black Wage Gap (cents per White $)` | float | ¢ per $1 | Black workers' median annual earnings as a share of white workers'. E.g., 63 = Black workers earn $0.63 per $1.00 white workers earn |
| `Latinx Wage Gap (cents per White $)` | float | ¢ per $1 | Latinx workers' median annual earnings as a share of white workers' |
| `Black Unemployment Rate (%)` | float | % | Black unemployment rate (ACS 2023 S2301) |
| `White Unemployment Rate (%)` | float | % | White (non-Hispanic) unemployment rate |
| `Unemployment Gap (ratio)` | float | ratio | Black unemployment rate ÷ white unemployment rate. 2.0 = twice as high |

---

## Commute Disparity

| Column | Type | Unit | Description |
|--------|------|------|-------------|
| `Black Avg Commute (min)` | float | minutes | Average one-way commute time for Black workers |
| `White Avg Commute (min)` | float | minutes | Average one-way commute time for white workers |
| `Commute Gap (min/week)` | float | min/week | Extra minutes per week Black workers spend commuting vs. white workers. Formula: `(Black avg − White avg) × 10 trips/week` |

---

## Qualitative

| Column | Type | Description |
|--------|------|-------------|
| `Accountability Gaps` | string | Pipe-separated (`\|`) list of qualitative assessments describing what is structurally missing from each city's equity plan (e.g., "No budget linkage", "No external enforcement", "Plan suspended under federal EO") |
| `Sources` | string | Pipe-separated (`\|`) list of primary sources used for each city's data |

---

## Boolean Encoding

All `true/false` columns use lowercase string literals in the CSV:

```
true  → element is present and documented
false → element is absent or undocumented
```

When loading in pandas:
```python
import pandas as pd
df = pd.read_csv('data/racial_equity_20_cities.csv')
bool_cols = ['Has Equity Plan', 'Measurable Goals', 'Has Timelines',
             'Has Budget Commitment', 'Has Enforcement',
             'Equity Office Exists', 'Annual Reporting']
df[bool_cols] = df[bool_cols].map({'true': True, 'false': False})
```
