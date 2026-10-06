# Downtown San Diego Homeless Population Analysis
**Project Context, Historical Log & AI Assistant Memory File**

> **Note for AI Assistant:**  
> When starting a new session or chat, read this file first. It contains the complete project context, URLs, account credentials/profiles, data schemas, historical findings, and the status of all completed and upcoming tasks. Do not re-run past tasks or ask redundant questions covered here.

---

## 1. Project Overview & Team

* **Project Title:** Downtown San Diego Homeless Population Analysis
* **Organization / Context:** Data Science Alliance (Volunteer / Public Interest Analytics)
* **Analyst / Assignee:** Kyaw Soe Lwin (`kylwin@ucsd.edu` / `kslwin.2000@gmail.com`)
* **Project Lead / Manager:** Adir Mancebo Jr. (`adir@datasciencealliance.org` via `ucsd.edu`)
* **Goal:** Analyze unsheltered homelessness in Downtown San Diego using monthly count data from the Downtown San Diego Partnership (2017–present) disaggregated by neighborhood and East Village sub-area. The ultimate objective is producing time-series forecasts, geospatial hotspot analysis, and policy impact assessments to guide service providers and municipal agencies.

---

## 2. Essential Links & Environments

* **Asana Project Workspace:**  
  [Downtown San Diego Homeless Population Analysis - Asana](https://app.asana.com/1/1211227519522850/project/1218064298575500/list)  
  *(Project Notebook tab contains full curriculum guidelines).*
* **Google Drive - Shared Deliverables Folder:**  
  [Shared Deliverables Folder (UC San Diego Account /u/2/)](https://drive.google.com/drive/u/2/folders/1LUWFhKsbER-XSY8VJFVdt0cgVeuaQ6Ek)
* **Google Drive - Assignment 1 Subfolder:**  
  [Assignment 1 - Data Validation, Cleaning & Standardization](https://drive.google.com/drive/u/2/folders/1qkwbmPe87IRlsnm1cJMub5NNMsWvukLH)
* **Google Drive - Assignment 2 Subfolder:**  
  [Assignment 2 - Exploratory Data Analysis](https://drive.google.com/drive/folders/1DNw_C0_HmjRWqwFFUE4aTTYQ9NNswiC1)
* **Google Drive - Assignment 3 Subfolder:**  
  [Assignment 3 - Block-Level Validation & Spatial Integration](https://drive.google.com/drive/folders/1Sj6Ly7BYi_nw69Tyix0IpHKUNyhTbBnm)
* **Google Drive - Assignment 4 Subfolder:**
  [Assignment 4 - Time Series Decomposition & Pattern Analysis](https://drive.google.com/drive/folders/1qQswTqrbEV1YW4NDTXOPVlbUmfDv9BxI)
* **Source PDF Archive (Downtown San Diego Partnership):**  
  [DSDP Clean & Safe Unhoused Care Reports](https://downtownsandiego.org/clean-and-safe/unhoused-care/)
* **Local Project Root:** `D:\Projects\Downtown-Homeless-Analysis\`
* **Python Environment:** Python 3.13 (`pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `pypdf`, `pymupdf`, `shapely`, `PIL`, `cv2`, `statsmodels`, `scikit-learn`, `xgboost`, `prophet`+`cmdstanpy` (added Task 7.2) installed).

---

## 3. The 10-Assignment Roadmap

| Assignment | Title | Status | Primary Focus |
| :---: | :--- | :---: | :--- |
| **1** | **Data Validation, Cleaning & Standardization** | **COMPLETED (100% - Tasks 1.1–1.4)** | Source audit, schema standardization, methodology fixes, data dictionary, methodology log, quality report. |
| **2** | **Exploratory Data Analysis (EDA)** | **COMPLETED (100% - Tasks 2.1-2.3)** | Descriptive stats, multi-year trends, visualizations, presentations. |
| **3** | **Block-Level Validation & Spatial Integration** | **COMPLETED (100% - Tasks 3.1-3.4 done)** | Validate digitized block counts against 12 PDF maps, fix unbalanced spatial panel, reconcile coverage table. |
| **4** | **Time Series Decomposition & Pattern Analysis** | **COMPLETED (100% - Tasks 4.1-4.4 done)** | Trend/seasonal/residual decomposition, structural breaks, stationarity tests. |
| **5** | **Geospatial Hotspot Analysis** | **COMPLETED (100% - Tasks 5.1-5.4 done)** | Getis-Ord Gi*, Moran's I, spatial clustering on `Downtown_BlockGrid.geojson`. |
| **6** | **Methodology Impact Assessment** | **COMPLETED (100% - Tasks 6.1-6.3 done)** | Quasi-experimental policy evaluation, continuous weighting models. |
| **7** | **Forecasting Model Development** | **COMPLETED (100% - Tasks 7.1-7.4 done)** | ARIMA, SARIMA, Prophet, Gradient Boosting models, production CLI pipeline. |
| **8** | **County-Level Estimation Model** | **COMPLETED (100% - Tasks 8.1–8.4 done)** | Ratio modeling with Regional Task Force on Homelessness (RTFH) PIT counts. |
| **9** | **Interactive Dashboard & Strategic Synthesis** | **COMPLETED (100% - Tasks 9.1–9.4 done)** | Streamlit interactive web dashboard, technical reports, presentation decks, operational runbooks. |
| **10** | **Multi-Source Predictive System** | **COMPLETED (100% - Tasks 10.1–10.4 done)** | Ingesting weather, 311 service calls, shelter censuses, ensemble modeling, automated anomaly alerts. |

---

## 4. Work Completed to Date

### **Task 1.1: Validate delivered count data against source reports** (COMPLETED)
* **Sampling:** Drew a reproducible 45-cell stratified random sample (`sample_45_verification.csv`, seed 42) across 2017–2025.
* **Source Check:** Downloaded 32 official DSDP monthly PDFs to `data/pdfs/`.
* **Audit Results:** 40 exact matches out of 41 published cells audited (**2.44% published error rate**, **97.56% fidelity**). 4 cells represent unreleased late-2025 counts (`NaN`).
* **Major Discoveries:**
  1. **`"Core"` Label Resolution:** `"Core"` is an empirical alias for **`City Center`** (not Gaslamp). It was used in 2017–2018, transitioned in Q1 2019, and retired after March 2019. Gaslamp co-exists as an independent neighborhood across all 9 years.
  2. **2019 East Village Duplication Bug:** Discovered that **all 48 sub-area rows in 2019 are 100% identical duplicates of 2020 counts**, causing severe negative discrepancies against true 2019 East Village totals (up to $-206$).
  3. **February 2018 Source Error:** Identified a $+30$ addition error ($504$ sub-area sum vs. $474$ reported) that originated directly inside DSDP's own published PDF table.
  4. **April 2025 Discrepancy:** South East EV reported as 43.0 in CSV vs. 27.0 in DSDP preliminary breakout table.
* **Deliverable Created & Uploaded:**  
  * Local: [`DataValidation_SourceCheck.md`](file:///D:/Projects/Downtown-Homeless-Analysis/DataValidation_SourceCheck.md)
  * Google Drive: [DataValidation_SourceCheck (Google Doc)](https://docs.google.com/document/d/1-9NQme-RdocLOqhGPTfUQRoIm_3bJnX0LlqzhL03_As/edit) placed in `Assignment 1` folder.

---

### **Task 1.2: Resolve schema and label inconsistencies across all files** (COMPLETED)
* **Null Handling in `BlockLevel_Counts.csv`:** Found single null at row index 930 (`16TH_ST_C_ST` on `2020-01-31`). Audited block across all 11 other dates (always 0). Imputed `0` and cast `tents_structures` to `int64`.
* **Quote Cleaning:** Stripped literal quotes from `count_date` (`"""2018-01-24"""` $\rightarrow$ `2018-01-24`).
* **Crosswalk Built:** Created [`Neighborhood_Crosswalk.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Neighborhood_Crosswalk.csv) mapping 18 variants (`Core`, `East Village South`, `South East Village`, `Barrio Logan`, `Golden Hill`, `Sherman Heights`) to canonical parents.
* **Standardized Dates:** Converted irregular month names (`June`, `July`, `Sept`) to standard 3-letter codes (`Jun`, `Jul`, `Sep`) and added ISO time series column `date` (`YYYY-MM-01`).
* **Cleaned Datasets Uploaded to Drive:**
  1. `Neighborhood_Crosswalk.csv`
  2. `RawCounts_AllYears_clean.csv` (2,814 rows)
  3. `MasterCounts_Adjusted_clean.csv` (2,814 rows)
  4. `BlockLevel_Counts_clean.csv` (3,737 rows, 0 nulls, integer types)
  5. `BlockMap_Coverage_clean.csv` (843 rows)
  6. `Downtown_BlockGrid_clean.csv` (382 blocks)

---

### **Task 1.3: Reconcile the methodology adjustment logic** (COMPLETED)
* **Core Problem Resolved:** In `MasterCounts_Adjusted.csv`, `total_count` was set strictly equal to `raw_count` for all `component == 'total'` rows. Adjusted totals had never been rebuilt from the adjusted components.
* **Multiplier Audit:** Empirical multipliers across all 1,722 component rows were verified against the documented schedule ($1.0\times$ individual, $1.75\times$ tent, $1.66\times$ APR2017 vehicle, $2.03\times$ MAY2018/POST2020 vehicle) with **100.0% fidelity**.
* **Rebuilt Canonical Dataset:** For all 544 area-months with components, recomputed:
  $$\text{total\_count} = \text{round}\Big(\text{total\_count}_{\text{individual}} + \text{total\_count}_{\text{tent}} + \text{total\_count}_{\text{vehicle}},\, 2\Big)$$
  Preserved `total_count = raw_count` for 548 rows lacking component breakdowns (18 PRE2017 rows, 384 sub-areas, 60 Outside Perimeter, 54 late-2017, and 2 missing 2021 breakouts).
* **Discrepancy Quantification:** 517 rows (95.0%) match published totals within $\pm 2.0$ (rounding). 27 rows (5.0%) with diff $> 2.0$ were individually cataloged and attributed to source PDF layout errors and preliminary release divergences.
* **Deliverables Created & Uploaded:**
  * Canonical dataset: [`data/MasterCounts_Adjusted_v2.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/MasterCounts_Adjusted_v2.csv) (2,814 rows, uploaded to Google Drive).
  * Technical report: [`Task1.3_Methodology_Reconciliation_Report.md`](file:///D:/Projects/Downtown-Homeless-Analysis/Task1.3_Methodology_Reconciliation_Report.md).

---

### **Task 1.4: Produce data dictionary, methodology log, and quality report** (COMPLETED)
* **Local Documentation Suite:** Created 3 technical markdown specifications in `docs/`:
  1. [`docs/DataDictionary_MasterCounts.md`](file:///D:/Projects/Downtown-Homeless-Analysis/docs/DataDictionary_MasterCounts.md): Comprehensive metadata covering all 6 delivered datasets (`MasterCounts_Adjusted_v2.csv`, `RawCounts_AllYears_clean.csv`, `BlockLevel_Counts_clean.csv`, `BlockMap_Coverage_clean.csv`, `Downtown_BlockGrid_clean.csv`, `Neighborhood_Crosswalk.csv`) with variable descriptions, datatypes, valid ranges, and notes.
  2. [`docs/MethodologyChangeLog.md`](file:///D:/Projects/Downtown-Homeless-Analysis/docs/MethodologyChangeLog.md): Chronological audit of the 4 methodology regimes (PRE2017, APR2017, MAY2018, POST2020), multiplier evolution ($1.75$ tent, $1.66$ vs $2.03$ vehicle), and the January 2020 divergence (RTFH stopped applying multipliers for HUD PIT; DSDP Clean & Safe continued applying them for longitudinal operational continuity).
  3. [`docs/DataQualityReport.md`](file:///D:/Projects/Downtown-Homeless-Analysis/docs/DataQualityReport.md):
     - **Scope Correction:** Delivered counts begin January 2017 (`2017-01-01`), not 2012 as originally scoped.
     - **Root-Cause Accounting for 134 Nulls:** 116 in 2025 (unreleased counts for Jul, Aug, Oct, Nov; true reporting lag) and 18 in Nov 2018 (published headline totals exist, but PDF omitted component table; source extraction gap).
     - **Annual Row Counts:** 72 in 2017; 336/yr in 2018–2020; 342 in 2021; 348/yr in 2022–2025 (2,814 total rows).
     - **Peer Review Protocol:** Recapped 45-cell audit (97.56% fidelity) and established a 4-step random sampling protocol for team members.
* **Published Google Docs in Shared Drive:**
  1. `DataDictionary_MasterCounts`: [Google Doc](https://docs.google.com/document/d/19xO_IhrTi8pQw2a4VNay0CXN2CJENqu0PQzmWnV8qOo/edit)
  2. `MethodologyChangeLog`: [Google Doc](https://docs.google.com/document/d/1oDj2KhdTS6eEuU3RxWYtBqjr79ygKTV2-O39Adc7ksI/edit)
  3. `DataQualityReport`: [Google Doc](https://docs.google.com/document/d/1E4iSf5QynufvJ-_9rH2qQSmlNFeIoE4EOhK0qzTHYg8/edit)
* **Asana Sign-off:** Posted detailed completion summary to Adir Mancebo Jr. and checked off Task 1.4 as Completed.

---

### **Task 2.1: Generate summary statistics and temporal patterns** (COMPLETED)
* **Notebook Built:** [`EDA_DowntownCounts.ipynb`](file:///D:/Projects/Downtown-Homeless-Analysis/EDA_DowntownCounts.ipynb), constructed programmatically (`nbformat`) and executed headlessly end-to-end (`jupyter nbconvert --execute`) with zero errors.
* **Scoping Decision:** `MasterCounts_Adjusted_v2.csv` is long-format (up to 4 rows per area-month: `total`, `individual`, `vehicle`, `tent` components). Filtered to `component == 'total'` **and** `area_type == 'neighborhood'` (708 rows across 7 neighborhoods) for headline analysis, excluding the 4 East Village sub-areas to avoid double-counting against the `East Village` parent row.
* **Summary Statistics:**
  * Overall (all neighborhoods, all months, 2017–2025): mean **156.78**, median **58.88**, min **0.0**, max **921.05**, std **197.38** (highly right-skewed — driven by East Village).
  * By neighborhood (mean, sorted): East Village 552.77 → Outside Perimeter 217.57 → City Center 171.81 → Cortez 59.52 → Gaslamp 48.43 → Columbia 44.49 → Marina 30.94.
* **Monthly Seasonality:** Overall variation is modest (range ~148.7–161.8). Highest months: **Feb (161.76), Aug (161.61), May (160.93)**. Lowest months: **Mar (148.67), Nov (153.43), Apr (153.53)**. Neighborhood heatmap shows East Village peaks in Jul–Aug (~601–604) and dips in spring (Mar–Apr, ~509), a distinct pattern from the overall trend.
* **Year-over-Year % Change (overall, avg monthly count by year):**
  | Year | Avg Count | YoY % |
  |---|---|---|
  | 2017 | 176.31 | — |
  | 2018 | 142.84 | −18.98% |
  | 2019 | 135.79 | −4.94% |
  | 2020 | 109.02 | −19.71% (COVID low) |
  | 2021 | 137.20 | +25.85% |
  | 2022 | 216.27 | +57.63% |
  | 2023 | 223.98 | +3.56% (peak) |
  | 2024 | 126.50 | −43.52% |
  | 2025 | 122.78 | −2.94% |
* **Top 3 Neighborhoods:**
  * By average count: East Village, Outside Perimeter, City Center.
  * By average YoY growth rate (2019+, excluding partial 2017/2018 transition): **Outside Perimeter (+26.90%)**, **Cortez (+11.96%)**, **City Center (+3.94%)**. Notably diverges from the size ranking — Marina (−12.76%) and Columbia (−4.28%) are shrinking despite mid-pack magnitude.
* **Data Quality Caveat Logged:** Outside Perimeter has only 56 observations (partial reporting coverage starting ~2022); 28 nulls remain in the neighborhood-level `total_count` slice (2025 unreleased months, consistent with `docs/DataQualityReport.md`). YoY figures for 2022/2025 in that area should be read cautiously.
* **Deliverable:** [`EDA_DowntownCounts.ipynb`](file:///D:/Projects/Downtown-Homeless-Analysis/EDA_DowntownCounts.ipynb) — not yet uploaded to Google Drive (pending Task 2.2/2.3 completion for a combined EDA upload).

---

### **Task 4.1: Perform time series decomposition** (COMPLETED)
* **Notebook Built:** [`TimeSeries_Decomposition.ipynb`](file:///D:/Projects/Downtown-Homeless-Analysis/TimeSeries_Decomposition.ipynb), built programmatically via `build_timeseries_decomposition.py` and executed end-to-end (8/8 code cells, 13 outputs, 0 errors — independently re-verified in a clean process).
* **Scope:** `component == 'total'` & `area_type == 'neighborhood'` rows from `MasterCounts_Adjusted_v2.csv` (708 rows validated, 0 duplicate area-month keys). Nine analysis series: Overall (reported footprint), Overall (fixed-core-six, excludes `Outside Perimeter`), and all 7 individual neighborhoods.
* **Methods:** Additive classical decomposition and robust STL (12-month seasonal period) applied to every series. Four unreleased 2025 months (Jul, Aug, Oct, Nov) were linearly interpolated **in memory only** for decomposition — source CSV confirmed unchanged (`git diff` clean).
* **Event annotations:** April 2017 and May 2018 methodology-multiplier changes, March 2020 COVID-19 onset — plotted as reference lines on every decomposition (except `Outside Perimeter`, whose reporting starts Jan 2021, after all three events). The May source report is dated May 31; the canonical monthly label is May 1.
* **Key finding:** Overall reported-footprint series has a low STL seasonal strength (near zero), meaning irregular/residual variation dominates any recurring monthly pattern at the aggregate level — this motivated the deeper significance testing in Task 4.2.
* **Deliverable:** [`TimeSeries_Decomposition.ipynb`](file:///D:/Projects/Downtown-Homeless-Analysis/TimeSeries_Decomposition.ipynb), `build_timeseries_decomposition.py`. Uploaded to Google Drive: [TimeSeries_Decomposition.ipynb](https://drive.google.com/file/d/1JxGhf9Xy6GrwyrRf-roYKNBeoLIO1fo_/view). Completed and approved in Asana.

---

### **Task 4.2: Quantify seasonal patterns with statistical significance tests** (COMPLETED)
* **Notebook Built:** [`SeasonalPatterns_Analysis.ipynb`](file:///D:/Projects/Downtown-Homeless-Analysis/SeasonalPatterns_Analysis.ipynb), built via `build_seasonal_indices.py`, executed end-to-end (9/9 code cells, 0 errors).
* **Method:** Reconstructed the same 9 Task 4.1 series, de-trended each via the same robust-STL fit (`detrended = observed − STL trend`). For each series × calendar month: seasonal index = mean de-trended value; 95% CI via t-distribution; per-month significance via one-sample t-test against 0 with Cohen's d effect size. Series-level seasonality tested via Kruskal-Wallis (primary) and one-way ANOVA (secondary) across the 12 month groups.
* **Key finding:** 8 of 9 series show **no statistically significant seasonality** after de-trending (Kruskal-Wallis, α=0.05) — including the overall reported-footprint series (H=3.00, p=0.99) and East Village (H=13.86, p=0.24), despite East Village's raw Jul–Aug bump noted in Task 2.1's EDA. Once trend is removed, that bump is not statistically distinguishable from noise across the ~9 years of data. **Marina** is the one series Kruskal-Wallis flags as significant (H=20.15, p=0.043; individually-significant month: Aug, d=0.83, p=0.037) — though its companion ANOVA test disagrees (p=0.146), a discrepancy reported transparently rather than resolved by cherry-picking.
* **Deliverable:** [`data/SeasonalIndices.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/SeasonalIndices.csv) (108 rows = 9 series × 12 months, 17 columns: index, 95% CI, per-month t-test/effect size, series-level Kruskal-Wallis/ANOVA). `SeasonalPatterns_Analysis.ipynb` and `build_seasonal_indices.py` kept in repo for QC/reproducibility (only the CSV was required as the Drive deliverable per the task spec).

---

### **Task 4.3: Conduct structural break analysis** (COMPLETED)
* **Notebook Built:** [`StructuralBreak_Analysis.ipynb`](file:///D:/Projects/Downtown-Homeless-Analysis/StructuralBreak_Analysis.ipynb), built via `build_structural_break_analysis.py`, executed end-to-end (0 errors).
* **Break-date resolution:** the two methodology dates are derived programmatically from the canonical `method` column; COVID is supplied explicitly. The `MAY2018` source report is dated May 31, while the monthly dataset normalizes it to **2018-05-01**. Task 4.1's former June 1 annotation was corrected to the canonical month label.
* **Method:** dummy-variable Chow test `y = β0 + β1·τ + β2·D + β3·(D·τ) + ε`. The joint F-test is primary; coefficient t-tests are descriptive mechanism labels and allow an indeterminate category. Added within-event Benjamini–Hochberg FDR values and HAC(12) serial-correlation sensitivities. The supplementary routine is correctly identified as an OLS-residual CUSUM, not CUSUM-of-squares.
* **April 2017:** only 3 pre-break months exist. The reduced level-shift intervention model and Columbia detection (p=0.001; FDR p=0.006) are explicitly **exploratory**, not confirmatory; robust inference is withheld.
* **May 2018:** 5 of 8 classical results survive within-event FDR; 4 also pass HAC(12), with fixed-core-six the exception. The matching raw-count pattern shows multiplier arithmetic is not the sole explanation, but does not prove behavioral causality or eliminate counting/reporting confounds.
* **COVID-19:** 7 of 8 classical results, 5 after within-event FDR. HAC(12) flags a different seven-series set (City Center enters, Marina drops), so borderline membership is model-sensitive. Marina's classical joint result is mechanistically indeterminate because neither component is individually significant.
* **OLS-residual CUSUM:** 7 of 9 series remain significant after FDR; Gaslamp and Marina do not. The discrepancy with targeted Chow results is reported as unresolved, without asserting an untested explanation.
* **Additional sensitivity:** dropping instead of interpolating the four unreleased 2025 months leaves all 24 classical targeted significance calls unchanged.
* **Deliverables:** [`data/StructuralBreaks.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/StructuralBreaks.csv) remains 57 rows (40 `chow_full` + 8 exploratory `chow_level_only` + 9 `cusum`) and adds FDR/HAC audit columns; [`StructuralBreak_Analysis.ipynb`](file:///D:/Projects/Downtown-Homeless-Analysis/StructuralBreak_Analysis.ipynb), `build_structural_break_analysis.py`, and [`StructuralBreak_Analysis.md`](file:///D:/Projects/Downtown-Homeless-Analysis/StructuralBreak_Analysis.md) contain the corrected analysis. [StructuralBreak_Analysis (Google Doc)](https://docs.google.com/document/d/1tOdyHRUOS_5eJZPamNojASwffal8b2B0gON4UXHwpfE/edit) was updated and verified saved in the UCSD Assignment 4 folder; the corrected Task 4.1 notebook was uploaded as a new version of its existing Drive file.

---

### **Task 4.4: Test stationarity and document autocorrelation structure** (COMPLETED)
* **Notebook Built:** [`Stationarity_Autocorrelation.ipynb`](file:///D:/Projects/Downtown-Homeless-Analysis/Stationarity_Autocorrelation.ipynb), built via `build_stationarity_autocorrelation.py` and executed end-to-end (10/10 code cells, 0 errors). The canonical source SHA-256 is checked before and after execution and remains unchanged.
* **Scope and tests:** Reconstructed the same nine Assignment 4 series for both methodology-adjusted `total_count` and `raw_count`. ADF (autolag AIC) and KPSS (automatic bandwidth) were run on adjusted levels, raw-count sensitivity levels, selected forecasting transformations, and a pre-first-gap sensitivity. Consensus stationarity requires ADF p < 0.05 and KPSS p > 0.05.
* **Stationarity result:** none of the nine adjusted level series reaches paired-test consensus. City Center and Marina are consensus nonstationary; the other seven have mixed evidence. The raw-count sensitivity has the same 2-versus-7 classification pattern. First differencing is the minimum successful treatment for the two aggregates plus East Village, City Center, Columbia, Marina, Cortez, and Gaslamp. Outside Perimeter reaches consensus after a `log1p` level transformation. All nine calls remain consensus stationary when truncated before the first unreleased 2025 month.
* **Autocorrelation result:** the reported-footprint aggregate and East Village do not reject the Ljung-Box white-noise null at lags 12 or 24 after transformation. The fixed-core-six aggregate, City Center, Columbia, Marina, Gaslamp, and Outside Perimeter retain significant dependence; Cortez is borderline at lag 24 (p=0.062). ACF/PACF screening suggests nonseasonal starting orders ranging from ARIMA(0,1,0) for the reported-footprint benchmark to ARIMA(2,1,1) for several neighborhoods and ARMA(1,2) on the `log1p` scale for Outside Perimeter. No automatic seasonal AR/MA term is selected from lag-12 significance. These are Task 7 starting values, not final models.
* **Forecasting handoff:** [`data/AdjustedTimeSeries_Forecasting.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/AdjustedTimeSeries_Forecasting.csv) contains 916 unique, non-null series-date rows with original/stationary values, transformation metadata, `d`/`D`, interpolation and dependency flags, paired-test p-values, and screened orders. Supporting outputs are [`data/StationarityTests.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/StationarityTests.csv), [`data/AutocorrelationDiagnostics.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/AutocorrelationDiagnostics.csv), and nine figures in `figures/task4_4/`.
* **Technical report and Drive:** [`TimeSeries_TechnicalReport.md`](file:///D:/Projects/Downtown-Homeless-Analysis/TimeSeries_TechnicalReport.md) mirrors the polished five-page [TimeSeries_TechnicalReport Google Doc](https://docs.google.com/document/d/1KqMnJYyLvVzu3_7XqeNljCzfXUNHF6R1SQqEZJk0Xwo/edit). The native Doc, notebook, forecasting CSV, stationarity table, and autocorrelation diagnostics were uploaded to the UCSD Assignment 4 folder. The native Google Doc was exported to PDF, rasterized to five page images, and visually inspected; tables, figures, headings, and page breaks render cleanly with no clipping or overlap.

---

### **Task 5.1: Prepare spatial datasets and test global spatial autocorrelation** (COMPLETED)
* **Script Built:** [`build_spatial_autocorrelation.py`](file:///D:/Projects/Downtown-Homeless-Analysis/build_spatial_autocorrelation.py), executed end-to-end (0 errors).
* **Method:** Joined `BlockPanel_Balanced_261.csv` / `BlockLevel_Counts_clean.csv` to `Downtown_BlockGrid.geojson` on `block_id`. Two scopes analyzed separately to avoid confounding the 2022 footprint expansion with a real spatial change: `balanced_261` (12 dates, 2018–2025, 261 fixed blocks per Task 3.3) and `full_382_recent` (5 dates, 2022–2025, all 382 blocks). Outcome variable: DSDP methodology-adjusted count (`individuals + 1.75×tents_structures + vehicle_multiplier×vehicles`, vehicle multiplier 1.66 pre-June 2018 / 2.03 after). Queen-contiguity weights (GeoPandas/libpysal), row-standardized; global Moran's I (esda) with 9,999 permutations, fixed seed `20260910`.
* **Result:** All 17 evaluated date/scope combinations show positive, statistically significant global clustering (balanced panel I range 0.063–0.239, p ≤ 0.0328; full recent panel I range 0.143–0.243, p ≤ 0.0008). Confirms clustering exists but not which blocks — motivates Task 5.2's local Gi*.
* **Deliverables:** [`data/SpatialAnalysis_AnalysisReady.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/SpatialAnalysis_AnalysisReady.csv) (5,042 rows), [`data/SpatialWeights_Queen.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/SpatialWeights_Queen.csv) (2,642 directed queen-neighbor links), [`data/SpatialAutocorrelation_Results.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/SpatialAutocorrelation_Results.csv) (17 rows), `build_spatial_autocorrelation.py`, and [`SpatialAutocorrelation_Report.md`](file:///D:/Projects/Downtown-Homeless-Analysis/SpatialAutocorrelation_Report.md).

---

### **Task 5.2: Run local Getis-Ord Gi\* hotspot analysis** (COMPLETED)
* **Script Built:** [`build_hotspot_analysis.py`](file:///D:/Projects/Downtown-Homeless-Analysis/build_hotspot_analysis.py), executed end-to-end (0 errors).
* **Method:** All 12 dates use the fixed 261-block balanced panel (the 121 blocks added in 2022 are excluded from every time-comparative calculation, per Task 3.3's footprint warning). esda `G_Local` with `star=True`, queen contiguity, 9,999 conditional random permutations per date with a deterministic date-derived seed. Classified `hotspot_99` (z≥2.576, p<0.01), `hotspot_95` (z≥1.96, p<0.05), analogous cold-spot tiers, else `not_significant`.
* **Result:** Positive local clustering is concentrated in a small share of the fixed footprint in 11 of 12 dates (0–4 blocks at 95%, 0–4 at 99% per date); no cold spots reach the 95% threshold on any date. 2022-03-01 is retained but flagged — Task 3.1's source-map anomaly (inconsistent handwritten dates) applies to this count date.
* **Deliverables:** [`data/Hotspot_Classifications.geojson`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Hotspot_Classifications.geojson) (3,132 block-date features with Gi*, z-score, p-value, classification, adjusted count, geometry), [`data/Hotspot_Summary_ByDate.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Hotspot_Summary_ByDate.csv), `build_hotspot_analysis.py`, and [`Hotspot_Analysis_Report.md`](file:///D:/Projects/Downtown-Homeless-Analysis/Hotspot_Analysis_Report.md).

---

### **Task 5.3 & 5.4: Cartographic outputs, persistence ranking, contextual indicators, and migration pattern** (COMPLETED)
* **Script Built:** [`build_hotspot_maps_persistence.py`](file:///D:/Projects/Downtown-Homeless-Analysis/build_hotspot_maps_persistence.py), executed end-to-end (0 errors).
* **Maps:** 4 publication-quality PNGs in `figures/hotspot_maps/` (Map 1: hotspot-date-count by block; Maps 2/3: max Gi* classification in the early 2018–2020 vs. recent 2022–2025 periods, deliberately excluding 2021 to avoid treating the coverage transition as a period boundary; Map 4: `became hotspot` / `remained hotspot` / `cooled off` / `never hotspot` transition classification), combined into [`Hotspot_Maps_Export.pdf`](file:///D:/Projects/Downtown-Homeless-Analysis/Hotspot_Maps_Export.pdf), plus an interactive per-date explorer at [`Hotspot_Interactive.html`](file:///D:/Projects/Downtown-Homeless-Analysis/Hotspot_Interactive.html).
* **Persistence ranking:** All 261 balanced-panel blocks ranked by hotspot-date count out of 12 (ties broken by mean Gi* z-score, then mean adjusted count) in [`data/Hotspot_Persistence_Ranking.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Hotspot_Persistence_Ranking.csv). Top block `16TH_ST_IMPERIAL_AV` (South East Village) is a hotspot on 9/12 dates; all top-10 blocks are in South East Village, spatially compact rather than dispersed.
* **Contextual indicators:** Nearest homeless/social-service and transit features (OpenStreetMap via Overpass API, queried 2026-09-13) for the top 10 persistent blocks in [`data/Hotspot_Top10_Context.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Hotspot_Top10_Context.csv), raw context in [`data/OSM_Service_Transit_Context.geojson`](file:///D:/Projects/Downtown-Homeless-Analysis/data/OSM_Service_Transit_Context.geojson) — proximity indicators only, not capacity/eligibility/walkability measures.
* **Migration pattern:** The adjusted-count-weighted centroid of hotspot block-date records moved 121 m south from 2018–2020 to 2022–2025 ([`data/Hotspot_Migration_Centroids.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Hotspot_Migration_Centroids.csv), unweighted centroid included as a sensitivity check). Framed as a shift in the center of significant clusters, not a precise trend estimate (only 12 digitized dates; March 2022 anomaly).
* **Deliverable:** [`Hotspot_TechnicalReport.md`](file:///D:/Projects/Downtown-Homeless-Analysis/Hotspot_TechnicalReport.md) — full Assignment 5 completion report covering methods, map series, persistence/context, migration, and service-siting implications/limits.

---

### **Task 6.1: Quantify the impact of each methodology change** (COMPLETED)
* **Notebook Built:** [`MethodologyImpact_Analysis.ipynb`](file:///D:/Projects/Downtown-Homeless-Analysis/MethodologyImpact_Analysis.ipynb), built via `build_methodology_impact.py` and executed end-to-end (0 errors). The canonical source `data/MasterCounts_Adjusted_v2.csv` and Task 4.3's `data/StructuralBreaks.csv` are hash-checked before and after execution and remain unchanged.
* **Method:** for each of the two DSDP multiplier changes (April 2017: tent 2.00→1.75, vehicle 2.00→1.66; May 2018: vehicle 1.66→2.03), computed a **theoretical** expected count change per neighborhood from a 4-month tent/vehicle/individual composition window times the multiplier delta, with a paired 95% t-interval (n=4, exploratory). Compared against the **observed** count change, read directly from Task 4.3's Chow `level_shift` coefficient (`chow_level_only` at April, `chow_full` at May) rather than recomputed, to keep the two sides independent. Verified the documented multiplier table against `total_count/raw_count` before use.
* **⚠️ April 2017 data limitation:** zero tent/vehicle/individual component data exists anywhere before January 2018 — 9 months after the true April 2017 break. Per an explicit project decision, Jan–Apr 2018 is used as an imperfect proxy for April-2017-regime composition; the April theoretical estimate is illustrative, not measured. This is a strictly worse sparsity problem than Task 4.3 flagged for the same date (3 pre-break aggregate months there vs. 0 component months here). May 2018 needed no proxy — real pre/post composition data exists on both sides of that break.
* **Result:** theoretical estimates are small relative to the much larger observed level shifts at both dates and frequently disagree in sign with the observed change (most starkly at May 2018, where every neighborhood's theoretical change is positive but every observed level shift is negative) — meaning the two breaks' observed count changes are driven mostly by real change, not by multiplier arithmetic alone. Composition (tent+vehicle share for April, vehicle share alone for May) does explain the *relative ranking* of theoretical impact across neighborhoods (East Village highest both times; Gaslamp/City Center zero where tent or vehicle presence is zero).
* **Deliverables:** [`data/MethodologyImpact_Composition.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/MethodologyImpact_Composition.csv) (72 rows), [`data/MethodologyImpact_TheoreticalVsObserved.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/MethodologyImpact_TheoreticalVsObserved.csv) (14 rows), `build_methodology_impact.py`, and [`MethodologyImpact_Analysis.md`](file:///D:/Projects/Downtown-Homeless-Analysis/MethodologyImpact_Analysis.md). Uploaded as [Methodology_ImpactAnalysis (Google Doc)](https://docs.google.com/document/d/1D2iUuHdF8YQUgPK2SVSb-huYrsvf8IUN5sKyMOxLX40/edit) to the newly created [Assignment 6 - Methodology Impact Assessment Drive folder](https://drive.google.com/drive/folders/1yEP2_tRowv4LcyNcQTBzthEalt-37KcJ) via the Google Drive MCP tool (converted from Markdown; headings/tables/bold rendered correctly, verified via `read_file_content`).

---

### **Task 6.2: Develop data-derived adjustment factors** (COMPLETED)
* **Notebook Built:** [`TimeSeries_ConstantMethodology.ipynb`](file:///D:/Projects/Downtown-Homeless-Analysis/TimeSeries_ConstantMethodology.ipynb), built via `build_adjustment_factors.py` and executed end-to-end (0 errors). `data/MasterCounts_Adjusted_v2.csv` and Task 6.1's `data/MethodologyImpact_Composition.csv` are hash-checked before and after execution and remain unchanged.
* **Method:** computed **observed** count ratios using the literal calendar-adjacent months at each break (March→April 2017; April→May 2018) and **theoretical** composition-weighted multiplier ratios (April: Task 6.1's Jan–Apr 2018 proxy composition; May: a real, single-month April 2018 composition) — then compared the two and selected the theoretical ratio as the basis for the applied adjustment factor.
* **⚠️ April 2017 data artifact:** verified live that `total_count == raw_count` for every neighborhood-month before 2018-01-01 — the literal adjacent-month observed ratio for April 2017 therefore carries zero multiplier signal by construction, not evidence of a small effect. Combined with Task 6.1's prior finding that both breaks' observed changes are dominated by real change, this is why the theoretical ratio (not the observed ratio) was selected to build the applied factor.
* **Result:** rescaled `total_count` onto the POST2020 (contemporary, individual 1.00/tent 1.75/vehicle 2.03) baseline — exact per-row factors for 2018-01–2018-04 rows with real component data (assert-verified to reconstruct `total_count` exactly), proxied per-neighborhood factors (reusing Task 6.1's Jan–Apr 2018 composition) for pre-2018 PRE2017/APR2017 rows, and factor=1.0 for all MAY2018/POST2020-regime rows and `Outside Perimeter` throughout (it only ever reports under POST2020).
* **Deliverables:** [`data/AdjustmentFactors_RatioComparison.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/AdjustmentFactors_RatioComparison.csv) (14 rows), [`data/TimeSeries_ConstantMethodology.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/TimeSeries_ConstantMethodology.csv) (924 rows, 9 series), `build_adjustment_factors.py`, and [`TimeSeries_ConstantMethodology.md`](file:///D:/Projects/Downtown-Homeless-Analysis/TimeSeries_ConstantMethodology.md). Uploaded to the same [Assignment 6 Drive folder](https://drive.google.com/drive/folders/1yEP2_tRowv4LcyNcQTBzthEalt-37KcJ): report as a Google Doc, CSV as a native Google Sheet.

---

### **Task 6.3: Compare adjustment approaches and issue forecasting recommendations** (COMPLETED)
* **Script Built:** [`build_adjustment_approach_comparison.py`](file:///D:/Projects/Downtown-Homeless-Analysis/build_adjustment_approach_comparison.py), executed end-to-end (0 errors). `data/MasterCounts_Adjusted_v2.csv`, `data/AdjustmentFactors_RatioComparison.csv`, and `data/TimeSeries_ConstantMethodology.csv` are hash-checked before and after execution and remain unchanged.
* **Method:** built 3 alternative constant-methodology series for the pooled fixed-core-six neighborhoods — **theoretical multipliers only** (compounds both breaks' Task 6.1/6.2 composition-weighted theoretical ratios uniformly), **data-derived only** (compounds the literal calendar-adjacent-month observed ratios), and **hybrid** (Task 6.2's already-selected, reviewed series: exact per-row reconstruction for the 16 real-data months, theoretical proxy elsewhere) — then compared all three against raw reported counts.
* **Result:** data-derived-only is confirmed unusable as a standalone adjustment (pre-2020 pooled mean +6.1% vs. raw, driven by real-change contamination per Task 6.1's sign-mismatch finding); theoretical-only and hybrid track raw closely and each other (+0.66% / +0.74% pre-2020 pooled mean gap). **Recommendation: use the hybrid series** for forecasting inputs, with one documented scope caveat (it does not compound the May 2018 correction onto the Apr 2017–Apr 2018 window). January 2020 (RTFH/DSDP divergence) requires no further adjustment to this project's DSDP-sourced series — the risk is cross-source comparison against raw HUD PIT figures, not this series in isolation.
* **Deliverables:** [`data/AdjustmentApproach_Comparison.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/AdjustmentApproach_Comparison.csv) (324 rows, 3 approaches × raw), [`data/AdjustmentApproach_SummaryStats.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/AdjustmentApproach_SummaryStats.csv), 4 comparison figures in [`figures/adjustment_approach_comparison/`](file:///D:/Projects/Downtown-Homeless-Analysis/figures/adjustment_approach_comparison/), `build_adjustment_approach_comparison.py`, and [`MethodologyAdjustment_RecommendationsMemo.md`](file:///D:/Projects/Downtown-Homeless-Analysis/MethodologyAdjustment_RecommendationsMemo.md). Uploaded to the same [Assignment 6 Drive folder](https://drive.google.com/drive/folders/1yEP2_tRowv4LcyNcQTBzthEalt-37KcJ): memo as [MethodologyAdjustment_RecommendationsMemo (Google Doc)](https://docs.google.com/document/d/1WpasSrKHb_FISwsI9EC5gFInYigP0cNzs1QbkHROr04/edit), comparison CSV as [AdjustmentApproach_Comparison (Google Sheet)](https://docs.google.com/spreadsheets/d/1QSAKRaMRnw2RSCd-6Pwjj6v6jf_2kRoilAEUGYKOGIo/edit).

---

### **Task 7.1: Prepare data and establish baseline models** (COMPLETED)
* **Notebook Built:** [`Forecasting_Models.ipynb`](file:///D:/Projects/Downtown-Homeless-Analysis/Forecasting_Models.ipynb), built via `build_forecasting_models.py` and executed end-to-end (0 errors). `data/AdjustedTimeSeries_Forecasting.csv` and `data/TimeSeries_ConstantMethodology.csv` are hash-checked before and after execution and remain unchanged.
* **Method:** reconstructed all 9 Assignment 4/6 series from both forecasting handoff files — the published *adjusted* series (Task 4.4) and Task 6.3's *constant-methodology* hybrid series — carried forward side by side rather than picking one upfront. Train/test split: held out the most recent 12 calendar months (2025-01 to 2025-12) as test, trained on all prior data. Per Task 1.4's documented 2025 reporting gap (Jul, Aug, Oct, Nov unreleased), naive forecasts are still produced for those months for horizon continuity, but excluded from metric scoring (tracked via `n_excluded_unreleased`). Naive seasonal baseline: `forecast(t) = actual(t-12 months)`. Metrics: RMSE/MAE/MAPE computed as cumulative windows at 1/3/6/12-month horizons.
* **Result:** established the benchmark-to-beat for Task 7.2's model families. For the "Overall - reported footprint" series, naive-baseline MAPE ranges ~7-20% across horizons (best at longer horizons, since the 12-month cumulative window absorbs more observed months).
* **Deliverables:** [`data/Forecast_Baseline_NaiveSeasonal.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Forecast_Baseline_NaiveSeasonal.csv) (216 rows = 9 series × 12 test months × 2 variants), [`data/Forecast_BaselineMetrics.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Forecast_BaselineMetrics.csv) (72 rows), `build_forecasting_models.py`. Marked complete in Asana with a summary comment (no Drive upload yet — Assignment 7 Drive subfolder has not been created).

---

### **Task 7.2: Build and tune multiple model families** (COMPLETED)
* **Notebook Extended:** `Forecasting_Models.ipynb` extended in place (not a new notebook) via the same `build_forecasting_models.py`, executed end-to-end (0 errors, 38 cells total). Both source CSVs hash-checked unchanged twice (after Task 7.1's save, and again at the very end of Task 7.2).
* **Scope:** all 9 series, **constant-methodology variant only** (`constant_methodology_count`), per Task 6.3's explicit recommendation of the hybrid series for forecasting inputs; the published *adjusted* series remains the Task 7.1 baseline comparison and was not independently re-modeled. Same train/test split, horizon set, and cumulative-window RMSE/MAE/MAPE convention as Task 7.1.
* **Method — 4 model families, each fit per series on training data only, forecast 12 months ahead:**
  1. **SARIMA:** starting `(p,d,q)` per series reused from Task 4.4's ACF/PACF screening (`candidate_p/d/q` columns, derived on the adjusted series — an explicitly documented reuse assumption, not re-derived for the constant-methodology variant). Grid search `p,q` ±1 around the candidate × seasonal `(P,D,Q) ∈ {0,1}³` at period 12, selected by lowest AIC via `SARIMAX`.
  2. **Holt-Winters:** triple exponential smoothing, additive trend, additive vs. multiplicative seasonality compared by training-fit AIC (multiplicative skipped for `Outside Perimeter`, which has 3 zero-value training months).
  3. **Prophet:** yearly seasonality, changepoints fixed at 2017-04-01, 2018-05-01, and 2020-03-01 (the two DSDP methodology-multiplier changes plus COVID-19 onset), restricted to whichever fall inside each series' training range (`Outside Perimeter` starts 2021, so it uses Prophet's automatic changepoint detection instead).
  4. **XGBoost (optional ML approach):** lag features (1,2,3,6,12), rolling means (3,6,12), calendar-month sine/cosine, linear trend index; shallow `XGBRegressor` (100 estimators, depth 3) given ~110 monthly observations per series; recursive one-step-ahead forecasting through the 12-month test window.
* **Result:** pooled (mean-across-series) MAPE at the 12-month horizon: XGBoost 38.5% (best at every horizon), Holt-Winters 40.2%, SARIMA 42.3%, naive baseline 41.9%, Prophet 46.8% (worst). **Key finding:** on both headline series (`Overall - reported footprint`, `East Village`), Prophet's fixed-changepoint configuration visibly overshoots the entire 2025 test window (~250-650 count-units high) — because it has no changepoint near the 2022-2023 peak or the 2024-2025 decline documented in Task 2.1's YoY analysis, so its piecewise-linear trend keeps extrapolating an older upward segment forward. This is reported as-is (the task specified fixed changepoints) rather than re-tuned, and is flagged directly for Task 7.3's model-selection weighing.
* **Deliverables:** [`data/Forecast_ModelPredictions.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Forecast_ModelPredictions.csv) (540 rows = 9 series × 12 test months × 5 models incl. naive baseline), [`data/Forecast_ModelComparison.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Forecast_ModelComparison.csv) (180 rows = 9 series × 4 horizons × 5 models, includes a `hyperparameters` column per series/model), 2 QC figures in [`figures/task7_2/`](file:///D:/Projects/Downtown-Homeless-Analysis/figures/task7_2/). Uploaded to Google Drive (`Assignment 7 - Forecasting Model Development`) as Google Sheets; marked complete in Asana.

---

### **Task 7.3: Perform time-series cross-validation and select final model** (COMPLETED)
* **Backtesting Architecture Built:** `build_forecasting_cv.py` and extended in `Forecasting_Models.ipynb`. Executed end-to-end (0 errors). Both source CSVs hash-verified unchanged before and after execution.
* **Expanding Window Folds:** 5 chronological folds across 2017–2024 (96 months, zero future leakage into the 2025 hold-out test set):
  1. Fold 1: Train 2017–2020 (48 mo) $\rightarrow$ Test 2021 (Post-COVID Rebound)
  2. Fold 2: Train 2017–2021 (60 mo) $\rightarrow$ Test 2022 (Historic Surge)
  3. Fold 3: Train 2017–2022 (72 mo) $\rightarrow$ Test 2023 (All-Time Peak Volume)
  4. Fold 4: Train 2017–mid 2023 (78 mo) $\rightarrow$ Test 2023-H2 to 2024-H1 (Camping Ordinance Transition)
  5. Fold 5: Train 2017–2023 (84 mo) $\rightarrow$ Test 2024 (Enforcement Contraction)
* **Models Tested Across All 9 Series:** Naive Seasonal baseline ($t-12$), SARIMA (AIC-optimized), Holt-Winters (Triple Exp Smoothing), Prophet (historical changepoints), and XGBoost (recursive 12-step forecaster with lag, rolling, and Fourier features).
* **Cross-Validation Results (12-Month Horizon CV MAPE, Mean ± Std%):**
  * **Overall - reported footprint:** **XGBoost 39.34%** (±25.36%) [Winner] vs. Holt-Winters 39.57% (±27.55%), SARIMA 40.10% (±34.48%), Naive 51.34% (±24.52%), Prophet 63.81% (±35.45%).
  * **Overall - fixed core six:** **XGBoost 22.26%** (±9.47%) [Dominant Winner] vs. SARIMA 26.81%, Holt-Winters 29.48%, Naive 30.90%, Prophet 40.16%.
  * **East Village:** **XGBoost 34.55%** (±21.09%) [Winner] vs. SARIMA 37.94%, Holt-Winters 40.64%, Naive 41.28%, Prophet 52.08%.
  * **City Center:** **XGBoost 30.13%** (±15.11%) [Winner]. (SARIMA experienced a unit-root numerical explosion in Fold 1, demonstrating real-world fragility).
  * **Columbia:** **SARIMA 30.54%** (±17.22%) [Winner] vs. Holt-Winters 32.12%, Naive 40.78%, XGBoost 41.41%, Prophet 51.48%.
  * **Cortez:** **XGBoost 37.22%** (±17.69%) [Winner] vs. Prophet 39.78%, Naive 40.08%, Holt-Winters 44.26%.
  * **Gaslamp:** **Prophet 28.83%** (±9.99%) [Winner] vs. Holt-Winters 30.12%, XGBoost 31.56%, Naive 36.40%.
  * **Marina:** **Prophet 45.84%** (±11.90%) [Winner] vs. Holt-Winters 59.42%, XGBoost 74.01%, Naive 76.40%.
  * **Outside Perimeter:** **SARIMA 561.09%** [Lowest error on small baseline denominator; evaluated on Folds 3–5].
* **Champion Model Selection & Handoff to Task 7.4:**
  * **Citywide Headline Champion:** **XGBoost** selected based on lowest 12-month CV error (39.34%) and highest stability. Holt-Winters selected as secondary parametric baseline (39.57%) providing closed-form prediction intervals.
  * **Out-of-Sample Hold-Out Confirmation (2025 Test Window):** XGBoost achieved **38.48% MAPE** (8.2% relative error reduction over Naive Seasonal baseline of 41.89%).
* **Deliverables:**
  * [`data/Forecast_CV_Predictions.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Forecast_CV_Predictions.csv) (2,580 rows = 5 folds × 9 series × 5 models × 12 months, minus short-series skips)
  * [`data/Forecast_CV_Metrics.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Forecast_CV_Metrics.csv) (860 rows = 5 folds × 9 series × 5 models × 4 horizons)
  * [`Forecasting_ModelComparison.md`](file:///D:/Projects/Downtown-Homeless-Analysis/Forecasting_ModelComparison.md) (comprehensive 5–7 page report covering CV methodology, fold definitions, multi-regime backtests, champion selection rationale, and pipeline handoff)
  * 3 Publication figures in [`figures/task7_3/`](file:///D:/Projects/Downtown-Homeless-Analysis/figures/task7_3/): `cv_mape_by_horizon_overall.png`, `cv_5fold_trajectories_overall.png`, `cv_neighborhood_champions.png`.

---

### **Task 7.4: Generate forecast outputs and build automated pipeline** (COMPLETED)
* **Master Notebook Consolidated:** `Forecasting_Models.ipynb` extended through Section 26, executing Tasks 7.1, 7.2, 7.3, and 7.4 end-to-end (0 errors, 887 KB executed output). Both source CSVs hash-verified unchanged before and after execution.
* **Standalone Automated Production Pipeline:** Packaged in `forecast_pipeline.py`. Operable via standard CLI:
  `python forecast_pipeline.py [--input PATH] [--output PATH] [--horizon 12] [--export-plots]`
  * Dynamic training split, zero-leakage regularization, and robust in-memory frequency interpolation (`freq='MS'`).
  * Automated champion architecture dispatching (XGBoost, SARIMA, Prophet) with Holt-Winters expanding variance calibration.
* **12-Month Prospective Projections (2026-01 to 2026-12):**
  * Generated across all 9 series with 80% and 95% statistically calibrated prediction intervals.
  * Policy scenario modeling: **Optimistic** (-24% at Month 12 via accelerated shelter expansion), **Baseline** (status quo), **Pessimistic** (+26% at Month 12 via shelter capacity exhaustion).
* **Deliverables:**
  * [`data/Forecasts_12Month.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Forecasts_12Month.csv) (108 rows = 9 series × 12 forward months, containing point forecasts, 80%/95% PIs, and scenario bounds).
  * [`forecast_pipeline.py`](file:///D:/Projects/Downtown-Homeless-Analysis/forecast_pipeline.py) (standalone production CLI script).
  * [`ForecastingPipeline_Documentation.md`](file:///D:/Projects/Downtown-Homeless-Analysis/ForecastingPipeline_Documentation.md) (operations runbook, CLI reference, retraining schedule, and monitoring guide).
  * 2 Publication figures in [`figures/task7_4/`](file:///D:/Projects/Downtown-Homeless-Analysis/figures/task7_4/): `forecast_overall_footprint_12month.png`, `forecast_neighborhoods_panel_12month.png`.
* **Asana Status:** Parent Task 7.4 and all 6 subtasks (7.4.1 through 7.4.6) marked **Completed**.

---

### **Task 8.1: Compile and document county-level PIT count data** (COMPLETED)
* **RTFH PIT Data Harvested (2017–2025):** 26 source PDF reports and tabular releases downloaded and cached in `data/rtfh_pdfs/`.
* **Empirical Pairing Built:** [`build_paired_counts.py`](file:///D:/Projects/Downtown-Homeless-Analysis/build_paired_counts.py) compiled [`data/Downtown_County_PairedCounts.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Downtown_County_PairedCounts.csv).
* **Key Findings:**
  1. **Pre-Pandemic Baseline (2017–2020):** Downtown held a stable **15.7% to 20.0%** share of countywide unsheltered homelessness.
  2. **Peak Crisis Convergence (2022–2023):** Downtown concentration doubled, reaching **35.2% (2022)** and **37.5% (2023)** of all unsheltered homelessness across San Diego County (accounting for 59.0% within the City of San Diego).
  3. **Post-Ordinance Spatial Dispersion (2024–2025):** Following enforcement of the July 2023 Unsafe Camping Ordinance, downtown counts contracted sharply while countywide unsheltered homelessness reached an all-time record of 6,110 in 2024. Downtown's share dropped to **16.7% (2024)** and **14.9% (2025)**, demonstrating widespread regional dispersion into surrounding riverbeds, freeway rights-of-way, and outlying municipalities.
  4. **2021 COVID-19 Waiver:** Unsheltered count officially waived by HUD; recorded as `NaN` in paired series.
  5. **2022 Omicron Postponement:** Count conducted Feb 24, 2022; paired accurately with Feb 2022 DSDP data.
* **Deliverables:**
  * Canonical CSV: [`data/Downtown_County_PairedCounts.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Downtown_County_PairedCounts.csv)
  * Technical Report: [`Task8.1_CountyPIT_Documentation.md`](file:///D:/Projects/Downtown-Homeless-Analysis/Task8.1_CountyPIT_Documentation.md)
  * Publication Visualizations: [`figures/task8_1/county_vs_downtown_trajectories.png`](file:///D:/Projects/Downtown-Homeless-Analysis/figures/task8_1/county_vs_downtown_trajectories.png) and [`figures/task8_1/downtown_share_of_county_unsheltered.png`](file:///D:/Projects/Downtown-Homeless-Analysis/figures/task8_1/downtown_share_of_county_unsheltered.png)
* **Google Drive Upload:** All 4 deliverables (`Downtown_County_PairedCounts.csv`, `Task8.1_CountyPIT_Documentation.md`, `county_vs_downtown_trajectories.png`, `downtown_share_of_county_unsheltered.png`) uploaded to `Shared with me > Downtown Homelessness > Deliverables > Assignment 8 - County-Level Estimation Model` (Folder ID: `1D8ffMhicVMGPcGRKxNtvlNnLGXXSSSws`).
* **Asana Status:** Task 8.1 parent task and all 6 subtasks (8.1.1 to 8.1.6) marked **Completed** with comprehensive completion summary posted to Project Lead Adir Mancebo Jr.

---

### **Task 8.2: Analyze the downtown-to-county relationship** (COMPLETED)
* **Statistical Analysis Pipeline:** Built and executed [`build_correlation_analysis.py`](file:///D:/Projects/Downtown-Homeless-Analysis/build_correlation_analysis.py) (0 errors). Source dataset [`data/Downtown_County_PairedCounts.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Downtown_County_PairedCounts.csv) hash-verified unchanged before and after execution.
* **Empirical Ratio Analysis (4 Definitions):**
  1. *Reported Adjusted / County Unsheltered:* Mean **21.99%** (Std 9.07%, Median 18.27%, Range 14.89%–37.49%, CV = 41.2%).
  2. *Core 6 Constant / County Unsheltered:* Mean **19.31%** (Std 5.25%, Median 18.04%, Range 13.42%–28.60%, CV = 27.2%). Constant methodology boundaries eliminate artificial boundary expansion volatility, reducing ratio variance by 34%.
  3. *Reported Adjusted / City SD Unsheltered:* Mean **37.39%** (Std 13.35%, Median 32.38%, Max 59.02% in 2023).
  4. *Core 6 Constant / City SD Unsheltered:* Mean **32.84%** (Std 7.37%, Median 31.97%, Range 23.33%–45.03%, CV = 22.4%).
* **Parametric & Non-Parametric Correlation Analysis:**
  - *Full Longitudinal Sample (2017–2025, $N=8$):* Pearson $r = -0.0609$ ($p = 0.8861, 95\%\text{ CI: } [-0.734, 0.673]$), Spearman $\rho = +0.2143$ ($p = 0.6103$).
  - *Pre-Ordinance Subsample (2017–2023, $n=6$):* Pearson $r = +0.1142$ ($p = 0.8294$), Spearman $\rho = +0.3143$ ($p = 0.5441$).
  - *Pre-Pandemic Baseline (2017–2020, $n=4$):* Pearson $r = +0.4464$ ($p = 0.5536$), Spearman $\rho = +0.4000$ ($p = 0.6000$).
  - *Downtown vs. City of San Diego Unsheltered ($N=8$):* Pearson $r = +0.2416$ ($p = 0.5642$), Spearman $\rho = +0.4286$ ($p = 0.2894$).
  - *Root Cause of Decoupling:* Enforcement of the City of San Diego's Unsafe Camping Ordinance (effective late July 2023) created a dramatic regional divergence in 2024–2025. Countywide unsheltered counts reached an all-time record of 6,110 while Downtown counts dropped precipitously (1,018 in 2024, 851 in 2025), collapsing Downtown's county share from 37.5% down to 14.9%.
* **Ratio Stability & Hypothesis Testing:**
  - *One-Way ANOVA across 3 Regimes:* $F(2, 5) = 66.51$, $p = 0.0002$ ($p < 0.001$), effect size $\eta^2 = 0.9638$.
    * Regime 1 (Pre-Pandemic Baseline 2017–2020, $n=4$): Mean $17.93\% \pm 2.27\%$
    * Regime 2 (Peak Crisis Convergence 2022–2023, $n=2$): Mean $36.34\% \pm 1.63\%$
    * Regime 3 (Post-Ordinance Spatial Dispersion 2024–2025, $n=2$): Mean $15.78\% \pm 1.25\%$
  - *Kruskal-Wallis Non-Parametric Test:* $H = 6.00$, $p = 0.0498$.
  - *Chow Structural Break Test (2023/2024 boundary):* $F = 43.19$, $p = 0.0028$.
  - *Linear Trend Test:* OLS slope $\beta = -0.0041$/yr ($t = -0.38, p = 0.7169$). The ratio does not exhibit a continuous linear trend; it behaves as distinct structural regimes governed by municipal policy shifts.
  - *Conclusion:* Decisively **REJECTS** the constant-ratio hypothesis ($96.4\%$ of total variance is explained by regime shifts). Constant-ratio expansion cannot be applied uniformly across historical eras without regime conditioning.
* **Small-Sample Statistical Power & MDES Audit ($N=8$):**
  - Small sample size severely limits bivariate correlation testing. Power to detect a moderate correlation ($|r| = 0.50$) at $\alpha=0.05$ is only **$23.3\%$** ($\beta = 76.7\%$ risk of Type II error).
  - Minimum Detectable Effect Size (MDES) at standard $80\%$ statistical power requires **$|r| \ge 0.850$** ($|r| \ge 0.896$ for $90\%$ power).
  - Detecting $r = 0.50$ with $80\%$ power requires **$N = 30$ annual observation pairs**.
* **Deliverables:**
  - Canonical Datasets: [`data/Downtown_County_CorrelationMetrics.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Downtown_County_CorrelationMetrics.csv), [`data/Downtown_County_RatioStability.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Downtown_County_RatioStability.csv), [`data/Downtown_County_PowerAnalysis.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Downtown_County_PowerAnalysis.csv).
  - Technical Report: [`Downtown_County_CorrelationAnalysis.md`](file:///D:/Projects/Downtown-Homeless-Analysis/Downtown_County_CorrelationAnalysis.md) (9 comprehensive sections covering mathematical formulation, ANOVA tables, power analysis, policy interpretation, and modeling guidance for Task 8.3).
  - Publication Visualizations (4 figures in [`figures/task8_2/`](file:///D:/Projects/Downtown-Homeless-Analysis/figures/task8_2/)): `county_vs_downtown_scatter.png`, `ratio_stability_regimes.png`, `statistical_power_curve.png`, `downtown_vs_city_vs_county_shares.png`.
  - Automation Script: [`build_correlation_analysis.py`](file:///D:/Projects/Downtown-Homeless-Analysis/build_correlation_analysis.py).
* **Google Drive Upload:** All 8 deliverables uploaded to `Shared with me > Downtown Homelessness > Deliverables > Assignment 8 - County-Level Estimation Model` (Folder ID: `1D8ffMhicVMGPcGRKxNtvlNnLGXXSSSws`).
* **Asana Status:** Task 8.2 parent task and all 7 subtasks (8.2.1 through 8.2.7) marked **Completed** with full technical summary posted to Project Lead Adir Mancebo Jr.

---

### **Task 8.3: Build and validate the estimation model** (COMPLETED)
* **Estimation Pipeline Implemented:** Built and executed [`county_estimation_model.py`](file:///D:/Projects/Downtown-Homeless-Analysis/county_estimation_model.py) (0 errors). Source dataset [`data/Downtown_County_PairedCounts.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Downtown_County_PairedCounts.csv) hash-verified unchanged before and after execution (`24bd3e0a53ef1263...`).
* **Models Evaluated under 8-Fold Leave-One-Year-Out Cross-Validation (LOOCV):**
  1. *Ordinary Least Squares (OLS - Best Standard Model):* $Y = 5,146.07 - 0.1171 \cdot X$. LOOCV RMSE **960.53** | MAE **879.68** | MAPE **18.19%** | Signed Bias **+1.39%**. Relaxes the origin-constraint to capture non-downtown baseline unsheltered homelessness (~5,146).
  2. *OLS with Secular Time Trend:* $Y = 5,038.27 - 0.4285 \cdot X + 110.89 \cdot t$ ($R^2 = 0.150$). LOOCV RMSE **1,050.44** | MAE **943.16** | MAPE **19.34%** | Signed Bias **-1.27%**. Incurs small-sample degrees-of-freedom penalty ($df = 4$ in folds).
  3. *Simple Ratio Estimators (Zero-Intercept Proportionality Failure):*
     - Pooled Ratio ($\hat{R} = 4.66$): LOOCV RMSE **2,392.61** | MAE **1,917.36** | MAPE **38.19%**. Fails in peak congestion years (in 2023, predicted 10,146 vs. 5,171 actual; $+96.2\%$ error).
     - Mean of Ratios ($\bar{r} = 5.10$): LOOCV RMSE **2,482.53** | MAE **1,777.41** | MAPE **35.90%**.
  4. *OLS with Policy Regime Indicator (Overall Champion Model):* $Y = 4,513.26 + 0.1859 \cdot X + 1,225.04 \cdot D_{\text{post}}$ ($R^2 = 0.504$). Incorporates the July 2023 Unsafe Camping Ordinance structural break. Restores positive downtown elasticity, cutting LOOCV RMSE down to **815.32** | MAE **721.22** | MAPE **14.89%** | Signed Bias **-0.34%**. Out-of-sample hold-out errors in 2024 and 2025 were only $-6.05\%$ and $+6.47\%$.
* **Predictor Sensitivity Check (`downtown_fixed6_constant`):**
  - Eliminating boundary expansion improves ratio RMSE from 2,392 to 1,473 (MAPE 25.2%), while OLS Regime RMSE drops to **772.07** (MAPE **14.44%**), confirming OLS superiority across definitions.
* **Uncertainty Quantification (Calibrated 95% Prediction Intervals):**
  - Uses exact Student's $t$-distributions ($t_{df, 0.975} \in [2.365, 2.571]$) rather than asymptotic normal $z=1.96$ to honestly reflect small-sample $N=8$ parameter and residual variance.
* **Current Operational County Estimates (Dec 2025 Historical Baseline $X_0 = 985.38$):**
  - Champion Policy Regime OLS: **5,921** [95% PI: **3,867 to 7,976**] ($SE_{\text{pred}} = 799.2$).
  - Standard OLS: **5,031** [95% PI: **2,834 to 7,227**] ($SE_{\text{pred}} = 897.8$).
  - Prospective 2026-01 projection (Task 7.4 XGBoost $X_0 = 885.63$): **5,903** [95% PI: **3,849 to 7,957**].
* **Deliverables:**
  - Standalone Pipeline: [`county_estimation_model.py`](file:///D:/Projects/Downtown-Homeless-Analysis/county_estimation_model.py)
  - Canonical Projections: [`data/CountyEstimate_Current.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/CountyEstimate_Current.csv)
  - Validation Benchmarks: [`data/CountyEstimation_LOOCV_Metrics.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/CountyEstimation_LOOCV_Metrics.csv), [`data/CountyEstimation_LOOCV_Predictions.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/CountyEstimation_LOOCV_Predictions.csv)
  - Technical Report: [`CountyEstimation_ModelReport.md`](file:///D:/Projects/Downtown-Homeless-Analysis/CountyEstimation_ModelReport.md)
  - Publication Visualizations (4 figures in [`figures/task8_3/`](file:///D:/Projects/Downtown-Homeless-Analysis/figures/task8_3/)): `model_fits_and_prediction_intervals.png`, `loocv_actual_vs_predicted_trajectories.png`, `loocv_error_metrics_comparison.png`, `current_county_estimates_scenarios.png`.
* **Google Drive Upload:** All 9 deliverables uploaded to `Shared with me > Downtown Homelessness > Deliverables > Assignment 8 - County-Level Estimation Model` (Folder ID: `1D8ffMhicVMGPcGRKxNtvlNnLGXXSSSws`).
* **Asana Status:** Task 8.3 marked **Completed** with comprehensive technical summary and metrics comment posted to Project Lead Adir Mancebo Jr.

---

### **Task 8.4: Document methodology, limitations, and produce final deliverables** (COMPLETED)
* **Limitations Document Authored:** Created [`CountyEstimation_LimitationsDocument.md`](file:///D:/Projects/Downtown-Homeless-Analysis/CountyEstimation_LimitationsDocument.md), formalizing the methodological boundaries, assumption stress-testing, and operational governance charter for macro-estimation.
* **Scope of Applicability Defined:**
  - *Permitted/Recommended:* Interim directional tracking between annual January PIT counts; macro-level countywide scenario planning and capacity stress-testing for service providers.
  - *Strictly Prohibited:* Official HUD Continuum of Care submissions; formulas determining statutory budget entitlements; sub-regional micro-allocations (East County, South Bay, etc.); unconditioned extrapolation across unmodeled policy shifts.
* **Assumption Audits Synthesized:**
  1. *Ratio Stability (Decisively Rejected):* Task 8.2 proved ratio fractured into 3 distinct policy regimes ($F=66.51, p=0.0002$): Baseline 2017–2020 ($17.93\%$), Peak Crisis 2022–2023 ($36.34\%$), and Post-Camping Ordinance 2024–2025 ($15.78\%$). Unconditioned constant-ratio expansion causes errors up to $+96\%$ and is empirically invalid.
  2. *Methodology Harmonization:* RTFH ceased multipliers for HUD PIT in 2020 while DSDP maintained multipliers (1.75 tent / 2.03 vehicle), introducing an artificial $\sim 15\%-22\%$ wedge, controlled in the pipeline via constant-methodology transformations.
  3. *Policy Invariance & Spatial Displacement:* Following the July 2023 City of San Diego Unsafe Camping Ordinance, Downtown counts fell $-56\%$ while countywide unsheltered numbers reached an all-time record (6,110). Encampment enforcement displaced unhoused populations into riverbeds and neighboring municipalities; a downtown decline does not represent regional recovery.
* **Margin of Error & Public Communication Guidance (The 4 Rules):**
  - Empirical Margin of Error: $\pm 2,050$ individuals ($\approx \pm 35\%$ relative spread) under Student's $t$ 95% prediction intervals.
  - Rule 1: Never report single-point precision (prohibited: "5,921").
  - Rule 2: Always round point estimates to the nearest 100 (required: "5,900").
  - Rule 3: Always report the calibrated 95% prediction interval range: "5,900 [3,900 to 8,000]".
  - Rule 4: Always disclose that estimates assume the post-July 2023 camping ordinance enforcement environment remains in effect.
* **Annual Retraining Runbook:** Established a 5-step maintenance protocol for future analysts to ingest new annual RTFH PIT reports, match January DSDP counts, re-evaluate Chow structural breaks, re-run LOOCV, and update prediction intervals.
* **Deliverables:**
  - Governance Charter: [`CountyEstimation_LimitationsDocument.md`](file:///D:/Projects/Downtown-Homeless-Analysis/CountyEstimation_LimitationsDocument.md).
* **Google Drive Upload:** Uploaded to `Shared with me > Downtown Homelessness > Deliverables > Assignment 8 - County-Level Estimation Model` (Folder ID: `1D8ffMhicVMGPcGRKxNtvlNnLGXXSSSws`).
* **Asana Status:** Task 8.4 marked **Completed** with comprehensive technical summary and governance protocols posted to Project Lead Adir Mancebo Jr. (Assignment 8 is 100% COMPLETE).

---

## 5. File & Directory Inventory (`D:\Projects\Downtown-Homeless-Analysis\`)

```text
D:\Projects\Downtown-Homeless-Analysis\
├── PROJECT_CONTEXT.md                           <-- THIS FILE (Master Project Memory)
├── DataValidation_SourceCheck.md                <-- Task 1.1 Complete Audit Deliverable
├── Task1.3_Methodology_Reconciliation_Report.md <-- Task 1.3 Complete Methodology Report
├── EDA_DowntownCounts.ipynb                     <-- [Task 2.1/2.2] Summary stats, seasonality, YoY, 10 charts
├── EDA_DowntownCounts.pdf                       <-- [Task 2.3] 21-page notebook export
├── EDA_SummaryReport.md                         <-- [Task 2.3] 7-section written summary report
├── EDA_Presentation.pptx                        <-- [Task 2.3] 8-slide deck
├── build_presentation.py                        <-- [Task 2.3] Script that builds the .pptx deck
├── build_html_deck.py                           <-- [Task 2.3] Script that builds an HTML mirror of the deck
├── BlockDigitization_ValidationReport.md        <-- [Task 3.1] Block-level source-map validation report
├── build_blocklevel_sample.py                   <-- [Task 3.1] Stratified sampling script (seed=42)
├── SpatialPanel_BalancingReport.md              <-- [Task 3.3] Unbalanced panel documentation & fix
├── build_balanced_panel.py                      <-- [Task 3.3] Balanced-panel build script
├── BlockDigitization_Methodology.md             <-- [Task 3.4] Consolidated digitization methodology
├── BlockMapCoverage_GapAnalysis.md              <-- [Task 3.4] Coverage table fix & digitization gap analysis
├── build_coverage_gap_analysis.py               <-- [Task 3.4] Gap-analysis build script
├── TimeSeries_Decomposition.ipynb                <-- [Task 4.1] Classical + STL decomposition, 9 series
├── build_timeseries_decomposition.py            <-- [Task 4.1] Decomposition notebook build script
├── SeasonalPatterns_Analysis.ipynb              <-- [Task 4.2] Seasonal indices, CIs, significance tests
├── build_seasonal_indices.py                    <-- [Task 4.2] Seasonal-indices notebook build script
├── StructuralBreak_Analysis.ipynb                <-- [Task 4.3] Chow/CUSUM structural break tests, 9 series
├── build_structural_break_analysis.py           <-- [Task 4.3] Structural-break notebook build script
├── StructuralBreak_Analysis.md                  <-- [Task 4.3] Full written report (Google Doc source)
├── MethodologyImpact_Analysis.ipynb              <-- [Task 6.1] Theoretical vs. observed methodology-change impact
├── build_methodology_impact.py                   <-- [Task 6.1] Methodology-impact notebook build script
├── MethodologyImpact_Analysis.md                  <-- [Task 6.1] Full written report (Google Doc source)
├── TimeSeries_ConstantMethodology.ipynb           <-- [Task 6.2] Data-derived vs. theoretical adjustment-factor build
├── build_adjustment_factors.py                    <-- [Task 6.2] Adjustment-factor notebook build script
├── TimeSeries_ConstantMethodology.md              <-- [Task 6.2] Full written report (Google Doc source)
├── build_adjustment_approach_comparison.py        <-- [Task 6.3] 3-approach comparison build script
├── MethodologyAdjustment_RecommendationsMemo.md   <-- [Task 6.3] Recommendations memo (Google Doc source)
├── Forecasting_Models.ipynb                       <-- [Task 7.1-7.4] Master executed forecasting notebook (887 KB)
├── build_forecasting_models.py                    <-- [Task 7.1-7.4] Master notebook generator
├── build_forecasting_cv.py                        <-- [Task 7.3] 5-fold walk-forward cross validation engine
├── Forecasting_ModelComparison.md                 <-- [Task 7.3] Comprehensive model comparison report
├── forecast_pipeline.py                           <-- [Task 7.4] Standalone production forecasting CLI pipeline
├── ForecastingPipeline_Documentation.md           <-- [Task 7.4] Production operations & CLI user guide
├── build_spatial_autocorrelation.py               <-- [Task 5.1] Spatial join & global Moran's I build script
├── SpatialAutocorrelation_Report.md               <-- [Task 5.1] Spatial dataset prep & global autocorrelation report
├── build_hotspot_analysis.py                      <-- [Task 5.2] Local Getis-Ord Gi* build script
├── Hotspot_Analysis_Report.md                     <-- [Task 5.2] Hotspot classification report
├── build_hotspot_maps_persistence.py              <-- [Task 5.3/5.4] Maps, persistence ranking, OSM context, migration build script
├── Hotspot_Maps_Export.pdf                        <-- [Task 5.3] 4-map combined PDF export
├── Hotspot_Interactive.html                       <-- [Task 5.3] Interactive per-date hotspot explorer
├── Hotspot_TechnicalReport.md                     <-- [Task 5.4] Full Assignment 5 completion report
├── Task8.1_CountyPIT_Documentation.md            <-- [Task 8.1] County PIT data audit & documentation
├── build_paired_counts.py                        <-- [Task 8.1] County PIT data pairing script
├── Downtown_County_CorrelationAnalysis.md        <-- [Task 8.2] Ratio stability, correlation & power analysis report
├── build_correlation_analysis.py                 <-- [Task 8.2] Correlation, ANOVA, power curve pipeline
├── CountyEstimation_ModelReport.md               <-- [Task 8.3] LOOCV estimation model report & uncertainty quantification
├── county_estimation_model.py                    <-- [Task 8.3] Production estimation model CLI & LOOCV pipeline
├── CountyEstimation_LimitationsDocument.md        <-- [Task 8.4] Methodology boundaries, assumption stress-testing & governance charter
│
├── docs/                                        <-- [NEW Task 1.4] Comprehensive Documentation Suite
│   ├── DataDictionary_MasterCounts.md           <-- Full metadata covering all 6 delivered datasets
│   ├── MethodologyChangeLog.md                  <-- Audit of 4 regimes & Jan 2020 RTFH/DSDP divergence
│   └── DataQualityReport.md                     <-- 134 nulls root-cause, scope correction, row counts
│
└── data\
    ├── RawCounts_AllYears.csv                   <-- Original raw monthly counts (2,814 rows)
    ├── MasterCounts_Adjusted.csv                <-- Original adjusted monthly counts (2,814 rows)
    ├── BlockLevel_Counts.csv                    <-- Original digitized block counts (3,737 rows)
    ├── Downtown_BlockGrid.csv                   <-- Original 382 downtown blocks reference table
    ├── Downtown_BlockGrid.geojson                <-- Official 382 Polygon features in CRS84
    ├── BlockMap_Coverage.csv                    <-- Inventory of source maps coverage (843 rows)
    │
    ├── Neighborhood_Crosswalk.csv               <-- [Task 1.2] Translation crosswalk (18 rows)
    ├── RawCounts_AllYears_clean.csv             <-- [Task 1.2] Standardized dates & canonical areas
    ├── MasterCounts_Adjusted_clean.csv          <-- [Task 1.2] Standardized dates & canonical areas
    ├── BlockLevel_Counts_clean.csv              <-- [Task 1.2] Cleaned dates, 0 nulls, integer counts
    ├── BlockMap_Coverage_clean.csv              <-- [Task 1.2] Standardized dates & canonical areas
    ├── Downtown_BlockGrid_clean.csv             <-- [Task 1.2] Mapped canonical neighborhoods
    │
    ├── MasterCounts_Adjusted_v2.csv             <-- [Task 1.3 Canonical] Rebuilt adjusted totals
    │
    ├── sample_45_verification.csv               <-- Reproducible 45-cell audit sample (Task 1.1)
    ├── sample_45_audit_results.csv              <-- Full audit results log (Task 1.1)
    ├── dsdp_pdf_links.csv                       <-- Scraped index of 93 source PDF URLs
    │
    ├── sample_blocklevel_verification.csv       <-- [Task 3.1] 48-row stratified sample (seed=42)
    ├── blocklevel_neighborhood_totals.csv       <-- [Task 3.1] Expected neighborhood x date totals
    ├── blocklevel_page_audit_results.csv        <-- [Task 3.1] 87-row page-level audit results
    ├── BlockGrid_GeometryValidation.csv         <-- [Task 3.2] 382-row geometry/join validation, 380 pass
    ├── BlockPanel_Balanced_261.csv               <-- [Task 3.3] Balanced 261-block x 12-date panel
    ├── SpatialPanel_FootprintEffect.csv          <-- [Task 3.3] Per-date footprint-expansion quantification
    ├── BlockMapCoverage_GapAnalysis.csv          <-- [Task 3.4] 96-row year-month coverage/digitization status
    ├── SeasonalIndices.csv                       <-- [Task 4.2] 108-row seasonal indices, CIs, significance tests
    ├── StructuralBreaks.csv                       <-- [Task 4.3] 57-row Chow/CUSUM structural-break test results
    ├── MethodologyImpact_Composition.csv          <-- [Task 6.1] 72-row monthly tent/vehicle/individual raw composition, 3 windows
    ├── MethodologyImpact_TheoreticalVsObserved.csv <-- [Task 6.1] 14-row theoretical-vs-observed impact comparison, per neighborhood + pooled
    ├── AdjustmentFactors_RatioComparison.csv       <-- [Task 6.2] 14-row observed-vs-theoretical ratio comparison
    ├── TimeSeries_ConstantMethodology.csv          <-- [Task 6.2] 924-row long-format constant-methodology series, 9 series
    ├── AdjustmentApproach_Comparison.csv           <-- [Task 6.3] 324-row 3-approach comparison, pooled fixed-core-six
    ├── AdjustmentApproach_SummaryStats.csv         <-- [Task 6.3] Pre-2020 pooled mean/gap summary, 3 approaches
    ├── SpatialAnalysis_AnalysisReady.csv           <-- [Task 5.1] 5,042-row joined block/date data, balanced_261 + full_382_recent scopes
    ├── SpatialWeights_Queen.csv                    <-- [Task 5.1] 2,642-row directed queen-contiguity neighbor links
    ├── SpatialAutocorrelation_Results.csv          <-- [Task 5.1] 17-row global Moran's I results & inference diagnostics
    ├── Hotspot_Classifications.geojson             <-- [Task 5.2] 3,132-feature block-date Gi* classifications
    ├── Hotspot_Summary_ByDate.csv                  <-- [Task 5.2] Hotspot classification counts aggregated by date
    ├── Hotspot_Persistence_Ranking.csv             <-- [Task 5.3/5.4] 261-block persistence ranking (hotspot-date count, ties by z-score/count)
    ├── Hotspot_Top10_Context.csv                   <-- [Task 5.4] Top-10 persistent blocks, nearest OSM service/transit distances
    ├── Hotspot_Migration_Centroids.csv             <-- [Task 5.4] Weighted/unweighted hotspot centroid shift, early vs. recent period
    ├── OSM_Service_Transit_Context.geojson         <-- [Task 5.4] Raw OpenStreetMap service/transit context (Overpass API, 2026-09-13)
    ├── Forecast_Baseline_NaiveSeasonal.csv         <-- [Task 7.1] 216-row naive-seasonal baseline forecasts, 9 series x 2 variants
    ├── Forecast_BaselineMetrics.csv                <-- [Task 7.1] 72-row RMSE/MAE/MAPE at 4 horizons, 9 series x 2 variants
    ├── Forecast_ModelPredictions.csv               <-- [Task 7.2] 540-row predictions, 9 series x 5 models (incl. naive baseline)
    ├── Forecast_ModelComparison.csv                <-- [Task 7.2] 180-row metrics + hyperparameters, 9 series x 4 horizons x 5 models
    ├── Forecast_CV_Predictions.csv                 <-- [Task 7.3] 2,580-row 5-fold CV predictions across 5 models, 9 series, 4 horizons
    ├── Forecast_CV_Metrics.csv                     <-- [Task 7.3] 860-row 5-fold CV multi-horizon evaluation metrics table
    ├── Forecasts_12Month.csv                       <-- [Task 7.4] 108-row canonical 12-month forward forecasts with PIs & scenarios
    ├── Downtown_County_PairedCounts.csv          <-- [Task 8.1] 8-year paired annual count dataset (2017-2025)
    ├── Downtown_County_CorrelationMetrics.csv     <-- [Task 8.2] Longitudinal correlation matrices & regime subsets
    ├── Downtown_County_RatioStability.csv        <-- [Task 8.2] ANOVA, Kruskal-Wallis & Chow test outputs
    ├── Downtown_County_PowerAnalysis.csv         <-- [Task 8.2] Small-sample power curves & MDES table (N=8)
    ├── CountyEstimate_Current.csv                <-- [Task 8.3] Current countywide unsheltered estimates & 95% PIs
    ├── CountyEstimation_LOOCV_Metrics.csv        <-- [Task 8.3] LOOCV evaluation metrics table (RMSE, MAE, MAPE, Bias)
    ├── CountyEstimation_LOOCV_Predictions.csv    <-- [Task 8.3] Annual hold-out cross-validation predictions table
    │
    └── pdfs\                                    <-- Local cache of downloaded DSDP monthly PDFs (41 total)
        ├── December-2018-Homeless-Count_FINAL.pdf (Covers all 2017 & 2018 monthly totals)
        ├── March-2021-Unsheltered-Homeless-Count-Packet.pdf
        ├── Unhseltered-Count-December-2022-with-Maps.pdf (Covers all 2022 monthly totals)
        ├── April-2025-Unsheltered-Counts-W-Maps.pdf (Covers 2024 & 2025 totals)
        ├── (32 monthly PDF packets cached from Task 1.1's audit)
        └── (7 more added in Task 3.1: Jan 2019/2020/2021/2022/2023/2024/2025, for block-map coverage)
```

---

## 6. Project Roadmap & Upcoming Assignments

* **Assignment 1: Data Validation, Cleaning & Standardization** (100% COMPLETE)
  * Tasks 1.1, 1.2, 1.3, 1.4 completed, uploaded to Drive, signed off in Asana.
* **Assignment 2: Exploratory Data Analysis (EDA)** (100% COMPLETE)
  * **Task 2.1: Generate summary statistics and temporal patterns** (COMPLETED)
    - Built & executed [`EDA_DowntownCounts.ipynb`](file:///D:/Projects/Downtown-Homeless-Analysis/EDA_DowntownCounts.ipynb) end-to-end (no errors).
    - Scoped to `component == 'total'` & `area_type == 'neighborhood'` (708 rows, 7 neighborhoods) to avoid double-counting components/sub-areas.
    - Overall: mean 156.8, median 58.9, std 197.4 (2017–2025). By neighborhood: East Village (552.8) ≫ Outside Perimeter (217.6) > City Center (171.8) > Cortez (59.5) > Gaslamp (48.4) > Columbia (44.5) > Marina (30.9).
    - Seasonality: overall flat; **Feb/Aug/May** highest, **Mar/Nov/Apr** lowest. East Village peaks Jul–Aug, dips in spring.
    - YoY: decline 2018–2020 (COVID low, −19.7% in 2020), rebound 2021–2022 (+25.9%, +57.6%, peak 224 in 2023), drop −43.5% in 2024, ~flat 2025 (−2.9%).
    - Top 3 by avg count: East Village, Outside Perimeter, City Center. Top 3 by growth rate (2019+): Outside Perimeter (+26.9%), Cortez (+12.0%), City Center (+3.9%) — diverges from size ranking; Marina/Columbia shrinking.
    - Caveat noted: Outside Perimeter has only 56 obs (partial coverage since 2022); 28 nulls remain in neighborhood-level `total_count` (2025 unreleased months).
  * **Task 2.2: Create required visualizations** (COMPLETED)
    - Added all 10 required charts to [`EDA_DowntownCounts.ipynb`](file:///D:/Projects/Downtown-Homeless-Analysis/EDA_DowntownCounts.ipynb): overall time series w/ regime markers, seasonal pattern, neighborhood stacked-area composition, EV sub-area comparison, before/after methodology-change comparison (2017 & 2018), YoY overall + by neighborhood, COVID-19 period (2020-2021 shaded), raw-vs-adjusted "adjustment gap" over time, and neighborhood distribution boxplot.
    - Each chart has title, axis labels, legend, source attribution, and verified (data-checked) commentary.
    - Key correction made during build: initial draft commentary assumed the adjustment gap grows with volume through 2021-2023; actual data shows the gap is largest/most volatile in 2018 (avg +13.5/mo, spike +156.61 in Feb 2018 — ties to the Feb 2018 source PDF addition error from Task 1.1) then near-zero (±1-5) from 2019 on. Commentary was corrected to match verified output before finalizing.
    - Peak overall count confirmed at 2,103 (May 2023), not initially assumed ~2,500.
  * **Task 2.3: Produce summary report and presentation** (COMPLETED)
    - Wrote [`EDA_SummaryReport.md`](file:///D:/Projects/Downtown-Homeless-Analysis/EDA_SummaryReport.md) covering all 7 required sections (overall trends/inflection points, quantified seasonality, neighborhood insights, COVID-19 impacts, methodology change effects, data limitations, 4 hypotheses for further analysis) — all figures pulled directly from verified Task 2.1/2.2 output.
    - Uploaded as Google Doc "EDA_SummaryReport" to Drive folder `Assignment 2 - Exploratory Data Analysis` (newly created under the shared Deliverables folder, matching the Assignment 1 naming convention).
    - Exported `EDA_DowntownCounts.ipynb` to PDF via `nbconvert --to html` + Playwright sync API print-to-PDF (nbconvert's native `--to webpdf` hit a Windows asyncio subprocess bug — worked around it). 21-page PDF uploaded to the same Drive folder.
    - Slide deck: built by Antigravity (8 slides) from a self-contained master prompt, then reviewed and corrected before acceptance -- found and fixed a real bug where Charts 1/3/9 plotted unreleased 2025 months (nulls) as zero instead of excluding them, creating a misleading crash-to-zero visual; regenerated those 3 charts from source data with nulls properly excluded, swapped Slide 4's chart from composition to YoY-by-neighborhood to match its text, removed decorative arrow glyphs, fixed image aspect-ratio distortion, re-embedded at 200 DPI. Cleaned up Antigravity's intermediate build artifacts before committing.
    - All 3 deliverables ([`EDA_SummaryReport.md`](file:///D:/Projects/Downtown-Homeless-Analysis/EDA_SummaryReport.md), [`EDA_DowntownCounts.pdf`](file:///D:/Projects/Downtown-Homeless-Analysis/EDA_DowntownCounts.pdf), [`EDA_Presentation.pptx`](file:///D:/Projects/Downtown-Homeless-Analysis/EDA_Presentation.pptx)) uploaded to Drive folder `Assignment 2 - Exploratory Data Analysis`.
* **Assignment 3: Block-Level Data Validation & Spatial Integration** (Tasks 3.1–3.4) — 100% COMPLETE
  * **Task 3.1: Validate block-level counts against source maps** (COMPLETED)
    - **Source-map coverage gap closed:** Only 5 of the 12 required monthly map PDFs were cached at task start; downloaded the 7 missing packets (Jan 2019, Jan 2020, Jan 2021, Jan 2022, Jan 2023, Jan 2024, Jan 2025) from the DSDP archive and verified each as genuine before use.
    - **Audit methodology revised mid-task:** A cell-level visual re-read (10% stratified sample, 372 rows, then reduced to 48) was abandoned as unreliable on rotated/handwritten scans after repeated cropping attempts failed to pinpoint individual cells with confidence. Redesigned around each page's printed "Count Breakdown" total (self-checkable via `Total = Individual + Vehicle×multiplier + Tent×multiplier`), cross-checked against the digitized neighborhood-month aggregate.
    - **Results:** 87 neighborhood×date cells audited across all 12 dates. 53 exact matches (65.4% of 81 verifiable cells; 73.6% excluding the 2022-03-01 anomaly), 28 discrepancies (nearly all small, ±1 to ±8 units), 6 unverifiable (no legible printed total).
    - **Major finding — 2022-03-01 anomaly:** This single date accounts for 9 of the 28 discrepancies with much larger gaps (10–60+ units) than any other date. Source pages carry inconsistent handwritten dates (3/24/22 vs. 3/29/22) within the same PDF, neither matching the CSV's normalized `2022-03-01` label — flagged for follow-up before use in Assignment 4/5 modeling.
    - **Null resolved:** The one null in `tents_structures` (`16TH_ST_C_ST`, 2020-01-31, row 930) was confirmed a true zero by checking the actual source map — the corresponding grid cell is completely blank, consistent with 0/0/0 on all 11 other dates for that block.
    - **Implausibility screen:** 0 negative values; 136 of 622 rows (21.9%) with a tent/vehicle present record zero individuals (expected per counting methodology, concentrated in East Village); 19 rows flagged as recurring high-concentration blocks (`17TH_ST_K_ST`, `PARK_BL_J_ST`, `15TH_ST_IMPERIAL_AV` in East Village; `03RD_AV_A_ST` in City Center) — candidate hotspots for Assignment 5.
    - **Deliverable:** [`BlockDigitization_ValidationReport.md`](file:///D:/Projects/Downtown-Homeless-Analysis/BlockDigitization_ValidationReport.md), plus `data/blocklevel_page_audit_results.csv`, `data/sample_blocklevel_verification.csv`, `data/blocklevel_neighborhood_totals.csv`, and `build_blocklevel_sample.py`. Uploaded as a Google Doc to Drive folder `Assignment 3 - Block-Level Validation & Spatial Integration` (newly created).
  * **Task 3.2: Verify block grid integrity and spatial joins** (COMPLETED)
    - **ID integrity:** 382 unique `block_id` in both `Downtown_BlockGrid_clean.csv` and `Downtown_BlockGrid.geojson`, identical sets, zero orphans in either join direction against `BlockLevel_Counts_clean.csv`. Full attribute agreement between the two files once compared against the correct columns (`source_neighborhood` in the CSV vs. the GeoJSON's `neighborhood` property — a naming difference, not a data error).
    - **Polygon geometry (shapely):** 0 invalid geometries, 0 unclosed rings, 0 zero-area features, 0 unintended overlaps across all 382 polygons.
    - **Centroid containment:** 380/382 blocks have their stated centroid inside their own polygon and inside their neighborhood's convex hull. The 2 exceptions (`22ND_ST_BROADWAY`, `22ND_ST_SR-94_EB_ON_RA`) are complex non-convex freeway-interchange parcels (110+ vertices) where the centroid sits ~7-12m outside the polygon due to concavity — matches the true polygon centroid almost exactly, not a data error.
    - **Boundary-street consistency:** 326/382 blocks have all 4 sides matching a plausible neighbor block's opposite boundary street; the remaining 56 have 2-3/4, and every one of those is a genuine study-area edge (Outside Perimeter, Map_Border, freeway ramps, waterfront) rather than a defect.
    - **Deliverable:** `data/BlockGrid_GeometryValidation.csv` (382 rows, one per block, all check results + overall pass/fail flag — 380/382 pass everything). Uploaded to Drive folder `Assignment 3 - Block-Level Validation & Spatial Integration` (trimmed to the essential pass/fail columns for the Drive copy; full-precision version with geometry diagnostics kept in the repo).
  * **Task 3.3: Document and correct the unbalanced spatial panel** (COMPLETED)
    - **Confirmed the coverage break:** `BlockLevel_Counts_clean.csv` has exactly 261 blocks on each of the 7 dates from 2018-01-24 to 2021-02-25, then jumps to 382 blocks on each of the 5 dates from 2022-01-27 to 2025-01-31. Early set is a strict subset of the later set (0 blocks dropped, 121 added).
    - **Root cause identified:** the 121 new blocks are exactly Golden Hill (52), Barrio Logan (35), and Sherman Heights (34) — three neighborhoods absent from every count date before 2022, rolled up under "Outside Perimeter" in `Downtown_BlockGrid_clean.csv`.
    - **Footprint effect quantified** (DSDP-multiplier-weighted adjusted totals, full 382-block vs. balanced 261-block, per post-2021 date): 2022-01-27 +18.42%, 2022-03-01 +16.82%, 2023-01-31 +32.77%, 2024-01-25 +3.65%, 2025-01-31 +9.96% — i.e., 4-33% of the reported full-panel total in those years is attributable purely to the expanded study area, not a real count change.
    - **Confirmed the underlying rise is still real:** re-running the balanced 261-block panel across all 12 dates shows the total still jumps from 671.42 (2021-02-25) to 1,149.07 (2022-01-27), a +71% increase on the *same fixed blocks* — the footprint expansion and the genuine 2021→2022 increase are both real, independent effects.
    - **Deliverables created:** [`data/BlockPanel_Balanced_261.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/BlockPanel_Balanced_261.csv) (3,132 rows = 261 blocks × 12 dates, same schema as source, for valid temporal comparison), `data/SpatialPanel_FootprintEffect.csv` (per-date expansion quantification), `build_balanced_panel.py` (build script), and [`SpatialPanel_BalancingReport.md`](file:///D:/Projects/Downtown-Homeless-Analysis/SpatialPanel_BalancingReport.md) (full writeup). Full 382-block file left untouched for recent-period-only (2022+) analysis.
    - **Cross-validated against prior tasks:** balanced-panel neighborhood×date aggregates (individuals/tents/vehicles) match `data/blocklevel_neighborhood_totals.csv` (Task 3.1) exactly — 0 mismatches across all 72 neighborhood-date combinations. All 261 panel block IDs confirmed present in `data/BlockGrid_GeometryValidation.csv` (Task 3.2) with matching neighborhood labels and 0 geometry-check failures.
    - **⚠️ Warning carried into Assignment 5:** any Getis-Ord Gi*/Moran's I hotspot comparison spanning the 2021→2022 boundary must use `data/BlockPanel_Balanced_261.csv`, not the full 382-block file — the added footprint has no pre-2022 baseline. Hotspot analysis confined entirely to 2022–2025 may safely use the full 382-block file (coverage is constant across those 5 dates).
  * **Task 3.4: Reconcile coverage table and document digitization methodology** (COMPLETED)
    - **Column-rename fix confirmed already done:** the coverage table's `block` column (which actually holds neighborhood/area names, e.g. "East Village South", "Barrio Logan") was already renamed to `source_area` with a canonical `neighborhood` column added, back in Task 1.2's `BlockMap_Coverage_clean.csv`. Verified all 10 `source_area` values have a matching entry in `Neighborhood_Crosswalk.csv` — zero unmapped.
    - **Digitization gap quantified:** `BlockMap_Coverage_clean.csv` spans 96 year-months (2018–2025), of which 90 have at least one map marked present. Only 12 of those 90 (13.3%) were ever digitized into `BlockLevel_Counts_clean.csv` — **78 year-months with a usable map remain undigitized**, documented as an explicit out-of-scope project limitation rather than queued work (9-11 undigitized months/year, fairly even across 2018-2024, 7 in partial-year 2025).
    - **Digitized-date coverage confirmed:** all 12 digitized dates have full "map present" (`Yes`) coverage rows. However, 3 source-area/date combinations were digitized from a map rated "Unclear": East Village South (2022-01-27, 2022-03-01) and Sherman Heights (2022-01-27). The 2022-03-01 East Village South flag independently corroborates Task 3.1's previously-found "2022-03-01 anomaly" (inconsistent handwritten source dates).
    - **Deliverables created:** [`BlockDigitization_Methodology.md`](file:///D:/Projects/Downtown-Homeless-Analysis/BlockDigitization_Methodology.md) (consolidated methodology: block identification, count-reading procedure, QC steps, disagreement resolution, referencing Tasks 3.1-3.3), [`BlockMapCoverage_GapAnalysis.md`](file:///D:/Projects/Downtown-Homeless-Analysis/BlockMapCoverage_GapAnalysis.md) (full gap analysis and column-fix confirmation), `data/BlockMapCoverage_GapAnalysis.csv` (96 rows, one per year-month), and `build_coverage_gap_analysis.py` (build script). Both markdown reports uploaded as Google Docs to the Assignment 3 Drive folder.
* **Assignment 4: Time Series Decomposition & Pattern Analysis** (Tasks 4.1–4.4) — 100% COMPLETE
  * **Task 4.1: Perform time series decomposition** (COMPLETED) — see full writeup above. Approved in Asana.
  * **Task 4.2: Quantify seasonal patterns with statistical significance tests** (COMPLETED) — see full writeup above.
  * **Task 4.3: Conduct structural break analysis** (COMPLETED) — see full writeup above.
  * **Task 4.4: Test stationarity and document autocorrelation structure** (COMPLETED) — see full writeup above; Asana completion pending final project update.
* **Assignment 5: Geospatial Hotspot Analysis** (Tasks 5.1–5.4) — **COMPLETE** (see full writeups above).
* **Assignment 7: Forecasting Model Development** (Tasks 7.1–7.4) — **COMPLETE** (see full writeups above).
* **Assignment 8: County-Level Estimation Model** (100% COMPLETE - Tasks 8.1–8.4 done)
  * **Task 8.1: Compile and document county-level PIT count data** (COMPLETED) — see full writeup above. Approved in Asana; deliverables synced to Google Drive.
  * **Task 8.2: Analyze the downtown-to-county relationship** (COMPLETED) — see full writeup above. Approved in Asana; deliverables synced to Google Drive.
  * **Task 8.3: Build and validate the estimation model** (COMPLETED) — see full writeup above. Approved in Asana; deliverables synced to Google Drive.
* **Assignment 9: Interactive Dashboard & Strategic Synthesis** (100% COMPLETE - Tasks 9.1–9.4 done)
  * **Task 9.1: Interactive Executive Dashboard** (COMPLETED) — Production Streamlit application (`app.py`, 6 tabs, sub-2s load, 10/10 automated tests passing).
  * **Task 9.2: Executive Summary & Technical Report** (COMPLETED) — Non-technical executive summary (`docs/ExecutiveSummary_NonTechnical.md`) and 10-chapter technical monograph (`docs/FullTechnicalReport.md`).
  * **Task 9.3: Strategic Recommendations & Slide Deck** (COMPLETED) — 14-slide Canva executive presentation (`Assignment9_StrategicSynthesis.pptx`) and standalone companion browser deck (`Assignment9_StrategicSynthesis.html`).
  * **Task 9.4: Final Project Handoff Documentation** (COMPLETED) — Master technical handoff (`PROJECT_MASTER_HANDOFF_ASSIGNMENTS_1_TO_9.md`) and 5 standardized operational runbooks (`docs/ProjectHandoff_OperationalRunbook.md`).
* **Assignment 10: Multi-Source Predictive System** (Queued on Roadmap)

## 7. Instructions for AI Assistant Resuming in a New Chat

1. **Read this file (`PROJECT_CONTEXT.md`) first.**
2. Check the user's active prompt to see which task they want to address (e.g., Task 2.1).
3. Do not re-download PDFs or re-create files that already exist in `data/`.
4. Canonical count dataset for all downstream analysis: [`data/MasterCounts_Adjusted_v2.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/MasterCounts_Adjusted_v2.csv).
5. Always save Google Drive deliverables into the school Google Drive folder:  
   `Shared with me > Downtown Homelessness > Deliverables` (organized by assignment folder).
6. Maintain strict data fidelity: never overwrite raw source CSVs; always write to `_clean.csv` or `_v2.csv`.
