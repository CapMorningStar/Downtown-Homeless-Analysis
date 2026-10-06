# Methodology Impact Analysis (Task 6.1)

**Downtown San Diego Homeless Population Analysis**
**Author:** Kyaw Soe Lwin (`kylwin@ucsd.edu`)
**Project Lead:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)
**Scope:** `data/MasterCounts_Adjusted_v2.csv` and `data/StructuralBreaks.csv` — the six neighborhoods that report tent/vehicle/individual composition (East Village, City Center, Columbia, Marina, Cortez, Gaslamp; `Outside Perimeter` excluded, no component data in any regime), the April 2017 and May 2018 DSDP multiplier changes

---

> **Correction (October 2026).** The February 2018 City Center components were corrected against the source map: 10 tents and 1 vehicle, not 100 tents and 0 vehicles. July 2018 East Village vehicles were also corrected, from 32 to 26. As a result:
> * City Center's Jan–Apr 2018 composition is now 95.1% individuals, 4.7% tents and 0.2% vehicles (was 86.5% / 13.5% / 0.0%).
> * Its April 2017 theoretical effect is now −1.6 (was −7.1).
> * Its observed May 2018 level shift is now −6.0 (was −37.6), because the old figure partly reflected the doubled February 2018 total.
>
> The tables below are from the corrected data (`data/source_corrections.csv`). The conclusion is unchanged: the observed shifts are much larger than, and often opposite in sign to, the multiplier effects.


## 1. The Two Multiplier Changes

DSDP's count methodology applies a per-component multiplier to raw tent, vehicle, and individual counts before summing to `total_count`. That table changed twice:

| Regime | First observed month | Individual × | Tent × | Vehicle × |
|---|---|---:|---:|---:|
| `PRE2017` | 2017-01-01 | — | 2.00 (documented; unobservable, no component rows exist) | 2.00 |
| `APR2017` | **2017-04-01** | 1.00 | 1.75 | 1.66 |
| `MAY2018` | **2018-05-01** | 1.00 | 1.75 | 2.03 |
| `POST2020` | 2020-01-01 | 1.00 | 1.75 | 2.03 |

Verified against the live data: `total_count / raw_count` reproduces this table exactly for every `(method, component)` cell in `MasterCounts_Adjusted_v2.csv`. Break dates are derived programmatically from the `method` column (`APR_BREAK == 2017-04-01`, `MAY_BREAK == 2018-05-01`), the same pattern used in Task 4.3.

**April 2017:** both the tent multiplier (2.00→1.75) and the vehicle multiplier (2.00→1.66) dropped — a mechanical downward pull on `total_count` at any neighborhood with tent/vehicle presence.
**May 2018:** only the vehicle multiplier changed (1.66→2.03) — a mechanical upward pull, proportional to each neighborhood's vehicle share.

---

## 2. ⚠️ April 2017 Data Limitation — Read Before the Numbers Below

**There is zero tent/vehicle/individual component breakdown anywhere in the delivered data before January 2018** — nine months after the true April 2017 break. Neither `MasterCounts_Adjusted_v2.csv` nor the underlying raw delivery ever separates components prior to 2018-01-01; only the aggregate `total_count` exists at and around the actual break date.

Per an explicit project decision, this analysis uses **January–April 2018** — the earliest available composition data, still nominally inside the `APR2017` regime — as an **imperfect proxy** for April-2017-regime tent/vehicle composition. This proxy is extrapolated **backward 9–21 months** and may reflect real 2017→2018 compositional drift rather than the true composition at the break. **The April 2017 theoretical estimate below should be read as an order-of-magnitude illustration, not a measurement.**

This is a strictly worse sparsity problem than Task 4.3 flagged for the same date: Task 4.3 had 3 pre-break *aggregate* monthly observations and labeled its April 2017 result "exploratory, not confirmatory"; this task has **zero** component observations at the break itself. The May 2018 estimate carries no such limitation — real composition data exists both immediately before and immediately after that break, using the same underlying Jan–Apr 2018 window as genuine (not proxied) pre-break evidence.

---

## 3. Composition Windows

Three 4-month raw-count composition windows, computed over the 6 component-reporting neighborhoods:

- **`APR2017_proxy_2018`** = Jan–Apr 2018 (proxy for the April 2017 break)
- **`MAY2018_pre`** = Jan–Apr 2018 (the same four months, used directly as real pre-break composition for May)
- **`MAY2018_post`** = May–Aug 2018 (real post-break composition)

