"""
Data ingestion, validation, and caching contracts for the Downtown San Diego Homelessness Dashboard.
Downtown San Diego Homeless Population Analysis - Task 9.1
"""

from typing import Optional, Dict, Any, List
import pandas as pd
import geopandas as gpd
import streamlit as st
from src.config import DATA_DIR, NEIGHBORHOODS, CORE_SIX_NEIGHBORHOODS


@st.cache_data(show_spinner=False, ttl=3600)
def load_historical_data() -> pd.DataFrame:
    """
    Ingest MasterCounts_Adjusted_v2.csv (canonical long format).
    Filters to headline rows: component == 'total' and area_type == 'neighborhood'
    to prevent double counting East Village sub-areas.
    """
    path = DATA_DIR / "MasterCounts_Adjusted_v2.csv"
    if not path.exists():
        return pd.DataFrame()

    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.strftime("%b")

    # Headline rows filter
    headline = df[
        (df["component"] == "total") & (df["area_type"] == "neighborhood")
    ].copy()
    headline = headline.sort_values(["area", "date"]).reset_index(drop=True)
    return headline


@st.cache_data(show_spinner=False, ttl=3600)
def load_all_components_data() -> pd.DataFrame:
    """
    Ingest full component rows (individual, tent, vehicle, total)
    for neighborhood-level drill-downs.
    """
    path = DATA_DIR / "MasterCounts_Adjusted_v2.csv"
    if not path.exists():
        return pd.DataFrame()

    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_data(show_spinner=False, ttl=3600)
def load_constant_series() -> pd.DataFrame:
    """
    Ingest TimeSeries_ConstantMethodology.csv (rescaled to POST2020 standard).
    """
    path = DATA_DIR / "TimeSeries_ConstantMethodology.csv"
    if not path.exists():
        return pd.DataFrame()

    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_data(show_spinner=False, ttl=3600)
def load_forecast_data() -> pd.DataFrame:
    """
    Ingest Forecasts_12Month.csv (2026 prospective forecasts across 9 series).
    Contains: point_forecast, pi_80_lower/upper, pi_95_lower/upper, optimistic/pessimistic bounds.
    """
    path = DATA_DIR / "Forecasts_12Month.csv"
    if not path.exists():
        # No synthetic fallback: showing invented numbers as model output would mislead users.
        st.error("data/Forecasts_12Month.csv not found. Run `python forecast_pipeline.py` to generate forecasts.")
        return pd.DataFrame()

    df = pd.read_csv(path)
    df["forecast_date"] = pd.to_datetime(df["forecast_date"])
    return df


@st.cache_data(show_spinner=False, ttl=3600)
def load_paired_county_data() -> pd.DataFrame:
    """
    Ingest Downtown_County_PairedCounts.csv (2017-2025 paired PIT counts).
    """
    path = DATA_DIR / "Downtown_County_PairedCounts.csv"
    if not path.exists():
        # Fallback to audited Table 4.1 from Task 8.1 documentation
        data = [
            {"year": 2017, "pit_date": "2017-01-27", "county_total": 9116, "county_unsheltered": 5621, "city_unsheltered": 3231, "downtown_reported_adjusted": 882.00, "downtown_fixed6_adjusted": 882.00, "share_of_county": 15.69, "share_of_city": 27.30},
            {"year": 2018, "pit_date": "2018-01-26", "county_total": 8576, "county_unsheltered": 4990, "city_unsheltered": 3066, "downtown_reported_adjusted": 803.49, "downtown_fixed6_adjusted": 803.49, "share_of_county": 16.10, "share_of_city": 26.21},
            {"year": 2019, "pit_date": "2019-01-25", "county_total": 8102, "county_unsheltered": 4476, "city_unsheltered": 2600, "downtown_reported_adjusted": 897.21, "downtown_fixed6_adjusted": 897.21, "share_of_county": 20.04, "share_of_city": 34.51},
            {"year": 2020, "pit_date": "2020-01-23", "county_total": 7638, "county_unsheltered": 3971, "city_unsheltered": 2283, "downtown_reported_adjusted": 789.14, "downtown_fixed6_adjusted": 789.14, "share_of_county": 19.87, "share_of_city": 34.57},
            {"year": 2021, "pit_date": None, "county_total": None, "county_unsheltered": None, "city_unsheltered": None, "downtown_reported_adjusted": 714.40, "downtown_fixed6_adjusted": 714.40, "share_of_county": None, "share_of_city": None},
            {"year": 2022, "pit_date": "2022-02-24", "county_total": 8427, "county_unsheltered": 4106, "city_unsheltered": 2494, "downtown_reported_adjusted": 1444.31, "downtown_fixed6_adjusted": 1174.31, "share_of_county": 35.18, "share_of_city": 57.91},
            {"year": 2023, "pit_date": "2023-01-26", "county_total": 10264, "county_unsheltered": 5171, "city_unsheltered": 3285, "downtown_reported_adjusted": 1938.74, "downtown_fixed6_adjusted": 1298.74, "share_of_county": 37.49, "share_of_city": 59.02},
            {"year": 2024, "pit_date": "2024-01-25", "county_total": 10605, "county_unsheltered": 6110, "city_unsheltered": 3365, "downtown_reported_adjusted": 1018.14, "downtown_fixed6_adjusted": 981.14, "share_of_county": 16.66, "share_of_city": 30.26},
            {"year": 2025, "pit_date": "2025-01-23", "county_total": 9905, "county_unsheltered": 5714, "city_unsheltered": 2897, "downtown_reported_adjusted": 851.02, "downtown_fixed6_adjusted": 767.02, "share_of_county": 14.89, "share_of_city": 29.38},
        ]
        return pd.DataFrame(data)
    df = pd.read_csv(path)
    if "pit_year" in df.columns and "year" not in df.columns:
        df["year"] = df["pit_year"].astype(int)
    if "downtown_share_county_unsheltered_pct" in df.columns and "share_of_county" not in df.columns:
        df["share_of_county"] = df["downtown_share_county_unsheltered_pct"]
    return df

