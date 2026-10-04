"""
Automated Pytest Suite for Feature Engineering Module (Task 10.2)
Downtown San Diego Homeless Population Analysis
"""

import numpy as np
import pandas as pd
import pytest

from feature_engineering.pipeline import FeatureEngineeringPipeline
from feature_engineering.importance_analyzer import FeatureImportanceAnalyzer
from feature_engineering.temporal import generate_temporal_features
from feature_engineering.autoregressive import generate_autoregressive_features
from feature_engineering.rolling_windows import generate_rolling_features
from feature_engineering.spatial_features import generate_spatial_features


@pytest.fixture(scope="module")
def feature_matrix():
    pipeline = FeatureEngineeringPipeline()
    df = pipeline.run(fill_initial_lags=True)
    return df


def test_temporal_cyclicality(feature_matrix):
    sin_vals = feature_matrix["temporal_sin_month"]
    cos_vals = feature_matrix["temporal_cos_month"]
    identity = (sin_vals ** 2) + (cos_vals ** 2)
    assert np.allclose(identity, 1.0, atol=1e-3)
    assert feature_matrix["temporal_trend_idx"].is_monotonic_increasing


def test_leakage_free_lags(feature_matrix):
    # lag_1m_adjusted at row t must strictly equal target at row t-1
    for i in range(1, len(feature_matrix)):
        expected = feature_matrix.loc[i - 1, "target_downtown_adjusted"]
        actual = feature_matrix.loc[i, "lag_1m_adjusted"]
        assert np.isclose(expected, actual, atol=1e-2)


def test_rolling_window_properties(feature_matrix):
    std_3m = feature_matrix["rolling_std_3m_adjusted"]
    min_3m = feature_matrix["rolling_min_3m_adjusted"]
    max_3m = feature_matrix["rolling_max_3m_adjusted"]
    assert (std_3m >= 0).all()
    assert (max_3m >= min_3m).all()
    # Bollinger upper envelope must be >= lower envelope
    upper = feature_matrix["bollinger_upper_12m_adjusted"]
    lower = feature_matrix["bollinger_lower_12m_adjusted"]
    assert (upper >= lower).all()


def test_spatial_hhi_bounds(feature_matrix):
    hhi = feature_matrix["spatial_hhi_concentration_index_lag1"]
    assert (hhi >= 0.0).all()
    assert (hhi <= 1.0).all()
    ev_share = feature_matrix["spatial_east_village_share_pct_lag1"]
    assert (ev_share >= 0.0).all()
    assert (ev_share <= 100.0).all()


def test_feature_count_and_training_subset(feature_matrix):
    assert len(feature_matrix) == 108
    meta_cols = ["date", "target_downtown_adjusted", "target_downtown_raw", "target_next_month_adjusted", "train_ready_flag"]
    feat_cols = [c for c in feature_matrix.columns if c not in meta_cols]
    # Mandate is 50+ features
    assert len(feat_cols) >= 50
    # Training subset (2018-2025) must have 96 rows and 0 nulls across all features
    train_subset = feature_matrix[feature_matrix["train_ready_flag"] == 1]
    assert len(train_subset) == 96
    assert train_subset[feat_cols].isnull().sum().sum() == 0


def test_importance_analyzer_execution():
    analyzer = FeatureImportanceAnalyzer()
    summary = analyzer.run_analysis()
    assert len(summary) >= 50
    assert "mean_abs_shap" in summary.columns
    assert "gini_importance" in summary.columns
    assert (summary["mean_abs_shap"] >= 0).all()
    # Gini importances must sum to approximately 1.0
    assert np.isclose(summary["gini_importance"].sum(), 1.0, atol=1e-2)
