"""
Feature Engineering Package for Downtown San Diego Homeless Population Analysis (Assignment 10).
Provides 67+ engineered features across 7 orthogonal families:
- Temporal & cyclical encoding
- Autoregressive lags, differences & momentum
- Rolling window statistics & volatility envelopes
- Spatial concentration & neighborhood distributions
- Cross-domain interactions (weather, 311, civic events, economic distress)
- Tree Gini, Permutation Importance, and SHAP attribution analysis
"""

from .pipeline import FeatureEngineeringPipeline
from .importance_analyzer import FeatureImportanceAnalyzer

__all__ = ["FeatureEngineeringPipeline", "FeatureImportanceAnalyzer"]
