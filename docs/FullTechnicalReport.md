# Downtown San Diego Homeless Population Analysis
## Full Technical Report (Assignments 1–8 synthesis)

**Organization:** Data Science Alliance (DSA)
**Data sources:** Downtown San Diego Partnership (DSDP) Clean & Safe monthly unsheltered counts; Regional Task Force on Homelessness (RTFH) annual Point-in-Time (PIT) counts
**Lead analyst:** Kyaw Soe Lwin (`kylwin@ucsd.edu`)
**Project lead & reviewer:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)
**Deliverable:** Assignment 9, Task 9.2 (`FullTechnicalReport`)
**Version:** 3.0 (October 2026) — fully revised; see §11 for what changed and why
**Repository:** [CapMorningStar/Downtown-Homeless-Analysis](https://github.com/CapMorningStar/Downtown-Homeless-Analysis)

---

## Abstract

This report synthesizes Assignments 1–8 of a study of unsheltered homelessness in Downtown San Diego from January 2017 to December 2025 (108 months, 104 with published counts), together with eight years of paired countywide PIT counts (2017–2020 and 2022–2025; the 2021 unsheltered count was waived).

Main findings, each traceable to a file in `data/`:

1. **Seasonality is weak.** After STL de-trending, Kruskal-Wallis tests find no significant calendar-month effect in 8 of 9 series. The overall series gives H = 2.66 (p = 0.995); only Marina is significant (H = 19.88, p = 0.047), and its ANOVA companion test is not (p = 0.162).
2. **Multi-year swings dominate.** The citywide monthly total averaged 1,057.8 in 2017 and fell to 654.1 in 2020 (−38.2%). It peaked at 2,103.3 in May 2023, then dropped 43.3% between the 2023 and 2024 annual averages.
3. **The 2022 boundary expansion inflates post-2021 totals.** The 121 blocks added in 2022 (Golden Hill, Barrio Logan, Sherman Heights) account for 3.7% to 32.8% of the digitized totals on the five post-2021 count dates.
4. **Hotspots are compact and persistent.** On a fixed 261-block panel, global Moran's I is positive on all 12 digitized dates (0.063–0.239, permutation p ≤ 0.034). The most persistent Getis-Ord Gi* hotspot (16th St & Imperial Ave) is significant on 9 of 12 dates. The count-weighted hotspot centroid moved about 120 m (bearing 160°, south-south-east) between 2018–2020 and 2022–2025.
5. **Forecast accuracy is modest.** At the 12-month horizon, XGBoost and Holt-Winters are essentially tied in 5-fold walk-forward cross-validation (mean MAPE 38.25% vs 38.44%, fold standard deviation ≈ 26–28 points). The 2026 status-quo forecast for the overall series is 816–896 per month.
6. **County estimates are directional only.** The best county model in leave-one-year-out cross-validation (OLS with a post-2023 policy-regime indicator) has LOOCV RMSE 815 and MAPE 14.9%, but in-sample R² is only **0.504** (adjusted R² 0.306). Neither the downtown slope (p = 0.78) nor the regime term (p = 0.075) is significant at the 5% level with N = 8. Current county estimates should be reported as about **5,900 [3,900–8,000]**.

---

## 1. Scope

### 1.1 Context
The RTFH PIT count is an annual, countywide, single-night census conducted in late January. The DSDP Clean & Safe count is a monthly overnight count covering only downtown. This project builds an audited monthly series from the DSDP reports, analyses its temporal and spatial structure, forecasts it, and tests how far it can be used to estimate the countywide unsheltered population between PIT counts.

### 1.2 Study areas
* **Monthly series (neighborhood level):** East Village, City Center (labelled "Core" in 2017 – early 2019 reports), Columbia, Cortez, Gaslamp, Marina, and an "Outside Perimeter" total that DSDP reports from January 2021. East Village is also reported in four quadrants (North East, North West, South East, South West EV; quadrant boundaries are Market St and Park Blvd).
* **Block level:** 382 blocks in `data/Downtown_BlockGrid.geojson`. 261 blocks are counted on every digitized date; 121 blocks in Golden Hill (52), Barrio Logan (35) and Sherman Heights (34) appear only from 2022.

### 1.3 Temporal scope
The delivered data begin in **January 2017**, not 2012 as originally scoped. DSDP's own summary tables go back to 2012, but only totals (no neighborhood breakdown) are available before 2017, and they were not part of the delivered dataset.

---

## 2. Data, validation and corrections

### 2.1 Adjusted counts and multipliers
Each neighborhood's adjusted count is

$$Y = \text{individuals} + \mu_{\text{tent}} \cdot \text{tents} + \mu_{\text{veh}} \cdot \text{vehicles}$$

| Regime (`method`) | First month | Tent × | Vehicle × | Note |
|---|---|---:|---:|---|
| `PRE2017` | Jan 2017 | 2.00 | 2.00 | no component breakdown in the data; total = raw |
| `APR2017` | Apr 2017 | 1.75 | 1.66 | Clean & Safe adopted the RTFH method on 27 Apr 2017 |
| `MAY2018` | May 2018 | 1.75 | 2.03 | implemented 31 May 2018, the night of the May count |
| `POST2020` | Jan 2020 | 1.75 | 2.03 | RTFH stopped applying multipliers for HUD reporting; DSDP continued |

Component data exist only from January 2018. For every month before that, the adjusted total equals the published total.

### 2.2 Validation results
* **45-cell source sample (Task 1.1):** 40 of the 41 published cells matched the source PDF (97.6%). The one mismatch (April 2025, South East EV) was later traced to DSDP's own breakout table, which does not add up to its East Village total (see §2.3).
* **Full re-check (October 2026):** all 945 neighborhood monthly totals for 2017–2025 match the summary tables on page 1 of the DSDP reports.
* **Missing values:** 134 cells. 116 are in 2025 (July, August, October and November were not yet published), and 18 are in November 2018 (the component breakdown is absent from that report while totals were published). City Center (September 2021) and Marina (December 2021) also lack component rows entirely.

### 2.3 Source corrections applied (October 2026)
Details are in `docs/DataQualityReport.md` and `data/source_corrections.csv`.
* **2019 East Village quadrants:** all 48 cells were a copy of the 2020 values. They were replaced with the 2019 breakout from the January 2020 report. The neighborhood totals were never affected.
* **Component typos found against the scanned maps:**
  * Feb 2018 City Center: 100 → 10 tents and 0 → 1 vehicle. The adjusted total had been 312.00 instead of 156.16.
  * Jul 2018 East Village: 32 → 26 vehicles.
  * Jul 2022 Cortez: 20 → 26 tents.
  * Nov 2022 Marina: 49 → 29 individuals (inferred from the map total).
  * Mar 2024 City Center: 8 → 18 tents.
* **No source available:** for December 2019 (East Village, City Center, Gaslamp), December 2023 (East Village) and September 2025 (East Village), the adjusted total is set to the published total.
* **Remaining flags:** 22 area-months where the adjusted and published totals differ by more than 2 are listed in `data/MasterCounts_QA_Flags.csv`. Three of these are map-verified conflicts within DSDP's own reports.

### 2.4 Data products and how they are produced
Every number in this report can be regenerated from the repository. The table lists the main files in dependency order.

| File (in `data/`) | Contents | Produced by |
|---|---|---|
| `RawCounts_AllYears_clean.csv` | 2,814 rows: monthly published counts by area and component, standardized labels and ISO dates | Task 1.2 cleaning, then `scripts/apply_source_corrections.py` |
| `MasterCounts_Adjusted_v2.csv` | Same rows with `raw_count`, multiplier-adjusted `total_count` and the `method` regime | Task 1.3 rebuild, then `scripts/apply_source_corrections.py` |
| `source_corrections.csv`, `MasterCounts_QA_Flags.csv` | Cell-level correction log with PDF and page; area-months still flagged | `scripts/apply_source_corrections.py` |
| `Neighborhood_Crosswalk.csv` | Maps every source label to a canonical neighborhood and sub-area | Task 1.2 |
| `BlockLevel_Counts_clean.csv`, `BlockPanel_Balanced_261.csv` | 3,737 block-date rows (382 blocks); fixed 261-block panel (3,132 rows) | Tasks 1.2, 3.3 (`build_balanced_panel.py`) |
| `SeasonalIndices.csv`, `StructuralBreaks.csv` | Task 4.2 indices and tests; Task 4.3 Chow, FDR, HAC and CUSUM results | `scripts/seasonal_indices.py`, `scripts/structural_breaks.py` |
| `AdjustedTimeSeries_Forecasting.csv`, `StationarityTests.csv` | Task 4.4 stationarity tests, transformations and candidate ARIMA orders | `Stationarity_Autocorrelation.ipynb` |
| `SpatialAutocorrelation_Results.csv`, `Hotspot_Classifications.geojson` | Task 5.1 Moran's I per date; Task 5.2 Gi* z, p and class per block-date | `scripts/hotspot_analysis.py` |
| `TimeSeries_ConstantMethodology.csv`, `AdjustmentFactors_RatioComparison.csv` | Task 6.2 POST2020-baseline series; observed vs theoretical ratios | `scripts/constant_methodology.py` |
| `Forecast_CV_Metrics.csv`, `Forecast_ModelComparison.csv`, `Forecasts_12Month.csv` | Task 7.2–7.4 cross-validation, hold-out metrics and 2026 forecasts | `Forecasting_Models.ipynb`, `forecast_pipeline.py` |
| `Downtown_County_PairedCounts.csv`, `CountyEstimation_LOOCV_*.csv`, `CountyEstimate_Current.csv` | Task 8.1 paired years; Task 8.3 validation and current estimates | Task 8.1, `scripts/county_estimation_build.py` |

`data/_audit_deltas.csv` records, for each result affected by the October 2026 corrections, the value before and after. `pytest` covers the correction rules (row counts, multipliers, component sums and the verified cells), the dashboard calculator, and the Assignment 10 pipelines.

---

## 3. Descriptive analysis

**Table 3.1 — Monthly counts by series, 2017–2025 (published months only).**

| Series | Months | Mean | SD | Min | Median | Max |
|---|---:|---:|---:|---:|---:|---:|
| Citywide total | 104 | 1,022.9 | 346.9 | 529.1 (Mar 2020) | 894.6 | 2,103.3 (May 2023) |
| East Village | 104 | 552.0 | 157.3 | 260.6 | 502.9 | 921.0 |
| City Center | 104 | 170.7 | 52.9 | 91.0 | 156.1 | 342.3 |
| Cortez | 104 | 59.6 | 30.3 | 16.0 | 51.9 | 170.5 |
| Gaslamp | 104 | 48.2 | 14.0 | 18.5 | 45.9 | 93.0 |
| Columbia | 104 | 44.5 | 13.7 | 13.8 | 45.1 | 84.5 |
| Marina | 104 | 30.7 | 15.5 | 4.1 | 27.4 | 79.0 |
| Outside Perimeter | 56 | 217.6 | 177.9 | 0.0 | 185.5 | 640.0 |

East Village accounts for 54.0% of all counted people over the period.

**Annual citywide averages:** 2017 1,057.8; 2018 843.0; 2019 810.4; 2020 654.1; 2021 960.4; 2022 1,513.1; 2023 1,563.1; 2024 886.9; 2025 864.3.

**Year-over-year changes:** the citywide-total basis gives 2021 +46.8% and 2022 +57.6%. The unweighted mean of the neighborhood changes is +25.9% for 2021, so the two statistics should not be mixed.

**Growth by neighborhood** (mean year-over-year change, 2019 onward):
* Outside Perimeter +26.9% per year
* Cortez +12.1%
* City Center +5.2%
* East Village +1.8%
* Marina −13.1%

These are descriptive rates only. The Outside Perimeter rate rests on five years of data.

---

## 4. Time-series analysis

### 4.1 Decomposition (Task 4.1)
The analysis used additive classical decomposition and robust STL (period 12) on 9 series: the reported-footprint total, a fixed "core six" total, and the 7 neighborhoods. The four unreleased 2025 months are interpolated in memory only.

STL seasonal strength (scale 0–1) is low:
* overall series 0.07
* core six 0.32
* East Village 0.26
* City Center 0.01
* the other neighborhoods 0.10–0.21

### 4.2 Seasonal significance (Task 4.2)
Seasonal indices are monthly means of the de-trended series, with t-based 95% CIs and Cohen's d.

| Series | Kruskal-Wallis H | p | ANOVA p |
|---|---:|---:|---:|
| Overall — reported footprint | 2.66 | 0.995 | 0.998 |
| Overall — fixed core six | 9.00 | 0.622 | 0.670 |
| East Village | 14.16 | 0.224 | 0.219 |
| City Center | 4.86 | 0.938 | 0.913 |
| Columbia | 8.76 | 0.644 | 0.473 |
| Cortez | 12.73 | 0.312 | 0.047 |
| Gaslamp | 14.57 | 0.203 | 0.087 |
| Marina | 19.88 | 0.047 | 0.162 |
| Outside Perimeter | 11.45 | 0.406 | 0.440 |

Eight of nine series show no significant seasonality under the primary (Kruskal-Wallis) test. The tests disagree for Marina (KW significant, ANOVA not) and for Cortez (ANOVA significant, KW not). Individually significant months:
* Gaslamp September (higher)
* Marina August and November (higher)
* Outside Perimeter September (lower)

No multiple-comparison correction was applied to these per-month tests.

### 4.3 Structural breaks (Task 4.3)
The Chow test uses a dummy-variable regression, y = β₀ + β₁τ + β₂D + β₃D(τ − τ_break), testing β₂ = β₃ = 0 jointly. Benjamini-Hochberg FDR correction is applied within each event, and a HAC(12) check is run.

* **April 2017:** only 3 pre-break months, so only a reduced level-shift model is run, and results are exploratory. Columbia is the only detection (F = 12.17, p = 0.001).
* **May 2018:** 5 of 8 eligible series break significantly (East Village, Cortez, core six, Columbia, Gaslamp). The **overall reported-footprint series does not** (F = 1.46, p = 0.237). The same five series are significant when tested on `raw_count`, so the pattern is not just multiplier arithmetic.
* **COVID-19 onset (March 2020):** 7 of 8 series are significant (all except City Center). After FDR correction 7 remain, with the reported-footprint total (level shift +318, p = 0.020) and Cortez exactly at the threshold (FDR p = 0.0499). The mechanisms differ by series: level-only, trend-only, both, or indeterminate.
* **CUSUM (OLS residuals):** 7 of 9 series are unstable over the full period. Gaslamp and Marina are not.

No break was tested at July 2023. Any statement about an ordinance-related break in the monthly series is outside the scope of Task 4.3.

### 4.4 Stationarity (Task 4.4)
In levels (constant-only ADF and KPSS), 7 of 9 series give mixed evidence and 2 are jointly non-stationary; ADF statistics range from −4.89 to −1.76. After the selected transformation (first difference for 8 series, log1p level for Outside Perimeter), all 9 are stationary under both tests.

ACF/PACF-based candidate orders are in `data/AdjustedTimeSeries_Forecasting.csv`. After the October 2026 correction, East Village's candidate AR order is 2 and Marina's is 1.

---

## 5. Block-level data and the 2022 footprint change

### 5.1 Grid integrity (Task 3.2)
* All 382 polygons are valid, with no overlaps and no zero-area features.
* 380 of 382 stated centroids fall inside their own polygon. The two exceptions, `22ND_ST_BROADWAY` and `22ND_ST_SR-94_EB_ON_RA`, are concave freeway-interchange parcels.
* 326 blocks have street boundaries consistent with all four neighbors. The remaining 56 are genuine edges of the study area.

### 5.2 Footprint effect (Task 3.3)
The balanced 261-block panel is compared with the full 382-block panel, both using multiplier-weighted totals.

| Count date | Full 382 | Balanced 261 | Added blocks | Share of full total |
|---|---:|---:|---:|---:|
| 2022-01-27 | 1,408.5 | 1,149.1 | 259.5 | 18.4% |
| 2022-03-01 | 1,392.5 | 1,158.2 | 234.3 | 16.8% |
| 2023-01-31 | 1,955.1 | 1,314.5 | 640.6 | 32.8% |
| 2024-01-25 | 1,019.0 | 981.8 | 37.2 | 3.7% |
| 2025-01-31 | 847.3 | 762.9 | 84.4 | 10.0% |

On the fixed 261 blocks, the total still rose 71% between the 2021 and 2022 dates, so both the footprint growth and a real increase are present. Any comparison across the 2021/2022 boundary must use the balanced panel. The March 2022 date carries a documented source-date anomaly.

---

## 6. Hotspot analysis (Assignment 5)

**Settings:** balanced 261-block panel; outcome = individuals + 1.75·tents + 1.66 or 2.03·vehicles; queen contiguity, row-standardized; 9,999 permutations.

* **Global Moran's I (Task 5.1):** positive on all 12 dates, from 0.063 (Jan 2019) to 0.239 (Feb 2018), with permutation p ≤ 0.034 (`data/SpatialAutocorrelation_Results.csv`).
* **Local Gi\* (Task 5.2):** each block-date is classified as a 99% or 95% hotspot or coldspot when z ≥ 2.576 / 1.96 *and* the permutation p < 0.01 / 0.05. Of 3,132 block-dates, 16 are 99% hotspots and 22 are 95% hotspots (`data/Hotspot_Classifications.geojson`).
* **Persistence (Task 5.4):** number of dates classified as a hotspot:

| Rank | Block | Hotspot dates (of 12) |
|---:|---|---:|
| 1 | 16TH_ST_IMPERIAL_AV | 9 |
| 2 | I-5_SB_IMPERIAL_AV | 8 |
| 3 | I-5_SB_OFF_RA_Map_Border | 6 |
| 4 | I-5_SB_ON_RA_Map_Border | 4 |
| 5 | 17TH_ST_IMPERIAL_AV | 4 |
| 6–8 | 16TH_ST_J_ST, 17TH_ST_J_ST, 16TH_ST_ISLAND_AV | 2 each |

All of the top ten are in South East Village.

* **Migration:** the count-weighted centroid of hotspot block-dates (block representative points, UTM 11N) moved about 120 m on a bearing of 160° (south-south-east) from 2018–2020 to 2022–2025. The unweighted centroid moved about 62 m. This describes where significant clusters sit, not the movement of people. With 12 dates it is a pointer for follow-up, not a trend estimate.

---

## 7. Methodology impact (Assignment 6)

* **Theoretical vs observed (Tasks 6.1–6.2):** the composition-weighted theoretical ratio is the change in total implied by the multiplier change alone, holding composition fixed.

  | Break | Theoretical ratio (pooled six) | Observed adjacent-month ratio |
  |---|---:|---:|
  | April 2017 | 0.964 (−3.6%) | 0.792 |
  | May 2018 | 1.007 (+0.7%) | 1.141 |

  The observed month-to-month changes are much larger than the multiplier effect, and in April 2017 they go in the opposite direction from it. Because no component data exist before 2018, the April 2017 observed ratio carries no multiplier signal at all.
* **Constant-methodology series (Task 6.2):** `data/TimeSeries_ConstantMethodology.csv` rescales all history to the POST2020 multipliers (1.75 / 2.03):
  * exact factors for Jan–Apr 2018, which have component data
  * a Jan–Apr 2018 composition proxy for 2017
  * a factor of 1.0 from May 2018 onward
* **Approach comparison (Task 6.3):** pre-2020 pooled mean gap versus raw counts is +0.10% for the hybrid, about +0.1% for theoretical-only, and +5.1% for data-derived-only. The hybrid is recommended. The data-derived series should be used only for diagnostics.

---

## 8. Forecasting (Assignment 7)

### 8.1 Validation design
* **Hold-out test:** 2025, with only 8 of 12 months published.
* **Cross-validation:** 5-fold walk-forward, with training windows expanding through 2020–2024.
* **Models:** naive seasonal (t−12), SARIMA (grid around the ACF/PACF candidates), Holt-Winters, Prophet (changepoints at the method changes and COVID), and XGBoost (lags 1, 2, 3, 6, 12; rolling means; month terms; recursive forecasting).

**Table 8.1 — Cross-validation MAPE (%) for the overall reported-footprint series; mean (SD) across the 5 folds.**

| Model | 1-month | 3-month | 6-month | 12-month |
|---|---:|---:|---:|---:|
| SARIMA | 5.4 (4.1) | 14.3 (10.3) | 24.7 (20.9) | 39.6 (35.5) |
| Holt-Winters | 13.0 (9.2) | 17.6 (10.4) | 25.2 (18.2) | 38.4 (28.5) |
| XGBoost | 14.0 (8.9) | 19.9 (14.8) | 26.7 (18.5) | 38.3 (26.0) |
| Naive seasonal | 39.5 (31.9) | 40.1 (31.3) | 48.5 (35.4) | 51.7 (24.5) |
| Prophet | 42.9 (26.0) | 42.7 (26.0) | 51.3 (31.9) | 64.2 (35.4) |

* **Short horizons:** SARIMA is clearly best.
* **12 months:** XGBoost, Holt-Winters and SARIMA are statistically indistinguishable given fold-to-fold variation of 26–36 points. XGBoost was kept as champion for the overall series because it has the lowest 12-month mean.
* **Prophet:** worst at every horizon. Its fixed changepoints have none near the 2022–2023 peak, so it extends the rise.
* **2025 hold-out (12-month horizon, overall series):** XGBoost MAPE 8.5%, Holt-Winters 20.4%, SARIMA 22.8%. The naive seasonal forecast scored 6.3% because 2025 closely repeated 2024, so this single hold-out year should not be over-read.

Per-series champions from cross-validation:
* XGBoost: overall series, core six, East Village, City Center, Cortez, Outside Perimeter
* SARIMA: Columbia
* Prophet: Gaslamp, Marina

Outside Perimeter's cross-validation MAPE exceeds 500% for every model, so its forecasts should not be used.

### 8.2 2026 forecast for the overall series
This is the output of `forecast_pipeline.py` (`data/Forecasts_12Month.csv`).

The prediction intervals are approximate. They come from Holt-Winters residual variance, inflated by √(1 + 0.08(h−1)). The scenarios are fixed paths of −2% and +2.2% per month (−24% / +26% by month 12), not model-based scenarios.

| Month | Forecast | 80% PI | 95% PI | Optimistic | Pessimistic |
|---|---:|---|---|---:|---:|
| Jan 2026 | 863 | 697–1,029 | 609–1,117 | 846 | 882 |
| Feb 2026 | 885 | 712–1,058 | 621–1,149 | 850 | 924 |
| Mar 2026 | 816 | 637–995 | 542–1,090 | 767 | 870 |
| Apr 2026 | 858 | 673–1,043 | 575–1,141 | 789 | 933 |
| May 2026 | 876 | 684–1,067 | 583–1,168 | 788 | 972 |
| Jun 2026 | 850 | 653–1,047 | 549–1,151 | 748 | 962 |
| Jul 2026 | 861 | 658–1,063 | 551–1,170 | 740 | 993 |
| Aug 2026 | 854 | 646–1,062 | 536–1,171 | 717 | 1,004 |
| Sep 2026 | 844 | 631–1,057 | 518–1,169 | 692 | 1,011 |
| Oct 2026 | 884 | 666–1,102 | 551–1,218 | 707 | 1,079 |
| Nov 2026 | 896 | 673–1,119 | 555–1,237 | 699 | 1,113 |
| Dec 2026 | 888 | 660–1,116 | 539–1,237 | 675 | 1,123 |

XGBoost results are not bit-for-bit reproducible across library versions. Re-running on the original inputs in a different environment moved the overall forecast by up to about 58 per month.

---

## 9. County-level estimation (Assignment 8)

### 9.1 Paired data (Task 8.1)
X is the January downtown adjusted total. Y is the county unsheltered PIT count.

| PIT year | Downtown X | County Y | City of SD unsheltered | Downtown share of county |
|---|---:|---:|---:|---:|
| 2017 | 882.0 | 5,621 | 3,231 | 15.7% |
| 2018 | 803.5 | 4,990 | 3,066 | 16.1% |
| 2019 | 897.2 | 4,476 | 2,600 | 20.0% |
| 2020 | 789.1 | 3,971 | 2,283 | 19.9% |
| 2022 | 1,444.3 | 4,106 | 2,494 | 35.2% |
| 2023 | 1,938.7 | 5,171 | 3,285 | 37.5% |
| 2024 | 1,018.1 | 6,110 | 3,365 | 16.7% |
| 2025 | 851.0 | 5,714 | 2,897 | 14.9% |

The 2022 PIT count was held on 24 February (postponed for Omicron) and is paired with the February downtown count.

### 9.2 Relationship (Task 8.2)
* **Correlation:** Pearson r = −0.061 (p = 0.886); Spearman ρ = 0.214 (p = 0.610).
* **Ratio stability:** a one-way ANOVA of the downtown share across three periods (2017–2020, 2022–2023, 2024–2025) gives F = 66.51, p = 0.0002, η² = 0.964. The ratio is not stable.
* **Power:** with N = 8, the power to detect r = 0.5 is about 23%.

### 9.3 Models and validation (Task 8.3)
**Table 9.1 — Leave-one-year-out cross-validation (8 folds).**

| Model | RMSE | MAE | MAPE | Signed bias |
|---|---:|---:|---:|---:|
| OLS + policy-regime indicator | 815.3 | 721.2 | 14.9% | −0.3% |
| OLS | 960.5 | 879.7 | 18.2% | +1.4% |
| OLS + time trend | 1,050.4 | 943.2 | 19.3% | −1.3% |
| Pooled ratio | 2,392.6 | 1,917.4 | 38.2% | +5.0% |
| Mean of ratios | 2,482.5 | 1,777.4 | 35.9% | +14.0% |
| Post-ordinance ratio | 3,142.6 | 1,976.4 | 42.2% | +39.3% |

**Selected model:** Y = 4,513.26 + 0.1859·X + 1,225.04·D_post, where D_post = 1 for the PIT years 2024 and 2025.

* **Coefficients:**

  | Term | Estimate | p |
  |---|---:|---:|
  | Intercept | 4,513.26 | 0.002 |
  | Slope (X) | 0.186 | 0.78 |
  | D_post | 1,225.0 | 0.075 |

* **Fit:** R² = 0.504, adjusted R² = 0.306, residual SE 652 on 5 df.
* **Caveats:**
  * Only two observations have D_post = 1, so the regime term is close to an indicator for those two years.
  * The model **describes** the post-2023 divergence between downtown and county counts. It does not prove that the ordinance displaced people.
  * The 2024 and 2025 LOOCV errors (−6.05% and +6.47%) are each predicted from essentially one post-ordinance year.

**Current estimates (Student's t, df = 5):**

| Scenario | Downtown input X₀ | Estimate | 95% PI |
|---|---:|---:|---|
| Dec 2025 (latest month) | 985.4 | 5,921 | 3,867–7,976 |
| Jan 2025 (PIT-matched) | 851.0 | 5,896 | 3,839–7,954 |
| Jan 2026 forecast (from §8.2) | 862.9 | 5,899 | 3,843–7,955 |

Under the reporting rules (§10) all three round to **5,900 [3,900–8,000]**, a margin of about ±2,050 (±35%).

---

## 10. Use and governance (Task 8.4)

### 10.1 Public communication rules
* **Rule 1 — no single-point precision:** do not publish unrounded point estimates (for example "5,921").
* **Rule 2 — round to the nearest 100:** "5,900".
* **Rule 3 — always give the 95% prediction interval:** "5,900 [3,900 to 8,000]".
* **Rule 4 — disclose the policy regime:** state that the estimate is derived from downtown counts and assumes the post-July 2023 Unsafe Camping Ordinance enforcement environment continues.

### 10.2 Appropriate and inappropriate uses

| Appropriate | Not appropriate |
|---|---|
| Directional tracking between annual PIT counts | HUD Continuum of Care submissions |
| Scenario planning and capacity stress tests | Formula funding or sub-regional allocations |
| Prioritising outreach and field validation (hotspots) | Single-number media statements without the interval |

### 10.3 Annual update
1. Add the new PIT year to `data/Downtown_County_PairedCounts.csv`.
2. Run `python scripts/county_estimation_build.py` to re-run LOOCV, refit, and regenerate `CountyEstimate_Current.csv`.
3. Re-test regime stability.
4. Update the constants in `src/config.py`.
5. Run `pytest`.

For monthly data, run `python scripts/apply_source_corrections.py` after appending new DSDP months. Then re-run the Assignment 4–7 scripts and notebooks in order (see `docs/ProjectHandoff_OperationalRunbook.md`).

### 10.4 Limitations

**Source data**
* **A single count night a month.** Each value is one overnight observation. Weather, events, enforcement activity and staffing on that night move the number, and none of these is recorded consistently in the source reports.
* **Conflicts inside the DSDP reports.**
  * In three verified months, the map pages and DSDP's own summary table give different totals (April 2020 Gaslamp, February 2023 Gaslamp, February 2023 East Village).
  * For 2025 (February–June) and November 2021, DSDP's East Village quadrant table does not add up to its East Village total.
  * The project follows the published neighborhood totals and the map-based components. The 22 flagged area-months in `data/MasterCounts_QA_Flags.csv` should be treated with caution.
* **Unpublished months.** Four 2025 months were unpublished when the data were extracted. Every 2025 statistic uses 8 months, and the decomposition and forecasting notebooks interpolate the missing months in memory.
* **Methodology changes.**
  * Multipliers changed in April 2017 and May 2018.
  * Component data do not exist before 2018, so 2017 constant-methodology values rest on a 2018 composition proxy.
  * The April 2017 break has only three pre-break months and cannot be tested reliably.

**Block-level and spatial analysis**
* **Coverage.** Only 12 of about 90 months with usable maps were digitized. Block-level and hotspot conclusions therefore describe January/February snapshots, not the whole year.
* **Expanded footprint.** The 2022 expansion means any 2018–2021 vs 2022–2025 comparison must use the balanced 261-block panel.
* **March 2022.** The source maps for this date carry two different handwritten dates.

**Models**
* **Forecasts.**
  * Fold-to-fold variation in cross-validation error (26–36 MAPE points at 12 months) is as large as the differences between the leading models.
  * The 2026 prediction intervals are approximate: they come from Holt-Winters residual variance, not from each champion model's own error distribution.
  * The optimistic and pessimistic scenarios are fixed percentage paths, not model outputs.
* **County model.**
  * Eight paired years, with only two after the ordinance, cannot separate a genuine change in the downtown–county relationship from noise.
  * Neither predictor is significant at the 5% level.
  * The ±35% prediction interval is the honest summary of what the model can say.
* **No causal identification.** None of the analyses establishes why counts rose or fell. Statements about shelters, enforcement or the economy are context, not findings.

### 10.5 Recommendations

**For DSDP**
1. Publish the component breakdown (individuals, tents, vehicles) for every neighborhood every month, and keep quadrant tables consistent with neighborhood totals. Several data problems found in this project come from inconsistencies inside the published reports.
2. Record the count date and conditions (weather, events, enforcement operations) in a machine-readable form with each monthly report.

**For analysts using these data**
3. Use the balanced 261-block panel for any comparison across 2021/2022, and report the footprint share alongside any post-2021 total.
4. Treat 12-month forecasts as a planning range, not a target. Re-run the cross-validation each year and keep the naive seasonal baseline in the comparison, since it was the most accurate model on the 2025 hold-out.
5. Use county estimates only as rounded ranges under Rules 1–4. Re-estimate the model every year when RTFH publishes a new PIT count, and add a regime indicator only when there is a documented policy change.

**For service providers and agencies**
6. Use the persistent hotspot blocks (the 16th & 17th St / Imperial Ave and I-5 southbound ramp cluster in South East Village) as a shortlist for field validation and outreach coordination. They are not, on their own, evidence of unmet need or of where a service should be located.

**For the project**
7. Extend block digitization beyond the 12 January/February dates. This is the most valuable data investment: it would allow seasonal and post-ordinance spatial analysis at block level.

---

## 11. Revision note (October 2026)

Version 2.0 of this report contained statements and tables that were not supported by the project's own outputs. All quantitative content was rebuilt from the files in `data/`. The main corrections:

**County model (§9)**
* The model's R² was given as 0.9638 (adjusted 0.9493). That figure was the η² of the Task 8.2 ANOVA. The model's actual R² is 0.504 (adjusted 0.306).
* The regime term was reported as significant (p = 0.0028). Its actual p-value is 0.075.
* The paired-data table had wrong downtown and county values for most years. For example, 3,231 is the City of San Diego count for 2017, not the county count.
* A "Log-Log Elasticity" model that was never built has been removed.
* The model description had wrong values for X̄ and Σ(X−X̄)².

**Data and methods (§2, §5)**
* The multiplier table showed 1.50 / 2.00 factors. The documented factors are 2.00 / 1.75 / 1.66 / 2.03.
* The 2019 data issue was described as a double-count that inflated totals by 8–14%. It was in fact a copy of 2020 quadrant values, and the totals were unaffected.
* The February 2018 values "1,281 / 1,251" were wrong; they have been removed.
* Little Italy was listed as a study neighborhood. It is not in the data.
* The footprint table used count dates that were never digitized. It now uses the five real post-2021 dates.

**Time series (§3, §4)**
* The summary-statistics table had wrong values for most series, including quadrant series that were never analysed.
* The seasonality table had wrong H statistics and included series that were not tested.
* The structural-break section reported results that do not exist ("May 2018 F = 14.82", "July 2023 F = 28.64").

**Hotspots and forecasting (§6, §8)**
* The hotspot migration bearing and centroid coordinates were wrong (now about 120 m at 160°).
* The cross-validation and forecast tables did not match the outputs.
* A 90% hotspot class was described; the analysis uses only 95% and 99%.

**Causal language**
* Causal statements not tested in the project have been removed. These included hepatitis A sweeps, fentanyl, and claims that the ordinance "caused" displacement.

**Data corrections**
* Figures now reflect the October 2026 source corrections (§2.3).
