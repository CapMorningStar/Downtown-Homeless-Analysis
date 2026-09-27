# Dashboard Deployment & Operational Information (Task 9.1)
## Downtown San Diego Homeless Population Analysis

**Project Title:** Downtown San Diego Homeless Population Analysis  
**Organization:** Data Science Alliance (Public Interest Data Science)  
**Lead Contributor:** Kyaw Soe Lwin (`kylwin@ucsd.edu` / `kslwin.2000@gmail.com`)  
**Project Lead:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)  
**Deliverable Document:** `Dashboard_DeploymentInfo`  
**Operational Status:** Production Ready & Live Locally (`http://localhost:8501`)  
**Deployment Target:** Streamlit Community Cloud (`https://downtown-sd-homelessness.streamlit.app`)  
**Repository Branch:** `main`  
**Date:** September 2026  

---

## 1. Executive Summary

As part of **Assignment 9: Interactive Dashboard & Strategic Synthesis**, this deliverable establishes the interactive production dashboard synthesizing the econometric, spatial, time-series, and macro-estimation models developed across **Assignments 1 through 8**.

The dashboard bridges the gap between deep empirical research and executive decision-making. Municipal leadership, service providers, and community researchers can explore multi-year trends, 12-month prospective forecasts with policy scenario envelopes, block-level Getis-Ord $G_i^*$ spatial hotspots, localized neighborhood STL decompositions, and an interactive countywide estimation calculator governed by strict public communication rules.

---

## 2. Access Links & System Architecture

