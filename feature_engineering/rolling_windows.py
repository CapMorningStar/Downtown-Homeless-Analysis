"""
Rolling Window Statistics & Volatility Envelopes Module
Computes 3-month, 6-month, and 12-month moving averages, dispersion metrics,
Bollinger volatility envelopes, and normalized z-scores over lookback history.
"""

import numpy as np
import pandas as pd


def generate_rolling_features(
    df: pd.DataFrame,
    target_col: str = "downtown_actual_adjusted_count",
) -> pd.DataFrame:
    """
    Generates 15 rolling statistics and volatility envelopes.
    All windows operate strictly over past observations (y.shift(1)) to prevent leakage.
    """
    y_hist = df[target_col].shift(1)

    # 3-Month Window
    roll_3 = y_hist.rolling(window=3, min_periods=1)
    mean_3m = roll_3.mean().round(2)
    std_3m = roll_3.std().fillna(0.0).round(2)
    min_3m = roll_3.min().round(2)
    max_3m = roll_3.max().round(2)
    safe_mean_3m = mean_3m.replace(0, np.nan)
    cv_3m = (std_3m / safe_mean_3m).fillna(0.0).round(4)

    # 6-Month Window
    roll_6 = y_hist.rolling(window=6, min_periods=1)
    mean_6m = roll_6.mean().round(2)
    std_6m = roll_6.std().fillna(0.0).round(2)
    min_6m = roll_6.min().round(2)
    max_6m = roll_6.max().round(2)
    safe_mean_6m = mean_6m.replace(0, np.nan)
    cv_6m = (std_6m / safe_mean_6m).fillna(0.0).round(4)

    # 12-Month Window & Envelopes
    roll_12 = y_hist.rolling(window=12, min_periods=1)
    mean_12m = roll_12.mean().round(2)
    std_12m = roll_12.std().fillna(0.0).round(2)
    bollinger_upper = (mean_12m + 2.0 * std_12m).round(2)
    bollinger_lower = np.maximum(0.0, mean_12m - 2.0 * std_12m).round(2)

    safe_std_12m = std_12m.replace(0, 1.0)
    z_score_12m = ((y_hist - mean_12m) / safe_std_12m).fillna(0.0).round(4)

    res = pd.DataFrame(
        {
            "rolling_mean_3m_adjusted": mean_3m,
            "rolling_std_3m_adjusted": std_3m,
            "rolling_min_3m_adjusted": min_3m,
            "rolling_max_3m_adjusted": max_3m,
            "rolling_cv_3m_adjusted": cv_3m,
            "rolling_mean_6m_adjusted": mean_6m,
            "rolling_std_6m_adjusted": std_6m,
            "rolling_min_6m_adjusted": min_6m,
            "rolling_max_6m_adjusted": max_6m,
            "rolling_cv_6m_adjusted": cv_6m,
            "rolling_mean_12m_adjusted": mean_12m,
            "rolling_std_12m_adjusted": std_12m,
            "bollinger_upper_12m_adjusted": bollinger_upper,
            "bollinger_lower_12m_adjusted": bollinger_lower,
            "z_score_12m_adjusted": z_score_12m,
        },
        index=df.index,
    )

    return res
