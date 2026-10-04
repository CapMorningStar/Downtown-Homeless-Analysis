"""
Cross-Domain Interaction & Exogenous Signal Feature Module
Engineers interaction terms across municipal 311 dispatches, surface climatology,
stadium foot traffic, shelter capacity headroom, and macroeconomic rent distress.
All exogenous features respect historical information boundaries.
"""

import numpy as np
import pandas as pd


def generate_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates 24 cross-domain interaction terms, anomalies, and ratios:
    - 311 Encampment Dynamics (6)
    - Meteorological & Climatological Signals (6)
    - Civic Events & Policy Interactions (6)
    - Macroeconomic Distress & Rent Pressure (6)
    """
    res = pd.DataFrame(index=df.index)
    y_hist = df["downtown_actual_adjusted_count"].shift(1)

    # ==========================================
    # 1. Municipal 311 Encampment Dynamics (6)
    # ==========================================
    encamp_311 = df.get("service_311_encampment_requests_count", pd.Series(0, index=df.index))
    tot_311 = df.get("service_311_total_requests_count", pd.Series(1, index=df.index))

    res["lag_1m_311_encampment"] = encamp_311.shift(1).fillna(0).astype(int)
    res["lag_3m_311_encampment"] = encamp_311.shift(3).fillna(0).astype(int)
    res["diff_1m_311_encampment"] = (encamp_311.shift(1) - encamp_311.shift(2)).fillna(0).astype(int)
    res["rolling_mean_3m_311_encampment"] = encamp_311.shift(1).rolling(3, min_periods=1).mean().round(2)

    safe_tot_311 = tot_311.shift(1).replace(0, 1)
    res["ratio_encampment_to_total_311_lag1"] = (encamp_311.shift(1) / safe_tot_311 * 100.0).round(2)

    safe_y = y_hist.replace(0, np.nan)
    res["encampment_complaint_pressure_per_capita_lag1"] = (encamp_311.shift(1) / safe_y).round(4)

    # ==========================================
    # 2. Meteorological & Climatology Signals (6)
    # ==========================================
    temp = df.get("weather_temp_mean_f", pd.Series(65.0, index=df.index))
    precip = df.get("weather_precip_total_in", pd.Series(0.0, index=df.index))
    heat_days = df.get("weather_extreme_heat_days_count", pd.Series(0, index=df.index))
    rain_days = df.get("weather_rainy_days_count", pd.Series(0, index=df.index))
    cdd = df.get("weather_cdd_total", pd.Series(0.0, index=df.index))
    hdd = df.get("weather_hdd_total", pd.Series(0.0, index=df.index))

    res["rolling_mean_3m_temp"] = temp.shift(1).rolling(3, min_periods=1).mean().round(2)
    res["rolling_sum_3m_precip"] = precip.shift(1).rolling(3, min_periods=1).sum().round(3)

    is_extreme = ((heat_days.shift(1) >= 2) | (rain_days.shift(1) >= 4)).astype(int)
    res["weather_extreme_event_flag_lag1"] = is_extreme

    temp_12m_base = temp.shift(1).rolling(12, min_periods=1).mean()
    precip_12m_base = precip.shift(1).rolling(12, min_periods=1).mean()
    res["weather_temp_anomaly_lag1"] = (temp.shift(1) - temp_12m_base).round(2)
    res["weather_precip_anomaly_lag1"] = (precip.shift(1) - precip_12m_base).round(3)

    res["weather_cdd_hdd_balance_lag1"] = ((cdd.shift(1) + 1.0) / (hdd.shift(1) + 1.0)).round(4)

    # ==========================================
    # 3. Civic Events & Policy Interactions (6)
    # ==========================================
    padres = df.get("events_padres_home_games_count", pd.Series(0, index=df.index))
    civic_intensity = df.get("events_major_civic_intensity_k", pd.Series(0.0, index=df.index))
    ban_active = df.get("shelter_unsafe_camping_ban_active", pd.Series(0, index=df.index))
    safe_sleep = df.get("shelter_safe_sleeping_capacity", pd.Series(0, index=df.index))
    shelter_tot = df.get("shelter_total_capacity", pd.Series(2000, index=df.index))
    sth_active = df.get("shelter_operation_shelter_to_home_active", pd.Series(0, index=df.index))

    res["events_padres_game_density"] = (padres / 30.0).round(3)
    res["events_major_civic_intensity_k"] = civic_intensity.round(1)
    res["policy_camping_ban_x_safe_sleeping"] = (ban_active * safe_sleep).astype(int)
    res["shelter_capacity_headroom_lag1"] = (shelter_tot.shift(1) - y_hist).round(2)

    capacity_diff = shelter_tot - shelter_tot.shift(1)
    res["shelter_capacity_expansion_shock"] = (capacity_diff >= 200).astype(int)
    res["covid_emergency_shelter_x_temp"] = (sth_active * temp).round(2)

    # ==========================================
    # 4. Macroeconomic Distress & Rent Pressure (6)
    # ==========================================
    unemp = df.get("econ_unemployment_rate_pct", pd.Series(5.0, index=df.index))
    zori = df.get("econ_rent_zori_downtown_92101", pd.Series(2200.0, index=df.index))
    zori_yoy = df.get("econ_rent_zori_downtown_yoy_pct", pd.Series(0.0, index=df.index))
    cpi = df.get("econ_cpi_sandiego_index", pd.Series(150.0, index=df.index))

    res["lag_1m_unemployment_rate"] = unemp.shift(1).round(2)
    res["diff_1m_unemployment_rate"] = (unemp.shift(1) - unemp.shift(2)).round(2)
    res["lag_1m_rent_zori_downtown_92101"] = zori.shift(1).round(2)

    safe_zori_lag2 = zori.shift(2).replace(0, np.nan)
    res["rent_acceleration_1m_pct"] = ((zori.shift(1) - zori.shift(2)) / safe_zori_lag2 * 100.0).round(2)
    res["rent_burden_distress_index_lag1"] = (zori_yoy.shift(1) * unemp.shift(1)).round(2)

    safe_cpi = cpi.shift(1).replace(0, 1.0)
    res["real_rent_index_lag1"] = (zori.shift(1) / safe_cpi * 100.0).round(2)

    return res
