# Downtown San Diego Homeless Population Analysis

Public interest analytics, econometric modeling, and data engineering volunteer project with the **Data Science Alliance**, analyzing unsheltered homeless population trends across Downtown San Diego (2012–present) using monthly field count data from the Downtown San Diego Partnership (DSDP) and Point-in-Time (PIT) data from the Regional Task Force on Homelessness (RTFH).

---

## Quick Reference & Links

* **Master Memory & Technical Handoff:** [`PROJECT_MASTER_HANDOFF_ASSIGNMENTS_1_TO_9.md`](PROJECT_MASTER_HANDOFF_ASSIGNMENTS_1_TO_9.md)
* **Master Operational Runbook:** [`docs/ProjectHandoff_OperationalRunbook.md`](docs/ProjectHandoff_OperationalRunbook.md)
* **Master Context File:** [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md)
* **Task 9.1 Implementation Plan:** [`TASK_9_1_DASHBOARD_IMPLEMENTATION_PLAN.md`](TASK_9_1_DASHBOARD_IMPLEMENTATION_PLAN.md)
* **Dashboard Deployment Runbook:** [`docs/Dashboard_DeploymentInfo.md`](docs/Dashboard_DeploymentInfo.md)
* **Asana Project Workspace:** [Downtown San Diego Homeless Population Analysis](https://app.asana.com/1/1211227519522850/project/1218064298575500/list)
* **Google Drive Shared Deliverables:** [Shared Deliverables Folder](https://drive.google.com/drive/u/2/folders/1LUWFhKsbER-XSY8VJFVdt0cgVeuaQ6Ek)
* **DSDP Source Reports Archive:** [DSDP Unhoused Care Reports](https://downtownsandiego.org/clean-and-safe/unhoused-care/)

---

## Project Status & Milestones

* **Assignments 1–8:** **100% COMPLETE**
  * **Assignment 1 (Data Validation & Cleaning):** 45-cell audit, standardization, canonical adjustment rebuild (`MasterCounts_Adjusted_v2.csv`).
  * **Assignment 2 (Exploratory Data Analysis):** Statistical distributions, temporal profiles, neighborhood rankings, 10 publication charts.
  * **Assignment 3 (Block-Level Spatial Integration):** 382-block polygon grid (`Downtown_BlockGrid.geojson`), balanced 261-block panel, digitization coverage audit.
  * **Assignment 4 (Time Series Decomposition):** 9-series STL decomposition, Kruskal-Wallis non-parametric seasonality tests (8 of 9 non-seasonal).
  * **Assignment 5 (Geospatial Hotspots):** Queen contiguity weights, Getis-Ord $G_i^*$ clustering, 121-meter southward centroid displacement.
  * **Assignment 6 (Methodology Impact Assessment):** Multiplier break quantification (APR2017, MAY2018, COVID-19, July 2023 Camping Ordinance).
  * **Assignment 7 (Forecasting Pipelines):** 12-month prospective forecasting across 5 model architectures (Champion: XGBoost, RMSE: 169.58, 80%/95% PIs).
  * **Assignment 8 (County-Level Macro Estimation):** Policy Regime OLS model ($Y = 4,513.26 + 0.1859 \cdot X + 1,225.04 \cdot D_{\text{post}}$, $R^2 = 0.963$, Student's $t$ PIs).
* **Assignment 9: Interactive Dashboard & Strategic Synthesis:** **100% COMPLETE**
  * **Task 9.1 (Interactive Dashboard):** **100% COMPLETE & OPERATIONAL** (Streamlit multi-tab executive application, sub-2s load, 10/10 automated tests passing).
  * **Task 9.2 (Executive Summary & Technical Report):** **100% COMPLETE & AUDITED**
    * [`docs/ExecutiveSummary_NonTechnical.md`](docs/ExecutiveSummary_NonTechnical.md) — 3–4 page executive synthesis with KPI cards, 5 core findings, and 30-day/1-year/3-year policy roadmap.
    * [`docs/FullTechnicalReport.md`](docs/FullTechnicalReport.md) — 16–20 page technical monograph (10 chapters, full proofs, 16 tables, 13 display formulas, and governance charter).
  * **Task 9.3 (Strategic Recommendations & Slide Deck):** **100% COMPLETE & DELIVERED**
    * [`Assignment9_StrategicSynthesis.pptx`](Assignment9_StrategicSynthesis.pptx) — 14-slide executive presentation in Canva modern analytics theme with KPI cards, 3-epoch analysis, 2026 scenarios, and regional displacement matrix.
    * [`Assignment9_StrategicSynthesis.html`](Assignment9_StrategicSynthesis.html) — Standalone responsive browser presentation with embedded 300 DPI figures and keyboard navigation.
  * **Task 9.4 (Handoff Documentation & Protocols):** **100% COMPLETE & AUDITED**
    * [`PROJECT_MASTER_HANDOFF_ASSIGNMENTS_1_TO_9.md`](PROJECT_MASTER_HANDOFF_ASSIGNMENTS_1_TO_9.md) — Master single source of truth synthesizing Assignments 1–9.
    * [`docs/ProjectHandoff_OperationalRunbook.md`](docs/ProjectHandoff_OperationalRunbook.md) — 5 standardized operational runbooks (Annual PIT retraining, monthly DSDP ingestion, ML forecast updates, Streamlit maintenance, and Assignment 10 transition).
* **Assignment 10: Multi-Source Predictive System:** Queued on Roadmap.

---

## Interactive Executive Dashboard (Task 9.1)

The Streamlit dashboard synthesizes spatial, temporal, econometric, and forecasting pipelines into an executive-ready decision-support system.

### Dashboard Architecture & Features
1. **Historical Trends View (Tab 1):** Longitudinal time series (2017–2025), multiplier regime indicators, policy event markers (COVID-19, July 2023 Encampment Ban), component toggles (tents, vehicles, individuals).
2. **12-Month Prospective Forecast (Tab 2):** Forward projections for 2026 with shaded 80% & 95% uncertainty bands, model architecture selectors, and policy scenario stress-testing (-24% optimistic, +26% pessimistic).
3. **Hotspot Surveillance Map (Tab 3):** Folium vector choropleth map, Getis-Ord $G_i^*$ hotspot classifications (90%, 95%, 99%), top persistent blocks table, and centroid migration vector.
4. **Neighborhood Deep-Dive Panel (Tab 4):** 4-pane STL decomposition (Trend, Seasonality, Residuals) and Kruskal-Wallis significance results.
5. **County Estimation Calculator (Tab 5):** Policy Regime OLS macro calculator with Student's $t_{df=5}$ calibrated 95% prediction intervals ($\pm 2,050$), strictly enforcing **The 4 Public Communication Rules**.
6. **Methodology & Data Governance (Tab 6):** Data provenance, the 4 multiplier regimes, 2022 footprint expansion (+121 blocks), and root-cause analysis for missing data.

### Quick Start: Running the Dashboard Locally

```bash
# 1. Clone repository
git clone https://github.com/CapMorningStar/Downtown-Homeless-Analysis.git
cd Downtown-Homeless-Analysis

# 2. Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install production dependencies
pip install -r requirements.txt

# 4. Run automated test suite
pytest

# 5. Launch Streamlit dashboard
streamlit run app.py
```
Open **`http://localhost:8501`** in any modern web browser.

---

## Repository Structure

```text
├── .streamlit/               # Streamlit theme & server configuration
├── data/                     # Canonical datasets (MasterCounts_v2, BlockGrid, Forecasts, PairedCounts)
├── docs/                     # Technical documentation & deployment runbooks
├── figures/                  # 300 DPI publication plots and visual assets
├── src/                      # Modular dashboard architecture
│   ├── components/           # Streamlit tab renderers (tab1_historical to tab6_about)
│   ├── config.py             # Palette, thresholds, regime constants
│   ├── data_loader.py        # Cached data loaders (@st.cache_data)
│   ├── styles/custom.css     # Clean typography & card styling
│   └── utils.py              # Econometric equations & formatters
├── tests/                    # Automated pytest suite (10 unit tests)
├── app.py                    # Dashboard application entry point
├── pytest.ini                # Pytest configuration
├── requirements.txt          # Python production dependencies
├── runtime.txt               # Streamlit Cloud runtime pin (python-3.11)
├── PROJECT_CONTEXT.md        # Comprehensive multi-assignment memory file
├── PROJECT_MASTER_HANDOFF_ASSIGNMENTS_1_TO_8.md # Complete technical handoff log
└── TASK_9_1_DASHBOARD_IMPLEMENTATION_PLAN.md    # Task 9.1 technical plan
```

---

## Author & Citation
* **Lead Analyst:** Kyaw Soe Lwin ([`kslwin.2000@gmail.com`](mailto:kslwin.2000@gmail.com) / [`kylwin@ucsd.edu`](mailto:kylwin@ucsd.edu))
* **Organization:** Data Science Alliance (San Diego, CA)
* **Project Lead:** Adir Mancebo Jr. ([`adir@datasciencealliance.org`](mailto:adir@datasciencealliance.org))
