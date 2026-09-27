# Task 9.1: Interactive Dashboard Design & Implementation Plan
## Downtown San Diego Homeless Population Analysis

**Document Status:** Production Ready  
**Project:** Downtown San Diego Homeless Population Analysis (Data Science Alliance)  
**Author / Contributor:** Kyaw Soe Lwin (`kylwin@ucsd.edu` / `kslwin.2000@gmail.com`)  
**Project Lead:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)  
**Deliverable Target:** Task 9.1 Interactive Dashboard & Deployment Protocol  

---

## Executive Summary & Objectives

The primary goal of **Task 9.1** is to synthesize the extensive empirical, econometric, spatial, and predictive findings from **Assignments 1 through 8** into a unified, executive-ready, interactive web dashboard. 

The dashboard provides municipal leaders, service providers, researchers, and community stakeholders with an accessible, high-performance platform for evidence-based decision-making. It bridges the gap between complex econometric models and policy execution by providing dynamic historical exploration, 12-month prospective forecasting with policy scenarios, block-level hotspot surveillance, neighborhood time-series decomposition, and a macro-level countywide estimation calculator governed by strict public communication rules.

```
+---------------------------------------------------------------------------------------------------+
|                        Downtown San Diego Homelessness Executive Dashboard                        |
+---------------------------------------------------------------------------------------------------+
| [1. Historical Trends] | [2. Forecast View] | [3. Hotspot Map] | [4. Neighborhoods] | [5. County Calc] | [6. About] |
+---------------------------------------------------------------------------------------------------+
| - 2017-2025 Series     | - 2026 12M Horizon | - 12 Date Gi*    | - STL Decomp       | - Regime OLS Calc | - DSDP/RTFH|
| - 4 Multiplier Regimes | - 80% & 95% PIs    | - 261/382 Blocks | - Seasonal CIs     | - Student's t PI  | - 261->382 |
| - Raw vs Constant Meth | - Policy Scenarios | - Centroid Shift | - Cross-Area Stats | - 4 Comm Rules    | - 2017 Base|
+---------------------------------------------------------------------------------------------------+
```

---

## 1. Technical Architecture & Technology Stack

### 1.1 Core Framework Selection: Streamlit
* **Selected Framework:** **Streamlit (`>= 1.35.0`)**
* **Architectural Rationale:**
  * **Rapid Reactive Execution:** Streamlit's pure Python execution model eliminates frontend/backend bifurcation, enabling instant state synchronization across multi-tiered filters.
  * **Built-in In-Memory Caching:** `@st.cache_data` and `@st.cache_resource` provide microsecond data retrievability, satisfying the sub-5-second page load mandate.
  * **Native Cloud Deployment:** Seamless integration with Streamlit Community Cloud (zero-container overhead, automatic HTTPS, Git webhook CD/CI).
  * **Ecosystem Parity:** Direct integration with Plotly, Folium/Leaflet, Pandas, and GeoPandas without complex serialization boilerplate.

### 1.2 Technology & Library Stack
| Layer | Library / Tool | Version | Operational Function |
|---|---|---|---|
| **Web Framework** | `streamlit` | `^1.35.0` | Reactive application runtime, layout, and component state management |
| **Interactive Charts** | `plotly` | `^5.22.0` | Interactive time series, scenario envelopes, and decomposition subplots |
| **Geospatial Mapping** | `streamlit-folium`<br>`folium` | `^0.20.0`<br>`^0.16.0` | Vector polygon rendering, Getis-Ord Gi* choropleth maps, custom tooltips |
| **Spatial Engine** | `geopandas`<br>`shapely` | `^0.14.4`<br>`^2.0.4` | GeoJSON ingestion, centroid calculations, spatial boundary filtering |
| **Data & Computation** | `pandas`<br>`numpy` | `^2.2.0`<br>`^1.26.4` | Vectorized aggregations, rolling metrics, and data wrangling |
| **Statistical Modeling** | `scipy`<br>`statsmodels` | `^1.13.0`<br>`^0.14.2` | Exact Student's $t$ prediction intervals, STL seasonal component extraction |
| **Testing & Quality** | `pytest`<br>`requests` | `^8.2.0`<br>`^2.32.0` | Unit testing of calculator equations, data contracts, and response latency |

