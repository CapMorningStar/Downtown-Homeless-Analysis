"""
Data Quality & Contract Validator
Performs exhaustive automated checks on the multi-source dataset:
- Temporal continuity & monotonicity (108 monthly observations)
- Column null thresholds & data typing
- Empirical domain boundary constraints
- Generates structured validation audit report
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd

logger = logging.getLogger(__name__)


class DataQualityValidator:
    """
    Validates data integrity, continuity, and physical bounds of the multi-source matrix.
    """

    EXPECTED_MONTHS = 108
    START_DATE = "2017-01-01"
    END_DATE = "2025-12-01"

    NUMERIC_BOUNDS = {
        "downtown_actual_adjusted_count": (400.0, 2500.0),
        "downtown_actual_raw_count": (400.0, 2500.0),
        "weather_temp_mean_f": (45.0, 85.0),
        "weather_temp_max_f": (55.0, 110.0),
        "weather_temp_min_f": (32.0, 75.0),
        "weather_precip_total_in": (0.0, 15.0),
        "weather_rainy_days_count": (0, 31),
        "weather_extreme_heat_days_count": (0, 31),
        "events_padres_home_games_count": (0, 22),
        "events_federal_holidays_count": (0, 4),
        "econ_unemployment_rate_pct": (2.0, 30.0),
        "econ_rent_zori_downtown_92101": (1500.0, 4000.0),
        "shelter_total_capacity": (1000, 3500),
        "service_311_total_requests_count": (0, 10000),
        "service_311_encampment_requests_count": (0, 6000),
    }

    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = data_path or Path("data/MultiSource_Master_Monthly.csv")
        self.logger = logging.getLogger(self.__class__.__name__)

    def load_data(self) -> pd.DataFrame:
        if not self.data_path.exists():
            raise FileNotFoundError(f"Dataset file does not exist: {self.data_path}")
        return pd.read_csv(self.data_path)

    def validate_temporal_continuity(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        errors = []
        if "date" not in df.columns:
            return False, ["Missing 'date' column in dataset."]

        dates = pd.to_datetime(df["date"])
        expected_range = pd.date_range(self.START_DATE, self.END_DATE, freq="MS")

        if len(dates) != self.EXPECTED_MONTHS:
            errors.append(f"Expected {self.EXPECTED_MONTHS} months, found {len(dates)} rows.")

        missing_dates = set(expected_range) - set(dates)
        if missing_dates:
            errors.append(f"Missing {len(missing_dates)} dates: {sorted(list(missing_dates))[:3]}...")

        if not dates.is_monotonic_increasing:
            errors.append("Dates are not strictly monotonically increasing.")

        return len(errors) == 0, errors

    def validate_nulls(self, df: pd.DataFrame) -> Tuple[bool, Dict[str, int]]:
        null_counts = df.isnull().sum().to_dict()
        critical_nulls = {k: v for k, v in null_counts.items() if v > 0}
        passed = (len(critical_nulls) == 0)
        return passed, critical_nulls

    def validate_domain_bounds(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        bound_violations = []
        for col, (low, high) in self.NUMERIC_BOUNDS.items():
            if col not in df.columns:
                bound_violations.append(f"Column '{col}' expected in bounds checks but not found.")
                continue

            vals = df[col].dropna()
            # For ground-truth counts, filter to positive counted months
            if col.startswith("downtown_actual_"):
                vals = vals[vals > 0]

            if vals.empty:
                continue

            min_val = vals.min()
            max_val = vals.max()

            if min_val < low:
                bound_violations.append(f"'{col}' min value {min_val} below lower bound {low}.")
            if max_val > high:
                bound_violations.append(f"'{col}' max value {max_val} above upper bound {high}.")

        return len(bound_violations) == 0, bound_violations

    def run_full_audit(self) -> Dict:
        """
        Executes full validation suite and returns structured audit results.
        """
        df = self.load_data()
        temp_ok, temp_errs = self.validate_temporal_continuity(df)
        null_ok, null_dict = self.validate_nulls(df)
        bound_ok, bound_errs = self.validate_domain_bounds(df)

        all_passed = temp_ok and null_ok and bound_ok

        audit_results = {
            "status": "PASSED" if all_passed else "FAILED",
            "row_count": len(df),
            "column_count": len(df.columns),
            "date_range": [df["date"].min(), df["date"].max()],
            "temporal_continuity_ok": temp_ok,
            "temporal_errors": temp_errs,
            "null_check_ok": null_ok,
            "columns_with_nulls": null_dict,
            "domain_bounds_ok": bound_ok,
            "domain_bound_violations": bound_errs,
            "columns": list(df.columns),
        }

        if all_passed:
            self.logger.info("All data quality checks PASSED (108 months, 0 nulls, all bounds respected).")
        else:
            self.logger.warning("Data quality checks reported issues: %s", audit_results)

        return audit_results
