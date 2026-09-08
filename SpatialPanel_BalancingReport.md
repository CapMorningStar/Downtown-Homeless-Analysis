# Spatial Panel Balancing Report (Task 3.3)

**Downtown San Diego Homeless Population Analysis**
**Author:** Kyaw Soe Lwin (`kylwin@ucsd.edu`)
**Project Lead:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)
**Scope:** `data/BlockLevel_Counts_clean.csv` — 12 digitized count dates, 2018–2025

---

## 1. The Issue: An Unbalanced Spatial Panel

Block-level coverage is **not constant over time**. Grouping `BlockLevel_Counts_clean.csv` by `count_date` and counting distinct `block_id`s shows a hard break:

| Period | Dates | Blocks per date |
|---|---|---|
| 2018–2021 | 2018-01-24, 2018-02-21, 2019-01-31, 2020-01-31, 2020-02-26, 2021-01-28, 2021-02-25 (7 dates) | **261** |
| 2022–2025 | 2022-01-27, 2022-03-01, 2023-01-31, 2024-01-25, 2025-01-31 (5 dates) | **382** |

No block present in the early era is ever absent later (the early 261 are a strict subset of the later 382) — this is a **footprint expansion**, not attrition or resampling.

The 121 blocks added starting 2022-01-27 belong to exactly three neighborhoods that do not appear on **any** date before 2022:

| New neighborhood | Blocks added |
|---|---:|
| Golden Hill | 52 |
| Barrio Logan | 35 |
| Sherman Heights | 34 |
| **Total** | **121** |

These three areas are canonically rolled up into "Outside Perimeter" in `Downtown_BlockGrid_clean.csv`'s neighborhood grouping, consistent with `Neighborhood_Crosswalk.csv` from Task 1.2.

**Implication:** any block-level or neighborhood-level spatial statistic computed on the raw 382-block file (Getis-Ord Gi*, Moran's I, density heatmaps, etc.) that spans the 2021→2022 boundary conflates a **real change in unsheltered counts** with a **change in what was measured** — the study area itself grew by 46% in block count that year.

---

## 2. Quantifying the Footprint Effect

For each post-2021 date, the DSDP-multiplier-weighted adjusted total (`individuals×1.00 + tents×1.75 + vehicles×vehicle_mult`, per `docs/MethodologyChangeLog.md`) was computed two ways: across all 382 blocks, and restricted to only the 261 blocks that exist in every count date.

| Date | Full 382-block total | Balanced 261-block total | Expansion delta | % of full total from expansion |
|---|---:|---:|---:|---:|
| 2022-01-27 | 1,408.53 | 1,149.07 | 259.46 | 18.42% |
| 2022-03-01 | 1,392.47 | 1,158.22 | 234.25 | 16.82% |
| 2023-01-31 | 1,955.09 | 1,314.49 | 640.60 | 32.77% |
| 2024-01-25 | 1,018.98 | 981.80 | 37.18 | 3.65% |
| 2025-01-31 | 847.33 | 762.90 | 84.43 | 9.96% |

*(Full detail in `data/SpatialPanel_FootprintEffect.csv`.)*

**Reading:** the footprint effect is not constant — it ranges from ~4% to ~33% of the reported total, peaking in 2023-01-31. Any raw year-over-year comparison using the full 382-block file overstates growth in those years by these margins, since 4–33 points of the "total" simply didn't exist as measured territory before 2022.

**Cross-check — is the post-2021 rise real, or purely the footprint?** Running the balanced 261-block panel across *all 12 dates* (not just post-2021) shows the underlying trend even with the expansion fully removed:

| Date | Balanced 261-block total |
|---|---:|
| 2018-01-24 | 804.49 |
| 2018-02-21 | 854.36 |
| 2019-01-31 | 891.21 |
| 2020-01-31 | 786.89 |
| 2020-02-26 | 742.99 |
| 2021-01-28 | 702.65 |
| 2021-02-25 | 671.42 |
| 2022-01-27 | 1,149.07 |
| 2022-03-01 | 1,158.22 |
| 2023-01-31 | 1,314.49 |
| 2024-01-25 | 981.80 |
| 2025-01-31 | 762.90 |

The 261-block-only total still jumps from 671.42 (2021-02-25) to 1,149.07 (2022-01-27), a +71% increase **on the same fixed set of blocks**. This confirms the 2021→2022 rise reflects a genuine increase in the unsheltered count within the original study area, on top of — not merely caused by — the separate footprint expansion. Both effects are real and must be reported separately.

---

## 3. Deliverable: The Balanced Panel

`data/BlockPanel_Balanced_261.csv` was built by restricting `BlockLevel_Counts_clean.csv` to the 261 `block_id`s present on all 12 count dates.

* **Shape:** 3,132 rows = 261 blocks × 12 dates (verified).
* **Schema:** identical to the source file (`block_id`, `neighborhood`, `source_neighborhood`, `count_date`, `individuals`, `tents_structures`, `vehicles`).
* **Excluded:** all rows for Golden Hill, Barrio Logan, and Sherman Heights blocks (121 blocks, only present 2022+).
* The full 382-block file (`BlockLevel_Counts_clean.csv`) is left untouched and remains the correct source for any **recent-period-only** analysis (2022–2025) that needs full study-area coverage.

**Build script:** `build_balanced_panel.py` (also emits `data/SpatialPanel_FootprintEffect.csv`).

---

## 4. Warning for Assignment 5 (Geospatial Hotspot Analysis)

> ⚠️ **Any hotspot comparison (Getis-Ord Gi*, Moran's I, or density change maps) that spans the 2021→2022 boundary must use `data/BlockPanel_Balanced_261.csv`, not the full 382-block file.**
>
> The full file's added footprint (Golden Hill, Barrio Logan, Sherman Heights) has no pre-2022 baseline — computing a "hotspot emerged" or "hotspot intensified" result for those blocks, or for neighborhood aggregates that include them, across that boundary would be comparing against blocks that were never measured, not against a true zero or prior value.
>
> Hotspot analysis restricted entirely to 2022–2025 (all within the expanded era) may safely use the full 382-block file, since coverage is constant across those 5 dates.

This warning is also logged in `PROJECT_CONTEXT.md` §4 (Task 3.3) for downstream sessions.

---

## 5. Summary

* Confirmed: block coverage steps from 261→382 blocks exactly at the 2021→2022 boundary, driven by the addition of Golden Hill, Barrio Logan, and Sherman Heights (121 blocks, 0 blocks dropped).
* Quantified: the footprint expansion inflates post-2021 full-panel totals by 3.65%–32.77% depending on date.
* Confirmed independently: even with the footprint held constant (balanced 261-block panel), the 2021→2022 rise is real (+71% on the same blocks) — not an artifact of coverage growth.
* Delivered: `data/BlockPanel_Balanced_261.csv` (balanced panel, 3,132 rows) and `data/SpatialPanel_FootprintEffect.csv` (per-date expansion quantification), with the full 382-block file preserved for recent-period-only use.
* Flagged: explicit warning carried into Assignment 5 to gate any cross-boundary hotspot comparison on the balanced panel.