### 1.3 Design System & Visual Hierarchy
* **Typography:** Clean sans-serif hierarchy (`Inter`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `Roboto`).
* **Design Language:** Executive Slate / Navy thematic system with high-contrast accessibility (WCAG AA compliant):
  * **Canvas Background:** `#F8FAFC` (Slate 50)
  * **Card / Container Background:** `#FFFFFF` (Pure White) with subtle `#E2E8F0` border
  * **Primary Header & Text:** `#0F172A` (Slate 900)
  * **Secondary / Muted Text:** `#64748B` (Slate 500)
  * **Primary Accent:** `#2563EB` (Royal Blue - Historical & Navigation)
  * **Forecast Accent:** `#0D9488` (Teal - Prospective Model & Uncertainty Bands)
  * **Intervention Markers:** `#D97706` (Amber - Multiplier Changes), `#7C3AED` (Purple - Camping Ordinance)
  * **Gi* Hotspot Scale:**
    * 99% Hotspot ($z \ge 2.576$): `#B91C1C` (Deep Red)
    * 95% Hotspot ($z \ge 1.960$): `#EF4444` (Crimson)
    * 90% Hotspot ($z \ge 1.645$): `#F87171` (Coral)
    * Not Significant ($|z| < 1.645$): `#E2E8F0` (Neutral Grey)
    * 90% Coldspot ($z \le -1.645$): `#93C5FD` (Soft Sky)
    * 95% Coldspot ($z \le -1.960$): `#3B82F6` (Cobalt)
    * 99% Coldspot ($z \le -2.576$): `#1D4ED8` (Navy Blue)

---

## 2. Directory Layout & File Structure

The project structure separates frontend presentation, data engineering contracts, business logic, and testing:

```text
Downtown-Homeless-Analysis/
├── app.py                             # Main Streamlit application entry point
├── requirements.txt                   # Production dependencies (optimized for cloud runtime)
├── runtime.txt                        # Python version pinning (python-3.11)
├── README.md                          # Public repo overview & dashboard architecture
│
├── .streamlit/
│   └── config.toml                    # Server settings, theme palette, layout width
│
├── src/
│   ├── __init__.py
│   ├── config.py                      # Global constants, colors, date limits, regime markers
│   ├── data_loader.py                 # Cached ingestion, schema validation, type enforcement
│   ├── utils.py                       # KPI formatters, Student's t math, scenario engines
│   │
│   ├── components/                    # Modular page renderers (Tabs 1 through 6)
│   │   ├── __init__.py
│   │   ├── header.py                  # Executive branding, high-level KPIs, global filters
│   │   ├── tab1_historical.py         # Component 1: Longitudinal Trends & Multiplier Regimes
│   │   ├── tab2_forecast.py           # Component 2: 12-Month Prospective Forecasts & Scenarios
│   │   ├── tab3_hotspots.py           # Component 3: Geospatial Gi* Hotspot Surveillance Map
│   │   ├── tab4_decomposition.py      # Component 4: Neighborhood Decomposition & Comparison
│   │   ├── tab5_calculator.py         # Component 5: County Estimation Calculator & 4 Rules
│   │   └── tab6_about.py              # Component 6: Methodology, Data Governance & Footprint
│   │
│   └── styles/
│       └── custom.css                 # Clean card styling, metric badges, button overrides
│
├── data/                              # Production analytical datasets (Assignments 1-8)
│   ├── MasterCounts_Adjusted_v2.csv          # Canonical monthly counts (2,814 rows)
│   ├── TimeSeries_ConstantMethodology.csv    # Rescaled constant-methodology series (924 rows)
│   ├── Forecasts_12Month.csv                 # 2026 prospective forecasts with PIs & scenarios
│   ├── Forecast_ModelComparison.csv          # CV and hold-out benchmark metrics
│   ├── Forecast_CV_Metrics.csv               # 5-fold CV evaluation table
│   ├── Downtown_BlockGrid.geojson            # 382 Downtown block polygons
│   ├── Hotspot_Classifications.geojson       # 3,132 block-date Getis-Ord Gi* classifications
│   ├── Hotspot_Summary_ByDate.csv            # Date-level cluster aggregations
│   ├── Hotspot_Persistence_Ranking.csv       # 261-block longitudinal persistence ranking
│   ├── Hotspot_Top10_Context.csv             # Nearest OSM transit/service proximity table
│   ├── Hotspot_Migration_Centroids.csv       # Centroid displacement coordinates
│   ├── SeasonalIndices.csv                   # Monthly seasonal indices, CIs, p-values
│   ├── StructuralBreaks.csv                  # Chow and CUSUM structural break metrics
│   ├── Downtown_County_PairedCounts.csv      # 8-year paired DSDP/RTFH dataset
│   ├── Downtown_County_RatioStability.csv    # ANOVA & Kruskal-Wallis ratio metrics
│   └── CountyEstimate_Current.csv            # Current Dec 2025 macro estimates & PIs
│
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py            # Automated schema checks & row-count validation
│   ├── test_calculator.py             # Validation of Policy Regime OLS & Student's t PIs
│   └── test_forecast_logic.py         # Scenario math (-24%, +26%) & PI monotonic sanity
│
└── docs/
    └── Dashboard_DeploymentInfo.md    # Master deployment runbook & Google Doc specification
```

