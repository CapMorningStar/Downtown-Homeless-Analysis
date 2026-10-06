#!/usr/bin/env python3
"""
Comprehensive Feature Engineering Module (Task 10.2)
Downtown San Diego Homeless Population Analysis

Builds 68 engineered features across 7 orthogonal domains:
1. Temporal & Cyclical
2. Autoregressive Lags & Momentum
3. Rolling Window Statistics & Envelopes
4. Spatial Geographic Concentration (HHI)
5. Municipal 311 Encampment Signals
6. Meteorological & Climate Anomalies
7. Civic Events, Shelter Capacities & Macroeconomic Rent Distress

Usage:
    python feature_engineering.py --generate --analyze
    python feature_engineering.py --generate
    python feature_engineering.py --analyze
"""

import argparse
import logging
import sys
from pathlib import Path
import pandas as pd

from feature_engineering.pipeline import FeatureEngineeringPipeline
from feature_engineering.importance_analyzer import FeatureImportanceAnalyzer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("feature_engineering")


def main():
    parser = argparse.ArgumentParser(description="Task 10.2 Feature Engineering Pipeline & Attribution Analyzer")
    parser.add_argument("--generate", action="store_true", help="Generate and save comprehensive feature matrix")
    parser.add_argument("--analyze", action="store_true", help="Run tree-based, permutation, and SHAP importance analysis")
    parser.add_argument("--output", type=str, default="data/FeatureMatrix_Comprehensive_68.csv", help="Output path")
    parser.add_argument("--plot", type=str, default="slide_assets/task10_feature_importance.png", help="Plot save path")

    args = parser.parse_args()

    if not args.generate and not args.analyze:
        parser.print_help()
        sys.exit(0)

    output_path = Path(args.output)

    if args.generate:
        logger.info("Executing comprehensive feature generation...")
        pipeline = FeatureEngineeringPipeline(output_path=output_path)
        feature_df = pipeline.run(fill_initial_lags=True)

        meta_cols = ["date", "target_downtown_adjusted", "target_downtown_raw", "target_next_month_adjusted", "train_ready_flag"]
        engineered_cols = [c for c in feature_df.columns if c not in meta_cols]

        print("\n=======================================================")
        print("✓ COMPREHENSIVE FEATURE MATRIX GENERATED SUCCESSFULLY")
        print("=======================================================")
        print(f"Destination: {output_path}")
        print(f"Total Rows: {len(feature_df)} months (2017-01-01 to 2025-12-01)")
        print(f"Total Columns: {len(feature_df.columns)}")
        print(f"Engineered Features Count: {len(engineered_cols)} (Mandate was 50+)")
        print(f"Training Ready Subset (2018-2025): {feature_df['train_ready_flag'].sum()} months")
        print("=======================================================\n")

    if args.analyze:
        logger.info("Running Feature Importance & Attribution Analyzer...")
        analyzer = FeatureImportanceAnalyzer(data_path=output_path)
        summary_df = analyzer.run_analysis()
        plot_path = analyzer.generate_importance_plot(summary_df, output_path=Path(args.plot), top_n=20)

        print("\n=======================================================")
        print("TOP 20 PREDICTIVE DRIVERS (SHAP, PERMUTATION & GINI)")
        print("=======================================================")
        top20 = summary_df.head(20)[
            ["rank", "feature_name", "category", "mean_abs_shap", "permutation_importance", "gini_importance", "pearson_r"]
        ]
        pd.set_option("display.max_columns", 10)
        pd.set_option("display.width", 120)
        print(top20.to_string(index=False))
        print("=======================================================")
        print(f"✓ Publication chart exported to: {plot_path}\n")


if __name__ == "__main__":
    main()
