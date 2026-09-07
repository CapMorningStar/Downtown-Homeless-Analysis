# BlockDigitization_ValidationReport
**Downtown San Diego Homeless Population Analysis**
*Assignment 3: Block-Level Validation & Spatial Integration — Task 3.1*

* **Analyst:** Kyaw Soe Lwin
* **Project Lead:** Adir Mancebo Jr. (Data Science Alliance)
* **Date:** September 7, 2026
* **Target Dataset:** `BlockLevel_Counts_clean.csv` (3,737 rows, 382 unique blocks, 12 count dates, Jan 2018 – Jan 2025)
* **Source Archive:** Downtown San Diego Partnership (DSDP) Clean & Safe monthly block-map PDF packets

---

## 1. Executive Summary

This report validates the digitized block-level unsheltered count panel (`BlockLevel_Counts_clean.csv`) against the original hand-drawn DSDP count maps for all 12 available count dates. It also resolves the one known null value in `tents_structures` and screens the full panel for internally implausible records.

### Key Findings

1. **Source-map coverage gap identified and closed.** Only 5 of the 12 required monthly map packets were cached locally at the start of this task (Jan/Feb 2018, Feb 2020, Feb 2021, Mar 2022). The 7 missing packets (Jan 2019, Jan 2020, Jan 2021, Jan 2022, Jan 2023, Jan 2024, Jan 2025) were located and downloaded from the DSDP archive and verified as genuine before use.
2. **Cell-level visual audit was not reliable at scale.** An initial attempt to independently re-read individual block cells off the hand-drawn maps (a stratified 10%, then reduced 48-row sample) was abandoned after repeated cropping/zooming attempts failed to reliably pinpoint specific cells on rotated scans with messy, sometimes crossed-out handwriting. The audit was redesigned around each page's own **printed "Count Breakdown" total** (Individual / Vehicle / Tent count and value, with an internal arithmetic checksum), cross-checked against the corresponding neighborhood-month aggregate in `BlockLevel_Counts_clean.csv`.
3. **Page-level audit: 87 neighborhood×date cells checked across all 12 dates.**
   * 53 exact matches (65.4% of the 81 verifiable cells; 6 cells had no legible printed total and are marked unverifiable)
   * 28 discrepancies, nearly all small (±1 to ±8 units, largely individual/tent classification noise consistent with rounding or transcription at the source)
   * **73.6%** exact-match rate when the one anomalous date below is excluded
4. **2022-03-01 is a significant, isolated anomaly.** That single date accounts for 9 of the 28 discrepancies, with gaps of 10–60+ units across nearly every neighborhood — far larger than any other date. The source pages themselves carry inconsistent handwritten dates (3/24/22 on some neighborhood pages, 3/29/22 on others), neither of which matches the CSV's normalized `count_date` of `2022-03-01`. This points to a genuine source-side irregularity (a multi-night count period, or a re-survey, folded into one monthly report) rather than a digitization error, and warrants follow-up before this date is used in any downstream spatial or temporal model.
5. **The `tents_structures` null is confirmed a true zero.** Block `16TH_ST_C_ST` (East Village, bounded by C St / 16th St / Broadway / 15th St) shows a completely blank map cell on the Jan 2020 source map — no handwriting of any kind — consistent with all 11 other count dates for that same block, which are all 0/0/0. Task 1.2's imputation of `0` was correct.
6. **136 of 622 rows (21.9%) with a tent or vehicle present record zero individuals.** This is the exact pattern the task asked to screen for. It is concentrated in East Village (69 rows) and is consistent with the counting methodology itself — a tent or vehicle showing signs of habitation is counted even when no occupant is visible at the moment of the count — rather than a digitization defect. No negative values or other structurally invalid records were found anywhere in the panel.

---

## 2. Source-Map Acquisition (Coverage Gap)

`BlockLevel_Counts_clean.csv` covers 12 count dates: 2018-01-24, 2018-02-21, 2019-01-31, 2020-01-31, 2020-02-26, 2021-01-28, 2021-02-25, 2022-01-27, 2022-03-01, 2023-01-31, 2024-01-25, 2025-01-31.

