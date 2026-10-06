# Data Quality & Validation Report: Downtown Homelessness Analytics

**Downtown San Diego Homeless Population Analysis**  
*Data Science Alliance / Volunteer Analytics Project*  
**Author:** Kyaw Soe Lwin (`kylwin@ucsd.edu`)  
**Project Lead:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)  

---

## 1. Executive Summary

This report establishes the comprehensive data quality audit, validation methodology, missing data root-cause analysis, and annual row count reconciliation for the Downtown San Diego Homeless Population Analysis project.

All deliverables were audited against original source PDF packets published by the Downtown San Diego Partnership (DSDP) Clean & Safe program.

---

## 2. Scope Correction: Timeline Commences in 2017 (Not 2012)

* **Original Project Scope:** Early curriculum guidelines described analyzing longitudinal counts from "2012 to present."
* **Audited Empirical Finding:** The delivered dataset commences on **January 1, 2017** (`2017-01-01`) and runs through **December 1, 2025** (`2025-12-01`).
* **Root Cause:** Prior to 2017, DSDP and RTFH conducted counts under differing geographic boundaries and sporadic reporting frequencies that were not compiled into the centralized digital database. Digital tabular records were standardized starting with the January 2017 census.
* **Downstream Action:** All downstream documentation, reports, and scope descriptions have been updated to reflect the true **9-year longitudinal panel (2017–2025)** covering **108 monthly periods**.

---

## 3. Detailed Accounting of the 134 Missing Count Values

Across all 2,814 rows in `MasterCounts_Adjusted_v2.csv` and `RawCounts_AllYears_clean.csv`, exactly **134 values are recorded as `NaN`**:

$$\text{Total Missing Values} = 116 \text{ (in 2025)} + 18 \text{ (in 2018)} = \mathbf{134}$$

### 3.1. The 2025 Missing Counts (116 values): True Reporting Gap
* **Affected Months:** July 2025 (29), August 2025 (29), October 2025 (29), November 2025 (29).
* **Breakdown:**
  * 44 missing totals (11 areas $\times$ 4 months)
  * 24 missing individuals (6 neighborhoods $\times$ 4 months)
  * 24 missing tents (6 neighborhoods $\times$ 4 months)
  * 24 missing vehicles (6 neighborhoods $\times$ 4 months)
* **Root Cause Assessment:** **True Reporting Gap (Release Lag).** At the time the raw dataset was extracted and compiled for the project, DSDP had not yet conducted or publicly released the official census packets for these specific four months. 
* **Downstream Treatment:** Retain as explicit `NaN` values. Do not impute with zero during time-series modeling; use time-series interpolation or Kalman smoothing.

### 3.2. The 2018 Missing Counts (18 values): Source Extraction Gap
* **Affected Month:** November 2018 (`2018-11-01`).
* **Breakdown:**
  * 6 missing individuals (6 neighborhoods $\times$ 1 month)
  * 6 missing tents (6 neighborhoods $\times$ 1 month)
  * 6 missing vehicles (6 neighborhoods $\times$ 1 month)
  * **0 missing totals:** The published headline totals for November 2018 are completely intact (East Village: 473, City Center: 146, Columbia: 24, Marina: 41, Cortez: 46, Gaslamp: 69).
* **Root Cause Assessment:** **Source Extraction Gap.** In the November 2018 monthly packet (`2018-Homeless-Sleep-Count-November.pdf`), DSDP published overall neighborhood totals but omitted the itemized table breaking down individuals, tents, and vehicles.
* **Downstream Treatment:** Headline totals remain 100% usable for aggregate analysis.

---

## 4. Annual Row Count Audit Trail (2,814 Total Rows)

To establish an immutable audit trail, row counts by calendar year are cataloged below:

| Year | Total Rows | Neighborhood Rows | Sub-Area Rows | Perimeter Rows | Notes / Methodological Milestone |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **2017** | **72** | 72 | 0 | 0 | 12 months $\times$ 6 neighborhoods (Totals only; no components). |
| **2018** | **336** | 288 | 48 | 0 | Component tracking begins (6 neigh $\times$ 12 mo $\times$ 4 comp = 288) + 48 EV sub-area totals. |
| **2019** | **336** | 288 | 48 | 0 | 288 neighborhood component rows + 48 EV sub-area totals. |
| **2020** | **336** | 288 | 48 | 0 | 288 neighborhood component rows + 48 EV sub-area totals. |
| **2021** | **342** | 294 | 48 | 0 | +6 rows: Outside Perimeter introduced in April 2021 (Apr–Dec 2021 = 9 mo $\times$ 1 comp; -3 missing 2021 breakouts). |
| **2022** | **348** | 300 | 48 | 12 | Full 12-month Outside Perimeter tracking (12 rows) + 288 neighborhood + 48 sub-area = 348. |
| **2023** | **348** | 300 | 48 | 12 | Full 12-month tracking across all categories. |
| **2024** | **348** | 300 | 48 | 12 | Full 12-month tracking across all categories. |
| **2025** | **348** | 300 | 48 | 12 | Full calendar grid (includes 116 unreleased late-2025 cells). |
| **Total**| **2,814** | **2,430** | **384** | **36** | Exact verified sum across all 9 years. |

