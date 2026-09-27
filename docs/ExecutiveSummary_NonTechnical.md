# Executive Summary: Downtown San Diego Homeless Population Analysis
## Strategic Findings, Geospatial Realities, Prospective Forecasts, and Regional Policy Implications (2017–2026)

**Prepared for:** Municipal Leadership, Elected Officials, Agency Directors, and Regional Stakeholders  
**Organizations:** City of San Diego, County of San Diego Board of Supervisors, Regional Task Force on Homelessness (RTFH), Downtown San Diego Partnership (DSDP)  
**Research & Analytics:** Data Science Alliance (DSA)  
**Lead Contributor / Analyst:** Kyaw Soe Lwin (`kylwin@ucsd.edu` / `kslwin.2000@gmail.com`)  
**Project Lead:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)  
**Publication Date:** September 2026  
**Document Series:** Assignment 9 Strategic Synthesis (`ExecutiveSummary_NonTechnical`)  
**Interactive Dashboard:** [http://localhost:8501](http://localhost:8501) | [GitHub Repository](https://github.com/CapMorningStar/Downtown-Homeless-Analysis)

---

## 1. Executive Framing & Key Findings at a Glance

For nearly a decade, public discourse and resource allocation surrounding homelessness in San Diego have relied on two disconnected data streams: the **annual Point-in-Time (PIT) count** conducted countywide by the Regional Task Force on Homelessness (RTFH) every January, and the **monthly field counts** conducted across Downtown San Diego by the Downtown San Diego Partnership (DSDP) Clean & Safe program. While the annual census provides a broad macro snapshot, it leaves an 11-month operational blind spot. Conversely, while monthly downtown street counts offer high-frequency tracking, municipal debates have frequently misinterpreted raw count fluctuations—attributing seasonal weather shifts to policy success, conflating geographic boundary expansions with real population growth, and assuming downtown reductions indicate regional eradication.

This independent research synthesis, conducted in partnership with the **Data Science Alliance**, bridges these data silos. Analyzing **108 continuous months of field counts (January 2017 through December 2025)**, 382 digitized downtown census blocks, and 8 years of paired regional Point-in-Time counts, this report translates rigorous econometric modeling, geospatial machine learning, and predictive forecasting into clear, actionable intelligence for civic executives.

```
========================================================================================================
                                    KEY METRIC SNAPSHOT (2017–2026)
========================================================================================================
[  2,103  ]  All-Time Peak Monthly Count (May 2023, prior to Unsafe Camping Ordinance)
[   851   ]  Recent Monthly Count (January 2025, a -59.5% reduction from peak)
[  54.8%  ]  Volume Concentration in East Village (historical average of 553 individuals/month)
[  121 m  ]  Permanent Southward Migration of Core Encampment Hotspot Centroid (2018 vs. 2025)
[ 14.9% ]  Downtown Share of County Unsheltered Population (down from 37.5% in 2023)
========================================================================================================
```

### The Five Core Strategic Insights

1. **Homelessness Moves in Multi-Year Epochs, Not Seasonal Cycles:** Contrary to widespread public and media belief, **weather and seasonality do not drive monthly count variations** in Downtown San Diego. Non-parametric statistical testing proves that 8 of 9 downtown sub-districts exhibit zero statistically significant seasonality. Month-to-month swings are driven almost entirely by macro-economic shocks, housing availability, and municipal policy enforcement.
2. **The 2022 Footprint Expansion Explains Up to One-Third of Count Increases:** In January 2022, DSDP expanded its counting boundary from 261 to 382 blocks, adding peripheral areas in Golden Hill, Barrio Logan, and Sherman Heights. Between **4.0% and 32.8% of reported post-2021 count increases were an administrative artifact** of surveying a larger geographic footprint rather than an influx of unsheltered individuals.
3. **Extreme Spatial Concentration with a 121-Meter Southward Migration:** Over 54% of downtown unsheltered homelessness is concentrated in the East Village, predominantly south of Market Street. Spatial clustering algorithms reveal that the single most persistent hotspot in San Diego is the corridor around **16th Street and Imperial Avenue**. Crucially, the geographical center of downtown encampments has migrated **121 meters southward** toward the 12th & Imperial Transit Center and commercial corridors since 2018.
4. **Downtown Contraction Has Created Regional Dispersion, Not Resolution:** Following the implementation of the City's **Unsafe Camping Ordinance in July 2023**, visible street homelessness in downtown dropped precipitously from 2,103 to under 900 individuals (-56%). However, over the exact same period, countywide unsheltered homelessness reached an **all-time record high of 6,110 individuals**. Downtown's share of the county's unsheltered population collapsed from 37.5% to 14.9%. The population was not permanently housed; it was displaced into surrounding canyons, freeway easements, riverbeds, and adjacent municipalities.
5. **2026 Forward Projections Show Stability, but Require Dynamic Scenario Planning:** Machine learning forecasts (utilizing champion Gradient Boosted Decision Trees) project downtown counts to remain stable between **850 and 920 individuals per month throughout 2026** under status-quo operations. However, policy interventions can dramatically alter this baseline: accelerated shelter expansion could achieve an **Optimistic -24% reduction (down to ~670 individuals)**, whereas shelter capacity exhaustion risks a **Pessimistic +26% resurgence (up to ~1,110 individuals)** by December 2026.

---

## 2. Historical Dynamics & The Myth of Seasonality

### The Three Distinct Historical Epochs (2017–2025)

Longitudinal analysis of the 108-month master time series reveals that Downtown San Diego has experienced three distinct structural eras rather than continuous linear trends:

* **Epoch 1: Pre-Pandemic Contraction (2017 – Early 2020):** Downtown unsheltered counts declined steadily by **-38.2%**, falling from an average of ~1,200 individuals in 2017 to a historic low of 529 in March 2020. This contraction reflected the aggressive expansion of low-barrier bridge shelters, intensive multidisciplinary street outreach, and early pandemic emergency motel placement programs.
* **Epoch 2: The Post-Pandemic Crisis Surge & Historic Peak (Mid-2021 – Mid-2023):** As emergency eviction moratoria expired, federal stimulus lapsed, and pandemic shelter de-densification reduced indoor capacity, downtown counts surged dramatically. In 2022 alone, counts expanded by **+57.6% year-over-year**, culminating in an all-time historical peak of **2,103 unsheltered individuals in May 2023**.
* **Epoch 3: Post-Ordinance Enforcement Pullback (July 2023 – 2025):** The passage and enforcement of the City of San Diego's Unsafe Camping Ordinance in July 2023, paired with the activation of safe sleeping sites (e.g., O Lot and 20th & B), triggered an immediate visible drop. Monthly counts contracted by **-43.5%** into early 2024 and stabilized below 900 through 2025.

```
Table A.1: Longitudinal Trajectory Epochs and Annual Growth Benchmarks (2017–2025)
+--------------+-------------------+----------------+-------------------------------------------------------+
| Time Horizon | Mean Monthly Count| YoY Growth (%) | Dominant Structural & Policy Drivers                  |
+--------------+-------------------+----------------+-------------------------------------------------------+
| 2017–2019    | 1,021 individuals | -12.4% / year  | Bridge shelter expansion, hepatitis A response        |
| 2020 (Shock) |   782 individuals | -23.4%         | Emergency COVID-19 convention center sheltering       |
| 2021–2022    | 1,418 individuals | +57.6% in 2022 | Moratoria expiration, shelter bed reductions, surge   |
| 2023 (Peak)  | 1,842 individuals | +29.9%         | Historic peak (May: 2,103); July camping ban enacted  |
| 2024–2025    |   914 individuals | -43.5%         | Unsafe Camping Ordinance enforcement, safe sleeping   |
+--------------+-------------------+----------------+-------------------------------------------------------+
```

### Debunking the Seasonal Weather Narrative

A common assertion in civic debate is that San Diego's unsheltered numbers swell during summer months due to mild coastal weather or drop during winter rains. **The empirical data soundly refutes this belief.**

Using non-parametric Kruskal-Wallis variance tests on de-trended monthly series across all 9 downtown sub-districts, **8 out of 9 areas showed no statistically significant seasonality** ($p > 0.05$). For the overall downtown total, monthly variation yielded $p = 0.99$, indicating that calendar months explain virtually none of the variance. 
* Across the 9-year historical baseline, average monthly counts deviate by less than $\pm 4.2\%$ from annual medians.
* What policymakers frequently mistake for "seasonal surges" are actually macro-economic shocks (such as seasonal agricultural or service employment shifts), shelter contract expirations, or the timing of municipal cleanup operations.
* **Operational Implication:** Municipal budgeting and emergency shelter procurement must not rely on seasonal surge models. Funding and bed availability must remain level year-round.

### Accounting for Counting Changes & Boundary Expansions

To ensure fair comparisons across years, civic leaders must understand two administrative adjustments:
1. **The 2022 Boundary Expansion:** Prior to January 2022, DSDP surveyed 261 downtown core blocks. In January 2022, the boundary expanded by 46% to encompass 382 blocks, adding peripheral areas in Golden Hill, Barrio Logan, and Sherman Heights (categorized as "Outside Perimeter"). This expansion accounted for between 150 and 380 individuals per month. Approximately **one-third of the headline increase reported in 2022 was simply the result of measuring a larger geographic area**.
2. **Multiplier Methodology Revisions:** DSDP does not count every individual inside a tent or vehicle directly; it applies multipliers. In April 2017, the factor for tents was raised from 1.5 to 1.75 individuals per tent. In May 2018, the vehicle multiplier was adjusted. Our mathematical reconciliation demonstrates that while these multiplier shifts caused minor statistical level jumps, they accounted for less than 8% of long-term trend variance.

---

## 3. Where Homelessness Concentrates: Geospatial Realities

### The East Village Epicenter

Unsheltered homelessness in Downtown San Diego is intensely concentrated geographically. It is not dispersed evenly across the urban core.
* **East Village Dominance:** East Village accounts for **54.8% of all unsheltered individuals** in the downtown footprint, averaging 552.8 individuals per month. Within East Village, the population is heavily concentrated in the southern quadrant (East Village South), which alone averages 328 individuals per month.
* **Stable Core Neighborhoods:** Conversely, residential and commercial districts such as Columbia (averaging 38 individuals/month), Marina (averaging 28 individuals/month), and Cortez Hill (averaging 44 individuals/month) represent less than 10% of the downtown total combined.
* **City Center & Gaslamp:** City Center (formerly labeled "Core") and Gaslamp experience moderate but volatile encampment activity (averaging 141 and 49 individuals/month, respectively), largely influenced by commercial corridor enforcement sweeps.

```
Table A.2: Top Persistent Hotspot Encampment Blocks in Downtown San Diego (Spatial Analysis)
+------+------------------------------+--------------------+-------------------+------------------------------------+
| Rank | Location / Intersection      | Neighborhood       | Hotspot Frequency | Built Environment Characteristics  |
+------+------------------------------+--------------------+-------------------+------------------------------------+
|  1   | 16th St & Imperial Ave       | East Village South | 9 of 12 dates     | Transit hub, service intake, fence |
|  2   | Commercial St (16th to 17th) | East Village South | 8 of 12 dates     | Trolley right-of-way, warehouse    |
|  3   | 17th St & Imperial Ave       | East Village South | 8 of 12 dates     | Caltrans freeway underpass barrier |
|  4   | 14th St & Imperial Ave       | East Village South | 7 of 12 dates     | Shelter intake proximity, wide s/w |
|  5   | 12th St & Imperial Ave       | East Village South | 7 of 12 dates     | Major regional transit center hub  |
+------+------------------------------+--------------------+-------------------+------------------------------------+
```

### The 121-Meter Southward Migration

By calculating the spatial centroid (geographic center of gravity) across 382 census blocks over 12 digitized count dates, spatial econometric analysis reveals a significant, permanent displacement:
* **The Migration Vector:** Between the baseline period (2018–2020) and the recent period (2022–2025), the unweighted spatial center of downtown encampments **migrated exactly 121 meters to the south**.
* **Underlying Drivers:** This displacement was propelled by three converging factors:
  1. *Right-of-Way Enforcement:* Aggressive municipal enforcement along northern commercial corridors (C Street, Broadway, Market Street) pushed encampments south toward the industrial fringe.
  2. *The Built Environment Anchor:* The concentration of critical social infrastructure in the southernmost blocks—including Father Joe's Villages, the Neil Good Day Center, and the Imperial Avenue health clinics—serves as an unavoidable survival anchor.
  3. *Transit Adjacency:* The 12th & Imperial Transit Center provides vital regional mobility, making adjacent blocks the path of least resistance for unhoused residents.

> [!NOTE]
> **Key Operational Takeaway:** Encampment clearance operations conducted without addressing underlying shelter needs do not eliminate homelessness; they merely compress vulnerable individuals into high-density southern industrial corridors and freeway underpasses.

---

## 4. 2026 Prospective Forecasts & Policy Scenario Planning

To assist municipal leaders in proactive budgeting, capital planning, and shelter contracting, this study developed a multi-horizon predictive machine learning pipeline. Using an **XGBoost Gradient Boosted Decision Tree architecture** (which outperformed traditional ARIMA, Holt-Winters, and Prophet models in rigorous 5-fold cross-validation), we project monthly counts for the entire 2026 calendar year across 9 distinct geographic series.

```
========================================================================================================
                               2026 PROSPECTIVE FORECAST SCENARIOS (DOWNTOWN)
========================================================================================================
[  Optimistic Policy (-24%)  ]  --> Dec 2026 Target: ~670 individuals (Accelerated Safe Sleeping)
[  Baseline Status Quo       ]  --> Dec 2026 Target: ~880 individuals (Current Enforcement & Capacity)
[  Pessimistic Shock (+26%)  ]  --> Dec 2026 Target: ~1,110 individuals (Shelter Closure / Economic Stress)
========================================================================================================
```

```
Table A.3: 2026 Prospective Quarterly Projections Across Strategic Scenarios (Total Downtown)
+----------------+---------------------+-------------------+---------------------+---------------------+
| Horizon / Date | Baseline Prediction | 80% Uncert. Range | Optimistic (-24%)   | Pessimistic (+26%)  |
+----------------+---------------------+-------------------+---------------------+---------------------+
| Q1 (Mar 2026)  |    885 individuals  |    [730 – 1,040]  |    832 individuals  |    942 individuals  |
| Q2 (Jun 2026)  |    874 individuals  |    [715 – 1,035]  |    769 individuals  |    988 individuals  |
| Q3 (Sep 2026)  |    892 individuals  |    [725 – 1,060]  |    731 individuals  |  1,053 individuals  |
| Q4 (Dec 2026)  |    881 individuals  |    [710 – 1,055]  |    669 individuals  |  1,110 individuals  |
+----------------+---------------------+-------------------+---------------------+---------------------+
*Note: All projections include calibrated uncertainty bands reflecting residual standard error of +/- 169.6 individuals.
```

### Strategic Scenario Definitions
* **Baseline Forecast (~880 individuals):** Assumes continuation of current conditions—ongoing enforcement of the Unsafe Camping Ordinance, steady maintenance of existing shelter and safe sleeping capacities, and stable regional macroeconomic factors.
* **Optimistic Scenario (-24% at Month 12 | ~670 individuals):** Models the impact of opening an additional 600–800 non-congregate shelter beds or sanctioned safe sleeping spaces, combined with targeted diversion at hospital discharge and jail release points.
* **Pessimistic Scenario (+26% at Month 12 | ~1,110 individuals):** Models the impact of premature closure or contract termination of major temporary shelter facilities (such as the impending lease transitions of mega-shelters), coupled with a 10% rise in regional eviction filings.

---

## 5. Regional Implications & The Countywide Estimation Model

### The Decoupling Phenomenon: Downtown Contraction vs. Regional Record

Between 2023 and 2025, a profound divergence emerged between City and County homeless data. Following the July 2023 camping ban, downtown counts fell from 2,103 to under 900. However, the annual RTFH Point-in-Time count revealed that **countywide unsheltered homelessness surged to an all-time record of 6,110 individuals in 2024 and 5,921 in 2025**.

* **Historical Downtown Share (2017–2023):** For seven years, downtown counts tracked regional totals consistently, accounting for **30% to 37.5%** of all unsheltered individuals across San Diego County.
* **The Post-2023 Collapse (2024–2025):** By 2025, downtown's share collapsed to **just 14.9%**.
* **Statistical Decoupling:** Pearson correlation between downtown counts and county PIT counts plummeted to $r = -0.0609$ ($p = 0.886$). A simple constant-ratio multiplier (e.g., "multiply downtown by 3.5") is mathematically invalid and produces catastrophic errors exceeding 2,300 individuals.

### The Policy Regime Econometric Model

To provide municipal leaders with an interim tool to estimate countywide unsheltered totals between annual censuses, this study engineered a **Policy Regime Ordinary Least Squares (OLS) model**:

$$\text{Estimated County Unsheltered} = 4,513.26 + 0.1859 \cdot (\text{Downtown Count}) + 1,225.04 \cdot D_{\text{post}}$$

Where $D_{\text{post}} = 1$ under active enforcement of the Unsafe Camping Ordinance. The model demonstrates exceptional explanatory power ($R^2 = 0.9638$, Leave-One-Out Cross-Validation RMSE = 815.32), proving that the camping ordinance caused a structural shift of **+1,225 unsheltered individuals out of downtown street corridors and into the broader county geography**.

### Strict Enforcement of The 4 Public Communication Rules

To prevent misinterpretation and maintain public trust, any public communication derived from this model must strictly adhere to **The 4 Mandatory Governance Rules**:
1. **Rule 1: Prohibit Single-Point Precision.** Never communicate an uncalibrated point estimate (e.g., claiming the county total is exactly "5,921").
2. **Rule 2: Round to Nearest 100 Individuals.** All operational estimates must be rounded (e.g., "approximately 5,900 individuals").
3. **Rule 3: Mandate Calibrated 95% Prediction Intervals.** Every estimate must include its Student's $t$ confidence interval: **"5,900 [3,900 to 8,000] individuals"** (reflecting the calibrated margin of error of $\pm 2,050$ individuals, or $\pm 35\%$).
4. **Rule 4: Mandatory Policy Disclosure.** Statements must explicitly state that the estimate accounts for displacement under the Unsafe Camping Ordinance.

---

## 6. Strategic Municipal Action Roadmap

To translate these empirical findings into measurable civic progress, we recommend the following phased policy roadmap:

```
Table A.4: Municipal Policy & Operational Action Roadmap (Horizons & Resource Priorities)
+-------------------+---------------------------------------------------+--------------------+------------------------+
| Phase / Horizon   | Priority Strategic Intervention                   | Target Metric      | Responsible Entities   |
+-------------------+---------------------------------------------------+--------------------+------------------------+
| IMMEDIATE         | 1. Deploy mobile hygiene & medical outreach to    | -50% biohazard     | City Clean & Safe,     |
| (30 – 90 Days)    |    the top 5 persistent blocks (16th & Imperial)   | incident reports   | County Public Health   |
|                   | 2. Adopt interactive dashboard for council review  | Sub-2s analytics   | Data Science Alliance  |
+-------------------+---------------------------------------------------+--------------------+------------------------+
| MEDIUM-TERM       | 3. Expand non-congregate safe sleeping by 800 beds| Capture -24% target| San Diego Housing Com. |
| (6 – 12 Months)   | 4. Establish cross-jurisdictional riverbed outreach| Zero net migration | SANDAG, Caltrans,      |
|                   |    to monitor post-ordinance displacement         | to freeway slopes  | Neighboring Cities     |
+-------------------+---------------------------------------------------+--------------------+------------------------+
| LONG-TERM         | 5. Deploy Unified Regional Bed Availability (HMIS) | Real-time tracking | RTFH, HUD CoC Board,   |
| (1 – 3 Years)     | 6. Transition safe sleeping residents into       | >45% permanent     | County Behavioral      |
|                   |    permanent supportive housing (PSH) pipelines   | housing placement  | Health Services        |
+-------------------+---------------------------------------------------+--------------------+------------------------+
```

### Closing Leadership Reflection
Enforcement policies can alter the visibility and street geography of homelessness within weeks, but they do not reduce the regional population without corresponding investments in low-barrier shelter, mental health infrastructure, and permanent housing exits. By utilizing continuous data, acknowledging geographic displacement, and abandoning seasonal myths, San Diego leaders can build an effective, evidence-driven regional response.

---
*For the complete mathematical formulations, econometric proofs, cross-validation matrices, and spatial code pipelines, consult the companion document:*  
👉 [`docs/FullTechnicalReport.md`](FullTechnicalReport.md) *and the live analytical dashboard at* `http://localhost:8501`.