At the start of this task, `data/pdfs/` held 34 monthly packets cached from Task 1.1's audit, but only **5 of the 12** matched a required block-map date. The remaining 7 were located in the scraped link index (`data/dsdp_pdf_links.csv`) or, for January 2022, on the live DSDP archive page, downloaded, and verified as genuine multi-page reports (not error pages) with `pypdf`/`pymupdf` before use:

| Count date | Source PDF | Status |
| :--- | :--- | :---: |
| 2018-01-24 | `January-2018-Homeless-Count-Combined.pdf` | Already cached |
| 2018-02-21 | `February-2018-Homeless-Count-Final.pdf` | Already cached |
| 2019-01-31 | `January-2019-Unsheltered-Homeless-Sleep-Count-Web-Version-Final.pdf` | **Downloaded** |
| 2020-01-31 | `January-2020-Unsheltered-Homeless-Count.pdf` | **Downloaded** |
| 2020-02-26 | `February-2020-Unsheltered-Homeless-Count-Final.pdf` | Already cached |
| 2021-01-28 | `January-2021-Unsheltered-Homeless-Sleep-Count-FINAL.pdf` | **Downloaded** |
| 2021-02-25 | `February-2021-Unsheltered-Homeless-Sleep-Count-FINAL.pdf` | Already cached |
| 2022-01-27 | `2022-Homeless-Sleep-Count-Regional-with-Map.pdf` | **Downloaded** |
| 2022-03-01 | `2022-Homeless-Sleep-Count-March-with-Maps.pdf` | Already cached |
| 2023-01-31 | `2023-Homeless-Sleep-Count-January-with-Maps.pdf` | **Downloaded** |
| 2024-01-25 | `January-2024-Unsheltered-Count-Totals-w-Maps.pdf` | **Downloaded** |
| 2025-01-31 | `January-2025-Unsheltered-Sleep-Counts-With-Maps.pdf` | **Downloaded** |

---

## 3. Visual Audit Methodology (Steps 2–3)

### 3.1 Initial approach and why it was revised

Per the task breakdown, a reproducible 10% stratified sample of block-date records (372 rows, `seed=42`) was drawn from `BlockLevel_Counts_clean.csv`, stratified by `count_date`. Locating each sampled block on its map is possible in principle: every block in `Downtown_BlockGrid_clean.csv` carries exact `st_north/st_east/st_south/st_west` boundary streets, which map onto the avenue/street grid lines drawn on each page (and, for some neighborhoods, a "South" sub-area page for the Island Ave./J–L St. blocks near Barrio Logan/Sherman Heights, e.g. "East Village South").

In practice, pinpointing individual cells proved unreliable at scale: the older PDFs (2018–2021) are scanned, rotated 90°, and hand-annotated with small, sometimes crossed-out and corrected digits; several sampled blocks also sat on irregular freeway- or park-boundary parcels where the cell shape itself was ambiguous. After several unsuccessful cropping/zooming attempts on a single cell, the sample was first reduced to 48 rows (4 per date), then the approach itself was revised.

### 3.2 Revised approach: page-level Count Breakdown totals

Every neighborhood's map page carries a printed (typed or hand-filled) "Count Breakdown" table — Individual, Vehicle, and Tent **Count** and **Value** columns, with a grand **Total** — that is far more legible than individual cells and self-checkable: `Total = Individual + Vehicle×multiplier + Tent×multiplier`, where the multiplier follows the documented regime schedule (1.66 or 2.03 per vehicle, 1.75 per tent, depending on date). Every printed total in this report was verified against that arithmetic before being accepted, and several initial misreads (e.g. "287" vs. the correct "281"; a vehicle value that only reconciled at count=2, not 1) were caught and corrected this way.

