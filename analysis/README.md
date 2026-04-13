# Analysis

This folder contains statistical analysis notebooks for the 20-city racial equity dataset.

## Notebooks

### `equity_regression_analysis.ipynb`

OLS regression analysis testing whether equity plan comprehensiveness predicts racial outcome gaps across the 20 largest U.S. cities.

**Research questions:**
1. Does a higher equity plan score (0–100) predict lower Black poverty rates?
2. Does plan comprehensiveness predict lower Black rent burden?
3. Do cities with more accountability elements show smaller Black–White poverty and rent burden gaps?

**Outcomes modeled:**
| Variable | Description |
|---|---|
| `black_poverty_rate` | % Black residents below federal poverty line (ACS 2023) |
| `black_rent_burden` | % Black renter households paying >30% income on rent |
| `poverty_gap` | Black poverty rate − White poverty rate (percentage points) |
| `rent_burden_gap` | Black rent burden − White rent burden (percentage points) |

**Predictors:**
| Variable | Type | Description |
|---|---|---|
| `equity_score` | Continuous 0–100 | Composite accountability index |
| `plan_ordinal` | Ordinal 0–3 | None=0, Partial=1, Comprehensive=2, Suspended=3 |
| `is_comprehensive` | Dummy | 1 if Plan Status = Comprehensive |
| `accountability_count` | Count 0–7 | Sum of 7 binary accountability flags |
| `log_median_income` | Continuous | log(citywide median household income) |

**Models (8 total):** 3 predictor specifications × 4 outcomes using `statsmodels` OLS with HC3 robust standard errors.

**Sections:**
1. Load & Prepare Data
2. Exploratory Data Analysis
3. Regression Models
4. Diagnostics (residuals, Q-Q, Cook's distance, Breusch-Pagan, VIF)
5. Bootstrap Confidence Intervals (5,000 resamples)
6. Coefficient Plot
7. Accountability Element Breakdown (point-biserial correlations)
8. Results Summary Table
9. Interpretation & Caveats

**Dependencies:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `statsmodels`, `scipy`, `scikit-learn`

**Run in Google Colab:**  
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Trulove111/racial-equity-dataset/blob/main/analysis/equity_regression_analysis.ipynb)

The notebook auto-loads the dataset from `../data/racial_equity_20_cities.csv` relative to this folder, or falls back to the GitHub raw URL automatically.

**Also available on Google Drive:** https://drive.google.com/file/d/154z-RtiReftj9iRbRPpFosyrlUlbL_KQ/view?usp=drivesdk

---

## Caveats

- **n=20** — All regression results should be interpreted with caution given the small sample. Effect sizes and confidence intervals are illustrative, not definitive.
- **Endogeneity** — Cities with better racial outcomes may have more institutional capacity to develop equity plans, reversing the causal direction.
- **Confounding** — Median income, historical segregation, housing market structure, and regional politics all correlate with both plan adoption and outcomes.
- **Plan age lag** — Plans adopted more recently may not yet show measurable effects in 2023 ACS data.
- **Equity score construction** — The composite score reflects our coding methodology; results are sensitive to weighting choices.