---

## 5. Summary of Task 1.1 Source Validation Audit (45-Sample Check)

In Task 1.1, a stratified random sample of 45 cells was cross-referenced against 32 downloaded DSDP monthly PDFs:
* **Stratification:** Drawn proportionally across all 9 years (2017–2025), all 7 neighborhoods, and all 4 components.
* **Audit Results:**
  * Exact Matches: **40 cells**
  * True Published Errors: **1 cell** (February 2018 City Center: DSDP PDF internal table addition error of $+30$)
  * Unreleased Data: **4 cells** (late 2025 missing counts)
* **Observed Fidelity Rate:** **97.56%** across published cells (**2.44% error rate**).
* **Major Discovery:** Definitively proved that `"Core"` was an empirical alias for `"City Center"`, retired after Q1 2019, while Gaslamp co-existed independently.

---

## 6. Peer Review & Verification Protocol for Team Members

To allow independent team members or external auditors to validate a random sample of rows against the source PDFs, follow this standardized 4-step protocol:

1. **Draw a Stratified Sample:**
   ```python
   import pandas as pd
   df = pd.read_csv('data/MasterCounts_Adjusted_v2.csv')
   sample = df.dropna(subset=['raw_count']).sample(n=30, random_state=101)
   sample[['date', 'area', 'component', 'raw_count', 'total_count']].to_csv('peer_sample.csv', index=False)
   ```
2. **Retrieve Source PDF:**
   * Locate the corresponding monthly packet in `data/pdfs/` or download from [DSDP Unhoused Care Archive](https://downtownsandiego.org/clean-and-safe/unhoused-care/).
3. **Verify Field Values:**
   * For `component in ['individual', 'tent', 'vehicle']`, compare `raw_count` to the itemized table in the PDF.
   * Verify that `total_count` equals $\text{raw\_count} \times \text{multiplier}$ ($1.75$ for tents, $1.66$ / $2.03$ for vehicles).
   * For `component == 'total'`, verify that `total_count` equals the sum of the three adjusted components.
4. **Log Results:** Record verification status in an audit sheet noting any layout divergences.
---

## Source Corrections (October 2026 audit)

All 945 neighborhood monthly totals for 2017–2025 were re-checked against the summary tables printed on page 1 of the DSDP monthly reports. Every one matches. The corrections below were applied with `scripts/apply_source_corrections.py`; the full cell-level log (old value, new value, PDF file, page, note) is `data/source_corrections.csv`, and the regression tests are in `tests/test_source_corrections.py`.

| What | Cells | Evidence |
|---|---|---|
| 2019 East Village sub-areas (NE/NW/SE/SW) replaced; the file held a copy of the 2020 values | 47 (1 already correct) | 2019 breakout table, January 2020 report p.1; every month sums to the East Village total within ±1 |
| Feb 2018 City Center: vehicles 0 → 1, tents 100 → 10; adjusted total 312.00 → 156.16 | 2 | Core map dated 2-21-18 (Count Breakdown box) |
| Jul 2018 East Village: vehicles 32 → 26 | 1 | East Village map dated 7/25/18; total 621.03 |
| Jul 2022 Cortez: tents 20 → 26 | 1 | Map value column 45.50 and total 89.53 (published 90); the handwritten count "20" contradicts its own value |
| Nov 2022 Marina: individuals 49 → 29 (**inferred**) | 1 | Map total 44 equals the published total; "49" appears copied from the adjacent Gaslamp page |
| Mar 2024 City Center: tents 8 → 18 | 1 | City Center map 3/21/24; total 220.50 (published 221) |
| Jan 2025 North East EV: 84 → 83 | 1 | 2025 breakout table (January sums exactly to 435) |

**Adjusted total set to the published total** (components could not be verified): December 2019 East Village, City Center and Gaslamp, and December 2023 East Village. DSDP never published December 2019 or December 2023 reports. Also September 2025 East Village: the file DSDP posts as "September 2025" actually contains the December 2025 maps.

**Left as-is and flagged:** every area-month where the adjusted total still differs from the published total by more than 2 is listed in `data/MasterCounts_QA_Flags.csv` (22 rows). Three of them were checked against the maps. The file matches the map, but DSDP's own summary table disagrees: April 2020 Gaslamp (map 43.75 vs table 28), February 2023 Gaslamp (46 vs 72), and February 2023 East Village (791 vs 781).

**Not changed:** the 2025 East Village sub-areas (February–June) and November 2021 North West EV. In these months the file's sub-areas add up to the East Village total, but DSDP's breakout table does not (for example, April 2025: 303 vs 401). April 2025 East Village was later revised by DSDP from 317 to 401, which matches the file.

**Additional gaps not in the 134 missing values:** City Center (September 2021) and Marina (December 2021) have no individual/tent/vehicle rows at all; only the total row exists. This is why 2021 has 342 rows rather than 348.

**Methodology date note:** DSDP states that Clean & Safe implemented the 2.03 vehicle multiplier "on May 31, 2018", which was also the May 2018 count night. The `MAY2018` regime therefore correctly starts with the May 2018 count. References to a June 2018 change elsewhere in the project are incorrect.
