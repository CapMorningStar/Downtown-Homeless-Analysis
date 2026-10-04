#!/usr/bin/env python3
"""
Ensemble Prediction System & Uncertainty Calibration (Task 10.3)
Downtown San Diego Homeless Population Analysis

Integrates:
1. Gradient Boosted Decision Trees (LightGBM / XGBoost)
2. Bayesian Structural Time Series (BSTS via State-Space Kalman Filtering)
3. Standardized Temporal Neural Network (Deep MLP with Adaptive Regularization)
4. Constrained Non-Negative Least Squares Stacking Meta-Learner (sum(w) = 1, w >= 0)
5. Calibrated Conformal Prediction Intervals (80% and 95%)
6. 5-Stage Feature Domain Ablation Engine

Usage:
    python ensemble_model.py --train --evaluate --ablation --plot
    python ensemble_model.py --train --evaluate
    python ensemble_model.py --ablation
"""

import argparse
import logging
from pathlib import Path
import sys
import pandas as pd

from ensemble_modeling.pipeline import EnsemblePipeline
from ensemble_modeling.ablation import AblationStudyEngine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("ensemble_model")


def print_banner(text: str):
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Task 10.3 Multi-Source Ensemble Prediction & Anomaly System")
    parser.add_argument("--train", action="store_true", help="Fit models and run expanding-window cross-validation")
    parser.add_argument("--evaluate", action="store_true", help="Print detailed fold and aggregate econometric metrics")
    parser.add_argument("--ablation", action="store_true", help="Run 5-stage feature domain ablation study")
    parser.add_argument("--plot", action="store_true", help="Export publication charts to slide_assets/")
    parser.add_argument("--data", type=str, default="data/FeatureMatrix_Comprehensive_67.csv", help="Input feature matrix")
    parser.add_argument("--output-dir", type=str, default="data", help="Output directory for predictions and tables")

    args = parser.parse_args()

    # Default to running all components if no flags are given
    if not (args.train or args.evaluate or args.ablation or args.plot):
        args.train = True
        args.evaluate = True
        args.ablation = True
        args.plot = True

    data_path = Path(args.data)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    pipeline = EnsemblePipeline(data_path=data_path)

    oof_df = None
    forecast_df = None
    fold_metrics_df = None
    overall_metrics = None

    if args.train or args.evaluate:
        print_banner("1. 5-FOLD EXPANDING-WINDOW TIME-SERIES CROSS-VALIDATION")
        fold_metrics_df, oof_df, overall_metrics = pipeline.run_cv_evaluation()

        print("\n--- PER-FOLD METRICS (2021–2025 TEST HORIZONS) ---")
        pd.set_option("display.max_columns", 12)
        pd.set_option("display.width", 130)
        display_cols = [
            "fold", "test_year", "train_months", "base_mae", "gbm_mae", "bsts_mae", "neural_mae", "ens_mae", "ens_rmse", "ens_r2"
        ]
        print(fold_metrics_df[display_cols].to_string(index=False))

        print_banner("2. OVERALL OUT-OF-SAMPLE ACCURACY BENCHMARK")
        summary_records = []
        for model_name, m in overall_metrics.items():
            summary_records.append({
                "Architecture": model_name,
                "MAE": m["mae"],
                "RMSE": m["rmse"],
                "MAPE (%)": f"{m['mape']:.2f}%",
                "MDA (%)": f"{m['mda']:.2f}%",
                "R²": m["r2"],
            })
        print(pd.DataFrame(summary_records).to_string(index=False))

        print_banner("3. FULL MODEL FITTING & CONSTRAINED STACKING OPTIMIZATION")
        meta_learner, conformal = pipeline.fit_full_and_calibrate(oof_df)
        print("\nOptimal Constrained Meta-Learner Stacking Weights (sum = 1.0, w >= 0):")
        for m_name, w in meta_learner.weights_dict.items():
            print(f"  • {m_name:18s}: {w * 100:.2f}%")

        print("\nCalibrated Conformal Prediction Intervals (Finite-Sample Non-Parametric):")
        cov_eval = conformal.evaluate_coverage(oof_df["y_true"], oof_df["pred_ensemble"])
        for conf_lvl, stats in cov_eval.items():
            print(f"  • {conf_lvl} Nominal Interval: Empirical Coverage = {stats['empirical_coverage_pct']:.1f}% | Margin = ±{stats['margin_error']:.1f} unsheltered count")

        print_banner("4. PROSPECTIVE 2026 FORECAST GENERATION")
        forecast_df = pipeline.generate_prospective_forecast_2026(n_months=12)
        print(forecast_df[["date", "pred_ensemble", "conformal_lower_80", "conformal_upper_80", "conformal_lower_95", "conformal_upper_95"]].to_string(index=False))

        # Save predictions
        oof_path = out_dir / "Ensemble_Predictions_OOF.csv"
        oof_df.to_csv(oof_path, index=False)
        forecast_path = out_dir / "Ensemble_Forecast_2026.csv"
        forecast_df.to_csv(forecast_path, index=False)
        print(f"\n✓ Saved OOF predictions to {oof_path}")
        print(f"✓ Saved 2026 forecast to {forecast_path}")

    if args.ablation:
        print_banner("5. 5-STAGE CUMULATIVE FEATURE DOMAIN ABLATION STUDY")
        ablation_engine = AblationStudyEngine(data_path=data_path)
        ablation_csv = out_dir / "Ensemble_AblationStudy.csv"
        ablation_df = ablation_engine.run_ablation(output_csv=ablation_csv)

        print("\nAblation Progression Across Orthogonal Data Domains:")
        print(ablation_df[["stage_name", "feature_count", "cv_mae", "cv_rmse", "mae_reduction_pct"]].to_string(index=False))

        if args.plot:
            ablation_plot = Path("slide_assets/task10_ablation_performance.png")
            ablation_engine.plot_ablation(ablation_df, output_path=ablation_plot)
            print(f"✓ Exported ablation visualization to {ablation_plot}")

    if args.plot and oof_df is not None and forecast_df is not None:
        print_banner("6. PUBLICATION PREDICTION PLOT EXPORT")
        pred_plot = Path("slide_assets/task10_ensemble_predictions.png")
        pipeline.plot_ensemble_results(oof_df, forecast_df, output_path=pred_plot)
        print(f"✓ Exported ensemble predictions chart to {pred_plot}")

    print_banner("TASK 10.3 EXECUTION COMPLETE")


if __name__ == "__main__":
    main()