---

## 3. Data Ingestion & Caching Contracts

To ensure sub-5-second page loads and complete isolation from computationally heavy model training pipelines, the dashboard ingests **precomputed analytical artifacts** produced in Assignments 1 through 8.

```
+-------------------------------------------------------------------------------------------------+
|                                    Data Ingestion Pipeline                                      |
+-------------------------------------------------------------------------------------------------+
| Master Data Files                       Data Loader (@st.cache_data)       Dashboard Consumers  |
|                                                                                                 |
| MasterCounts_Adjusted_v2.csv        --> [load_historical_data()]        --> Component 1 & 4     |
| TimeSeries_ConstantMethodology.csv  --> [load_constant_series()]        --> Component 1 & 2     |
| Forecasts_12Month.csv               --> [load_forecast_data()]          --> Component 2         |
| Hotspot_Classifications.geojson     --> [load_hotspot_geodata()]        --> Component 3         |
| Downtown_BlockGrid.geojson          --> [load_grid_geodata()]           --> Component 3         |
| SeasonalIndices.csv                 --> [load_decomposition_data()]     --> Component 4         |
| Downtown_County_PairedCounts.csv    --> [load_paired_county_data()]     --> Component 5         |
+-------------------------------------------------------------------------------------------------+
```

### 3.1 Dataset Ingestion Contracts

| Dataset | Canonical Source | Row / Feature Count | Primary Keys | Ingestion Validation Criteria |
|---|---|---|---|---|
| **Historical Counts** | `MasterCounts_Adjusted_v2.csv` | 2,814 rows | `date`, `area_name`, `component` | Filter: `component == 'total'` & `area_type == 'neighborhood'`. Validate 708 headline rows, dates `2017-01-01` to `2025-12-01`. |
| **Constant Methodology** | `TimeSeries_ConstantMethodology.csv` | 924 rows | `date`, `series_id` | Confirm 9 series present. Verify `constant_methodology_count` non-null. |
| **Prospective Forecasts** | `Forecasts_12Month.csv` | 108 rows | `series_name`, `forecast_date` | 9 series × 12 months (`2026-01-01` to `2026-12-01`). Check columns: `point_forecast`, `pi_80_lower/upper`, `pi_95_lower/upper`, `optimistic_scenario`, `pessimistic_scenario`. |
| **Hotspot Classifications** | `Hotspot_Classifications.geojson` | 3,132 features | `block_id`, `count_date` | 261 balanced blocks × 12 dates. CRS must be EPSG:4326. Validate Gi* z-score, p-value, and classification labels. |
| **Block Grid Polygons** | `Downtown_BlockGrid.geojson` | 382 features | `block_id` | EPSG:4326 geometry validation. Attributes: `block_id`, `neighborhood`. |
| **Hotspot Rankings** | `Hotspot_Persistence_Ranking.csv` | 261 rows | `block_id` | Top block must match `16TH_ST_IMPERIAL_AV` (9/12 dates). |
| **Seasonal Indices** | `SeasonalIndices.csv` | 108 rows | `series_name`, `month` | 9 series × 12 months. Validate `seasonal_index`, `ci_lower`, `ci_upper`, `kw_pvalue`. |
| **Structural Breaks** | `StructuralBreaks.csv` | 57 rows | `series_name`, `break_event` | Chow F-test statistics and within-event FDR p-values. |
| **Paired PIT Counts** | `Downtown_County_PairedCounts.csv` | 8 rows | `year` | Years 2017–2025 (2021 skipped). Confirm `county_unsheltered`, `city_unsheltered`, `downtown_reported_adjusted`. |

### 3.2 Caching Strategy (`src/data_loader.py`)
All loading functions use `@st.cache_data(show_spinner=False, ttl=3600)`. GeoJSON parsing uses GeoPandas once into memory, caching simplified Shapely geometries and attribute dictionaries to avoid repeated JSON serialization.

---

## 4. Step-by-Step Implementation of Dashboard Components

