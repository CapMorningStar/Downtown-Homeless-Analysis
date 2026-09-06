# EDA Summary Report: Downtown San Diego Unsheltered Homeless Population (2017–2025)

*Prepared by Kyaw Soe Lwin, Data Science Alliance | Assignment 2, Task 2.3 | Source: Downtown San Diego Partnership (DSDP) Clean & Safe monthly counts, `MasterCounts_Adjusted_v2.csv`*

---

## 1. Overall Trends and Inflection Points

Across 2017–2025, the overall downtown unsheltered count (summed across 7 neighborhoods) averaged 156.78 per neighborhood-month (median 58.88, std 197.38), with the citywide monthly total ranging from a series low near 529 (March 2020) to a series peak of 2,103 (May 2023). The trajectory has three clear phases:

- **2017–2020 decline:** Annual average count fell from 176.31 (2017) to 109.02 (2020), a cumulative drop of roughly 38%, with year-over-year changes of −18.98% (2018), −4.94% (2019), and −19.71% (2020).
- **2021–2023 rebound and peak:** Counts rebounded sharply: +25.85% (2021) and +57.63% (2022), reaching an annual average of 223.98 in 2023 — the highest in the dataset, and more than double the 2020 trough.
- **2024–2025 pullback:** A steep −43.52% drop in 2024 brought the average back down to 126.50, with 2025 roughly flat (−2.94%) at 122.78.

The two sharpest inflection points are the COVID-era trough (2020, −19.71% YoY) and the 2022 rebound (+57.63% YoY) — the single largest year-over-year swing in the series.

## 2. Seasonal Patterns (Quantified)

Calendar-month seasonality is real but modest. Average counts by month deviate from the all-months grand mean (156.78) by no more than about 5%:

- **Highest months:** Feb (+3.2%), Aug (+3.1%), May (+2.6%)
- **Lowest months:** Mar (−5.2%), Sep (−2.0%), Nov (−2.1%)

The spread between the highest and lowest month is about 8.4 percentage points of the grand mean — small relative to the roughly 40–60% year-over-year swings observed in Section 1. Month-to-month standard deviations (187–216) are large relative to these mean differences, confirming that which *year* a month falls in matters far more than which *month* it is. One neighborhood-level exception: East Village itself peaks in Jul–Aug (~601–604) and dips in spring (Mar–Apr, ~509), a pattern distinct from the citywide average.

## 3. Neighborhood-Level Insights

Average monthly count by neighborhood (2017–2025), ranked:

1. East Village — 552.77 (also highest volatility, std 157.09)
2. Outside Perimeter — 217.57 (partial reporting coverage since ~2022, only 56 observations)
3. City Center — 171.81
4. Cortez — 59.52
5. Gaslamp — 48.43
6. Columbia — 44.49
7. Marina — 30.94 (smallest and least volatile, std 15.82)

Ranking by average **growth rate** (mean YoY %, 2019 onward) tells a different story: **Outside Perimeter (+26.90%/yr)**, **Cortez (+11.96%/yr)**, and **City Center (+3.94%/yr)** are growing fastest, while East Village — despite being largest by far — grows modestly (+1.64%/yr), and **Marina (−12.76%/yr)** and **Columbia (−4.28%/yr)** are shrinking. Growth is concentrated in mid-sized areas, not the largest one.

East Village's four sub-areas (available Jan 2018–Dec 2025) show North East EV and South East EV consistently running higher than the two West sub-areas, suggesting the eastern half of East Village concentrates more of the unsheltered population, though all four sub-areas broadly track the same citywide peaks and troughs.

## 4. COVID-19 Period Impacts

The pandemic period shows a clear, quantifiable dip: the citywide monthly total fell to its series low of 529 in March 2020, and the 2020 annual average (654.1) sat well below the 2019 pre-COVID average (814.72) — a roughly 20% reduction. Counts partially recovered through 2021 (annual average 960.37, +46.82% YoY on a citywide-total basis, above the 2019 baseline) before the larger 2022–2023 climb described in Section 1. Note this +46.82% is the total-count YoY change; it differs from the +25.85% figure in Section 1, which is the unweighted average of each neighborhood's own YoY growth rate — the two are different statistics and are not directly comparable. This pattern is consistent with pandemic-era shelter placements and reduced outreach/count visibility temporarily suppressing observed unsheltered presence, followed by a rebound once conditions normalized.

