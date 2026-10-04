"""
Spatial Distribution & Geographic Concentration Feature Module
Computes neighborhood population shares, core vs periphery dispersion ratios,
and the spatial Hirschman-Herfindahl Index (HHI) strictly lagged to avoid leakage.
"""

from pathlib import Path
from typing import Optional
import numpy as np
import pandas as pd


def generate_spatial_features(
    master_counts_path: Optional[Path] = None,
    canonical_dates: Optional[pd.Series] = None,
) -> pd.DataFrame:
    """
    Computes spatial concentration and neighborhood distribution metrics:
    - spatial_east_village_share_pct_lag1
    - spatial_city_center_share_pct_lag1
    - spatial_outside_perimeter_share_pct_lag1
    - spatial_hhi_concentration_index_lag1
    - spatial_east_village_growth_diff_lag1
    """
    path = master_counts_path or Path("data/MasterCounts_Adjusted_v2.csv")
    if not path.exists():
        raise FileNotFoundError(f"Master counts file not found at {path}")

    df = pd.read_csv(path)
    neigh = df[(df["area_type"] == "neighborhood") & (df["component"] == "total")].copy()
    neigh["date"] = pd.to_datetime(neigh["date"]).dt.strftime("%Y-%m-%d")

    # Pivot to date x neighborhood
    piv = neigh.pivot(index="date", columns="area", values="total_count").fillna(0.0)
    piv = piv.sort_index()

    tot = piv.sum(axis=1)
    safe_tot = tot.replace(0, np.nan)

    # Neighborhood shares (percentages)
    ev_share = (piv["East Village"] / safe_tot * 100.0).fillna(0.0) if "East Village" in piv.columns else pd.Series(0, index=piv.index)
    cc_share = (piv["City Center"] / safe_tot * 100.0).fillna(0.0) if "City Center" in piv.columns else pd.Series(0, index=piv.index)
    op_share = (piv["Outside Perimeter"] / safe_tot * 100.0).fillna(0.0) if "Outside Perimeter" in piv.columns else pd.Series(0, index=piv.index)

    # Hirschman-Herfindahl Index across all neighborhoods
    proportions = piv.div(safe_tot, axis=0).fillna(0.0)
    hhi = (proportions ** 2).sum(axis=1)

    # Growth difference: East Village MoM growth vs non-EV MoM growth
    non_ev_tot = tot - piv.get("East Village", 0.0)
    ev_growth = piv.get("East Village", 0.0).pct_change().fillna(0.0) * 100.0
    non_ev_growth = non_ev_tot.pct_change().fillna(0.0) * 100.0
    growth_diff = (ev_growth - non_ev_growth).round(2)

    spatial_df = pd.DataFrame(
        {
            "date": list(piv.index),
            "spatial_east_village_share_pct": ev_share.values.round(2),
            "spatial_city_center_share_pct": cc_share.values.round(2),
            "spatial_outside_perimeter_share_pct": op_share.values.round(2),
            "spatial_hhi_concentration_index": hhi.values.round(4),
            "spatial_east_village_growth_diff": growth_diff.values,
        }
    ).reset_index(drop=True)

    # Strictly lag spatial features by 1 month (t-1)
    res = pd.DataFrame()
    res["date"] = spatial_df["date"]
    res["spatial_east_village_share_pct_lag1"] = spatial_df["spatial_east_village_share_pct"].shift(1)
    res["spatial_city_center_share_pct_lag1"] = spatial_df["spatial_city_center_share_pct"].shift(1)
    res["spatial_outside_perimeter_share_pct_lag1"] = spatial_df["spatial_outside_perimeter_share_pct"].shift(1)
    res["spatial_hhi_concentration_index_lag1"] = spatial_df["spatial_hhi_concentration_index"].shift(1)
    res["spatial_east_village_growth_diff_lag1"] = spatial_df["spatial_east_village_growth_diff"].shift(1)
    res = res.reset_index(drop=True)

    # Reindex to canonical dates if provided
    if canonical_dates is not None:
        grid_df = pd.DataFrame({"date": canonical_dates.astype(str)}).reset_index(drop=True)
        res = pd.merge(grid_df, res, on="date", how="left")

    return res.drop(columns=["date"])
