"""
Master Feature Engineering Pipeline
Orchestrates temporal, autoregressive, rolling window, spatial, and interaction feature extraction.
Produces the canonical FeatureMatrix_Comprehensive_68.csv dataset for downstream predictive modeling.
"""

import logging
from pathlib import Path
from typing import Optional
import numpy as np
import pandas as pd

from .temporal import generate_temporal_features
from .autoregressive import generate_autoregressive_features
from .rolling_windows import generate_rolling_features
from .spatial_features import generate_spatial_features
from .interactions import generate_interaction_features

logger = logging.getLogger(__name__)


class FeatureEngineeringPipeline:
    """
    Orchestrates the construction of 68 engineered features from the multi-source monthly matrix.
    Enforces strict temporal order and produces both contemporaneous and 1-month-forward targets.
    """

    DEFAULT_INPUT = Path("data/MultiSource_Master_Monthly.csv")
    DEFAULT_OUTPUT = Path("data/FeatureMatrix_Comprehensive_68.csv")

    def __init__(
        self,
        input_path: Optional[Path] = None,
        output_path: Optional[Path] = None,
        master_counts_path: Optional[Path] = None,
    ):
        self.input_path = input_path or self.DEFAULT_INPUT
        self.output_path = output_path or self.DEFAULT_OUTPUT
        self.master_counts_path = master_counts_path or Path("data/MasterCounts_Adjusted_v2.csv")
        self.logger = logging.getLogger(self.__class__.__name__)

    def load_input_data(self) -> pd.DataFrame:
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input multi-source file not found: {self.input_path}")
        return pd.read_csv(self.input_path)

    def build_feature_matrix(self, fill_initial_lags: bool = True) -> pd.DataFrame:
        """
        Executes all 5 feature generators and concatenates them into a single dataframe.
        """
        self.logger.info("Loading input multi-source matrix from %s", self.input_path)
        actual_df = self.load_input_data()
        # Unpublished months (downtown_count_released == 0) have NaN counts. Features are built from a
        # copy where those months are time-interpolated (as in Tasks 4.1/7.1); targets keep the NaN.
        raw_df = actual_df.copy()
        count_cols = [c for c in raw_df.columns if c.startswith("downtown_actual_")]
        idx = pd.to_datetime(raw_df["date"])
        for col in count_cols:
            raw_df[col] = (pd.Series(raw_df[col].values, index=idx)
                           .interpolate(method="time", limit_direction="both").values)

        self.logger.info("Generating temporal & cyclical features (9)...")
        df_temporal = generate_temporal_features(raw_df)

        self.logger.info("Generating autoregressive & momentum features (15)...")
        df_autoreg = generate_autoregressive_features(raw_df)

        self.logger.info("Generating rolling window & volatility envelope features (15)...")
        df_rolling = generate_rolling_features(raw_df)

        self.logger.info("Generating spatial distribution & HHI features (5)...")
        df_spatial = generate_spatial_features(
            master_counts_path=self.master_counts_path,
            canonical_dates=raw_df["date"],
        )

        self.logger.info("Generating cross-domain interaction & anomaly features (24)...")
        df_interact = generate_interaction_features(raw_df)

        # Targets & Identifiers
        meta_df = pd.DataFrame(index=raw_df.index)
        meta_df["date"] = raw_df["date"]
        meta_df["target_downtown_adjusted"] = actual_df["downtown_actual_adjusted_count"]
        meta_df["target_downtown_raw"] = actual_df["downtown_actual_raw_count"]
        # Prospective 1-month ahead prediction target: y_{t+1}
        meta_df["target_next_month_adjusted"] = actual_df["downtown_actual_adjusted_count"].shift(-1)

        # Training ready flag: 2018-2025 (12M lookback observed) AND the month's count was published
        dt_series = pd.to_datetime(raw_df["date"])
        released = actual_df["downtown_actual_adjusted_count"].notna()
        meta_df["train_ready_flag"] = ((dt_series >= pd.Timestamp("2018-01-01")) & released).astype(int)

        # Concatenate all blocks
        features_only = pd.concat([df_temporal, df_autoreg, df_rolling, df_spatial, df_interact], axis=1)

        if fill_initial_lags:
            # Backfill initial 2017 lag boundary NaNs so regression models can train cleanly
            features_clean = features_only.bfill().fillna(0.0)
        else:
            features_clean = features_only

        full_matrix = pd.concat([meta_df, features_clean], axis=1)

        self.logger.info(
            "Feature matrix built successfully: %d rows, %d total columns (%d engineered features).",
            len(full_matrix),
            len(full_matrix.columns),
            len(features_clean.columns),
        )

        return full_matrix

    def run(self, fill_initial_lags: bool = True) -> pd.DataFrame:
        """
        Executes pipeline and saves the feature matrix to output_path.
        """
        matrix = self.build_feature_matrix(fill_initial_lags=fill_initial_lags)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        matrix.to_csv(self.output_path, index=False)
        self.logger.info("Saved canonical comprehensive feature matrix to %s", self.output_path)
        return matrix
