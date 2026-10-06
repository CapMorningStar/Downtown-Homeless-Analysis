# Comprehensive Feature Engineering Library & Attribution Monograph (Task 10.2)
## Downtown San Diego Homeless Population Analysis

**Document Status:** Production Ready & Validated  
**Project:** Downtown San Diego Homeless Population Analysis (Data Science Alliance)  
**Author / Contributor:** Kyaw Soe Lwin (`kylwin@ucsd.edu` / `kslwin.2000@gmail.com`)  
**Project Lead:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)  
**Milestone:** Task 10.2 (Build comprehensive feature engineering module: 50+ features)  
**Associated Deliverables:** `feature_engineering.py`, `feature_engineering/`, `data/FeatureMatrix_Comprehensive_68.csv`, `slide_assets/task10_feature_importance.png`, `tests/test_feature_engineering.py`  

---

## 1. Executive Summary & Objectives

**Task 10.2** establishes the core feature engineering and machine learning feature store for the predictive modeling architecture of the **Downtown San Diego Homeless Population Analysis**.

While Task 10.1 unified five external data streams onto a canonical 108-month index (`data/MultiSource_Master_Monthly.csv`), raw indicators cannot be fed directly into supervised machine learning algorithms without feature transformation. Raw time series suffer from non-stationarity, high collinearity, unmodeled seasonal harmonics, and data leakage if not structured under strict chronological lookback protocols.

Task 10.2 transforms the multi-source dataset into **68 engineered features** spanning **7 orthogonal domain families**, with a validated in-sample Random Forest baseline achieving $R^2 = 0.9631$. All features strictly enforce backward lookback shifts ($t-1$) relative to prospective prediction horizons, ensuring zero lookahead leakage.

```
+---------------------------------------------------------------------------------------------------------------+
|                                    68 Engineered Features by Domain Family                                    |
+---------------------------------------------------------------------------------------------------------------+
|  1. Temporal & Cyclical (9)          --> Harmonics (sin/cos), Trend index, Days since COVID, Post-2020, Ban   |
|  2. Autoregressive & Momentum (15)   --> Lags (1M, 2M, 3M, 6M, 12M), Differences, YoY Growth, Tent/Veh Ratios|
|  3. Rolling Envelopes (15)           --> 3M, 6M, 12M Means, Std, CV, Bollinger Envelopes, Anomaly Z-scores   |
|  4. Spatial Concentration (5)        --> East Village share, Perimeter share, Hirschman-Herfindahl Index (HHI)|
|  5. Municipal 311 Encampments (6)    --> Encampment complaint lags, momentum, complaint intensity per capita  |
|  6. Meteorology & Climate (6)        --> 3M thermal/precip moving totals, extreme weather flags, anomalies   |
|  7. Events, Shelter & Economics (12) --> Stadium density, Camping ban x Safe sleeping, Rent distress burden   |
+---------------------------------------------------------------------------------------------------------------+
                                                       │
                                                       ▼
+---------------------------------------------------------------------------------------------------------------+
|                                Feature Attribution & Importance Engine                                        |
|  - TimeSeriesSplit CV Permutation Importance (no lookahead bias)                                              |
|  - Random Forest Tree Impurity (Gini MDI)                                                                     |
|  - TreeExplainer SHAP Values (|φ_i| mean absolute attribution in individuals)                                 |
+---------------------------------------------------------------------------------------------------------------+
```

---

## 2. Feature Library Catalog & Mathematical Specifications

### 2.1 Domain 1: Temporal & Cyclical Features (9 Features)
Models continuous annual periodicity and tracks chronological distance from structural policy shocks:
* `temporal_month`: Calendar month $m \in [1, 12]$.
* `temporal_quarter`: Calendar quarter $q \in [1, 4]$.
* `temporal_year`: Calendar year $[2017, 2025]$.
* `temporal_sin_month`: $\sin\left(\frac{2\pi \cdot m}{12}\right)$, continuous seasonal encoding satisfying $\sin^2 + \cos^2 = 1.0$.
* `temporal_cos_month`: $\cos\left(\frac{2\pi \cdot m}{12}\right)$, orthogonal seasonal phase shift coordinate.
* `temporal_trend_idx`: Monotonic integer trend counter $t \in [0, 107]$.
* `temporal_days_since_covid_shock`: $\max(0, \text{date} - \text{2020-03-01})$, tracking post-pandemic emergency interventions.
* `temporal_days_since_methodology_post2020`: $\max(0, \text{date} - \text{2020-01-01})$, tracking the POST2020 multiplier era.
* `temporal_days_since_camping_ban`: $\max(0, \text{date} - \text{2023-07-01})$, tracking sidewalk enforcement duration.