### Component 1: Historical Trends View
* **Objective:** Display the full longitudinal trajectory (2017–2025) of unsheltered homelessness in Downtown San Diego, highlighting critical methodology shifts and policy inflection points.
* **UI Controls & Interactivity:**
  * **Series / Neighborhood Filter:** Multi-select dropdown featuring:
    * `Overall - reported footprint` (All reporting areas)
    * `Overall - fixed core six` (Balanced historical footprint)
    * 7 Individual Neighborhoods (`East Village`, `City Center`, `Columbia`, `Cortez`, `Gaslamp`, `Marina`, `Outside Perimeter`).
  * **Methodology Alignment Toggle:**
    * Option A: *Published Adjusted Counts* (DSDP operational baseline).
    * Option B: *Constant-Methodology Hybrid Series* (Rescaled to POST2020 standard).
  * **Date Range Range-Slider:** Dynamic range from `2017-01-01` to `2025-12-01`.
  * **Regime Annotation Toggle:** Show/hide vertical marker lines for key methodology and macro events:
    1. `2017-04-01`: APR2017 Multiplier Change (Tent $2.00 \rightarrow 1.75$, Vehicle $2.00 \rightarrow 1.66$).
    2. `2018-05-01`: MAY2018 Multiplier Change (Vehicle $1.66 \rightarrow 2.03$).
    3. `2020-03-01`: COVID-19 Pandemic Emergency Declaration.
    4. `2023-07-31`: City of San Diego Unsafe Camping Ordinance Enacted.
  * **Component Breakdown Mode:** When a single neighborhood is selected, a secondary toggle allows breaking down the total into Individuals, Tents, and Vehicles.
* **Visualization Implementation:**
  * Interactive Plotly figure (`go.Scatter`) with hover templates showing date, exact count, YoY change, and active multiplier regime.
  * Shaded background intervals for COVID-19 (March 2020 – June 2021) and Post-Camping Ordinance (August 2023 – Present).
* **KPI Metric Cards:**
  * Current Total Count (Latest available month).
  * All-Time Peak Count (`2,103` in May 2023).
  * COVID Era Trough (`689` in April 2020).
  * YoY % Contraction (`-43.5%` following camping ordinance).

---

### Component 2: 12-Month Prospective Forecast View
* **Objective:** Present rigorous, prospective 12-month ahead projections (2026-01 to 2026-12) based on Assignment 7's cross-validated machine learning and econometric models.
* **UI Controls & Interactivity:**
  * **Neighborhood / Series Selector:** Select between citywide aggregates or individual neighborhoods.
  * **Model Family Selector:**
    * `XGBoost Champion` (Citywide 12-month CV MAPE: **39.34%**, hold-out test MAPE: **38.48%**).
    * `Holt-Winters Parametric` (CV MAPE: **39.57%**, smooth parametric trend).
    * `SARIMA` (Optimal seasonal differencing benchmark).
    * `Prophet` (Historical changepoint architecture).
    * `Naive Seasonal Baseline` (Prior year $t-12$ benchmark, CV MAPE: 51.34%).
  * **Policy Scenario Mode:**
    * `Baseline (Status Quo)`: Pure statistical champion trajectory.
    * `Optimistic (-24% at Month 12)`: Graduated ramp down reflecting aggressive shelter expansion and rapid permanent supportive housing placement.
    * `Pessimistic (+26% at Month 12)`: Graduated ramp up reflecting shelter capacity exhaustion, regional economic shocks, or legal injunctions on enforcement.
    * `Interactive Custom Scenario Slider`: Allows policy makers to stress-test arbitrary $\pm 40\%$ year-end shifts.
  * **Prediction Interval Toggles:** Independent toggles for 80% and 95% uncertainty envelopes.
* **Visualization Implementation:**
  * Plotly visualization displaying historical context (2024–2025 actuals) transitioning smoothly into the 2026 forecast horizon.
  * Shaded uncertainty fan charts:
    * 95% Prediction Interval: Shaded translucent teal (`rgba(13, 148, 136, 0.15)`).
    * 80% Prediction Interval: Shaded medium teal (`rgba(13, 148, 136, 0.25)`).
    * Baseline Forecast: Solid dark teal line (`#0D9488`, width 3).
    * Optimistic Scenario: Dashed green line (`#16A34A`).
    * Pessimistic Scenario: Dashed red line (`#DC2626`).
* **Benchmarking & Validation Expander:**
  * Collapsible table displaying 5-fold walk-forward cross-validation performance metrics (RMSE, MAE, MAPE) across 1, 3, 6, and 12-month cumulative evaluation horizons.

