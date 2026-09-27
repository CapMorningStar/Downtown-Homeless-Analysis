"""
Unit tests for econometric calculations and policy regime OLS model.
Downtown San Diego Homeless Population Analysis - Task 9.1
"""

import pytest
from src.utils import calculate_county_estimate, calculate_scenario_forecast


def test_county_calculator_baseline_dec2025():
    """Verify Dec 2025 baseline downtown count (~985.38) under post-ordinance regime."""
    res = calculate_county_estimate(downtown_count=985.38, post_ordinance=True)
    
    # Mathematical expectation:
    # 4513.26 + (0.1859 * 985.38) + 1225.04 = 5921.48
    assert round(res["raw_point_estimate"], 1) == 5921.5
    assert res["rounded_point_estimate"] == 5900
    
    # Verify 95% prediction interval sanity
    assert res["raw_lower_95"] < res["raw_point_estimate"]
    assert res["raw_upper_95"] > res["raw_point_estimate"]
    
    # Verify Rule 2 & 3 public text format
    assert res["public_display_text"].startswith("5,900 [")
    assert "to" in res["public_display_text"]


def test_county_calculator_pre_ordinance():
    """Verify pre-ordinance regime (D_post = 0)."""
    res = calculate_county_estimate(downtown_count=985.38, post_ordinance=False)
    
    # 4513.26 + (0.1859 * 985.38) = 4696.44
    assert round(res["raw_point_estimate"], 1) == 4696.4
    assert res["rounded_point_estimate"] == 4700


def test_county_calculator_margin_of_error():
    """Verify margin of error is approximately +/- 2,050 individuals (+/- 35%)."""
    res = calculate_county_estimate(downtown_count=1245.50, post_ordinance=True)
    assert 2000 <= res["margin_of_error"] <= 2250


def test_scenario_forecast_graduated():
    """Verify linear graduated scenario calculations at horizons 1, 6, and 12."""
    base = 1000.0
    
    # Optimistic (-24% at month 12)
    m1 = calculate_scenario_forecast(base, month_step=1, total_horizon=12, target_pct=-0.24)
    m6 = calculate_scenario_forecast(base, month_step=6, total_horizon=12, target_pct=-0.24)
    m12 = calculate_scenario_forecast(base, month_step=12, total_horizon=12, target_pct=-0.24)
    
    assert m1 == pytest.approx(1000.0 * (1 - 0.02), abs=0.1)
    assert m6 == pytest.approx(1000.0 * (1 - 0.12), abs=0.1)
    assert m12 == pytest.approx(760.0, abs=0.1)
    
    # Monotonicity check
    assert m12 < m6 < m1 < base
