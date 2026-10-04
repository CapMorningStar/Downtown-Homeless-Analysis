"""
Model-Based Anomaly Detection Surveillance (Engine 2)
Implements:
1. Multivariate Isolation Forest over 68 multi-source features
2. Non-Parametric Conformal Residual Bound Violations
"""

from typing import List, Optional, Union
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


class IsolationForestDetector:
    """
    Multivariate Isolation Forest Outlier Detector.
    Isolates anomalies by randomly selecting features and split values.
    """

    def __init__(
        self,
        contamination: float = 0.08,
        n_estimators: int = 150,
        random_state: int = 42,
    ):
        self.contamination = contamination
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.model = IsolationForest(
            contamination=self.contamination,
            n_estimators=self.n_estimators,
            random_state=self.random_state,
            n_jobs=-1,
        )
        self.scaler = StandardScaler()
        self.feature_names: List[str] = []

    def fit_detect(
        self,
        X: pd.DataFrame,
        dates: Optional[pd.Series] = None,
    ) -> pd.DataFrame:
        self.feature_names = list(X.columns)
        X_scaled = self.scaler.fit_transform(X.fillna(0.0))

        # Fit and predict (-1 = anomaly, 1 = normal)
        raw_preds = self.model.fit_predict(X_scaled)
        # raw_scores: lower is more abnormal
        raw_scores = self.model.decision_function(X_scaled)
        # Normalize score so higher score = more anomalous (0 to 1)
        min_s, max_s = np.min(raw_scores), np.max(raw_scores)
        norm_anomaly_score = (max_s - raw_scores) / (max_s - min_s + 1e-6)

        is_anomaly = raw_preds == -1

        res_df = pd.DataFrame({
            "iso_decision_score": np.round(raw_scores, 4),
            "iso_anomaly_score": np.round(norm_anomaly_score, 4),
            "iso_is_anomaly": is_anomaly,
        })

        if dates is not None:
            res_df.insert(0, "date", pd.to_datetime(dates).values)

        return res_df


class ConformalResidualDetector:
    """
    Residual-based detector identifying observations exceeding 95% conformal bounds.
    """

    def __init__(self, conformal_margin: float = 761.15):
        self.conformal_margin = conformal_margin

    def detect_residuals(
        self,
        y_true: Union[pd.Series, np.ndarray],
        y_pred: Union[pd.Series, np.ndarray],
        dates: Optional[pd.Series] = None,
        margin: Optional[float] = None,
    ) -> pd.DataFrame:
        y_t = np.asarray(y_true, dtype=float)
        y_p = np.asarray(y_pred, dtype=float)
        q = margin if margin is not None else self.conformal_margin

        residuals = y_t - y_p
        abs_res = np.abs(residuals)
        is_anomaly = abs_res > q

        status = []
        for r, anom in zip(residuals, is_anomaly):
            if anom and r > 0:
                status.append("RESIDUAL_SURGE")
            elif anom and r < 0:
                status.append("RESIDUAL_PLUNGE")
            else:
                status.append("NORMAL")

        res_df = pd.DataFrame({
            "actual_count": np.round(y_t, 1),
            "predicted_count": np.round(y_p, 1),
            "residual": np.round(residuals, 2),
            "abs_residual": np.round(abs_res, 2),
            "conformal_margin": round(q, 2),
            "conformal_status": status,
            "conformal_is_anomaly": is_anomaly,
        })

        if dates is not None:
            res_df.insert(0, "date", pd.to_datetime(dates).values)

        return res_df
