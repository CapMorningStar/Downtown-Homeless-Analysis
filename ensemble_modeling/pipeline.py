"""
Master Ensemble Pipeline
Orchestrates:
- 5-Fold Expanding-Window TimeSeriesSplit Cross-Validation (2021–2025)
- Model Fitting for LightGBM, BSTS, and Temporal Neural Network
- Constrained SLSQP Stacking Meta-Learner Weight Optimization
- Calibrated Conformal Prediction Intervals (80% and 95%)
- 2026 Prospective Trajectory Generation
- High-Resolution Visualization Export
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .cross_validation import TimeSeriesExpandingCV, compute_metrics
from .models_gbm import GBMModel
from .models_bsts import BSTSModel
from .models_neural import NeuralNetworkModel
from .stacking import StackingMetaLearner
from .conformal import ConformalPredictor

logger = logging.getLogger(__name__)


class EnsemblePipeline:
    """
    Coordinates end-to-end ensemble training, cross-validation, stacking, and uncertainty quantification.
    """

    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = data_path or Path("data/FeatureMatrix_Comprehensive_68.csv")
        self.logger = logging.getLogger(self.__class__.__name__)
        self.meta_cols = [
            "date",
            "target_downtown_adjusted",
            "target_downtown_raw",
            "target_next_month_adjusted",
            "train_ready_flag",
        ]
        self.meta_learner: Optional[StackingMetaLearner] = None
        self.conformal_predictor: Optional[ConformalPredictor] = None
        self.fitted_gbm: Optional[GBMModel] = None
        self.fitted_bsts: Optional[BSTSModel] = None
        self.fitted_neural: Optional[NeuralNetworkModel] = None
        self.feature_cols: List[str] = []

    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        if not self.data_path.exists():
            raise FileNotFoundError(f"Feature matrix not found at {self.data_path}")

        df = pd.read_csv(self.data_path)
        df["date"] = pd.to_datetime(df["date"])
        train_df = df[df["train_ready_flag"] == 1].reset_index(drop=True)
        self.feature_cols = [c for c in train_df.columns if c not in self.meta_cols]
        return df, train_df

    def run_cv_evaluation(self) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Dict[str, float]]]:
        """
        Executes expanding-window cross-validation across folds (2021 to 2025).
        Returns:
            - fold_metrics_df: per-fold accuracy metrics for each model architecture
            - oof_predictions_df: out-of-fold predictions aligned by date
            - overall_metrics: dictionary of full-sample OOF metrics per model
        """
        _, train_df = self.load_data()
        cv = TimeSeriesExpandingCV()

        oof_dates: List[pd.Timestamp] = []
        oof_y: List[float] = []
        oof_baseline: List[float] = []
        oof_gbm: List[float] = []
        oof_bsts: List[float] = []
        oof_neural: List[float] = []
        oof_ensemble: List[float] = []

        fold_records = []

        self.logger.info("Executing 5-Fold Expanding-Window Cross-Validation...")

        for fold_idx, tr_idx, te_idx, test_year in cv.split(train_df):
            X_tr = train_df.loc[tr_idx, self.feature_cols]
            y_tr = train_df.loc[tr_idx, "target_downtown_adjusted"]
            dates_tr = train_df.loc[tr_idx, "date"]

            X_te = train_df.loc[te_idx, self.feature_cols]
            y_te = train_df.loc[te_idx, "target_downtown_adjusted"]
            dates_te = train_df.loc[te_idx, "date"]

            # 0. Baseline (Univariate Lag 1)
            p_base = X_te["lag_1m_adjusted"].values

            # 1. GBM (LightGBM)
            gbm = GBMModel(
                n_estimators=110,
                learning_rate=0.035,
                max_depth=4,
                num_leaves=14,
                random_state=42,
            )
            gbm.fit(X_tr, y_tr)
            p_gbm = gbm.predict(X_te)

            # 2. BSTS
            bsts = BSTSModel(level="local level", seasonal=12)
            bsts.fit(X_tr, y_tr)
            p_bsts = bsts.predict(X_te, y_test=y_te)

            # 3. Neural Network
            neural = NeuralNetworkModel(
                hidden_layer_sizes=(32, 16),
                alpha=1.0,
                k_features=5,
                random_state=42,
            )
            neural.fit(X_tr, y_tr)
            p_neural = neural.predict(X_te)

            # Fold Stacking Meta-Learner (fit on fold training predictions or equal combination)
            # To avoid intra-fold leakage, use training fit
            Y_te_hat = np.column_stack([p_gbm, p_bsts, p_neural])
            # For fold prediction, compute constrained meta-learner fit on current train fold
            p_tr_gbm = gbm.predict(X_tr)
            p_tr_bsts = bsts.predict(X_tr)
            p_tr_neural = neural.predict(X_tr)
            Y_tr_hat = np.column_stack([p_tr_gbm, p_tr_bsts, p_tr_neural])

            fold_stacker = StackingMetaLearner(model_names=["LightGBM", "BSTS", "NeuralNetwork"])
            fold_stacker.fit(Y_tr_hat, y_tr)
            p_ens = fold_stacker.predict(Y_te_hat)

            # Metrics
            m_base = compute_metrics(y_te, p_base)
            m_gbm = compute_metrics(y_te, p_gbm)
            m_bsts = compute_metrics(y_te, p_bsts)
            m_neural = compute_metrics(y_te, p_neural)
            m_ens = compute_metrics(y_te, p_ens)

            fold_records.append({
                "fold": fold_idx,
                "test_year": test_year,
                "train_months": len(tr_idx),
                "test_months": len(te_idx),
                "base_mae": m_base["mae"],
                "gbm_mae": m_gbm["mae"],
                "bsts_mae": m_bsts["mae"],
                "neural_mae": m_neural["mae"],
                "ens_mae": m_ens["mae"],
                "base_rmse": m_base["rmse"],
                "gbm_rmse": m_gbm["rmse"],
                "bsts_rmse": m_bsts["rmse"],
                "neural_rmse": m_neural["rmse"],
                "ens_rmse": m_ens["rmse"],
                "ens_mape": m_ens["mape"],
                "ens_r2": m_ens["r2"],
            })

            oof_dates.extend(dates_te)
            oof_y.extend(y_te.values)
            oof_baseline.extend(p_base)
            oof_gbm.extend(p_gbm)
            oof_bsts.extend(p_bsts)
            oof_neural.extend(p_neural)
            oof_ensemble.extend(p_ens)

        fold_metrics_df = pd.DataFrame(fold_records)

        oof_df = pd.DataFrame({
            "date": oof_dates,
            "y_true": oof_y,
            "pred_baseline": oof_baseline,
            "pred_gbm": oof_gbm,
            "pred_bsts": oof_bsts,
            "pred_neural": oof_neural,
            "pred_ensemble": oof_ensemble,
        }).sort_values("date").reset_index(drop=True)

        overall_metrics = {
            "Baseline (ARIMA Proxy)": compute_metrics(oof_df["y_true"], oof_df["pred_baseline"]),
            "LightGBM": compute_metrics(oof_df["y_true"], oof_df["pred_gbm"]),
            "Bayesian Structural TS": compute_metrics(oof_df["y_true"], oof_df["pred_bsts"]),
            "Temporal Neural Net": compute_metrics(oof_df["y_true"], oof_df["pred_neural"]),
            "Constrained Ensemble": compute_metrics(oof_df["y_true"], oof_df["pred_ensemble"]),
        }

        return fold_metrics_df, oof_df, overall_metrics

    def fit_full_and_calibrate(self, oof_df: pd.DataFrame) -> Tuple[StackingMetaLearner, ConformalPredictor]:
        """
        Fits full models on all 96 historical training months (2018–2025)
        and solves global meta-learner stacking weights and conformal calibration.
        """
        _, train_df = self.load_data()
        X_all = train_df[self.feature_cols]
        y_all = train_df["target_downtown_adjusted"]

        self.logger.info("Fitting full base models on 2018–2025 dataset (96 months)...")
        self.fitted_gbm = GBMModel(
            n_estimators=110, learning_rate=0.035, max_depth=4, num_leaves=14, random_state=42
        ).fit(X_all, y_all)

        self.fitted_bsts = BSTSModel(level="local level", seasonal=12).fit(X_all, y_all)

        self.fitted_neural = NeuralNetworkModel(
            hidden_layer_sizes=(32, 16), alpha=1.0, k_features=5, random_state=42
        ).fit(X_all, y_all)

        # Optimize Global Stacking Weights over OOF predictions
        Y_oof = oof_df[["pred_gbm", "pred_bsts", "pred_neural"]].values
        self.meta_learner = StackingMetaLearner(model_names=["LightGBM", "BSTS", "NeuralNetwork"])
        self.meta_learner.fit(Y_oof, oof_df["y_true"].values)
        self.logger.info(f"Optimal Stacking Weights: {self.meta_learner.weights_dict}")

        # Recalculate full ensemble OOF with optimal weights
        y_ens_oof = self.meta_learner.predict(Y_oof)

        # Calibrate Conformal Prediction Intervals
        self.conformal_predictor = ConformalPredictor(confidence_levels=[0.80, 0.95])
        self.conformal_predictor.fit(oof_df["y_true"].values, y_ens_oof)

        cov_report = self.conformal_predictor.evaluate_coverage(oof_df["y_true"].values, y_ens_oof)
        self.logger.info(f"Conformal Calibration Coverage: {cov_report}")

        return self.meta_learner, self.conformal_predictor

    def generate_prospective_forecast_2026(self, n_months: int = 12) -> pd.DataFrame:
        """
        Generates prospective monthly forecasts across 2026 (2026-01-01 to 2026-12-01)
        with 80% and 95% conformal prediction bounds.
        """
        if self.meta_learner is None or self.conformal_predictor is None:
            raise RuntimeError("Must call fit_full_and_calibrate() before generating 2026 forecast")

        df, train_df = self.load_data()
        last_row = train_df.iloc[-1].copy()
        last_date = pd.to_datetime(last_row["date"])

        future_dates = [last_date + pd.DateOffset(months=i) for i in range(1, n_months + 1)]
        preds_records = []

        curr_features = last_row[self.feature_cols].copy()
        curr_y = float(last_row["target_downtown_adjusted"])

        for step_idx, f_date in enumerate(future_dates, 1):
            feat_dict = curr_features.to_dict()
            month = f_date.month

            # Update calendar harmonics
            feat_dict["temporal_month"] = month
            feat_dict["temporal_quarter"] = (month - 1) // 3 + 1
            feat_dict["temporal_year"] = f_date.year
            feat_dict["temporal_sin_month"] = np.sin(2 * np.pi * month / 12.0)
            feat_dict["temporal_cos_month"] = np.cos(2 * np.pi * month / 12.0)
            feat_dict["temporal_trend_idx"] = float(last_row["temporal_trend_idx"]) + step_idx

            # Lag updates
            feat_dict["lag_1m_adjusted"] = curr_y

            X_step = pd.DataFrame([feat_dict])[self.feature_cols]

            # Model point predictions
            p_gbm = float(self.fitted_gbm.predict(X_step)[0])
            p_bsts = float(self.fitted_bsts.predict(X_step)[0])
            p_nn = float(self.fitted_neural.predict(X_step)[0])

            Y_step = np.array([[p_gbm, p_bsts, p_nn]])
            p_ens = float(self.meta_learner.predict(Y_step)[0])

            # Conformal intervals
            intervals = self.conformal_predictor.predict_intervals(np.array([p_ens]))
            low80 = float(intervals["lower_80"][0])
            up80 = float(intervals["upper_80"][0])
            low95 = float(intervals["lower_95"][0])
            up95 = float(intervals["upper_95"][0])

            preds_records.append({
                "date": f_date.strftime("%Y-%m-%d"),
                "pred_gbm": round(p_gbm, 1),
                "pred_bsts": round(p_bsts, 1),
                "pred_neural": round(p_nn, 1),
                "pred_ensemble": round(p_ens, 1),
                "conformal_lower_80": round(low80, 1),
                "conformal_upper_80": round(up80, 1),
                "conformal_lower_95": round(low95, 1),
                "conformal_upper_95": round(up95, 1),
            })

            # Update autoregressive state for recursive multi-step rollout
            curr_y = p_ens

        forecast_df = pd.DataFrame(preds_records)
        return forecast_df

    def plot_ensemble_results(
        self,
        oof_df: pd.DataFrame,
        forecast_df: pd.DataFrame,
        output_path: Path = Path("slide_assets/task10_ensemble_predictions.png"),
    ) -> Path:
        """
        Creates a high-resolution 300 DPI publication chart showing:
        - Historical observations (2018–2025)
        - Cross-validated out-of-fold predictions
        - Prospective 2026 forecast with calibrated 80% & 95% conformal uncertainty envelopes
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        _, train_df = self.load_data()

        fig, ax = plt.subplots(figsize=(15, 7))

        hist_dates = pd.to_datetime(train_df["date"])
        hist_y = train_df["target_downtown_adjusted"]
        oof_dates = pd.to_datetime(oof_df["date"])
        fore_dates = pd.to_datetime(forecast_df["date"])

        # Plot Historical Ground Truth
        ax.plot(
            hist_dates,
            hist_y,
            color="#0F172A",
            linewidth=2.4,
            marker="o",
            markersize=4.5,
            label="Historical Ground Truth (Adjusted)",
            zorder=4,
        )

        # Plot Cross-Validated Out-of-Fold Predictions
        ax.plot(
            oof_dates,
            oof_df["pred_ensemble"],
            color="#2563EB",
            linewidth=2.0,
            linestyle="--",
            label="Ensemble CV Predictions (2021–2025)",
            zorder=3,
        )

        # Plot Individual Model Tracks (muted)
        ax.plot(
            oof_dates,
            oof_df["pred_gbm"],
            color="#10B981",
            linewidth=1.2,
            alpha=0.6,
            linestyle=":",
            label="LightGBM Track",
        )
        ax.plot(
            oof_dates,
            oof_df["pred_bsts"],
            color="#F59E0B",
            linewidth=1.2,
            alpha=0.6,
            linestyle=":",
            label="BSTS Track",
        )

        # Plot Prospective 2026 Forecast
        ax.plot(
            fore_dates,
            forecast_df["pred_ensemble"],
            color="#DC2626",
            linewidth=2.6,
            marker="s",
            markersize=5,
            label="Ensemble 2026 Prospective Forecast",
            zorder=5,
        )

        # 80% Conformal Fan
        ax.fill_between(
            fore_dates,
            forecast_df["conformal_lower_80"],
            forecast_df["conformal_upper_80"],
            color="#FCA5A5",
            alpha=0.45,
            label="80% Calibrated Conformal Interval",
            zorder=2,
        )

        # 95% Conformal Fan
        ax.fill_between(
            fore_dates,
            forecast_df["conformal_lower_95"],
            forecast_df["conformal_upper_95"],
            color="#FEE2E2",
            alpha=0.55,
            label="95% Calibrated Conformal Interval",
            zorder=1,
        )

        # Key Milestones Annotations
        ax.axvline(pd.to_datetime("2020-04-01"), color="#64748B", linestyle="--", alpha=0.5)
        ax.text(pd.to_datetime("2020-04-01"), 2000, " COVID Demobilization", color="#475569", fontsize=9, rotation=90)

        ax.axvline(pd.to_datetime("2023-07-01"), color="#EF4444", linestyle="--", alpha=0.6)
        ax.text(pd.to_datetime("2023-07-01"), 2000, " Unsafe Camping Ban", color="#B91C1C", fontsize=9, rotation=90)

        ax.axvline(pd.to_datetime("2026-01-01"), color="#2563EB", linestyle="-", alpha=0.7)
        ax.text(pd.to_datetime("2026-01-01"), 2000, " 2026 Forecast Horizon", color="#1D4ED8", fontsize=9, rotation=90)

        ax.set_title(
            "Task 10.3 Multi-Source Ensemble Prediction System: Historical Fit & 2026 Calibrated Projection",
            fontsize=13,
            fontweight="bold",
            pad=14,
        )
        ax.set_ylabel("Downtown Unsheltered Homeless Count", fontsize=11, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend(loc="upper left", framealpha=0.9, fontsize=9.5)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        self.logger.info(f"Predictions figure saved to {output_path}")
        return output_path
