"""
5-Stage Feature Domain Ablation Study Engine
Quantifies the marginal value of orthogonal data streams:
Stage 0: Univariate Baseline (Autoregressive Lags only: lag 1, 2, 12)
Stage 1: + Municipal 311 Encampments (Volume, backlog, per-capita intensity)
Stage 2: + Meteorological & Climate Anomalies (Temperature, precipitation, CDD/HDD)
Stage 3: + Macroeconomic Distress (Unemployment rate, rent ZORI, rent burden)
Stage 4: + Full Multi-Source System (Shelter capacity headroom, safe sleeping interaction, spatial HHI, harmonics)
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .cross_validation import TimeSeriesExpandingCV, compute_metrics
from .models_gbm import GBMModel

logger = logging.getLogger(__name__)


class AblationStudyEngine:
    """
    Evaluates cumulative marginal value of feature domains across expanding-window CV.
    """

    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = data_path or Path("data/FeatureMatrix_Comprehensive_68.csv")
        self.logger = logging.getLogger(self.__class__.__name__)

    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        df = pd.read_csv(self.data_path)
        train_df = df[df["train_ready_flag"] == 1].reset_index(drop=True)
        return df, train_df

    def get_stages_features(self, all_features: List[str]) -> Dict[str, List[str]]:
        stage0 = [
            f for f in ["lag_1m_adjusted", "lag_2m_adjusted", "lag_12m_seasonal_adjusted"]
            if f in all_features
        ]
        if not stage0:
            stage0 = [all_features[0]]

        stage1 = stage0 + [f for f in all_features if "311" in f and f not in stage0]
        stage2 = stage1 + [f for f in all_features if "weather" in f and f not in stage1]
        stage3 = stage2 + [
            f for f in all_features
            if any(k in f for k in ["unemployment", "rent", "zori", "cpi"]) and f not in stage2
        ]
        stage4 = all_features

        return {
            "Stage 0: Univariate Lags": stage0,
            "Stage 1: + 311 Encampment Signals": stage1,
            "Stage 2: + Weather Anomalies": stage2,
            "Stage 3: + Economic Rent Distress": stage3,
            "Stage 4: Full Multi-Source System": stage4,
        }

    def run_ablation(self, output_csv: Optional[Path] = None) -> pd.DataFrame:
        _, train_df = self.load_data()
        meta_cols = [
            "date",
            "target_downtown_adjusted",
            "target_downtown_raw",
            "target_next_month_adjusted",
            "train_ready_flag",
        ]
        all_features = [c for c in train_df.columns if c not in meta_cols]

        stages = self.get_stages_features(all_features)
        cv = TimeSeriesExpandingCV()

        records = []
        baseline_mae: Optional[float] = None

        self.logger.info("Starting 5-Stage Ablation Study across expanding-window CV...")

        for stage_idx, (stage_name, feat_cols) in enumerate(stages.items()):
            fold_maes: List[float] = []
            fold_rmses: List[float] = []
            fold_mapes: List[float] = []
            fold_r2s: List[float] = []

            for fold_idx, tr_idx, te_idx, test_year in cv.split(train_df):
                X_tr = train_df.loc[tr_idx, feat_cols]
                y_tr = train_df.loc[tr_idx, "target_downtown_adjusted"]
                X_te = train_df.loc[te_idx, feat_cols]
                y_te = train_df.loc[te_idx, "target_downtown_adjusted"]

                model = GBMModel(
                    n_estimators=100,
                    learning_rate=0.03,
                    max_depth=3,
                    num_leaves=12,
                    random_state=42,
                )
                model.fit(X_tr, y_tr)
                preds = model.predict(X_te)
                metrics = compute_metrics(y_te, preds)

                fold_maes.append(metrics["mae"])
                fold_rmses.append(metrics["rmse"])
                fold_mapes.append(metrics["mape"])
                fold_r2s.append(metrics["r2"])

            avg_mae = float(np.mean(fold_maes))
            avg_rmse = float(np.mean(fold_rmses))
            avg_mape = float(np.mean(fold_mapes))
            avg_r2 = float(np.mean(fold_r2s))

            if stage_idx == 0:
                baseline_mae = avg_mae
                mae_reduction = 0.0
            else:
                mae_reduction = ((baseline_mae - avg_mae) / baseline_mae) * 100.0

            records.append({
                "stage_idx": stage_idx,
                "stage_name": stage_name,
                "feature_count": len(feat_cols),
                "cv_mae": round(avg_mae, 2),
                "cv_rmse": round(avg_rmse, 2),
                "cv_mape_pct": round(avg_mape, 2),
                "cv_r2": round(avg_r2, 4),
                "mae_reduction_pct": round(mae_reduction, 2),
            })
            self.logger.info(
                f"{stage_name} ({len(feat_cols)} feats) -> MAE: {avg_mae:.2f}, RMSE: {avg_rmse:.2f}, Reduction: {mae_reduction:.2f}%"
            )

        ablation_df = pd.DataFrame(records)

        if output_csv is not None:
            output_csv.parent.mkdir(parents=True, exist_ok=True)
            ablation_df.to_csv(output_csv, index=False)
            self.logger.info(f"Saved ablation study to {output_csv}")

        return ablation_df

    def plot_ablation(
        self, ablation_df: pd.DataFrame, output_path: Path = Path("slide_assets/task10_ablation_performance.png")
    ) -> Path:
        """
        Generates a 300 DPI publication bar chart of MAE reduction across ablation stages.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), gridspec_kw={"width_ratios": [1.2, 1]})

        stage_labels = [
            "Stage 0\nUnivariate Lags\n(ARIMA Baseline)",
            "Stage 1\n+ Municipal 311\nEncampments",
            "Stage 2\n+ Weather &\nClimate",
            "Stage 3\n+ Economic Rent\n& Job Distress",
            "Stage 4\nFull Multi-Source\nEnsemble",
        ]
        maes = ablation_df["cv_mae"].values
        reductions = ablation_df["mae_reduction_pct"].values

        colors = ["#94A3B8", "#60A5FA", "#38BDF8", "#34D399", "#10B981"]

        # Bar chart for MAE
        bars = ax1.bar(range(len(stage_labels)), maes, color=colors, edgecolor="#1E293B", linewidth=1.2, width=0.6)
        ax1.set_xticks(range(len(stage_labels)))
        ax1.set_xticklabels(stage_labels, fontsize=10, fontweight="medium")
        ax1.set_ylabel("Cross-Validated MAE (Unsheltered People)", fontsize=11, fontweight="bold")
        ax1.set_title("Prediction Error (MAE) Across Cumulative Feature Stages", fontsize=12, fontweight="bold", pad=12)
        ax1.grid(axis="y", linestyle="--", alpha=0.4)

        for bar, mae in zip(bars, maes):
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 3.0,
                f"{mae:.1f}",
                ha="center",
                va="bottom",
                fontsize=11,
                fontweight="bold",
                color="#0F172A",
            )

        # Bar chart for MAE Reduction %
        bars2 = ax2.bar(
            range(len(stage_labels)),
            reductions,
            color=["#E2E8F0" if r == 0 else "#059669" for r in reductions],
            edgecolor="#1E293B",
            linewidth=1.2,
            width=0.6,
        )
        ax2.set_xticks(range(len(stage_labels)))
        ax2.set_xticklabels([s.split("\n")[0] for s in stage_labels], fontsize=10, fontweight="medium")
        ax2.set_ylabel("Error Reduction vs. Univariate Baseline (%)", fontsize=11, fontweight="bold")
        ax2.set_title("Incremental Accuracy Gain (% MAE Reduction)", fontsize=12, fontweight="bold", pad=12)
        ax2.grid(axis="y", linestyle="--", alpha=0.4)

        for bar, red in zip(bars2, reductions):
            if red > 0:
                ax2.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.5,
                    f"+{red:.1f}%",
                    ha="center",
                    va="bottom",
                    fontsize=11,
                    fontweight="bold",
                    color="#047857",
                )
            else:
                ax2.text(
                    bar.get_x() + bar.get_width() / 2,
                    1.0,
                    "Baseline",
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    fontstyle="italic",
                    color="#64748B",
                )

        fig.suptitle(
            "Task 10.3 Feature Domain Ablation: Demonstrating Value of Multi-Source Integration",
            fontsize=14,
            fontweight="bold",
            y=1.02,
        )
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        self.logger.info(f"Ablation figure saved to {output_path}")
        return output_path
