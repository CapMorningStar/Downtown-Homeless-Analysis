"""
Master Anomaly Surveillance Pipeline (Task 10.4)
Coordinates:
- Statistical Surveillance (Shewhart 2σ/3σ, Tabular CUSUM)
- Model-Based Surveillance (Isolation Forest, Conformal Residuals)
- 4-Quadrant Anomaly Taxonomy Classification
- Historical Ground-Truth Benchmark Validation
- Alert Dispatching & Persistent Audit Trail Updates
- 300 DPI Publication Figure Generation
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .control_charts import ShewhartControlChart, TabularCUSUM
from .model_detectors import IsolationForestDetector, ConformalResidualDetector
from .classifier import AnomalyClassifier
from .historical_validator import HistoricalBenchmarkValidator
from .alerting import AlertEngine

logger = logging.getLogger(__name__)


class AnomalySurveillancePipeline:
    """
    Coordinates end-to-end anomaly surveillance, classification, alerting, and reporting.
    """

    def __init__(
        self,
        feature_data_path: Optional[Path] = None,
        oof_predictions_path: Optional[Path] = None,
    ):
        self.feature_data_path = feature_data_path or Path("data/FeatureMatrix_Comprehensive_68.csv")
        self.oof_predictions_path = oof_predictions_path or Path("data/Ensemble_Predictions_OOF.csv")
        self.logger = logging.getLogger(self.__class__.__name__)
        self.shewhart = ShewhartControlChart(window=12, min_periods=6, warning_sigma=2.0, critical_sigma=3.0)
        self.cusum = TabularCUSUM(slack_k=0.5, threshold_h=4.0, window=12)
        self.iso_forest = IsolationForestDetector(contamination=0.08, random_state=42)
        self.conformal = ConformalResidualDetector(conformal_margin=761.15)
        self.classifier = AnomalyClassifier()
        self.validator = HistoricalBenchmarkValidator()
        self.alert_engine = AlertEngine()

    def run_surveillance(self) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
        """
        Runs dual detection engines, classifies anomalies, validates benchmarks, and stores alerts.
        """
        if not self.feature_data_path.exists():
            raise FileNotFoundError(f"Feature matrix not found at {self.feature_data_path}")

        df = pd.read_csv(self.feature_data_path)
        train_df = df[df["train_ready_flag"] == 1].copy().reset_index(drop=True)
        train_df["date"] = pd.to_datetime(train_df["date"])
        dates = train_df["date"]
        y = train_df["target_downtown_adjusted"]

        meta_cols = [
            "date", "target_downtown_adjusted", "target_downtown_raw",
            "target_next_month_adjusted", "train_ready_flag",
        ]
        feat_cols = [c for c in train_df.columns if c not in meta_cols]
        X = train_df[feat_cols]

        self.logger.info("Executing Statistical Surveillance (Shewhart & CUSUM)...")
        shew_df = self.shewhart.fit_detect(y, dates=dates)
        cusum_df = self.cusum.fit_detect(y, dates=dates)

        self.logger.info("Executing Model-Based Surveillance (Isolation Forest & Conformal)...")
        iso_df = self.iso_forest.fit_detect(X, dates=dates)

        # Conformal residuals: use OOF predictions if available or fallback to rolling center line
        if self.oof_predictions_path.exists():
            oof_df = pd.read_csv(self.oof_predictions_path)
            oof_df["date"] = pd.to_datetime(oof_df["date"])
            merged_oof = pd.merge(train_df[["date", "target_downtown_adjusted"]], oof_df[["date", "pred_ensemble"]], on="date", how="left")
            y_pred = merged_oof["pred_ensemble"].fillna(shew_df["center_line"]).values
        else:
            y_pred = shew_df["center_line"].values

        conf_df = self.conformal.detect_residuals(y, y_pred, dates=dates)

        # Merge all signals
        merged_signals = pd.concat([
            shew_df,
            cusum_df.drop(columns=["date"]),
            iso_df.drop(columns=["date"]),
            conf_df.drop(columns=["date", "actual_count"]),
        ], axis=1)

        self.logger.info("Classifying anomalies across 4-quadrant taxonomy...")
        classified_df = self.classifier.classify(merged_signals, feature_df=train_df)

        self.logger.info("Validating against historical benchmark policy shocks...")
        event_df, global_metrics = self.validator.validate(classified_df)

        # Months DSDP has not published are excluded from surveillance (train_ready_flag == 0) and
        # recorded here as data-quality alerts, after validation so they do not count as shock detections.
        gap_rows = df[(pd.to_datetime(df["date"]) >= pd.Timestamp("2018-01-01")) & df["target_downtown_adjusted"].isna()]
        if len(gap_rows):
            gaps = pd.DataFrame({
                "date": pd.to_datetime(gap_rows["date"]).values,
                "value": np.nan,
                "center_line": np.nan,
                "anomaly_typology": "Potential Data Quality Issue",
                "anomaly_severity": "WARNING",
                "anomaly_description": "Monthly count not published by DSDP (reporting gap); excluded from modeling.",
                "is_classified_anomaly": True,
            })
            classified_df = pd.concat([classified_df, gaps], ignore_index=True).sort_values("date").reset_index(drop=True)

        self.logger.info("Ingesting anomalies into persistent Alert Store...")
        alerts_list = self.alert_engine.ingest_anomalies(classified_df)

        summary = {
            "total_months": len(classified_df),
            "total_anomalies_detected": int(classified_df["is_classified_anomaly"].sum()),
            "count_spikes": int((classified_df["anomaly_typology"] == "Count Spike").sum()),
            "count_drops": int((classified_df["anomaly_typology"] == "Count Drop").sum()),
            "spatial_shifts": int((classified_df["anomaly_typology"] == "Spatial Shift").sum()),
            "data_quality_issues": int((classified_df["anomaly_typology"] == "Potential Data Quality Issue").sum()),
            "validation_metrics": global_metrics,
            "total_active_alerts": len(alerts_list),
        }

        return classified_df, event_df, summary

    def plot_control_charts(
        self,
        classified_df: pd.DataFrame,
        output_path: Path = Path("slide_assets/task10_control_charts.png"),
    ) -> Path:
        """
        Creates a 300 DPI publication quality control chart and CUSUM accumulator visual.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        dates = pd.to_datetime(classified_df["date"])
        y = classified_df["value"].values
        cl = classified_df["center_line"].values
        ucl_w = classified_df["ucl_warning"].values
        lcl_w = classified_df["lcl_warning"].values
        ucl_c = classified_df["ucl_critical"].values
        lcl_c = classified_df["lcl_critical"].values

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 9), sharex=True, gridspec_kw={"height_ratios": [2.2, 1]})

        # Panel 1: Shewhart Control Chart
        ax1.plot(dates, y, color="#0F172A", linewidth=2.2, marker="o", markersize=4, label="Monthly Count (Adjusted)", zorder=5)
        ax1.plot(dates, cl, color="#2563EB", linewidth=1.8, linestyle="--", label="12-Month Rolling Mean (Center Line)", zorder=4)

        # Control bands
        ax1.fill_between(dates, lcl_w, ucl_w, color="#FEF3C7", alpha=0.65, label="±2σ Warning Limits", zorder=2)
        ax1.fill_between(dates, lcl_c, ucl_c, color="#FEE2E2", alpha=0.45, label="±3σ Critical Action Limits", zorder=1)

        # Highlight anomalies by category
        anom_mask = classified_df["is_classified_anomaly"]
        for typology, color, marker in [
            ("Count Spike", "#DC2626", "^"),
            ("Count Drop", "#2563EB", "v"),
            ("Spatial Shift", "#D97706", "s"),
            ("Potential Data Quality Issue", "#9333EA", "D"),
        ]:
            subset = classified_df[anom_mask & (classified_df["anomaly_typology"] == typology)]
            if not subset.empty:
                ax1.scatter(
                    pd.to_datetime(subset["date"]),
                    subset["value"],
                    color=color,
                    s=80,
                    marker=marker,
                    edgecolors="#0F172A",
                    linewidth=1.2,
                    label=f"Anomaly: {typology}",
                    zorder=6,
                )

        # Policy shock milestones
        ax1.axvline(pd.to_datetime("2020-04-01"), color="#64748B", linestyle=":", alpha=0.7)
        ax1.text(pd.to_datetime("2020-04-01"), 1900, " COVID Demobilization", color="#475569", fontsize=8.5, rotation=90)
        ax1.axvline(pd.to_datetime("2023-07-01"), color="#EF4444", linestyle=":", alpha=0.7)
        ax1.text(pd.to_datetime("2023-07-01"), 1900, " Camping Ban Enacted", color="#B91C1C", fontsize=8.5, rotation=90)

        ax1.set_title("Task 10.4 Statistical Quality Control Surveillance: Shewhart Limits & Tabular CUSUM", fontsize=13, fontweight="bold", pad=12)
        ax1.set_ylabel("Unsheltered Homeless Count", fontsize=10, fontweight="bold")
        ax1.grid(True, linestyle="--", alpha=0.4)
        ax1.legend(loc="upper left", framealpha=0.9, fontsize=8.5, ncol=2)

        # Panel 2: Tabular CUSUM Accumulators
        s_pos = classified_df["cusum_s_pos"].values
        s_neg = classified_df["cusum_s_neg"].values
        h = classified_df["cusum_threshold"].iloc[0]

        ax2.bar(dates, s_pos, width=20, color="#DC2626", alpha=0.75, label="CUSUM Positive Drift (S⁺)", zorder=3)
        ax2.bar(dates, -s_neg, width=20, color="#2563EB", alpha=0.75, label="CUSUM Negative Drift (S⁻)", zorder=3)
        ax2.axhline(h, color="#991B1B", linestyle="--", linewidth=1.5, label=f"Decision Threshold (+h={h})", zorder=4)
        ax2.axhline(-h, color="#1E40AF", linestyle="--", linewidth=1.5, label=f"Decision Threshold (-h=-{h})", zorder=4)
        ax2.axhline(0, color="#0F172A", linewidth=1.0)

        ax2.set_ylabel("CUSUM Accumulator (S)", fontsize=10, fontweight="bold")
        ax2.grid(True, linestyle="--", alpha=0.4)
        ax2.legend(loc="upper left", framealpha=0.9, fontsize=8.5, ncol=2)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        self.logger.info(f"Control charts figure saved to {output_path}")
        return output_path

    def plot_anomaly_classification(
        self,
        classified_df: pd.DataFrame,
        event_df: pd.DataFrame,
        output_path: Path = Path("slide_assets/task10_anomaly_classification.png"),
    ) -> Path:
        """
        Creates a 300 DPI publication graphic displaying taxonomy proportions and historical validation rate.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={"width_ratios": [1, 1.3]})

        # Panel 1: Typology Distribution Pie
        counts = classified_df[classified_df["is_classified_anomaly"]]["anomaly_typology"].value_counts()
        colors = {"Count Spike": "#EF4444", "Count Drop": "#3B82F6", "Spatial Shift": "#F59E0B", "Potential Data Quality Issue": "#8B5CF6"}
        pie_colors = [colors.get(t, "#94A3B8") for t in counts.index]

        wedges, texts, autotexts = ax1.pie(
            counts.values,
            labels=counts.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=pie_colors,
            wedgeprops={"edgecolor": "#1E293B", "linewidth": 1.2},
            textprops={"fontsize": 10, "fontweight": "medium"},
        )
        for at in autotexts:
            at.set_color("white")
            at.set_fontweight("bold")
        ax1.set_title("Distribution of Detected Anomalies by Typology", fontsize=12, fontweight="bold", pad=12)

        # Panel 2: Historical Benchmark Sensitivity
        events = event_df["event_name"].values
        rates = event_df["detection_rate_pct"].values

        bars = ax2.barh(events, rates, color="#10B981", edgecolor="#065F46", linewidth=1.2, height=0.55)
        ax2.set_xlim(0, 115)
        ax2.set_xlabel("Historical Detection Sensitivity Rate (%)", fontsize=10, fontweight="bold")
        ax2.set_title("Ground-Truth Benchmark Policy Validation (TPR)", fontsize=12, fontweight="bold", pad=12)
        ax2.grid(axis="x", linestyle="--", alpha=0.4)

        for bar, rate in zip(bars, rates):
            ax2.text(
                bar.get_width() + 2.0,
                bar.get_y() + bar.get_height() / 2,
                f"{rate:.1f}%",
                va="center",
                fontsize=11,
                fontweight="bold",
                color="#065F46",
            )

        fig.suptitle("Task 10.4 Anomaly Taxonomy & Benchmark Validation Performance", fontsize=13, fontweight="bold", y=1.02)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        self.logger.info(f"Anomaly classification visual saved to {output_path}")
        return output_path