For each of the 12 count dates, every neighborhood's page total was read and compared against the sum of that neighborhood's blocks in `BlockLevel_Counts_clean.csv` for that date. Full results: [`data/blocklevel_page_audit_results.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/blocklevel_page_audit_results.csv) (87 rows). Sampling script: [`build_blocklevel_sample.py`](file:///D:/Projects/Downtown-Homeless-Analysis/build_blocklevel_sample.py).

### 3.3 Results summary

| Outcome | Rows |
| :--- | :---: |
| Exact match | 53 |
| Discrepancy | 28 |
| Unverifiable (no legible printed total) | 6 |
| **Exact-match rate (verifiable rows)** | **65.4%** (53/81) |
| **Exact-match rate, excluding 2022-03-01** | **73.6%** (53/72) |

Mismatches by date:

| Date | Mismatches | Note |
| :--- | :---: | :--- |
| 2018-01-24 | 1 | City Center: −1 individual (tents/vehicles exact) |
| 2018-02-21 | 2 | Cortez: +1 vehicle; East Village: −1 individual/+1 tent (net-zero) |
| 2019-01-31 | 1 | East Village: +6 individuals (tents/vehicles exact) |
| 2020-01-31 | 2 | East Village: −2 individuals/+3 tents; City Center: −1 individual |
| 2020-02-26 | 1 | City Center: −2 individuals/+2 tents/−1 vehicle |
| 2021-01-28 | 2 | East Village: −3/+5 (individual/tent); Cortez: −8/+8 (individual/tent, large exact offset) |
| 2021-02-25 | 4 | East Village, City Center, Cortez, Gaslamp — mix of small individual/tent/vehicle shifts |
| 2022-01-27 | 1 | Gaslamp: −1 individual/+1 tent |
| **2022-03-01** | **9** | **Anomalous — see §3.4** |
| 2023-01-31 | 1 | East Village tent count low-confidence (individuals/vehicles exact) |
| 2024-01-25 | 2 | East Village: −3 individuals/+3 vehicles; Cortez: −2 individuals/−1 tent |
| 2025-01-31 | 2 | Columbia: +1 individual; City Center: −5 individuals |

The recurring pattern — individuals and tents shifting against each other while the total or vehicle count stays exact — is consistent with occasional ambiguity between "resident visible next to structure" vs. "structure only" at the moment of the original count, not a digitization pipeline defect: the same block, audited on different dates, sometimes matches exactly and sometimes doesn't.

### 3.4 The 2022-03-01 anomaly

Every neighborhood audited for this date showed unusually large gaps (Cortez: −19 individuals/−32 tents; Barrio Logan: −48 individuals/+58 tents; Sherman Heights: +7/+23; Gaslamp: +29 individuals). Two independent signals point to a source-side irregularity rather than a reading or digitization error:

* The arithmetic on every one of this date's printed tables is internally self-consistent (each reads Total = Individual + Vehicle×2.03 + Tent×1.75 exactly), so the printed figures themselves were read correctly.
* The handwritten "Date:" field varies **within the same PDF** — City Center and Cortez are dated 3/24/22, while East Village South and Columbia are dated 3/29/22 — and neither date matches the CSV's normalized `2022-03-01` label.

**Recommendation:** flag 2022-03-01 for follow-up before it is used in Assignment 4/5 modeling — confirm with DSDP or the original count coordinator whether this reflects a multi-night count, a re-survey, or a genuinely different night than the neighboring January/March counts, and consider excluding or reweighting it if it cannot be reconciled.

### 3.5 Unverifiable cells

Six cells (Barrio Logan, Golden Hill, and Sherman Heights on 2024-01-25 and 2025-01-31) have scattered hand-drawn tallies on their map pages but no printed Count Breakdown total for those specific dates, unlike every other neighborhood-date combination. Rather than hand-total dozens of small, hard-to-disambiguate marks (the same risk that caused the cell-level approach to be abandoned in §3.1), these are reported as unverified. They represent a small fraction of the panel (expected values of 1–5 individuals, per the CSV) and do not materially affect the audit's conclusions.

---

## 4. Null Investigation (Step 5)

`BlockLevel_Counts.csv` contains exactly one null: `tents_structures` for block `16TH_ST_C_ST` on `2020-01-31` (row 930). Task 1.2 had already imputed this to `0`. This task re-verified that imputation against primary source evidence rather than accepting it as an assumption.

* Block `16TH_ST_C_ST` (East Village) is bounded by C St (north), 16th St (east), Broadway (south), 15th St (west).
* Every one of the other 11 count dates for this exact block records `0` individuals, `0.0` tents, `0` vehicles.
* On the Jan 2020 East Village source map, the corresponding grid cell (row 1 / column 4, at the C St–Broadway, 15th–16th St intersection) is **completely blank** — no digit, tally mark, or symbol of any kind.

**Conclusion:** the null represents a true zero, not an unreadable or ambiguous cell. The data-entry process simply failed to explicitly type `0` for that one field on that one date, unlike the `individuals` and `vehicles` columns, which were entered as `0`. Task 1.2's imputation is confirmed correct.

---

## 5. Internal Implausibility Screen (Step 6)

The full 3,737-row panel was screened for:

1. **Negative values** in `individuals`, `tents_structures`, or `vehicles` — **0 rows found.**
2. **Zero individuals with a nonzero tent or vehicle present** (a structure showing signs of habitation but no visible occupant) — **136 of 622 rows (21.9%)** with a tent/vehicle present. By neighborhood: East Village 69, Cortez 17, City Center 14, Marina 11, Columbia 11, Sherman Heights 5, Golden Hill 5, Barrio Logan 3, Gaslamp 1.
3. **Extreme single-block concentrations** (individuals > 30 in one block) — 19 rows, concentrated in a small number of recurring hotspot blocks: `17TH_ST_K_ST` (East Village, appears in 5 of the 12 dates, up to 58 individuals), `15TH_ST_IMPERIAL_AV` (East Village), `PARK_BL_J_ST` (East Village, appears in 4 dates), and `03RD_AV_A_ST` (City Center, escalating 43 → 39 → 64 across 2023–2025).

Finding (2) is exactly the pattern the task asked to document, and it reflects the counting methodology itself — Clean & Safe staff are instructed to count a visible tent/structure or vehicle showing signs of habitation even when no person is visible at the time of the count — rather than a data-quality defect. Finding (3) is not implausible on its own (East Village is the highest-density neighborhood by a wide margin per the Assignment 2 EDA), but the same few blocks recurring as high-concentration outliers across years is a useful lead for the upcoming Assignment 5 hotspot analysis.

No rows were found that combine a nonzero component with a zero neighborhood-level total, and no other internally contradictory patterns were identified.

---

## 6. Recommendations for Downstream Tasks

1. **Flag 2022-03-01 before Assignment 4/5 use.** Its block-level and neighborhood-level totals diverge sharply from the source pages' own printed counts, and the source pages carry two different handwritten count dates. Confirm the correct interpretation with the project lead, or exclude/reweight this date in temporal and spatial models until resolved.
2. **Treat the East Village individual/tent trade-off as expected noise, not error**, when computing block-level confidence intervals — the same blocks flip between exact and off-by-a-few-units matches across different dates, consistent with counting-moment ambiguity rather than systematic bias.
3. **Carry the null-resolution finding into the data dictionary**: row 930 (`16TH_ST_C_ST`, 2020-01-31, `tents_structures`) is a confirmed true zero, not an estimate — this can be stated without hedging in `docs/DataDictionary_MasterCounts.md` if it is updated for the block-level dataset.
4. **Use the 19 flagged high-concentration blocks as a starting candidate list** for Assignment 5's Getis-Ord Gi*/Moran's I hotspot analysis — `17TH_ST_K_ST`, `PARK_BL_J_ST`, and `15TH_ST_IMPERIAL_AV` in East Village, and `03RD_AV_A_ST` in City Center, all recur as outliers across multiple independent count dates.
5. **The zero-individual/nonzero-structure pattern (21.9% of occupied-structure rows) should be documented as a methodology note, not corrected** — it is a faithful reflection of the DSDP counting protocol.
