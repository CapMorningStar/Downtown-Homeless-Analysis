# DataValidation_SourceCheck
**Downtown San Diego Homeless Population Analysis**  
*Assignment 1: Data Validation, Cleaning & Standardization — Task 1.1*

* **Analyst:** Kyaw Soe Lwin  
* **Project Lead:** Adir Mancebo Jr. (Data Science Alliance)  
* **Date:** September 3, 2026  
* **Target Dataset:** `RawCounts_AllYears.csv` (2,814 records, 2017–2025)  
* **Source Archive:** Downtown San Diego Partnership (DSDP) Clean & Safe Unhoused Care Reports ([downtownsandiego.org/clean-and-safe/unhoused-care/](https://downtownsandiego.org/clean-and-safe/unhoused-care/))

---

## 1. Executive Summary

This report delivers the verification and quality audit of the historical unsheltered count dataset (`RawCounts_AllYears.csv`) against the original monthly PDF reports published by the Downtown San Diego Partnership (DSDP) Clean & Safe program.

### Key Audit Highlights:
1. **Resolution of "Core" Label:** Definitively resolved. `"Core"` is an earlier historical name for **`City Center`**, not Gaslamp. `"Core"` was used exclusively in 2017 and 2018, transitioned in early 2019, and was completely retired after March 2019 in favor of `"City Center"`. Gaslamp is an independent neighborhood co-reported in every period.
2. **Major Data Duplication Bug in East Village Sub-Areas:** **All 48 sub-area records for 2019 are an exact 100% copy-paste duplicate of the 2020 sub-area counts.** This explains massive negative discrepancies between reported East Village totals and sub-area sums in 2019 (diverging by up to $-206$). Outside of 2019, sub-area sums match reported totals within $\pm 1$ due to rounding, except for a documented $+30$ addition error inside DSDP's own February 2018 published report.
3. **Source Verification Sample:** A reproducible random sample of 45 cells across 2017–2025, 9 geographic areas, and 4 components (`total`, `individual`, `tent`, `vehicle`) was verified against 32 downloaded DSDP monthly PDF reports.
4. **Observed Error Rate:**
   * **Published Cells Audited:** 41 cells
   * **Exact Matches:** 40 cells (97.56% fidelity)
   * **Observed Discrepancy:** 1 cell (2.44% error rate on published records; 2.22% overall sample error rate)
   * **Unpublished / Placeholder Cells:** 4 cells (unreleased late-2025 counts appropriately stored as `NaN`).

---

## 2. Resolution of the "Core" Area Label

The project dataset includes an area label `"Core"`, comprising 69 rows across 2017, 2018, and early 2019. The task required determining whether `"Core"` is a distinct reporting area or an alias for `"City Center"` or `"Gaslamp"`.

### Empirical Findings:
* **Gaslamp Independence:** `"Gaslamp"` exists as an independent reporting area with its own published counts in every single month from January 2017 through December 2025 (co-existing with `"Core"` in 66 records). `"Core"` is therefore **not** Gaslamp.
* **Mutual Exclusivity with City Center:** `"Core"` and `"City Center"` never co-exist in any single month or component cell.
  * **2017 – 2018:** Only `"Core"` is used. Zero records for `"City Center"`.
  * **2019 (Transition Year):**
    * For the `total` component: All 12 months (Jan–Dec 2019) are labeled `"City Center"`.
    * For the sub-components (`individual`, `tent`, `vehicle`): January, February, and March 2019 are labeled `"Core"`, while April through December 2019 are labeled `"City Center"`.
  * **2020 – 2025:** `"Core"` never appears. Only `"City Center"` is used.

### Conclusion & Recommendation:
`"Core"` refers to the Downtown San Diego Civic and Commercial Core, which DSDP rebranded as `"City Center"` during the first quarter of 2019. 

> **Recommendation for Task 1.2:** In the data cleaning and standardization pipeline, all rows where `area == 'Core'` should be recoded to `area = 'City Center'` to establish a unified longitudinal series for that neighborhood from 2017 through 2025.

---

## 3. East Village Sub-Area Summation Consistency Analysis

East Village is divided into four geographic quadrants:
* **North East EV:** North of Market Street & East of Park Avenue
* **North West EV:** North of Market Street & West of Park Avenue
* **South East EV:** South of Market Street & East of Park Avenue
* **South West EV:** South of Market Street & West of Park Avenue

A mathematical check was run comparing:
$$\text{Sum of Sub-Areas} = (\text{North East EV} + \text{North West EV} + \text{South East EV} + \text{South West EV})$$
against the reported $\text{East Village Total}$ across all 96 available monthly observation periods.

### Detailed Findings by Period:

| Year / Period | Matching Records | Discrepancies | Primary Cause / Observation |
| :--- | :---: | :---: | :--- |
| **2017** | 0 | 0 | Sub-area counts were not disaggregated in the CSV dataset for 2017. |
| **2018** | 12 | 2 | Feb 2018 has a $+30$ discrepancy ($504$ sub-area sum vs. $474$ reported). Nov 2018 has a $+1$ rounding difference. |
| **2019** | 12 | 12 | **Severe Data Corruption:** 100% of 2019 sub-area counts are identical duplicates of 2020 sub-area counts (48/48 exact cell matches). Discrepancies range from $-206$ to $-36$. |
| **2020** | 12 | 2 | May and Nov have $+1$ discrepancies due to rounding formulas. |
| **2021** | 12 | 4 | Mar ($+1$), Jul ($-1$), Aug ($+1$), Sep ($-1$) due to rounding. |
| **2022** | 12 | 0 | **100% perfect consistency** ($\text{diff} = 0$) across all 12 months. |
| **2023** | 12 | 5 | Feb ($+1$), Jun ($+2$), Oct ($+1$), Dec ($-1$) rounding; Mar has a $-8$ discrepancy ($657$ vs. $665$). |
| **2024** | 12 | 6 | Mar ($+1$), Apr ($+1$), May ($+1$), Aug ($+1$), Oct ($+1$), Nov ($+1$) consistent $+1$ rounding artifact. |
| **2025** | 12 | 11 | Jan, Feb, Mar, May, Jun, Dec show $\pm 1$ rounding. Sep shows a $-38$ discrepancy. Jul, Aug, Oct, Nov have missing totals (`NaN`). |

### Deep Dive: February 2018 Source Error
In February 2018, the sub-area sum is $504$ ($68 + 45 + 361 + 30$), while the reported East Village total is $474$. Tracing directly to page 1 of the official DSDP report (*December-2018-Homeless-Count_FINAL.pdf*), the source table itself prints:
* `East Village`: $474$
* `North East EV`: $68$
* `North West EV`: $45$
* `South East EV`: $361$
* `South West EV`: $30$  
This confirms that the $+30$ discrepancy originated inside DSDP's own published arithmetic, not an ingestion error.

### Deep Dive: 2019 Duplication Anomaly
In `RawCounts_AllYears.csv`, the sub-area values for all 12 months of 2019 are verbatim duplicates of the 2020 numbers. For example:
* **Jan 2019 CSV sub-areas:** NE=65, NW=88, SE=282, SW=32 (Sum = 467). True Jan 2019 EV total = 543. Difference = $-76$.
* **Jan 2020 CSV sub-areas:** NE=65, NW=88, SE=282, SW=32 (Sum = 467). Jan 2020 EV total = 467. Difference = $0$.

> **Recommendation for Task 1.2 / 1.3:** Replace the duplicated 2019 East Village sub-area records with the true monthly breakout numbers extracted from the 2019 DSDP PDF reports (*March-2019-Homeless-Sleep-Count.pdf*, *July-2019-Homeless-Count-Final.pdf*, etc.).

---

## 4. Source Report Sample Audit (45-Cell Audit Table)

A sample of 45 cells was drawn using pseudo-random sampling with a fixed seed (`random_state=42`) from `RawCounts_AllYears.csv`. Each cell was audited against the corresponding official DSDP PDF report.

| # | Year | Month | Area | Component | CSV Value | Source PDF Value | Source PDF Reference | Status | Notes |
| :-: | :-: | :--- | :--- | :--- | :-: | :-: | :--- | :-: | :--- |
| **1** | 2017 | Feb | Marina | total | 62.0 | 62.0 | Dec-2018 PDF (p.1) | **MATCH** | Exact match in 2017 summary table |
| **2** | 2017 | Oct | East Village | total | 649.0 | 649.0 | Dec-2018 PDF (p.1) | **MATCH** | Exact match in 2017 summary table |
| **3** | 2018 | Apr | South West EV | total | 41.0 | 41.0 | Apr-2018 PDF (p.1) | **MATCH** | Exact match in EV breakout table |
| **4** | 2018 | Dec | Core | individual | 121.0 | 121.0 | Dec-2018 PDF (p.1) | **MATCH** | Exact match from Core breakdown |
| **5** | 2018 | Feb | Gaslamp | tent | 0.0 | 0.0 | Feb-2018 PDF (p.8) | **MATCH** | Exact match in count breakdown |
| **6** | 2018 | Jan | Marina | tent | 2.0 | 2.0 | Jan-2018 PDF (p.4) | **MATCH** | Exact match in count breakdown |
| **7** | 2018 | June | Marina | vehicle | 0.0 | 0.0 | Jun-2018 PDF (p.4) | **MATCH** | Exact match in count breakdown |
| **8** | 2018 | May | Marina | vehicle | 1.0 | 1.0 | May-2018 PDF (p.4) | **MATCH** | Exact match in count breakdown |
| **9** | 2019 | Apr | Cortez | total | 44.0 | 44.0 | Apr-2019 PDF (p.1) | **MATCH** | Exact match in summary table |
| **10** | 2019 | Dec | City Center | tent | 11.0 | 11.0 | Dec-2019 / Jan-2020 PDF | **MATCH** | Exact match in City Center breakdown |
| **11** | 2019 | July | City Center | vehicle | 0.0 | 0.0 | Jul-2019 PDF (p.4) | **MATCH** | Exact match in count breakdown |
| **12** | 2019 | July | Columbia | total | 52.0 | 52.0 | Jul-2019 PDF (p.1) | **MATCH** | Exact match in summary table |
| **13** | 2019 | Mar | Columbia | tent | 9.0 | 9.0 | Mar-2019 PDF (p.5) | **MATCH** | Exact match in count breakdown |
| **14** | 2019 | Nov | Columbia | individual | 22.0 | 22.0 | Nov-2019 PDF (p.5) | **MATCH** | Exact match in count breakdown |
| **15** | 2019 | Nov | Gaslamp | tent | 2.0 | 2.0 | Nov-2019 PDF (p.8) | **MATCH** | Exact match in count breakdown |
| **16** | 2020 | Apr | East Village | tent | 39.0 | 39.0 | Apr-2020 PDF (p.2) | **MATCH** | Exact match in EV breakdown |
| **17** | 2020 | Dec | Columbia | individual | 46.0 | 46.0 | Dec-2020 PDF (p.5) | **MATCH** | Exact match in count breakdown |
| **18** | 2020 | Feb | Columbia | tent | 6.0 | 6.0 | Feb-2020 PDF (p.5) | **MATCH** | Exact match in count breakdown |
| **19** | 2020 | June | Columbia | vehicle | 0.0 | 0.0 | Jun-2020 PDF (p.5) | **MATCH** | Exact match in count breakdown |
| **20** | 2021 | Feb | Gaslamp | tent | 1.0 | 1.0 | Feb-2021 PDF (p.8) | **MATCH** | Exact match in count breakdown |
| **21** | 2021 | July | East Village | vehicle | 9.0 | 9.0 | Jul-2021 PDF (p.2) | **MATCH** | Exact match in EV breakdown |
| **22** | 2021 | Mar | City Center | vehicle | 0.0 | 0.0 | Mar-2021 PDF (p.4) | **MATCH** | Exact match in count breakdown |
| **23** | 2022 | Aug | Gaslamp | individual | 44.0 | 44.0 | Aug-2022 PDF (p.8) | **MATCH** | Exact match in count breakdown |
| **24** | 2022 | Dec | City Center | total | 271.0 | 271.0 | Dec-2022 PDF (p.1) | **MATCH** | Exact match in summary table |
| **25** | 2022 | Dec | Gaslamp | vehicle | 0.0 | 0.0 | Dec-2022 PDF (p.8) | **MATCH** | Exact match in count breakdown |
| **26** | 2022 | July | City Center | total | 234.0 | 234.0 | Jul-2022 PDF (p.1) | **MATCH** | Exact match in summary table |
| **27** | 2022 | Mar | City Center | total | 214.0 | 214.0 | Mar-2022 PDF (p.1) | **MATCH** | Exact match in summary table |
| **28** | 2022 | May | Marina | tent | 0.0 | 0.0 | May-2022 PDF (p.6) | **MATCH** | Exact match in count breakdown |
| **29** | 2022 | Nov | City Center | total | 235.0 | 235.0 | Nov-2022 PDF (p.1) | **MATCH** | Exact match in summary table |
| **30** | 2023 | Aug | Cortez | total | 65.0 | 65.0 | Mar-2024 / Aug-2023 PDF | **MATCH** | Exact match in summary table |
| **31** | 2023 | July | East Village | vehicle | 10.0 | 10.0 | Jul-2023 PDF (p.2) | **MATCH** | Exact match in EV breakdown |
| **32** | 2023 | May | Cortez | tent | 39.0 | 39.0 | May-2023 PDF (p.7) | **MATCH** | Exact match in count breakdown |
| **33** | 2023 | May | Marina | individual | 28.0 | 28.0 | May-2023 PDF (p.6) | **MATCH** | Exact match in count breakdown |
| **34** | 2023 | Sept | Marina | vehicle | 0.0 | 0.0 | Sep-2023 PDF (p.6) | **MATCH** | Exact match in count breakdown |
| **35** | 2024 | June | Cortez | tent | 13.0 | 13.0 | Jun-2024 PDF (p.7) | **MATCH** | Exact match in count breakdown |
| **36** | 2024 | Mar | Columbia | individual | 36.0 | 36.0 | Mar-2024 PDF (p.5) | **MATCH** | Exact match in count breakdown |
| **37** | 2025 | Apr | Cortez | individual | 49.0 | 49.0 | Apr-2025 PDF (p.6) | **MATCH** | Exact match in count breakdown table |
| **38** | 2025 | Apr | Gaslamp | vehicle | 0.0 | 0.0 | Apr-2025 PDF (p.8) | **MATCH** | Exact match in count breakdown table |
| **39** | 2025 | Apr | South East EV | total | 43.0 | 27.0 | Apr-2025 / Jun-2025 (p.1) | **DISCREPANCY** | Source PDF reports 27; CSV has 43.0 |
| **40** | 2025 | Aug | City Center | total | `NaN` | `NaN` | Not Published / Future | **VALID NaN** | Unreleased count month |
| **41** | 2025 | Feb | East Village | total | 409.0 | 409.0 | Feb-2025 PDF (p.1) | **MATCH** | Exact match in summary table |
| **42** | 2025 | July | Columbia | individual | `NaN` | `NaN` | Not Published / Future | **VALID NaN** | Unreleased count month |
| **43** | 2025 | July | Cortez | vehicle | `NaN` | `NaN` | Not Published / Future | **VALID NaN** | Unreleased count month |
| **44** | 2025 | June | East Village | individual | 291.0 | 291.0 | Jun-2025 PDF (p.3) | **MATCH** | Exact match in count breakdown table |
| **45** | 2025 | Nov | East Village | individual | `NaN` | `NaN` | Not Published / Future | **VALID NaN** | Unreleased count month |

---

## 5. Discrepancy Log & Error Rate Calculation

### Discrepancy Log

| Sample ID | Year | Month | Area | Component | File Value | Source Value | Discrepancy | Impact & Root Cause Analysis |
| :-: | :-: | :--- | :--- | :--- | :-: | :-: | :-: | :--- |
| **39** | 2025 | Apr | South East EV | total | **43.0** | **27.0** | **+16.0** | In `RawCounts_AllYears.csv`, April 2025 EV sub-areas were recorded as NE=264, NW=53, SE=43, SW=41 (summing to 401). In DSDP's published breakout table, the numbers are NE=193, NW=51, SE=27, SW=32 (summing to 303 preliminary, later revised). File value 43 reflects an unverified manual entry. |

### Error Rate Metrics:
$$\text{Observed Error Rate (Published Cells)} = \frac{1 \text{ discrepancy}}{41 \text{ published cells audited}} = \mathbf{2.44\%}$$

$$\text{Total Sample Error Rate (All Cells)} = \frac{1 \text{ discrepancy}}{45 \text{ total sampled cells}} = \mathbf{2.22\%}$$

* **Transcription Accuracy:** $\mathbf{97.56\%}$ of audited published values match the original DSDP source documents with 100% precision.

---

## 6. Recommendations for Downstream Tasks (Assignment 1)

1. **Recode Historical Area Names (Task 1.2):**
   * Standardize all occurrences of `area == 'Core'` to `'City Center'`.
   * Standardize component labels to lowercase (`total`, `individual`, `tent`, `vehicle`).
2. **Correct East Village 2019 Sub-Areas (Task 1.2 / 1.3):**
   * Overwrite the duplicate 2020 values currently residing in the 2019 East Village sub-area rows with genuine 2019 values extracted from the monthly PDF reports.
3. **Handle Missing & Partial Data Appropriately (Task 1.4):**
   * Document in the data dictionary that 2025 records for July, August, October, and November represent unreleased or cancelled counts and should remain as missing (`NaN`), not zeros.
4. **Methodology Weight Adjustment (Task 1.3):**
   * When building `MasterCounts_Adjusted_v2.csv`, ensure that multipliers are applied consistently:
     * **Pre-April 2017:** 2.0 per tent, 2.0 per vehicle
     * **Apr 2017 – May 2018:** 1.75 per tent, 1.66 per vehicle
     * **May 2018 – Jan 2020:** 1.75 per tent, 2.03 per vehicle
     * **Post-2020:** Unweighted raw counts (or DSDP continuous multipliers as specified in Task 1.3).
