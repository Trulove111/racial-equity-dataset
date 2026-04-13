#!/usr/bin/env python3
"""
validate_csv.py — Racial Equity Dataset CSV Validator
======================================================
Checks every CSV file in data/ for:

  1. SCHEMA DRIFT      — unexpected / missing columns vs. the locked schema
  2. TYPE ERRORS       — numeric fields that aren't numeric, booleans that
                         aren't true/false, enum fields with unknown values
  3. RANGE VIOLATIONS  — values outside domain-specific acceptable bounds
  4. MISSING VALUES    — required fields that are blank or null
  5. OUTLIERS          — values >3 IQR-fences from the column distribution
                         (flagged as warnings, not hard failures)
  6. ROW COUNT DRIFT   — fewer rows than baseline (hard fail) or more than
                         expected without a CHANGELOG bump (warning)
  7. DUPLICATE ROWS    — same City+State appearing more than once
  8. CROSS-FIELD LOGIC — sanity checks across related columns
                         (e.g. Unemployment Gap = Black / White rate)

Exit codes
----------
  0  all checks passed (warnings printed but ignored)
  1  one or more hard failures
"""

import csv
import sys
import math
import pathlib
import argparse
import statistics
from collections import defaultdict

# ── Schema definition ─────────────────────────────────────────────────────────

# All 40 expected column names in order
EXPECTED_COLUMNS = [
    "Rank",
    "City",
    "State",
    "Equity Score (0-100)",
    "Plan Status",
    "Plan Year",
    "Has Equity Plan",
    "Measurable Goals",
    "Has Timelines",
    "Has Budget Commitment",
    "Has Enforcement",
    "Equity Office Exists",
    "Annual Reporting",
    "Agency Count",
    "Official Poverty Rate (%)",
    "Black Poverty Rate (%)",
    "Latinx Poverty Rate (%)",
    "White Poverty Rate (%)",
    "Median Household Income ($)",
    "Black Median Income ($)",
    "Latinx Median Income ($)",
    "White Median Income ($)",
    "True COL Gap (% below)",
    "Median Rent ($/mo)",
    "Black Rent Burden (%)",
    "Latinx Rent Burden (%)",
    "White Rent Burden (%)",
    "Black Homeownership (%)",
    "White Homeownership (%)",
    "Rent Burden Gap (pp Black-White)",
    "Black Wage Gap (cents per White $)",
    "Latinx Wage Gap (cents per White $)",
    "Black Unemployment Rate (%)",
    "White Unemployment Rate (%)",
    "Unemployment Gap (ratio)",
    "Black Avg Commute (min)",
    "White Avg Commute (min)",
    "Commute Gap (min/week)",
    "Accountability Gaps",
    "Sources",
]

# Required (non-nullable) columns — empty string is a hard failure
REQUIRED_COLUMNS = [
    "Rank", "City", "State", "Equity Score (0-100)", "Plan Status",
    "Has Equity Plan", "Measurable Goals", "Has Timelines",
    "Has Budget Commitment", "Has Enforcement", "Equity Office Exists",
    "Annual Reporting",
    "Official Poverty Rate (%)", "Black Poverty Rate (%)",
    "Latinx Poverty Rate (%)", "White Poverty Rate (%)",
    "Median Household Income ($)", "Black Median Income ($)",
    "Latinx Median Income ($)", "White Median Income ($)",
    "Median Rent ($/mo)",
    "Black Rent Burden (%)", "Latinx Rent Burden (%)", "White Rent Burden (%)",
    "Black Homeownership (%)", "White Homeownership (%)",
    "Rent Burden Gap (pp Black-White)",
    "Black Wage Gap (cents per White $)", "Latinx Wage Gap (cents per White $)",
    "Black Unemployment Rate (%)", "White Unemployment Rate (%)",
    "Unemployment Gap (ratio)",
    "Black Avg Commute (min)", "White Avg Commute (min)",
    "Commute Gap (min/week)",
    "Accountability Gaps", "Sources",
]

# Optional (nullable) columns — empty string is allowed
OPTIONAL_COLUMNS = ["Plan Year", "Agency Count", "True COL Gap (% below)"]

# Integer columns
INT_COLUMNS = [
    "Rank", "Equity Score (0-100)", "Plan Year", "Agency Count",
    "Median Household Income ($)", "Black Median Income ($)",
    "Latinx Median Income ($)", "White Median Income ($)",
    "Median Rent ($/mo)",
]