### 2.2 Domain 2: Autoregressive Lags & Momentum (15 Features)
Captures persistent population inertia and acceleration:
* `lag_1m_adjusted`: $y_{t-1}$ (prior month adjusted count).
* `lag_2m_adjusted`: $y_{t-2}$.
* `lag_3m_adjusted`: $y_{t-3}$ (quarterly lag).
* `lag_6m_adjusted`: $y_{t-6}$ (semi-annual lag).
* `lag_12m_adjusted`: $y_{t-12}$ (same-month prior year).
* `lag_1m_raw`: $\text{raw}_{t-1}$.
* `lag_12m_raw`: $\text{raw}_{t-12}$.
* `diff_1m_adjusted`: $y_{t-1} - y_{t-2}$ (first difference / velocity).
* `diff_12m_adjusted`: $y_{t-1} - y_{t-13}$ (annual seasonal velocity).
* `acceleration_1m_adjusted`: $(y_{t-1} - y_{t-2}) - (y_{t-2} - y_{t-3})$ (second difference / acceleration).
* `growth_rate_1m_pct`: $\frac{y_{t-1} - y_{t-2}}{y_{t-2}} \times 100$.
* `growth_rate_12m_pct`: $\frac{y_{t-1} - y_{t-13}}{y_{t-13}} \times 100$.
* `ratio_tent_to_individual_lag1`: $\frac{\text{tent}_{t-1}}{\text{individual}_{t-1} + 1}$, measuring structural encamped density.
* `ratio_vehicle_to_individual_lag1`: $\frac{\text{vehicle}_{t-1}}{\text{individual}_{t-1} + 1}$, measuring vehicular homelessness.
* `ratio_shelter_to_unsheltered_lag1`: $\frac{\text{shelter\_capacity}_{t-1}}{y_{t-1} + 1}$, measuring municipal shelter coverage ratio.

### 2.3 Domain 3: Rolling Window Statistics & Volatility Envelopes (15 Features)
Smooths short-term counting volatility and identifies regime boundaries:
* `rolling_mean_3m_adjusted`: $\frac{1}{3}\sum_{k=1}^3 y_{t-k}$.
* `rolling_std_3m_adjusted`: 3-month sample standard deviation $\sigma_{3m}$.
* `rolling_min_3m_adjusted`, `rolling_max_3m_adjusted`: 3-month rolling envelope.
* `rolling_cv_3m_adjusted`: Rolling coefficient of variation $\frac{\sigma_{3m}}{\mu_{3m}}$.
* `rolling_mean_6m_adjusted`, `rolling_std_6m_adjusted`, `rolling_min_6m_adjusted`, `rolling_max_6m_adjusted`, `rolling_cv_6m_adjusted`: 6-month medium-term statistics.
* `rolling_mean_12m_adjusted`, `rolling_std_12m_adjusted`: 12-month annual moving baseline.
* `bollinger_upper_12m_adjusted`: $\mu_{12m} + 2\sigma_{12m}$ (statistical upper bound).
* `bollinger_lower_12m_adjusted`: $\max(0, \mu_{12m} - 2\sigma_{12m})$ (statistical lower bound).
* `z_score_12m_adjusted`: $\frac{y_{t-1} - \mu_{12m}}{\sigma_{12m}}$, measuring standardized anomaly distance.

### 2.4 Domain 4: Spatial Concentration & Neighborhood Distribution (5 Features)
Tracks geographic clustering using canonical neighborhood totals from `MasterCounts_Adjusted_v2.csv`:
* `spatial_east_village_share_pct_lag1`: $\frac{\text{EastVillage}_{t-1}}{T_{t-1}} \times 100$ (historical core $\approx 60\text{--}71\%$).
* `spatial_city_center_share_pct_lag1`: $\frac{\text{CityCenter}_{t-1}}{T_{t-1}} \times 100$.
* `spatial_outside_perimeter_share_pct_lag1`: $\frac{\text{OutsidePerimeter}_{t-1}}{T_{t-1}} \times 100$.
* `spatial_hhi_concentration_index_lag1`: Normalized Hirschman-Herfindahl Index $HHI = \sum_{i=1}^6 (s_i)^2 \in [0, 1]$.
* `spatial_east_village_growth_diff_lag1`: MoM percentage growth difference between East Village and outer neighborhoods.

### 2.5 Domain 5: Municipal 311 Encampment Dynamics (6 Features)
Connects public reporting pressure with visible street counts:
* `lag_1m_311_encampment`: Prior-month 311 encampment complaints in Downtown.
* `lag_3m_311_encampment`: 3-month lagged complaint volume.
* `diff_1m_311_encampment`: Month-over-month change in 311 complaints.
* `rolling_mean_3m_311_encampment`: 3-month smoothed 311 encampment calls.
* `ratio_encampment_to_total_311_lag1`: Percentage of Downtown 311 calls specifically concerning encampments.
* `encampment_complaint_pressure_per_capita_lag1`: $\frac{\text{311 Encampments}_{t-1}}{y_{t-1}}$, reporting intensity per unhoused person.

