"""
Multi-Source Temporal Alignment Engine
Performs relational and temporal alignment of all ingested external streams
onto the canonical 108-month Downtown San Diego index (2017-01-01 to 2025-12-01),
joined with canonical monthly unsheltered counts from MasterCounts_Adjusted_v2.csv.
"""

import logging
from pathlib import Path
from typing import Optional
import pandas as pd

from .sources.weather_noaa import WeatherIngestionPipeline
from .sources.major_events import MajorEventsIngestionPipeline
from .sources.economic_indicators import EconomicIngestionPipeline
from .sources.shelter_capacity import ShelterCapacityIngestionPipeline
from .sources.get_it_done_311 import GetItDone311IngestionPipeline

logger = logging.getLogger(__name__)


class MultiSourceAligner:
    """
    Coordinates multi-source data extraction and aligns all feature columns
    onto a single canonical time series matrix.
    """

    START_DATE = "2017-01-01"
    END_DATE = "2025-12-01"

    def __init__(
        self,
        master_counts_path: Optional[Path] = None,
        output_path: Optional[Path] = None,
        cache_dir: Optional[Path] = None,
    ):
        self.master_counts_path = master_counts_path or Path("data/MasterCounts_Adjusted_v2.csv")
        self.output_path = output_path or Path("data/MultiSource_Master_Monthly.csv")
        self.cache_dir = cache_dir or Path("data/raw")
        self.logger = logging.getLogger(self.__class__.__name__)

        # Instantiate pipelines
        self.weather_pipe = WeatherIngestionPipeline(raw_cache_dir=self.cache_dir)
        self.events_pipe = MajorEventsIngestionPipeline(raw_cache_dir=self.cache_dir)
        self.econ_pipe = EconomicIngestionPipeline(raw_cache_dir=self.cache_dir)
        self.shelter_pipe = ShelterCapacityIngestionPipeline(raw_cache_dir=self.cache_dir)
        self.get_it_done_pipe = GetItDone311IngestionPipeline(raw_cache_dir=self.cache_dir)

    def extract_downtown_ground_truth(self) -> pd.DataFrame:
        """
        Loads canonical Downtown monthly adjusted and raw totals from MasterCounts_Adjusted_v2.csv.
        """
        if not self.master_counts_path.exists():
            raise FileNotFoundError(f"Master counts file not found at {self.master_counts_path}")

        df = pd.read_csv(self.master_counts_path)
        
        # Filter for aggregate neighborhood rows
        df_neigh = df[df["area_type"] == "neighborhood"].copy()
        
        # Total counts (adjusted and raw)
        df_tot = df_neigh[df_neigh["component"] == "total"]
        tot_agg = df_tot.groupby("date").agg(
            downtown_actual_adjusted_count=("total_count", "sum"),
            downtown_actual_raw_count=("raw_count", "sum"),
        ).reset_index()

        # Individual, vehicle, tent breakdown
        piv = df_neigh[df_neigh["component"].isin(["individual", "vehicle", "tent"])]
        piv_agg = piv.groupby(["date", "component"])["total_count"].sum().unstack(fill_value=0).reset_index()
        piv_agg = piv_agg.rename(columns={
            "individual": "downtown_actual_individual_count",
            "vehicle": "downtown_actual_vehicle_count",
            "tent": "downtown_actual_tent_count",
        })

        merged = pd.merge(tot_agg, piv_agg, on="date", how="left")
        merged["date"] = pd.to_datetime(merged["date"]).dt.strftime("%Y-%m-%d")
        merged = merged.sort_values("date").reset_index(drop=True)

        # Round counts and fill unsegmented historical subcomponents (2017) with 0.0
        merged["downtown_actual_adjusted_count"] = merged["downtown_actual_adjusted_count"].fillna(0.0).round(2)
        merged["downtown_actual_raw_count"] = merged["downtown_actual_raw_count"].fillna(0.0).round(2)
        merged["downtown_actual_individual_count"] = merged["downtown_actual_individual_count"].fillna(0.0).round(2)
        merged["downtown_actual_vehicle_count"] = merged["downtown_actual_vehicle_count"].fillna(0.0).round(2)
        merged["downtown_actual_tent_count"] = merged["downtown_actual_tent_count"].fillna(0.0).round(2)

        return merged

    def run_all(self, use_cache: bool = True) -> pd.DataFrame:
        """
        Executes all 5 pipelines and performs strict temporal merge.
        """
        self.logger.info("Executing MultiSourceAligner for period %s to %s", self.START_DATE, self.END_DATE)

        # 1. Base canonical counts (108 months)
        ground_truth_df = self.extract_downtown_ground_truth()
        self.logger.info("Extracted %d monthly ground-truth observations.", len(ground_truth_df))

        # 2. Extract external sources
        weather_df = self.weather_pipe.run(start_date=self.START_DATE, end_date=self.END_DATE, use_cache=use_cache)
        events_df = self.events_pipe.run(start_date=self.START_DATE, end_date=self.END_DATE, use_cache=use_cache)
        econ_df = self.econ_pipe.run(start_date=self.START_DATE, end_date=self.END_DATE, use_cache=use_cache)
        shelter_df = self.shelter_pipe.run(start_date=self.START_DATE, end_date=self.END_DATE, use_cache=use_cache)
        get_it_done_df = self.get_it_done_pipe.run(start_date=self.START_DATE, end_date=self.END_DATE, use_cache=use_cache)

        # 3. Sequential Left Joins on 'date'
        aligned = ground_truth_df.copy()
        aligned = pd.merge(aligned, weather_df, on="date", how="left")
        aligned = pd.merge(aligned, events_df, on="date", how="left")
        aligned = pd.merge(aligned, econ_df, on="date", how="left")
        aligned = pd.merge(aligned, shelter_df, on="date", how="left")
        aligned = pd.merge(aligned, get_it_done_df, on="date", how="left")

        # 4. Filter strictly to requested window
        aligned["date_dt"] = pd.to_datetime(aligned["date"])
        aligned = aligned[
            (aligned["date_dt"] >= pd.Timestamp(self.START_DATE))
            & (aligned["date_dt"] <= pd.Timestamp(self.END_DATE))
        ].drop(columns=["date_dt"]).sort_values("date").reset_index(drop=True)

        # 5. Save canonical multi-source dataset
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        aligned.to_csv(self.output_path, index=False)
        self.logger.info(
            "Saved aligned multi-source table (%d rows, %d columns) to %s",
            len(aligned),
            len(aligned.columns),
            self.output_path,
        )

        return aligned
