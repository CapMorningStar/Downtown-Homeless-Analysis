"""
Base Ingestion Pipeline Interface
Defines the standard operational lifecycle for external data ingestion modules.
"""

from abc import ABC, abstractmethod
import logging
from pathlib import Path
from typing import Optional
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


class BaseIngestionPipeline(ABC):
    """
    Abstract base class providing standard extraction, cleaning, monthly resampling,
    schema validation, and local caching protocols.
    """

    def __init__(self, raw_cache_dir: Optional[Path] = None):
        self.raw_cache_dir = raw_cache_dir or Path("data/raw")
        self.raw_cache_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Unique identifier name for this data source."""
        pass

    @abstractmethod
    def fetch_raw(self, use_cache: bool = True) -> pd.DataFrame:
        """
        Fetch raw observations from external API, portal, or local cache.
        """
        pass

    @abstractmethod
    def clean_and_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Perform column renaming, type casting, spatial clipping, and categorical filtering.
        """
        pass

    @abstractmethod
    def aggregate_monthly(
        self,
        df: pd.DataFrame,
        start_date: str = "2017-01-01",
        end_date: str = "2025-12-01",
    ) -> pd.DataFrame:
        """
        Resample and aggregate observations onto monthly index (YYYY-MM-01).
        """
        pass

    @abstractmethod
    def validate_schema(self, df: pd.DataFrame) -> bool:
        """
        Verify presence of expected schema columns, non-empty observations, and bounds.
        """
        pass

    def run(
        self,
        start_date: str = "2017-01-01",
        end_date: str = "2025-12-01",
        use_cache: bool = True,
    ) -> pd.DataFrame:
        """
        Execute end-to-end ingestion lifecycle and return monthly aligned dataframe.
        """
        self.logger.info("Starting ingestion lifecycle for source: %s", self.source_name)
        raw_df = self.fetch_raw(use_cache=use_cache)
        self.logger.info("Fetched %d raw records for %s", len(raw_df), self.source_name)

        cleaned_df = self.clean_and_transform(raw_df)
        self.logger.info("Cleaned and transformed %d records for %s", len(cleaned_df), self.source_name)

        monthly_df = self.aggregate_monthly(cleaned_df, start_date=start_date, end_date=end_date)
        self.logger.info("Aggregated %d monthly records for %s", len(monthly_df), self.source_name)

        if not self.validate_schema(monthly_df):
            error_msg = f"Schema validation failed for {self.source_name}"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        self.logger.info("Successfully completed ingestion for %s", self.source_name)
        return monthly_df