### 2.6 Domain 6: Meteorology & Climatological Signals (6 Features)
Controls for thermal and precipitation shocks driving shelter seeking:
* `rolling_mean_3m_temp`: 3-month moving average temperature ($^\circ\text{F}$).
* `rolling_sum_3m_precip`: 3-month cumulative rainfall (winter wetness index).
* `weather_extreme_event_flag_lag1`: Binary $\{0, 1\}$ (1 if extreme heat days $\ge 2$ or rainy days $\ge 4$).
* `weather_temp_anomaly_lag1`: Prior-month temperature minus 12-month baseline.
* `weather_precip_anomaly_lag1`: Prior-month precipitation minus 12-month baseline.
* `weather_cdd_hdd_balance_lag1`: Seasonal degree-day ratio $\frac{CDD_{t-1} + 1}{HDD_{t-1} + 1}$.

### 2.7 Domain 7: Civic Events, Shelter Policies & Economic Distress (12 Features)
* `events_padres_game_density`: Home games per calendar day at Petco Park in East Village.
* `events_major_civic_intensity_k`: Foot traffic pressure index (Padres + Comic-Con + holidays).
* `policy_camping_ban_x_safe_sleeping`: $\text{Camping Ban Active} \times \text{Safe Sleeping Spaces}$, measuring displacement capacity.
* `shelter_capacity_headroom_lag1`: Total shelter beds minus $y_{t-1}$ (net capacity buffer).
* `shelter_capacity_expansion_shock`: Binary $\{0, 1\}$ flag for $\Delta \text{capacity}_{1m} \ge 200$.
* `covid_emergency_shelter_x_temp`: Interaction between Convention Center emergency shelter and temperature.
* `lag_1m_unemployment_rate`: Prior-month San Diego County unemployment rate ($\%$).
* `diff_1m_unemployment_rate`: MoM percentage point change in unemployment.
* `lag_1m_rent_zori_downtown_92101`: Prior-month observed typical rent in ZIP 92101 ($\$$).
* `rent_acceleration_1m_pct`: MoM rent inflation acceleration rate.
* `rent_burden_distress_index_lag1`: $\text{Rent YoY Growth} \times \text{Unemployment Rate}$.
* `real_rent_index_lag1`: $\frac{\text{ZORI Rent 92101}}{\text{San Diego CPI}} \times 100$.

---

## 3. Leakage-Free Design & Boundary Handling

1. **Strict Lookback Rule:** All predictor features are computed over $[t-12, t-1]$. The survey count at month $t$ is strictly reserved as target $y_t$ (or $y_{t+1}$ for prospective multi-step forecasting).
2. **Initial Boundary Handling (2017):** Features requiring a 12-month lookback (such as `lag_12m` and `diff_12m`) are backfilled at the boundary, and a metadata flag `train_ready_flag = 1` is designated for `2018-01-01` through `2025-12-01` (96 contiguous months with zero imputed boundaries).
3. **Data Quality Audit:** In the 96-month model-ready training subset, **0 missing values (0.00% nulls)** exist across all 68 features.

---

## 4. Multi-Method Feature Importance & SHAP Attribution Findings

Importance was measured on a tree model fitted to the 92 published training months, using three methods. The model's in-sample fit is high, but in-sample fit is not forecast accuracy (see `docs/Ensemble_PerformanceReport.md` for out-of-fold results).
1. **Tree impurity (Gini / MDI):** total variance reduction across split nodes.
2. **Time-series-split permutation importance:** out-of-fold increase in MSE when a feature is permuted.
3. **TreeExplainer SHAP values:** mean absolute Shapley attribution |φ|, in people.

### Top 20 Features (corrected run, October 2026)

