"""
Temporal & Cyclical Feature Engineering Module
Transforms standard date timestamps into cyclical harmonics, linear trend indices,
and policy event clocks without lookahead leakage.
"""

import numpy as np
import pandas as pd


def generate_temporal_features(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """
    Generates 9 temporal features from the date index:
    - temporal_month
    - temporal_quarter
    - temporal_year
    - temporal_sin_month
    - temporal_cos_month
    - temporal_trend_idx
    - temporal_days_since_covid_shock
    - temporal_days_since_methodology_post2020
    - temporal_days_since_camping_ban
    """
    dt_series = pd.to_datetime(df[date_col])

    month = dt_series.dt.month
    quarter = dt_series.dt.quarter
    year = dt_series.dt.year

    # Cyclical trigonometric transforms (period = 12)
    sin_month = np.sin(2 * np.pi * month / 12.0)
    cos_month = np.cos(2 * np.pi * month / 12.0)

    # Monotonic trend counter
    trend_idx = np.arange(len(df))

    # Policy clocks (days elapsed)
    covid_date = pd.Timestamp("2020-03-01")
    post2020_date = pd.Timestamp("2020-01-01")
    camping_ban_date = pd.Timestamp("2023-07-01")

    days_since_covid = np.maximum(0, (dt_series - covid_date).dt.days)
    days_since_post2020 = np.maximum(0, (dt_series - post2020_date).dt.days)
    days_since_camping_ban = np.maximum(0, (dt_series - camping_ban_date).dt.days)

    res = pd.DataFrame(
        {
            "temporal_month": month,
            "temporal_quarter": quarter,
            "temporal_year": year,
            "temporal_sin_month": np.round(sin_month, 4),
            "temporal_cos_month": np.round(cos_month, 4),
            "temporal_trend_idx": trend_idx,
            "temporal_days_since_covid_shock": days_since_covid,
            "temporal_days_since_methodology_post2020": days_since_post2020,
            "temporal_days_since_camping_ban": days_since_camping_ban,
        },
        index=df.index,
    )

    return res
