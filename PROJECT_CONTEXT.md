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
* **Goal:** Analyze unsheltered homelessness in Downtown San Diego using monthly count data from the Downtown San Diego Partnership (2012–present) disaggregated by neighborhood and East Village sub-area. The ultimate objective is producing time-series forecasts, geospatial hotspot analysis, and policy impact assessments to guide service providers and municipal agencies.

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
* **Source PDF Archive (Downtown San Diego Partnership):**  
  [DSDP Clean & Safe Unhoused Care Reports](https://downtownsandiego.org/clean-and-safe/unhoused-care/)
* **Local Project Root:** `D:\Projects\Downtown-Homeless-Analysis\`
* **Python Environment:** Python 3.13 (`pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `pypdf`, `pymupdf`, `shapely`, `PIL`, `cv2` installed).

---

## 3. The 10-Assignment Roadmap

| Assignment | Title | Status | Primary Focus |
| :---: | :--- | :---: | :--- |
| **1** | **Data Validation, Cleaning & Standardization** | **COMPLETED (100% - Tasks 1.1–1.4)** | Source audit, schema standardization, methodology fixes, data dictionary, methodology log, quality report. |
| **2** | **Exploratory Data Analysis (EDA)** | **COMPLETED (100% - Tasks 2.1-2.3)** | Descriptive stats, multi-year trends, visualizations, presentations. |
| **3** | **Block-Level Validation & Spatial Integration** | **IN PROGRESS (75% - Tasks 3.1-3.3 done)** | Validate digitized block counts against 12 PDF maps, fix unbalanced spatial panel. |
| **4** | **Time Series Decomposition & Pattern Analysis** | Queued | Trend/seasonal/residual decomposition, structural breaks, stationarity tests. |
| **5** | **Geospatial Hotspot Analysis** | Queued | Getis-Ord Gi*, Moran's I, spatial clustering on `Downtown_BlockGrid.geojson`. |
| **6** | **Methodology Impact Assessment** | Queued | Quasi-experimental policy evaluation, continuous weighting models. |
| **7** | **Forecasting Model Development** | Queued | ARIMA, SARIMA, Prophet, Gradient Boosting models. |
| **8** | **County-Level Estimation Model** | Queued | Ratio modeling with Regional Task Force on Homelessness (RTFH) PIT counts. |
| **9** | **Interactive Dashboard & Strategic Synthesis** | Queued | Web dashboard, executive handoff documentation. |
| **10** | **Multi-Source Predictive System** | Queued | Ingesting weather, 311 service calls, shelter censuses, anomaly alerts. |

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
* **Assignment 3: Block-Level Data Validation & Spatial Integration** (Tasks 3.1–3.4) — IN PROGRESS
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
    - **⚠️ Warning carried into Assignment 5:** any Getis-Ord Gi*/Moran's I hotspot comparison spanning the 2021→2022 boundary must use `data/BlockPanel_Balanced_261.csv`, not the full 382-block file — the added footprint has no pre-2022 baseline. Hotspot analysis confined entirely to 2022–2025 may safely use the full 382-block file (coverage is constant across those 5 dates).
* **Assignment 4: Time Series Decomposition & Pattern Analysis** (Tasks 4.1–4.4)
* **Assignment 5: Geospatial Hotspot Analysis** (Tasks 5.1–5.4)
* **Assignment 6: Methodology Impact Assessment** (Tasks 6.1–6.3)
* **Assignment 7: Forecasting Model Development** (Tasks 7.1–7.3)

---

## 7. Instructions for AI Assistant Resuming in a New Chat

1. **Read this file (`PROJECT_CONTEXT.md`) first.**
2. Check the user's active prompt to see which task they want to address (e.g., Task 2.1).
3. Do not re-download PDFs or re-create files that already exist in `data/`.
4. Canonical count dataset for all downstream analysis: [`data/MasterCounts_Adjusted_v2.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/MasterCounts_Adjusted_v2.csv).
5. Always save Google Drive deliverables into the school Google Drive folder:  
   `Shared with me > Downtown Homelessness > Deliverables` (organized by assignment folder).
6. Maintain strict data fidelity: never overwrite raw source CSVs; always write to `_clean.csv` or `_v2.csv`.