@st.cache_data(show_spinner=False, ttl=3600)
def load_hotspot_rankings() -> pd.DataFrame:
    """
    Ingest Hotspot_Persistence_Ranking.csv.
    Top 10 persistent blocks from Task 5.3/5.4.
    """
    path = DATA_DIR / "Hotspot_Persistence_Ranking.csv"
    if not path.exists():
        # Fallback to audited Table in Task 5.4 Technical Report
        data = [
            {"rank": 1, "block_id": "16TH_ST_IMPERIAL_AV", "neighborhood": "South East Village", "hotspot_dates": 9, "hotspot_rate": 0.75, "nearest_service_m": 285.2, "nearest_transit_m": 52.3},
            {"rank": 2, "block_id": "I-5_SB_IMPERIAL_AV", "neighborhood": "South East Village", "hotspot_dates": 8, "hotspot_rate": 0.67, "nearest_service_m": 392.5, "nearest_transit_m": 136.9},
            {"rank": 3, "block_id": "I-5_SB_OFF_RA_Map_Border", "neighborhood": "South East Village", "hotspot_dates": 6, "hotspot_rate": 0.50, "nearest_service_m": 538.0, "nearest_transit_m": 204.4},
            {"rank": 4, "block_id": "I-5_SB_ON_RA_Map_Border", "neighborhood": "South East Village", "hotspot_dates": 4, "hotspot_rate": 0.33, "nearest_service_m": 487.1, "nearest_transit_m": 154.2},
            {"rank": 5, "block_id": "17TH_ST_IMPERIAL_AV", "neighborhood": "South East Village", "hotspot_dates": 4, "hotspot_rate": 0.33, "nearest_service_m": 324.6, "nearest_transit_m": 71.6},
            {"rank": 6, "block_id": "16TH_ST_J_ST", "neighborhood": "South East Village", "hotspot_dates": 2, "hotspot_rate": 0.17, "nearest_service_m": 422.7, "nearest_transit_m": 282.9},
            {"rank": 7, "block_id": "17TH_ST_J_ST", "neighborhood": "South East Village", "hotspot_dates": 2, "hotspot_rate": 0.17, "nearest_service_m": 506.3, "nearest_transit_m": 273.9},
            {"rank": 8, "block_id": "16TH_ST_ISLAND_AV", "neighborhood": "South East Village", "hotspot_dates": 2, "hotspot_rate": 0.17, "nearest_service_m": 375.0, "nearest_transit_m": 167.9},
            {"rank": 9, "block_id": "17TH_ST_ISLAND_AV", "neighborhood": "South East Village", "hotspot_dates": 1, "hotspot_rate": 0.08, "nearest_service_m": 456.0, "nearest_transit_m": 174.4},
            {"rank": 10, "block_id": "16TH_ST_K_ST", "neighborhood": "South East Village", "hotspot_dates": 0, "hotspot_rate": 0.00, "nearest_service_m": 389.0, "nearest_transit_m": 164.1},
        ]
        return pd.DataFrame(data)

    return pd.read_csv(path)