# Float columns
FLOAT_COLUMNS = [
    "Official Poverty Rate (%)", "Black Poverty Rate (%)",
    "Latinx Poverty Rate (%)", "White Poverty Rate (%)",
    "True COL Gap (% below)",
    "Black Rent Burden (%)", "Latinx Rent Burden (%)", "White Rent Burden (%)",
    "Black Homeownership (%)", "White Homeownership (%)",
    "Rent Burden Gap (pp Black-White)",
    "Black Wage Gap (cents per White $)", "Latinx Wage Gap (cents per White $)",
    "Black Unemployment Rate (%)", "White Unemployment Rate (%)",
    "Unemployment Gap (ratio)",
    "Black Avg Commute (min)", "White Avg Commute (min)",
    "Commute Gap (min/week)",
]

# Boolean columns — must be exactly "true" or "false"
BOOL_COLUMNS = [
    "Has Equity Plan", "Measurable Goals", "Has Timelines",
    "Has Budget Commitment", "Has Enforcement",
    "Equity Office Exists", "Annual Reporting",
]

# Enum columns
ENUM_COLUMNS = {
    "Plan Status": {"Comprehensive", "Partial", "Suspended", "None"},
    "State": {
        "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN",
        "IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV",
        "NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN",
        "TX","UT","VT","VA","WA","WV","WI","WY","DC",
    },
}

# Domain-specific hard bounds (inclusive): [min, max]
# Values outside these are hard failures
HARD_BOUNDS = {
    "Rank":                              [1, 100],
    "Equity Score (0-100)":             [0, 100],
    "Plan Year":                         [2000, 2030],
    "Agency Count":                      [0, 500],
    "Official Poverty Rate (%)":         [0, 60],
    "Black Poverty Rate (%)":            [0, 70],
    "Latinx Poverty Rate (%)":           [0, 70],
    "White Poverty Rate (%)":            [0, 50],
    "Median Household Income ($)":       [10000, 250000],
    "Black Median Income ($)":           [10000, 200000],
    "Latinx Median Income ($)":          [10000, 200000],
    "White Median Income ($)":           [10000, 250000],
    "True COL Gap (% below)":            [0, 100],
    "Median Rent ($/mo)":                [300, 6000],
    "Black Rent Burden (%)":             [20, 85],
    "Latinx Rent Burden (%)":            [20, 85],
    "White Rent Burden (%)":             [10, 75],
    "Black Homeownership (%)":           [5, 75],
    "White Homeownership (%)":           [20, 90],
    "Rent Burden Gap (pp Black-White)":  [-10, 50],
    "Black Wage Gap (cents per White $)":[30, 100],
    "Latinx Wage Gap (cents per White $)":[30, 100],
    "Black Unemployment Rate (%)":       [0, 30],
    "White Unemployment Rate (%)":       [0, 20],
    "Unemployment Gap (ratio)":          [0.5, 8],
    "Black Avg Commute (min)":           [10, 90],
    "White Avg Commute (min)":           [10, 90],
    "Commute Gap (min/week)":            [-20, 100],
}

# Soft warning bounds — values outside these trigger a warning, not a failure
SOFT_BOUNDS = {
    "Equity Score (0-100)":             [0, 100],
    "Black Poverty Rate (%)":            [5, 55],
    "Black Rent Burden (%)":             [30, 80],
    "Black Wage Gap (cents per White $)":[45, 95],
    "Unemployment Gap (ratio)":          [1.0, 6.0],
    "Commute Gap (min/week)":            [-5, 60],
}

# Minimum expected row count (hard fail if fewer)
MIN_ROW_COUNT = 20
# Expected row count (warn if more without CHANGELOG note)
EXPECTED_ROW_COUNT = 20
# IQR fence multiplier for outlier detection
IQR_FENCE = 3.0


# ── Helpers ───────────────────────────────────────────────────────────────────

class Issue:
    FAIL = "FAIL"
    WARN = "WARN"
    INFO = "INFO"

    def __init__(self, level, check, row, column, message):
        self.level = level
        self.check = check
        self.row = row          # 1-based data row number (0 = file-level)
        self.column = column
        self.message = message

    def __str__(self):
        loc = f"row {self.row}" if self.row else "file"
        col = f" [{self.column}]" if self.column else ""
        return f"  [{self.level}] {self.check}{col} @ {loc}: {self.message}"


def try_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def try_int(value):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None