## 5. Methodology Change Effects

Four methodology regimes governed data collection and adjustment: PRE2017 (Jan–Mar 2017, no component breakout), APR2017 (Apr 2017–Apr 2018, vehicle multiplier 1.66×), MAY2018 (May 2018–Dec 2019, vehicle multiplier raised to 2.03×), and POST2020 (Jan 2020–present, same multipliers as MAY2018, continued by DSDP for longitudinal continuity after RTFH stopped applying them for HUD PIT purposes in Jan 2020).

The gap between raw and methodology-adjusted totals (`total_count - raw_count`) was largest and most volatile in 2018 — averaging +13.5/month and spiking to +156.61 in February 2018, right at the APR2017→MAY2018 transition — then shrank to near-zero (roughly ±1 to ±5) from 2019 onward. Notably, the Feb 2018 spike is partly attributable to a documented source-PDF addition error (+30 discrepancy) already logged in Task 1.1's audit, not purely the multiplier change. A single-month before/after comparison at the 2017 transition shows *zero* gap, because component-level breakouts were not available before January 2018 — raw and adjusted totals are identical for all of 2017. This means multiplier-driven adjustment effects are only meaningfully observable from 2018 onward, and even then the effect is modest at the aggregate level (rounding-scale, within the ±2 tolerance documented in Task 1.3) rather than a large systematic shift.

## 6. Data Limitations

- **Incomplete 2025 data:** 28 nulls remain in the neighborhood-level total_count series, all in Jul, Aug, Oct, and Nov 2025 across all 7 neighborhoods — these are unreleased counts (reporting lag), not missing/corrupted data. Any 2025 annual figures should be read as partial-year.
- **Outside Perimeter partial coverage:** Only 56 observations (reporting began around 2022), making its growth-rate figure (+26.90%/yr) the least statistically reliable of the neighborhood rankings.
- **Pre-2018 no component breakout:** Raw and adjusted totals are identical for all of 2017, limiting how far back methodology-effect analysis can go.
- **Known source-PDF errors:** Task 1.1's 45-cell audit found a 97.56% fidelity rate against source PDFs, with specific known errors (Feb 2018 +30 addition error, 2019 East Village sub-area duplication bug, April 2025 discrepancy) that could still introduce small anomalies into month-level analysis.
- **Scope correction:** Data begins January 2017, not 2012 as originally scoped in the project charter (see `docs/DataQualityReport.md`).

## 7. Hypotheses for Further Analysis

1. **H1 — Policy/enforcement driver of the 2022–2023 peak:** The +57.63% (2022) and continued rise to a 2023 peak of 2,103 coincides with a broad-based spike across nearly every neighborhood simultaneously (Cortez +129%, Outside Perimeter +87%, East Village +50% in 2022 alone) rather than one area. This suggests a citywide driver (e.g., pandemic-era shelter/eviction-moratorium expirations, encampment sweep policy changes, or regional housing cost shocks) rather than localized neighborhood dynamics — worth testing against RTFH policy timelines and 311 service call data in later assignments.
2. **H2 — East vs. West East Village asymmetry reflects built environment, not just population:** North/South East EV consistently outcount their West counterparts. This could be explored spatially (Assignment 5, Getis-Ord Gi*/Moran's I) against block-level infrastructure factors (shelter proximity, transit access, commercial vs. residential zoning) rather than assuming it is purely a population-density effect.
3. **H3 — The 2024 pullback (−43.52%) is a reporting/methodology artifact, not a true population drop:** A drop this steep in a single year, immediately following the highest point in the series, warrants a check against RTFH's independent PIT counts and any DSDP operational changes in 2024 (e.g., a change in count area, timing, or staffing) before being read as a genuine reduction in unsheltered population.
4. **H4 — Neighborhood growth is inversely related to neighborhood size:** The fastest-growing areas (Outside Perimeter, Cortez, City Center) are all mid-sized, while the largest (East Village) grows slowly and the smallest (Marina) shrinks. This could reflect a spillover/displacement dynamic worth testing with spatial adjacency analysis in Assignment 5.

---

## Appendix: Key Figures Referenced

Full charts and underlying computations are available in [`EDA_DowntownCounts.ipynb`](EDA_DowntownCounts.ipynb) (Tasks 2.1–2.2), also exported as `EDA_DowntownCounts.pdf`.
