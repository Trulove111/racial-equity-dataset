# Contributing

Contributions that improve accuracy, add missing data, or extend coverage are welcome.

## Types of Contributions

### Data Corrections
If you find an error in an existing value:
1. Open an issue with the title format: `[Data Correction] City Name — Field Name`
2. Include the current value, the correct value, and a link to the primary source

### New City Plans or Policy Updates
When a city adopts, updates, or suspends an equity plan:
1. Open an issue titled: `[Plan Update] City Name — Status Change`
2. Include the effective date, new status, and source link (city council record, official announcement, or credible news coverage)

### Source Additions
To add a stronger or more recent source for an existing field:
1. Open a pull request updating `docs/sources.md`
2. Update the `Sources` column in `data/racial_equity_20_cities.csv` for the affected city

### New Metrics
For proposals to add columns:
1. Open an issue describing the metric, its definition, and national data availability
2. Metrics must be available for ≥15 of the 20 cities to be added to the main dataset

## Data Standards

- All numeric values must cite a primary source (government data, Census, peer-reviewed)
- Race/ethnicity categories follow ACS conventions: Black or African American, Hispanic or Latino (any race), White (non-Hispanic)
- Boolean fields (`true`/`false`) require explicit documented evidence — absence of evidence → `false`
- For fields where data is unavailable for a city, use an empty string (not zero, not N/A)

## Version Bumping

| Change type | Version bump |
|-------------|-------------|
| Add or remove columns, change scoring methodology | Major (x.0.0) |
| Add new cities or time periods | Minor (1.x.0) |
| Correct existing values, update sources | Patch (1.0.x) |

## Code of Conduct

This dataset documents racial disparities. Contributions should be made in good faith to improve accuracy and usefulness for researchers, journalists, and advocates working on racial equity. Data should not be altered to minimize or obscure documented disparities.
