# Changelog

All notable changes to this dataset will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-04-12

### Added
- Initial dataset release: 20 largest U.S. cities by 2024 Census population
- 40 columns spanning accountability, poverty, housing, wages, commute, and qualitative fields
- CSV and TSV formats in `data/`
- Full methodology documentation in `docs/methodology.md`
- Column definitions data dictionary in `docs/column_definitions.md`
- Per-city primary source citations in `docs/sources.md`
- Equity Score (0–100) composite accountability index

### Data sources
- NYC Preliminary Citywide Racial Equity Plan (April 7, 2026) — first-ever REP
- NYC True Cost of Living Measure (April 2026) — inaugural official measure
- U.S. Census Bureau ACS 2023 1-Year Estimates
- City-specific equity plans, budgets, and council records
- McKinsey Institute for Black Economic Mobility (2024)
- NLIHC Housing Gap Report 2025
- Federal Reserve Bank of Philadelphia commute analysis

### Notable findings at v1.0.0
- Only 3/20 cities have equity plans with both budget commitments and enforcement (Chicago, Philadelphia, Seattle)
- 2 cities suspended plans under federal executive orders (Dallas, Fort Worth)
- 2 cities defunding/eliminating equity offices (LA, San Diego)
- Average equity score across 20 cities: 35/100
- Average Black rent burden: 58% vs. ~41% white

---

## [1.1.0] — 2026-04-12

### Added
- **`scripts/validate_csv.py`** — standalone Python validator (no external dependencies beyond stdlib) covering 8 check categories:
  - *Schema drift* — hard fail on missing columns; warning on unexpected extra columns; warning on column order changes vs. the locked 40-column schema
  - *Type errors* — enforces lowercase `true`/`false` for boolean fields; validates integers, floats, and enum values (`Plan Status`, `State`)
  - *Range violations* — domain-specific hard bounds per column (e.g. equity score 0–100, rent burden 20–85%, wage gap 30–100¢)
  - *Soft range warnings* — typical expected ranges that flag unusual values for source review without failing the build
  - *Missing values* — hard fail on any of 37 required fields left blank; 3 optional fields (`Plan Year`, `Agency Count`, `True COL Gap`) allowed to be empty
  - *Outliers* — IQR ×3 fence per numeric column; values statistically extreme relative to the other 19 cities trigger a warning
  - *Cross-field logic* — consistency checks across related fields: `Plan Status=None` ↔ `Has Equity Plan=false`; unemployment gap ratio ≈ Black÷White rates; rent burden gap ≈ Black%−White%; budget commitment requires an equity plan
  - *Row count & duplicates* — hard fail if fewer than 20 rows; warning if more than 20 without a CHANGELOG update; hard fail on duplicate `City+State` pairs
- **`.github/workflows/validate-data.yml`** — GitHub Actions CI workflow:
  - Triggers on push and PR when `data/*.csv`, `scripts/validate_csv.py`, or the workflow file itself changes
  - Detects which CSV files changed per commit for targeted diff reporting
  - Runs full validation with `scripts/validate_csv.py` and inline schema drift check
  - Posts a formatted validation report as a PR comment (updates existing bot comment on re-push instead of creating duplicates)
  - Uploads full report as a 30-day downloadable artifact keyed to the commit SHA
  - Prints actionable fix suggestions per failure type on job failure
  - Cancels stale in-progress runs on the same branch automatically
- **CLI flags** on `scripts/validate_csv.py`: `--warn-only` (exit 0 despite failures, for draft PRs) and `--no-outliers` (skip IQR check when intentionally adding a verified extreme value)
- **`.github/ISSUE_TEMPLATE/`** — two structured issue templates added in v1.0.0, now documented here for completeness

### Changed
- No data values changed in this release
- No column schema changes — this is a tooling-only minor bump

### Validation baseline (v1.1.0)
- Validator confirmed clean against current dataset: **0 failures, 1 expected warning**
- The 1 warning is Chicago's Black/White unemployment ratio of 3.21× (IQR outlier) — verified correct against ACS 2023 and documented in `docs/sources.md`

---

## [1.2.0] — 2026-04-12

### Added
- **`analysis/equity_regression_analysis.ipynb`** — Jupyter notebook running OLS regression with HC3 robust standard errors to test whether equity plan comprehensiveness predicts racial outcome gaps across all 20 cities. Covers 9 sections:
  - *Load & Prepare* — feature engineering: `plan_ordinal` (0–3 ordinal encoding of plan status), `is_comprehensive` dummy, `accountability_count` (sum of 7 binary plan flags), `poverty_gap` (Black−White poverty rate difference), `rent_burden_gap` (Black−White rent burden difference), `log_median_income`
  - *EDA* — summary statistics by plan status group, Pearson correlation matrix heatmap, scatter plots with OLS fit lines, boxplots by plan status for all four outcome variables
  - *Regression models (8 total)* — 3 predictor specifications × 4 outcomes using `statsmodels.formula.api.ols` with HC3 heteroskedasticity-robust standard errors:
    - Outcomes: Black Poverty Rate, Black Rent Burden %, Poverty Gap (B−W), Rent Burden Gap (B−W)
    - M1a/M1b/M1c: equity_score continuous, plan_ordinal ordinal, equity_score + log_median_income controlled
    - M2a/M2b/M2c: same predictors on rent burden outcomes
    - M3a/M3b: poverty gap and rent burden gap as outcomes
  - *Diagnostics* — residuals vs. fitted, Q-Q normality plot, Cook's distance influence plot, Breusch-Pagan heteroskedasticity test, Variance Inflation Factor (VIF) for multicollinearity
  - *Bootstrap CIs* — 5,000-resample percentile-method confidence intervals on all slope coefficients
  - *Coefficient plot* — forest plot of all 8 models with HC3 CI error bars side-by-side for comparison
  - *Accountability element breakdown* — point-biserial correlations between each of the 7 binary plan accountability flags (budget commitment, enforcement mechanism, timeline, agency accountability, community oversight, housing focus, anti-displacement) and each outcome variable
  - *Results summary table* — consolidated β, SE, p-value, and 95% CI for all models
  - *Interpretation & caveats* — endogeneity (cities with better outcomes may have more capacity for plans), confounding (income, history, demographics), n=20 power limitations, plan age lag (older plans may show stronger effects)
- Notebook auto-loads CSV from `../data/racial_equity_20_cities.csv` relative to `analysis/`, falling back to the GitHub raw URL if not found locally — works out-of-the-box in Google Colab with no additional setup
- Notebook available on Google Drive: https://drive.google.com/file/d/154z-RtiReftj9iRbRPpFosyrlUlbL_KQ/view?usp=drivesdk

### Changed
- No data values or schema changed in this release
- No validator changes — this is a pure analysis addition

### Dependencies (notebook only)
- `pandas`, `numpy`, `matplotlib`, `seaborn`, `statsmodels`, `scipy` — all available in standard Colab/conda environments
- `scikit-learn` used only for `StandardScaler` in EDA section

---

## [Unreleased]

### Planned
- Update Dallas/Fort Worth entries when plan reinstatement status is clarified
- Add FY2026–27 budget data as cities finalize budgets (Q3 2026)
- Add `blackMedianWealth` and `whiteMedianWealth` fields when city-level data available
- Expand to 30 largest cities (cities 21–30 by population)
- Add notebook for time-series analysis once longitudinal data is available
