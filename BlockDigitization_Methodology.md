# Block Digitization Methodology (Task 3.4)

**Downtown San Diego Homeless Population Analysis**
**Author:** Kyaw Soe Lwin (kylwin@ucsd.edu)
**Project Lead:** Adir Mancebo Jr. (adir@datasciencealliance.org)
**Target dataset:** `data/BlockLevel_Counts_clean.csv` (3,737 rows, 261–382 blocks depending on era, 12 count dates, Jan 2018 – Jan 2025)
**Source archive:** Downtown San Diego Partnership (DSDP) Clean & Safe monthly block-map PDF packets

This document formalizes, as a standalone methodology reference, how the block-level dataset was produced and validated. It draws on the audit work already performed and documented in `BlockDigitization_ValidationReport.md` (Task 3.1) and `data/BlockGrid_GeometryValidation.csv` (Task 3.2); it does not repeat new analysis, only consolidates the method into one reference document as required by Task 3.4.

---

## 1. How Blocks Were Identified

Each of the 382 downtown blocks in `Downtown_BlockGrid_clean.csv` / `Downtown_BlockGrid.geojson` is defined by:

* A unique `block_id` (a slug built from the two bounding streets, e.g. `16TH_ST_C_ST`).
* Four boundary streets (`st_north`, `st_east`, `st_south`, `st_west`) that correspond directly to the avenue/street grid lines printed on each DSDP source map page.
* A polygon geometry and centroid (validated in Task 3.2: 0 invalid geometries, 0 unclosed rings, 380/382 centroids contained in their own polygon).
* A `neighborhood` assignment (one of 7 canonical downtown neighborhoods, or "Outside Perimeter" for Barrio Logan / Golden Hill / Sherman Heights, per `Neighborhood_Crosswalk.csv`).

DSDP's own maps are organized one page per neighborhood per count date, with a hand-drawn or printed street grid matching this same boundary-street structure — including a separate "South" sub-area page for some neighborhoods (e.g. East Village's Island Ave./J–L St. blocks, labeled "East Village South" in the map coverage log, which maps to `sub_area = South East EV` under the `East Village` parent).

## 2. How Counts Were Read From the Maps

Two approaches were used, in sequence:

1. **Cell-level visual read (attempted, not used for final validation).** Individual grid cells on the source maps were initially targeted for a stratified sample read (see §3.1 of the Task 3.1 report). Older PDFs (2018–2021) are scanned, rotated 90°, and hand-annotated with small, sometimes crossed-out digits, making cell-level identification unreliable at scale — several sampled blocks also fall on irregular freeway- or park-boundary parcels where the cell shape itself is ambiguous. This approach was abandoned as a validation method after repeated failed attempts on a reduced 48-row sample.
2. **Page-level Count Breakdown totals (used for all validation).** Every neighborhood's map page carries a printed "Count Breakdown" table — Individual, Vehicle, and Tent **Count** and **Value** columns, with a grand **Total** — that is self-checkable: `Total = Individual + Vehicle × vehicle_multiplier + Tent × tent_multiplier`, where the multiplier follows the documented regime schedule (`docs/MethodologyChangeLog.md`: 1.66 or 2.03 per vehicle, 1.75 per tent, depending on date). Every printed total used in validation was independently re-derived from this arithmetic before being accepted as ground truth.

The digitized panel itself (`BlockLevel_Counts_clean.csv`) was delivered pre-digitized at the block level (one row per block per count date, with `individuals`, `tents_structures`, `vehicles` columns); this task's role was to validate that digitization against the source maps, not to perform the original cell-by-cell transcription.

## 3. Quality Control Procedures

