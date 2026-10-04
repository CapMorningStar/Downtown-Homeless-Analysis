# Multi-Source Predictive System: Data Ingestion & Schema Specification (Task 10.1)
## Downtown San Diego Homeless Population Analysis

**Document Status:** Production Ready & Validated  
**Project:** Downtown San Diego Homeless Population Analysis (Data Science Alliance)  
**Author / Contributor:** Kyaw Soe Lwin (`kylwin@ucsd.edu` / `kslwin.2000@gmail.com`)  
**Project Lead:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)  
**Milestone:** Task 10.1 (Data Ingestion Pipeline, Canonical Multi-Source Dataset, and QA Engine)  
**Associated Deliverables:** `data/MultiSource_Master_Monthly.csv`, `data_ingestion/`, `scripts/run_ingestion_pipeline.py`, `tests/test_data_ingestion.py`  

---

## 1. Executive Summary & Architectural Overview

**Task 10.1** establishes the high-performance multi-source data ingestion and temporal normalization infrastructure for the **Downtown San Diego Homeless Population Analysis** predictive forecasting system. 

Prior to Task 10.1, longitudinal modeling relied primarily on univariate monthly field counts (108 continuous monthly intervals from January 2017 to December 2025 across 11 neighborhood subdivisions). To empower the multi-source machine learning forecasters (Task 10.3) and automated anomaly detection engines (Task 10.4), Task 10.1 extracts, standardizes, validates, and aligns five foundational external data streams onto the canonical monthly time series index:

```
+---------------------------------------------------------------------------------------------------------+
|                                    Modular Ingestion Framework Architecture                             |
+---------------------------------------------------------------------------------------------------------+
|  [Source 1: City 311]    -->  get_it_done_311.py      --> Downtown Encampments, Dumping & Case Latency  |
|  [Source 2: NOAA/Meteo]  -->  weather_noaa.py         --> Daily Temperatures, Precipitation, CDD/HDD    |
|  [Source 3: MLB Events]  -->  major_events.py         --> Petco Park Games, Comic-Con, Civic Holidays   |
|  [Source 4: Macro Econ]  -->  economic_indicators.py  --> FRED Unemployment, CPI, Zillow ZORI Rent 92101|
|  [Source 5: Shelters]    -->  shelter_capacity.py     --> Bed Inventories, Safe Sleeping, Policy Bans   |
+---------------------------------------------------------------------------------------------------------+
                                                     │
                                                     ▼
+---------------------------------------------------------------------------------------------------------+
|                              MultiSourceAligner (data_ingestion/aligner.py)                             |
|  - Strict left joins on canonical 108-month index (2017-01-01 to 2025-12-01)                           |
|  - Relational join with MasterCounts_Adjusted_v2.csv ground truth totals                                |
|  - Output: data/MultiSource_Master_Monthly.csv (108 observations x 40 verified columns)                 |
+---------------------------------------------------------------------------------------------------------+
                                                     │
                                                     ▼
+---------------------------------------------------------------------------------------------------------+
|                           DataQualityValidator (data_ingestion/validator.py)                            |
|  - Temporal continuity & monotonicity check (108/108 contiguous months verified)                        |
|  - 0% critical null rates across all 40 columns                                                         |
|  - Physical domain bound verification (100% compliant)                                                  |
+---------------------------------------------------------------------------------------------------------+
```

---

## 2. Master Table Inventory (`MultiSource_Master_Monthly.csv`)

* **File Location:** `data/MultiSource_Master_Monthly.csv`
* **Temporal Grain:** Monthly (`YYYY-MM-01`), exactly 108 rows spanning `2017-01-01` to `2025-12-01`.
* **Total Schema Dimensions:** 40 columns (6 ground-truth counts + 9 weather + 5 events + 7 economic + 6 shelter/policy + 7 municipal 311).
* **Missing Value Rate:** **0.00%** across all external exogenous signals.

---

## 3. Comprehensive Data Dictionary