Average tent/vehicle/individual share per neighborhood (Jan–Apr 2018, the shared pre-break window):

| Neighborhood | Tent share | Vehicle share | Individual share |
|---|---:|---:|---:|
| City Center | 4.7% | 0.2% | 95.1% |
| Columbia | 18.9% | 0.4% | 80.7% |
| Cortez | 5.3% | 3.0% | 91.7% |
| East Village | 18.5% | 3.8% | 77.6% |
| Gaslamp | 0.0% | 0.0% | 100.0% |
| Marina | 5.9% | 4.0% | 90.0% |

East Village and Columbia carry the largest tent shares; Marina and Cortez the largest vehicle shares; Gaslamp reports no tents or vehicles in this window (100% individual), so both multiplier changes are mechanically inert there.

Full monthly detail: [`data/MethodologyImpact_Composition.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/MethodologyImpact_Composition.csv) (72 rows: 4 months × 6 neighborhoods × 3 windows).

---

## 4. Theoretical vs. Observed Count Change

**Theoretical** change = `raw_individual·Δmult_individual + raw_tent·Δmult_tent + raw_vehicle·Δmult_vehicle`, evaluated per window month, averaged with a paired 95% t-interval across the 4 window months (n=4 — exploratory, matching the status Task 4.3 gave its own n=3 April model; not confirmatory).

**Observed** change is read directly from Task 4.3's `data/StructuralBreaks.csv` Chow `level_shift` coefficient — the `chow_level_only` reduced model at April 2017 (Task 4.3's own recommended model for that break's 3-month pre-period), and the `chow_full` model at May 2018 — not recomputed here, keeping the two sides methodologically independent.

### April 2017 (tent 2.00→1.75, vehicle 2.00→1.66)

| Neighborhood | Theoretical Δ (95% CI) | Observed Δ (Chow level shift) | Difference |
|---|---:|---:|---:|
| East Village | −26.2 (−33.2, −19.1) | −140.2 | −114.0 |
| Columbia | −2.2 (−4.4, −0.1) | +25.7 | +27.9 |
| City Center | −1.6 (−3.2, 0.0) | −17.4 | −15.9 |
| Cortez | −1.3 (−3.3, +0.6) | +3.2 | +4.6 |
| Marina | −0.9 (−1.5, −0.3) | +0.3 | +1.1 |
| Gaslamp | 0.0 (0.0, 0.0) | +10.2 | +10.2 |
| **All six (pooled)** | **−32.2 (−42.2, −22.1)** | **−118.1** | **−86.0** |

The theoretical estimate is negative everywhere (as expected — both multipliers dropped), but small relative to the observed level shifts, and the two disagree in *sign* for Columbia, Cortez, and Gaslamp. Given the proxy limitation in §2, this divergence is expected and not surprising: April 2017's observed level shift is dominated by real population/reporting change, not by the multiplier arithmetic, and the proxy composition cannot be trusted as representative of the true break-date mix.

### May 2018 (vehicle 1.66→2.03)

| Neighborhood | Theoretical Δ (95% CI) | Observed Δ (Chow level shift) | Difference |
|---|---:|---:|---:|
| East Village | +6.3 (+3.6, +9.0) | −55.7 | −62.0 |
| Cortez | +0.6 (−0.7, +2.0) | −35.8 | −36.5 |
| Marina | +0.5 (+0.2, +0.8) | −2.9 | −3.4 |
| City Center | +0.1 (−0.2, +0.4) | −6.0 | −6.1 |
| Columbia | +0.1 (−0.2, +0.4) | −6.4 | −6.5 |
| Gaslamp | 0.0 (0.0, 0.0) | −18.8 | −18.8 |
| **All six (pooled)** | **+7.6 (+3.4, +11.8)** | **−125.6** | **−133.2** |

Here the sign mismatch is total and worth reading as a genuine finding, not a limitation artifact: May 2018's vehicle-multiplier increase should have pushed `total_count` mechanically *upward* by a modest amount (a few points per neighborhood, ~7.6 pooled), but every neighborhood's *observed* level shift is substantially *negative*. **`pct_theoretical_of_observed` is left undefined (NaN) for every row here** rather than reported as "0% explained" — the two estimates disagree in direction, meaning the observed May 2018 decline is driven by something other than (and larger than, and opposite in sign to) the multiplier arithmetic alone.

Full table with SEs, FDR-adjusted p-values, and `pct_theoretical_of_observed`: [`data/MethodologyImpact_TheoreticalVsObserved.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/MethodologyImpact_TheoreticalVsObserved.csv) (14 rows: 2 breaks × 7 areas including the pooled row).