* **Self-checking arithmetic.** Every source page's printed total was checked against `Individual + Vehicle×multiplier + Tent×multiplier` before use. This caught and corrected several initial misreads during validation (e.g. "287" vs. the correct "281"; a vehicle value that only reconciled at count=2, not 1).
* **Neighborhood-total cross-check.** For each of the 12 digitized dates, every neighborhood's page total was compared against the sum of that neighborhood's blocks in `BlockLevel_Counts_clean.csv`. Full results in `data/blocklevel_page_audit_results.csv` (87 rows, all 12 dates).
* **Null resolution against the primary source.** The single null in the panel (`tents_structures`, block `16TH_ST_C_ST`, 2020-01-31) was re-verified directly against the source map image (not just cross-block pattern inference): the corresponding grid cell is completely blank, consistent with 0/0/0 on all 11 other dates for that block. Confirmed a true zero, not a missing/ambiguous read.
* **Implausibility screening.** The full panel was screened for negative values (0 found), zero-individual-with-structure-present rows (136/622, expected under DSDP's counting protocol — a visible tent/vehicle is counted even with no occupant visible), and extreme single-block concentrations (19 rows, flagged as candidate hotspots for Assignment 5, not errors).
* **Geometric/spatial QC.** Independently of the count values, the block grid itself was validated for polygon validity, centroid containment, and boundary-street consistency with neighboring blocks (Task 3.2: 380/382 blocks pass every check; the 2 exceptions are non-convex freeway-interchange parcels, not defects).
* **Coverage reconciliation.** Every digitized count date was confirmed to have a full set of "Yes" (map present) rows in `BlockMap_Coverage_clean.csv` (see `BlockMapCoverage_GapAnalysis.md`), and any digitized date drawn from a map rated "Unclear" was explicitly flagged rather than silently accepted.

## 4. How Disagreements Were Resolved

* **Small discrepancies (±1–8 units, 28 of 87 audited cells).** The recurring pattern is individuals and tents shifting against each other while the neighborhood total or vehicle count stays exact — consistent with occasional ambiguity between "resident visible next to structure" vs. "structure only" at the moment of the original count, not a digitization pipeline defect. These are documented and retained as-is; no correction was applied, since the printed source total (the higher-confidence figure) still reconciles with the digitized aggregate within a small margin.
* **Large, isolated disagreement (2022-03-01, 9 of 28 discrepancies, gaps of 10–60+ units).** Traced to a genuine source-side irregularity: the handwritten "Date:" field on the source PDF varies within the same document (3/24/22 on some neighborhood pages, 3/29/22 on others), neither matching the CSV's normalized `2022-03-01` label. This was **not resolved by correcting the digitized data** — the printed arithmetic on every page is internally self-consistent, so the underlying disagreement is about which count period the source represents, not a reading error. It is instead carried forward as an explicit, documented flag for follow-up before use in Assignment 4/5 modeling (see `BlockDigitization_ValidationReport.md` §3.4 and §6).
* **Unverifiable cells (6 of 87, Barrio Logan/Golden Hill/Sherman Heights on 2024-01-25 and 2025-01-31).** These pages have scattered hand-drawn tallies but no printed Count Breakdown total. Rather than attempting a manual re-total of ambiguous marks (the same failure mode that ruled out the cell-level approach), these were left as documented "unverifiable" rather than forced to a resolution — they represent a small fraction of the panel (expected values of 1–5 individuals) and do not materially affect the audit's conclusions.
* **Unbalanced spatial coverage (261 vs. 382 blocks).** Not a disagreement to resolve at the data level — documented and structurally addressed in Task 3.3 by producing a separate balanced 261-block panel (`data/BlockPanel_Balanced_261.csv`) for valid cross-era comparison, while preserving the full 382-block file for recent-period analysis.

## 5. Summary of Prior Validation Work Referenced

| Deliverable | Task | What it covers |
|---|---|---|
| `BlockDigitization_ValidationReport.md` | 3.1 | Full page-level audit (87 neighborhood×date cells, 12 dates), null resolution, implausibility screen |
| `data/blocklevel_page_audit_results.csv` | 3.1 | Row-level audit results underlying the report above |
| `data/BlockGrid_GeometryValidation.csv` | 3.2 | Polygon validity, centroid containment, boundary-street consistency for all 382 blocks |
| `data/BlockPanel_Balanced_261.csv`, `SpatialPanel_BalancingReport.md` | 3.3 | Balanced-panel construction for the 261-vs-382-block coverage discontinuity |
| `data/BlockMapCoverage_GapAnalysis.csv`, `BlockMapCoverage_GapAnalysis.md` | 3.4 | Reconciliation of the coverage table and quantification of the undigitized-map gap |

This methodology document is intended as the single reference point for "how was this data produced and checked" going into Assignments 4 and 5, so downstream analysts do not need to re-derive it from the individual task reports.
