"""
Ensemble Prediction Package for Downtown San Diego Homeless Population Analysis (Assignment 10).
Integrates:
- Gradient Boosted Decision Trees (LightGBM / XGBoost)
- Bayesian Structural Time Series (BSTS via State Space UnobservedComponents)
- Temporal Neural Networks (Standardized Deep MLP)
- Constrained Non-Negative Least Squares Stacking Meta-Learner
- Calibrated Conformal Prediction Intervals (80% and 95%)
- 5-Stage Feature Domain Ablation Engine
"""

from .pipeline import EnsemblePipeline
from .stacking import StackingMetaLearner
from .conformal import ConformalPredictor
from .ablation import AblationStudyEngine

__all__ = ["EnsemblePipeline", "StackingMetaLearner", "ConformalPredictor", "AblationStudyEngine"]
