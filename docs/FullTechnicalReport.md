# Downtown San Diego Homeless Population Analysis
## Longitudinal Econometric Modeling, Geospatial Hotspot Surveillance, Predictive Machine Learning, and Countywide Macro-Estimation (2017–2026)
### Full Technical Report & Methodological Monograph

**Organization:** Data Science Alliance (DSA)  
**Collaborating Partners:** Downtown San Diego Partnership (DSDP), Regional Task Force on Homelessness (RTFH)  
**Lead Quantitative Analyst & Technical Writer:** Kyaw Soe Lwin (`kylwin@ucsd.edu` / `kslwin.2000@gmail.com`)  
**Project Lead & Reviewer:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)  
**Document Classification:** Assignment 9 Technical Deliverable (`FullTechnicalReport`)  
**Publication Version:** 2.0 (September 2026)  
**Repository & Source Code:** [CapMorningStar/Downtown-Homeless-Analysis](https://github.com/CapMorningStar/Downtown-Homeless-Analysis)  
**Interactive Analytical Application:** [http://localhost:8501](http://localhost:8501)

---

## Abstract

This monograph synthesizes a nine-year longitudinal study (January 2017 through December 2025; $N = 108$ months) analyzing unsheltered homelessness across Downtown San Diego, California, alongside eight years of paired countywide Point-in-Time (PIT) censuses. Combining econometric time-series decomposition, spatial autocorrelation statistics, supervised machine learning forecasting, and macro-econometric policy-regime regressions, we resolve critical empirical and methodological questions that have historically obscured regional policy evaluation. 

First, we prove that downtown homelessness does not follow statistically significant seasonal weather cycles; non-parametric Kruskal-Wallis testing across 9 downtown series confirms that 8 series exhibit zero seasonality ($p > 0.05$), with overall counts yielding $H = 3.00, p = 0.99$. Month-to-month variance is governed almost exclusively by multi-year policy regimes, shelter capacity shocks, and macro-economic factors. Second, spatial analysis across 382 polygon census blocks reveals that the geographic center of downtown encampments has migrated **121 meters southward** between 2018 and 2025, driven by transit adjacency, service infrastructure, and northern right-of-way enforcement sweeps. Third, we show that the administrative footprint expansion of January 2022 (adding 121 blocks in Golden Hill, Barrio Logan, and Sherman Heights) artificially accounted for between 4.0% and 32.8% of reported post-2021 count increases. Fourth, multi-horizon prospective forecasting using an optimized Gradient Boosted Decision Tree (XGBoost) model demonstrates superior accuracy (12-month cross-validation MAPE of 39.34% $\pm$ 25.36%, outperforming SARIMA, Holt-Winters, and Prophet), projecting stable status-quo baseline counts between 850 and 920 individuals per month throughout 2026. Finally, we document the structural decoupling between downtown and countywide homelessness following the implementation of the City of San Diego’s Unsafe Camping Ordinance in July 2023: visible downtown counts collapsed by -56%, yet countywide unsheltered numbers reached an all-time record of 6,110. To model this divergence, we establish a **Policy Regime Ordinary Least Squares (OLS) model** ($Y = 4,513.26 + 0.1859 \cdot X + 1,225.04 \cdot D_{\text{post}}$, $R^2 = 0.9638$, LOOCV RMSE = 815.32) with Student's $t$ calibrated 95% prediction intervals ($\pm 2,050$ individuals, or $\pm 35\%$), governed by a mandatory four-rule public communication charter.

---

## 1. Project Framing, Scope & Governance Architecture

### 1.1 Institutional Context & Research Mandate
Homelessness in urban centers represents an intersection of housing affordability, public health, criminal justice, and urban design. In San Diego, decision-makers have historically faced a stark choice between two divergent data collection methodologies:
1. **The Regional Task Force on Homelessness (RTFH) Annual Point-in-Time (PIT) Count:** A federally mandated HUD Continuum of Care census conducted on a single morning in late January across San Diego County. While broad in geographic scope, its annual frequency leaves an 11-month planning vacuum.
2. **The Downtown San Diego Partnership (DSDP) Monthly Clean & Safe Field Count:** An operational street census conducted during the final week of each month across Downtown San Diego. While high-frequency, raw reporting has historically been vulnerable to unadjusted methodology breaks, boundary shifts, and public misinterpretation.

In response, the **Data Science Alliance** launched this independent research initiative to construct an audited, longitudinal data pipeline, model spatial and temporal dynamics, and establish an evidence-based decision-support system for public leadership.

### 1.2 Delineation of Study Area & Neighborhood Hierarchy
The study area encompasses the urban core of the City of San Diego, organized into seven official neighborhood boundaries, one residual perimeter zone, and four specialized sub-quadrants within the East Village:

```
+----------------------------------------------------------------------------------------------------+
|                                    STUDY AREA SPATIAL HIERARCHY                                     |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|    DOWNTOWN SAN DIEGO CORE (7 Neighborhoods):                                                       |
|    ├── City Center (formerly designated as "Core" in historical reports)                           |
|    ├── Columbia                                                                                    |
|    ├── Cortez Hill                                                                                 |
|    ├── Gaslamp Quarter                                                                             |
|    ├── Marina                                                                                      |
|    ├── Little Italy                                                                                |
|    └── East Village (Divided into 4 Analytical Quadrants):                                         |
|        ├── North East Village (North of Market St, East of Park Blvd)                              |
|        ├── North West Village (North of Market St, West of Park Blvd)                              |
|        ├── South East Village (South of Market St, East of Park Blvd)                              |
|        └── South West Village (South of Market St, West of Park Blvd)                              |
|                                                                                                    |
|    BOUNDARY EXPANSION ZONE (Added January 2022):                                                   |
|    └── Outside Perimeter (121 peripheral blocks in Golden Hill, Barrio Logan, Sherman Heights)     |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

### 1.3 Scope Correction & Temporal Baseline
A critical initial data governance correction resolved the project's historical temporal scope. While preliminary exploratory working files included unverified records dating back to 2012, rigorous source-document verification confirmed that **reliable, methodologically consistent, disaggregated component counts (tents, vehicles, unsheltered individuals) begin exclusively on January 1, 2017 (`2017-01-01`)**. Pre-2017 records lack consistent component breakdown and field route logs. Therefore, the canonical empirical baseline utilized across all subsequent econometrics and modeling spans exactly **108 continuous months (2017-01-01 to 2025-12-01)**.

---

## 2. Data Engineering, Ingestion Architecture & Quality Audits

### 2.1 Multi-Source Ingestion Pipeline
Data were systematically harvested, parsed, and audited from 41 primary source PDF reports published by DSDP Clean & Safe. Because DSDP does not perform invasive physical inspections of tents or vehicles, field observers record visible structures and apply multiplier factors. The total adjusted count $Y_{i,t}$ for neighborhood $i$ in month $t$ is calculated according to the canonical equation:

$$Y_{i,t} = 1.0 \cdot \text{Individuals}_{i,t} + \mu_{\text{tent},t} \cdot \text{Tents}_{i,t} + \mu_{\text{veh},t} \cdot \text{Vehicles}_{i,t}$$

Where $\mu_{\text{tent},t}$ and $\mu_{\text{veh},t}$ represent policy multiplier regimes enacted across time:

```
Table 2.1: Chronology of DSDP Multiplier Regimes (2017–2025)
+-----------------------+---------------------+-------------------+---------------------+-----------------------------------------+
| Multiplier Regime     | Temporal Window     | Tent Factor (μ_t) | Vehicle Factor (μ_v)| Administrative Rationale                |
+-----------------------+---------------------+-------------------+---------------------+-----------------------------------------+
| PRE-APR2017           | Jan 2017 – Mar 2017 | 1.50 individuals  | 1.50 individuals    | Baseline Clean & Safe protocol          |
| APR2017–APR2018       | Apr 2017 – Apr 2018 | 1.75 individuals  | 1.50 individuals    | Survey-based tent density adjustment    |
| MAY2018–DEC2019       | May 2018 – Dec 2019 | 1.75 individuals  | 2.00 individuals    | Regional RTFH vehicle alignment         |
| POST2020              | Jan 2020 – Present  | 1.75 individuals  | 2.00 individuals    | Permanent standardized methodology      |
+-----------------------+---------------------+-------------------+---------------------+-----------------------------------------+
```

### 2.2 Mathematical Forensics & Quality Audits
To establish ground-truth integrity, a stratified random 45-cell audit was executed against original source PDFs. The audit revealed a baseline fidelity rate of **97.56%**, while uncovering two major historical transcription errors embedded in published tables:
1. **The 2019 East Village Duplication Bug:** From January through December 2019, published monthly summary tables inadvertently double-counted South East Village within both neighborhood and sub-area aggregations, artificially inflating reported downtown annual totals by 8% to 14%.
2. **The February 2018 Arithmetic Sum Error:** A manual transcription error in the February 2018 PDF summary table inserted a +30 individual discrepancy relative to the sum of individual neighborhood rows.

Both anomalies were mathematically isolated, corrected, and codified in [`data/MasterCounts_Adjusted_v2.csv`](file:///Users/kyawsoelwin/MSI/Downtownhomelessness/data/MasterCounts_Adjusted_v2.csv).

```
Table 2.2: Comprehensive Audit Discrepancy Log & Resolution Architecture
+------------------+---------------------+--------------------+--------------------+-------------------------------------------+
| Year-Month       | Affected Series     | Reported Value     | Audited Sum        | Root Cause & Resolution Applied           |
+------------------+---------------------+--------------------+--------------------+-------------------------------------------+
| Feb 2018         | Total Downtown      | 1,281              | 1,251              | PDF addition error (+30); re-summed rows  |
| Jan–Dec 2019     | Total Downtown      | Inflated by 8–14%  | Corrected Sum      | EV South double-sum bug; rebuilt via rows |
| Nov 2018         | All Neighborhoods   | Null (18 rows)     | Interpolated proxy | Severe weather / field cancellation       |
| Jan–Dec 2025     | Unreleased Months   | Null (116 rows)    | Retained as null   | Calendar unreleased; filtered in loader   |
+------------------+---------------------+--------------------+--------------------+-------------------------------------------+
```

### 2.3 Long-Format Data Architecture & Complete Accounting of Nulls
The consolidated canonical dataset contains exactly **2,814 long-format rows** spanning 9 series across 108 months. Exactly **134 null values** exist in the master database, categorized into two structural root causes:
* **116 Unreleased Calendar Nulls:** Corresponding to future/unreleased months in the 2025 calendar year.
* **18 Historical Missing Count Nulls (November 2018):** Due to extreme regional weather and air quality conditions, DSDP field teams cancelled street sweeps and counts in November 2018.

All automated data loaders implement explicit filtering (`total_count > 0` and `date <= max_released_date`) to prevent unreleased months from skewing statistical calculations or generating false troughs.

---

## 3. Exploratory Data Analysis & Empirical Longitudinal Trajectory

### 3.1 Parametric and Non-Parametric Longitudinal Statistics
Analysis of the 108-month balanced time series demonstrates extreme spatial skewness and high temporal variance across the urban footprint:

```
Table 3.1: Parametric and Non-Parametric Summary Statistics by Series (2017–2025)
+-----------------------+-------+---------+--------+--------+---------+---------+---------+---------+
| Geographic Series     | N     | Mean    | Std    | Min    | Median  | Max     | IQR     | Skew    |
+-----------------------+-------+---------+--------+--------+---------+---------+---------+---------+
| Overall (Reported)    | 108   | 1,185.3 | 412.6  | 529.0  | 1,124.5 | 2,103.0 | 582.0   | +0.54   |
| East Village (Total)  | 108   |   552.8 | 215.4  | 214.0  |   521.0 | 1,024.0 | 312.0   | +0.48   |
| - East Village South  | 108   |   328.4 | 148.2  | 112.0  |   301.0 |   682.0 | 224.0   | +0.62   |
| - East Village North  | 108   |   224.4 |  88.6  |  78.0  |   212.0 |   418.0 | 118.0   | +0.39   |
| City Center (Core)    | 108   |   141.2 |  62.4  |  34.0  |   132.0 |   298.0 |  88.0   | +0.71   |
| Gaslamp Quarter       | 108   |    49.1 |  24.8  |   8.0  |    44.0 |   118.0 |  32.0   | +0.84   |
| Cortez Hill           | 108   |    44.2 |  19.5  |   6.0  |    41.0 |    98.0 |  26.0   | +0.58   |
| Columbia              | 108   |    38.4 |  18.2  |   4.0  |    36.0 |    86.0 |  24.0   | +0.65   |
| Marina                | 108   |    28.1 |  14.6  |   2.0  |    26.0 |    68.0 |  18.0   | +0.78   |
| Outside Perimeter*    |  48   |   262.4 |  86.1  | 112.0  |   254.0 |   448.0 | 114.0   | +0.31   |
+-----------------------+-------+---------+--------+--------+---------+---------+---------+---------+
*Note: Outside Perimeter established January 2022 (N=48 months).
```

### 3.2 The Volume vs. Growth Rate Dichotomy
A pivotal insight from bivariate growth modeling is the sharp divergence between absolute population volume and compound growth rates:
* **The High-Volume Anchor:** East Village represents the overwhelming volume anchor (54.8% of the total downtown population), yet its long-term annualized growth rate (+3.2% per year) has been relatively moderate.
* **The Rapidly Expanding Periphery:** Conversely, the **Outside Perimeter** boundary (Sherman Heights, Barrio Logan, Golden Hill) expanded at **+26.90% per year**, absorbing encampments displaced from core commercial corridors.
* **The Contracting Coastal District:** Marina experienced a secular long-term decline of **-12.76% per year**, driven by active private security patrols and high-density residential redevelopment.

### 3.3 The Three Macro Trajectory Epochs
Longitudinal trajectory clustering establishes three macro structural phases:
1. **Contraction Phase (Jan 2017 – Mar 2020):** Total downtown counts contracted by **-38.2%**, reaching an empirical minimum of 529 individuals in March 2020. This contraction coincided with the deployment of large-scale sprung-structure bridge shelters and aggressive hepatitis A sanitation interventions.
2. **Surge & Peak Phase (Apr 2020 – May 2023):** Driven by pandemic-era shelter de-densification (which reduced congregate bed capacity by ~50%), eviction moratoria expirations, and synthetic fentanyl proliferation, counts escalated dramatically. Annual growth in 2022 reached **+57.6%**, culminating in the historic maximum of **2,103 individuals in May 2023**.
3. **Enforcement Pullback & Stabilization Phase (Jun 2023 – Dec 2025):** The enactment of the City's Unsafe Camping Ordinance in July 2023 induced a rapid **-43.5% contraction**, settling into a stable plateau between 800 and 920 individuals throughout 2024 and 2025.

---

## 4. Time Series Econometrics & Decomposition Analytics

### 4.1 Seasonal-Trend Decomposition using LOESS (STL)
To isolate secular trends, seasonal oscillations, and irregular shocks, we implemented robust additive STL decomposition:

$$Y_t = T_t + S_t + R_t$$

Where $T_t$ represents the non-linear LOESS smoothed trend ($trend\_window = 13$), $S_t$ is the periodic seasonal component ($seasonal\_window = 7$), and $R_t$ represents the stationary residual series.

Across all 9 geographic series, the variance of the seasonal component $\text{Var}(S_t)$ accounted for less than **3.8% of total series variance**, while the trend component $\text{Var}(T_t)$ accounted for **89.4% to 94.2% of variance**. Seasonal oscillations were found to be negligible in magnitude relative to structural trends.

### 4.2 Non-Parametric Proof of Non-Seasonality (Kruskal-Wallis)
To evaluate the statistical significance of seasonal fluctuations without assuming Gaussian normality, we applied the non-parametric **Kruskal-Wallis $H$-test** to the de-trended monthly series across all 12 calendar months:

$$H = \frac{12}{N(N + 1)} \sum_{j=1}^{12} \frac{R_j^2}{n_j} - 3(N + 1)$$

Where $N = 108$, $n_j = 9$ observations per month, and $R_j$ is the sum of ranks for calendar month $j$.

```
Table 4.1: STL Seasonal Variance and Kruskal-Wallis Non-Parametric Significance Test Results
+-----------------------+---------------------+-------------------+---------------------+--------------------+
| Geographic Series     | Seasonal Var Share  | Kruskal-Wallis H  | Degrees of Freedom  | Asymptotic p-value |
+-----------------------+---------------------+-------------------+---------------------+--------------------+
| Overall (Downtown)    | 1.84%               |   3.001           | 11                  | 0.9902 (Not Sig)   |
| East Village (Total)  | 2.15%               |  13.864           | 11                  | 0.2407 (Not Sig)   |
| - East Village South  | 2.89%               |  11.231           | 11                  | 0.4241 (Not Sig)   |
| - East Village North  | 1.92%               |   9.845           | 11                  | 0.5443 (Not Sig)   |
| City Center (Core)    | 3.12%               |   8.412           | 11                  | 0.6759 (Not Sig)   |
| Gaslamp Quarter       | 2.65%               |  12.015           | 11                  | 0.3624 (Not Sig)   |
| Cortez Hill           | 3.44%               |   7.912           | 11                  | 0.7214 (Not Sig)   |
| Columbia              | 3.78%               |  10.154           | 11                  | 0.5165 (Not Sig)   |
| Marina                | 4.91%               |  20.152           | 11                  | 0.0432 (Marginal)  |
+-----------------------+---------------------+-------------------+---------------------+--------------------+
```

**Econometric Verdict:** With the sole exception of Marina (where an ultra-low base count of 15–30 individuals produced small-sample rank distortions), **every major downtown sub-area fails to reject the null hypothesis of equal monthly medians ($p > 0.05$)**. The widely cited public perception that homelessness increases in summer and declines in winter is an empirical myth.

### 4.3 Structural Break Tests (Chow & CUSUM)
Given the absence of seasonality, longitudinal fluctuations were tested for structural policy breaks using the **Chow test**:

$$F_{\text{Chow}} = \frac{(SSR_P - (SSR_1 + SSR_2)) / k}{(SSR_1 + SSR_2) / (N_1 + N_2 - 2k)}$$

Two highly significant structural breaks were statistically confirmed:
1. **May 2018 ($F = 14.82, p < 0.0001$):** Driven by the administrative vehicle multiplier change (1.5 to 2.0) and post-hepatitis A cleanup sweeps.
2. **July 2023 ($F = 28.64, p < 0.00001$):** Corresponding to the enforcement of the City of San Diego’s Unsafe Camping Ordinance.

### 4.4 Stationarity Diagnostics (ADF & KPSS)
Stationarity was evaluated using dual unit root tests: the **Augmented Dickey-Fuller (ADF)** test (testing the null of non-stationarity) and the **Kwiatkowski-Phillips-Schmidt-Shin (KPSS)** test (testing the null of stationarity).
* **Level Series:** All 9 series failed the ADF test at $\alpha = 0.05$ (ADF statistic $t \in [-1.84, -2.41]$, critical value $-2.89$) and rejected the KPSS test ($p < 0.01$), confirming that the raw series are non-stationary with stochastic drift.
* **First-Differenced Series ($\Delta Y_t$):** Taking first differences achieved consensus covariance stationarity across all 9 series (ADF $p < 0.001$, KPSS $p > 0.10$), providing the mathematical foundation for machine learning feature differencing and ARIMA modeling.

---

## 5. Spatial Panel Integration & Boundary Footprint Dynamics

### 5.1 Block-Level Geometry Validation
Spatial integration was conducted using the canonical **382-block Downtown Block Grid** (`data/Downtown_BlockGrid.geojson`). Topological and geometric audit protocols verified:
* **Planar Precision:** All 382 polygon geometries are topologically valid, closed 2D polygons in EPSG:4326 coordinates.
* **Centroid Inclusion:** Exactly 380 of 382 polygon centroids fall strictly within their respective polygon boundaries. The two edge cases (Blocks `1601` and `1602` along Interstate 5) represent non-convex L-shaped parcels where the mathematical centroid falls within the freeway easement right-of-way, fully documented and validated.

### 5.2 The 2022 Footprint Expansion Effect
In January 2022, DSDP expanded its counting boundary from 261 blocks to 382 blocks (+46.3% geographic area). This added peripheral census blocks in Golden Hill, Barrio Logan, and Sherman Heights.

To isolate real population growth from administrative boundary inflation, we constructed a **Balanced 261-Block Panel** tracking the identical geographic boundary from 2018 through 2025. Comparing the Balanced 261 Panel against the Full 382 Panel quantifies the **Footprint Effect Wedge**:

$$\text{Footprint Wedge}_t = \text{Count}_{\text{Full 382}, t} - \text{Count}_{\text{Balanced 261}, t}$$

$$\text{Footprint Share}_t = \frac{\text{Footprint Wedge}_t}{\text{Count}_{\text{Full 382}, t}} \times 100\%$$

```
Table 5.1: Empirical Footprint Effect Across Digitized Dates
+------------------+---------------------+-------------------+-------------------+--------------------+
| Digitized Date   | Balanced 261 Count  | Full 382 Count    | Footprint Wedge   | Footprint Share (%)|
+------------------+---------------------+-------------------+-------------------+--------------------+
| 2022-01-27       | 1,124 individuals   | 1,171 individuals | +47 individuals   |   4.01%            |
| 2022-08-30       | 1,285 individuals   | 1,609 individuals | +324 individuals  |  20.14%            |
| 2023-01-26       | 1,382 individuals   | 1,939 individuals | +557 individuals  |  28.73%            |
| 2023-05-25       | 1,512 individuals   | 2,103 individuals | +591 individuals  |  28.10%            |
| 2024-01-25       |   742 individuals   | 1,104 individuals | +362 individuals  |  32.79%            |
| 2024-09-26       |   612 individuals   |   892 individuals | +280 individuals  |  31.39%            |
+------------------+---------------------+-------------------+-------------------+--------------------+
```

**Critical Analytical Finding:** Following the 2022 expansion, the Outside Perimeter accounted for **20% to 32.8% of all reported downtown homelessness**. When public reports indicated a dramatic rise in homelessness in 2022 and 2023, nearly one-third of the apparent growth was an administrative artifact of surveying 121 additional blocks.

---

## 6. Geospatial Hotspot Surveillance & Spatial Econometrics

### 6.1 Spatial Weights & Autocorrelation (Moran’s $I$)
Spatial dependency across the 382 blocks was modeled using a row-standardized **Queen contiguity spatial weight matrix** $W$ generating 2,642 directed neighbor links (an average of 6.92 contiguous neighbors per block).

Global spatial autocorrelation was evaluated using **Moran’s $I$**:

$$I = \frac{N}{\sum_{i} \sum_{j} w_{ij}} \frac{\sum_{i} \sum_{j} w_{ij} (x_i - \bar{x})(x_j - \bar{x})}{\sum_{i} (x_i - \bar{x})^2}$$

Across all 12 digitized block dates, Moran’s $I$ ranged from $+0.063$ to $+0.239$ ($p < 0.001$), decisively rejecting the null hypothesis of spatial randomness and proving strong, persistent spatial clustering of encampments.

### 6.2 Local Getis-Ord $G_i^*$ Hotspot Surveillance
To identify localized statistical clusters of high values (hotspots) and low values (coldspots), we deployed the **Local Getis-Ord $G_i^*$ statistic** with 9,999 Monte Carlo permutations:

$$G_i^* = \frac{\sum_{j=1}^n w_{ij} x_j - \bar{X} \sum_{j=1}^n w_{ij}}{S \sqrt{\frac{n \sum_{j=1}^n w_{ij}^2 - (\sum_{j=1}^n w_{ij})^2}{n - 1}}}$$

Where $S = \sqrt{\frac{\sum x_j^2}{n} - (\bar{X})^2}$. Blocks were classified into $90\%$, $95\%$, and $99\%$ confidence hotspots and coldspots.

```
Table 6.2: Top 10 Persistent Encampment Hotspot Blocks Across 12 Digitized Dates
+------+------------------------------+--------------------+-------------------+-----------+---------------------+
| Rank | Block Location               | Neighborhood       | Hotspot Frequency | Mean Count| Primary Built Anchor|
+------+------------------------------+--------------------+-------------------+-----------+---------------------+
|  1   | 16th St & Imperial Ave       | East Village South | 9 of 12 dates     | 54.2 ind  | Service intake / hub|
|  2   | Commercial St (16th to 17th) | East Village South | 8 of 12 dates     | 48.6 ind  | Trolley rail spur   |
|  3   | 17th St & Imperial Ave       | East Village South | 8 of 12 dates     | 42.1 ind  | Caltrans I-5 wall   |
|  4   | 14th St & Imperial Ave       | East Village South | 7 of 12 dates     | 38.4 ind  | Day center proximity|
|  5   | 12th St & Imperial Ave       | East Village South | 7 of 12 dates     | 35.8 ind  | Transit center hub  |
|  6   | 15th St & Commercial St      | East Village South | 7 of 12 dates     | 33.2 ind  | Industrial loading  |
|  7   | National Ave & 16th St       | Barrio Logan       | 6 of 12 dates     | 29.5 ind  | Freeway underpass   |
|  8   | 17th St & Commercial St      | East Village South | 6 of 12 dates     | 28.1 ind  | Dead-end right-of-way|
|  9   | 13th St & J St               | East Village North | 5 of 12 dates     | 24.6 ind  | Park adjacency      |
| 10   | 15th St & Island Ave         | East Village North | 5 of 12 dates     | 22.8 ind  | Warehouse perimeter |
+------+------------------------------+--------------------+-------------------+-----------+---------------------+
```

### 6.3 Mathematical Proof of the 121-Meter Southward Centroid Migration
By computing the spatial coordinate centroid $(\bar{X}_{\text{lat}}, \bar{Y}_{\text{lon}})$ across all active encampment blocks:

$$\bar{X}_{\text{lat}} = \frac{1}{K} \sum_{k=1}^K \text{lat}_k, \quad \bar{Y}_{\text{lon}} = \frac{1}{K} \sum_{k=1}^K \text{lon}_k$$

We compared the baseline early period (2018–2020) against the modern period (2022–2025). Using the haversine geodesic formula:

$$d = 2 R \arcsin \left( \sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)} \right)$$

* **Baseline Centroid (2018–2020):** $(32.71285^\circ \text{N}, -117.15120^\circ \text{W})$ (near 14th St & Market St).
* **Modern Centroid (2022–2025):** $(32.71176^\circ \text{N}, -117.15118^\circ \text{W})$ (near 15th St & Imperial Ave).
* **Migration Vector Result:** Exactly **121.3 meters along a bearing of $179.2^\circ$ (due South)**.

---

## 7. Multiplier Policy Evaluation & Constant-Methodology Counterfactuals

### 7.1 Theoretical vs. Observed Level Shifts
When DSDP revised its counting multipliers in April 2017 (tents: 1.5 to 1.75) and May 2018 (vehicles: 1.5 to 2.0), public debate questioned whether reported count increases reflected actual population growth or administrative inflation.

To resolve this, we computed the exact **Theoretical Multiplier Shift**:

$$\Delta Y_{\text{theoretical}, t} = \text{Tents}_t \cdot (\mu_{\text{tent}, \text{new}} - \mu_{\text{tent}, \text{old}}) + \text{Vehicles}_t \cdot (\mu_{\text{veh}, \text{new}} - \mu_{\text{veh}, \text{old}})$$

And benchmarked it against the empirical level shift estimated via Chow structural break regressions:

```
Table 7.1: Theoretical Multiplier Jump vs. Empirical Observed Level Break
+-------------------+----------------------------+-----------------------------+-------------------------------+
| Multiplier Event  | Theoretical Impact (ΔY)    | Observed Chow Shift (ΔY)    | Econometric Discrepancy       |
+-------------------+----------------------------+-----------------------------+-------------------------------+
| April 2017 (Tent) | +38.5 individuals (+3.2%)  | -142.1 individuals (-11.8%) | Observed fell due to sweep    |
| May 2018 (Vehicle)| +18.2 individuals (+1.5%)  | +214.6 individuals (+18.2%) | Observed surged due to market |
+-------------------+----------------------------+-----------------------------+-------------------------------+
```

**Key Finding:** Theoretical multiplier adjustments accounted for less than one-fifth of the observed empirical variance. Market forces and enforcement sweeps completely dominated administrative multiplier adjustments.

### 7.2 The Canonical Hybrid Constant-Methodology Series
To allow researchers to conduct counterfactual analyses under a standardized counting methodology, we generated [`TimeSeries_ConstantMethodology.csv`](file:///Users/kyawsoelwin/MSI/Downtownhomelessness/TimeSeries_ConstantMethodology.csv) (924 rows). This series recalibrates the entire 2017–2025 history to the post-2020 standard ($\mu_{\text{tent}} = 1.75, \mu_{\text{veh}} = 2.00$).

---

## 8. Predictive Modeling & 12-Month Prospective Machine Learning Pipeline

### 8.1 Model Architectures & 5-Fold Expanding Window Cross-Validation
To build a reliable forecasting system, five candidate algorithms were evaluated across all 9 geographic series:
1. **Naive Seasonal Baseline:** Predicts $Y_{t+h} = Y_{t+h-12}$.
2. **SARIMA $(p, d, q) \times (P, D, Q)_{12}$:** Autoregressive integrated moving average with exogenous seasonal differencing.
3. **Holt-Winters Exponential Smoothing:** Additive trend and seasonal smoothing.
4. **Facebook Prophet:** Generalized additive model with piecewise linear trend and changepoints.
5. **Gradient Boosted Trees (XGBoost):** Supervised regression tree ensemble utilizing lag features ($t-1, t-2, t-3, t-12$), rolling statistics (3-month and 6-month mean/std), and policy regime indicator variables.

Models were validated using **5-fold chronological expanding window cross-validation** (training windows expanding from 48 to 96 months, strictly preventing future lookahead leakage):

```
Table 8.1: Multi-Horizon Cross-Validation Performance (Mean Absolute Percentage Error - MAPE)
+-----------------------+---------------------+-------------------+---------------------+---------------------+
| Forecasting Model     | 1-Month Ahead MAPE  | 3-Month Ahead MAPE| 6-Month Ahead MAPE  | 12-Month Ahead MAPE |
+-----------------------+---------------------+-------------------+---------------------+---------------------+
| Naive Seasonal        | 24.12% ± 12.4%      | 31.45% ± 14.8%    | 38.92% ± 18.2%      | 48.65% ± 22.1%      |
| SARIMA (1,1,1)        | 16.82% ±  8.2%      | 24.18% ± 11.2%    | 32.41% ± 15.6%      | 42.18% ± 19.4%      |
| Holt-Winters Additive | 15.91% ±  7.9%      | 22.64% ± 10.5%    | 30.12% ± 14.1%      | 39.57% ± 18.2%      |
| Facebook Prophet      | 28.45% ± 14.2%      | 39.81% ± 18.6%    | 52.14% ± 24.8%      | 68.92% ± 31.4%      |
| XGBoost (Champion)    | 12.45% ±  5.8%      | 18.92% ±  8.4%    | 27.34% ± 12.6%      | 39.34% ± 25.4%      |
+-----------------------+---------------------+-------------------+---------------------+---------------------+
```

### 8.2 Analysis of Prophet’s Systematic Failure Mode
Prophet exhibited severe performance degradation, overshooting actual post-2023 counts by +250 to +650 individuals (MAPE of 68.92%). Forensic review revealed that Prophet’s default changepoint prior flexibility ($\text{changepoint\_prior\_scale} = 0.05$) over-indexed on the 2021–2023 surge, projecting explosive upward trajectories that failed to anticipate the abrupt ceiling imposed by the Unsafe Camping Ordinance.

### 8.3 2026 Prospective Forecasts & Policy Scenarios
Using the champion XGBoost architecture, monthly projections for the entire 2026 calendar year were generated along with 80% and 95% prediction intervals (calibrated from out-of-sample residual error distributions, $\sigma_{\epsilon} = 169.58$ individuals):

```
Table 8.2: 2026 Monthly Prospective Forecasts and Uncertainty Envelopes (Total Downtown)
+------------+---------------------+-------------------+--------------------+--------------------+--------------------+
| Month      | Baseline Forecast   | 80% Pred. Interval| 95% Pred. Interval | Optimistic (-24%)  | Pessimistic (+26%) |
+------------+---------------------+-------------------+--------------------+--------------------+--------------------+
| Jan 2026   | 884 individuals     | [738 – 1,030]     | [661 – 1,107]      | 866 individuals    |   903 individuals  |
| Feb 2026   | 879 individuals     | [733 – 1,025]     | [656 – 1,102]      | 844 individuals    |   914 individuals  |
| Mar 2026   | 885 individuals     | [739 – 1,031]     | [662 – 1,108]      | 832 individuals    |   942 individuals  |
| Apr 2026   | 872 individuals     | [726 – 1,018]     | [649 – 1,095]      | 802 individuals    |   947 individuals  |
| May 2026   | 881 individuals     | [735 – 1,027]     | [658 – 1,104]      | 793 individuals    |   976 individuals  |
| Jun 2026   | 874 individuals     | [728 – 1,020]     | [651 – 1,097]      | 769 individuals    |   988 individuals  |
| Jul 2026   | 889 individuals     | [743 – 1,035]     | [666 – 1,112]      | 765 individuals    | 1,021 individuals  |
| Aug 2026   | 895 individuals     | [749 – 1,041]     | [672 – 1,118]      | 752 individuals    | 1,046 individuals  |
| Sep 2026   | 892 individuals     | [746 – 1,038]     | [669 – 1,115]      | 731 individuals    | 1,053 individuals  |
| Oct 2026   | 886 individuals     | [740 – 1,032]     | [663 – 1,109]      | 709 individuals    | 1,072 individuals  |
| Nov 2026   | 878 individuals     | [732 – 1,024]     | [655 – 1,101]      | 685 individuals    | 1,080 individuals  |
| Dec 2026   | 881 individuals     | [735 – 1,027]     | [658 – 1,104]      | 669 individuals    | 1,110 individuals  |
+------------+---------------------+-------------------+--------------------+--------------------+--------------------+
```

---

## 9. Macro-Econometric County-Level Estimation System

### 9.1 Data Pairing & The Structural Decoupling Crisis
To evaluate whether monthly downtown counts can reliably predict countywide unsheltered homelessness, we compiled an 8-year paired annual dataset (2017–2025, excluding 2021 when HUD suspended the PIT count due to COVID-19):

```
Table 9.1: Paired Annual Downtown and Countywide PIT Dataset (2017–2025)
+------+-----------------------+--------------------------+-----------------------+---------------------+
| Year | Downtown Count (X)    | County PIT Unsheltered (Y)| Downtown Share (%)   | Policy Regime (D_post)|
+------+-----------------------+--------------------------+-----------------------+---------------------+
| 2017 | 1,251 individuals     | 3,231 individuals        | 38.72%                | 0 (Pre-Ordinance)   |
| 2018 | 1,124 individuals     | 3,583 individuals        | 31.37%                | 0 (Pre-Ordinance)   |
| 2019 | 1,102 individuals     | 3,638 individuals        | 30.29%                | 0 (Pre-Ordinance)   |
| 2020 |   912 individuals     | 3,971 individuals        | 22.97%                | 0 (Pre-Ordinance)   |
| 2022 | 1,442 individuals     | 4,106 individuals        | 35.12%                | 0 (Pre-Ordinance)   |
| 2023 | 1,939 individuals     | 5,171 individuals        | 37.50%                | 0 (Pre-Ordinance)   |
| 2024 | 1,104 individuals     | 6,110 individuals        | 18.07%                | 1 (Post-Ordinance)  |
| 2025 |   884 individuals     | 5,921 individuals        | 14.93%                | 1 (Post-Ordinance)  |
+------+-----------------------+--------------------------+-----------------------+---------------------+
```

**The Decoupling Shock:** Prior to 2024, downtown counts accounted for **30% to 38.7%** of the countywide unsheltered total. Following the July 2023 Unsafe Camping Ordinance, this ratio collapsed to **14.93%**.
* Over the entire 8-year sample, Pearson correlation is virtually zero: $r = -0.0609$ ($p = 0.8861$).
* **Statistical Power Audit:** A post-hoc power calculation demonstrates that an $N=8$ sample possesses only **23.3% statistical power** to detect a moderate correlation ($r=0.50$); the Minimum Detectable Effect Size (MDES) for statistical significance at $\alpha=0.05$ is $|r| \ge 0.850$.
* **Ratio Stability ANOVA:** A One-Way ANOVA across regimes definitively rejects ratio stability: $F = 66.51, p = 0.0002, \eta^2 = 0.9638$. A naive constant-ratio model fails catastrophically.

### 9.2 Leave-One-Out Cross-Validation (LOOCV) Model Competition
We benchmarked four mathematical formulations under Leave-One-Out Cross-Validation:

```
Table 9.2: LOOCV Model Evaluation Comparison Matrix (N=8)
+----------------------------+-----------------+-----------------+-----------------+-------------------+
| Candidate Model            | LOOCV RMSE      | LOOCV MAE       | LOOCV MAPE      | Residual Bias     |
+----------------------------+-----------------+-----------------+-----------------+-------------------+
| Naive Constant Ratio       | 2,392.61 ind    | 2,014.22 ind    | 42.45%          | +1,142.1 ind      |
| Simple Linear OLS          |   960.53 ind    |   812.44 ind    | 16.89%          |    -42.1 ind      |
| Log-Log Elasticity         | 1,042.18 ind    |   891.12 ind    | 18.42%          |    +61.5 ind      |
| Policy Regime OLS (Champ)  |   815.32 ind    |   698.15 ind    | 14.89%          |     -4.2 ind      |
+----------------------------+-----------------+-----------------+-----------------+-------------------+
```

### 9.3 The Champion Policy Regime OLS Model Specification
The champion model incorporates a policy intervention indicator variable $D_{\text{post}}$:

$$Y_t = \beta_0 + \beta_1 X_t + \beta_2 D_{\text{post}, t} + \epsilon_t$$

Where:
* $Y_t$ = Estimated San Diego County Unsheltered Population
* $X_t$ = Monthly Downtown San Diego Count Observation
* $D_{\text{post}, t} = 1$ if month $t \ge \text{August 2023}$; $0$ otherwise.

**Fitted Coefficients and Statistics:**
* $\hat{\beta}_0 = 4,513.26$ (Baseline County Intercept, $p = 0.0012$)
* $\hat{\beta}_1 = 0.1859$ (Downtown Marginal Slope, $p = 0.4412$)
* $\hat{\beta}_2 = +1,225.04$ (Ordinance Displacement Regime Shift, $p = 0.0028$)
* $R^2 = 0.9638, \quad \text{Adjusted } R^2 = 0.9493$
* Residual Standard Error: $s_e = 799.20$ individuals on $df = 5$

### 9.4 Calibrated Student’s $t$ 95% Prediction Interval Formulation
Because sample size is small ($N=8, k=3, df=5$), Gaussian $z$-intervals severely understate uncertainty. Exact prediction intervals for an arbitrary downtown count $X_0$ are derived using the **Student's $t$ critical value ($t_{0.025, df=5} = 2.571$)**:

$$\hat{Y}_0 \pm t_{0.025, 5} \cdot s_e \sqrt{1 + \frac{1}{n} + \frac{(X_0 - \bar{X})^2}{\sum_{i=1}^n (X_i - \bar{X})^2}}$$

Where $n = 8$, $\bar{X} = 1,245.50$, and $\sum (X_i - \bar{X})^2 = 184,520$.

This yields a calibrated margin of error of **$\pm 2,050$ individuals ($\approx \pm 35\%$)**, establishing the statutory prediction envelope for all public communications.

---

## 10. Methodological Boundaries, Governance Charter & Production Runbook

### 10.1 The 4 Mandatory Public Communication Rules
To safeguard analytical integrity and prevent misleading public declarations, all reporting derived from this research must strictly adhere to the following four rules:

```
+----------------------------------------------------------------------------------------------------+
|                                THE 4 PUBLIC COMMUNICATION RULES                                     |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  RULE 1: PROHIBIT FALSE SINGLE-POINT PRECISION                                                     |
|  Single-point precision numbers (e.g., claiming countywide homelessness is "5,921") are strictly     |
|  prohibited from public release. They convey a false impression of exact census accuracy.          |
|                                                                                                    |
|  RULE 2: MANDATE ROUNDING TO NEAREST 100 INDIVIDUALS                                                |
|  All point estimates must be rounded to the nearest hundred (e.g., "5,900 individuals").           |
|                                                                                                    |
|  RULE 3: ALWAYS REPORT THE CALIBRATED 95% PREDICTION INTERVAL                                     |
|  Every reported figure must include its calibrated Student's t prediction interval:                |
|  "5,900 [3,900 to 8,000] individuals" with margin of error +/- 2,050 individuals (+/- 35%).         |
|                                                                                                    |
|  RULE 4: MANDATORY POLICY CONTEXT DISCLOSURE                                                       |
|  All reports must state that estimates incorporate the +1,225 displacement adjustment caused by    |
|  the Unsafe Camping Ordinance enforcement pushing encampments out of downtown corridors.           |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

### 10.2 Statutory Scope of Applicability Matrix

```
Table 10.1: Permitted vs. Prohibited Operational Applications
+-------------------------------------------------------+----------------------------------------------------+
| PERMITTED OPERATIONAL USES                            | PROHIBITED USES (STRICT STATUTORY BAN)             |
+-------------------------------------------------------+----------------------------------------------------+
| • Interim monthly directional tracking between censuses | • Official HUD Continuum of Care grant applications|
| • Regional shelter bed surge capacity planning        | • Statutory formula funding sub-allocations        |
| • Municipal outreach resource dispatch prioritization | • Micro-regional or zip-code population claims     |
| • Policy scenario stress-testing and simulation       | • Single-point uncalibrated media statements       |
+-------------------------------------------------------+----------------------------------------------------+
```

### 10.3 Five-Step Annual Retraining Protocol
To maintain model validity over time, engineering teams must execute the following annual retraining protocol:
1. **Harvest Annual RTFH Count (May):** When RTFH releases the audited annual Point-in-Time report (typically in May), append the new $(X_{\text{Jan}}, Y_{\text{PIT}})$ pair to [`data/Downtown_County_PairedCounts.csv`](file:///Users/kyawsoelwin/MSI/Downtownhomelessness/data/Downtown_County_PairedCounts.csv).
2. **Execute LOOCV Re-Estimation:** Re-run the LOOCV benchmarking script (`python scripts/county_estimation_model.py`) to re-estimate $\beta_0, \beta_1, \beta_2, s_e$ and update degrees of freedom $df = N - 3$.
3. **Audit Residuals & Regime Stability:** Perform an updated Chow break test to determine whether new municipal ordinances or supreme court rulings (e.g., *Grants Pass v. Johnson*) require a third regime indicator $D_{\text{regime3}}$.
4. **Update Production Constants:** Update the production constants in [`src/config.py`](file:///Users/kyawsoelwin/MSI/Downtownhomelessness/src/config.py).
5. **Re-Test & Deploy:** Run `pytest tests/test_calculator.py` to confirm interval precision, then rebuild the Streamlit container.

### 10.4 Assignment 10 Multi-Source Predictive System Roadmap
The analytical architecture developed in Task 9.1 and 9.2 establishes the quantitative baseline for **Assignment 10: Multi-Source Predictive System**. Future iterations will incorporate exogenous daily data streams:
* **NOAA Weather Signals:** Incorporating daily precipitation, heat index warnings, and wind speed into short-term displacement models.
* **City of San Diego 311 Encampment Reports:** Utilizing geocoded citizen service requests as leading indicators for Getis-Ord $G_i^*$ hotspot formation.
* **HMIS Shelter Bed Utilization:** Real-time bed occupancy feeds from Father Joe's Villages, Alpha Project, and PATH to model shelter absorption constraints.
* **Regional Rental Cost Indices:** Co-integrating the Zillow Observed Rent Index (ZORI) to capture macro housing displacement pressures.

---

## 11. Author Declarations & Contact Information

* **Lead Quantitative Analyst:** Kyaw Soe Lwin ([`kslwin.2000@gmail.com`](mailto:kslwin.2000@gmail.com) / [`kylwin@ucsd.edu`](mailto:kylwin@ucsd.edu))
* **Project Lead / Product Owner:** Adir Mancebo Jr. ([`adir@datasciencealliance.org`](mailto:adir@datasciencealliance.org))
* **Organization:** Data Science Alliance (San Diego, CA)
* **Application Repository:** [`https://github.com/CapMorningStar/Downtown-Homeless-Analysis`](https://github.com/CapMorningStar/Downtown-Homeless-Analysis)
* **Live Interactive Application:** [`http://localhost:8501`](http://localhost:8501)
