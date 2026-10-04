"""
Macroeconomic Ingestion Pipeline
Ingests San Diego County Unemployment Rate (FRED CASAND5URN),
San Diego-Carlsbad Consumer Price Index (FRED CUUSA429SA0),
and Zillow Observed Rent Index (ZORI) for Downtown ZIP 92101 and San Diego Metro.
"""

import io
import logging
from pathlib import Path
from typing import Optional
import urllib.request
import numpy as np
import pandas as pd

from ..base import BaseIngestionPipeline

logger = logging.getLogger(__name__)


class EconomicIngestionPipeline(BaseIngestionPipeline):
    """
    Ingests macroeconomic drivers:
    - San Diego County Unemployment Rate (FRED CASAND5URN)
    - San Diego-Carlsbad CPI (FRED CUUSA429SA0)
    - Zillow Observed Rent Index for ZIP 92101 and Metro
    """

    FRED_UNEMPLOYMENT_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CASAND5URN"
    FRED_CPI_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CUUSA429SA0"
    ZILLOW_ZIP_URL = "https://files.zillowstatic.com/research/public_csvs/zori/Zip_zori_uc_sfrcondomfr_sm_sa_month.csv"
    ZILLOW_METRO_URL = "https://files.zillowstatic.com/research/public_csvs/zori/Metro_zori_uc_sfrcondomfr_sm_sa_month.csv"

    @property
    def source_name(self) -> str:
        return "economic_indicators"

    def fetch_raw(self, use_cache: bool = True) -> dict:
        """
        Fetches or loads cached raw datasets for FRED and Zillow.
        Returns a dict of raw dataframes.
        """
        unemp_file = self.raw_cache_dir / "fred_unemployment_cached.csv"
        cpi_file = self.raw_cache_dir / "fred_cpi_cached.csv"
        zori_zip_file = self.raw_cache_dir / "zillow_zori_92101_cached.csv"
        zori_metro_file = self.raw_cache_dir / "zillow_zori_metro_cached.csv"

        # 1. Unemployment
        if not (use_cache and unemp_file.exists()):
            try:
                self.logger.info("Fetching FRED CASAND5URN...")
                req = urllib.request.Request(self.FRED_UNEMPLOYMENT_URL, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    with open(unemp_file, "w", encoding="utf-8") as f:
                        f.write(resp.read().decode("utf-8"))
            except Exception as e:
                self.logger.warning("Failed to fetch FRED unemployment: %s", e)

        # 2. CPI
        if not (use_cache and cpi_file.exists()):
            try:
                self.logger.info("Fetching FRED CUUSA429SA0...")
                req = urllib.request.Request(self.FRED_CPI_URL, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    with open(cpi_file, "w", encoding="utf-8") as f:
                        f.write(resp.read().decode("utf-8"))
            except Exception as e:
                self.logger.warning("Failed to fetch FRED CPI: %s", e)

        # 3. ZORI ZIP 92101
        if not (use_cache and zori_zip_file.exists()):
            try:
                self.logger.info("Streaming Zillow ZIP 92101...")
                req = urllib.request.Request(self.ZILLOW_ZIP_URL, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=45) as resp:
                    hdr = resp.readline().decode("utf-8")
                    for line in resp:
                        text = line.decode("utf-8")
                        if ",92101," in text:
                            with open(zori_zip_file, "w", encoding="utf-8") as f:
                                f.write(hdr)
                                f.write(text)
                            break
            except Exception as e:
                self.logger.warning("Failed to fetch Zillow ZIP: %s", e)

        # 4. ZORI Metro
        if not (use_cache and zori_metro_file.exists()):
            try:
                self.logger.info("Streaming Zillow Metro San Diego...")
                req = urllib.request.Request(self.ZILLOW_METRO_URL, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=45) as resp:
                    hdr = resp.readline().decode("utf-8")
                    for line in resp:
                        text = line.decode("utf-8")
                        if '"San Diego, CA"' in text or "San Diego, CA" in text:
                            with open(zori_metro_file, "w", encoding="utf-8") as f:
                                f.write(hdr)
                                f.write(text)
                            break
            except Exception as e:
                self.logger.warning("Failed to fetch Zillow Metro: %s", e)

        df_unemp = pd.read_csv(unemp_file) if unemp_file.exists() else pd.DataFrame(columns=["observation_date", "CASAND5URN"])
        df_cpi = pd.read_csv(cpi_file) if cpi_file.exists() else pd.DataFrame(columns=["observation_date", "CUUSA429SA0"])
        df_zori_zip = pd.read_csv(zori_zip_file) if zori_zip_file.exists() else pd.DataFrame()
        df_zori_metro = pd.read_csv(zori_metro_file) if zori_metro_file.exists() else pd.DataFrame()

        return {
            "unemployment": df_unemp,
            "cpi": df_cpi,
            "zori_zip": df_zori_zip,
            "zori_metro": df_zori_metro,
        }

    def clean_and_transform(self, raw_dict: dict) -> pd.DataFrame:
        """
        Cleans and pivots raw series into monthly columns.
        """
        # --- 1. Unemployment ---
        df_u = raw_dict["unemployment"].copy()
        df_u = df_u.rename(columns={"observation_date": "date", "CASAND5URN": "unemp_rate"})
        df_u["date"] = pd.to_datetime(df_u["date"], errors="coerce")
        df_u["unemp_rate"] = pd.to_numeric(df_u["unemp_rate"], errors="coerce")
        # Linearly interpolate any occasional BLS/FRED gap (e.g. 2025-10)
        df_u["unemp_rate"] = df_u["unemp_rate"].interpolate(method="linear").bfill().ffill()
        df_u = df_u.dropna(subset=["date"]).sort_values("date")
        df_u["unemp_yoy_chg"] = df_u["unemp_rate"] - df_u["unemp_rate"].shift(12)

        # --- 2. CPI (Semi-Annual -> Interpolated Monthly) ---
        df_cpi = raw_dict["cpi"].copy()
        df_cpi = df_cpi.rename(columns={"observation_date": "date", "CUUSA429SA0": "cpi"})
        df_cpi["date"] = pd.to_datetime(df_cpi["date"], errors="coerce")
        df_cpi["cpi"] = pd.to_numeric(df_cpi["cpi"], errors="coerce")
        df_cpi = df_cpi.dropna().sort_values("date")

        # Full monthly grid for CPI interpolation
        if not df_cpi.empty:
            full_idx = pd.date_range("2016-01-01", "2026-01-01", freq="MS")
            df_cpi_monthly = pd.DataFrame({"date": full_idx})
            df_cpi_monthly = pd.merge_asof(
                df_cpi_monthly.sort_values("date"),
                df_cpi.sort_values("date"),
                on="date",
                direction="nearest",
            )
            # Interpolate smoothly between semi-annual observations
            df_cpi_monthly["cpi"] = df_cpi_monthly["cpi"].interpolate(method="linear").bfill().ffill()
            df_cpi_monthly["cpi_yoy_pct"] = (
                (df_cpi_monthly["cpi"] - df_cpi_monthly["cpi"].shift(12)) / df_cpi_monthly["cpi"].shift(12) * 100.0
            )
        else:
            df_cpi_monthly = pd.DataFrame(columns=["date", "cpi", "cpi_yoy_pct"])

        # --- 3. Zillow ZORI (Wide to Long) ---
        def reshape_zori(wide_df: pd.DataFrame, col_name: str) -> pd.DataFrame:
            if wide_df.empty:
                return pd.DataFrame(columns=["date", col_name, f"{col_name}_yoy_pct"])
            date_cols = [c for c in wide_df.columns if c.startswith("20")]
            row = wide_df.iloc[0]
            records = []
            for dc in date_cols:
                val = pd.to_numeric(row[dc], errors="coerce")
                records.append({"date_str": dc, col_name: val})
            z_df = pd.DataFrame(records)
            z_df["date"] = pd.to_datetime(z_df["date_str"]).dt.to_period("M").dt.to_timestamp()
            z_df = z_df.sort_values("date")
            z_df[f"{col_name}_yoy_pct"] = (
                (z_df[col_name] - z_df[col_name].shift(12)) / z_df[col_name].shift(12) * 100.0
            )
            return z_df[["date", col_name, f"{col_name}_yoy_pct"]]

        df_zori_92101 = reshape_zori(raw_dict["zori_zip"], "rent_zori_downtown_92101")
        df_zori_metro = reshape_zori(raw_dict["zori_metro"], "rent_zori_metro_sd")

        # Merge all into unified date index
        merged = pd.merge(df_u, df_cpi_monthly, on="date", how="outer")
        merged = pd.merge(merged, df_zori_92101, on="date", how="outer")
        merged = pd.merge(merged, df_zori_metro[["date", "rent_zori_metro_sd"]], on="date", how="outer")
        merged = merged.sort_values("date").reset_index(drop=True)

        return merged

    def aggregate_monthly(
        self,
        df: pd.DataFrame,
        start_date: str = "2017-01-01",
        end_date: str = "2025-12-01",
    ) -> pd.DataFrame:
        start_ts = pd.to_datetime(start_date)
        end_ts = pd.to_datetime(end_date)
        work = df[(df["date"] >= start_ts) & (df["date"] <= end_ts)].copy()

        monthly = pd.DataFrame()
        monthly["date"] = work["date"].dt.strftime("%Y-%m-%d")
        monthly["econ_unemployment_rate_pct"] = work["unemp_rate"].round(2)
        monthly["econ_unemployment_yoy_chg"] = work["unemp_yoy_chg"].round(2)
        monthly["econ_cpi_sandiego_index"] = work["cpi"].round(2)
        monthly["econ_cpi_sandiego_yoy_pct"] = work["cpi_yoy_pct"].round(2)
        monthly["econ_rent_zori_downtown_92101"] = work["rent_zori_downtown_92101"].round(2)
        monthly["econ_rent_zori_downtown_yoy_pct"] = work["rent_zori_downtown_92101_yoy_pct"].round(2)
        monthly["econ_rent_zori_metro_sd"] = work["rent_zori_metro_sd"].round(2)

        return monthly.reset_index(drop=True)

    def validate_schema(self, df: pd.DataFrame) -> bool:
        required_cols = [
            "date",
            "econ_unemployment_rate_pct",
            "econ_unemployment_yoy_chg",
            "econ_cpi_sandiego_index",
            "econ_cpi_sandiego_yoy_pct",
            "econ_rent_zori_downtown_92101",
            "econ_rent_zori_downtown_yoy_pct",
            "econ_rent_zori_metro_sd",
        ]
        for col in required_cols:
            if col not in df.columns:
                self.logger.error("Missing schema column in economic: %s", col)
                return False

        if len(df) == 0:
            self.logger.error("Empty economic indicators dataframe.")
            return False

        # Physical sanity checks
        if (df["econ_unemployment_rate_pct"] < 2.0).any() or (df["econ_unemployment_rate_pct"] > 35.0).any():
            self.logger.error("Unemployment rate out of plausible range [2.0, 35.0].")
            return False

        if (df["econ_rent_zori_downtown_92101"] < 1200.0).any() or (df["econ_rent_zori_downtown_92101"] > 4500.0).any():
            self.logger.error("Downtown ZORI rent out of plausible range [1200, 4500].")
            return False

        return True
