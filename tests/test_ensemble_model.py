"""
Unit & Integration Tests for Task 10.3 Ensemble Prediction System
Tests:
- Expanding-window TimeSeriesSplit temporal monotonicity (no future leakage)
- Individual model fitting & prediction bounds (LightGBM, BSTS, Neural Net)
- Constrained SLSQP Stacking weights (w_i >= 0, sum(w) = 1.0)
- Conformal prediction interval calibration and width monotonicity (95% > 80%)
- 5-Stage Ablation study structure
- Prospective 2026 forecast shape & completeness
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from ensemble_modeling.cross_validation import TimeSeriesExpandingCV, compute_metrics
from ensemble_modeling.models_gbm import GBMModel
from ensemble_modeling.models_bsts import BSTSModel
from ensemble_modeling.models_neural import NeuralNetworkModel
from ensemble_modeling.stacking import StackingMetaLearner
from ensemble_modeling.conformal import ConformalPredictor
from ensemble_modeling.ablation import AblationStudyEngine
from ensemble_modeling.pipeline import EnsemblePipeline


FEATURE_MATRIX_PATH = Path("data/FeatureMatrix_Comprehensive_67.csv")


@pytest.fixture
def sample_feature_data():
    if not FEATURE_MATRIX_PATH.exists():
        pytest.skip(f"Feature matrix {FEATURE_MATRIX_PATH} does not exist.")
    df = pd.read_csv(FEATURE_MATRIX_PATH)
    train_df = df[df["train_ready_flag"] == 1].reset_index(drop=True)
    return df, train_df


def test_cv_splits_temporal_monotonicity(sample_feature_data):
    """Verifies that all train indices strictly precede test indices with no future data leakage."""
    _, train_df = sample_feature_data
    cv = TimeSeriesExpandingCV()

    for fold_idx, tr_idx, te_idx, test_year in cv.split(train_df):
        assert len(tr_idx) > 0
        assert len(te_idx) > 0
        # Strict temporal monotonicity: max(train_idx) < min(test_idx)
        assert np.max(tr_idx) < np.min(te_idx), f"Fold {fold_idx} ({test_year}) leaks future data into train set!"
        # Test year matches actual test dates
        test_dates = pd.to_datetime(train_df.loc[te_idx, "date"])
        assert (test_dates.dt.year == test_year).all()


def test_compute_metrics():
    """Verifies econometric accuracy metric formulas."""
    y_true = np.array([100.0, 200.0, 300.0])
    y_pred = np.array([110.0, 190.0, 300.0])
    m = compute_metrics(y_true, y_pred)
    assert m["mae"] == pytest.approx(6.67, 0.05)
    assert m["rmse"] == pytest.approx(8.16, 0.05)
    assert m["r2"] > 0.95


def test_base_models_fit_and_predict(sample_feature_data):
    """Verifies LightGBM, BSTS, and Neural Net fit and predict valid non-negative counts."""
    _, train_df = sample_feature_data
    meta_cols = ["date", "target_downtown_adjusted", "target_downtown_raw", "target_next_month_adjusted", "train_ready_flag"]
    feat_cols = [c for c in train_df.columns if c not in meta_cols]

    X_tr = train_df.loc[:50, feat_cols]
    y_tr = train_df.loc[:50, "target_downtown_adjusted"]
    X_te = train_df.loc[51:60, feat_cols]

    # LightGBM
    gbm = GBMModel(n_estimators=20, max_depth=3, random_state=42).fit(X_tr, y_tr)
    p_gbm = gbm.predict(X_te)
    assert len(p_gbm) == len(X_te)
    assert np.all(p_gbm >= 0)
    assert not np.isnan(p_gbm).any()

    # BSTS
    bsts = BSTSModel(seasonal=12, maxiter=50).fit(X_tr, y_tr)
    p_bsts = bsts.predict(X_te)
    assert len(p_bsts) == len(X_te)
    assert np.all(p_bsts >= 0)
    assert not np.isnan(p_bsts).any()

    # Neural Network
    nn = NeuralNetworkModel(hidden_layer_sizes=(16, 8), max_iter=200, random_state=42).fit(X_tr, y_tr)
    p_nn = nn.predict(X_te)
    assert len(p_nn) == len(X_te)
    assert np.all(p_nn >= 0)
    assert not np.isnan(p_nn).any()


def test_stacking_weights_constraints():
    """Verifies that SLSQP meta-learner guarantees non-negative weights that sum to 1.0."""
    np.random.seed(42)
    y_true = np.array([1000, 1100, 1050, 1200, 1150], dtype=float)
    Y_hat = np.array([
        [980, 1020, 990],
        [1090, 1110, 1120],
        [1040, 1060, 1045],
        [1210, 1190, 1205],
        [1140, 1160, 1155],
    ], dtype=float)

    meta = StackingMetaLearner(model_names=["M1", "M2", "M3"])
    meta.fit(Y_hat, y_true)

    weights = meta.weights
    assert len(weights) == 3
    assert np.all(weights >= 0.0), f"Weights violate non-negativity constraint: {weights}"
    assert np.sum(weights) == pytest.approx(1.0, 1e-4), f"Weights do not sum to 1.0: {np.sum(weights)}"

    preds = meta.predict(Y_hat)
    assert len(preds) == len(y_true)
    assert np.all(preds >= 0)


def test_conformal_interval_monotonicity():
    """Verifies that 95% conformal interval width is strictly wider than 80% interval width."""
    y_true = np.array([1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900], dtype=float)
    y_pred = y_true + np.random.normal(0, 50, size=len(y_true))

    cp = ConformalPredictor(confidence_levels=[0.80, 0.95])
    cp.fit(y_true, y_pred)

    intervals = cp.predict_intervals(np.array([1500.0]))
    width_80 = intervals["upper_80"][0] - intervals["lower_80"][0]
    width_95 = intervals["upper_95"][0] - intervals["lower_95"][0]

    assert width_95 > width_80, f"95% interval ({width_95}) should be strictly wider than 80% interval ({width_80})"
    assert intervals["lower_80"][0] >= 0.0
    assert intervals["lower_95"][0] >= 0.0


def test_ablation_study_structure():
    """Verifies ablation study definitions and execution output format."""
    engine = AblationStudyEngine()
    features = [
        "lag_1m_adjusted", "lag_2m_adjusted", "lag_12m_seasonal_adjusted",
        "lag_1m_311_encampment", "weather_temp_mean_lag1", "lag_1m_unemployment_rate",
        "shelter_capacity_headroom_lag1"
    ]
    stages = engine.get_stages_features(features)
    assert len(stages) == 5
    assert len(stages["Stage 0: Univariate Lags"]) <= len(stages["Stage 1: + 311 Encampment Signals"])
    assert len(stages["Stage 1: + 311 Encampment Signals"]) <= len(stages["Stage 2: + Weather Anomalies"])


def test_prospective_2026_forecast_shape():
    """Verifies that the generated prospective forecast has 12 months with valid bounds."""
    forecast_path = Path("data/Ensemble_Forecast_2026.csv")
    if not forecast_path.exists():
        pytest.skip(f"{forecast_path} does not exist yet.")
    df = pd.read_csv(forecast_path)
    assert len(df) == 12
    assert "date" in df.columns
    assert "pred_ensemble" in df.columns
    assert "conformal_lower_80" in df.columns
    assert "conformal_upper_80" in df.columns
    assert "conformal_lower_95" in df.columns
    assert "conformal_upper_95" in df.columns

    # Verify bounds ordering
    assert (df["conformal_lower_95"] <= df["conformal_lower_80"]).all()
    assert (df["conformal_lower_80"] <= df["pred_ensemble"]).all()
    assert (df["pred_ensemble"] <= df["conformal_upper_80"]).all()
    assert (df["conformal_upper_80"] <= df["conformal_upper_95"]).all()
