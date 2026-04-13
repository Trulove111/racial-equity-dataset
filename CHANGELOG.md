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

## [Unreleased]

### Planned
- Update Dallas/Fort Worth entries when plan reinstatement status is clarified
- Add FY2026–27 budget data as cities finalize budgets (Q3 2026)
- Add `blackMedianWealth` and `whiteMedianWealth` fields when city-level data available
- Expand to 30 largest cities (cities 21–30 by population)
