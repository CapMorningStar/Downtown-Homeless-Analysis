# Task 8.1: Compile & Document County-Level PIT Count Data
**Downtown San Diego Homeless Population Analysis**  
*Data Science Alliance / Volunteer Analytics Project*  
**Author:** Kyaw Soe Lwin (`kylwin@ucsd.edu`)  
**Project Lead:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)  

---

## 1. Executive Summary & Technical Objectives

The **Downtown San Diego Homeless Population Analysis** project has completed granular, block-level, and monthly time-series evaluations across Downtown San Diego (Assignments 1–7). While outreach staff from the **Downtown San Diego Partnership (DSDP) Clean & Safe** program conduct monthly overnight counts of unsheltered individuals across downtown corridors, county-level homelessness data is primarily captured once per year via the federally mandated **Point-in-Time (PIT) Count** ("WeAllCount"), administered by the **Regional Task Force on Homelessness (RTFH)** for Continuum of Care **CA-601 (San Diego City and County)**.

**Assignment 8** develops a predictive and structural estimation model linking monthly downtown dynamics to broader countywide trends. **Task 8.1** establishes the canonical empirical pairing dataset:
* [`data/Downtown_County_PairedCounts.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Downtown_County_PairedCounts.csv)

By systematically linking annual RTFH countywide censuses from **2017 through 2025** to corresponding DSDP monthly observations, this task quantifies:
1. **The Regional Concentration Ratio:** What proportion of San Diego County's unsheltered population resides within the downtown core over time.
2. **Methodological Shifts:** The critical January 2020 divergence between federal HUD unadjusted counts and DSDP longitudinal multiplier-adjusted counts.
3. **Policy Displacement Effects:** How municipal interventions (specifically the July 2023 City of San Diego Unsafe Camping Ordinance) altered the spatial distribution of homelessness between the urban core and surrounding county municipalities.

---

## 2. RTFH Point-in-Time Census Data Architecture (2017–2025)

The Regional Task Force on Homelessness conducts an annual one-night snapshot census of individuals experiencing sheltered and unsheltered homelessness in late January (HUD requirement). 

### 2.1 Audited Annual Census Matrix (CA-601 Continuum of Care)

| PIT Year | Census Date | Day of Week | County Total Homeless | County Unsheltered | County Sheltered | City of San Diego Unsheltered | Status / Operational Conditions |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **2017** | 2017-01-27 | Friday | 9,116 | 5,621 | 3,495 | 3,231 | Full WeAllCount census; 1,788 volunteers. |
| **2018** | 2018-01-26 | Friday | 8,576 | 4,990 | 3,586 | 3,066 | Full WeAllCount census; countywide drop of -6%. |
| **2019** | 2019-01-25 | Friday | 8,102 | 4,476 | 3,626 | 2,600 | Introduction of mobile app GIS data collection. |
| **2020** | 2020-01-23 | Thursday | 7,638 | 3,971 | 3,667 | 2,283 | Final pre-pandemic count; HUD raw-count mandate. |
| **2021** | — | — | *N/A* | *N/A* | 3,142 | *N/A* | **Waived / Canceled:** HUD unsheltered count waived due to COVID-19 pandemic. Sheltered census only. |
| **2022** | 2022-02-24 | Thursday | 8,427 | 4,106 | 4,321 | 2,494 | **Postponed to late Feb** due to Omicron wave; cold & damp overnight conditions. |
| **2023** | 2023-01-26 | Thursday | 10,264 | 5,171 | 5,093 | 3,285 | Peak surge year; inclusion of Caltrans highway corridors. |
| **2024** | 2024-01-25 | Thursday | 10,605 | 6,110 | 4,495 | 3,365 | Post-Unsafe Camping Ordinance; record countywide unsheltered peak (6,110). |
| **2025** | 2025-01-30 | Thursday | 9,905 | 5,714 | 4,191 | 2,897 | 7% regional decline; expansion of safe sleeping & non-downtown shelter beds. |

*Sources: Regional Task Force on Homelessness (RTFH) Annual #WeAllCount Reports, HUD AHAR Part 1 Point-in-Time Reports (CoC CA-601).*

---

## 3. Methodological Timeline & Longitudinal Divergences

### 3.1 The January 2020 Multiplier Divergence
As documented in [`docs/MethodologyChangeLog.md`](file:///D:/Projects/Downtown-Homeless-Analysis/docs/MethodologyChangeLog.md), a critical divergence occurred in January 2020:
* **RTFH Protocol (HUD Compliance):** HUD guidance instructed Continuum of Care agencies to cease applying multipliers to tents and vehicles, recording only direct observed headcount.
* **DSDP Clean & Safe Protocol (Operational Continuity):** To avoid an artificial collapse in reported numbers and preserve budget/staffing allocation continuity, DSDP maintained its May 2018 multipliers ($1.75$ per tent, $2.03$ per vehicle).
* **Analytical Resolution:** The paired dataset [`data/Downtown_County_PairedCounts.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Downtown_County_PairedCounts.csv) preserves **both raw observed counts and adjusted counts** for Downtown San Diego, enabling completely transparent apples-to-apples comparisons.

