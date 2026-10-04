"""
Statistical Quality Control Chart Surveillance (Engine 1)
Implements:
1. Shewhart Control Chart with dynamic rolling center line and 2σ / 3σ action limits
2. Two-sided Tabular Cumulative Sum (CUSUM) for rapid detection of small, persistent mean drifts
"""

from typing import Dict, Optional, Tuple
import numpy as np
import pandas as pd


class ShewhartControlChart:
    """
    Shewhart individual measurement (X-mR / I-MR) control chart with rolling parameters.
    """

    def __init__(
        self,
        window: int = 12,
        min_periods: int = 6,
        warning_sigma: float = 2.0,
        critical_sigma: float = 3.0,
    ):
        self.window = window
        self.min_periods = min_periods
        self.warning_sigma = warning_sigma
        self.critical_sigma = critical_sigma

    def fit_detect(self, series: pd.Series, dates: Optional[pd.Series] = None) -> pd.DataFrame:
        """
        Computes rolling center line, sigma limits, and detects boundary violations.
        """
        y = series.astype(float).values
        n = len(y)

        roll_mean = np.copy(pd.Series(y).rolling(window=self.window, min_periods=self.min_periods).mean().values)
        roll_std = np.copy(pd.Series(y).rolling(window=self.window, min_periods=self.min_periods).std().values)

        # Fallback for initial periods where window < min_periods
        initial_mean = float(np.nanmean(y[: self.min_periods]))
        initial_std = float(np.nanstd(y[: self.min_periods]))
        if initial_std < 1e-4:
            initial_std = 1.0

        for i in range(n):
            if np.isnan(roll_mean[i]):
                roll_mean[i] = initial_mean
            if np.isnan(roll_std[i]) or roll_std[i] < 1e-4:
                roll_std[i] = initial_std

        ucl_warning = roll_mean + self.warning_sigma * roll_std
        lcl_warning = np.maximum(0.0, roll_mean - self.warning_sigma * roll_std)
        ucl_critical = roll_mean + self.critical_sigma * roll_std
        lcl_critical = np.maximum(0.0, roll_mean - self.critical_sigma * roll_std)

        z_scores = np.abs(y - roll_mean) / np.maximum(1e-4, roll_std)

        status = []
        is_anomaly = []
        severity = []

        for i in range(n):
            val = y[i]
            if val > ucl_critical[i]:
                status.append("CRITICAL_HIGH")
                is_anomaly.append(True)
                severity.append("CRITICAL")
            elif val < lcl_critical[i]:
                status.append("CRITICAL_LOW")
                is_anomaly.append(True)
                severity.append("CRITICAL")
            elif val > ucl_warning[i]:
                status.append("WARNING_HIGH")
                is_anomaly.append(True)
                severity.append("WARNING")
            elif val < lcl_warning[i]:
                status.append("WARNING_LOW")
                is_anomaly.append(True)
                severity.append("WARNING")
            else:
                status.append("NORMAL")
                is_anomaly.append(False)
                severity.append("NONE")

        res_df = pd.DataFrame({
            "value": y,
            "center_line": np.round(roll_mean, 2),
            "rolling_std": np.round(roll_std, 2),
            "lcl_warning": np.round(lcl_warning, 2),
            "ucl_warning": np.round(ucl_warning, 2),
            "lcl_critical": np.round(lcl_critical, 2),
            "ucl_critical": np.round(ucl_critical, 2),
            "shewhart_z_score": np.round(z_scores, 2),
            "shewhart_status": status,
            "shewhart_is_anomaly": is_anomaly,
            "shewhart_severity": severity,
        })

        if dates is not None:
            res_df.insert(0, "date", pd.to_datetime(dates).values)

        return res_df


class TabularCUSUM:
    """
    Two-Sided Tabular Cumulative Sum (CUSUM) Quality Control Detector.
    Accumulates standardized residuals above/below allowance slack parameter k.
    """

    def __init__(
        self,
        slack_k: float = 0.5,
        threshold_h: float = 4.0,
        window: int = 12,
        min_periods: int = 6,
        reset_on_alarm: bool = True,
    ):
        self.slack_k = slack_k
        self.threshold_h = threshold_h
        self.window = window
        self.min_periods = min_periods
        self.reset_on_alarm = reset_on_alarm

    def fit_detect(self, series: pd.Series, dates: Optional[pd.Series] = None) -> pd.DataFrame:
        """
        Executes positive and negative CUSUM accumulations.
        """
        y = series.astype(float).values
        n = len(y)

        roll_mean = np.copy(pd.Series(y).rolling(window=self.window, min_periods=self.min_periods).mean().values)
        roll_std = np.copy(pd.Series(y).rolling(window=self.window, min_periods=self.min_periods).std().values)

        init_m = float(np.nanmean(y[: self.min_periods]))
        init_s = float(np.nanstd(y[: self.min_periods]))
        if init_s < 1e-4:
            init_s = 1.0

        for i in range(n):
            if np.isnan(roll_mean[i]):
                roll_mean[i] = init_m
            if np.isnan(roll_std[i]) or roll_std[i] < 1e-4:
                roll_std[i] = init_s

        z = (y - roll_mean) / roll_std

        s_pos = np.zeros(n, dtype=float)
        s_neg = np.zeros(n, dtype=float)
        is_anomaly = np.zeros(n, dtype=bool)
        cusum_status = []

        for t in range(1, n):
            s_pos[t] = max(0.0, s_pos[t - 1] + z[t] - self.slack_k)
            s_neg[t] = max(0.0, s_neg[t - 1] - z[t] - self.slack_k)

            up = s_pos[t] > self.threshold_h
            down = s_neg[t] > self.threshold_h

            if up and down:
                cusum_status.append("DUAL_DRIFT")
                is_anomaly[t] = True
                if self.reset_on_alarm:
                    s_pos[t] = 0.0
                    s_neg[t] = 0.0
            elif up:
                cusum_status.append("UPWARD_DRIFT")
                is_anomaly[t] = True
                if self.reset_on_alarm:
                    s_pos[t] = 0.0
            elif down:
                cusum_status.append("DOWNWARD_DRIFT")
                is_anomaly[t] = True
                if self.reset_on_alarm:
                    s_neg[t] = 0.0
            else:
                cusum_status.append("NORMAL")

        cusum_status.insert(0, "NORMAL")

        res_df = pd.DataFrame({
            "cusum_z": np.round(z, 2),
            "cusum_s_pos": np.round(s_pos, 2),
            "cusum_s_neg": np.round(s_neg, 2),
            "cusum_threshold": self.threshold_h,
            "cusum_status": cusum_status,
            "cusum_is_anomaly": is_anomaly,
        })

        if dates is not None:
            res_df.insert(0, "date", pd.to_datetime(dates).values)

        return res_df