---

### Component 3: Geospatial Hotspot Surveillance Map (Getis-Ord Gi\*)
* **Objective:** Map spatial concentration, statistically significant spatial clustering, and the longitudinal migration of unsheltered homelessness across downtown city blocks.
* **UI Controls & Interactivity:**
  * **Count Date Selector:** Dropdown / Slider accessing the 12 digitized count dates:
    * `2018-01-24`, `2018-06-27`, `2018-12-19`
    * `2019-01-30`, `2020-01-31`, `2021-02-25`
    * `2022-01-27`, `2022-03-01` (Flagged: source-map date anomaly)
    * `2023-01-31`, `2024-01-25`, `2025-01-31`
  * **Footprint Scope Toggle:**
    * *Balanced Longitudinal Panel (261 blocks)*: Statistically valid across all 12 dates (2018–2025).
    * *Expanded Footprint (382 blocks)*: Enabled only for 2022–2025 dates (incorporates Golden Hill, Barrio Logan, Sherman Heights).
  * **Significance Filter:** Multi-select for `99% Hotspot`, `95% Hotspot`, `90% Hotspot`, `Not Significant`, `Coldspot`.
* **Map Engine (`folium` + `streamlit-folium`):**
  * Base layer: CartoDB Positron (clean, high-contrast, uncluttered basemap).
  * Polygons: Downtown block polygons shaded by Gi* classification.
  * Vector Styling: Dynamic boundary highlights on hover.
  * Popups & Tooltips:
    * Block ID (e.g. `16TH_ST_IMPERIAL_AV`).
    * Neighborhood (e.g. `East Village`).
    * Total Adjusted Count, Individuals, Tents, Vehicles.
    * Getis-Ord Gi* $z$-score and permutation $p$-value.
* **Supporting Analytical Panels:**
  * **Top Persistent Hotspots Table:** Displays `Hotspot_Persistence_Ranking.csv` showing blocks that remained significant across the most count dates (Leader: `16TH_ST_IMPERIAL_AV`, significant on 9 of 12 dates).
  * **Centroid Migration Callout Card:** Visualizes the **121-meter southward centroid migration** toward Commercial St / Imperial Ave between the early (2018–2020) and recent (2022–2025) epochs.
  * **OSM Service & Transit Proximity:** Proximity indicators showing distance to nearest transit stops and day centers.

---

### Component 4: Neighborhood Deep-Dive & Time Series Decomposition
* **Objective:** Disaggregate citywide totals to reveal localized trends, robust STL time-series decompositions, seasonality tests, and cross-neighborhood variance.
* **UI Controls & Interactivity:**
  * **Neighborhood Focus Selector:** Single-select dropdown (`East Village`, `City Center`, `Columbia`, `Cortez`, `Gaslamp`, `Marina`, `Outside Perimeter`).
* **Visualizations & Statistical Modules:**
  * **STL Decomposition Subplots (4 Panes):**
    1. *Observed Series:* Historical monthly counts.
    2. *Trend Component:* De-seasonalized long-term trajectory.
    3. *Seasonal Component:* Recurring monthly cycle (quantifying why citywide seasonal strength is near zero).
    4. *Residual / Irregular Component:* Highlighting exogenous shocks.
  * **Monthly Seasonal Indices & Significance:**
    * Bar chart showing monthly deviations from trend with 95% confidence intervals.
    * Kruskal-Wallis non-parametric test annotation ($H$-statistic and $p$-value) proving that **8 of 9 series exhibit no statistically significant seasonality** (East Village summer bump is non-significant; Marina is the sole borderline series).
  * **Cross-Neighborhood Comparison Panel:**
    * Summary metric matrix: Average Count, Std Dev, Peak Volume, Post-Ordinance % Change.
    * Boxplot distribution comparing dispersion and extreme outliers across all 7 neighborhoods.

---