| Column Name | Data Type | Units / Range | Source System | Null % | Physical Bounds | Operational Description |
|---|---|---|---|---|---|---|
| `date` | `string` | `YYYY-MM-01` | Canonical Grid | 0.0% | 2017-01 to 2025-12 | First day of observation calendar month. |
| `downtown_actual_adjusted_count` | `float64` | Individuals | DSDP / DSA | 0.0% | $[400, 2500]^*$ | Adjusted unsheltered homeless population in Downtown core. |
| `downtown_actual_raw_count` | `float64` | Individuals | DSDP / DSA | 0.0% | $[400, 2500]^*$ | Raw unadjusted field tally across downtown survey routes. |
| `downtown_actual_individual_count` | `float64` | Individuals | DSDP / DSA | 0.0% | $[0, 2000]$ | Sub-tally of unhoused individuals observed outside structures. |
| `downtown_actual_tent_count` | `float64` | Tents / Structures | DSDP / DSA | 0.0% | $[0, 1500]$ | Sub-tally of observed tents and makeshift encampment structures. |
| `downtown_actual_vehicle_count` | `float64` | Vehicles | DSDP / DSA | 0.0% | $[0, 500]$ | Sub-tally of observed inhabited vehicles / RVs. |
| `weather_temp_mean_f` | `float64` | $^\circ\text{F}$ | Open-Meteo / NOAA | 0.0% | $[45.0, 85.0]$ | Monthly average surface air temperature at Lindbergh Field. |
| `weather_temp_max_f` | `float64` | $^\circ\text{F}$ | Open-Meteo / NOAA | 0.0% | $[55.0, 110.0]$ | Extreme maximum daily temperature recorded in month. |
| `weather_temp_min_f` | `float64` | $^\circ\text{F}$ | Open-Meteo / NOAA | 0.0% | $[32.0, 75.0]$ | Extreme minimum daily temperature recorded in month. |
| `weather_precip_total_in` | `float64` | Inches | Open-Meteo / NOAA | 0.0% | $[0.0, 15.0]$ | Cumulative monthly liquid precipitation. |
| `weather_rainy_days_count` | `int64` | Days | Open-Meteo / NOAA | 0.0% | $[0, 31]$ | Number of calendar days with precipitation $\ge 0.10$ inches. |
| `weather_extreme_heat_days_count` | `int64` | Days | Open-Meteo / NOAA | 0.0% | $[0, 31]$ | Number of calendar days with max temperature $\ge 85^\circ\text{F}$. |
| `weather_cdd_total` | `float64` | Degree-Days | Open-Meteo / NOAA | 0.0% | $\ge 0.0$ | Cumulative Cooling Degree Days: $\sum \max(0, T_{mean} - 65)$. |
| `weather_hdd_total` | `float64` | Degree-Days | Open-Meteo / NOAA | 0.0% | $\ge 0.0$ | Cumulative Heating Degree Days: $\sum \max(0, 65 - T_{mean})$. |
| `weather_wind_max_mph` | `float64` | MPH | Open-Meteo / NOAA | 0.0% | $[0.0, 60.0]$ | Peak wind speed recorded at Lindbergh Field. |
| `events_padres_home_games_count` | `int64` | Games | MLB Stats API | 0.0% | $[0, 22]$ | Total Padres home games played at Petco Park in East Village. |
| `events_padres_season_active` | `int64` | Binary $\{0, 1\}$ | MLB Calendar | 0.0% | $\{0, 1\}$ | 1 during active baseball season (Apr–Oct), 0 otherwise. |
| `events_comic_con_active` | `int64` | Binary $\{0, 1\}$ | Convention Center | 0.0% | $\{0, 1\}$ | 1 during San Diego Comic-Con convention, 0 otherwise. |
| `events_federal_holidays_count` | `int64` | Holidays | Statutory US | 0.0% | $[0, 4]$ | Count of statutory federal/state holidays in month. |
| `events_major_civic_intensity_k` | `float64` | Thousands | Composite Model | 0.0% | $\ge 0.0$ | Composite foot-traffic congestion driver index. |
| `econ_unemployment_rate_pct` | `float64` | Percent ($\%$) | FRED `CASAND5URN` | 0.0% | $[2.0, 30.0]$ | San Diego County monthly unemployment rate. |
| `econ_unemployment_yoy_chg` | `float64` | Pct Points | FRED `CASAND5URN` | 0.0% | $[-15.0, 15.0]$ | Year-over-year change in county unemployment rate. |
| `econ_cpi_sandiego_index` | `float64` | Index Points | FRED `CUUSA429SA0` | 0.0% | $[120.0, 220.0]$ | Semi-annual San Diego CPI smoothly interpolated to monthly. |
| `econ_cpi_sandiego_yoy_pct` | `float64` | Percent ($\%$) | FRED `CUUSA429SA0` | 0.0% | $[-5.0, 15.0]$ | Year-over-year consumer price index inflation rate. |
| `econ_rent_zori_downtown_92101` | `float64` | USD ($\$$) | Zillow ZORI | 0.0% | $[1500.0, 4000.0]$ | Observed typical monthly rent for Downtown ZIP 92101. |
| `econ_rent_zori_downtown_yoy_pct` | `float64` | Percent ($\%$) | Zillow ZORI | 0.0% | $[-15.0, 30.0]$ | Year-over-year rent inflation rate in ZIP 92101. |
| `econ_rent_zori_metro_sd` | `float64` | USD ($\$$) | Zillow ZORI | 0.0% | $[1500.0, 4000.0]$ | Observed typical monthly rent for San Diego Metro MSA. |
| `shelter_base_beds_capacity` | `int64` | Beds | SDHC / RTFH | 0.0% | $[1000, 2500]$ | Operational emergency and bridge shelter beds downtown. |
| `shelter_safe_sleeping_capacity` | `int64` | Spaces | City of San Diego | 0.0% | $[0, 1000]$ | Active municipal Safe Sleeping spaces (20th & B, O Lot). |
| `shelter_total_capacity` | `int64` | Total Units | SDHC / Municipal | 0.0% | $[1000, 3500]$ | Sum of baseline shelter beds and safe sleeping capacity. |
| `shelter_capacity_yoy_chg` | `float64` | Units | SDHC / Municipal | 0.0% | $[-1000, 1500]$ | Year-over-year change in available shelter/sleeping units. |
| `shelter_operation_shelter_to_home_active`| `int64` | Binary $\{0, 1\}$ | City / Convention | 0.0% | $\{0, 1\}$ | 1 during Convention Center COVID emergency operation. |
| `shelter_unsafe_camping_ban_active` | `int64` | Binary $\{0, 1\}$ | City of San Diego | 0.0% | $\{0, 1\}$ | 1 post-Unsafe Camping Ordinance enactment (Jul 2023+). |
| `service_311_total_requests_count` | `int64` | Requests | City of San Diego | 0.0% | $[0, 10000]$ | Total municipal 311 requests dispatched in Downtown core. |
| `service_311_encampment_requests_count` | `int64` | Requests | City of San Diego | 0.0% | $[0, 6000]$ | Encampment-specific complaint dispatches in Downtown. |
| `service_311_dumping_requests_count` | `int64` | Requests | City of San Diego | 0.0% | $[0, 2000]$ | Illegal dumping and debris service calls in Downtown. |
| `service_311_sanitation_requests_count` | `int64` | Requests | City of San Diego | 0.0% | $[0, 2000]$ | Sidewalk washing, right-of-way sanitation dispatches. |
| `service_311_closed_rate_pct` | `float64` | Percent ($\%$) | City of San Diego | 0.0% | $[0.0, 100.0]$ | Percentage of 311 calls resolved/closed within same month. |
| `service_311_mean_resolution_days` | `float64` | Days | City of San Diego | 0.0% | $[0.0, 90.0]$ | Mean elapsed days from service request filing to resolution. |
| `service_311_reporting_mature_flag` | `int64` | Binary $\{0, 1\}$ | Municipal Ops | 0.0% | $\{0, 1\}$ | 1 when mobile Get It Done app reached broad saturation (2019+). |

