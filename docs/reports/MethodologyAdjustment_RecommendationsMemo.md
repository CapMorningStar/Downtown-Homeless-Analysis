# Recommendations Memo: Selecting an Adjustment Approach for Forecasting Models

**Project:** Downtown Homeless Count — Methodology Impact Assessment (Assignment 6, Task 6.3)
**Date:** 2026-09-14
**Prepared for:** Analysts and forecasters consuming the adjusted DSDP/RTFH count series

---

## 1. Purpose

Two DSDP multiplier changes (April 2017: tent 2.00→1.75, vehicle 2.00→1.66; May 2018: vehicle 1.66→2.03) and one estimation-model divergence (January 2020) break the count series' internal consistency. Tasks 6.1–6.2 quantified each break's impact and built a data-derived adjustment factor. This memo compares three candidate adjustment approaches end-to-end and recommends one for use in forecasting.

## 2. Approaches tested

| Approach | Construction | Source |
|---|---|---|
| **Theoretical multipliers only** | Per-neighborhood composition-weighted multiplier ratios (tent/vehicle/individual shares × documented multiplier deltas), applied uniformly regardless of data availability | Task 6.1/6.2 composition windows |
| **Data-derived only** | Literal observed ratios between calendar-adjacent months at each break (e.g., Mar→Apr 2017) | Task 6.2 `AdjustmentFactors_RatioComparison.csv` |
| **Hybrid (selected in Task 6.2)** | Exact per-row multiplier reconstruction where real tent/vehicle/individual component data exists (Jan–Apr 2018); theoretical composition-weighted ratio as a proxy where it doesn't (pre-2018) | Task 6.2 `TimeSeries_ConstantMethodology.csv` |

All three rescale historical counts onto the POST2020 multiplier baseline (individual 1.00, tent 1.75, vehicle 2.03). Full build logic and hash-verified inputs: `build_adjustment_approach_comparison.py`. Comparison output: `data/AdjustmentApproach_Comparison.csv`; figures: `figures/adjustment_approach_comparison/`.

## 3. Findings

- **Data-derived-only is unusable as a standalone adjustment.** Task 6.1 already showed both breaks' observed level shifts are dominated by real change, not multiplier arithmetic — in April 2017 the pre-2018 data literally cannot carry multiplier signal (`total_count == raw_count` for every row before 2018-01-01). Applying it anyway inflates the pre-2020 pooled mean by **+6.1%** (Fig. 1, 3), and around the May 2018 break it swings up to +260 counts above raw in a single month, an artifact of real change, not methodology (Fig. 3, right panel).
- **Theoretical-only and hybrid track each other and raw counts closely** (+0.66% and +0.74% pooled pre-2020 mean gap respectively) — because the hybrid falls back to the same theoretical composition-weighted ratio everywhere except the 16 months (Jan 2018–Apr 2018) where exact component data exists. In those 16 months the two approaches diverge slightly, since hybrid uses the true per-row multiplier reconstruction instead of a fixed neighborhood ratio.
- **The theoretical correction itself is small in absolute terms** relative to raw count fluctuations — consistent with Task 6.1's conclusion that both structural breaks are driven mostly by real change on the ground, not by the multiplier revisions.

## 4. Recommendation: use the hybrid approach

Use the **hybrid series** (`data/TimeSeries_ConstantMethodology.csv`, column `constant_methodology_count`) as the input to forecasting models. It is strictly more accurate than theoretical-only wherever real component data exists (Jan–Apr 2018) and degrades gracefully to the same theoretical proxy elsewhere — it dominates the other two approaches rather than trading accuracy for coverage. Do **not** use the data-derived-only series in any capacity; it should be treated as diagnostic only (it is useful for illustrating the presence of real change, not for correcting methodology).

**One caveat on the hybrid series' scope:** as built, it corrects the April-2017-regime window (Apr 2017–Apr 2018) for the April break, but does **not** additionally compound the May-2018 vehicle-multiplier correction onto that same window before the May 2018 transition month. Forecasters running models that span across April 2017–April 2018 specifically should re-run that segment through the theoretical-only factor (`factor_theoretical` in the comparison script) to compound both corrections, or treat pre-May-2018 hybrid values as approximate.

## 5. Handling the January 2020 county estimation model change

January 2020 is **not a multiplier change** — it is a divergence in *who* applies the multiplier. RTFH stopped applying DSDP's occupancy multipliers when reporting to HUD's Point-in-Time count, while DSDP's Clean & Safe program continued applying them for operational continuity (`docs/MethodologyChangeLog.md`). Because this project's canonical series (`MasterCounts_Adjusted_v2.csv`) is sourced from the DSDP/Clean & Safe side, **`total_count` already carries POST2020 multipliers continuously from January 2020 forward** — no additional adjustment factor is needed after that date (all three approaches converge to `factor = 1.0` post-2020, as confirmed in Fig. 1).

The practical risk is **cross-source comparison**, not this project's series in isolation: any analyst who pulls a parallel RTFH/HUD PIT figure for 2020+ and compares it directly to this project's `total_count` will see an artificial gap that looks like a real-world decline but is actually the multiplier being dropped on the RTFH side. Forecasting models should:
1. Use only DSDP/Clean & Safe-sourced counts (this project's series) as the training target — never blend in raw RTFH/HUD PIT figures post-2020 without first re-applying the DSDP multipliers.
2. Flag any external benchmarking against HUD PIT totals as methodologically incomparable unless the PIT source's multiplier treatment is confirmed.

## 6. Caveats for users of adjusted data

- **Pre-2018 values are proxied, not measured.** No tent/vehicle/individual component breakdown exists before January 2018; all PRE2017/APR2017-regime adjustment factors before that date reuse the Jan–Apr 2018 composition as an imperfect stand-in. Treat pre-2018 adjusted values as illustrative, and widen uncertainty bands accordingly in any forecast that extends training data that far back.
- **The April 2017 theoretical estimate cannot be cross-checked against observed data** — the observed ratio at that break is definitionally uninformative (see §3). Confidence in the April 2017 factor rests entirely on the theoretical composition model.
- **Adjustment factors are small relative to real month-to-month variation.** Do not interpret the adjusted series as removing most of the volatility in the raw counts — real change (COVID-19 decline, 2022–2023 rebound, 2024 drop) dominates the signal; the methodology adjustment is a secondary correction layered on top.
- **`Outside Perimeter` and East Village sub-areas are unaffected.** `Outside Perimeter` reports only under POST2020 and always carries `factor = 1.0`; sub-area rows were excluded from this comparison to avoid double-counting against the neighborhood-level East Village total.
- **A small number of 2025 months have zero raw counts** (apparent reporting gaps, not real zeros) — all three approaches agree at those points since `factor = 1.0` post-2020, but forecasters should treat those specific months as missing data, not literal zero counts.

## 7. Deliverables

- `build_adjustment_approach_comparison.py` — comparison build script
- `data/AdjustmentApproach_Comparison.csv` — 324-row long-format monthly series (3 approaches × raw, pooled fixed-core-six)
- `data/AdjustmentApproach_SummaryStats.csv` — pre-2020 pooled mean/gap summary
- `figures/adjustment_approach_comparison/01_raw_vs_three_approaches.png` — full-history comparison
- `figures/adjustment_approach_comparison/02_methodology_gap_over_time.png` — gap (adjusted − raw) over time, all three approaches
- `figures/adjustment_approach_comparison/03_break_window_closeups.png` — zoomed comparison at each break
- `figures/adjustment_approach_comparison/04_annual_mean_with_spread.png` — annual mean, raw vs. hybrid, with approach-spread band
