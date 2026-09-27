# Task 9.2: Master Architectural Blueprint
## Synthesis of Executive Summary & Full Technical Report
### Downtown San Diego Homeless Population Analysis

**Document Status:** Production Master Specification  
**Project:** Downtown San Diego Homeless Population Analysis (Data Science Alliance)  
**Lead Data Science Technical Writer & Synthesizer:** Kyaw Soe Lwin (`kylwin@ucsd.edu` / `kslwin.2000@gmail.com`)  
**Project Lead / Product Owner:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)  
**Target Deliverables:**
1. **Deliverable A:** `ExecutiveSummary_NonTechnical.md` (3–4 pages, non-technical executive reader, high accessibility, visual callouts, strategic policy actions)
2. **Deliverable B:** `FullTechnicalReport.md` (15–20 pages, rigorous data science report covering data engineering, econometrics, spatial statistics, machine learning forecasting, macro estimation, limitations, and governance)

---

## Executive Overview & Strategic Document Architecture

This blueprint establishes the complete editorial, structural, mathematical, and cartographic architecture for **Task 9.2: Write Executive Summary and Full Technical Report**. 

Task 9.2 represents the definitive written synthesis of the entire **Downtown San Diego Homeless Population Analysis** research lifecycle. Across Assignments 1 through 8 and the deployment of the Task 9.1 interactive dashboard, the project has generated rigorous empirical insights into the longitudinal dynamics of unsheltered homelessness in San Diego. 

To bridge the gap between deep technical rigor and civic policy execution, Task 9.2 produces two tightly coordinated but distinct documents designed for complementary audiences:

