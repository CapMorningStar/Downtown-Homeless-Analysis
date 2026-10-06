# Task 5.1: Spatial Dataset Preparation and Global Spatial Autocorrelation

**Project:** Downtown San Diego Homeless Population Analysis  
**Scope:** Assignment 5, Task 5.1  
**Source data:** `BlockPanel_Balanced_261.csv`, `BlockLevel_Counts_clean.csv`, and `Downtown_BlockGrid.geojson`

## Objective

Prepare validated block-level spatial analysis datasets and test whether adjusted unsheltered counts are globally clustered rather than randomly distributed across Downtown San Diego blocks.

## Analysis design

Two analyses are intentionally separated to avoid mistaking a change in the measured footprint for a spatial change:

| Analysis scope | Dates | Blocks | Appropriate use |
|---|---:|---:|---|
| `balanced_261` | 12 dates, 2018-2025 | 261 | Comparisons spanning the 2021-2022 coverage break |
| `full_382_recent` | 5 dates, 2022-2025 | 382 | Recent-period-only analysis after coverage became constant |

The 121 blocks added in 2022 (Golden Hill, Barrio Logan, and Sherman Heights) are excluded from the balanced panel. This follows Task 3.3's documented footprint warning.

## Data preparation and validation

- Counts were joined to the polygon grid on `block_id` with a many-to-one validation.
- The count panel's `source_neighborhood` was compared to the GeoJSON `neighborhood`, the field pairing established in Task 3.2.
- The outcome is DSDP methodology-adjusted count:

  `individuals + 1.75 * tents_structures + vehicle_multiplier * vehicles`

  Vehicle multiplier is 1.66 before June 2018 and 2.03 from June 2018 forward.
- All zero-count blocks remain in the analysis; removing them would bias a global clustering statistic.

## Spatial weights and inference

Queen-contiguity weights were built from the validated block polygons with GeoPandas and libpysal. Blocks are neighbors when they share an edge or vertex. The binary weights were row-standardized before analysis.

| Scope | Undirected queen edges | Islands |
|---|---:|---:|
| Balanced 261-block panel | 924 | 0 |
| Full 382-block recent panel | 1,321 | 0 |

For each date, global Moran's I was evaluated with esda using 9,999 random permutations (`p_sim`) and a fixed random seed (`20260910`) for reproducibility.

## Results

### Balanced 261-block panel

| Date | Moran's I | Permutation p (`p_sim`) |
|---|---:|---:|
| 2018-01-24 | 0.2250 | 0.0001 |
| 2018-02-21 | 0.2387 | 0.0001 |
| 2019-01-31 | 0.0628 | 0.0328 |
| 2020-01-31 | 0.0944 | 0.0082 |
| 2020-02-26 | 0.1045 | 0.0038 |
| 2021-01-28 | 0.1229 | 0.0018 |
| 2021-02-25 | 0.1857 | 0.0001 |
| 2022-01-27 | 0.0850 | 0.0074 |
| 2022-03-01 | 0.1112 | 0.0010 |
| 2023-01-31 | 0.1502 | 0.0003 |
| 2024-01-25 | 0.1012 | 0.0039 |
| 2025-01-31 | 0.1123 | 0.0050 |

### Full 382-block recent panel

| Date | Moran's I | Permutation p (`p_sim`) |
|---|---:|---:|
| 2022-01-27 | 0.1425 | 0.0008 |
| 2022-03-01 | 0.1661 | 0.0001 |
| 2023-01-31 | 0.2425 | 0.0001 |
| 2024-01-25 | 0.1429 | 0.0004 |
| 2025-01-31 | 0.1455 | 0.0006 |

## Interpretation and limitations

All evaluated dates show positive, statistically significant global spatial autocorrelation. In plain terms, blocks with similar adjusted counts are geographically more clustered than expected under random reassignment of counts to blocks. The effect is weakest but still significant in the balanced January 2019 panel (I = 0.0628, p = 0.0328), and strongest in the full recent January 2023 panel (I = 0.2425, p = 0.0001).

Global Moran's I establishes clustering across the full study area; it does not identify the particular hot or cold blocks. Task 5.2 will use local Getis-Ord Gi* analysis for that purpose. The March 2022 source-map anomaly remains flagged from Task 3.1, so its result should be retained but interpreted with appropriate caution.

## Deliverables

- `build_spatial_autocorrelation.py` — reproducible analysis build script.
- `data/SpatialAnalysis_AnalysisReady.csv` — joined long-format block/date data for both scopes (5,042 rows).
- `data/SpatialWeights_Queen.csv` — 2,642 directed queen-neighbor links.
- `data/SpatialAutocorrelation_Results.csv` — 17 Moran's I results and inference diagnostics.