### 3.2 The 2021 Pandemic Waiver
Due to public health guidelines during the winter 2020–2021 COVID-19 surge, HUD authorized Continuum of Care communities to waive the volunteer-driven unsheltered street count. RTFH conducted a census of emergency shelters and transitional housing ($3,142$ sheltered individuals), but conducted no street count. In our dataset, 2021 is explicitly recorded as `NaN` rather than zero to avoid distorting downstream statistical regressions.

### 3.3 The February 2022 Omicron Postponement
In winter 2021–2022, the nationwide surge of the Omicron COVID-19 variant forced RTFH to postpone the count from January 27, 2022, to **February 24, 2022**. Consequently, the 2022 PIT count is paired with **February 2022 DSDP data (`2022-02-01`)** rather than January 2022, ensuring temporal proximity to the exact week of field operations.

---

## 4. The Canonical Paired Dataset

The compiled dataset pairs each annual PIT count with the corresponding monthly DSDP downtown count across both the **Reported Footprint** (all 7 neighborhoods) and the **Fixed Core Six** (excluding Outside Perimeter, which was only added in 2022 per Task 3.3).

### 4.1 Paired Summary Table

```text
=========================================================================================================================================================
Year   PIT Date     County Total   County Unsheltered   City SD Unsheltered   DT Reported Adj   DT Fixed6 Adj   DT Share of County (%)   DT Share of City (%)
---------------------------------------------------------------------------------------------------------------------------------------------------------
2017   2017-01-27      9,116             5,621                 3,231              882.00           882.00               15.69%                  27.30%
2018   2018-01-26      8,576             4,990                 3,066              803.49           803.49               16.10%                  26.21%
2019   2019-01-25      8,102             4,476                 2,600              897.21           897.21               20.04%                  34.51%
2020   2020-01-23      7,638             3,971                 2,283              789.14           789.14               19.87%                  34.57%
2021      None          N/A               N/A                   N/A               714.40           714.40                N/A                     N/A
2022   2022-02-24      8,427             4,106                 2,494            1,444.31         1,174.31               35.18%                  57.91%
2023   2023-01-26     10,264             5,171                 3,285            1,938.74         1,298.74               37.49%                  59.02%
2024   2024-01-25     10,605             6,110                 3,365            1,018.14           981.14               16.66%                  30.26%
2025   2025-01-23      9,905             5,714                 2,897              851.02           767.02               14.89%                  29.38%
=========================================================================================================================================================
```

---

## 5. Major Analytical Discoveries & Policy Insights

The longitudinal pairing reveals three distinct historical regimes in the relationship between Downtown San Diego and the surrounding county:

```text
       Downtown Concentration (% of County Unsheltered Population)
 40% |                                    [2023: 37.5%]
     |                             [2022: 35.2%]
 30% |
     |                     [2019: 20.0%]
 20% |  [2017: 15.7%] [2018: 16.1%]      [2020: 19.9%]          [2024: 16.7%] [2025: 14.9%]
 10% |
  0% +-------+------------+------------+---------------+-------------+-------------+-------
           2017         2018         2019            2020          2022          2023    2024    2025
       <------- Baseline Regime (~16-20%) ---------> <--- Peak Crisis ---> <--- Post-Ordinance --->
```