$^*$Note: Ground-truth counts equal 0.0 during 4 documented unperformed count months in late 2025 (Jul, Aug, Oct, Nov). All positive counted months strictly fall within $[400, 2500]$.

---

## 4. Technical Source Specifications & Ingestion Details

### 4.1 City of San Diego 311 "Get It Done" Service Requests
* **Official URL:** `https://data.sandiego.gov/datasets/get-it-done-311/`
* **Streaming Endpoint:** `https://seshat.datasd.org/get_it_done_reports/get_it_done_requests_CD3_datasd.csv`
* **Spatial Clipping:** Filtered for `comm_plan_name == 'DOWNTOWN'` and `council_district == 3`.
* **Throughput Performance:** Over 794,000 records processed in 3.27 seconds via line-buffered CSV streaming.
* **Maturity Boundary:** The City launched Get It Done in 2016, with full encampment logging adoption maturing by January 2019. The pipeline includes `service_311_reporting_mature_flag` to protect machine learning feature engineering against reporting-growth bias.

### 4.2 NOAA / Open-Meteo Surface Climatology
* **Station:** San Diego Lindbergh Field (KSAN, Lat: 32.7157, Lon: -117.1611, Elev: 15 ft).
* **API Endpoint:** `https://archive-api.open-meteo.com/v1/archive`
* **Units:** Natively extracted in standard US customary units (Fahrenheit, inches, MPH).
* **Empirical Relevance:** Empirically accounts for weather shocks (e.g. cold winter downpours driving unhoused individuals into emergency winter shelters, or extreme summer heat waves).

