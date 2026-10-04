"""
Constrained Stacking Meta-Learner (Non-Negative Least Squares with Sum-to-One Equality)
Solves:
    min_w || y - Y_hat * w ||_2^2
    subject to: w_i >= 0, sum(w_i) = 1.0
Guarantees that the ensemble output is a strictly convex, non-negative combination of base models.
"""

from typing import Dict, List, Optional, Union
import numpy as np
import pandas as pd
from scipy.optimize import minimize


class StackingMetaLearner:
    """
    Constrained meta-learner optimizing convex ensemble weights over out-of-fold predictions.
    """

    def __init__(self, model_names: Optional[List[str]] = None):
        self.model_names = model_names or ["LightGBM", "BSTS", "NeuralNetwork"]
        self.weights: Optional[np.ndarray] = None
        self.loss_: Optional[float] = None

    def fit(self, Y_hat: Union[pd.DataFrame, np.ndarray], y_true: Union[pd.Series, np.ndarray]):
        """
        Fits optimal convex weights w using SLSQP quadratic programming.
        """
        if isinstance(Y_hat, pd.DataFrame):
            self.model_names = list(Y_hat.columns)
            Y_arr = Y_hat.values.astype(float)
        else:
            Y_arr = np.asarray(Y_hat, dtype=float)

        y_arr = np.asarray(y_true, dtype=float)
        n_models = Y_arr.shape[1]

        def objective(w):
            pred = np.dot(Y_arr, w)
            return float(np.mean((y_arr - pred) ** 2))

        # Initial uniform weights
        w0 = np.ones(n_models) / float(n_models)
        bounds = [(0.0, 1.0)] * n_models
        constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1.0}

        res = minimize(
            objective,
            w0,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
            options={"ftol": 1e-9, "maxiter": 500},
        )

        if res.success and np.all(res.x >= -1e-6):
            raw_weights = np.maximum(res.x, 0.0)
            self.weights = raw_weights / np.sum(raw_weights)
        else:
            # Fallback to equal weighting if solver encounters numerical instability
            self.weights = np.ones(n_models) / float(n_models)

        self.loss_ = objective(self.weights)
        return self

    def predict(self, Y_hat: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        if self.weights is None:
            raise RuntimeError("StackingMetaLearner must be fitted before predict()")

        if isinstance(Y_hat, pd.DataFrame):
            Y_arr = Y_hat.values.astype(float)
        else:
            Y_arr = np.asarray(Y_hat, dtype=float)

        preds = np.dot(Y_arr, self.weights)
        return np.clip(preds, 0.0, None)

    @property
    def weights_dict(self) -> Dict[str, float]:
        if self.weights is None:
            return {}
        return {
            name: round(float(w), 4)
            for name, w in zip(self.model_names, self.weights)
        }
