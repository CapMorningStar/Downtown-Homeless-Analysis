# Block Map Coverage Gap Analysis (Task 3.4)

**Downtown San Diego Homeless Population Analysis**
**Author:** Kyaw Soe Lwin (kylwin@ucsd.edu)
**Project Lead:** Adir Mancebo Jr. (adir@datasciencealliance.org)
**Scope:** `data/BlockMap_Coverage_clean.csv` (843 rows) vs. `data/BlockLevel_Counts_clean.csv` (12 digitized count dates)

---

## 1. Coverage Table Column Fix (Already Resolved in Task 1.2)

The Task 3.4 brief flags that the coverage table's original `block` column actually holds neighborhood/area names, not block IDs. Checking `data/BlockMap_Coverage.csv` (raw) against `data/BlockMap_Coverage_clean.csv` confirms **this was already corrected in Task 1.2**, before this task began:

* The raw file's `block` column (values: City Center, Columbia, Cortez, East Village, East Village South, Gaslamp, Marina, Barrio Logan, Golden Hill, Sherman Heights — 10 distinct labels) was renamed to **`source_area`** in the clean file.
* A new **`neighborhood`** column was added, mapping each `source_area` to its canonical parent via `data/Neighborhood_Crosswalk.csv` (e.g. "East Village South" → `East Village`; "Barrio Logan"/"Golden Hill"/"Sherman Heights" → `Outside Perimeter`).
* **Crosswalk completeness verified:** all 10 `source_area` values present in the coverage table have a matching `source_label` entry in `Neighborhood_Crosswalk.csv`. Zero unmapped values.

No further action was needed on this sub-item; it is documented here for completeness since the task notes call it out explicitly.

---

## 2. The Digitization Gap

`BlockMap_Coverage_clean.csv` logs map availability and quality for **96 distinct year-months** from January 2018 through December 2025, across up to 10 source areas per month (7 in 2018–2021, before Barrio Logan/Golden Hill/Sherman Heights coverage began; 10 from 2022 onward — the same 261→382 block transition documented in Task 3.3).

| Metric | Count |
|---|---:|
| Total year-months logged | 96 |
| Year-months with ≥1 map marked present (`block_map = Yes`) | 90 |
| Year-months with a map rated `Clear` | (773 of 843 rows overall) |
| **Year-months actually digitized** into `BlockLevel_Counts_clean.csv` | **12** |
| **Year-months with a usable map that was never digitized** | **78** |
| Digitization rate (digitized ÷ available) | **13.3%** |

**By year, undigitized-but-available months:**

| Year | Undigitized months with a usable map |
|---|---:|
| 2018 | 9 |
| 2019 | 10 |
| 2020 | 10 |
| 2021 | 10 |
| 2022 | 10 |
| 2023 | 11 |
| 2024 | 11 |
| 2025 | 7 |

*(Full per-year-month detail in `data/BlockMapCoverage_GapAnalysis.csv`.)*

### This is a documented limitation, not outstanding project work

Per the Task 3.4 brief, this gap is recorded here as a **known scope boundary**: the project's block-level spatial analysis (Assignments 3 and 5) works from the 12 dates that were digitized, roughly one count per year (two in some years) rather than the full monthly cadence available at the neighborhood/citywide level (`MasterCounts_Adjusted_v2.csv`, 2,814 rows, monthly since 2017). Digitizing the remaining 78 available map-months is explicitly **out of scope for this project** and is not queued as a future task — it would require the same page-by-page hand-transcription effort documented in `BlockDigitization_Methodology.md`, multiplied roughly 6.5×.

---

## 3. Digitized-Date Coverage Confirmation

Every one of the 12 digitized count dates was checked against the coverage table by year-month:

| Year-month | Coverage rows | Rows marked "Yes" | All rows "Yes"? | Unclear maps used |
|---|---:|---:|---|---|
| 2018-01 | 7 | 7 | ✅ | — |
| 2018-02 | 7 | 7 | ✅ | — |
| 2019-01 | 7 | 7 | ✅ | — |
| 2020-01 | 7 | 7 | ✅ | — |
| 2020-02 | 7 | 7 | ✅ | — |
| 2021-01 | 7 | 7 | ✅ | — |
| 2021-02 | 7 | 7 | ✅ | — |
| 2022-01 | 10 | 10 | ✅ | **2**: East Village South, Sherman Heights |
| 2022-03 | 10 | 10 | ✅ | **1**: East Village South |
| 2023-01 | 10 | 10 | ✅ | — |
| 2024-01 | 10 | 10 | ✅ | — |
| 2025-01 | 10 | 10 | ✅ | — |

**Result:** every digitized date has full "map present" coverage (no digitized date was drawn from a source with no logged map). However, **3 source-area/date combinations were digitized from a map rated "Unclear"**: East Village South on both 2022-01-27 and 2022-03-01, and Sherman Heights on 2022-01-27.

### Cross-reference to Task 3.1's independent finding

The **2022-03-01 East Village South "Unclear" flag corroborates** Task 3.1's independently-discovered "2022-03-01 anomaly" (`BlockDigitization_ValidationReport.md` §3.4): that date's audit found 9 of 28 discrepancies concentrated on 2022-03-01 alone, with the source PDF carrying two different handwritten count dates (3/24/22 vs. 3/29/22) neither matching the CSV's normalized label. The coverage table's own "Unclear" quality rating for that map was recorded independently (as part of the original coverage inventory, not the Task 3.1 audit) and points to the same underlying source-document problem from a second angle.

The 2022-01-27 flags (East Village South and Sherman Heights) did not surface as large discrepancies in the Task 3.1 page-level audit (2022-01-27 had only 1 mismatch, in Gaslamp), suggesting the "Unclear" rating there reflects legibility difficulty that did not ultimately compromise the printed Count Breakdown totals for those two areas — but this should be treated as a lower-confidence data point, consistent with its explicit "Unclear" rating.

---

## 4. Recommendations

1. **Do not schedule further digitization work** against the 78 undigitized-but-available months; treat the 12-date panel as the fixed scope for this project's block-level spatial analysis, per this documented limitation.
2. **Carry a lower-confidence flag** on East Village South (2022-01-27, 2022-03-01) and Sherman Heights (2022-01-27) into any block-level or sub-area analysis that weights by data quality.
3. **The 2022-03-01 date remains flagged for follow-up** (per Task 3.1's recommendation), now with a second, independent corroborating signal from the coverage table's own quality rating.
4. If additional months are ever digitized in a future phase, prioritize by year-over-year gap size — 2023 and 2024 currently have the most undigitized available months (11 each) despite being the most recent, best-quality maps.

---

## 5. Summary

* Confirmed the `block`→`source_area`/`neighborhood` column fix was already completed in Task 1.2; crosswalk mapping is complete for all 10 source areas.
* Quantified the digitization gap: 78 of 90 year-months with a usable map (86.7%) were never digitized — documented as an explicit, out-of-scope project limitation.
* Confirmed all 12 digitized dates have full map-present coverage, but flagged 3 source-area/date combinations digitized from "Unclear"-rated maps, one of which corroborates Task 3.1's independently-found 2022-03-01 anomaly.
* Deliverable: `data/BlockMapCoverage_GapAnalysis.csv` (96 rows, one per year-month, with availability/quality/digitized-status columns) and `build_coverage_gap_analysis.py` (build script).
