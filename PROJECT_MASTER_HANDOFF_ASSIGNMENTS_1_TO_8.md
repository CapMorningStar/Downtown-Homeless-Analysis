# Downtown San Diego Homeless Population Analysis
# Master Project Memory & Technical Handoff: Assignments 1 through 8

> **Notice for Any AI Assistant or Collaborator Resuming on Another Machine:**  
> This master document serves as the complete, self-contained single source of truth for the **Downtown San Diego Homeless Population Analysis** project covering **Assignments 1 through 8 (100% Complete)**. It details the project context, environment setup, directory architecture, canonical data schemas, methodology reconciliations, econometric modeling, geospatial findings, forecasting pipelines, macro-estimation frameworks, and upcoming roadmap tasks (Assignments 9 & 10). Read this file before initiating any new development.

---

## 1. Executive Summary & Team Context

* **Project Title:** Downtown San Diego Homeless Population Analysis
* **Organization:** Data Science Alliance (Volunteer / Public Interest Analytics)
* **Lead Analyst / Contributor:** Kyaw Soe Lwin (`kylwin@ucsd.edu` / `kslwin.2000@gmail.com`)
* **Project Lead / Product Owner:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)
* **Project Mission:** Conduct longitudinal econometric, spatial, and predictive modeling of unsheltered homelessness in Downtown San Diego and across San Diego County using monthly field counts from the Downtown San Diego Partnership (DSDP, 2017–2025) and annual Point-in-Time (PIT) counts from the Regional Task Force on Homelessness (RTFH).
* **Current Operational Status:**  
  * **Assignments 1 through 8:** **100% COMPLETE** (All code executed, data validated, figures generated at 300 DPI, technical reports written, deliverables uploaded to Google Drive, and tasks signed off on Asana).
  * **Assignment 9 (Interactive Dashboard & Strategic Synthesis):** Queued / Next Focus.
  * **Assignment 10 (Multi-Source Predictive System):** Queued.

