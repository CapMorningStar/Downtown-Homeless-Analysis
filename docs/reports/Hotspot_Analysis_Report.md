# Task 5.2: Getis-Ord Gi* Hotspot Analysis

**Project:** Downtown San Diego Homeless Population Analysis  
**Scope:** Assignment 5, Task 5.2  
**Outcome:** DSDP methodology-adjusted block-level unsheltered count

## Objective

Identify blocks whose adjusted counts occur in statistically significant local clusters of high values (hotspots) or low values (cold spots), then preserve comparable results across time without confounding them with the 2022 study-area expansion.

## Spatial scope

All 12 dates use the 261-block balanced panel from Task 3.3. The 121 blocks added in 2022 are excluded from every time-comparative calculation. This fixes the footprint across 2018-2025 and prevents a block's first appearance in the data from being mistaken for hotspot emergence.

## Method

- **Polygons:** `Downtown_BlockGrid.geojson`, filtered to the balanced 261 block IDs.
- **Outcome:** `individuals + 1.75 × tents_structures + vehicle_multiplier × vehicles`; vehicle multiplier is 1.66 before June 2018 and 2.03 afterward.
- **Weights:** libpysal queen contiguity; blocks sharing an edge or vertex are neighbors. The 261-block network has no islands.
- **Statistic:** esda `G_Local` with `star=True`, so the focal block is included in its Gi* neighborhood; weights are row-standardized internally for each date.
- **Inference:** 9,999 conditional random permutations per date, a deterministic date-derived seed, and permutation p-values.
- **Classification:** `hotspot_99` (z ≥ 2.576 and p < 0.01), `hotspot_95` (z ≥ 1.96 and p < 0.05), analogous cold-spot categories for negative z, otherwise `not_significant`.

## Results summary

| Date | 95% hotspots | 99% hotspots | Cold spots | Not significant |
|---|---:|---:|---:|---:|
| 2018-01-24 | 3 | 0 | 0 | 258 |
| 2018-02-21 | 1 | 0 | 0 | 260 |
| 2019-01-31 | 2 | 1 | 0 | 258 |
| 2020-01-31 | 1 | 1 | 0 | 259 |
| 2020-02-26 | 1 | 0 | 0 | 260 |
| 2021-01-28 | 2 | 1 | 0 | 258 |
| 2021-02-25 | 2 | 3 | 0 | 256 |
| 2022-01-27 | 3 | 3 | 0 | 255 |
| 2022-03-01 | 4 | 3 | 0 | 254 |
| 2023-01-31 | 1 | 0 | 0 | 260 |
| 2024-01-25 | 0 | 0 | 0 | 261 |
| 2025-01-31 | 2 | 4 | 0 | 255 |

Positive local clustering is therefore concentrated in a small share of the fixed study footprint in 11 of 12 dates. No cold spots meet the configured 95% significance threshold. The March 2022 result remains flagged in the GeoJSON because Task 3.1 identified a source-map anomaly on that count date; it is retained for transparency but requires cautious interpretation.

## Deliverables

- `build_hotspot_analysis.py` — reproducible GeoPandas/libpysal/esda build script.
- `data/Hotspot_Classifications.geojson` — 3,132 block-date features, including Gi*, z-score, p-value, classification, adjusted count, and geometry.
- `data/Hotspot_Summary_ByDate.csv` — hotspot classifications aggregated by date.
- `Hotspot_Analysis_Report.md` — this methods and findings report.

## Next task

Task 5.3 should turn this GeoJSON into interpretable cartographic outputs. It should use the same fixed 261-block footprint for maps comparing dates across 2021-2022 and retain the March 2022 anomaly annotation.