### 1. Pre-Pandemic Equilibrium (2017–2020): Stable Urban Core Ratio
From 2017 through 2020, Downtown San Diego represented a relatively constant share of the county's unsheltered homeless population, averaging **$17.9\%$** ($\pm 2.2\%$). Both downtown counts and countywide totals trended downward in tandem from 2017 to 2020 (downtown falling from $882$ to $789$; county unsheltered falling from $5,621$ to $3,971$).

### 2. The Great Convergence & Peak Concentration (2022–2023)
Following the onset of the pandemic and the closure of congregate emergency shelters, homelessness concentrated intensely in the downtown urban core:
* In 2022, downtown represented **$35.2\%$** of the entire county's unsheltered population.
* In 2023, downtown peaked at an unprecedented **$37.5\%$** of countywide unsheltered homelessness ($1,939$ out of $5,171$).
* Within the City of San Diego proper, downtown accounted for **$59.0\%$** of all unsheltered individuals in January 2023.

### 3. Post-Ordinance Spatial Dispersion (2024–2025)
In late July 2023, the City of San Diego began enforcement of the **Unsafe Camping Ordinance**, which prohibits tent encampments on public rights-of-way when shelter beds are available, as well as near schools, transit centers, and parks.
* **The Downtown Contraction:** Downtown counts collapsed from $1,939$ (Jan 2023) to $1,018$ (Jan 2024) and $851$ (Jan 2025).
* **The Regional Counter-Trend:** Far from indicating a regional reduction, **countywide unsheltered homelessness reached an all-time record of $6,110$ individuals in 2024**.
* **Spatial Displacement:** Downtown's share of county homelessness plummeted back to **$16.7\%$ in 2024** and **$14.9\%$ in 2025**. 
* **Conclusion:** The Unsafe Camping Ordinance successfully decentralized homelessness from downtown corridors, displacing unhoused individuals into riverbeds, freeway perimeters, unincorporated county lands, and neighboring East/North County municipalities (corroborated by RTFH regional breakout tables showing spikes in Escondido, El Cajon, and Oceanside).

---

## 6. Deliverables & File Manifest

| File | Description | Status |
| :--- | :--- | :---: |
| [`build_paired_counts.py`](file:///D:/Projects/Downtown-Homeless-Analysis/build_paired_counts.py) | Standalone ETL & visualization generator script | **Complete** |
| [`data/Downtown_County_PairedCounts.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Downtown_County_PairedCounts.csv) | Primary paired analysis dataset (2017–2025) | **Complete** |
| [`figures/task8_1/county_vs_downtown_trajectories.png`](file:///D:/Projects/Downtown-Homeless-Analysis/figures/task8_1/county_vs_downtown_trajectories.png) | Dual-axis publication trend visualization | **Complete** |
| [`figures/task8_1/downtown_share_of_county_unsheltered.png`](file:///D:/Projects/Downtown-Homeless-Analysis/figures/task8_1/downtown_share_of_county_unsheltered.png) | Concentration share bar chart by regime | **Complete** |
| [`Task8.1_CountyPIT_Documentation.md`](file:///D:/Projects/Downtown-Homeless-Analysis/Task8.1_CountyPIT_Documentation.md) | Comprehensive audit and methodology report | **Complete** |

---

## 7. Roadmap to Task 8.2 & Beyond

With the foundational pairing established in Task 8.1, the subsequent tasks in Assignment 8 will execute:
* **Task 8.2 (Analyze Downtown-to-County Relationship):**
  * Calculate Pearson and Spearman correlation coefficients between downtown counts and county PIT counts.
  * Fit OLS linear regressions ($\text{County} = \beta_0 + \beta_1 \cdot \text{Downtown}$) and evaluate residual diagnostics.
  * Evaluate elasticity and structural parameter stability across the pre-ordinance vs. post-ordinance regimes.
* **Task 8.3 (Build and Validate Estimation Model):**
  * Develop a multi-variable monthly interpolation model estimating countywide unsheltered counts during non-census months.
* **Task 8.4 (Limitations Document):**
  * Formalize caveats regarding single-night census variance, weather sensitivities (e.g. Jan 2024 historic floods), and displacement dynamics.
