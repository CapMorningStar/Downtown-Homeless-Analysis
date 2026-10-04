"""
Autoregressive & Momentum Feature Engineering Module
Computes multi-scale lags, velocity differences, growth rates, acceleration,
and structural component ratios with strict backward lookback shifts to prevent lookahead leakage.
"""

import numpy as np
import pandas as pd


def generate_autoregressive_features(
    df: pd.DataFrame,
    target_col: str = "downtown_actual_adjusted_count",
    raw_col: str = "downtown_actual_raw_count",
    individual_col: str = "downtown_actual_individual_count",
    tent_col: str = "downtown_actual_tent_count",
    vehicle_col: str = "downtown_actual_vehicle_count",
    shelter_capacity_col: str = "shelter_total_capacity",
) -> pd.DataFrame:
    """
    Generates 15 autoregressive, differenced momentum, and ratio features.
    All features are strictly lagged (t-1 or greater) relative to observation t.
    """
    y = df[target_col]
    raw = df[raw_col]
    indiv = df[individual_col] if individual_col in df.columns else pd.Series(0, index=df.index)
    tent = df[tent_col] if tent_col in df.columns else pd.Series(0, index=df.index)
    veh = df[vehicle_col] if vehicle_col in df.columns else pd.Series(0, index=df.index)
    shelter = df[shelter_capacity_col] if shelter_capacity_col in df.columns else pd.Series(2000, index=df.index)

    # 1. Multi-scale lags of adjusted counts
    lag_1m = y.shift(1)
    lag_2m = y.shift(2)
    lag_3m = y.shift(3)
    lag_6m = y.shift(6)
    lag_12m = y.shift(12)

    # 2. Raw count lags
    lag_1m_raw = raw.shift(1)
    lag_12m_raw = raw.shift(12)

    # 3. Differences and Momentum
    diff_1m = lag_1m - lag_2m
    diff_12m = lag_1m - y.shift(13)
    acceleration_1m = diff_1m - (lag_2m - lag_3m)

    # Percentage growth rates
    safe_lag_2m = lag_2m.replace(0, np.nan)
    safe_lag_13m = y.shift(13).replace(0, np.nan)
    growth_1m_pct = ((lag_1m - lag_2m) / safe_lag_2m * 100.0).round(2)
    growth_12m_pct = ((lag_1m - y.shift(13)) / safe_lag_13m * 100.0).round(2)

    # 4. Component ratios (evaluated at t-1)
    indiv_lag1 = indiv.shift(1).replace(0, 1.0)
    ratio_tent = (tent.shift(1) / indiv_lag1).round(4)
    ratio_vehicle = (veh.shift(1) / indiv_lag1).round(4)

    safe_y_lag1 = lag_1m.replace(0, 1.0)
    ratio_shelter = (shelter.shift(1) / safe_y_lag1).round(4)

    res = pd.DataFrame(
        {
            "lag_1m_adjusted": lag_1m,
            "lag_2m_adjusted": lag_2m,
            "lag_3m_adjusted": lag_3m,
            "lag_6m_adjusted": lag_6m,
            "lag_12m_adjusted": lag_12m,
            "lag_1m_raw": lag_1m_raw,
            "lag_12m_raw": lag_12m_raw,
            "diff_1m_adjusted": diff_1m,
            "diff_12m_adjusted": diff_12m,
            "acceleration_1m_adjusted": acceleration_1m,
            "growth_rate_1m_pct": growth_1m_pct,
            "growth_rate_12m_pct": growth_12m_pct,
            "ratio_tent_to_individual_lag1": ratio_tent,
            "ratio_vehicle_to_individual_lag1": ratio_vehicle,
            "ratio_shelter_to_unsheltered_lag1": ratio_shelter,
        },
        index=df.index,
    )

    return res
