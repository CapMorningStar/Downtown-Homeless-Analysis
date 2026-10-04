"""
Temporal Neural Network Model Wrapper (Model Family 3)
Standardized Multi-Layer Perceptron (MLP) with feature selection, dual standard scaling,
L2 weight decay regularization, and strictly bounded outputs for small-sample time series.
"""

from typing import List, Optional, Union
import numpy as np
import pandas as pd
from sklearn.compose import TransformedTargetRegressor
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


class NeuralNetworkModel:
    """
    Standardized Deep MLP with target scaling and variance-stabilized feature filtering.
    """

    def __init__(
        self,
        hidden_layer_sizes: tuple = (32, 16),
        alpha: float = 1.0,
        max_iter: int = 1000,
        k_features: int = 5,
        random_state: int = 42,
    ):
        self.hidden_layer_sizes = hidden_layer_sizes
        self.alpha = alpha
        self.max_iter = max_iter
        self.k_features = k_features
        self.random_state = random_state
        self.model: Optional[TransformedTargetRegressor] = None
        self.feature_names: List[str] = []

    def fit(self, X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray]):
        if isinstance(X, pd.DataFrame):
            self.feature_names = list(X.columns)
            X_arr = X.values
        else:
            X_arr = np.asarray(X)
            self.feature_names = [f"f_{i}" for i in range(X_arr.shape[1])]

        y_arr = np.asarray(y, dtype=float)
        n_features = X_arr.shape[1]
        k = min(self.k_features, n_features)

        if k < n_features:
            pipeline_steps = [
                ("selector", SelectKBest(score_func=f_regression, k=k)),
                ("scaler", StandardScaler()),
                (
                    "mlp",
                    MLPRegressor(
                        hidden_layer_sizes=self.hidden_layer_sizes,
                        activation="relu",
                        solver="lbfgs",
                        alpha=self.alpha,
                        max_iter=self.max_iter,
                        random_state=self.random_state,
                    ),
                ),
            ]
        else:
            pipeline_steps = [
                ("scaler", StandardScaler()),
                (
                    "mlp",
                    MLPRegressor(
                        hidden_layer_sizes=self.hidden_layer_sizes,
                        activation="relu",
                        solver="lbfgs",
                        alpha=self.alpha,
                        max_iter=self.max_iter,
                        random_state=self.random_state,
                    ),
                ),
            ]

        pipe = Pipeline(pipeline_steps)
        self.model = TransformedTargetRegressor(regressor=pipe, transformer=StandardScaler())
        self.model.fit(X_arr, y_arr)
        return self

    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        if self.model is None:
            raise RuntimeError("NeuralNetworkModel must be fitted before predict()")

        if isinstance(X, pd.DataFrame):
            X_arr = X.values
        else:
            X_arr = np.asarray(X)

        preds = self.model.predict(X_arr)
        # Ensure count is non-negative
        return np.clip(preds, 0.0, None)
