# Constant-Methodology Time Series — Data-Derived Adjustment Factors (Task 6.2)

**Downtown San Diego Homeless Population Analysis**
**Author:** Kyaw Soe Lwin (`kylwin@ucsd.edu`)
**Project Lead:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)
**Scope:** `data/MasterCounts_Adjusted_v2.csv` and Task 6.1's `data/MethodologyImpact_Composition.csv` — the six component-reporting neighborhoods plus `Outside Perimeter` and two aggregates, rescaled onto one consistent multiplier baseline across the April 2017 and May 2018 DSDP methodology changes.

---

## 1. The Two Multiplier Changes (Recap)

| Regime | Individual × | Tent × | Vehicle × |
|---|---:|---:|---:|
| `PRE2017` | 1.00 | 2.00 | 2.00 |
| `APR2017` | 1.00 | 1.75 | 1.66 |
| `MAY2018` | 1.00 | 1.75 | 2.03 |
| `POST2020` | 1.00 | 1.75 | 2.03 |

Full derivation and verification: see Task 6.1's [`MethodologyImpact_Analysis.md`](file:///D:/Projects/Downtown-Homeless-Analysis/MethodologyImpact_Analysis.md) §1. `MAY2018` and `POST2020` share identical multipliers.

---

## 2. ⚠️ April 2017 Data Artifact — Read Before the Numbers Below

**`total_count == raw_count` exactly for every neighborhood-month in this dataset before 2018-01-01** — verified directly against the full dataset (all rows, not just a sample). The delivered `total_count` series does not actually begin reflecting the April 2017 multipliers (tent 2.00→1.75, vehicle 2.00→1.66) until January 2018, nine months after the regime officially starts.

**Consequence:** the literal calendar-adjacent-month observed ratio for the April 2017 break (March 2017 → April 2017, both `total_count`) carries **zero multiplier signal**. It is not evidence that the methodology change had a small effect — it reflects a data-delivery artifact, not the methodology. This is documented explicitly rather than smoothed over, and is one of the two reasons (§4) the observed ratio was rejected as the basis for the applied adjustment factor.

---

## 3. Observed vs. Theoretical Ratio Comparison

**Observed ratio** = `total_count(post_month) / total_count(pre_month)`, using the literal adjacent calendar months (March→April 2017; April→May 2018).

**Theoretical ratio** = a composition-weighted multiplier ratio at fixed composition — `composite(new_regime, shares) / composite(old_regime, shares)`, isolating the pure mechanical effect. April 2017 uses Task 6.1's Jan–Apr 2018 composition proxy (the earliest available, 9–21 months post-break); May 2018 uses a real, single-month April 2018 composition (no proxy needed).

### April 2017 (tent 2.00→1.75, vehicle 2.00→1.66)

| Neighborhood | Observed ratio | Theoretical ratio | Gap |
|---|---:|---:|---:|
| East Village | 0.764 | 0.952 | −19.7% |
| City Center | 0.716 | 0.970 | −26.2% |
| Columbia | 2.300 | 0.959 | +139.8% |
| Marina | 0.732 | 0.974 | −24.8% |
| Cortez | 0.703 | 0.978 | −28.2% |
| Gaslamp | 1.075 | 1.000 | +7.5% |
| **All six (pooled)** | **0.792** | **0.961** | **−17.6%** |

The theoretical ratios cluster tightly near 1.0 (a modest few-percent mechanical decline, as expected since both multipliers dropped). The observed ratios are wildly inconsistent with this — ranging from a 30% real decline (Cortez) to a 130% real increase (Columbia) — confirming these single-month observed ratios are dominated by real month-to-month change and the data artifact in §2, not by the multiplier shift.

### May 2018 (vehicle 1.66→2.03)

| Neighborhood | Observed ratio | Theoretical ratio | Gap |
|---|---:|---:|---:|
| East Village | 1.043 | 1.010 | +3.2% |
| City Center | 1.614 | 1.000 | +61.4% |
| Columbia | 0.995 | 1.000 | −0.5% |
| Marina | 0.942 | 1.010 | −6.8% |
| Cortez | 1.166 | 1.008 | +15.7% |
| Gaslamp | 1.324 | 1.000 | +32.4% |
| **All six (pooled)** | **1.141** | **1.007** | **+13.2%** |

Here the theoretical ratios sit essentially at 1.0 (the vehicle multiplier increase alone is a very small effect, since vehicle shares are small everywhere in this window) — but observed ratios again vary widely and mostly exceed the theoretical prediction substantially, consistent with Task 6.1's finding that May 2018's observed change is dominated by real change (in that task, real change ran in the *opposite* direction from the small positive mechanical effect at the pooled level; here, month-to-month volatility at the single-neighborhood level shows both directions).

