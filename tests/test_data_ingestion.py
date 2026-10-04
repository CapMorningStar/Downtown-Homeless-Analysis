"""
Automated Pytest Suite for Multi-Source Data Ingestion Pipeline (Task 10.1)
Downtown San Diego Homeless Population Analysis
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from data_ingestion.aligner import MultiSourceAligner
from data_ingestion.validator import DataQualityValidator
from data_ingestion.sources.weather_noaa import WeatherIngestionPipeline
from data_ingestion.sources.major_events import MajorEventsIngestionPipeline
from data_ingestion.sources.economic_indicators import EconomicIngestionPipeline
from data_ingestion.sources.shelter_capacity import ShelterCapacityIngestionPipeline
from data_ingestion.sources.get_it_done_311 import GetItDone311IngestionPipeline


@pytest.fixture(scope="module")
def aligned_master_dataset():
    aligner = MultiSourceAligner()
    df = aligner.run_all(use_cache=True)
    return df


def test_weather_pipeline():
    pipe = WeatherIngestionPipeline()
    df = pipe.run(use_cache=True)
    assert len(df) == 108
    assert "weather_temp_mean_f" in df.columns
    assert "weather_precip_total_in" in df.columns
    assert (df["weather_precip_total_in"] >= 0).all()
    assert (df["weather_temp_mean_f"] >= 45.0).all()
    assert (df["weather_temp_mean_f"] <= 85.0).all()


def test_major_events_pipeline():
    pipe = MajorEventsIngestionPipeline()
    df = pipe.run(use_cache=True)
    assert len(df) == 108
    assert "events_padres_home_games_count" in df.columns
    assert "events_comic_con_active" in df.columns
    # In winter months (Dec, Jan), Padres home games must be 0
    df["dt"] = pd.to_datetime(df["date"])
    winter = df[df["dt"].dt.month.isin([12, 1])]
    assert (winter["events_padres_home_games_count"] == 0).all()
    # Comic-Con cancelled in July 2020 due to COVID
    assert df.loc[df["date"] == "2020-07-01", "events_comic_con_active"].values[0] == 0
    # Comic-Con active in July 2019
    assert df.loc[df["date"] == "2019-07-01", "events_comic_con_active"].values[0] == 1


def test_economic_indicators_pipeline():
    pipe = EconomicIngestionPipeline()
    df = pipe.run(use_cache=True)
    assert len(df) == 108
    assert "econ_unemployment_rate_pct" in df.columns
    assert "econ_rent_zori_downtown_92101" in df.columns
    assert (df["econ_unemployment_rate_pct"] >= 2.0).all()
    assert (df["econ_unemployment_rate_pct"] <= 30.0).all()
    assert (df["econ_rent_zori_downtown_92101"] >= 1500.0).all()
    # Check that unemployment has 0 nulls after interpolation
    assert df["econ_unemployment_rate_pct"].isnull().sum() == 0


def test_shelter_capacity_pipeline():
    pipe = ShelterCapacityIngestionPipeline()
    df = pipe.run(use_cache=True)
    assert len(df) == 108
    # Safe sleeping capacity step-functions
    pre_safe = df[df["date"] < "2023-07-01"]
    assert (pre_safe["shelter_safe_sleeping_capacity"] == 0).all()

    mid_safe = df[(df["date"] >= "2023-07-01") & (df["date"] < "2023-10-01")]
    assert (mid_safe["shelter_safe_sleeping_capacity"] == 400).all()

    full_safe = df[df["date"] >= "2023-10-01"]
    assert (full_safe["shelter_safe_sleeping_capacity"] == 800).all()

    # Convention center operation shelter to home active March 2020 - March 2021
    sth = df[(df["date"] >= "2020-03-01") & (df["date"] <= "2021-03-01")]
    assert (sth["shelter_operation_shelter_to_home_active"] == 1).all()


def test_get_it_done_311_pipeline():
    pipe = GetItDone311IngestionPipeline()
    df = pipe.run(use_cache=True)
    assert len(df) == 108
    assert "service_311_total_requests_count" in df.columns
    assert "service_311_encampment_requests_count" in df.columns
    assert (df["service_311_total_requests_count"] >= 0).all()
    assert (df["service_311_closed_rate_pct"] >= 0).all()
    assert (df["service_311_closed_rate_pct"] <= 100.0).all()


def test_aligner_temporal_integrity(aligned_master_dataset):
    df = aligned_master_dataset
    assert len(df) == 108
    assert df["date"].min() == "2017-01-01"
    assert df["date"].max() == "2025-12-01"
    dates = pd.to_datetime(df["date"])
    assert dates.is_monotonic_increasing
    # Ground truth total matches canonical master counts sum
    mc = pd.read_csv("data/MasterCounts_Adjusted_v2.csv")
    mc_neigh_tot = mc[(mc["area_type"] == "neighborhood") & (mc["component"] == "total")]
    expected_sum = mc_neigh_tot["total_count"].sum()
    actual_sum = df["downtown_actual_adjusted_count"].sum()
    assert np.isclose(expected_sum, actual_sum, atol=1e-2)


def test_validator_full_audit(aligned_master_dataset):
    validator = DataQualityValidator()
    audit = validator.run_full_audit()
    assert audit["status"] == "PASSED"
    assert audit["row_count"] == 108
    assert audit["temporal_continuity_ok"] is True
    assert audit["null_check_ok"] is True
    assert audit["domain_bounds_ok"] is True


def test_validator_catches_violations(tmp_path):
    # Test that validator detects missing months and out-of-bounds
    bad_df = pd.DataFrame({
        "date": ["2017-01-01", "2017-02-01"],  # only 2 rows
        "downtown_actual_adjusted_count": [100.0, 9999.0],  # out of bounds
        "weather_temp_mean_f": [60.0, 150.0],  # 150F out of bounds
        "econ_unemployment_rate_pct": [np.nan, 5.0],  # null
    })
    bad_csv = tmp_path / "bad.csv"
    bad_df.to_csv(bad_csv, index=False)

    val = DataQualityValidator(data_path=bad_csv)
    audit = val.run_full_audit()
    assert audit["status"] == "FAILED"
    assert audit["temporal_continuity_ok"] is False
    assert audit["null_check_ok"] is False
    assert audit["domain_bounds_ok"] is False
