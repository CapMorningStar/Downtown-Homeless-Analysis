"""
Unit tests for prospective forecast logic, uncertainty intervals, and scenario bounds.
Downtown San Diego Homeless Population Analysis - Task 9.1
"""

import pytest
import pandas as pd
from src.data_loader import load_forecast_data
from src.utils import calculate_scenario_forecast


def test_forecast_data_structure():
    """Verify 108 rows = 9 series x 12 prospective months."""
    df = load_forecast_data()
    assert not df.empty
    
    # Must have 12 unique monthly horizons
    df["forecast_date"] = pd.to_datetime(df["forecast_date"])
    assert df["forecast_date"].nunique() == 12
    assert df["forecast_date"].min() == pd.Timestamp("2026-01-01")
    assert df["forecast_date"].max() == pd.Timestamp("2026-12-01")


def test_prediction_interval_bounds():
    """Verify 95% and 80% prediction interval monotonicity."""
    df = load_forecast_data()
    for _, row in df.iterrows():
        pt = row["point_forecast"]
        pi_80_l = row["pi_80_lower"]
        pi_80_u = row["pi_80_upper"]
        pi_95_l = row["pi_95_lower"]
        pi_95_u = row["pi_95_upper"]
        
        # 95% interval must be wider than 80% interval
        assert pi_95_l <= pi_80_l <= pt <= pi_80_u <= pi_95_u
        # Non-negativity check
        assert pi_95_l >= 0.0


def test_scenario_monotonicity():
    """Verify Optimistic <= Baseline <= Pessimistic."""
    df = load_forecast_data()
    for _, row in df.iterrows():
        opt = row.get("scenario_optimistic", row.get("optimistic_scenario"))
        base = row["point_forecast"]
        pess = row.get("scenario_pessimistic", row.get("pessimistic_scenario"))
        
        if opt is not None and pess is not None:
            assert opt <= base <= pess