* **Local Development Access:** `http://localhost:8501`
* **Public Cloud Deployment URL:** `https://downtown-sd-homelessness.streamlit.app` (Streamlit Community Cloud)
* **GitHub Repository:** `https://github.com/CapMorningStar/Downtown-Homeless-Analysis`
* **Shared Deliverables Drive:** `Shared with me > Downtown Homelessness > Deliverables > Assignment 9 - Interactive Dashboard & Strategic Synthesis`
* **Asana Task Reference:** [Task 9.1: Design and build the interactive dashboard](https://app.asana.com/1/1211227519522850/project/1218064298575500/task/1218105502019244)

```text
Downtown-Homeless-Analysis/
├── app.py                             # Main Streamlit application entry point & router
├── requirements.txt                   # Production dependencies (optimized for cloud runtime)
├── runtime.txt                        # Python 3.11 pinning
├── README.md                          # Public repo overview & architecture
│
├── .streamlit/
│   └── config.toml                    # Executive Slate theme palette, layout width, port 8501
│
├── src/
│   ├── config.py                      # Global constants, colors, date limits, regime markers
│   ├── data_loader.py                 # Cached ingestion (@st.cache_data), schema validation
│   ├── utils.py                       # KPI formatters, Student's t prediction interval math
│   │
│   ├── components/                    # Modular page renderers (Components 1 through 6)
│   │   ├── header.py                  # Executive branding, high-level KPIs, status indicator
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
├── data/                              # Canonical analytical datasets (Assignments 1-8)
│   ├── MasterCounts_Adjusted_v2.csv          # Canonical monthly counts (2,814 rows)
│   ├── Downtown_BlockGrid.geojson            # 382 Downtown block polygons
│   ├── Forecasts_12Month.csv                 # 2026 prospective forecasts with PIs & scenarios
│   ├── SeasonalIndices.csv                   # Monthly seasonal indices, CIs, p-values
│   ├── Downtown_County_PairedCounts.csv      # 8-year paired DSDP/RTFH dataset
│   └── Hotspot_Persistence_Ranking.csv       # 261-block longitudinal persistence ranking
│
└── tests/
    ├── test_data_loader.py            # Automated schema checks & row-count validation
    ├── test_calculator.py             # Validation of Policy Regime OLS & Student's t PIs
    └── test_forecast_logic.py         # Scenario math (-24%, +26%) & PI monotonic sanity
```

---

## 3. Interactive Component Guide

### Component 1: Historical Trends View (`tab1_historical.py`)
* **Longitudinal Trajectory (2017–2025):** Interactive Plotly time-series spanning all 108 monthly observations.
* **Neighborhood Footprints:** Toggle between `Overall - reported footprint`, `Overall - fixed core six`, and all 7 individual neighborhoods.
* **Methodology Markers:** Dynamic vertical annotations marking APR2017, MAY2018, COVID-19 emergency, and the July 2023 Unsafe Camping Ordinance.
* **Component Breakdown:** Option to inspect individual, tent, and vehicle counts for specific neighborhoods.
* **Shaded Macro Epochs:** Highlights COVID-19 emergency shelter housing and post-camping ordinance enforcement windows.

### Component 2: 12-Month Prospective Forecast View (`tab2_forecast.py`)
* **2026 Projections (2026-01 to 2026-12):** Features Assignment 7 champion models:
  * **XGBoost Champion** (12-Month CV MAPE: **39.34%**, hold-out test MAPE: **38.48%**).
  * **Holt-Winters Parametric** (CV MAPE: **39.57%**, variance anchor).
  * SARIMA, Prophet, and Naive seasonal baselines ($t-12$).
* **Uncertainty Fans:** Shaded 80% and 95% prediction intervals expanding monotonically with forecast horizon.
* **Policy Scenarios:** Status Quo (baseline), Optimistic ($-24\%$ at Month 12), Pessimistic ($+26\%$ at Month 12), and interactive custom $\pm 50\%$ slider.
* **Validation Expander:** Collapsible 5-fold cross-validation performance comparison table.

### Component 3: Geospatial Hotspot Surveillance Map (`tab3_hotspots.py`)
* **Mapping Engine:** Folium with CartoDB Positron basemap and interactive block polygon tooltips.
* **Date Selector:** Seamless navigation across the 12 digitized count dates (2018–2025).
* **Footprint Toggle:** Balanced Longitudinal Panel (261 blocks) vs. Expanded Footprint (382 blocks for 2022+).
* **Getis-Ord $G_i^*$ Symbology:** Highlights persistent clusters at 99%, 95%, and 90% confidence.
* **Analytical Modules:**
  * **Top 10 Persistent Hotspots Ranking Table** (led by `16TH_ST_IMPERIAL_AV`, significant on 9 of 12 dates).
  * **121-Meter Southward Centroid Shift** callout card documenting cluster migration toward Commercial St / Imperial Ave.
  * Nearest transit and social service proximity indicators.

### Component 4: Neighborhood Deep-Dive Panel (`tab4_decomposition.py`)
* **STL Time-Series Decomposition:** 4 synchronized panes displaying Observed, Trend, Seasonal, and Residual components.
* **Statistical Seasonality Audit:** Kruskal-Wallis non-parametric test outputs ($H$-statistic and $p$-value) proving that **8 of 9 series exhibit no statistically significant seasonality** (East Village summer bump is non-significant; Marina is the sole borderline series).
* **Cross-Neighborhood Comparison:** Summary metrics and distribution boxplots illustrating extreme right-skew.

### Component 5: County-Level Estimation Calculator & Governance Charter (`tab5_calculator.py`)
* **Econometric Model:** Policy Regime OLS model ($Y = 4,513.26 + 0.1859 \cdot X + 1,225.04 \cdot D_{\text{post}}$) from Assignment 8.
* **Interactive Inputs:** Downtown count parameter input $X$, quick preset buttons (Dec 2025 = 985, Jan 2026 Forecast = 886, Peak Crisis = 2,103, COVID Low = 689), and enforcement regime toggle ($D_{\text{post}} \in \{0, 1\}$).
* **The 4 Public Communication Rules (Strictly Enforced in UI):**
  1. *Rule 1 (Precision Prohibition):* Raw single-point precision (e.g. `5,921`) is hidden.
  2. *Rule 2 (Mandatory Rounding):* Outputs automatically rounded to nearest 100 (`5,900`).
  3. *Rule 3 (Mandatory Calibrated Range):* Mandatory Student's $t$ 95% range: `5,900 [3,900 to 8,000]`.
  4. *Rule 4 (Policy Context Disclosure):* Mandatory disclosure of active Camping Ordinance regime.
* **Statutory Governance Banner:** Explicit legal/governance warning prohibiting official HUD or statutory budget formula use.
* **Ratio Fragility Context:** Proof of ratio fracturing via ANOVA ($F=66.51, p=0.0002$).

### Component 6: Methodology, Data Governance & Footprint (`tab6_about.py`)
* **Data Sources:** In-depth documentation of DSDP monthly morning counts vs. RTFH annual Point-in-Time censuses.
* **The 4 Multiplier Regimes:** Comprehensive audit of PRE2017, APR2017, MAY2018, and POST2020 regimes, and the Constant-Methodology Hybrid Series.
* **2022 Footprint Expansion:** Detailed warning explaining that adding 121 blocks in Golden Hill, Barrio Logan, and Sherman Heights drove $4\%$ to $33\%$ of post-2021 count increases.
* **Data Quality Audit Log:** Root-cause accounting of 134 null values and confirmation of the January 2017 empirical series start date.

---

## 4. Performance Benchmarks & Quality Assurance

* **Load Time:** Sub-2.0 seconds initial boot; $< 200$ ms reactive tab transitions (satisfying the $< 5$-second mandate).
* **In-Memory Caching:** `@st.cache_data` applied across all data loading functions.
* **Automated Test Results:**
  * `pytest tests/`: **10 passed in 0.32 seconds** (100% pass rate).
  * Validates data schemas, econometric calculator math, Student's $t$ prediction intervals, and scenario bounds.

---

## 5. Deployment Runbook (Streamlit Community Cloud)

1. **Commit and Push to GitHub:**
   ```bash
   git add .
   git commit -m "feat(dashboard): Task 9.1 interactive executive dashboard"
   git push origin main
   ```
2. **Configure Streamlit Community Cloud:**
   * Log into [share.streamlit.io](https://share.streamlit.io/) with `@CapMorningStar`.
   * Click **New app** $\rightarrow$ select `CapMorningStar/Downtown-Homeless-Analysis`.
   * Set Main file path: `app.py`.
   * Advanced Settings: Python version `3.11`.
   * Click **Deploy!**
3. **Google Drive Sync:**
   * Convert this document to a Google Doc titled `Dashboard_DeploymentInfo`.
   * Place in `Deliverables > Assignment 9 - Interactive Dashboard & Strategic Synthesis`.
4. **Asana Task Update:**
   * Mark Task 9.1 as Complete on Asana with deployment links and test summary.