### 4.3 Major Civic Events & Stadium Attendance
* **MLB Stats API:** Official public REST endpoint `https://statsapi.mlb.com/api/v1/schedule` (Team ID 135).
* **Petco Park Dynamics:** Petco Park is located in South East Village (the primary epicenter of downtown unsheltered counts). High-density home stands coincide with enhanced sidewalk cleaning dispatches and perimeter enforcement.
* **San Diego Comic-Con:** ~135,000 attendees centered at the San Diego Convention Center and Gaslamp Quarter in late July. Accounting for Comic-Con removes false anomaly alerts during summer sweeps.

### 4.4 Macroeconomic Drivers (FRED & Zillow Research)
* **FRED San Diego Unemployment (`CASAND5URN`):** Captures labor market shocks (e.g. the April 2020 COVID peak at 15.9%).
* **FRED San Diego CPI (`CUUSA429SA0`):** Regional inflation index smoothly interpolated between semi-annual benchmarks.
* **Zillow Observed Rent Index (ZORI):** Extracted via streaming parser for Downtown ZIP 92101 and the San Diego Metro Area, capturing the steep housing affordability crisis that pushed typical downtown rents from $1,917/mo (Jan 2015) to over $2,880/mo (2024–2025).

### 4.5 Shelter Bed Inventories & Policy Regimes
* **Operation Shelter to Home:** Convention Center temporary de-densification shelter active from March 2020 through March 2021 (~1,300 occupants).
* **Safe Sleeping Sites:** City municipal safe sleeping site additions at 20th & B (opened July 2023, +400 beds) and O Lot in Balboa Park (opened October 2023, +400 beds -> 800 total).
* **Unsafe Camping Ordinance:** Banned tent encampments on public sidewalks when shelter beds are available, enacted in July 2023.

---

## 5. Automated Data Quality Audit Report

The table below reflects the automated audit generated by `DataQualityValidator.run_full_audit()`:

```text
=======================================================
DATA QUALITY AUDIT REPORT: PASSED
=======================================================
Audit Execution Timestamp: 2026-10-04 12:10:21
Dataset Target: data/MultiSource_Master_Monthly.csv
Status: PASSED (100% Compliant)

Temporal Continuity:
  - Row Count: 108 contiguous monthly observations
  - Expected Range: 2017-01-01 to 2025-12-01
  - Monotonicity: Strictly increasing (0 missing intervals)
  - Result: PASS

Completeness & Null Check:
  - Critical Schema Columns: 40
  - Total Missing Values: 0 (0.00% null rate)
  - Result: PASS

Domain Boundary Compliance:
  - Temperature Mean: 55.4°F to 76.8°F (within [45.0, 85.0])
  - Total Precipitation: 0.00 in to 6.25 in (within [0.0, 15.0])
  - Padres Home Games: 0 to 17 games/month (within [0, 22])
  - Unemployment Rate: 2.7% to 15.9% (within [2.0, 30.0])
  - Downtown Rent 92101: $2,063 to $2,899/month (within [1500.0, 4000.0])
  - Total Shelter Capacity: 1,350 to 2,850 units (within [1000, 3500])
  - 311 Monthly Requests: 312 to 3,425 requests/month (within [0, 10000])
  - Result: PASS
=======================================================
```

---

## 6. Downstream Consumption Guide for Task 10.2 & 10.3

The output table `data/MultiSource_Master_Monthly.csv` is immediately ready for consumption:

1. **Task 10.2 (Feature Engineering Module - 50+ Features):**
   * **Lag Features:** 1, 2, 3, 6, and 12-month lags of `service_311_encampment_requests_count`, `econ_unemployment_rate_pct`, and `econ_rent_zori_downtown_yoy_pct`.
   * **Rolling Window Statistics:** 3-month and 6-month rolling averages and standard deviations of precipitation, temperature, and 311 request volume.
   * **Interaction Terms:** Interaction between `shelter_unsafe_camping_ban_active` and `shelter_safe_sleeping_capacity`.
2. **Task 10.3 (Ensemble Prediction System):**
   * Feed exogenous feature matrix into Gradient Boosting (XGBoost/LightGBM), Bayesian Structural Time Series (BSTS), and Temporal Neural Networks.
3. **Task 10.4 (Anomaly Detection & Early Warning):**
   * Utilize `service_311_encampment_requests_count` residuals against historical prediction envelopes to alert when rapid street encampment expansions deviate from seasonal capacity baselines.