| Rank | Feature | Category | Mean \|SHAP\| (people) | Permutation | Gini | Pearson r |
|:---:|:---|:---|---:|---:|---:|---:|
| 1 | `lag_1m_raw` | Autoregressive & Momentum | 81.57 | 0.0065 | 0.2602 | +0.927 |
| 2 | `lag_1m_adjusted` | Autoregressive & Momentum | 66.10 | 0.0035 | 0.2127 | +0.927 |
| 3 | `rolling_max_3m_adjusted` | Rolling Window Envelopes | 44.04 | 0.0050 | 0.1376 | +0.896 |
| 4 | `ratio_shelter_to_unsheltered_lag1` † | Autoregressive & Momentum | 32.91 | 0.0050 | 0.1071 | −0.740 |
| 5 | `rolling_mean_3m_adjusted` | Rolling Window Envelopes | 18.24 | 0.0100 | 0.0619 | +0.908 |
| 6 | `shelter_capacity_headroom_lag1` † | Civic Events & Shelter Policy | 13.82 | 0.0119 | 0.0363 | −0.669 |
| 7 | `rolling_min_3m_adjusted` | Rolling Window Envelopes | 13.58 | 0.0110 | 0.0389 | +0.906 |
| 8 | `covid_emergency_shelter_x_temp` | Meteorology & Climate | 13.13 | 0.0000 | 0.0106 | −0.412 |
| 9 | `ratio_tent_to_individual_lag1` | Autoregressive & Momentum | 9.43 | 0.0117 | 0.0069 | +0.792 |
| 10 | `rent_burden_distress_index_lag1` | Macroeconomic Distress | 5.85 | 0.0037 | 0.0048 | +0.430 |
| 11 | `spatial_outside_perimeter_share_pct_lag1` | Spatial Concentration | 5.40 | 0.0113 | 0.0083 | +0.775 |
| 12 | `lag_2m_adjusted` | Autoregressive & Momentum | 5.15 | −0.0006 | 0.0174 | +0.883 |
| 13 | `rolling_sum_3m_precip` | Rolling Window Envelopes | 4.58 | −0.0038 | 0.0095 | +0.123 |
| 14 | `diff_12m_adjusted` | Autoregressive & Momentum | 3.65 | 0.0016 | 0.0046 | +0.596 |
| 15 | `rolling_cv_3m_adjusted` | Rolling Window Envelopes | 3.16 | 0.0005 | 0.0039 | −0.170 |
| 16 | `lag_12m_raw` | Autoregressive & Momentum | 3.02 | −0.0070 | 0.0027 | +0.275 |
| 17 | `rolling_mean_6m_adjusted` | Rolling Window Envelopes | 2.87 | 0.0083 | 0.0028 | +0.858 |
| 18 | `growth_rate_12m_pct` | Autoregressive & Momentum | 2.85 | −0.0002 | 0.0043 | +0.602 |
| 19 | `acceleration_1m_adjusted` | Other Exogenous | 2.54 | 0.0003 | 0.0050 | −0.006 |
| 20 | `diff_1m_311_encampment` | Autoregressive & Momentum | 2.46 | −0.0024 | 0.0033 | +0.156 |

† Built from the shelter-capacity series, which is an analyst-constructed timeline, not administrative records (see `docs/MultiSource_DataDocumentation.md`). Its importance reflects that constructed series.

---

## 5. Key Analytical Insights

1. **Persistence dominates.** Last month's count (`lag_1m_raw`, `lag_1m_adjusted`) and the 3-month rolling maximum are the top three features by SHAP. This matches the Task 10.3 finding that a plain lag-1 forecast beats every model.
2. **The shelter features are not evidence of a shelter effect.** `ratio_shelter_to_unsheltered_lag1` (rank 4) has the downtown count in its denominator, so it partly re-encodes the count itself. `shelter_capacity_headroom_lag1` (rank 6) comes from the constructed capacity timeline. Neither supports a conclusion about how shelter capacity affects street counts.
3. **Economic and weather signals are weak.** The rent-burden index ranks 10th (|SHAP| 5.9). The only weather feature in the top 20 is 3-month precipitation, ranked 13th with near-zero correlation. This agrees with the ablation result that external data do not improve forecasts.
4. **Importance is association, not cause.** Correlations such as the negative one between days-since-camping-ban and counts describe co-movement over time. They do not identify the effect of any policy.

> Earlier versions of this table came from a run in which four unpublished 2025 months were treated as zero counts. Values above are from the corrected run.

---

## 6. Downstream Interface for Task 10.3 (Ensemble Prediction System)

The dataset `data/FeatureMatrix_Comprehensive_68.csv` is fully engineered and formatted for immediate model consumption in Task 10.3:
* **Gradient Boosting (XGBoost / LightGBM):** Ingests all 68 features directly; tree splits naturally handle non-linear interactions like `policy_camping_ban_x_safe_sleeping` and `rent_burden_distress_index_lag1`.
* **Bayesian Structural Time Series (BSTS):** Uses `temporal_sin_month`, `temporal_cos_month`, `temporal_trend_idx`, and top 5 exogenous drivers (`lag_1m_raw`, `shelter_capacity_headroom`, `rent_burden`).
* **Temporal Neural Networks (LSTM):** Sequential tensors built from the training subset (2018–2025, 92 published months).
