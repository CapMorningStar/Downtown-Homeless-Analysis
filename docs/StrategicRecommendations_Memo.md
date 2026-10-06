# Strategic Recommendations Memo
## Downtown San Diego Homeless Population Analysis (Task 9.3)

**To:** City of San Diego, County of San Diego, Regional Task Force on Homelessness (RTFH), Downtown San Diego Partnership (DSDP), downtown service providers
**From:** Data Science Alliance (DSA): Kyaw Soe Lwin, lead analyst; Adir Mancebo Jr., project lead
**Date:** October 2026
**Basis:** [`ExecutiveSummary_NonTechnical.md`](ExecutiveSummary_NonTechnical.md) and [`FullTechnicalReport.md`](FullTechnicalReport.md) (October 2026 revision, using source-corrected data)

---

## 1. Purpose

This memo turns the project's findings into recommendations for specific organizations. It is meant to be read on its own. Every number comes from the corrected October 2026 outputs, and the technical report gives the methods and caveats behind each one.

Two limits apply throughout:
* **None of the analyses identifies causes.** Where this memo mentions shelters, enforcement or displacement, it describes patterns that fit the data, not proven effects.
* **The recommendations have not yet been tested with the agencies they are addressed to** (see Section 6).

---

## 2. Bottom line

1. **Downtown changes in multi-year phases, not seasons.** Plan capacity for swings lasting several years rather than for a summer peak.
2. **A smaller downtown count is not a smaller regional problem.** Since mid-2023 downtown has fallen sharply while the county unsheltered count reached its highest level in the series.
3. **People are concentrated in a small part of East Village.** A handful of blocks around 16th–17th St / Imperial Ave and the I-5 southbound ramps are statistical hotspots on most mapped dates.
4. **Forecasts and county estimates are ranges, not numbers.** Both have wide uncertainty and should be quoted that way.
5. **The biggest gains now come from better data, not more models.** Consistent component reporting by DSDP and more digitized block maps would make every later analysis stronger.

---

## 3. What the evidence shows

### 3.1 Trend: three phases since 2017

| Period | Average monthly downtown count | Change |
|---|---:|---|
| 2017 → 2020 | about 1,060 → about 650 | −38% |
| 2021 → 2023 | rose to about 1,560 | peak 2,103 in May 2023 |
| 2024 → 2025 | about 890 | −43% from 2023, then roughly flat |

After the long-term trend is removed, the calendar month makes no statistically significant difference in 8 of 9 series (downtown total: p = 0.995).

**Implication:** seasonal surge planning is not supported by these data. Capacity and outreach budgets should be set using the multi-year range.

### 3.2 Part of the 2022–2023 rise came from counting a bigger area

In 2022 DSDP added 121 blocks in Golden Hill, Barrio Logan and Sherman Heights. On the five count dates since, those blocks made up **4–33%** of the downtown total. There was also a real increase: on the original 261 blocks alone, counts rose about 71% from early 2021 to early 2022.

**Implication:** any public comparison across 2021/2022 must say which area it covers.

### 3.3 Concentration in South East Village

East Village holds about 54% of the downtown count (about 552 people a month). Its south-east quadrant averages about 317 a month, more than the other three quadrants combined.

On the 12 dates with block-level maps (Getis-Ord Gi\*, 95% and 99% significance only):

| Block | Hotspot on (of 12 dates) |
|---|---:|
| 16th St & Imperial Ave | 9 |
| I-5 southbound at Imperial Ave | 8 |
| I-5 southbound off-ramp (map edge) | 6 |
| I-5 southbound on-ramp (map edge) | 4 |
| 17th St & Imperial Ave | 4 |

Between 2018–2020 and 2022–2025, the count-weighted center of the hotspot clusters moved about 120 m south-south-east.

**Implication:** these blocks are a sensible shortlist for coordinated outreach and field checks. They do not show *why* people concentrate there, and they are not by themselves evidence of where a new service should go.

### 3.4 Downtown and the county have moved apart since 2023

| Period | Downtown share of county unsheltered count |
|---|---|
| 2017–2020 | 16–20% |
| 2022–2023 | 35–37.5% |
| 2024–2025 | 15–17% |

Downtown January counts fell from 1,939 (2023) to 1,018 (2024) and 851 (2025). Over the same period the county unsheltered count reached 6,110 (2024), the highest in the series, and 5,714 (2025). This is consistent with people moving elsewhere rather than leaving homelessness after the July 2023 Unsafe Camping Ordinance. The project has no data on where people went, so it cannot confirm that.

**Implication:** a falling downtown count should not be read or reported as regional progress.

### 3.5 What to expect in 2026

The leading models (XGBoost, Holt-Winters, SARIMA) had similar one-year-ahead error in cross-validation, about 38–40% on average, and that error varied widely between test periods. The selected model expects downtown to stay at **about 820–900 people a month** in 2026, with a **95% range of roughly 520 to 1,240**. The naive seasonal baseline was the most accurate model on the 2025 hold-out year.

