"""Shared construction of the 9 monthly analysis series used in Assignments 4 and 6.

Mirrors TimeSeries_Decomposition.ipynb (Task 4.1) exactly: neighborhood totals from
MasterCounts_Adjusted_v2.csv, a reported-footprint overall series, a fixed-core-six
overall series, and the 7 neighborhoods; internal gaps (the unreleased 2025 months)
are time-interpolated in memory only.
"""
from pathlib import Path

import pandas as pd

NEIGHBORHOODS = [
    "East Village", "City Center", "Columbia", "Marina",
    "Cortez", "Gaslamp", "Outside Perimeter",
]
OVERALL = "Overall — reported footprint"
CORE_SIX = "Overall — fixed core six"
SEASONAL_PERIOD = 12


def load_monthly(path="data/MasterCounts_Adjusted_v2.csv", value="total_count"):
    df = pd.read_csv(Path(path), parse_dates=["date"])
    monthly = df.loc[
        (df["component"] == "total")
        & (df["area_type"] == "neighborhood")
        & (df["area"].isin(NEIGHBORHOODS)),
        ["date", "area", value, "method"],
    ].sort_values(["area", "date"])
    assert monthly.duplicated(["date", "area"]).sum() == 0
    return monthly


def prepare_monthly(series):
    observed = series.dropna()
    idx = pd.date_range(observed.index.min(), observed.index.max(), freq="MS")
    regular = series.reindex(idx).astype(float)
    gaps = regular[regular.isna()].index
    filled = regular.interpolate(method="time", limit_direction="both")
    assert filled.notna().all() and len(filled) >= 2 * SEASONAL_PERIOD
    filled.index.name = "date"
    return filled, gaps


def build_series(path="data/MasterCounts_Adjusted_v2.csv", value="total_count"):
    """Return {series name: interpolated monthly pd.Series} for the 9 analysis series."""
    monthly = load_monthly(path, value)
    pivot = monthly.pivot(index="date", columns="area", values=value).sort_index()
    core = [n for n in NEIGHBORHOODS if n != "Outside Perimeter"]
    raw = {
        OVERALL: pivot.sum(axis=1, min_count=1),
        CORE_SIX: pivot[core].sum(axis=1, min_count=len(core)),
    }
    raw.update({n: pivot[n] for n in NEIGHBORHOODS})
    return {name: prepare_monthly(s.rename(name))[0] for name, s in raw.items()}
