# Structural Break Analysis (Task 4.3)

**Downtown San Diego Homeless Population Analysis**
**Author:** Kyaw Soe Lwin (`kylwin@ucsd.edu`)
**Project Lead:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)
**Scope:** `data/MasterCounts_Adjusted_v2.csv` — the nine Task 4.1/4.2 analysis series (overall reported footprint, the fixed-core-six sensitivity series, and the seven individual neighborhoods), 2017–2025

---

> **Correction (October 2026).** All tables were regenerated with `scripts/structural_breaks.py`, which reproduces the original results exactly on the original data, after the source corrections in `data/source_corrections.csv`. Classifications are unchanged. The only threshold change is that two COVID results (the reported-footprint total and Cortez) now fall exactly at the FDR cut-off (0.0499 vs 0.054 / 0.050 before).


## 1. Three Candidate Break Dates, Derived or Supplied Transparently

The task specifies testing the April 2017 and May 2018 DSDP methodology changes and the March 2020 COVID-19 onset. The two methodology dates are now derived programmatically from `MasterCounts_Adjusted_v2.csv`'s `method` column. COVID is an external event and is therefore supplied explicitly.

| Regime | First observed month |
|---|---|
| `PRE2017` | 2017-01-01 |
| `APR2017` | **2017-04-01** |
| `MAY2018` | **2018-05-01** |
| `POST2020` | 2020-01-01 |

**Date reconciliation:** the `MAY2018` source report is dated May 31, 2018, while the canonical monthly dataset normalizes that reporting month to **May 1, 2018**. Task 4.3 tests the canonical month label. Task 4.1's former June 1 annotation has also been corrected to May 1. COVID (March 2020) remains distinct from the `POST2020` accounting label that begins January 2020.

**Method:** a dummy-variable Chow test: `y = β0 + β1·τ + β2·D + β3·(D·τ) + ε`. The joint F-test of `β2 = β3 = 0` is the requested classical Chow test; `β2` is the discontinuity at the break and `β3` is the slope change. Their individual t-tests provide descriptive mechanism labels, not additional confirmatory tests. A significant joint test with neither coefficient individually significant is retained as **indeterminate** rather than forced into level/trend/both.

**Inference safeguards added after audit:** Benjamini–Hochberg FDR p-values are calculated across the eight series within each event/test family. HAC(12) joint and coefficient p-values are included for May 2018 and COVID as a serial-correlation sensitivity; they are withheld for April because three pre-period points cannot support credible robust inference. These safeguards are sensitivities, not replacements for the requested classical statistic.

`Outside Perimeter` begins reporting in January 2021 — after all three candidate dates — so it has zero pre-period observations at every one of them and is excluded from all Chow tests (its whole-series CUSUM check still runs; see §3).

---

## 2. Chow Test Results by Candidate Date

### 2.1 April 2017 — and the short-baseline limitation

The series begins January 2017, leaving only **3 pre-break monthly observations**. The reduced level-shift intervention model below is shown only as an **exploratory result**; it is not a full Chow test or confirmatory evidence. The full model is retained in the CSV for transparency but its pre-period slope has only one residual degree of freedom and is not reliable.

| Series | F | p | Level shift | Level p | Classification |
|---|---:|---:|---:|---:|---|
| Columbia | 12.169 | <0.001 | +25.71 | <0.001 | **Significant** — level shift |
| East Village | 2.194 | 0.142 | −140.15 | 0.142 | Not significant |
| Gaslamp | 1.652 | 0.202 | +10.24 | 0.202 | Not significant |
| Overall — fixed core six | 0.774 | 0.381 | −118.14 | 0.381 | Not significant |
| City Center | 0.344 | 0.559 | −17.44 | 0.559 | Not significant |
| Overall — reported footprint | 0.341 | 0.561 | −120.46 | 0.561 | Not significant |
| Cortez | 0.037 | 0.848 | +3.25 | 0.848 | Not significant |
| Marina | 0.001 | 0.971 | +0.25 | 0.971 | Not significant |

**Reading:** Columbia is the only exploratory detection (p=0.001; within-event FDR p=0.006). It must not be treated as confirmed. For every series, the valid conclusion is that April break detection is fundamentally underpowered; both false negatives and fragile positive results are plausible.

### 2.2 May 2018