The "optimistic" (−24%) and "pessimistic" (+26%) paths, about 675 and about 1,120 by December 2026, are fixed what-if paths for stress-testing. They are not predictions of what any particular policy would achieve.

### 3.6 Estimating the county from downtown

Downtown counts alone are a weak guide to the county total (correlation −0.06 over eight paired years). The best model tested lets the relationship change after 2023 and gives a current estimate of **about 5,900 (95% range 3,900 to 8,000)**. It explains about half of the year-to-year variation (R² = 0.50), and neither of its inputs is statistically significant. It is a planning aid between annual PIT counts, not a measurement.

---

## 4. Recommendations

Each recommendation lists the finding it rests on, who should own it, and how soon.

### 4.1 Act now (0–3 months)

**R1. Use the persistent-hotspot blocks as a shortlist for joint outreach and field checks.**
*Owners:* outreach providers, City of San Diego
*Basis:* §3.3
Coordinate outreach schedules around 16th–17th St / Imperial Ave and the I-5 southbound ramps. Record contacts in a way that can be compared month to month. Treat the list as a place to start looking, not a siting decision.

**R2. Plan with ranges in every public statement.**
*Owners:* all agencies, communications staff, media partners
*Basis:* §3.5, §3.6
Apply the four public communication rules to any county estimate:
1. no exact single numbers;
2. round to the nearest 100;
3. always give the 95% range;
4. say that the estimate comes from downtown counts and assumes the post-2023 enforcement environment continues.

Use the same approach for downtown forecasts.

**R3. Always state which area a figure covers.**
*Owners:* DSDP, City, analysts
*Basis:* §3.2
When comparing totals before and after 2022, report either the fixed 261-block area or the share contributed by the added blocks.

### 4.2 Next 6–12 months

**R4. Publish complete, internally consistent monthly component data.**
*Owner:* DSDP
*Basis:* data audit (technical report §2, §10.4)
* Publish individual, tent and vehicle counts for every neighborhood every month.
* Make sure the East Village quadrant table adds up to the East Village total.
* Record the count date and conditions (weather, events, enforcement operations) in a machine-readable file.

Several of the data problems this project had to correct came from inconsistencies inside the published reports.

**R5. Test the displacement explanation directly.**
*Owners:* City, County, RTFH
*Basis:* §3.4
Use outreach contact records, or coordinated counts in neighboring areas, to see whether people who were downtown before mid-2023 are now elsewhere in the region. Without this, the post-2023 divergence can be described but not explained.

**R6. Re-run the forecasts and county model when the 2026 PIT count is published.**
*Owner:* DSA / analysts
*Basis:* §3.5, §3.6
Follow the annual update procedure in [`Dashboard_MaintenanceGuide.md`](Dashboard_MaintenanceGuide.md). Keep the naive seasonal baseline in every model comparison.

**R7. Replace the placeholder shelter-capacity series with administrative data.**
*Owners:* DSA, with SDHC/RTFH
*Basis:* Assignment 10 data audit
The shelter-capacity inputs used in the multi-source system are constructed placeholders. They should be replaced with Housing Inventory Count records before anyone draws a capacity conclusion from those models.

### 4.3 Next 1–3 years

**R8. Digitize more of the monthly block maps.**
*Owners:* DSA, DSDP
*Basis:* §3.3; technical report §10.4
Only 12 of about 90 months with usable maps have been digitized, all from January or February. Digitizing the rest is the single most valuable data investment. It would allow seasonal and post-ordinance block-level analysis, and would show whether the hotspot pattern holds outside winter.

---

## 5. What this memo does not claim

* It does not claim that the Unsafe Camping Ordinance, shelter openings, or any other policy *caused* changes in the counts.
* It does not recommend where to build or locate services. The hotspot analysis identifies places to look more closely, not unmet need.
* The county estimate is not suitable for HUD Continuum of Care submissions, formula funding, or sub-regional allocations.
* Monthly counts are single-night observations, so weather, events and enforcement on the count night all affect them.

---

## 6. Stakeholder review and user testing: pending

> **Status: pending.** The recommendations and the companion dashboard have **not yet been reviewed or tested** with the agencies named above. No feedback is reported here, and none should be assumed.

Proposed review steps:
1. Share this memo and the dashboard with DSDP, a City homelessness-strategy contact, RTFH, and at least one outreach provider.
2. Ask each reviewer three questions:
   * Is each recommendation feasible for your organization?
   * Is anything in the dashboard or memo unclear or misleading?
   * What decision would you actually use this for?
3. Record responses in a short appendix and revise the recommendations. Record who reviewed, when, and what changed.

---

*Prepared by the Data Science Alliance. Methods, full results and limitations: [`FullTechnicalReport.md`](FullTechnicalReport.md). Plain-language summary: [`ExecutiveSummary_NonTechnical.md`](ExecutiveSummary_NonTechnical.md).*
