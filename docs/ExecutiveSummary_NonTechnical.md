# Executive Summary: Downtown San Diego Homeless Population Analysis
## What nine years of downtown counts tell us, and how far they can be trusted (2017–2026)

**Prepared for:** city and county leaders, agency directors, service providers and regional partners
**Research & analytics:** Data Science Alliance (DSA)
**Lead analyst:** Kyaw Soe Lwin (`kylwin@ucsd.edu`)
**Project lead:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)
**Version:** October 2026 (revised; see "About this revision" at the end)
**Companion document:** [`docs/FullTechnicalReport.md`](FullTechnicalReport.md)

---

## 1. Why this study, in one paragraph

San Diego has two sources of numbers on people sleeping outside:
* the **annual Point-in-Time (PIT) count**, which covers the whole county on one night each January;
* the **monthly downtown count** by the Downtown San Diego Partnership (DSDP), which covers only downtown but is repeated every month.

The annual count leaves an 11-month gap. The monthly count is easy to misread: it changed its counting rules twice, and it began covering a larger area in 2022. This study checked the monthly downtown data against the original reports, cleaned and corrected it, and used it to answer four questions:
1. How has downtown changed?
2. Where do people concentrate?
3. What is likely next year?
4. Can downtown counts tell us about the whole county?

---

## 2. Key numbers

| Measure | Value |
|---|---|
| Highest monthly downtown count | **2,103** (May 2023) |
| Lowest monthly downtown count | **529** (March 2020) |
| January 2025 downtown count | **851** |
| Share of downtown's count in East Village (2017–2025) | **54%** (about 552 people a month) |
| Downtown share of the county's unsheltered count | **16–20%** (2017–2020) → **35–37.5%** (2022–2023) → **15–17%** (2024–2025) |
| County unsheltered PIT count | **6,110** (2024, the highest in the series) · **5,714** (2025) |
| 2026 downtown forecast (status quo) | **about 820–900 a month**, with wide uncertainty |
| Current county estimate from downtown counts | **about 5,900 [3,900 to 8,000]** |

---

## 3. Five main findings

### 3.1 Downtown moves in multi-year phases, not seasons
Once the long-term trend is removed, the calendar month makes no statistically significant difference in 8 of 9 downtown series; for the downtown total, p = 0.995. Monthly averages differ from the overall average by no more than about 5%.

The real changes are multi-year:
* **2017 → 2020:** the yearly average fell from about 1,060 to about 650 a month (−38%).
* **2021 → 2023:** it rose to about 1,560 a month, peaking at 2,103 in May 2023.
* **2024:** it fell back to about 890 (−43% from 2023) and stayed near that level in 2025.

**What this means:** shelter capacity and outreach should be planned for these longer swings, not for a summer peak.

### 3.2 About a sixth to a third of the 2022–2023 increase came from counting a bigger area
In 2022 DSDP began counting 121 additional blocks in Golden Hill, Barrio Logan and Sherman Heights. On the five count dates after the change, those blocks made up between **4% and 33%** of the downtown total: 18% and 17% in early 2022, 33% in January 2023, then 4% and 10% in 2024–2025.

There was also a real increase. On the original blocks alone, counts rose about 71% from early 2021 to early 2022.

**What this means:** any comparison across 2021/2022 needs to say which area it covers.

### 3.3 People concentrate in a small part of East Village
East Village holds just over half of downtown's count. Within it, the south-east quadrant (south of Market St, east of Park Blvd) averages about 317 people a month, more than the other three quadrants combined.

Average monthly counts in the other neighborhoods:

| Neighborhood | People per month |
|---|---:|
| City Center | 171 |
| Cortez | 60 |
| Gaslamp | 48 |
| Columbia | 45 |
| Marina | 31 |

On the 12 dates with block-level maps, the blocks most often found to be statistical hotspots are:

| Block | Hotspot on (of 12 dates) |
|---|---:|
| 16th St & Imperial Ave | 9 |
| I-5 southbound at Imperial Ave | 8 |
| I-5 southbound off-ramp (map edge) | 6 |
| I-5 southbound on-ramp (map edge) and 17th St & Imperial Ave | 4 each |

All of these are in the south-east corner of East Village. Between 2018–2020 and 2022–2025, the center of these hotspot clusters (weighted by how many people were counted) shifted about **120 m to the south-south-east**.

**What this means:** these blocks are a sensible shortlist for coordinated outreach and field checks. The data do not show *why* people concentrate there, and they do not show where a new service should go.