| Series | F | p | Level shift | Level p | Trend shift | Trend p | Classification |
|---|---:|---:|---:|---:|---:|---:|---|
| East Village | 5.718 | 0.004 | −55.68 | 0.510 | +12.15 | 0.137 | Significant (joint), neither term individually significant |
| Overall — fixed core six | 4.304 | 0.016 | −125.57 | 0.298 | +9.76 | 0.402 | Significant (joint), neither term individually significant |
| Cortez | 4.284 | 0.016 | −35.82 | 0.019 | −1.22 | 0.405 | **Level shift only** |
| Columbia | 3.803 | 0.025 | −6.40 | 0.360 | −1.55 | 0.023 | **Trend change only** |
| Gaslamp | 3.714 | 0.028 | −18.77 | 0.010 | −1.77 | 0.012 | **Level shift and trend change** |
| Overall — reported footprint | 1.461 | 0.237 | −84.81 | 0.655 | +11.85 | 0.517 | Not significant |
| Marina | 1.215 | 0.301 | −2.93 | 0.643 | +0.33 | 0.592 | Not significant |
| City Center | 1.030 | 0.361 | −5.98 | 0.827 | +1.82 | 0.491 | Not significant |

**Reading:** 5 of 8 eligible series (East Village, Cortez, the fixed-core-six aggregate, Columbia, Gaslamp) show a statistically significant break at May 2018; neither overall "public-facing" aggregate — reported footprint or fixed-core-six — shows a clean single-mechanism break (fixed-core-six is significant only jointly, with neither coefficient individually distinguishable; reported-footprint is not significant at all).

**Cross-check — is the May 2018 break mechanical or behavioral?** `docs/MethodologyChangeLog.md` explicitly recommends `raw_count`, not `total_count`, for structural-break testing, since the May 2018 multiplier change ($1.66\times \to 2.03\times$ per vehicle) mechanically shifts `total_count` regardless of any real change in unsheltered population. Re-running the same test on `raw_count`:

| Series | Date | F | p | Classification |
|---|---|---:|---:|---|
| East Village | 2018-05-01 | 5.736 | 0.004 | Significant (joint), neither term individually significant |
| Cortez | 2018-05-01 | 4.325 | 0.016 | **Level shift only** |
| Overall — fixed core six | 2018-05-01 | 4.284 | 0.016 | Significant (joint), neither term individually significant |
| Columbia | 2018-05-01 | 3.908 | 0.023 | **Trend change only** |
| Gaslamp | 2018-05-01 | 3.478 | 0.035 | **Level shift and trend change** |
| Overall — reported footprint | 2018-05-01 | 1.458 | 0.237 | Not significant |
| Marina | 2018-05-01 | 1.122 | 0.330 | Not significant |
| City Center | 2018-05-01 | 1.025 | 0.363 | Not significant |

**Interpretation:** the exact same five series are significant on `raw_count` and `total_count`, with matching descriptive classifications. This shows that multiplier arithmetic alone is not sufficient to explain the pattern. It does **not** establish a behavioral cause: counting practice, reporting, coverage, model misspecification, or another coincident event could affect both targets. The April raw comparison is not independently interpretable because PRE2017 has no component breakdown and preserves aggregate `raw_count == total_count`.

### 2.3 COVID-19 (March 2020): level shift, trend change, both, or indeterminate?

| Series | F | p | Level shift | Level p | Trend shift | Trend p | Classification |
|---|---:|---:|---:|---:|---:|---:|---|
| Columbia | 10.706 | <0.001 | +10.09 | 0.036 | −0.49 | 0.010 | **Level shift and trend change** |
| East Village | 6.160 | 0.003 | +113.40 | 0.064 | +8.29 | <0.001 | **Trend change only** |
| Gaslamp | 5.068 | 0.008 | −15.12 | 0.004 | −0.07 | 0.741 | **Level shift only** |
| Overall — fixed core six | 4.548 | 0.013 | +137.22 | 0.116 | +10.20 | 0.003 | **Trend change only** |
| Marina | 4.193 | 0.018 | −4.93 | 0.267 | +0.32 | 0.070 | Significant (joint), neither term individually significant |
| Cortez | 3.325 | 0.040 | +2.48 | 0.822 | +1.02 | 0.020 | **Trend change only** |
| Overall — reported footprint | 3.228 | 0.044 | +317.94 | 0.020 | +10.13 | 0.057 | **Level shift only** |
| City Center | 1.591 | 0.209 | +31.31 | 0.113 | +1.12 | 0.148 | Not significant |

**Reading:** classically, 7 of 8 eligible series have p<0.05 (all except City Center). After within-event FDR correction all seven remain significant, but the reported-footprint total and Cortez sit exactly at the threshold (FDR p = 0.0499). HAC(12) sensitivity flags seven series (City Center in, Marina out), so membership near the threshold is model-sensitive. Mechanisms: level-only (Gaslamp, reported footprint), trend-only (East Village, fixed-core-six, Cortez), both (Columbia), and **indeterminate** (Marina). The defensible conclusion is that COVID coincides with heterogeneous level and trend disruption, not that every individual classification is definitive.