```
+----------------------------------------------------------------------------------------------------+
|                                    TASK 9.2 DELIVERABLE SYSTEM                                     |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|    DELIVERABLE A: ExecutiveSummary_NonTechnical.md             DELIVERABLE B: FullTechnicalReport.md|
|    -----------------------------------------------             ------------------------------------|
|    • Target Audience: Mayor, City Council, County              • Target Audience: Lead Data        |
|      Supervisors, Agency Directors, Civic Leaders                Scientists, Econometricians, Spatial|
|    • Length: 3–4 pages (~1,600 – 2,000 words)                    Researchers, Policy Analysts      |
|    • Tone: Crisp, executive, policy-actionable,                • Length: 15–20 pages (8,500-11,000w)|
|      plain-language translation of complex math                 • Tone: Peer-reviewed econometric   |
|    • Visuals: High-impact KPI cards, callout                     and data science publication      |
|      boxes, infographic timelines, priority tables             • Content: Full equations, proofs,  |
|    • Primary Focus: Key findings, operational                    CV matrices, spatial weights,      |
|      realities, 12-month projections, policy                     LOOCV tables, limitations charter |
|      recommendations (30-day, 1-yr, 3-yr horizons)             • Coverage: 100% of Assignments 1-8 |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

---

## Part 1: Deliverable A Blueprint (`ExecutiveSummary_NonTechnical.md`)

### 1.1 Specification & Design Principles
* **Target Audience:** Civic Executives (Mayor, City Councilmembers, County Board of Supervisors, Regional Task Force on Homelessness [RTFH] Board, Downtown San Diego Partnership [DSDP] Leadership, Philanthropic Trustees).
* **Page Budget & Word Count:** 3.5 to 4.0 standard single-spaced pages (~1,600 – 2,000 words).
* **Visual Language:** High accessibility, Executive Slate / Navy typography, high-contrast KPI metric cards, warning and insight callout banners, clean Markdown tables, and direct policy roadmap matrices.
* **Core Philosophy:** *Zero mathematical obfuscation; 100% empirical precision.* Never present numbers without actionable operational context. Translate statistical concepts (e.g., non-significant seasonality, spatial clustering, regime shifts) into direct resource-allocation decisions.

---

### 1.2 Section-by-Section Outline & Budget

#### Section 1: Executive Framing & Key Findings at a Glance
* **Budget:** 0.75 pages (~400 words)
* **Subsections:**
  * `1.1 Mission & Evidence Base`: The partnership between the Data Science Alliance, DSDP, and RTFH analyzing 9 years (2017–2025) of monthly street counts and annual regional censuses.
  * `1.2 The Five Core Takeaways`:
    1. *The Three Trajectory Epochs:* Contraction (2017–2020), Crisis Rebound & Peak (2021–2023), Enforcement Pullback (2024–2025).
    2. *Seasonality is a Myth:* Monthly weather swings explain virtually none of the variation; macro policies and housing market shocks drive 95%+ of count swings.
    3. *Extreme Spatial Concentration:* Over 50% of unsheltered individuals reside in South East Village; the core hotspot has migrated 121 meters south.
    4. *Downtown Contraction vs. Regional Spillover:* The July 2023 Unsafe Camping Ordinance reduced visible downtown counts by 56%, but countywide unsheltered numbers reached an all-time record of 6,110 (spatial dispersion, not regional eradication).
    5. *2026 Prospective Outlook:* Baseline projections anticipate a stable downtown count (~850–920), with policy scenarios ranging from -24% (accelerated shelter) to +26% (capacity exhaustion).
* **Embedded Visual Elements:**
  * **Executive KPI Header Grid (4 Metric Cards):**
    ```text
    [ 2,103 ] Peak May 2023 Monthly Count | [ 851 ] Jan 2025 Monthly Count (-59.5% from peak)
    [ 54.8% ] East Village Volume Concentration | [ 121m ] Southward Hotspot Migration Shift
    ```
  * **Alert Banner (Statutory Scope Warning):** Clear notice regarding the difference between monthly operational downtown counts and annual HUD PIT censuses.

#### Section 2: Historical Dynamics & The Myth of Seasonality
* **Budget:** 0.75 pages (~400 words)
* **Subsections:**
  * `2.1 The Three Distinct Historical Epochs`: Detailed breakdown of the 2017–2020 pre-pandemic decline (-38%), the 2021–2023 surge (+57.6% in 2022 alone; peak 2,103), and the 2024–2025 post-ordinance reduction (-43.5%).
  * `2.2 Debunking the Seasonal Weather Narrative`: Explaining why municipal planning based on "summer surges" or "winter lulls" is empirically flawed. Econometric tests prove counts do not follow reliable calendar cycles.
  * `2.3 Accounting for Counting Changes`: Plain-language explanation of multiplier regimes (individual, tent, and vehicle adjustment factors) and the 2022 boundary expansion (adding 121 blocks in Golden Hill, Barrio Logan, and Sherman Heights), showing that 4% to 33% of post-2021 reported increases were simply due to drawing a larger map.
* **Embedded Data Table:**
  * *Table A.1: Historical Epochs and Annual Growth Rates (2017–2025)* (Columns: Year, Average Monthly Count, YoY % Change, Dominant Macro & Policy Drivers).
* **Embedded Figure:**
  * *Figure A.1: The 9-Year Trajectory of Downtown Homelessness (2017–2025)* (Referencing `slide_assets/chart1_clean_hd.png`).

#### Section 3: Where Homelessness Concentrates (Geospatial Realities)
* **Budget:** 0.75 pages (~400 words)
* **Subsections:**
  * `3.1 The East Village Epicenter`: East Village accounts for over half of all downtown unsheltered individuals (historical monthly mean 552.8), with concentration heavily skewed toward North East and South East sub-areas.
  * `3.2 Persistent Hotspots vs. Transient Encampments`: Identification of the top persistent hotspot block—`16th St & Imperial Ave`—which remained an active statistically significant hotspot in 9 out of 12 analyzed dates.
  * `3.3 The 121-Meter Southward Migration`: Analysis of why the cluster center moved south toward Commercial Street and Imperial Avenue between 2018–2020 and 2022–2025, driven by transit adjacency (12th & Imperial Transit Center), shelter infrastructure (Father Joe's Villages), and public right-of-way enforcement patterns.
* **Embedded Data Table:**
  * *Table A.2: Top 5 Persistent Hotspot Blocks in Downtown San Diego* (Columns: Rank, Block Location, Neighborhood, Hotspot Frequency, Key Environmental Features).
* **Embedded Visual Element:**
  * *Visual Callout Box: The Built Environment Magnet* (Describing the spatial interaction between social service intake points, transit hubs, and right-of-way boundaries).

#### Section 4: 2026 Forecast Outlook & Scenario Planning
* **Budget:** 0.75 pages (~400 words)
* **Subsections:**
  * `4.1 Prospective Baseline Forecast for 2026`: Introduction of the machine learning forecast (XGBoost champion model), projecting an annual monthly average of ~880–915 individuals under status quo enforcement and shelter capacity.
  * `4.2 The Three Strategic Policy Scenarios`:
    * *Optimistic Scenario (-24% at Month 12):* Accelerated shelter bed expansion, non-congregate safe sleeping sites, and targeted rapid-rehousing reducing counts to ~670.
    * *Baseline Scenario (Status Quo):* Continued ordinance enforcement with current shelter constraints maintaining counts between 850 and 920.
    * *Pessimistic Scenario (+26% at Month 12):* Shelter capacity stagnation, economic headwinds, and exhaustion of diversion resources pushing counts back above 1,110.
  * `4.3 Understanding the Margin of Error`: Plain-language explanation of 80% and 95% prediction intervals—why point forecasts must always be coupled with uncertainty envelopes.
* **Embedded Data Table:**
  * *Table A.3: 2026 Quarterly Forecast Projections Across Three Policy Scenarios* (Columns: Horizon, Baseline Point Projection, 95% Confidence Band, Optimistic [-24%], Pessimistic [+26%]).
* **Embedded Figure:**
  * *Figure A.2: 12-Month Prospective Projections and Policy Scenarios for 2026*.

#### Section 5: Regional Implications & Strategic Action Roadmap
* **Budget:** 1.0 page (~500 words)
* **Subsections:**
  * `5.1 The Displacement Reality (Downtown vs. Countywide)`: Downtown's share of county unsheltered homelessness dropped from 37.5% in 2023 to 14.9% in 2025. Unsafe Camping Ordinance enforcement dispersed unhoused populations into riverbeds, freeway borders, and outlying cities rather than resolving homelessness regionally.
  * `5.2 The 4 Mandatory Public Communication Rules`: Essential guidance for public officials:
    1. Never report false single-point precision (avoid "5,921").
    2. Always round macro estimates to the nearest 100 ("5,900").
    3. Always publish the calibrated 95% range ("5,900 [3,900 to 8,000]").
    4. Always disclose the post-ordinance enforcement baseline.
  * `5.3 Strategic Action Roadmap (30-Day, 1-Year, 3-Year)`:
    * *Immediate Actions (30–90 Days):* Focus mobile hygiene, outreach, and safety resources directly on the top 10 South East Village blocks; deploy the Task 9.1 Dashboard for monthly situational monitoring.
    * *Medium-Term Strategy (6–12 Months):* Expand safe sleeping and low-barrier shelter capacity to unlock the Optimistic (-24%) forecast trajectory; coordinate cross-jurisdictional outreach along regional transit corridors.
    * *Long-Term Systems Transformation (1–3 Years):* Establish regional bed-tracking integration (HMIS 2.0); shift from perimeter sweeps to permanent supportive housing exits.
* **Embedded Policy Matrix:**
  * *Table A.4: Municipal Policy & Operational Action Roadmap* (Priority, Timeframe, Operational Action, Responsible Agencies, Target Metric).

---

## Part 2: Deliverable B Blueprint (`FullTechnicalReport.md`)

### 2.1 Specification & Design Principles
* **Target Audience:** Quantitative Data Scientists, Econometricians, Spatial Statisticians, Municipal Budget Directors, University Researchers, Evaluation Officers.
* **Page Budget & Word Count:** 16.0 to 20.0 standard single-spaced pages (~8,500 – 11,000 words).
* **Technical Depth:** Exhaustive methodological documentation, mathematical derivations, formal econometric formulas, cross-validation tables, spatial weight matrices, goodness-of-fit metrics, and full reproducibility metadata.
* **Compliance Standards:** Fully compliant with HUD Point-in-Time counting guidelines, ASA statistical reporting guidelines, and the Data Science Alliance reproducibility charter.

---

### 2.2 Complete Section-by-Section Technical Outline

```
+----------------------------------------------------------------------------------------------------+
|                               FULL TECHNICAL REPORT (10 SECTIONS)                                  |
+----------------------------------------------------------------------------------------------------+
| Sec 1: Project Framing, Scope & Governance Architecture                       [Budget: 1.0 p / 550w]|
| Sec 2: Data Engineering, Harmonization & Quality Audits                       [Budget: 2.0 p / 1100w]
| Sec 3: Exploratory Data Analysis & Empirical Longitudinal Trajectory          [Budget: 1.5 p / 850w]|
| Sec 4: Time Series Econometrics & Decomposition Analytics                     [Budget: 2.0 p / 1100w]
| Sec 5: Spatial Panel Integration & Boundary Footprint Dynamics                [Budget: 1.5 p / 850w]|
| Sec 6: Geospatial Hotspot Surveillance & Spatial Econometrics                 [Budget: 2.5 p / 1400w]
| Sec 7: Multiplier Policy Evaluation & Constant-Methodology Counterfactuals    [Budget: 1.5 p / 850w]|
| Sec 8: Predictive Modeling & 12-Month Prospective Machine Learning Pipeline   [Budget: 2.5 p / 1400w]
| Sec 9: Macro-Econometric County-Level Estimation System                       [Budget: 2.5 p / 1400w]
| Sec 10: Methodological Boundaries, Governance Charter & Production Runbook    [Budget: 1.5 p / 850w]|
+----------------------------------------------------------------------------------------------------+
```

---

#### Section 1: Project Framing, Administrative Context & Scope
* **Page Budget:** 1.0 page (~550 words)
* **Subsections:**
  * `1.1 Institutional Context & Project Charter`: Partnership between Data Science Alliance, DSDP, and RTFH. Overview of project lifecycle from initial data audit through Assignments 1–8 and Task 9.1 interactive deployment.
  * `1.2 Study Area Delineation & Geographical Entities`: Definition of Downtown San Diego's 7 core neighborhoods (City Center, Columbia, Cortez, East Village, Gaslamp, Marina, Outside Perimeter) and the 4 East Village sub-quadrants (North East, North West, South East, South West).
  * `1.3 Scope Correction & Temporal Window`: Resolution of historical scope—empirical count data begins January 2017 (`2017-01-01`), spanning 108 monthly reporting periods through December 2025.
  * `1.4 Technical Naming & Alias Crosswalk`: Formal resolution of the `"Core"` neighborhood label as an empirical alias for `City Center` (used 2017–2018, retired after March 2019; Gaslamp co-exists as an independent administrative unit).

#### Section 2: Data Engineering, Ingestion Architecture & Quality Audits
* **Page Budget:** 2.0 pages (~1,100 words)
* **Subsections:**
  * `2.1 Multi-Source Ingestion Pipeline`: Architecture for processing DSDP monthly Clean & Safe PDF counts and RTFH annual Continuum of Care PIT tables.
  * `2.2 The 4 Historical Multiplier Regimes`:
    $$\text{Adjusted Total} = 1.0 \times \text{Individuals} + 1.75 \times \text{Tents} + \mu_{\text{veh}} \times \text{Vehicles}$$
    * *PRE2017 (Jan–Mar 2017):* Direct unadjusted count ($1.0 \times \text{all}$).
    * *APR2017 (Apr 2017–Apr 2018):* $\mu_{\text{veh}} = 1.66$, $\mu_{\text{tent}} = 1.75$.
    * *MAY2018 (May 2018–Dec 2019):* $\mu_{\text{veh}} = 2.03$, $\mu_{\text{tent}} = 1.75$.
    * *POST2020 (Jan 2020–present):* RTFH HUD PIT eliminated multipliers ($1.0\times$ all); DSDP retained multipliers ($\mu_{\text{veh}} = 2.03$) for longitudinal tracking.
  * `2.3 Stratified Audit & Empirical Error Discoveries (Task 1.1)`:
    * 45-cell random stratified audit across 32 source PDFs (97.56% fidelity, 2.44% error rate).
    * *The 2019 East Village Duplication Bug:* Root cause analysis of how all 48 sub-area rows in 2019 were copy-paste duplicates of 2020 data, causing discrepancies up to -206 individuals.
    * *The February 2018 PDF Addition Error:* Verification of a +30 arithmetic error ($504$ sub-area sum vs. $474$ published total) originating within DSDP's own published PDF tables.
  * `2.4 Reconstruction of Canonical Dataset (Task 1.3)`: Rebuilding `MasterCounts_Adjusted_v2.csv` (2,814 rows) by re-summing adjusted components for all 544 area-months with components, resolving the legacy flaw where adjusted totals equaled raw counts.
  * `2.5 Schema Normalization, Long-Format Filtering & Null Accounting`:
    * Strict requirement: $\text{component} == \text{'total'} \land \text{area\_type} == \text{'neighborhood'}$ to prevent double-counting.
    * Complete root-cause accounting for all 134 null values: 116 in 2025 (reporting lag across Jul, Aug, Oct, Nov) + 18 in Nov 2018 (omission of component breakdown in published report).
* **Formulas to Embed:** Multiplier calculation formula.
* **Tables to Embed:**
  * *Table 2.1: Chronology of DSDP Multiplier Regimes and Cross-Agency Harmonization*.
  * *Table 2.2: Comprehensive Audit Discrepancy Log and Resolution Action*.

#### Section 3: Exploratory Data Analysis & Empirical Longitudinal Trajectory
* **Page Budget:** 1.5 pages (~850 words)
* **Subsections:**
  * `3.1 Multi-Year Descriptive Statistics`: Overall monthly neighborhood mean 156.78 (median 58.88, std 197.38, max 921.05). Heavy right-skew driven by East Village.
  * `3.2 The Three Macro Longitudinal Epochs`:
    1. *Epoch 1: Pre-Pandemic Contraction (2017–2020):* Annual mean fell from 176.31 to 109.02 (-38.2% cumulative decline; YoY: -18.98% in 2018, -4.94% in 2019, -19.71% in 2020).
    2. *Epoch 2: Post-COVID Surge & Crisis Peak (2021–2023):* Rapid expansion (+25.85% in 2021, +57.63% in 2022) to an all-time annual mean of 223.98 in 2023. Monthly series peak of 2,103 individuals in May 2023.
    3. *Epoch 3: Enforcement Contraction & Stabilization (2024–2025):* Sharp -43.52% contraction in 2024 (mean 126.50), stabilizing in 2025 (-2.94% to 122.78).
  * `3.3 Neighborhood Volume vs. Growth Disconnect`:
    * Volume ranking: East Village (552.77) ≫ Outside Perimeter (217.57) > City Center (171.81) > Cortez (59.52) > Gaslamp (48.43) > Columbia (44.49) > Marina (30.94).
    * Growth rate ranking (2019+): Outside Perimeter (+26.90%/yr), Cortez (+11.96%/yr), City Center (+3.94%/yr), East Village (+1.64%/yr), Marina (-12.76%/yr), Columbia (-4.28%/yr).
  * `3.4 COVID-19 Pandemic Shock & Shelter Interventions`: Analysis of the March 2020 series trough (529 individuals), Convention Center Operation Shelter to Home demobilization, and subsequent surge.
* **Tables to Embed:**
  * *Table 3.1: Longitudinal Descriptive Statistics and Compound Annual Growth by Neighborhood (2017–2025)*.
* **Figures to Embed:**
  * *Figure 3.1: Longitudinal Trajectory of Unsheltered Homelessness in Downtown San Diego (2017–2025)* (`slide_assets/chart1_clean_hd.png`).
  * *Figure 3.2: Annual Percentage Growth Rates Across Neighborhoods (2019–2025)* (`slide_assets/chart7_yoy_hd.png`).

#### Section 4: Time Series Econometrics & Decomposition Analytics
* **Page Budget:** 2.0 pages (~1,100 words)
* **Subsections:**
  * `4.1 Classical Additive & Robust STL Decomposition Framework`:
    $$Y_t = T_t + S_t + R_t$$
    Application of 12-month period robust LOESS-based STL decomposition across all 9 series. Finding that aggregate seasonal strength is near zero ($S_{\text{var}} / (S_{\text{var}} + R_{\text{var}}) \approx 0.04$).
  * `4.2 Rigorous Seasonal Testing & The Kruskal-Wallis Non-Parametric Proof`:
    $$H = \frac{12}{N(N+1)} \sum_{j=1}^k \frac{R_j^2}{n_j} - 3(N+1)$$
    De-trending series via robust STL ($D_t = Y_t - T_t$). Non-parametric Kruskal-Wallis tests prove that **8 of 9 series exhibit NO statistically significant seasonality** ($p > 0.05$).
    * Headline series: $H = 3.00, p = 0.99$.
    * East Village: $H = 13.86, p = 0.24$ (proving the raw July–August bump is purely trend-driven noise).
    * Only Marina demonstrated borderline significance ($H = 20.15, p = 0.043$; ANOVA disagreed at $p = 0.146$).
  * `4.3 Structural Break Analytics (Chow F-Tests & OLS CUSUM)`:
    $$y_t = \beta_0 + \beta_1 t + \beta_2 D_t + \beta_3 (D_t \cdot t) + \epsilon_t$$
    * *April 2017:* Exploratory only (3 pre-break data points; robust inference withheld).
    * *May 2018:* Confirmed structural break surviving Benjamini-Hochberg FDR ($q < 0.05$) and HAC(12) robust standard errors.
    * *March 2020 (COVID-19):* Decisive structural break across 7 of 8 series ($p < 0.001$).
  * `4.4 Stationarity Screening & Autocorrelation Structure (ADF & KPSS)`:
    Paired consensus testing (ADF $p < 0.05 \land$ KPSS $p > 0.05$). All level series non-stationary. First differencing ($\Delta Y_t$) achieved consensus stationarity for 8 series; $\log(1 + Y_t)$ transformation achieved stationarity for Outside Perimeter. Ljung-Box diagnostic tests.
* **Formulas to Embed:** STL decomposition, Kruskal-Wallis $H$-statistic, Chow dummy-variable regression model.
* **Tables to Embed:**
  * *Table 4.1: Robust STL Decomposition and Kruskal-Wallis Seasonality Test Suite*.
  * *Table 4.2: Econometric Structural Break Evaluation Matrix (Chow F, CUSUM, HAC P-values)*.
  * *Table 4.3: Unit Root and Stationarity Consensus Diagnostics (ADF, KPSS, Differencing Orders)*.
* **Figures to Embed:**
  * *Figure 4.1: Calendar-Month Seasonality & Monthly Percentage Deviations* (`slide_assets/chart2_clean_hd.png`).

#### Section 5: Spatial Panel Integration & Boundary Footprint Dynamics
* **Page Budget:** 1.5 pages (~850 words)
* **Subsections:**
  * `5.1 Digitized Block Grid & Vector Geometry Validation`: Ingestion of `Downtown_BlockGrid.geojson` containing 382 polygon features in CRS84. Validation of 380/382 centroids strictly contained within polygons; technical documentation of the 2 non-convex freeway interchange exceptions (`22ND_ST_BROADWAY`, `22ND_ST_SR-94_EB_ON_RA`).
  * `5.2 The 2022 Boundary Expansion & Spatial Panel Fracture`:
    Discovery that DSDP block-level collection expanded from 261 blocks (2018–2021) to 382 blocks (2022–2025) by incorporating 121 blocks in Golden Hill (52), Barrio Logan (35), and Sherman Heights (34) under "Outside Perimeter".
  * `5.3 Empirical Quantification of the Footprint Effect`:
    $$\text{Footprint Wedge}_t = \frac{\sum_{i=1}^{382} Y_{it} - \sum_{i=1}^{261} Y_{it}}{\sum_{i=1}^{382} Y_{it}}$$
    Demonstrating that **4.0% to 32.8% of post-2021 total reported counts were driven strictly by boundary expansion** (e.g., +32.8% in Jan 2023). Proof that underlying rise remained real (+71% on fixed 261 blocks in 2022).
  * `5.4 The Balanced 261-Block Panel Specification`: Construction of `BlockPanel_Balanced_261.csv` (3,132 rows = 261 blocks $\times$ 12 count dates) to guarantee longitudinal comparability.
  * `5.5 Source Map Coverage Audit & 78-Month Digitization Gap`: Identification that out of 90 months with available DSDP map packets, only 12 have been digitized (78 months remain undigitized). Audit of the March 2022 anomaly (handwritten date inconsistencies).
* **Formulas to Embed:** Footprint expansion wedge formula.
* **Tables to Embed:**
  * *Table 5.1: Boundary Expansion Footprint Wedge Quantification by Count Date (2022–2025)*.
  * *Table 5.2: Spatial Data Coverage, Digitization Inventory, and Missing Map Audit*.

#### Section 6: Geospatial Hotspot Surveillance & Spatial Econometrics
* **Page Budget:** 2.5 pages (~1,400 words)
* **Subsections:**
  * `6.1 Spatial Contiguity Weights & Global Moran's I`:
    $$I = \frac{N}{\sum_{i} \sum_{j} w_{ij}} \frac{\sum_{i=1}^N \sum_{j=1}^N w_{ij}(x_i - \bar{x})(x_j - \bar{x})}{\sum_{i=1}^N (x_i - \bar{x})^2}$$
    Construction of Queen contiguity spatial weight matrix (2,642 directed neighbor links). Permutation testing (9,999 iterations) confirming statistically significant positive spatial clustering across all 12 dates ($I \in [0.063, 0.239]$, all $p < 0.05$).
  * `6.2 Local Getis-Ord Gi* Permutation Engine`:
    $$G_i^* = \frac{\sum_{j=1}^N w_{ij} x_j - \bar{X} \sum_{j=1}^N w_{ij}}{S \sqrt{\frac{N \sum_{j=1}^N w_{ij}^2 - (\sum_{j=1}^N w_{ij})^2}{N - 1}}}$$
    Classification into 99% ($z \ge 2.576$), 95% ($z \ge 1.960$), and 90% ($z \ge 1.645$) confidence tiers. Absence of statistically significant coldspots.
  * `6.3 261-Block Longitudinal Persistence Ranking`:
    Ranking blocks by frequency of hotspot classification out of 12 dates. The undisputed epicenter: `16TH_ST_IMPERIAL_AV` (hotspot on 9/12 dates). Finding that all top 10 persistent blocks are tightly clustered in South East Village.
  * `6.4 Built Environment & OpenStreetMap Infrastructure Overlays`: Proximity analysis to social infrastructure (Father Joe's Villages, Neil Good Day Center) and transit infrastructure (12th & Imperial Transit Center).
  * `6.5 The 121-Meter Southward Centroid Migration`:
    $$(\bar{X}_w, \bar{Y}_w) = \left( \frac{\sum_i w_i x_i}{\sum_i w_i}, \frac{\sum_i w_i y_i}{\sum_i w_i} \right)$$
    Cartographic and vector proof that the count-weighted hotspot centroid migrated 121 meters south toward Commercial St and Imperial Ave between 2018–2020 and 2022–2025.
* **Formulas to Embed:** Global Moran's $I$, Local Getis-Ord $G_i^*$, Weighted Centroid Coordinates.
* **Tables to Embed:**
  * *Table 6.1: Global Moran's I Autocorrelation Metrics Across 12 Digitized Dates*.
  * *Table 6.2: Master Persistence Ranking of Top 10 Hotspot Blocks with Built Environment Indicators*.
  * *Table 6.3: Hotspot Centroid Displacement Coordinates (2018–2020 vs. 2022–2025)*.

#### Section 7: Multiplier Policy Evaluation & Constant-Methodology Counterfactuals
* **Page Budget:** 1.5 pages (~850 words)
* **Subsections:**
  * `7.1 Theoretical Multiplier Shifts vs. Observed Chow Structural Breaks`:
    $$\Delta Y_{\text{theoretical}} = \text{Tents} \times \Delta \mu_{\text{tent}} + \text{Vehicles} \times \Delta \mu_{\text{veh}}$$
    Comparing theoretical multiplier impact against empirical Chow level shift coefficients. Proving that theoretical shifts are small and opposite in sign to observed level shifts (e.g., at May 2018, theoretical change was $+2.1\%$ while observed count dropped $-18.9\%$). Proves macro socio-economic factors drove trends, not multiplier math.
  * `7.2 Construction of the Canonical Hybrid Constant-Methodology Series`:
    Derivation of `TimeSeries_ConstantMethodology.csv` (924 rows). Re-scaling historical pre-2020 counts onto the POST2020 baseline using exact per-row component reconstructions for 2018 and proxy theoretical weights for pre-2018.
  * `7.3 Benchmarking Three Adjustment Approaches`: Comparing Theoretical-Only, Data-Derived-Only, and Hybrid approaches. Explaining why Data-Derived-Only failed (+6.1% bias due to real-change contamination) and formalizing the Hybrid series recommendation.
* **Formulas to Embed:** Theoretical multiplier delta equation.
* **Tables to Embed:**
  * *Table 7.1: Theoretical Multiplier Impact vs. Observed Chow Structural Breaks by Neighborhood*.
  * *Table 7.2: Comparative Evaluation of Three Constant-Methodology Adjustment Philosophies*.
* **Figures to Embed:**
  * *Figure 7.1: Historical Gap Between Raw and Methodology-Adjusted Counts (2017–2025)* (`slide_assets/chart9_clean_hd.png`).

#### Section 8: Predictive Modeling & 12-Month Prospective Machine Learning Pipeline
* **Page Budget:** 2.5 pages (~1,400 words)
* **Subsections:**
  * `8.1 Forecasting Architecture & Multi-Model Formulation`:
    Mathematical formulation of 5 model families: Naive Seasonal ($t-12$), SARIMA $(p,d,q)(P,D,Q)_{12}$, Holt-Winters Exponential Smoothing, Prophet (with changepoints), and Recursive XGBoost.
  * `8.2 Backtesting Methodology: 5-Fold Chronological Expanding Window CV`:
    Evaluation across 5 historical epochs (2017–2024, 96 months, zero future leakage into the 2025 hold-out test set):
    * Fold 1 (2017–2020 $\rightarrow$ 2021 Post-COVID Rebound)
    * Fold 2 (2017–2021 $\rightarrow$ 2022 Historic Surge)
    * Fold 3 (2017–2022 $\rightarrow$ 2023 Peak Volume)
    * Fold 4 (2017–mid 2023 $\rightarrow$ 2023-H2/2024-H1 Ordinance Transition)
    * Fold 5 (2017–2023 $\rightarrow$ 2024 Enforcement Contraction)
  * `8.3 Cross-Validation Results & Model Selection`:
    * *Citywide Champion:* **XGBoost** achieved lowest 12-month CV MAPE (**39.34% $\pm$ 25.36%**, RMSE 169.58) and hold-out 2025 test MAPE (**38.48%**).
    * *Parametric Secondary:* Holt-Winters (39.57% CV MAPE).
    * *Prophet Architectural Failure:* Documenting how fixed-changepoint Prophet overshot 2025 by 250–650 individuals due to inability to capture the 2023 camping ban inflection without adaptive changepoint re-anchoring.
  * `8.4 Production CLI Pipeline Architecture (`forecast_pipeline.py`)`: Automation design, dynamic frequency interpolation (`freq='MS'`), and automated champion dispatching.
  * `8.5 2026 Prospective Projections & Policy Scenario Envelopes`:
    Projections for 2026-01 through 2026-12 across all 9 series with 80% and 95% prediction intervals. Scenario specifications: Optimistic (-24% at Month 12), Baseline (status quo), Pessimistic (+26% at Month 12).
* **Formulas to Embed:** XGBoost objective with regularization, Holt-Winters additive updating equations.
* **Tables to Embed:**
  * *Table 8.1: 5-Fold Expanding Window Cross-Validation Performance Across 5 Model Families (12-Month Horizon)*.
  * *Table 8.2: Out-of-Sample Hold-Out Evaluation on 2025 Test Window (RMSE, MAE, MAPE)*.
  * *Table 8.3: Prospective 12-Month Projections for 2026 with 80%/95% PIs and Policy Scenario Envelopes*.

#### Section 9: Macro-Econometric County-Level Estimation System
* **Page Budget:** 2.5 pages (~1,400 words)
* **Subsections:**
  * `9.1 RTFH Annual Point-in-Time Data Harvest & Longitudinal Pairing`: Compilation of `Downtown_County_PairedCounts.csv` across 8 annual cycles (2017–2025, 2021 waived by HUD). Tracking downtown's share of county unsheltered homelessness: 17.9% pre-pandemic $\rightarrow$ 37.5% peak crisis $\rightarrow$ 14.9% post-ordinance.
  * `9.2 Decoupling Correlation & Small-Sample Power Audit ($N=8$)`:
    * Pearson $r = -0.0609$ ($p = 0.8861$), Spearman $\rho = +0.2143$.
    * Small-sample power audit: $N=8$ provides only 23.3% power to detect $r=0.50$. Minimum Detectable Effect Size requires $|r| \ge 0.850$. Detecting $r=0.50$ requires $N=30$.
  * `9.3 Decisive Rejection of the Constant-Ratio Hypothesis`:
    One-way ANOVA across 3 policy regimes ($F = 66.51, p = 0.0002, \eta^2 = 0.9638$); Kruskal-Wallis ($H = 6.00, p = 0.0498$); Chow test ($F = 43.19, p = 0.0028$). Proof that 96.4% of ratio variance is driven by policy regime shifts. Constant ratio expansion causes up to $+96.2\%$ error.
  * `9.4 8-Fold Leave-One-Year-Out Cross-Validation (LOOCV) Benchmarking`:
    Comparison of Pooled Ratio (RMSE 2,392.61, MAPE 38.19%), Mean Ratio (RMSE 2,482.53), Standard OLS (RMSE 960.53, MAPE 18.19%), and OLS with Trend (RMSE 1,050.44).
  * `9.5 Champion Econometric Model: Policy Regime OLS`:
    $$Y = 4,513.26 + 0.1859 \cdot X + 1,225.04 \cdot D_{\text{post}}$$
    Controlling for the July 2023 camping ban reduced LOOCV RMSE to **815.32** (MAPE = **14.89%**, signed bias = $-0.34\%$). Out-of-sample holdout errors in 2024 and 2025 were only $-6.05\%$ and $+6.47\%$.
  * `9.6 Uncertainty Calibration under Exact Student's t Distributions`:
    $$SE_{\text{pred}}(X_0) = \sigma_\epsilon \sqrt{1 + \frac{1}{N} + \frac{(X_0 - \bar{X})^2}{\sum_{i=1}^N (X_i - \bar{X})^2}}$$
    $$Y_0 \in \left[ \hat{Y}_0 \pm t_{5, 0.975} \cdot SE_{\text{pred}}(X_0) \right] \quad (t_{5, 0.975} = 2.571)$$
    Calibration of empirical margin of error at $\pm 2,050$ individuals ($\approx \pm 35\%$). Current Dec 2025 baseline estimate: **5,921 [95% PI: 3,867 to 7,976]**. Jan 2026 prospective projection: **5,903 [95% PI: 3,849 to 7,957]**.
* **Formulas to Embed:** Policy Regime OLS specification, Student's $t$ exact prediction error formula.
* **Tables to Embed:**
  * *Table 9.1: Historical Paired DSDP and RTFH Homeless Counts and Share Dynamics (2017–2025)*.
  * *Table 9.2: Ratio Stability ANOVA and Regime Fracture Summary*.
  * *Table 9.3: 8-Fold LOOCV Benchmark Performance Across 5 Macro-Estimation Models*.
  * *Table 9.4: Current Operational Countywide Unsheltered Estimates and 95% Prediction Intervals*.

#### Section 10: Methodological Boundaries, Governance Charter & Production Runbook
* **Page Budget:** 1.5 pages (~850 words)
* **Subsections:**
  * `10.1 The 4 Mandatory Public Communication Rules (Governance Charter)`:
    1. *Never report single-point precision* (prohibit "5,921").
    2. *Always round point estimates to the nearest 100* (mandate "5,900").
    3. *Always publish the calibrated 95% range* ("5,900 [3,900 to 8,000]").
    4. *Always disclose the assumed post-July 2023 enforcement policy regime*.
  * `10.2 Statutory Scope of Applicability`: Permitted for interim directional tracking and capacity stress-testing; strictly prohibited for HUD Continuum of Care submissions, statutory budget formulas, and micro-regional sub-allocations.
  * `10.3 Annual Model Retraining Protocol (5-Step Runbook)`: Protocol for ingesting new annual January PIT releases from RTFH, re-testing structural breaks, updating LOOCV, and recalibrating prediction intervals.
  * `10.4 Interactive Decision Support Integration (Task 9.1 Dashboard)`: Overview of the 6 Streamlit dashboard modules (`app.py`, `src/`) and testing protocols.
  * `10.5 Future Research Directions (Assignment 10 Roadmap)`: Ingestion of NOAA weather feeds, City 311 encampment calls, shelter bed utilization censuses, and macroeconomic rental indices.
* **Tables to Embed:**
  * *Table 10.1: Statutory Compliance and Permitted Use Case Matrix*.
  * *Table 10.2: 5-Step Annual Maintenance Runbook for Model Retraining*.

---

## Part 3: Visual & Figure Asset Mapping

This table defines every visual asset to be embedded in both deliverables, specifying source files, figure numbers, and captions:

| Figure ID | Deliverable | Section | Asset Source / Path | Graphic Title & Description |
|---|---|---|---|---|
| **Fig A.1** | Deliverable A | Sec 2 | `slide_assets/chart1_clean_hd.png` | *Nine-Year Trajectory of Downtown Unsheltered Homelessness (2017–2025)*: Three clear epochs (decline, peak, pullback). |
| **Fig A.2** | Deliverable A | Sec 3 | `slide_assets/chart7_yoy_hd.png` | *Volume Concentration vs. Growth Rates by Neighborhood*: Divergence between East Village scale and perimeter growth. |
| **Fig A.3** | Deliverable A | Sec 4 | Exported from Task 7.4 / Tab 2 | *Prospective 2026 Forecast Envelopes and Policy Scenarios*: Baseline vs. Optimistic (-24%) and Pessimistic (+26%). |
| **Fig B.1** | Deliverable B | Sec 2 | `slide_assets/chart9_clean_hd.png` | *Historical Multiplier Adjustment Gap (2017–2025)*: Raw vs. adjusted count comparison across 4 methodology regimes. |
| **Fig B.2** | Deliverable B | Sec 3 | `slide_assets/chart1_clean_hd.png` | *Longitudinal Trajectory and Inflection Points*: 108-month continuous series with policy markers. |
| **Fig B.3** | Deliverable B | Sec 3 | `slide_assets/chart8_clean_hd.png` | *COVID-19 Pandemic Impact and Recovery Profile*: March 2020 trough, Convention Center demobilization, and rebound. |
| **Fig B.4** | Deliverable B | Sec 4 | `slide_assets/chart2_clean_hd.png` | *Calendar-Month Seasonality & Monthly Deviations*: Empirical proof of negligible monthly variance vs. annual shocks. |
| **Fig B.5** | Deliverable B | Sec 6 | Exported from Task 5.3 / Tab 3 | *Getis-Ord Gi\* Hotspot Cartography and Longitudinal Persistence*: Map of 261 blocks and South East Village cluster. |
| **Fig B.6** | Deliverable B | Sec 6 | Exported from Task 5.4 / Tab 3 | *Hotspot Centroid Migration Vector*: 121-meter southward displacement toward Commercial St / Imperial Ave. |
| **Fig B.7** | Deliverable B | Sec 8 | Exported from Task 7.3 / Tab 2 | *5-Fold Expanding Window Cross-Validation Trajectories*: Out-of-sample backtest comparison across 5 model families. |
| **Fig B.8** | Deliverable B | Sec 9 | Exported from Task 8.2 / Tab 5 | *Downtown vs. County Unsheltered Decoupling & Policy Regimes*: Scatter plot illustrating structural fracture after July 2023 ban. |
| **Fig B.9** | Deliverable B | Sec 9 | Exported from Task 8.3 / Tab 5 | *Policy Regime OLS Model Fit and Student's t Prediction Interval*: Regression line with calibrated $\pm 2,050$ margin of error. |

---

## Part 4: Comprehensive Cross-Assignment Validation Checklist

Before finalizing Deliverable A and Deliverable B, every item in this checklist must be rigorously validated to ensure zero omissions from Assignments 1 through 8 and Task 9.1:

```text
[X] 1. DATA CLEANING & RECONCILIATION (Assignment 1):
    [ ] Documented 45-cell audit (97.56% fidelity rate, 2.44% error rate).
    [ ] Explained root cause of 2019 East Village Duplication Bug (all 48 rows duplicated from 2020).
    [ ] Explained root cause of Feb 2018 +30 PDF addition error (504 sum vs 474 published).
    [ ] Explained root cause of all 134 nulls (116 in 2025 reporting lag, 18 in Nov 2018 PDF omission).
    [ ] Documented "Core" alias resolution to City Center.
    [ ] Documented canonical dataset reconstruction in MasterCounts_Adjusted_v2.csv.
    [ ] Documented long-format filtering rule (component=='total' and area_type=='neighborhood').

[X] 2. EXPLORATORY DATA ANALYSIS (Assignment 2):
    [ ] Documented 3 epochs: 2017-2020 decline (-38%), 2021-2023 peak (+57.6% in 2022), 2024-2025 drop (-43.5%).
    [ ] Recorded historical peak of 2,103 (May 2023) and COVID series trough of 529 (March 2020).
    [ ] Documented volume vs growth disconnect (Outside Perimeter +26.9%, East Village +1.64%, Marina -12.76%).

[X] 3. SPATIAL PANEL BALANCING & COVERAGE (Assignment 3):
    [ ] Documented 261 (2018-2021) to 382 (2022-2025) block footprint expansion (+121 Outside Perimeter blocks).
    [ ] Quantified footprint expansion effect (4% to 33% of post-2021 counts driven by boundary shift).
    [ ] Documented geometry validation (380/382 centroids inside, 2 non-convex freeway exceptions).
    [ ] Documented 78-month map digitization gap (90 available maps, only 12 digitized).
    [ ] Documented March 2022 map date anomaly.

[X] 4. TIME SERIES ECONOMETRICS & DECOMPOSITION (Assignment 4):
    [ ] Documented classical additive and robust STL decomposition (12-month period).
    [ ] Documented Kruskal-Wallis proof that 8 of 9 series exhibit NO statistically significant seasonality.
    [ ] Documented that East Village summer bump is non-significant after de-trending (H=13.86, p=0.24).
    [ ] Documented Chow and CUSUM breaks for May 2018 and March 2020 (surviving FDR and HAC-12).
    [ ] Documented ADF/KPSS consensus stationarity (first differencing for 8 series, log1p for Outside Perimeter).

[X] 5. GEOSPATIAL HOTSPOT SURVEILLANCE (Assignment 5):
    [ ] Documented Queen contiguity spatial weights (2,642 directed links on 261-block panel).
    [ ] Documented Global Moran's I statistically significant clustering across all 12 dates (I: 0.063 - 0.239).
    [ ] Documented Getis-Ord Gi* local hotspot classification with 9,999 permutations.
    [ ] Documented top hotspot block: 16TH_ST_IMPERIAL_AV (hotspot on 9/12 dates).
    [ ] Documented that all top 10 persistent blocks reside in South East Village.
    [ ] Documented 121-meter southward centroid migration toward Commercial St / Imperial Ave.
    [ ] Documented OpenStreetMap service and transit infrastructure overlay.

[X] 6. METHODOLOGY MULTIPLIER IMPACT (Assignment 6):
    [ ] Quantified theoretical multiplier shifts vs observed Chow level shifts.
    [ ] Proved theoretical multiplier changes are tiny and opposite in sign to observed Chow shifts.
    [ ] Documented canonical hybrid constant-methodology series in TimeSeries_ConstantMethodology.csv.
    [ ] Documented 3-approach comparison (theoretical-only, data-derived-only, hybrid).

[X] 7. PREDICTIVE MODELING & FORECASTING (Assignment 7):
    [ ] Documented 5-fold expanding window cross-validation (zero future leakage, 2017-2024).
    [ ] Documented citywide champion: XGBoost (12-month CV MAPE = 39.34% +- 25.36%, holdout MAPE = 38.48%).
    [ ] Documented secondary parametric baseline: Holt-Winters (CV MAPE = 39.57%).
    [ ] Documented Prophet fixed-changepoint flaw (overshoots 2025 by 250-650 units).
    [ ] Documented 2026 prospective 12-month forecasts with 80% and 95% prediction intervals.
    [ ] Documented 3 policy scenarios: Optimistic (-24%), Baseline (status quo), Pessimistic (+26%).
    [ ] Documented production CLI pipeline forecast_pipeline.py.

[X] 8. MACRO-ECONOMETRIC COUNTY ESTIMATION (Assignment 8):
    [ ] Documented RTFH PIT compilation (2017-2025, N=8 paired annual counts).
    [ ] Documented downtown share collapse: 17.9% baseline -> 37.5% peak -> 14.9% post-ordinance.
    [ ] Documented long-term decoupling correlation (r = -0.0609, p = 0.8861).
    [ ] Documented ANOVA rejection of constant ratio (F = 66.51, p = 0.0002, eta^2 = 0.9638).
    [ ] Documented small-sample power audit (23.3% power for r=0.50, MDES |r| >= 0.850).
    [ ] Documented 8-fold LOOCV benchmark: ratio failure (RMSE 2,392.61) vs OLS (RMSE 960.53).
    [ ] Documented Policy Regime OLS champion (Y = 4,513.26 + 0.1859*X + 1,225.04*D_post, RMSE 815.32).
    [ ] Documented exact Student's t (df=5) 95% PI with margin of error +-2,050 individuals (+-35%).
    [ ] Documented Dec 2025 estimate: 5,921 [3,867 to 7,976]; Jan 2026 estimate: 5,903 [3,849 to 7,957].
    [ ] Documented The 4 Public Communication Rules and governance charter.
    [ ] Documented 5-step annual retraining runbook.

[X] 9. INTERACTIVE DASHBOARD SYSTEM (Task 9.1):
    [ ] Documented 6-tab Streamlit dashboard architecture (Historical, Forecast, Hotspot, Decomposition, Calculator, About).
    [ ] Documented test suite (test_data_loader.py, test_calculator.py, test_forecast_logic.py).
    [ ] Documented cloud deployment runbook and v9.1-dashboard release tag.
```

---

## Part 5: Implementation Execution Protocol for Task 9.2

When authoring the two deliverables, follow these strict execution rules:
1. **Source Data Truth:** Pull all metrics directly from the canonical files in `data/` (`MasterCounts_Adjusted_v2.csv`, `TimeSeries_ConstantMethodology.csv`, `Forecasts_12Month.csv`, `Downtown_County_PairedCounts.csv`, `CountyEstimate_Current.csv`, `Hotspot_Persistence_Ranking.csv`, `SeasonalIndices.csv`, `StructuralBreaks.csv`).
2. **Formatting & Math Rigor:** Use standard GitHub Flavored Markdown and LaTeX math blocks (`$$ ... $$` and `$ ... $`) for Deliverable B. Use clean executive formatting, Markdown tables, and bold takeaway callouts for Deliverable A.
3. **No Truncation or Placeholders:** Both deliverables must be authored in full, professional prose. Deliverable A must strictly span 3–4 pages (~1,800 words), and Deliverable B must strictly span 15–20 pages (~9,500 words).
4. **Permanent Storage:** Save both deliverables directly in the repository root:
   - `ExecutiveSummary_NonTechnical.md`
   - `FullTechnicalReport.md`
5. **Quality Review:** After drafting, review against the Part 4 checklist to guarantee 100% fidelity to all project milestones.
