"""
Gradient Boosted Decision Tree Model Wrapper (Model Family 1)
Supports LightGBM and XGBoost with automatic fallback to HistGradientBoostingRegressor.
Includes L1/L2 regularization and tree depth constraints suited for monthly time series.
"""

from typing import Dict, List, Optional, Union
import numpy as np
import pandas as pd

try:
    from lightgbm import LGBMRegressor
    HAS_LIGHTGBM = True
except ImportError:
    HAS_LIGHTGBM = False

try:
    from xgboost import XGBRegressor
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

from sklearn.ensemble import HistGradientBoostingRegressor


class GBMModel:
    """
    Gradient Boosted Decision Tree model for time-series forecasting.
    """

    def __init__(
        self,
        model_type: str = "lightgbm",
        n_estimators: int = 120,
        learning_rate: float = 0.04,
        max_depth: int = 4,
        num_leaves: int = 15,
        subsample: float = 0.85,
        colsample_bytree: float = 0.85,
        reg_alpha: float = 0.2,
        reg_lambda: float = 1.0,
        random_state: int = 42,
    ):
        self.model_type = model_type.lower()
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.num_leaves = num_leaves
        self.subsample = subsample
        self.colsample_bytree = colsample_bytree
        self.reg_alpha = reg_alpha
        self.reg_lambda = reg_lambda
        self.random_state = random_state
        self.model = None
        self.feature_names: List[str] = []
        self._init_model()

    def _init_model(self):
        if self.model_type == "lightgbm" and HAS_LIGHTGBM:
            self.model = LGBMRegressor(
                n_estimators=self.n_estimators,
                learning_rate=self.learning_rate,
                max_depth=self.max_depth,
                num_leaves=self.num_leaves,
                subsample=self.subsample,
                colsample_bytree=self.colsample_bytree,
                reg_alpha=self.reg_alpha,
                reg_lambda=self.reg_lambda,
                random_state=self.random_state,
                verbose=-1,
                n_jobs=-1,
            )
        elif self.model_type == "xgboost" and HAS_XGBOOST:
            self.model = XGBRegressor(
                n_estimators=self.n_estimators,
                learning_rate=self.learning_rate,
                max_depth=self.max_depth,
                subsample=self.subsample,
                colsample_bytree=self.colsample_bytree,
                reg_alpha=self.reg_alpha,
                reg_lambda=self.reg_lambda,
                random_state=self.random_state,
                n_jobs=-1,
            )
        else:
            self.model = HistGradientBoostingRegressor(
                max_iter=self.n_estimators,
                learning_rate=self.learning_rate,
                max_depth=self.max_depth,
                l2_regularization=self.reg_lambda,
                random_state=self.random_state,
            )

    def fit(self, X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray]):
        if isinstance(X, pd.DataFrame):
            self.feature_names = list(X.columns)
            X_arr = X.values
        else:
            X_arr = np.asarray(X)
            self.feature_names = [f"f_{i}" for i in range(X_arr.shape[1])]

        y_arr = np.asarray(y, dtype=float)
        self.model.fit(X_arr, y_arr)
        return self

    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        if isinstance(X, pd.DataFrame):
            X_arr = X.values
        else:
            X_arr = np.asarray(X)

        preds = self.model.predict(X_arr)
        # Non-negative count constraint
        return np.clip(preds, 0.0, None)

    @property
    def feature_importances_(self) -> np.ndarray:
        if hasattr(self.model, "feature_importances_"):
            return self.model.feature_importances_
        return np.zeros(len(self.feature_names))