---

## 5. Which Neighborhoods Were Most Affected?

Ranking by `|theoretical_change_mean|` within each break, cross-checked with a Spearman correlation against composition share (tent+vehicle share for April, since both multipliers moved; vehicle share alone for May, since only that one did):

- **April 2017:** East Village (rank 1) > Columbia (2) > City Center (3) > Cortez (4) > Marina (5) > Gaslamp (6, zero impact). This tracks each neighborhood's combined tent+vehicle share reasonably well — East Village has the highest combined share (22.3%) and the largest theoretical impact; Gaslamp has zero tent/vehicle presence in this window and zero theoretical impact.
- **May 2018:** East Village (rank 1) > Cortez (2) > Marina (3) > City Center/Columbia (tied, about +0.1) > Gaslamp (last, zero vehicle share, zero impact). This tracks vehicle share specifically — Marina and Cortez have higher vehicle shares than tent shares, so their relative ranking shifts compared to April even though their tent shares alone would rank them lower.

In both cases, **composition mechanically explains which neighborhoods carry any theoretical multiplier effect at all** (zero tent/vehicle presence ⇒ zero theoretical impact, as at Gaslamp) — but composition does **not** explain the much larger *observed* level shifts, which are dominated by whatever real change (population, coverage, reporting practice) coincided with each break date. That distinction — mechanical multiplier effect vs. everything else — is the central finding of this task.

---

## 6. Limitations

1. **April 2017 proxy (see §2):** zero component data exists at or near the true break; the Jan–Apr 2018 proxy is 9–21 months later and may reflect drift, not the true April-2017 mix. Treat April's theoretical numbers as illustrative, not measured.
2. **n=4 window months** means every confidence interval and p-value here is exploratory, not confirmatory — the same status Task 4.3 assigned its own n=3 April 2017 model.
3. **Sign-mismatched `pct_theoretical_of_observed` values are left undefined (NaN) and reported as a finding** (the two estimates disagree in direction), never silently reported as "0% explained" or as a spurious large/negative percentage.
4. **The observed and theoretical sides are not two estimators of one shared statistical object.** The observed number is a Chow `level_shift` coefficient (a regression discontinuity against a fitted linear trend); the theoretical number is a direct multiplier-delta calculation on raw composition. They are two independent, reasonable proxies for "count change at the break," compared but not reconciled into a single estimate.
5. `Outside Perimeter` is excluded throughout — zero tent/vehicle/individual component data in any regime (its coverage begins in 2021), the same exclusion Task 4.3 applied to its Chow tests at these two dates.
6. Source data (`data/MasterCounts_Adjusted_v2.csv`, `data/StructuralBreaks.csv`) was verified unchanged (hash-checked) before and after this analysis ran.

---

## 7. Deliverables

- [`data/MethodologyImpact_Composition.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/MethodologyImpact_Composition.csv) — 72-row monthly tent/vehicle/individual raw composition across the 3 windows.
- [`data/MethodologyImpact_TheoreticalVsObserved.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/MethodologyImpact_TheoreticalVsObserved.csv) — 14-row theoretical-vs-observed comparison, per neighborhood + pooled, per break.
- [`MethodologyImpact_Analysis.ipynb`](file:///D:/Projects/Downtown-Homeless-Analysis/MethodologyImpact_Analysis.ipynb) — full reproducible notebook, executed end-to-end with 0 errors.
- `build_methodology_impact.py` — notebook build script.
- This report, uploaded as a Google Doc ("Methodology_ImpactAnalysis") to the `Assignment 6 - Methodology Impact Assessment` Drive folder.

**Forward note for later assignments:** any forecasting or pooled-trend model (Assignment 7) spanning April 2017 or May 2018 should account for the mechanical multiplier contribution quantified here as a small, separate component from the much larger real change these two breaks otherwise reflect — the two should not be conflated when interpreting model coefficients that span these dates.
