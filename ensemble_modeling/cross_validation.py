"""
Time-Series Cross-Validation Harness & Econometric Evaluation Metrics
Provides expanding-window splits across annual holdout folds (2021–2025)
and computes standardized accuracy metrics: MAE, RMSE, MAPE, MDA, and R².
"""

from typing import Dict, Generator, List, Tuple
import numpy as np
import pandas as pd


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_hist_last: float = None) -> Dict[str, float]:
    """
    Computes standard econometric accuracy metrics.
    """
    y_t = np.asarray(y_true, dtype=float)
    y_p = np.asarray(y_pred, dtype=float)

    # Filter out uncounted zero months for MAPE computation
    valid_mask = (y_t > 0)
    mae = np.mean(np.abs(y_t - y_p))
    rmse = np.sqrt(np.mean((y_t - y_p) ** 2))

    if np.any(valid_mask):
        mape = np.mean(np.abs((y_t[valid_mask] - y_p[valid_mask]) / y_t[valid_mask])) * 100.0
    else:
        mape = 0.0

    ss_res = np.sum((y_t - y_p) ** 2)
    ss_tot = np.sum((y_t - np.mean(y_t)) ** 2)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

    # Mean Directional Accuracy
    if len(y_t) > 1:
        dir_true = np.sign(np.diff(y_t))
        dir_pred = np.sign(np.diff(y_p))
        mda = np.mean(dir_true == dir_pred) * 100.0
    else:
        mda = 50.0

    return {
        "mae": round(float(mae), 2),
        "rmse": round(float(rmse), 2),
        "mape": round(float(mape), 2),
        "mda": round(float(mda), 2),
        "r2": round(float(r2), 4),
    }


class TimeSeriesExpandingCV:
    """
    Generates 5 annual expanding-window time-series CV splits:
    Fold 1: Train 2018–2020 (36M) -> Test 2021 (12M)
    Fold 2: Train 2018–2021 (48M) -> Test 2022 (12M)
    Fold 3: Train 2018–2022 (60M) -> Test 2023 (12M)
    Fold 4: Train 2018–2023 (72M) -> Test 2024 (12M)
    Fold 5: Train 2018–2024 (84M) -> Test 2025 (12M)
    """

    TEST_YEARS = [2021, 2022, 2023, 2024, 2025]

    def __init__(self, start_train_year: int = 2018):
        self.start_train_year = start_train_year

    def split(self, df: pd.DataFrame, date_col: str = "date") -> Generator[Tuple[int, np.ndarray, np.ndarray, int], None, None]:
        dates = pd.to_datetime(df[date_col])
        years = dates.dt.year

        for fold_idx, test_year in enumerate(self.TEST_YEARS, 1):
            train_mask = (years >= self.start_train_year) & (years < test_year)
            test_mask = (years == test_year)

            train_indices = np.where(train_mask)[0]
            test_indices = np.where(test_mask)[0]

            if len(train_indices) == 0 or len(test_indices) == 0:
                continue

            yield fold_idx, train_indices, test_indices, test_year
