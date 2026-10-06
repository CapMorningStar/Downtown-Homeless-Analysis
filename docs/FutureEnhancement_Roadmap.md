# Future Enhancement Roadmap
## Downtown San Diego Homeless Population Analysis (Task 9.4)

**Version:** October 2026
**Related:** [`Dashboard_MaintenanceGuide.md`](Dashboard_MaintenanceGuide.md), [`StrategicRecommendations_Memo.md`](StrategicRecommendations_Memo.md), [`FullTechnicalReport.md`](FullTechnicalReport.md) §10.4–10.5

Each enhancement is scored on two scales from 1 (low) to 5 (high):
* **Impact:** how much it would improve the reliability or usefulness of the findings.
* **Feasibility:** how easily it can be done with current data, access and skills.

Items are ranked by impact × feasibility. Ties go to the higher impact.

---

## Ranked roadmap

| Rank | Enhancement | Impact | Feasibility | Score | Owner |
|---:|---|:---:|:---:|:---:|---|
| 1 | Extend block-level digitization | 5 | 4 | 20 | DSA, DSDP |
| 2 | Replace placeholder shelter-capacity data with administrative records | 4 | 4 | 16 | DSA, SDHC/RTFH |
| 3 | Automate the annual PIT update and county-model refit | 3 | 5 | 15 | DSA |
| 4 | Machine-readable DSDP monthly reporting | 5 | 3 | 15 | DSDP |
| 5 | Prediction intervals from each champion model | 3 | 4 | 12 | DSA |
| 6 | Displacement tracking beyond downtown | 5 | 2 | 10 | City, County, RTFH |
| 7 | Clean the 311 resolution-time field | 2 | 4 | 8 | DSA |

---

## 1. Extend block-level digitization (Impact 5 · Feasibility 4)

**Problem.** Only 12 of about 90 months with usable DSDP block maps have been digitized, all from January or February. About 78 months with maps remain.

**Benefit.**
* Hotspot analysis for every season and for the period after the 2023 ordinance.
* A test of whether the South East Village cluster holds outside winter.
* More data for spatial models.

**Approach.**
1. Prioritize one map per quarter from 2023 onward, then fill in earlier years.
2. Reuse the existing digitization method and QC steps in `BlockDigitization_Methodology.md`: check against printed totals and use double entry on a sample.
3. Append to `data/BlockLevel_Counts_clean.csv`, add each new date to `DIGITIZED_COUNT_DATES`, and re-run `scripts/hotspot_analysis.py`.

**Effort.** About 2–4 analyst hours per map date. The work is mainly manual and can be split among volunteers.

## 2. Replace placeholder shelter-capacity data (Impact 4 · Feasibility 4)

**Problem.** The Assignment 10 shelter series is a hand-written timeline in `data_ingestion/sources/shelter_capacity.py`, not administrative data. Every model result that uses it (shelter headroom, the BSTS regressor, the "full system" ablation stage) inherits that weakness.

**Approach.**
1. Obtain the annual Housing Inventory Count (HIC) from RTFH, and SDHC shelter and safe-sleeping occupancy data if available.
2. Replace the source module.
3. Re-run §3.3 of the maintenance guide and update `docs/Ensemble_PerformanceReport.md`.

## 3. Automate the annual PIT update (Impact 3 · Feasibility 5)

**Problem.** After `scripts/county_estimation_build.py` runs, its constants are copied into `src/config.py` by hand. This is error-prone, and the September documentation already contained wrong values.

**Approach.**
* Have the build script write a small JSON or CSV of parameters that `src/config.py` reads.
* Add a test that the dashboard calculator reproduces `data/CountyEstimate_Current.csv`.

## 4. Machine-readable DSDP monthly reporting (Impact 5 · Feasibility 3)

**Problem.** Every month is copied by hand from PDFs. Several errors found in the audit came from DSDP's own tables disagreeing with each other, or from transcription.

**Approach.** Agree with DSDP on a simple monthly CSV covering:
* area, individuals, tents, vehicles and total;
* the East Village quadrants;
* count date and conditions.

Feasibility depends on DSDP's willingness, which is why it scores 3.

## 5. Prediction intervals from each champion model (Impact 3 · Feasibility 4)

**Problem.** The 2026 forecast intervals come from Holt-Winters residual variance, not from the error distribution of each series' selected model.

**Approach.** Derive intervals from the cross-validation residuals of each champion model, or use conformal prediction. Then check the coverage of the 80% and 95% intervals on the 2025 hold-out year.

## 6. Displacement tracking beyond downtown (Impact 5 · Feasibility 2)

**Problem.** Since 2023, downtown counts have fallen while the county count reached record levels. The project cannot tell whether people moved elsewhere.

**Approach.**
* Coordinate counts or outreach-contact records in neighboring areas (riverbeds, freeway rights-of-way, nearby cities).
* Possibly link to de-identified HMIS location histories.

Feasibility is low because it needs data-sharing agreements between several agencies.

## 7. Clean the 311 resolution-time field (Impact 2 · Feasibility 4)

**Problem.** 32 of 126 months have negative mean resolution days, which come from the source `case_age_days` field.

**Approach.** Recompute resolution time from the opened and closed timestamps. Drop records whose closed time is before their opened time, and document how many are removed.

---

## Recommended sequence

| Period | Items |
|---|---|
| Next 3 months | 3, 7 |
| Next 6–12 months | 1 (in progress), 2, 5 |
| Next 1–3 years | 1 (completion), 4, 6 |