Full table: [`data/AdjustmentFactors_RatioComparison.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/AdjustmentFactors_RatioComparison.csv) (14 rows).

---

## 4. Why the Theoretical Ratio Was Chosen

Two evidence-backed reasons, not a default assumption:

1. **April 2017:** the artifact in §2 proves the observed ratio at this break is mathematically incapable of carrying any multiplier signal — `total_count` simply doesn't move independently of `raw_count` until 2018. It cannot be used to build a multiplier-correction factor for this break, full stop.
2. **Both breaks:** Task 6.1 already established that observed count changes at both dates are dominated by real population/reporting change, not multiplier arithmetic (its forward note: *"any forecasting or pooled-trend model spanning these breaks should treat the mechanical multiplier contribution as small and separate from the much larger real change"*). §3's comparison table reconfirms this in ratio form — the theoretical ratios sit near 1.0 at both breaks while the observed ratios swing widely.

**Conclusion:** the constant-methodology series (§5) is built from the **theoretical multiplier-based ratio**, not the observed ratio. The observed ratio is retained in `data/AdjustmentFactors_RatioComparison.csv` for documentation and comparison only.

---

## 5. Constructing the Constant-Methodology Series

**Baseline: POST2020** (individual 1.00, tent 1.75, vehicle 2.03) — the contemporary multiplier structure, matching `docs/MethodologyChangeLog.md` §4.1's own recommendation to "scale forecasts by the contemporary multiplier structure" when presenting adjusted series.

Four cases, applied per row of `data/MasterCounts_Adjusted_v2.csv` (`component=="total"`, `area_type=="neighborhood"`):

- **Identity (`MAY2018`/`POST2020` regime rows, 796 rows):** factor = 1.0 exactly — these regimes already use the POST2020 multipliers. This includes **all** `Outside Perimeter` rows, since that neighborhood only ever reports under `POST2020` (2021 onward).
- **Exact (`APR2017`-regime rows dated 2018-01 through 2018-04, 32 rows across 6 neighborhoods + 2 aggregates):** the row's own real tent/vehicle/individual composition is used to compute both its actual regime total (verified to reconstruct `total_count` exactly) and its POST2020-equivalent total; the factor is the ratio of the two. This is mathematically exact, not an approximation.
- **Proxied — APR2017, pre-2018 (72 rows):** for the April–December 2017 months (no component data exists), a single per-neighborhood factor is computed from the Jan–Apr 2018 proxy composition (the same one used in §3) and applied uniformly across all of that neighborhood's 2017 APR2017-regime months.
- **Proxied — PRE2017 (24 rows):** same proxy composition, but computed against the `PRE2017` regime's multipliers (2.00/2.00) instead of `APR2017`'s, applied to January–March 2017.

Aggregates (`Overall - fixed core six`, `Overall - reported footprint`) are built by summing each constituent neighborhood's **already-adjusted** `constant_methodology_count` — never by averaging factors and reapplying to a pre-summed total, since constituents can fall in different `factor_basis` cases within the same month.

**Output:** [`data/TimeSeries_ConstantMethodology.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/TimeSeries_ConstantMethodology.csv) — 924 rows, 9 series (6 neighborhoods + Outside Perimeter + 2 aggregates), columns `date, series, method, raw_count, total_count, adjustment_factor, constant_methodology_count, factor_basis, composition_source, baseline_regime`.

---

## 6. Limitations

1. **April 2017 proxy (reused from Task 6.1):** the Jan–Apr 2018 composition is 9–21 months after the true break; every `proxied_PRE2017`/`proxied_APR2017_pre2018` factor rests on this same imperfect assumption — treat 2017 constant-methodology values as best-available estimates, not exact.
2. **May 2018's composition (April 2018)** is real, not proxied, but still assumes composition is unchanged across the one-month gap — a much weaker assumption than the April proxy, but still an assumption for any row beyond that single verified month.
3. **Proxy uniformity:** every pre-2018 month in a neighborhood's PRE2017 or APR2017 regime receives the *same* proxy factor regardless of distance from the Jan–Apr 2018 source window — real composition drift within 2017, if any, is not captured.
4. **Exact-vs-proxied split:** only 32 rows (2018-01 to 2018-04, 6 neighborhoods + 2 aggregates) are mathematically exact; every other pre-baseline-regime row is proxied.
5. **`Outside Perimeter`** never needs adjustment — it only ever reports under POST2020.
6. Source data (`data/MasterCounts_Adjusted_v2.csv`, `data/MethodologyImpact_Composition.csv`) was verified unchanged (hash-checked) before and after this analysis ran.

---

## 7. Deliverables

- [`data/AdjustmentFactors_RatioComparison.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/AdjustmentFactors_RatioComparison.csv) — 14-row observed-vs-theoretical ratio comparison.
- [`data/TimeSeries_ConstantMethodology.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/TimeSeries_ConstantMethodology.csv) — 924-row long-format constant-methodology series, 9 series.
- [`TimeSeries_ConstantMethodology.ipynb`](file:///D:/Projects/Downtown-Homeless-Analysis/TimeSeries_ConstantMethodology.ipynb) — full reproducible notebook, executed end-to-end with 0 errors.
- `build_adjustment_factors.py` — notebook build script.
- This report, uploaded as a Google Doc to the `Assignment 6 - Methodology Impact Assessment` Drive folder; the CSV uploaded as a native Google Sheet in the same folder.
