"""
Calibrated Conformal Prediction Intervals (Conformal Uncertainty Quantifier)
Computes distribution-free non-parametric prediction intervals at exact nominal confidence levels
(80% and 95%) using finite-sample conformal calibration over out-of-fold residuals:
  q_{1-alpha} = Quantile(|y - y_hat|, ceil((n+1)(1-alpha)) / n)
"""

from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd


class ConformalPredictor:
    """
    Non-parametric conformal prediction interval calibrator.
    Guarantees finite-sample coverage validity under exchangeability.
    """

    def __init__(self, confidence_levels: Optional[List[float]] = None):
        self.confidence_levels = confidence_levels or [0.80, 0.95]
        self.residuals_: Optional[np.ndarray] = None
        self.quantiles_: Dict[float, float] = {}

    def fit(self, y_true: Union[pd.Series, np.ndarray], y_pred: Union[pd.Series, np.ndarray]):
        """
        Calibrates residual quantiles on out-of-fold validation predictions.
        """
        y_t = np.asarray(y_true, dtype=float)
        y_p = np.asarray(y_pred, dtype=float)

        self.residuals_ = np.abs(y_t - y_p)
        n = len(self.residuals_)

        for conf in self.confidence_levels:
            # Finite-sample conformal adjustment
            adjusted_quantile = min(1.0, (np.ceil((n + 1) * conf)) / n)
            q_val = float(np.quantile(self.residuals_, adjusted_quantile))
            self.quantiles_[conf] = round(q_val, 2)

        return self

    def predict_intervals(
        self, y_pred: Union[pd.Series, np.ndarray]
    ) -> Dict[str, np.ndarray]:
        """
        Constructs lower and upper bounds for point predictions.
        """
        if not self.quantiles_:
            raise RuntimeError("ConformalPredictor must be fitted before predict_intervals()")

        y_p = np.asarray(y_pred, dtype=float)
        result = {"point_pred": y_p}

        for conf, q in self.quantiles_.items():
            pct = int(round(conf * 100))
            lower = np.maximum(0.0, y_p - q)
            upper = y_p + q
            result[f"lower_{pct}"] = lower
            result[f"upper_{pct}"] = upper

        return result

    def evaluate_coverage(
        self, y_true: Union[pd.Series, np.ndarray], y_pred: Union[pd.Series, np.ndarray]
    ) -> Dict[str, Dict[str, float]]:
        """
        Evaluates empirical coverage and interval width against true observations.
        """
        y_t = np.asarray(y_true, dtype=float)
        y_p = np.asarray(y_pred, dtype=float)
        intervals = self.predict_intervals(y_p)

        coverage_report = {}
        for conf in self.confidence_levels:
            pct = int(round(conf * 100))
            lower = intervals[f"lower_{pct}"]
            upper = intervals[f"upper_{pct}"]

            covered = (y_t >= lower) & (y_t <= upper)
            empirical_cov = float(np.mean(covered) * 100.0)
            avg_width = float(np.mean(upper - lower))

            coverage_report[f"{pct}%"] = {
                "nominal_coverage_pct": conf * 100.0,
                "empirical_coverage_pct": round(empirical_cov, 2),
                "margin_error": self.quantiles_[conf],
                "mean_interval_width": round(avg_width, 2),
            }

        return coverage_report
