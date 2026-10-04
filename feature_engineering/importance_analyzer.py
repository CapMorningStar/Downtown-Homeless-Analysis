"""
Feature Importance & Interpretability Attribution Analyzer
Computes Permutation Importance with TimeSeriesSplit, Tree Gini Impurity,
and SHAP TreeExplainer attributions to rank the most predictive drivers of downtown unsheltered counts.
"""

import logging
from pathlib import Path
from typing import Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
import shap
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import TimeSeriesSplit

logger = logging.getLogger(__name__)


class FeatureImportanceAnalyzer:
    """
    Evaluates global feature predictive power using:
    1. Random Forest Gini Impurity (MDI)
    2. Time-Series Cross-Validated Permutation Importance
    3. SHAP (Shapley Additive exPlanations)
    4. Pearson Correlation
    """

    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = data_path or Path("data/FeatureMatrix_Comprehensive_67.csv")
        self.logger = logging.getLogger(self.__class__.__name__)

    def load_data(self) -> Tuple[pd.DataFrame, pd.Series, list]:
        if not self.data_path.exists():
            raise FileNotFoundError(f"Feature matrix not found at {self.data_path}")

        df = pd.read_csv(self.data_path)
        # Use complete training observations (2018–2025)
        train_df = df[df["train_ready_flag"] == 1].copy()

        target_col = "target_downtown_adjusted"
        exclude_cols = [
            "date",
            "target_downtown_adjusted",
            "target_downtown_raw",
            "target_next_month_adjusted",
            "train_ready_flag",
        ]
        feature_cols = [c for c in train_df.columns if c not in exclude_cols]

        X = train_df[feature_cols].copy()
        y = train_df[target_col].copy()

        return X, y, feature_cols

    @staticmethod
    def _categorize_feature(feat_name: str) -> str:
        """Assigns broad architectural domain category to feature name."""
        if feat_name.startswith("temporal_"):
            return "Temporal & Cyclical"
        elif feat_name.startswith("lag_") or feat_name.startswith("diff_") or "growth_" in feat_name or "ratio_" in feat_name:
            return "Autoregressive & Momentum"
        elif feat_name.startswith("rolling_") or feat_name.startswith("bollinger_") or feat_name.startswith("z_score_"):
            return "Rolling Window Envelopes"
        elif feat_name.startswith("spatial_"):
            return "Spatial Concentration"
        elif "311" in feat_name:
            return "Municipal 311 Encampments"
        elif "weather_" in feat_name or "temp" in feat_name or "precip" in feat_name:
            return "Meteorology & Climate"
        elif "events_" in feat_name or "padres" in feat_name or "shelter_" in feat_name or "camping_ban" in feat_name or "policy_" in feat_name:
            return "Civic Events & Shelter Policy"
        elif "unemployment" in feat_name or "rent_" in feat_name or "real_rent" in feat_name:
            return "Macroeconomic Distress"
        else:
            return "Other Exogenous"

    def run_analysis(self) -> pd.DataFrame:
        """
        Executes models, computes metrics, and produces ranked feature summary table.
        """
        self.logger.info("Starting multi-method feature importance analysis...")
        X, y, feature_cols = self.load_data()

        # 1. Train Random Forest model
        rf = RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42)
        rf.fit(X, y)
        r2 = rf.score(X, y)
        self.logger.info("Random Forest fitted successfully. In-sample R^2 = %.4f", r2)

        # 2. Gini Impurity (MDI)
        gini_importances = rf.feature_importances_

        # 3. TimeSeriesSplit Permutation Importance
        tscv = TimeSeriesSplit(n_splits=5)
        perm_scores = []
        for train_idx, test_idx in tscv.split(X):
            X_tr, y_tr = X.iloc[train_idx], y.iloc[train_idx]
            X_te, y_te = X.iloc[test_idx], y.iloc[test_idx]
            fold_rf = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)
            fold_rf.fit(X_tr, y_tr)
            perm = permutation_importance(fold_rf, X_te, y_te, n_repeats=5, random_state=42)
            perm_scores.append(perm.importances_mean)
        mean_perm_importance = np.mean(perm_scores, axis=0)

        # 4. SHAP Values
        explainer = shap.TreeExplainer(rf)
        shap_values = explainer.shap_values(X)
        mean_abs_shap = np.mean(np.abs(shap_values), axis=0)

        # 5. Pearson Correlations with Target
        corrs = []
        p_vals = []
        for c in feature_cols:
            r, p = pearsonr(X[c], y)
            corrs.append(round(r, 4))
            p_vals.append(round(p, 6))

        # Assemble summary dataframe
        summary_df = pd.DataFrame(
            {
                "feature_name": feature_cols,
                "category": [self._categorize_feature(c) for c in feature_cols],
                "mean_abs_shap": np.round(mean_abs_shap, 2),
                "permutation_importance": np.round(mean_perm_importance, 4),
                "gini_importance": np.round(gini_importances, 4),
                "pearson_r": corrs,
                "p_value": p_vals,
            }
        )

        # Rank primarily by SHAP attribution, tie-broken by Gini
        summary_df = summary_df.sort_values(by=["mean_abs_shap", "gini_importance"], ascending=[False, False]).reset_index(drop=True)
        summary_df["rank"] = summary_df.index + 1

        self.logger.info("Feature importance analysis complete. Top driver: %s", summary_df.iloc[0]["feature_name"])
        return summary_df

    def generate_importance_plot(
        self,
        summary_df: Optional[pd.DataFrame] = None,
        output_path: Optional[Path] = None,
        top_n: int = 15,
    ) -> Path:
        """
        Generates and saves high-resolution publication plot of top features.
        """
        if summary_df is None:
            summary_df = self.run_analysis()

        save_path = output_path or Path("slide_assets/task10_feature_importance.png")
        save_path.parent.mkdir(parents=True, exist_ok=True)

        top_df = summary_df.head(top_n).sort_values("mean_abs_shap", ascending=True)

        # Set up aesthetic Canva/Executive style
        fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FAFAFB")

        # Color mapping by category
        cat_palette = {
            "Autoregressive & Momentum": "#1E3A8A",      # Deep Navy
            "Rolling Window Envelopes": "#2563EB",       # Royal Blue
            "Spatial Concentration": "#0D9488",          # Teal
            "Civic Events & Shelter Policy": "#D97706",  # Amber
            "Macroeconomic Distress": "#DC2626",         # Crimson
            "Municipal 311 Encampments": "#7C3AED",      # Purple
            "Meteorology & Climate": "#059669",          # Green
            "Temporal & Cyclical": "#64748B",            # Slate
        }
        bar_colors = [cat_palette.get(cat, "#3B82F6") for cat in top_df["category"]]

        y_pos = np.arange(len(top_df))
        bars = ax.barh(y_pos, top_df["mean_abs_shap"], color=bar_colors, height=0.65, edgecolor="none")

        ax.set_yticks(y_pos)
        ax.set_yticklabels(top_df["feature_name"], fontsize=9.5, fontweight="medium", color="#1F2937")
        ax.set_xlabel("Mean Absolute SHAP Attribution (|Δ Unsheltered Individuals|)", fontsize=10, fontweight="bold", color="#374151")
        ax.set_title(
            f"Top {top_n} Predictive Drivers: Downtown San Diego Unsheltered Counts\n(Task 10.2 Comprehensive Multi-Source Attribution)",
            fontsize=12,
            fontweight="bold",
            color="#111827",
            pad=15,
        )

        # Value annotations
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + 1.5,
                bar.get_y() + bar.get_height() / 2,
                f"{width:.1f}",
                va="center",
                ha="left",
                fontsize=8.5,
                fontweight="semibold",
                color="#4B5563",
            )

        ax.grid(axis="x", linestyle="--", alpha=0.5, color="#D1D5DB")
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#9CA3AF")
        ax.spines["bottom"].set_color("#9CA3AF")

        plt.tight_layout()
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        self.logger.info("Saved feature importance chart to %s", save_path)
        return save_path