---

## 3. OLS-Residual CUSUM Cross-Check

A full-series **OLS-residual CUSUM** test (`statsmodels.stats.diagnostic.breaks_cusumolsresid`) was run once per series against a pooled trend line. This routine uses the maximum absolute scaled cumulative OLS residual; it is not a CUSUM-of-squares test.

| Series | sup(B) | p | Significant |
|---|---:|---:|---|
| Overall — fixed core six | 1.914 | 0.001 | **Yes** |
| East Village | 1.787 | 0.003 | **Yes** |
| Overall — reported footprint | 1.761 | 0.004 | **Yes** |
| City Center | 1.735 | 0.005 | **Yes** |
| Cortez | 1.665 | 0.008 | **Yes** |
| Columbia | 1.541 | 0.017 | **Yes** |
| Outside Perimeter | 1.520 | 0.020 | **Yes** |
| Gaslamp | 0.907 | 0.383 | No |
| Marina | 0.880 | 0.421 | No |

**Reading:** 7 of 9 series remain significant after FDR correction; Gaslamp and Marina do not. This is reported as an unresolved test-family discrepancy. CUSUM is an omnibus stability check while Chow targets specified dates. Cancellation or short-lived deviations are possible explanations, but no breakpoint-location analysis establishes either explanation here.

`Outside Perimeter`'s significant CUSUM result is notable on its own: even restricted to its short 2021–2025 window (no candidate date falls inside it), the series is not parameter-stable — a flag worth carrying into Assignment 6 (Methodology Impact Assessment) if `Outside Perimeter` is modeled on its own.

---

## 4. Deliverable

* **`data/StructuralBreaks.csv`** — 57 rows: 40 `chow_full`, 8 exploratory `chow_level_only`, and 9 `cusum`. The original 19 fields are retained, with `p_value_fdr`, `significant_fdr`, `hac_joint_p`, `hac_level_p`, and `hac_trend_p` added for audit-ready inference.
* **`StructuralBreak_Analysis.ipynb`** — full reproducible notebook (candidate-date resolution, series reconstruction, test implementations, all results tables, per-series break-annotated plots, the COVID classification narrative, and the April 2017 limitation walkthrough). Executed end-to-end with 0 errors.
* **Build script:** `build_structural_break_analysis.py`.
* **Verified unchanged:** `data/MasterCounts_Adjusted_v2.csv` (the 4 interpolated 2025 months used for series continuity, identical to Tasks 4.1/4.2, exist only in memory — confirmed via `git status`, no source data modified).

---

## 5. Warning for Assignments 6 and 7 (Methodology Impact Assessment, Forecasting)

> ⚠️ A pooled model spanning May 2018 or March 2020 should test intervention terms and model serial dependence. Five May results survive within-event FDR, but fixed-core-six does not survive the HAC(12) sensitivity. Five COVID results survive FDR, while HAC changes which borderline series are detected. The raw-count agreement rules out multiplier arithmetic as the sole explanation; it does not prove behavior caused the breaks.
>
> `Outside Perimeter` cannot be evaluated at any of the three candidate dates (0 pre-period observations before 2021) but is not parameter-stable even within its own post-2021 window (CUSUM p=0.020) — treat any pooled model of that series with the same caution.

This warning is also logged in `PROJECT_CONTEXT.md` §4 (Task 4.3) for downstream sessions.

---

## 6. Summary

* Methodology dates are now derived from the canonical regime labels; COVID is explicitly supplied. May 1 is the normalized label for the May 31 source report.
* **April 2017:** Columbia is an exploratory detection only; the three-month baseline precludes confirmatory inference.
* **May 2018:** five classical and FDR-adjusted detections; four also pass HAC(12). Raw agreement excludes multiplier arithmetic as the sole cause, not all confounding.
* **COVID-19:** seven classical detections, seven after FDR (two exactly at the threshold); HAC gives a different seven-series set. Marina is mechanistically indeterminate.
* **OLS-residual CUSUM:** seven of nine remain significant after FDR; Gaslamp and Marina disagree with targeted results and remain unresolved.
* **Delivered:** `data/StructuralBreaks.csv` (57 rows), `StructuralBreak_Analysis.ipynb`, `build_structural_break_analysis.py`, with `data/MasterCounts_Adjusted_v2.csv` verified unchanged.
* **Flagged:** downstream pooled models spanning May 2018 or COVID onset should test intervention terms, model serial dependence, and report multiplicity-aware sensitivity.