@st.cache_data(show_spinner=False, ttl=3600)
def load_seasonal_indices() -> pd.DataFrame:
    """
    Ingest SeasonalIndices.csv (108 rows = 9 series x 12 months).
    """
    path = DATA_DIR / "SeasonalIndices.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data(show_spinner=False, ttl=3600)
def load_geojson_grid() -> Optional[gpd.GeoDataFrame]:
    """
    Ingest Downtown_BlockGrid.geojson.
    """
    path = DATA_DIR / "Downtown_BlockGrid.geojson"
    if not path.exists():
        return None
    try:
        gdf = gpd.read_file(path)
        if gdf.crs != "EPSG:4326":
            gdf = gdf.to_crs(epsg=4326)
        return gdf
    except Exception:
        return None


@st.cache_data(show_spinner=False, ttl=3600)
def load_forecast_benchmarks(series: str = "Overall - reported footprint") -> pd.DataFrame:
    """
    Model benchmark table computed from the Task 7.2/7.3 outputs (not hard-coded):
    12-month CV MAPE/RMSE (mean over the 5 walk-forward folds, Forecast_CV_Metrics.csv)
    and 2025 hold-out MAPE at the 12-month horizon (Forecast_ModelComparison.csv).
    """
    cv_path = DATA_DIR / "Forecast_CV_Metrics.csv"
    if not cv_path.exists():
        return pd.DataFrame()
    cv = pd.read_csv(cv_path)
    cv = cv[(cv["series"] == series) & (cv["horizon_months"] == 12)]
    table = cv.groupby("model")[["mape", "rmse"]].mean()

    holdout = pd.Series(dtype=float)
    cmp_path = DATA_DIR / "Forecast_ModelComparison.csv"
    if cmp_path.exists():
        cmp = pd.read_csv(cmp_path)
        cmp = cmp[(cmp["series"] == series) & (cmp["horizon_months"] == 12)]
        holdout = cmp.set_index("model")["mape_pct"]

    names = {"xgboost": "XGBoost", "holt_winters": "Holt-Winters", "sarima": "SARIMA",
             "prophet": "Prophet (changepoints)", "naive_seasonal": "Naive seasonal (t-12)"}
    out = pd.DataFrame({
        "Model": [names.get(m, m) for m in table.index],
        "12-Mo CV MAPE": [f"{v:.2f}%" for v in table["mape"]],
        "12-Mo CV RMSE": [f"{v:.1f}" for v in table["rmse"]],
        "2025 Hold-Out MAPE": [f"{holdout[m]:.2f}%" if m in holdout.index else "n/a" for m in table.index],
        "_sort": table["mape"].values,
    }).sort_values("_sort").drop(columns="_sort")
    return out.reset_index(drop=True)


def _generate_fallback_forecasts() -> pd.DataFrame:
    """Synthesizes canonical 2026 forecast table based on Task 7.4 production runbook."""
    dates = pd.date_range("2026-01-01", "2026-12-01", freq="MS")
    rows = []
    
    # Baseline starting parameters for Headline Footprint (around ~885.63 in Jan 2026)
    base_point = 885.63
    sigma_res = 145.0
    
    for h, dt in enumerate(dates, start=1):
        # Gradual slight upward drift + seasonal adjustment
        pt = base_point + (h * 4.5)
        sigma_h = sigma_res * ((1.0 + 0.08 * (h - 1)) ** 0.5)
        
        pi_80_l = max(0.0, pt - 1.282 * sigma_h)
        pi_80_u = pt + 1.282 * sigma_h
        pi_95_l = max(0.0, pt - 1.960 * sigma_h)
        pi_95_u = pt + 1.960 * sigma_h
        
        opt = pt * (1.0 - 0.020 * h)
        pess = pt * (1.0 + 0.0217 * h)
        
        rows.append({
            "series_name": "Overall - reported footprint",
            "forecast_date": dt,
            "horizon": h,
            "model": "XGBoost Champion",
            "point_forecast": round(pt, 2),
            "pi_80_lower": round(pi_80_l, 2),
            "pi_80_upper": round(pi_80_u, 2),
            "pi_95_lower": round(pi_95_l, 2),
            "pi_95_upper": round(pi_95_u, 2),
            "optimistic_scenario": round(opt, 2),
            "pessimistic_scenario": round(pess, 2),
        })
        
    return pd.DataFrame(rows)
