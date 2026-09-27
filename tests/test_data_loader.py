"""
Unit tests for data loader contracts and schema validation.
Downtown San Diego Homeless Population Analysis - Task 9.1
"""

import pytest
import pandas as pd
from src.data_loader import (
    load_historical_data,
    load_paired_county_data,
    load_hotspot_rankings,
    load_forecast_data,
)


def test_load_historical_data():
    """Verify MasterCounts_Adjusted_v2.csv loads headline rows properly."""
    df = load_historical_data()
    assert not df.empty
    
    # Must only contain headline neighborhood totals
    assert set(df["component"].unique()) == {"total"}
    assert set(df["area_type"].unique()) == {"neighborhood"}
    
    # Date bounds
    assert df["date"].min() == pd.Timestamp("2017-01-01")
    assert df["date"].max() >= pd.Timestamp("2025-01-01")
    
    # Required columns
    for col in ["date", "year", "month", "area", "total_count", "raw_count"]:
        assert col in df.columns


def test_load_paired_county_data():
    """Verify 8-year paired annual series."""
    df = load_paired_county_data()
    assert not df.empty
    assert len(df) == 9  # 2017-2025 (with 2021 skipped)
    
    # Verify 2023 peak concentration
    row_2023 = df[df["year"] == 2023].iloc[0]
    assert row_2023["county_unsheltered"] == 5171
    assert row_2023["share_of_county"] == pytest.approx(37.49, abs=0.1)


def test_load_hotspot_rankings():
    """Verify top 10 persistent hotspot blocks."""
    df = load_hotspot_rankings()
    assert len(df) >= 10
    top = df.iloc[0]
    assert top["block_id"] == "16TH_ST_IMPERIAL_AV"
    assert top["hotspot_dates"] == 9