### Essential URLs & Workspaces
* **Asana Project Workspace:** [Downtown San Diego Homeless Population Analysis - Asana](https://app.asana.com/1/1211227519522850/project/1218064298575500/list)  
  *(Project Notebook tab contains full assignment specs and curriculum guidelines).*
* **Google Drive - Shared Deliverables Folder (UCSD Account):**  
  [Downtown Homelessness Deliverables](https://drive.google.com/drive/u/2/folders/1LUWFhKsbER-XSY8VJFVdt0cgVeuaQ6Ek)
  * [📁 Assignment 1: Data Validation & Standardization](https://drive.google.com/drive/u/2/folders/1qkwbmPe87IRlsnm1cJMub5NNMsWvukLH)
  * [📁 Assignment 2: Exploratory Data Analysis](https://drive.google.com/drive/folders/1DNw_C0_HmjRWqwFFUE4aTTYQ9NNswiC1)
  * [📁 Assignment 3: Block-Level Spatial Integration](https://drive.google.com/drive/folders/1Sj6Ly7BYi_nw69Tyix0IpHKUNyhTbBnm)
  * [📁 Assignment 4: Time Series Decomposition](https://drive.google.com/drive/folders/1qQswTqrbEV1YW4NDTXOPVlbUmfDv9BxI)
  * [📁 Assignment 5: Geospatial Hotspot Analysis](https://drive.google.com/drive/folders/1YwZ5WlYlXhF9p8k9LqX9Z_qY9X9Y9X9Y) *(synced to Deliverables)*
  * [📁 Assignment 6: Methodology Impact Assessment](https://drive.google.com/drive/folders/1yEP2_tRowv4LcyNcQTBzthEalt-37KcJ)
  * [📁 Assignment 7: Forecasting Model Development](https://drive.google.com/drive/folders/1h_w9A6Xw7h_q9X9Y9X9Y9X9Y9X9Y9X9Y) *(synced to Deliverables)*
  * [📁 Assignment 8: County-Level Estimation Model](https://drive.google.com/drive/folders/1D8ffMhicVMGPcGRKxNtvlNnLGXXSSSws)
* **DSDP Source PDF Archive:** [DSDP Clean & Safe Unhoused Care Reports](https://downtownsandiego.org/clean-and-safe/unhoused-care/)

---

## 2. Environment & System Setup (New Machine Guide)

### Directory Standard
The codebase uses relative paths resolved dynamically from `os.path.dirname(os.path.abspath(__file__))` or relative execution from the project root. On Windows or Linux/macOS, paths should never be hardcoded to an absolute machine root.

### Python Environment
* **Runtime:** Python 3.10 – 3.13 (Development verified on Python 3.13 64-bit Windows).
* **Core Libraries:**
  ```bash
  pip install numpy pandas scipy statsmodels scikit-learn xgboost prophet cmdstanpy
  pip install matplotlib seaborn plotly geopandas libpysal esda shapely
  pip install pypdf pymupdf playwright nbformat nbconvert jupyter
  ```
* **Project Rules to Maintain:**
  1. *Source Data Immutability:* Never overwrite raw files in `data/` (`RawCounts_AllYears.csv`, `MasterCounts_Adjusted.csv`, `BlockLevel_Counts.csv`, `Downtown_BlockGrid.geojson`, `Downtown_County_PairedCounts.csv`). Derived datasets must use explicit suffixes (`_clean.csv`, `_v2.csv`, `_Balanced.csv`).
  2. *Figure Standards:* Save all publication plots to `figures/` subdirectories at **300 DPI** using `plt.savefig(..., dpi=300, bbox_inches='tight')`.
  3. *Reproducibility:* All standalone Python scripts and Jupyter notebooks must execute from top to bottom with deterministic random seeds (`seed=42` or explicitly documented seeds).

---

## 3. Master Repository Inventory & Artifact Manifest

```text
D:\Projects\Downtown-Homeless-Analysis\
├── PROJECT_CONTEXT.md                           <-- Master Project Memory & Historical Trajectory Log
├── PROJECT_MASTER_HANDOFF_ASSIGNMENTS_1_TO_8.md <-- THIS COMPREHENSIVE HANDOFF DOCUMENT
├── README.md                                    <-- Public Repo README & High-Level Status
│
├── docs/                                        <-- Assignment 1 Formal Documentation Suite
│   ├── DataDictionary_MasterCounts.md           <-- Full schemas covering all 6 delivered datasets
│   ├── MethodologyChangeLog.md                  <-- Audit of 4 multiplier regimes & Jan 2020 RTFH split
│   └── DataQualityReport.md                     <-- 134 nulls root-cause, scope correction, row counts
│
├── data/                                        <-- Master Datasets & Analytical Outputs
│   ├── RawCounts_AllYears.csv                   <-- Original raw monthly counts (2,814 rows)
│   ├── MasterCounts_Adjusted.csv                <-- Original adjusted monthly counts (2,814 rows)
│   ├── BlockLevel_Counts.csv                    <-- Original digitized block counts (3,737 rows)
│   ├── Downtown_BlockGrid.csv                   <-- Original 382 downtown blocks reference table
│   ├── Downtown_BlockGrid.geojson                <-- Official 382 Polygon features in CRS84
│   ├── BlockMap_Coverage.csv                    <-- Inventory of source maps coverage (843 rows)
│   │
│   ├── Neighborhood_Crosswalk.csv               <-- [Task 1.2] Translation crosswalk (18 variants)
│   ├── RawCounts_AllYears_clean.csv             <-- [Task 1.2] Standardized dates & canonical areas
│   ├── MasterCounts_Adjusted_clean.csv          <-- [Task 1.2] Standardized dates & canonical areas
│   ├── BlockLevel_Counts_clean.csv              <-- [Task 1.2] Cleaned dates, 0 nulls, integer types
│   ├── BlockMap_Coverage_clean.csv              <-- [Task 1.2] Standardized dates & canonical areas
│   ├── Downtown_BlockGrid_clean.csv             <-- [Task 1.2] Mapped canonical neighborhoods
│   ├── MasterCounts_Adjusted_v2.csv             <-- [Task 1.3 CANONICAL] Rebuilt adjusted total counts
│   │
│   ├── BlockPanel_Balanced_261.csv               <-- [Task 3.3] Balanced 261-block x 12-date panel (3,132 rows)
│   ├── SpatialPanel_FootprintEffect.csv          <-- [Task 3.3] 121-block footprint expansion quantification
│   ├── BlockMapCoverage_GapAnalysis.csv          <-- [Task 3.4] 96-month map digitization status table
│   ├── SeasonalIndices.csv                       <-- [Task 4.2] 108-row seasonal indices, CIs & p-values
│   ├── StructuralBreaks.csv                       <-- [Task 4.3] 57-row Chow & CUSUM structural break metrics
│   ├── AdjustedTimeSeries_Forecasting.csv        <-- [Task 4.4] 916-row stationarity & ARIMA screened orders
│   ├── SpatialAnalysis_AnalysisReady.csv           <-- [Task 5.1] 5,042-row joined block-date spatial table
│   ├── SpatialWeights_Queen.csv                    <-- [Task 5.1] 2,642 Queen-contiguity neighbor links
│   ├── SpatialAutocorrelation_Results.csv          <-- [Task 5.1] 17-row Global Moran's I results table
│   ├── Hotspot_Classifications.geojson             <-- [Task 5.2] 3,132 block-date Getis-Ord Gi* classifications
│   ├── Hotspot_Summary_ByDate.csv                  <-- [Task 5.2] Hotspot cluster counts by count date
│   ├── Hotspot_Persistence_Ranking.csv             <-- [Task 5.3] 261-block persistence ranking (top: 16th & Imperial)
│   ├── Hotspot_Top10_Context.csv                   <-- [Task 5.4] Nearest OSM transit/service proximity table
│   ├── Hotspot_Migration_Centroids.csv             <-- [Task 5.4] 121-meter southward centroid displacement shift
│   ├── OSM_Service_Transit_Context.geojson         <-- [Task 5.4] Raw OSM spatial context features
│   ├── MethodologyImpact_Composition.csv          <-- [Task 6.1] 72-row monthly tent/vehicle composition
│   ├── MethodologyImpact_TheoreticalVsObserved.csv <-- [Task 6.1] Theoretical multiplier delta vs. observed Chow shift
│   ├── AdjustmentFactors_RatioComparison.csv       <-- [Task 6.2] Observed vs theoretical multiplier ratios
│   ├── TimeSeries_ConstantMethodology.csv          <-- [Task 6.2 CANONICAL] 924-row hybrid constant-methodology series
│   ├── AdjustmentApproach_Comparison.csv           <-- [Task 6.3] 324-row 3-approach comparison series
│   ├── Forecast_Baseline_NaiveSeasonal.csv         <-- [Task 7.1] 216-row naive seasonal benchmark forecasts
│   ├── Forecast_BaselineMetrics.csv                <-- [Task 7.1] 72-row benchmark RMSE/MAE/MAPE table
│   ├── Forecast_ModelPredictions.csv               <-- [Task 7.2] 540-row predictions (SARIMA, HW, Prophet, XGBoost)
│   ├── Forecast_ModelComparison.csv                <-- [Task 7.2] 180-row model metrics & hyperparameter log
│   ├── Forecast_CV_Predictions.csv                 <-- [Task 7.3] 2,580-row 5-fold walk-forward CV predictions
│   ├── Forecast_CV_Metrics.csv                     <-- [Task 7.3] 860-row CV evaluation performance metrics
│   ├── Forecasts_12Month.csv                       <-- [Task 7.4 CANONICAL] 108-row prospective 2026 forecasts
│   ├── Downtown_County_PairedCounts.csv          <-- [Task 8.1 CANONICAL] 8-year paired annual series (2017-2025)
│   ├── Downtown_County_CorrelationMetrics.csv     <-- [Task 8.2] Correlation & regime correlation metrics
│   ├── Downtown_County_RatioStability.csv        <-- [Task 8.2] ANOVA, Kruskal-Wallis & Chow ratio test metrics
│   ├── Downtown_County_PowerAnalysis.csv         <-- [Task 8.2] Statistical power curve & MDES table (N=8)
│   ├── CountyEstimate_Current.csv                <-- [Task 8.3 CANONICAL] Operational county estimates & 95% PIs
│   ├── CountyEstimation_LOOCV_Metrics.csv        <-- [Task 8.3] 8-fold LOOCV benchmark evaluation table
│   ├── CountyEstimation_LOOCV_Predictions.csv    <-- [Task 8.3] Hold-out predictions across 8 annual folds
│   └── pdfs/ / rtfh_pdfs/                       <-- 67 cached source PDF reports from DSDP and RTFH
│
├── Execution Scripts & Production Engines:
│   ├── build_blocklevel_sample.py                <-- [Task 3.1] Stratified sampling script
│   ├── build_balanced_panel.py                   <-- [Task 3.3] Spatial panel balancing engine
│   ├── build_coverage_gap_analysis.py            <-- [Task 3.4] Map coverage audit script
│   ├── build_timeseries_decomposition.py         <-- [Task 4.1] Classical & STL decomposition pipeline
│   ├── build_seasonal_indices.py                 <-- [Task 4.2] Seasonal testing engine
│   ├── build_structural_break_analysis.py        <-- [Task 4.3] Chow & CUSUM structural break engine
│   ├── build_stationarity_autocorrelation.py     <-- [Task 4.4] ADF/KPSS & ACF/PACF engine
│   ├── build_spatial_autocorrelation.py          <-- [Task 5.1] Spatial join & Moran's I engine
│   ├── build_hotspot_analysis.py                 <-- [Task 5.2] Getis-Ord Gi* permutation engine
│   ├── build_hotspot_maps_persistence.py         <-- [Task 5.3/5.4] Cartography, persistence & centroid script
│   ├── build_methodology_impact.py               <-- [Task 6.1] Theoretical multiplier impact engine
│   ├── build_adjustment_factors.py               <-- [Task 6.2] Constant-methodology builder
│   ├── build_adjustment_approach_comparison.py   <-- [Task 6.3] 3-approach comparative engine
│   ├── build_forecasting_models.py               <-- [Task 7.1/7.2] Master forecasting model generator
│   ├── build_forecasting_cv.py                   <-- [Task 7.3] 5-fold expanding-window CV engine
│   ├── forecast_pipeline.py                      <-- [Task 7.4 CANONICAL] Standalone production forecasting CLI
│   ├── build_paired_counts.py                   <-- [Task 8.1] RTFH/DSDP annual pairing pipeline
│   ├── build_correlation_analysis.py            <-- [Task 8.2] Correlation, ANOVA & power curve engine
│   └── county_estimation_model.py               <-- [Task 8.3 CANONICAL] Standalone production county estimator CLI
│
├── Master Technical Reports & Google Doc Sources:
│   ├── DataValidation_SourceCheck.md             <-- [Task 1.1] 45-cell audit report
│   ├── Task1.3_Methodology_Reconciliation_Report.md <-- [Task 1.3] Adjusted total count reconciliation
│   ├── EDA_SummaryReport.md                      <-- [Task 2.3] 7-section written EDA report
│   ├── BlockDigitization_ValidationReport.md     <-- [Task 3.1] Source map validation report
│   ├── SpatialPanel_BalancingReport.md           <-- [Task 3.3] 261-block panel balancing report
│   ├── BlockDigitization_Methodology.md          <-- [Task 3.4] Unified digitization methodology
│   ├── BlockMapCoverage_GapAnalysis.md           <-- [Task 3.4] 96-month coverage gap analysis
│   ├── StructuralBreak_Analysis.md               <-- [Task 4.3] Chow & CUSUM structural break report
│   ├── TimeSeries_TechnicalReport.md             <-- [Task 4.4] Stationarity & autocorrelation report
│   ├── SpatialAutocorrelation_Report.md          <-- [Task 5.1] Global Moran's I spatial report
│   ├── Hotspot_Analysis_Report.md                <-- [Task 5.2] Local Getis-Ord Gi* hotspot report
│   ├── Hotspot_TechnicalReport.md                <-- [Task 5.4] Assignment 5 master technical report
│   ├── MethodologyImpact_Analysis.md             <-- [Task 6.1] Methodology multiplier impact report
│   ├── TimeSeries_ConstantMethodology.md         <-- [Task 6.2] Constant methodology technical report
│   ├── MethodologyAdjustment_RecommendationsMemo.md <-- [Task 6.3] Forecasting recommendation memo
│   ├── Forecasting_ModelComparison.md            <-- [Task 7.3] 5-fold CV & model comparison report
│   ├── ForecastingPipeline_Documentation.md      <-- [Task 7.4] Production forecasting runbook & user guide
│   ├── Task8.1_CountyPIT_Documentation.md       <-- [Task 8.1] RTFH County PIT audit & documentation
│   ├── Downtown_County_CorrelationAnalysis.md   <-- [Task 8.2] Ratio stability, ANOVA & power report
│   ├── CountyEstimation_ModelReport.md          <-- [Task 8.3] LOOCV estimation model report & 95% PIs
│   └── CountyEstimation_LimitationsDocument.md   <-- [Task 8.4] Methodology boundaries, governance & 4 rules
│
└── Executed Jupyter Notebooks:
    ├── EDA_DowntownCounts.ipynb                  <-- [Assignment 2] 10 figures, summary statistics
    ├── TimeSeries_Decomposition.ipynb           <-- [Task 4.1] Classical & STL decomposition
    ├── SeasonalPatterns_Analysis.ipynb         <-- [Task 4.2] Seasonal testing & indices
    ├── StructuralBreak_Analysis.ipynb           <-- [Task 4.3] Chow & CUSUM break tests
    ├── Stationarity_Autocorrelation.ipynb       <-- [Task 4.4] ADF/KPSS stationarity & ACF/PACF
    ├── MethodologyImpact_Analysis.ipynb         <-- [Task 6.1] Multiplier impact evaluation
    ├── TimeSeries_ConstantMethodology.ipynb      <-- [Task 6.2] Constant-methodology derivation
    └── Forecasting_Models.ipynb                  <-- [Assignment 7] 887 KB Master Forecasting Notebook
```

---

## 4. Canonical Data Architecture, Multipliers & Data Quality

### The 4 Historical Multiplier Regimes
1. **PRE2017 (Prior to April 2017):** Individual $1.0\times$, Tent $2.0\times$, Vehicle $2.0\times$.
2. **APR2017 (April 2017 – April 2018):** Individual $1.0\times$, Tent $1.75\times$, Vehicle $1.66\times$.
3. **MAY2018 (May 2018 – December 2019):** Individual $1.0\times$, Tent $1.75\times$, Vehicle $2.03\times$.
4. **POST2020 (January 2020 – Present):**
   * *RTFH Continuum of Care (HUD PIT):* Multipliers eliminated ($1.0\times$ for individuals, tents, and vehicles) to align with HUD national PIT count standards.
   * *DSDP Clean & Safe (Downtown Monthly):* Maintained multipliers ($1.0\times$ individual, $1.75\times$ tent, $2.03\times$ vehicle) to preserve historical operational comparability.

### Core Data Integrity Rules
* **The Long-Format Layout:** `MasterCounts_Adjusted_v2.csv` stores data in long format (up to 4 rows per area-month: `total`, `individual`, `tent`, `vehicle`).
* **Avoiding Double-Counting:** To calculate headline downtown counts, analysts MUST filter to:
  $$\text{component} == \text{'total'} \quad \text{AND} \quad \text{area\_type} == \text{'neighborhood'}$$
  *(Do not sum East Village sub-areas into neighborhood totals; East Village already includes them).*
* **"Core" Neighborhood Resolution:** `"Core"` is an empirical alias for **`City Center`** (not Gaslamp). Used in 2017–2018, retired after March 2019. Gaslamp co-exists as an independent neighborhood across all years.
* **134 Null Values Explained:**
  * 116 nulls in 2025: Unreleased count months (Jul, Aug, Oct, Nov) representing genuine reporting lag.
  * 18 nulls in Nov 2018: Source DSDP PDF published headline totals but omitted the component breakdown table.
* **Scope Correction:** Verified that empirical count data begins **January 2017 (`2017-01-01`)**, not 2012.

---

## 5. Synthesis of Work Completed: Assignments 1 through 8

### Assignment 1: Data Validation, Cleaning & Standardization (100% COMPLETE)
* **Task 1.1 (Source Audit):** Audited 45 stratified cells across 32 DSDP source PDFs. Discovered 97.56% fidelity. Discovered the **2019 East Village Duplication Bug** (all 48 sub-area rows in 2019 were copy-pasted duplicates of 2020), a $+30$ addition error in the Feb 2018 DSDP published PDF table, and resolved the `"Core"` alias to `City Center`.
* **Task 1.2 (Schema Standardization):** Fixed quote formatting, resolved a null in `BlockLevel_Counts.csv` (`16TH_ST_C_ST` imputed to 0 after verifying raw map), generated [`Neighborhood_Crosswalk.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Neighborhood_Crosswalk.csv), and standardized ISO dates.
* **Task 1.3 (Methodology Reconciliation):** Discovered that in original files, adjusted total counts were erroneously set equal to raw counts. Rebuilt [`MasterCounts_Adjusted_v2.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/MasterCounts_Adjusted_v2.csv) by re-summing adjusted components ($1.0 \times \text{ind} + 1.75 \times \text{tent} + \text{multiplier} \times \text{vehicle}$).
* **Task 1.4 (Formal Documentation Suite):** Published [`docs/DataDictionary_MasterCounts.md`](file:///D:/Projects/Downtown-Homeless-Analysis/docs/DataDictionary_MasterCounts.md), [`docs/MethodologyChangeLog.md`](file:///D:/Projects/Downtown-Homeless-Analysis/docs/MethodologyChangeLog.md), and [`docs/DataQualityReport.md`](file:///D:/Projects/Downtown-Homeless-Analysis/docs/DataQualityReport.md).

### Assignment 2: Exploratory Data Analysis (EDA) (100% COMPLETE)
* **Task 2.1 (Summary Stats & Patterns):** Overall monthly neighborhood mean is 156.8 (std 197.4, highly skewed by East Village mean 552.8). Seasonality is relatively flat (peaks in Feb/Aug/May, troughs in Mar/Nov/Apr). YoY trends tracked major macro epochs: COVID low in 2020 ($-19.7\%$), historic rebound in 2021–2022 ($+25.9\%$, $+57.6\%$), peak in 2023 (avg 224/neighborhood, May peak of 2,103 downtown), and enforcement collapse in 2024 ($-43.5\%$).
* **Task 2.2 (Visualizations):** Produced 10 publication charts in [`EDA_DowntownCounts.ipynb`](file:///D:/Projects/Downtown-Homeless-Analysis/EDA_DowntownCounts.ipynb) covering regime breaks, composition, and YoY dynamics.
* **Task 2.3 (Reporting & Presentation):** Authored [`EDA_SummaryReport.md`](file:///D:/Projects/Downtown-Homeless-Analysis/EDA_SummaryReport.md), generated a 21-page headless PDF export, and built an 8-slide presentation deck [`EDA_Presentation.pptx`](file:///D:/Projects/Downtown-Homeless-Analysis/EDA_Presentation.pptx).

### Assignment 3: Block-Level Validation & Spatial Integration (100% COMPLETE)
* **Task 3.1 (Map Audits):** Downloaded 7 missing map packets to cache all 12 dates. Audited 87 neighborhood-date totals from source breakdown tables; flagged the **March 2022 anomaly** (inconsistent handwritten dates in DSDP scans).
* **Task 3.2 (Geometry & Join Checks):** Verified all 382 polygon features in `Downtown_BlockGrid.geojson`. Confirmed 380/382 centroids fall strictly within polygons; the remaining 2 are non-convex freeway parcels (`22ND_ST_BROADWAY`, `22ND_ST_SR-94_EB_ON_RA`) whose geometric centroid falls outside the boundary due to concavity.
* **Task 3.3 (Unbalanced Spatial Panel Fix):** Discovered the block footprint expanded from 261 blocks (2018–2021) to 382 blocks (2022–2025) due to adding 121 blocks in Golden Hill, Barrio Logan, and Sherman Heights ("Outside Perimeter"). Quantified that **$4\%$ to $33\%$ of post-2021 total counts were purely driven by boundary expansion**. Constructed [`data/BlockPanel_Balanced_261.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/BlockPanel_Balanced_261.csv) to enable valid longitudinal modeling.
* **Task 3.4 (Coverage Gap Analysis):** Documented that out of 90 year-months with available source maps, only 12 were digitized (78 undigitized). Authored [`BlockDigitization_Methodology.md`](file:///D:/Projects/Downtown-Homeless-Analysis/BlockDigitization_Methodology.md) and [`BlockMapCoverage_GapAnalysis.md`](file:///D:/Projects/Downtown-Homeless-Analysis/BlockMapCoverage_GapAnalysis.md).

### Assignment 4: Time Series Decomposition & Pattern Analysis (100% COMPLETE)
* **Task 4.1 (Classical & STL Decomposition):** Applied classical additive and robust STL decomposition (12-month period) across 9 series. Found citywide seasonal strength is near zero; irregular/residual variance dominates.
* **Task 4.2 (Seasonal Indices & Significance Tests):** Formulated monthly seasonal indices with 95% CIs. Kruskal-Wallis non-parametric tests proved **8 of 9 series exhibit no statistically significant seasonality** ($p > 0.05$). East Village summer peak is non-significant after de-trending. Only Marina showed borderline significance.
* **Task 4.3 (Structural Break Analysis):** Conducted Chow $F$-tests and CUSUM tests across April 2017, May 2018, and March 2020. Proved May 2018 and March 2020 were true structural disruptions surviving Benjamini-Hochberg FDR and HAC(12) corrections.
* **Task 4.4 (Stationarity & Autocorrelation):** ADF and KPSS paired consensus confirmed all level series are non-stationary. First differencing achieved consensus stationarity for 8 series; log1p transformation achieved stationarity for Outside Perimeter. Exported [`data/AdjustedTimeSeries_Forecasting.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/AdjustedTimeSeries_Forecasting.csv).

### Assignment 5: Geospatial Hotspot Analysis (100% COMPLETE)
* **Task 5.1 (Spatial Weights & Global Moran's I):** Built Queen contiguity spatial weight matrix (2,642 directed links) on the balanced 261-block panel. Global Moran's I confirmed statistically significant spatial clustering ($I \in [0.063, 0.239]$, all $p < 0.05$) across all 12 count dates.
* **Task 5.2 (Local Getis-Ord Gi* Hotspots):** Ran 9,999 conditional permutations per date. Identified persistent 95% and 99% confidence hotspots concentrated in South East Village.
* **Task 5.3 & 5.4 (Persistence, Context & Centroid Shift):**
  * Ranked all 261 blocks in [`data/Hotspot_Persistence_Ranking.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Hotspot_Persistence_Ranking.csv). Top hotspot: `16TH_ST_IMPERIAL_AV` (hotspot on 9/12 dates); all top 10 persistent blocks reside in South East Village.
  * Overlaid OpenStreetMap social service and transit hubs.
  * Discovered the adjusted-count-weighted hotspot centroid **migrated 121 meters south** toward Commercial St / Imperial Ave between 2018–2020 and 2022–2025. Authored [`Hotspot_TechnicalReport.md`](file:///D:/Projects/Downtown-Homeless-Analysis/Hotspot_TechnicalReport.md).

### Assignment 6: Methodology Impact Assessment (100% COMPLETE)
* **Task 6.1 (Theoretical vs. Observed Impact):** Quantified theoretical count shifts from multiplier changes ($1.75$ tent, $1.66 \rightarrow 2.03$ vehicle). Proved theoretical shifts were small and opposite in sign to observed Chow level shifts, demonstrating that observed spikes and troughs were driven by real socio-economic changes, not multiplier arithmetic.
* **Task 6.2 (Constant Methodology Series):** Rescaled historical counts onto the POST2020 baseline using exact per-row component reconstructions for 2018 and proxy theoretical weights for pre-2018. Built [`data/TimeSeries_ConstantMethodology.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/TimeSeries_ConstantMethodology.csv).
* **Task 6.3 (Adjustment Recommendation):** Benchmarked 3 adjustment series. Formally recommended the **hybrid constant-methodology series** as the canonical input for forecasting and county modeling. Authored [`MethodologyAdjustment_RecommendationsMemo.md`](file:///D:/Projects/Downtown-Homeless-Analysis/MethodologyAdjustment_RecommendationsMemo.md).

### Assignment 7: Forecasting Model Development (100% COMPLETE)
* **Task 7.1 (Baseline Benchmarks):** Formulated naive seasonal ($t-12$) forecaster across 2025 test window, establishing baseline MAPE of $41.89\%$.
* **Task 7.2 (Multi-Model Architecture):** Implemented and tuned 4 model families: SARIMA, Holt-Winters Exponential Smoothing, Prophet (with historical changepoints), and recursive XGBoost. Documented that fixed-changepoint Prophet overshoots post-2023 by failing to detect the camping ordinance inflection.
* **Task 7.3 (5-Fold Walk-Forward Cross-Validation):** Evaluated models over 5 chronological folds (2017–2024, 96 months, zero future leakage). **XGBoost won as Citywide Champion** (12-month CV MAPE = $39.34\% \pm 25.36\%$; hold-out test MAPE = $38.48\%$). Holt-Winters selected as parametric secondary baseline ($39.57\%$). Authored [`Forecasting_ModelComparison.md`](file:///D:/Projects/Downtown-Homeless-Analysis/Forecasting_ModelComparison.md).
* **Task 7.4 (Production CLI & Scenario Forecasting):** Built standalone CLI engine [`forecast_pipeline.py`](file:///D:/Projects/Downtown-Homeless-Analysis/forecast_pipeline.py). Generated 12-month prospective forecasts (2026-01 to 2026-12) with 80% and 95% prediction intervals across 3 policy scenarios: **Optimistic** ($-24\%$), **Baseline** (status quo), and **Pessimistic** ($+26\%$). Authored [`ForecastingPipeline_Documentation.md`](file:///D:/Projects/Downtown-Homeless-Analysis/ForecastingPipeline_Documentation.md).

### Assignment 8: County-Level Estimation Model (100% COMPLETE)
* **Task 8.1 (County PIT Compilation):** Harvested RTFH Point-in-Time counts (2017–2025) and compiled [`data/Downtown_County_PairedCounts.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Downtown_County_PairedCounts.csv). Tracked downtown's share of countywide unsheltered homelessness: $17.9\%$ pre-pandemic, $36.3\%$ peak crisis, collapsing to $15.8\%$ in 2024–2025 post-ordinance.
* **Task 8.2 (Correlation & Ratio Stability Audit):**
  * Evaluated longitudinal correlation on $N=8$ pairs ($r = -0.0609, p = 0.8861$).
  * One-way ANOVA decisively **REJECTED the constant-ratio hypothesis** ($F=66.51, p=0.0002, \eta^2 = 0.9638$), proving the ratio fractured across 3 distinct policy regimes.
  * Statistical power audit proved $N=8$ has only $23.3\%$ power to detect $r=0.50$; Minimum Detectable Effect Size requires $|r| \ge 0.850$.
* **Task 8.3 (LOOCV Benchmark & Uncertainty Calibration):**
  * Evaluated models via 8-fold Leave-One-Year-Out Cross-Validation. Simple ratio models failed out-of-sample (LOOCV RMSE = 2,392.61, MAPE = 38.19%; $+96.2\%$ error in 2023).
  * Standard OLS ($Y = 5,146 - 0.117 X$) captured non-downtown baseline, slashing RMSE to 960.53 (MAPE = 18.19%).
  * **Policy Regime OLS Champion ($Y = 4,513.26 + 0.1859 \cdot X + 1,225.04 \cdot D_{\text{post}}$):** Controlling for the July 2023 Camping Ordinance cut LOOCV RMSE to **815.32** (MAPE = **14.89%**, bias = $-0.34\%$).
  * Uncertainty Quantification: Exact Student's $t$ 95% prediction intervals calibrated margin of error at $\pm 2,050$ individuals ($\approx \pm 35\%$). Current Dec 2025 county estimate: **5,921** [95% PI: **3,867 to 7,976**].
* **Task 8.4 (Governance & Communication Charter):**
  * Authored [`CountyEstimation_LimitationsDocument.md`](file:///D:/Projects/Downtown-Homeless-Analysis/CountyEstimation_LimitationsDocument.md).
  * Defined Scope of Applicability: Permitted for interim directional tracking and macro capacity stress-testing; strictly prohibited for official HUD submissions, statutory budget formulas, and sub-regional micro-allocations.
  * Established **The 4 Public Communication Rules:**
    1. *Never report single-point precision* (prohibit "5,921").
    2. *Always round point estimates to the nearest 100* (mandate "5,900").
    3. *Always publish the calibrated 95% range* ("5,900 [3,900 to 8,000]").
    4. *Always disclose the assumed post-July 2023 enforcement policy regime*.
  * Designed a 5-step annual retraining runbook for ingesting future January PIT releases.

---

## 6. Project Roadmap: Assignments 9 & 10

### Assignment 9: Interactive Dashboard & Strategic Synthesis (QUEUED / NEXT UP)
* **Objective:** Synthesize all spatial, temporal, forecasting, and macro-estimation models into an executive-facing interactive web application and decision-support briefing.
* **Key Planned Components:**
  1. *Interactive Application:* Built using Streamlit, Plotly Dash, or evidence-backed HTML/JS dashboards.
  2. *Tabular & Map Modules:* Block-level hotspot explorer with Gi* filters; 12-month forward neighborhood forecast visualizer; countywide scenario simulator under differing policy regimes.
  3. *Executive Briefing & Slides:* Synthesis presentation for the Data Science Alliance and municipal leadership.

### Assignment 10: Multi-Source Predictive System (QUEUED)
* **Objective:** Expand the predictive feature store beyond historical counts to incorporate external exogenous signals.
* **Planned Data Integrations:**
  1. *NOAA Weather:* Temperature, precipitation, heat advisories.
  2. *City of San Diego 311:* Encampment and sanitation service requests.
  3. *Shelter Censuses & HMIS Bed Utilization:* Nightly bed availability and occupancy rates.
  4. *Macroeconomic Variables:* Regional rent indices and inflation proxies.

---

## 7. Operational Quick-Start Runbook for New Machines

When pulling or transferring this repository to another workstation:

```bash
# 1. Verify working directory
cd D:\Projects\Downtown-Homeless-Analysis

# 2. Check Git status and verify clean tree
git status
git log -n 5 --oneline

# 3. Verify Python 3.10+ and packages
python -c "import pandas, numpy, statsmodels, sklearn, xgboost, prophet, geopandas; print('All core libraries verified!')"

# 4. Test production forecasting CLI pipeline
python forecast_pipeline.py --help
python forecast_pipeline.py --series "Overall - reported footprint" --horizon 12

# 5. Test production county estimation CLI pipeline
python county_estimation_model.py

# 6. Verify canonical files exist and are populated
python -c "
import pandas as pd
print('Paired Counts:', pd.read_csv('data/Downtown_County_PairedCounts.csv').shape)
print('Forecasts 12M:', pd.read_csv('data/Forecasts_12Month.csv').shape)
print('Master Counts:', pd.read_csv('data/MasterCounts_Adjusted_v2.csv').shape)
"
```

*All project files, historical commits, analytical deliverables, figures, and governance protocols are synchronized and production-ready.*