### Component 5: County-Level Estimation Calculator & Governance Charter
* **Objective:** Implement the validated Policy Regime OLS model ($Y = 4,513.26 + 0.1859 \cdot X + 1,225.04 \cdot D_{post}$) for interim macro-tracking, strictly enforcing the 4 Public Communication Rules and governance limitations.
* **Mathematical Specification:**
  $$\hat{Y} = \beta_0 + \beta_1 \cdot X + \beta_2 \cdot D_{\text{post}}$$
  Where:
  * $\beta_0 = 4,513.26$ (Non-downtown countywide baseline unsheltered unhoused)
  * $\beta_1 = 0.1859$ (Downtown elasticity slope coefficient)
  * $\beta_2 = 1,225.04$ (Structural policy shift indicator coefficient)
  * $X =$ Downtown monthly count input
  * $D_{\text{post}} \in \{0, 1\}$ (Post-July 2023 Camping Ordinance enforcement indicator)
  * Degrees of Freedom: $df = N - 3 = 8 - 3 = 5$
  * Student's $t$ critical value at 95% confidence: $t_{5, 0.975} = 2.571$
  * Prediction Standard Error:
    $$SE_{\text{pred}}(X_0, D_0) = \hat{\sigma}_{\varepsilon} \sqrt{1 + \mathbf{x}_0^T (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{x}_0}$$
    Calibrated empirical margin of error: $\approx \pm 2,050$ individuals ($\pm 35\%$).
* **UI Controls & Inputs:**
  * **Downtown Count Input ($X$):** Numeric input and slider (range: $200$ to $2,500$).
  * **Quick Preset Buttons:**
    * *Latest Baseline (Dec 2025):* $X = 985$
    * *Prospective Forecast (Jan 2026):* $X = 886$
    * *Peak Crisis (May 2023):* $X = 2,103$
    * *COVID Low (April 2020):* $X = 689$
  * **Policy Enforcement Toggle ($D_{\text{post}}$):**
    * `Active Camping Ordinance (Post-July 2023)` ($D_{\text{post}} = 1$)
    * `Pre-Ordinance / Non-Enforcement Baseline` ($D_{\text{post}} = 0$)
* **Executive Calculation Output & The 4 Public Communication Rules:**
  * **Rule 1 (Precision Prohibition):** Single-point raw outputs (e.g. `5,921`) are explicitly hidden or visually struck through.
  * **Rule 2 (Mandatory Rounding):** Primary display mandates rounding to the nearest 100 individuals (`5,900`).
  * **Rule 3 (Mandatory Calibrated Range):** Must display the full 95% Student's $t$ prediction interval:  
    $$\mathbf{5,900} \quad [\mathbf{3,900} \text{ to } \mathbf{8,000}]$$
  * **Rule 4 (Policy Context Disclosure):** Explicit disclaimer badge stating: *"Estimate assumes active enforcement of the City of San Diego Unsafe Camping Ordinance ($D_{post}=1$)."*
* **Statutory Governance Warning Banner:**
  * Prominent red callout box:
    > **GOVERNANCE NOTICE (Task 8.4 Charter):** This tool is authorized strictly for interim directional tracking and macro capacity stress-testing. It is **STRICTLY PROHIBITED** for official HUD Continuum of Care submissions, statutory budget formulas, and sub-regional micro-allocations.
* **Longitudinal Ratio Context Expander:**
  * Visualizes the 8-year paired DSDP vs RTFH Point-in-Time data, proving why simple constant-ratio models failed (ANOVA $F=66.51, p=0.0002$).

---

### Component 6: Methodology, Data Governance & Footprint Expansion
* **Objective:** Transparently document the data provenance, methodology adjustments, and spatial boundary expansions across the study period.
* **Content Sections:**
  1. **Data Sources & Provenance:**
     * Downtown San Diego Partnership (DSDP) Clean & Safe monthly morning counts (unsheltered).
     * Regional Task Force on Homelessness (RTFH) annual Point-in-Time (PIT) counts.
  2. **The 4 Multiplier Regimes:**
     * Comprehensive timeline of DSDP multipliers for individuals ($1.0\times$), tents ($1.75\times$), and vehicles ($1.66\times \rightarrow 2.03\times$).
     * The January 2020 divergence: RTFH eliminated multipliers for HUD compliance; DSDP retained them for longitudinal consistency.
  3. **Methodology Adjustment Strategy:**
     * Explanation of the *Constant-Methodology Hybrid Series* (Task 6.2/6.3) that rescales pre-2020 counts onto the POST2020 standard.
  4. **The 2022 Footprint Expansion Warning:**
     * Deep dive into the addition of 121 blocks in Golden Hill, Barrio Logan, and Sherman Heights in January 2022 (expanding from 261 to 382 blocks).
     * Documentation that **$4\%$ to $33\%$ of post-2021 total counts were purely driven by boundary expansion**.
  5. **Data Quality & Audit Log:**
     * Accounting for the 134 null values in raw data (116 reporting lag, 18 missing PDF table).
     * Correction of the series start date to January 2017 (disproving the 2012 myth).
     * March 2022 block map date anomaly notice.

---

## 5. Performance Optimization & Caching Strategy (< 5-Second Target)

To guarantee page load times well under the 5-second target (target: $< 2.0$ seconds initial load, $< 300$ ms per tab interaction) on standard cloud hardware (Streamlit Community Cloud 1 vCPU / 1GB RAM):

```
+-------------------------------------------------------------------------------------------------+
|                                 Performance Optimization Engine                                 |
+-------------------------------------------------------------------------------------------------+
| 1. Zero Runtime Training   | All SARIMA, XGBoost, STL, and Gi* models precomputed into CSV/GeoJSON |
| 2. Geometry Simplification | GeoJSON coordinates rounded to 5 decimal places (~1m precision)    |
| 3. In-Memory Cache         | @st.cache_data with 1-hour TTL and fast PyArrow deserialization    |
| 4. Lazy Folium Rendering   | Component 3 map initialized only upon tab activation               |
| 5. Lightweight Dependencies| Exclude heavy training packages (cmdstanpy, prophet) from cloud app|
+-------------------------------------------------------------------------------------------------+
```

### 5.1 Optimization Techniques
1. **Pre-computation Mandate:**
   * No machine learning models (XGBoost, Prophet) or spatial permutation tests (Getis-Ord Gi* 9,999 permutations) execute at dashboard runtime. All predictions, intervals, and cluster statistics are read directly from canonical CSVs/GeoJSONs.
2. **GeoJSON Payload Compression:**
   * `Downtown_BlockGrid.geojson` and `Hotspot_Classifications.geojson` are cleaned and simplified to 5 decimal places of coordinate precision (accuracy within 1.1 meters), reducing payload size by $> 45\%$.
3. **Session State & Reactive Filtering:**
   * Filter queries use vectorized Pandas indexing (`df[df['neighborhood'] == selected]`) rather than iterated loops.
4. **Target Performance Budget:**
   * Initial App Boot: **$1.2 - 1.8$ seconds**
   * Historical Trends Tab Render: **$< 200$ ms**
   * Forecast Tab Render: **$< 250$ ms**
   * Hotspot Map Generation: **$< 800$ ms**
   * Calculator Reactive Update: **$< 50$ ms**

---

## 6. Step-by-Step Testing & Verification Protocol

The testing framework covers mathematical accuracy, data integrity, user interaction, and performance benchmarks:

```
+-------------------------------------------------------------------------------------------------+
|                                     Testing & QA Matrix                                         |
+-------------------------------------------------------------------------------------------------+
| Unit Tests (pytest)        | UI Interaction Tests        | Governance & Math Tests              |
| - test_data_loader.py      | - Multi-select empty states | - Student's t distribution df=5      |
| - test_schema_keys.py      | - Date slider boundaries    | - Calculator 100-rounding rule       |
| - test_geojson_validity.py | - Map zoom / tooltip hover  | - PI monotonicity (lower <= upper)   |
+-------------------------------------------------------------------------------------------------+
```

### 6.1 Automated Unit Tests (`pytest tests/`)
* **Test 1: Data Contract Integrity (`test_data_loader.py`)**
  * Assert `MasterCounts_Adjusted_v2.csv` has exactly 2,814 rows and 0 nulls in key identifiers.
  * Assert `Forecasts_12Month.csv` has 108 rows covering 9 series and 12 months.
  * Assert `Hotspot_Classifications.geojson` contains exactly 3,132 features.
* **Test 2: Calculator Mathematics (`test_calculator.py`)**
  * Assert that inputting $X = 985.38$ with $D_{post} = 1$ yields point estimate $5,921.49 \approx 5,900$.
  * Assert that inputting $X = 985.38$ with $D_{post} = 0$ yields point estimate $4,696.45 \approx 4,700$.
  * Assert that calculated 95% PI lower bound is strictly less than point estimate, and upper bound is strictly greater.
* **Test 3: Scenario Sanity (`test_forecast_logic.py`)**
  * Assert that Month 12 Optimistic Forecast equals $\text{Baseline} \times (1 - 0.24)$.
  * Assert that Month 12 Pessimistic Forecast equals $\text{Baseline} \times (1 + 0.26)$.

### 6.2 Manual & UI Verification Steps
1. **Empty Filter Handling:** Deselect all neighborhoods in Component 1; verify app defaults gracefully to `Overall - reported footprint` without raising an unhandled exception.
2. **Date Range Continuity:** Move the historical slider to 2018–2020; verify plots update dynamically and annotations resize properly.
3. **Map Rendering & Tooltip Check:** Select `2022-03-01` on Hotspot Map; confirm warning badge appears regarding source-map date anomaly; click block `16TH_ST_IMPERIAL_AV` and confirm popup displays $z \ge 2.576$.
4. **Calculator Presets:** Click "2023 Peak Crisis" button; verify count input snaps to $2,103$ and prediction updates instantaneously.

---

## 7. Deployment & Delivery Workflow

### 7.1 GitHub Repository Configuration
* **Target Repository:** `https://github.com/CapMorningStar/Downtown-Homeless-Analysis.git`
* **Branch Strategy:**
  * `main`: Production release branch linked to Streamlit Cloud.
  * `feat/task9-dashboard`: Active development branch for Task 9.1 dashboard assets.
* **Production `requirements.txt` Optimization:**
  To ensure rapid builds on Streamlit Community Cloud without compiling heavy dependencies from source, omit dev libraries (`playwright`, `cmdstanpy`, `pymupdf`):
  ```text
  streamlit>=1.35.0
  plotly>=5.22.0
  streamlit-folium>=0.20.0
  folium>=0.16.0
  pandas>=2.2.0
  numpy>=1.26.4
  geopandas>=0.14.4
  shapely>=2.0.4
  scipy>=1.13.0
  statsmodels>=0.14.2
  ```

### 7.2 Streamlit Community Cloud Deployment Protocol
1. Log into [Streamlit Community Cloud](https://share.streamlit.io/) with authorized GitHub account (`@CapMorningStar`).
2. Click **"New App"**.
3. Select Repository: `CapMorningStar/Downtown-Homeless-Analysis`.
4. Select Branch: `main`.
5. Main file path: `app.py`.
6. Advanced Settings: Python version `3.11`.
7. Click **"Deploy!"**.
8. Verify custom subdomain assignment: `downtown-sd-homelessness.streamlit.app` (or default generated slug).

### 7.3 Google Drive Deliverable Protocol
* **Target Folder:** `Shared with me > Downtown Homelessness > Deliverables > Assignment 9 - Interactive Dashboard & Strategic Synthesis`
* **Deliverable Artifact:** `Dashboard_DeploymentInfo` (Google Doc)
* **Document Contents:**
  * Public Live URL of the deployed dashboard.
  * GitHub repository commit hash and source code links.
  * System architecture summary and directory manifest.
  * Step-by-step user guide for municipal stakeholders.
  * Testing sign-off and latency audit benchmarks.
* **Submission Protocol:**
  * Markdown draft generated locally as `docs/Dashboard_DeploymentInfo.md`.
  * Synced to Google Drive via Google Docs conversion.
  * Asana Task 9.1 updated with completion memo and live URLs.

---

## 8. Implementation Roadmap & Execution Checklist

| Step | Milestone / Action Item | Target File(s) | Status |
|---|---|---|---|
| **Phase 1** | Set up repository layout, `.streamlit/config.toml`, and `requirements.txt` | `requirements.txt`, `config.toml` | Pending |
| **Phase 2** | Build cached data ingestion engine & unit tests | `src/data_loader.py`, `tests/` | Pending |
| **Phase 3** | Implement Component 1 (Historical Trends & Regime Annotations) | `src/components/tab1_historical.py` | Pending |
| **Phase 4** | Implement Component 2 (12-Month Prospective Forecast & Scenarios) | `src/components/tab2_forecast.py` | Pending |
| **Phase 5** | Implement Component 3 (Getis-Ord Gi* Folium Hotspot Map) | `src/components/tab3_hotspots.py` | Pending |
| **Phase 6** | Implement Component 4 (Neighborhood Deep-Dive & STL Decomposition) | `src/components/tab4_decomposition.py` | Pending |
| **Phase 7** | Implement Component 5 (County Estimation Calculator & 4 Rules) | `src/components/tab5_calculator.py` | Pending |
| **Phase 8** | Implement Component 6 (Methodology, Footprint & Limitations) | `src/components/tab6_about.py` | Pending |
| **Phase 9** | Integrate master navigation, CSS styling, and executive header | `app.py`, `src/styles/custom.css` | Pending |
| **Phase 10**| Execute automated test suite & verify sub-5-second performance | `pytest tests/` | Pending |
| **Phase 11**| Deploy to Streamlit Community Cloud and author `Dashboard_DeploymentInfo` | `docs/Dashboard_DeploymentInfo.md` | Pending |

---

*This document establishes the definitive engineering specification for Task 9.1. All subsequent code implementation must adhere strictly to these architectural boundaries, mathematical models, and governance rules.*