### 3.4 Downtown and the county have moved apart since 2023
Before the pandemic, downtown's count was 16–20% of the county's unsheltered count. In 2022–2023 it was 35–37.5%. After the City's Unsafe Camping Ordinance took effect in mid-2023:
* **Downtown:** January counts fell from 1,939 (2023) to 1,018 (2024) and 851 (2025).
* **County:** the unsheltered count reached its highest level in the series (6,110 in 2024; 5,714 in 2025).

The fall downtown did not appear as a fall countywide, which is consistent with people moving elsewhere rather than leaving homelessness. This study cannot prove that, because it has no data on where people went.

**What this means:** a smaller downtown count should not be read as a smaller regional problem.

### 3.5 Next year's forecast is a range, not a number
The forecasting models were tested by repeatedly predicting periods they had not seen. The three best models (XGBoost, Holt-Winters, SARIMA) were about equally good one year ahead, with an average error of about 38–40%. Errors varied widely from one test period to another.

For 2026, the selected model expects downtown to stay at **about 820–900 people a month**. The 95% range is roughly 520 to 1,240.

The "optimistic" (−24% by December) and "pessimistic" (+26%) paths, about 675 and about 1,120 in December 2026, are fixed what-if paths for planning. They are not predictions of what specific policies would achieve.

---

## 4. Estimating the county total from downtown counts

Downtown counts alone are a weak guide to the county total. Over the eight years with both counts, the two moved almost independently: correlation −0.06. A fixed multiplier ("downtown × 4.7") would have missed by about 2,400 people on average.

The most accurate approach tested allows the relationship to change after 2023:

> County unsheltered ≈ 4,513 + 0.186 × downtown count + 1,225 (for 2024 onward)

In tests where each year was predicted from the other years, it was off by about **15%** on average (815 people). It explains only about half of the year-to-year variation (R² = 0.50). With so few years, neither of its inputs is statistically significant. It is a planning aid, not a measurement.

### Rules for any public use of a county estimate
1. **Rule 1:** never quote an exact single number (not "5,921").
2. **Rule 2:** round to the nearest 100 ("about 5,900").
3. **Rule 3:** always give the range: **"about 5,900 (95% range 3,900 to 8,000)"**.
4. **Rule 4:** say that it is estimated from downtown counts and assumes the post-2023 Unsafe Camping Ordinance enforcement environment continues.

---

## 5. How much to trust these numbers
* **Monthly totals are reliable copies of DSDP's published figures.** In October 2026 all 945 neighborhood monthly totals were checked against the source reports and matched. Typing errors in the detailed tent and vehicle counts were found and corrected: 48 East Village quadrant values for 2019 and 7 other cells.
* **DSDP's own reports occasionally disagree with themselves.** For example, a map page shows 46 people while the summary table shows 72. These months are flagged, not silently changed.
* **Each monthly figure is one night.** Weather, events and enforcement on that night all affect it.
* **Block-level maps exist for only 12 nights,** all in January or February. Hotspot findings describe those nights.
* **None of these analyses identifies causes.** Explanations involving shelters, enforcement, the economy or public health are reasonable hypotheses, not findings of this study.

---

## 6. Recommended actions

| When | Action | Who |
|---|---|---|
| Now | Publish tent, vehicle and individual counts for every neighborhood each month, and keep the East Village quadrant table consistent with the neighborhood total | DSDP |
| Now | Use the persistent-hotspot blocks around 16th & 17th St / Imperial Ave and the I-5 ramps as a shortlist for coordinated outreach and field validation | Outreach providers, City |
| Now | Quote county estimates only as rounded ranges under the four rules above | All agencies, media |
| 6–12 months | Track people leaving downtown (for example through outreach contact records) to test whether the post-2023 divergence reflects displacement | City, County, RTFH |
| 6–12 months | Re-run forecasts and the county model when the 2026 PIT count is published; plan with the forecast range, not the point forecast | DSA / analysts |
| 1–3 years | Digitize more of the monthly block maps (about 78 months with usable maps are not yet digitized) to allow seasonal and post-2023 block-level analysis | DSA, DSDP |

---

## About this revision (October 2026)

An earlier version of this summary contained several figures and claims that were not supported by the project's results:
* a model fit of R² = 0.96 (the real value is 0.50);
* a 2025 county count of 5,921 (the real count is 5,714; 5,921 is a model estimate);
* a pre-2023 downtown share of 30–37.5%;
* neighborhood averages and a hotspot table that did not match the data;
* a tent multiplier change described as "1.5 to 1.75";
* causal explanations that were never tested.

It also used data that have since been corrected against the original DSDP reports. All numbers above come from the corrected files and the companion technical report.
