"""
Bayesian Structural Time Series (BSTS) Model Wrapper (Model Family 2)
Implements state-space unobserved components models:
  y_t = mu_t + gamma_t + beta^T X_t + eps_t
  - mu_t: Local level / linear trend with stochastic drift
  - gamma_t: Stochastic seasonal harmonics (period = 12)
  - beta^T X_t: Exogenous regressors with standardized Kalman coefficients
"""

from typing import List, Optional, Union
import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.structural import UnobservedComponents


class BSTSModel:
    """
    Bayesian Structural Time Series Model using State Space Unobserved Components.
    """

    DEFAULT_EXOG = [
        "lag_1m_adjusted",
        "shelter_capacity_headroom_lag1",
        "rent_burden_distress_index_lag1",
    ]

    def __init__(
        self,
        level: str = "local level",
        seasonal: int = 12,
        exog_cols: Optional[List[str]] = None,
        maxiter: int = 250,
    ):
        self.level = level
        self.seasonal = seasonal
        self.exog_cols = exog_cols if exog_cols is not None else self.DEFAULT_EXOG
        self.maxiter = maxiter
        self.model = None
        self.result = None
        self.mean_X = None
        self.std_X = None
        self.active_exog_cols: List[str] = []
        self.train_y: Optional[np.ndarray] = None

    def _extract_exog(self, X: Union[pd.DataFrame, np.ndarray]) -> Optional[np.ndarray]:
        if isinstance(X, pd.DataFrame):
            # Select available exogenous columns
            present = [c for c in self.exog_cols if c in X.columns]
            if not present:
                # If none of default exog found, take first min(3, len(columns))
                present = list(X.columns[: min(3, len(X.columns))])
            self.active_exog_cols = present
            return X[present].values.astype(float)
        elif isinstance(X, np.ndarray):
            if X.ndim == 1:
                return X[:, np.newaxis].astype(float)
            k = min(len(self.exog_cols), X.shape[1])
            return X[:, :k].astype(float)
        return None

    def fit(self, X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray]):
        y_arr = np.asarray(y, dtype=float)
        self.train_y = y_arr

        X_raw = self._extract_exog(X)
        if X_raw is not None and X_raw.shape[1] > 0:
            self.mean_X = np.mean(X_raw, axis=0)
            self.std_X = np.std(X_raw, axis=0)
            self.std_X[self.std_X < 1e-6] = 1.0
            X_norm = (X_raw - self.mean_X) / self.std_X
        else:
            X_norm = None

        self.model = UnobservedComponents(
            y_arr,
            level=self.level,
            seasonal=self.seasonal,
            exog=X_norm,
        )
        self.result = self.model.fit(disp=False, maxiter=self.maxiter)
        return self

    def predict(
        self,
        X: Union[pd.DataFrame, np.ndarray],
        y_test: Optional[Union[pd.Series, np.ndarray]] = None,
    ) -> np.ndarray:
        """
        Forecasts out-of-sample or 1-step ahead using Kalman state updates.
        """
        if self.result is None:
            raise RuntimeError("BSTSModel must be fitted before predict()")

        X_raw = self._extract_exog(X)
        if X_raw is not None and self.mean_X is not None:
            X_norm = (X_raw - self.mean_X) / self.std_X
        else:
            X_norm = None

        steps = len(X) if hasattr(X, "__len__") else 1

        if y_test is not None:
            # 1-step ahead filtering across the test sequence
            y_te_arr = np.asarray(y_test, dtype=float)
            combined_y = np.concatenate([self.train_y, y_te_arr])
            if X_norm is not None:
                combined_X = np.concatenate([
                    (self._extract_exog(self.train_y_X) - self.mean_X) / self.std_X
                    if hasattr(self, "train_y_X") else X_norm,
                    X_norm
                ], axis=0) if hasattr(self, "train_y_X") else None
            # Standard prediction via forecast or rolling apply
            try:
                updated_res = self.result.apply(combined_y, exog=combined_X if X_norm is not None else None)
                preds = updated_res.predict()[len(self.train_y):]
            except Exception:
                preds = self.result.forecast(steps=steps, exog=X_norm)
        else:
            preds = self.result.forecast(steps=steps, exog=X_norm)

        # Ensure return type is 1D array
        preds_arr = np.asarray(preds, dtype=float).ravel()
        return np.clip(preds_arr, 0.0, None)
