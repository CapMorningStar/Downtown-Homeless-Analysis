"""
Utility functions, econometric calculators, KPI formatters, and mathematical routines.
Downtown San Diego Homeless Population Analysis - Task 9.1
"""

from typing import Dict, Any, Tuple
import math
from src.config import (
    BETA_0,
    BETA_1,
    BETA_2,
    STUDENT_T_CRITICAL_95,
    SIGMA_EPSILON,
    X_BAR,
    VAR_X,
)


def format_count(val: float, round_to_hundred: bool = False) -> str:
    """Format numeric counts with comma separators."""
    if val is None or math.isnan(val):
        return "N/A"
    if round_to_hundred:
        rounded = int(round(val / 100.0) * 100)
        return f"{rounded:,}"
    return f"{int(round(val)):,}"


def format_pct(val: float, include_sign: bool = True) -> str:
    """Format percentage values."""
    if val is None or math.isnan(val):
        return "N/A"
    sign = "+" if include_sign and val > 0 else ""
    return f"{sign}{val:.1f}%"


def calculate_county_estimate(
    downtown_count: float,
    post_ordinance: bool = True,
) -> Dict[str, Any]:
    """
    Calculate countywide unsheltered estimate using Assignment 8 Champion Policy Regime OLS:
        Y = beta_0 + beta_1 * X + beta_2 * D_post
    With exact Student's t 95% Prediction Interval.
    
    Enforces the 4 Public Communication Rules:
    1. Prohibits single-point precision display.
    2. Mandates rounding to nearest 100.
    3. Mandates reporting the 95% PI range.
    4. Mandates policy regime context disclosure.
    """
    d_post_val = 1.0 if post_ordinance else 0.0
    
    # Point prediction
    y_hat_raw = BETA_0 + (BETA_1 * downtown_count) + (BETA_2 * d_post_val)
    
    # Exact Prediction Standard Error calculation
    # SE_pred = sigma * sqrt(1 + 1/N + (X - X_bar)^2 / ((N - 1) * Var(X)))
    # N = 8 paired annual observations
    n_obs = 8
    leverage = (1.0 / n_obs) + ((downtown_count - X_BAR) ** 2) / ((n_obs - 1) * VAR_X)
    se_pred = SIGMA_EPSILON * math.sqrt(1.0 + leverage)
    
    # Margin of error under Student's t (df = 5, alpha = 0.05)
    margin_of_error = STUDENT_T_CRITICAL_95 * se_pred
    
    lower_raw = max(0.0, y_hat_raw - margin_of_error)
    upper_raw = y_hat_raw + margin_of_error
    
    # Rule 2: Rounding to nearest 100
    y_hat_rounded = int(round(y_hat_raw / 100.0) * 100)
    lower_rounded = int(round(lower_raw / 100.0) * 100)
    upper_rounded = int(round(upper_raw / 100.0) * 100)
    
    # Rule 4: Policy context
    policy_context = (
        "Active Camping Ordinance Enforcement (Post-July 2023 Regime)"
        if post_ordinance
        else "Pre-Ordinance / Non-Enforcement Baseline"
    )
    
    return {
        "raw_point_estimate": y_hat_raw,
        "raw_lower_95": lower_raw,
        "raw_upper_95": upper_raw,
        "rounded_point_estimate": y_hat_rounded,
        "rounded_lower_95": lower_rounded,
        "rounded_upper_95": upper_rounded,
        "public_display_text": f"{y_hat_rounded:,} [{lower_rounded:,} to {upper_rounded:,}]",
        "margin_of_error": margin_of_error,
        "se_pred": se_pred,
        "policy_context": policy_context,
        "is_post_ordinance": post_ordinance,
    }


def calculate_scenario_forecast(
    base_forecast: float,
    month_step: int,
    total_horizon: int = 12,
    target_pct: float = 0.0,
) -> float:
    """
    Calculate linear graduated policy scenario forecast for a given horizon month.
    target_pct: e.g. -0.24 for Optimistic, +0.26 for Pessimistic at month 12.
    """
    graduated_factor = 1.0 + (target_pct * (month_step / float(total_horizon)))
    return max(0.0, base_forecast * graduated_factor)