def iqr_fences(values, k=IQR_FENCE):
    """Return (lower_fence, upper_fence) using k * IQR rule."""
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n < 4:
        return None, None
    q1 = sorted_vals[n // 4]
    q3 = sorted_vals[(3 * n) // 4]
    iqr = q3 - q1
    if iqr == 0:
        return None, None
    return q1 - k * iqr, q3 + k * iqr


# ── Validator ─────────────────────────────────────────────────────────────────

def validate_file(path: pathlib.Path) -> list[Issue]:
    issues = []

    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        actual_columns = reader.fieldnames or []
        rows = list(reader)

    # ── 1. Schema drift ───────────────────────────────────────────────────────
    expected_set = set(EXPECTED_COLUMNS)
    actual_set = set(actual_columns)

    missing_cols = expected_set - actual_set
    extra_cols = actual_set - expected_set

    if missing_cols:
        issues.append(Issue(
            Issue.FAIL, "SCHEMA_DRIFT", 0, None,
            f"Missing columns: {sorted(missing_cols)}"
        ))
    if extra_cols:
        issues.append(Issue(
            Issue.WARN, "SCHEMA_DRIFT", 0, None,
            f"Unexpected extra columns: {sorted(extra_cols)} — add to schema or remove"
        ))

    # Check column ORDER only if all expected columns are present
    if not missing_cols:
        present = [c for c in actual_columns if c in expected_set]
        expected_ordered = [c for c in EXPECTED_COLUMNS if c in actual_set]
        if present != expected_ordered:
            issues.append(Issue(
                Issue.WARN, "SCHEMA_DRIFT", 0, None,
                "Column order differs from schema — consider reordering for consistency"
            ))

    # ── 2. Row count ──────────────────────────────────────────────────────────
    n_rows = len(rows)
    if n_rows < MIN_ROW_COUNT:
        issues.append(Issue(
            Issue.FAIL, "ROW_COUNT", 0, None,
            f"Only {n_rows} data rows — minimum is {MIN_ROW_COUNT}. "
            f"Were rows accidentally deleted?"
        ))
    elif n_rows > EXPECTED_ROW_COUNT:
        issues.append(Issue(
            Issue.WARN, "ROW_COUNT", 0, None,
            f"{n_rows} rows found (expected {EXPECTED_ROW_COUNT}). "
            f"If cities were added, bump MINOR version in CHANGELOG."
        ))

    # ── 3. Duplicate City+State ───────────────────────────────────────────────
    seen_cities = defaultdict(list)
    for i, row in enumerate(rows, 1):
        key = (row.get("City", "").strip(), row.get("State", "").strip())
        seen_cities[key].append(i)
    for key, row_nums in seen_cities.items():
        if len(row_nums) > 1:
            issues.append(Issue(
                Issue.FAIL, "DUPLICATE_ROW", row_nums[1], "City",
                f"'{key[0]}, {key[1]}' appears in rows {row_nums}"
            ))

    # ── Per-row checks ────────────────────────────────────────────────────────
    # Collect numeric values per column for outlier analysis
    col_numeric_values = defaultdict(list)  # col -> list of (row_num, float)

    for i, row in enumerate(rows, 1):
        bg = LIGHT_GRAY if i % 2 == 0 else WHITE  # (unused — leftover from template)

        # 4. Required / missing values
        for col in REQUIRED_COLUMNS:
            if col not in actual_set:
                continue
            val = row.get(col, "").strip()
            if val == "":
                issues.append(Issue(
                    Issue.FAIL, "MISSING_VALUE", i, col,
                    f"Required field is empty"
                ))

        # 5. Boolean type check
        for col in BOOL_COLUMNS:
            if col not in actual_set:
                continue
            val = row.get(col, "").strip().lower()
            if val not in ("true", "false", ""):
                issues.append(Issue(
                    Issue.FAIL, "TYPE_ERROR", i, col,
                    f"Expected 'true' or 'false', got '{row.get(col, '')}'"
                ))

        # 6. Enum checks
        for col, valid_values in ENUM_COLUMNS.items():
            if col not in actual_set:
                continue
            val = row.get(col, "").strip()
            if val and val not in valid_values:
                issues.append(Issue(
                    Issue.FAIL, "TYPE_ERROR", i, col,
                    f"Unknown value '{val}' — allowed: {sorted(valid_values)}"
                ))

        # 7. Integer type checks
        for col in INT_COLUMNS:
            if col not in actual_set:
                continue
            val = row.get(col, "").strip()
            if val == "":
                continue  # handled by missing-value check
            if try_int(val) is None:
                issues.append(Issue(
                    Issue.FAIL, "TYPE_ERROR", i, col,
                    f"Expected integer, got '{val}'"
                ))

        # 8. Float type checks
        for col in FLOAT_COLUMNS:
            if col not in actual_set:
                continue
            val = row.get(col, "").strip()
            if val == "":
                continue
            fv = try_float(val)
            if fv is None:
                issues.append(Issue(
                    Issue.FAIL, "TYPE_ERROR", i, col,
                    f"Expected number, got '{val}'"
                ))
            else:
                col_numeric_values[col].append((i, fv))

        # Collect int columns for outlier analysis too
        for col in INT_COLUMNS:
            if col not in actual_set:
                continue
            val = row.get(col, "").strip()
            fv = try_float(val)
            if fv is not None:
                col_numeric_values[col].append((i, fv))

        # 9. Hard range bounds
        all_numeric_cols = list(HARD_BOUNDS.keys())
        for col in all_numeric_cols:
            if col not in actual_set:
                continue
            val = row.get(col, "").strip()
            if val == "":
                continue
            fv = try_float(val)
            if fv is None:
                continue
            lo, hi = HARD_BOUNDS[col]
            if not (lo <= fv <= hi):
                issues.append(Issue(
                    Issue.FAIL, "RANGE_VIOLATION", i, col,
                    f"Value {fv} is outside allowed range [{lo}, {hi}]"
                ))

        # 10. Soft range warnings
        for col, (lo, hi) in SOFT_BOUNDS.items():
            if col not in actual_set:
                continue
            val = row.get(col, "").strip()
            if val == "":
                continue
            fv = try_float(val)
            if fv is None:
                continue
            if not (lo <= fv <= hi):
                issues.append(Issue(
                    Issue.WARN, "SOFT_RANGE", i, col,
                    f"Value {fv} is outside typical range [{lo}, {hi}] — verify source"
                ))

        # 11. Cross-field logic checks
        city = row.get("City", "").strip()

        # If Has Equity Plan is false, Plan Year should be empty
        has_plan = row.get("Has Equity Plan", "").strip().lower()
        plan_year = row.get("Plan Year", "").strip()
        if has_plan == "false" and plan_year:
            issues.append(Issue(
                Issue.WARN, "CROSS_FIELD", i, "Plan Year",
                f"{city}: Has Equity Plan=false but Plan Year='{plan_year}' is set"
            ))

        # If Plan Status is None, Has Equity Plan should be false
        plan_status = row.get("Plan Status", "").strip()
        if plan_status == "None" and has_plan == "true":
            issues.append(Issue(
                Issue.FAIL, "CROSS_FIELD", i, "Plan Status",
                f"{city}: Plan Status='None' but Has Equity Plan='true'"
            ))

        # Comprehensive plans should have measurable goals
        goals = row.get("Measurable Goals", "").strip().lower()
        if plan_status == "Comprehensive" and goals == "false":
            issues.append(Issue(
                Issue.WARN, "CROSS_FIELD", i, "Measurable Goals",
                f"{city}: Plan Status='Comprehensive' but Measurable Goals='false' — verify"
            ))

        # Budget commitment requires an equity plan
        budget = row.get("Has Budget Commitment", "").strip().lower()
        if budget == "true" and has_plan == "false":
            issues.append(Issue(
                Issue.FAIL, "CROSS_FIELD", i, "Has Budget Commitment",
                f"{city}: Has Budget Commitment=true but Has Equity Plan=false"
            ))

        # Unemployment gap should be approximately Black rate / White rate
        black_unemp = try_float(row.get("Black Unemployment Rate (%)", ""))
        white_unemp = try_float(row.get("White Unemployment Rate (%)", ""))
        gap_ratio = try_float(row.get("Unemployment Gap (ratio)", ""))
        if black_unemp and white_unemp and white_unemp > 0 and gap_ratio:
            expected_ratio = round(black_unemp / white_unemp, 1)
            if abs(expected_ratio - gap_ratio) > 0.3:
                issues.append(Issue(
                    Issue.WARN, "CROSS_FIELD", i, "Unemployment Gap (ratio)",
                    f"{city}: Gap ratio={gap_ratio} but Black/White={expected_ratio:.1f} "
                    f"(Black={black_unemp}%, White={white_unemp}%)"
                ))

        # Rent burden gap should be approximately Black - White
        black_rb = try_float(row.get("Black Rent Burden (%)", ""))
        white_rb = try_float(row.get("White Rent Burden (%)", ""))
        rb_gap = try_float(row.get("Rent Burden Gap (pp Black-White)", ""))
        if black_rb is not None and white_rb is not None and rb_gap is not None:
            expected_gap = round(black_rb - white_rb, 1)
            if abs(expected_gap - rb_gap) > 2.0:
                issues.append(Issue(
                    Issue.WARN, "CROSS_FIELD", i, "Rent Burden Gap (pp Black-White)",
                    f"{city}: Gap={rb_gap}pp but Black({black_rb}%) - White({white_rb}%) = {expected_gap}pp"
                ))

        # Black median income should be less than white (almost universally)
        black_inc = try_float(row.get("Black Median Income ($)", ""))
        white_inc = try_float(row.get("White Median Income ($)", ""))
        if black_inc and white_inc and black_inc > white_inc * 1.1:
            issues.append(Issue(
                Issue.WARN, "CROSS_FIELD", i, "Black Median Income ($)",
                f"{city}: Black income (${black_inc:,.0f}) exceeds White income (${white_inc:,.0f}) by >10% — verify"
            ))

        # Equity score 0 should not have Comprehensive status
        score = try_int(row.get("Equity Score (0-100)", ""))
        if score is not None and score < 20 and plan_status == "Comprehensive":
            issues.append(Issue(
                Issue.FAIL, "CROSS_FIELD", i, "Equity Score (0-100)",
                f"{city}: Score={score} but Plan Status='Comprehensive' — inconsistent"
            ))

    # ── 12. Outlier detection (IQR method) ────────────────────────────────────
    OUTLIER_SKIP = {"Rank", "Plan Year", "Agency Count"}  # skip structural cols
    for col, vals in col_numeric_values.items():
        if col in OUTLIER_SKIP or len(vals) < 5:
            continue
        numeric_only = [v for _, v in vals]
        lower, upper = iqr_fences(numeric_only)
        if lower is None:
            continue
        for row_num, fv in vals:
            if fv < lower or fv > upper:
                issues.append(Issue(
                    Issue.WARN, "OUTLIER", row_num, col,
                    f"Value {fv} is an outlier (IQR fence: [{lower:.1f}, {upper:.1f}]) — verify source"
                ))

    return issues


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Validate racial equity dataset CSV files"
    )
    parser.add_argument(
        "files", nargs="*",
        help="CSV files to validate (default: all files in data/)"
    )
    parser.add_argument(
        "--warn-only", action="store_true",
        help="Exit 0 even if hard failures found (useful for PRs in draft)"
    )
    parser.add_argument(
        "--no-outliers", action="store_true",
        help="Skip outlier detection (useful when intentionally adding extreme values)"
    )
    args = parser.parse_args()

    repo_root = pathlib.Path(__file__).parent.parent
    if args.files:
        csv_files = [pathlib.Path(f) for f in args.files]
    else:
        csv_files = sorted((repo_root / "data").glob("*.csv"))

    if not csv_files:
        print("No CSV files found to validate.")
        sys.exit(0)

    total_failures = 0
    total_warnings = 0

    for csv_path in csv_files:
        print(f"\n{'='*60}")
        print(f"Validating: {csv_path.name}")
        print(f"{'='*60}")

        if not csv_path.exists():
            print(f"  [FAIL] File not found: {csv_path}")
            total_failures += 1
            continue

        issues = validate_file(csv_path)

        if args.no_outliers:
            issues = [i for i in issues if i.check != "OUTLIER"]

        failures = [i for i in issues if i.level == Issue.FAIL]
        warnings = [i for i in issues if i.level == Issue.WARN]
        infos    = [i for i in issues if i.level == Issue.INFO]

        if failures:
            print(f"\n  ❌ {len(failures)} FAILURE(S):")
            for issue in failures:
                print(issue)

        if warnings:
            print(f"\n  ⚠️  {len(warnings)} WARNING(S):")
            for issue in warnings:
                print(issue)

        if infos:
            for issue in infos:
                print(issue)

        if not failures and not warnings:
            print("  ✅ All checks passed.")
        elif not failures:
            print(f"\n  ✅ No failures. {len(warnings)} warning(s) noted.")

        total_failures += len(failures)
        total_warnings += len(warnings)

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"SUMMARY: {total_failures} failure(s), {total_warnings} warning(s)")
    print(f"{'='*60}\n")

    if total_failures > 0:
        if args.warn_only:
            print("--warn-only set: exiting 0 despite failures.")
            sys.exit(0)
        sys.exit(1)

    sys.exit(0)


# Remove accidental leftover from template paste
LIGHT_GRAY = ""
WHITE = ""

if __name__ == "__main__":
    main()
