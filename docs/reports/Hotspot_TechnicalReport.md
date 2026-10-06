# Hotspot Technical Report

## Purpose and scope

This report completes Assignment 5 using Getis-Ord Gi* hotspot results for DSDP methodology-adjusted block-level unsheltered counts. All cross-time results use the balanced 261-block footprint over 12 count dates from 2018 through 2025. This avoids treating the 121 blocks added in 2022 as a geographic change. March 2022 is retained but flagged because the source-map audit identified inconsistent handwritten dates.

## Methods

Task 5.1 found positive, statistically significant global Moran's I on all 12 balanced-panel dates (range 0.063–0.239; permutation p ≤ 0.0328). Task 5.2 applied queen-contiguity, row-standardized Getis-Ord Gi* with 9,999 conditional permutations. A hotspot is `hotspot_95` or `hotspot_99`, requiring the configured z-score and permutation-p thresholds. Persistence is the number of hotspot classifications out of 12 dates; ties are resolved by mean Gi* z-score, then mean adjusted count.

The outcome remains the DSDP methodology-adjusted total: individuals plus 1.75 times tents/structures plus the applicable vehicle multiplier. Zero-count blocks remain in the analysis because removing them would change the spatial reference distribution. Queen contiguity treats blocks sharing either an edge or a vertex as neighbors. The result is an evidence base for local clustering, not a census of individual locations or a causal explanation for why concentration occurs.

## Map series

Four publication-quality maps accompany this report. Map 1 displays the number of count dates in which each block was a statistically significant hotspot, allowing a reader to distinguish persistent concentration from one-date signals. Maps 2 and 3 summarize maximum Gi* classification in the early (2018–2020) and recent (2022–2025) periods. They deliberately omit 2021 from the period contrast so the comparison centers on the initial and post-expansion eras without treating the coverage transition itself as a period boundary. Map 4 compares those two periods directly: a block is classified as `became hotspot` only when it had no early hotspot date and at least one recent hotspot date; `remained hotspot` requires one or more dates in both periods; `cooled off` is the inverse; and `never hotspot` covers the remaining blocks.

All four maps use the fixed 261-block footprint, include a north arrow, scale bar, source attribution, and colorblind-accessible colors. Their visual role is descriptive: the polygons show the geographic position of a block, while the color represents a Gi*-based classification or frequency. The interactive HTML map preserves the original per-date results so users can inspect the adjusted count, Gi* z-score, permutation p-value, and classification rather than relying only on an aggregated map.

## Persistence and contextual indicators

The top ten blocks are ranked in `Hotspot_Persistence_Ranking.csv`. Their nearest homeless/social-service and transit features were obtained from OpenStreetMap through the Overpass API on 2026-09-13. Distances are straight-line meters from a block representative point; they are proximity indicators only, not measures of capacity, eligibility, walkability, or service use.

| persistence_rank | block_id | neighborhood | hotspot_dates | hotspot_rate | nearest_service_m | nearest_transit_m |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 16TH_ST_IMPERIAL_AV | South East Village | 9 | 0.75 | 285.2 | 52.28 |
| 2 | I-5_SB_IMPERIAL_AV | South East Village | 8 | 0.67 | 392.52 | 136.91 |
| 3 | I-5_SB_OFF_RA_Map_Border | South East Village | 6 | 0.5 | 537.95 | 204.44 |
| 4 | I-5_SB_ON_RA_Map_Border | South East Village | 4 | 0.33 | 487.05 | 154.18 |
| 5 | 17TH_ST_IMPERIAL_AV | South East Village | 4 | 0.33 | 324.64 | 71.57 |
| 6 | 16TH_ST_J_ST | South East Village | 2 | 0.17 | 422.66 | 282.91 |
| 7 | 17TH_ST_J_ST | South East Village | 2 | 0.17 | 506.31 | 273.92 |
| 8 | 16TH_ST_ISLAND_AV | South East Village | 2 | 0.17 | 374.95 | 167.93 |
| 9 | 17TH_ST_ISLAND_AV | South East Village | 1 | 0.08 | 456.01 | 174.42 |
| 10 | 16TH_ST_K_ST | South East Village | 0 | 0.0 | 389.01 | 164.11 |

The persistence ranking makes an important distinction between a recurring concentration and a single high count. The leading block, `16TH_ST_IMPERIAL_AV`, is significant on 9 of 12 dates; the next two blocks are significant on 8 and 6 dates. The ranking then falls to four dates or fewer. This pattern indicates that the highest-priority cluster is spatially compact rather than spread evenly throughout the study area. All top-ten entries in this analysis carry the South East Village source-neighborhood label, which identifies the local area for field review but should not be generalized to a causal neighborhood effect.

OpenStreetMap context is included to support operational discussion. The service category includes mapped social-facility and shelter features; the transit category includes mapped bus stops, transit platforms/stations, and rail stops. These data are a current public map inventory rather than an authoritative operational directory. A short distance does not show that a program serves unsheltered residents, that a stop is accessible, or that an intervention can be located there. Conversely, a longer distance does not prove a service gap. The values are best used as a reproducible screening indicator that can be checked against agency inventories before any decision.

## Migration pattern

The adjusted-count-weighted centroid of hotspot block-date records moved 121 meters toward the S from the 2018–2020 period to the 2022–2025 period. The supplementary unweighted centroid is included in `Hotspot_Migration_Centroids.csv`; it is a sensitivity check against a small number of high-count blocks dominating the weighted center.

The directional result is intentionally modest: it describes the shift in the center of significant local clusters, not movement of people or a one-to-one relocation of a hotspot. The weighted center gives more influence to block-date records with higher adjusted counts, while the unweighted center gives each significant block-date record equal influence. Reporting both keeps the conclusion transparent if a small number of high-count blocks have disproportionate leverage. Because only 12 digitized dates are available and March 2022 has a documented source anomaly, the migration result should guide follow-up rather than be read as a precise trend estimate.

## Service-siting implications and limits

Persistent hotspots should be prioritized for field validation and coordinated outreach, with the top-ten contextual indicators used to identify where service access may merit attention. They do not independently establish unmet need, causality, or an optimal service location. Recommendations must remain conditional on current service inventories, operational constraints, community input, and the documented March 2022 source anomaly. The map series, interactive explorer, ranking, and raw OSM context provide reproducible evidence for that next-stage review.

An appropriate next step is a site-review shortlist beginning with the first three persistently significant blocks and then evaluating the nearby blocks as a cluster rather than as isolated polygons. Service providers can compare the OSM screening distances with outreach routes, shelter intake capacity, hygiene services, transit operations, and safety constraints. Any siting recommendation should also be reviewed with people with lived experience and neighborhood stakeholders. The quantitative evidence supports prioritization, not displacement-oriented action or a claim that a single service would resolve the observed pattern.

## Reproducibility and limitations

The build script saves the four PNG maps, combined PDF, interactive HTML explorer, full 261-block persistence ranking, top-ten context table, migration-centroid table, and raw OSM context GeoJSON. The OSM query date and feature tags are retained with the context file. All calculations can therefore be repeated without altering raw count data. The analysis is constrained by the 12 digitized count dates, changing data collection methods documented in earlier assignments, the 2022 study-footprint expansion handled through balancing, and the March 2022 anomaly. Gi* p-values are date-specific permutation results and are not evidence of a causal service effect. These limits should remain visible whenever the outputs are used outside the technical workflow.
