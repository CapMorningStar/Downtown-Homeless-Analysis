# Downtown-to-County Correlation Analysis & Ratio Stability Report
**Project:** Downtown San Diego Homeless Population Analysis  
**Assignment:** Assignment 8 — County-Level Estimation Model  
**Task:** Task 8.2 — Analyze the downtown-to-county relationship  
**Author:** Kyaw Soe Lwin  
**Organization:** Data Science Alliance (`datasciencealliance.org`)  
**Date:** September 19, 2026  
**Status:** Completed & Verified  

---

## 1. Executive Summary

This report establishes the empirical, correlation, and ratio dynamics between Downtown San Diego monthly unsheltered homeless counts and annual Regional Task Force on the Homeless (RTFH) Point-in-Time (PIT) county-wide census data across 2017–2025 ($N=8$ observed paired years, with 2021 unsheltered census waived by HUD due to COVID-19). This analysis provides the mandatory empirical foundation for Task 8.3's county-level estimation model.

### Primary Analytical Findings:
1. **Empirical Decoupling across the Full Time Series ($r = -0.0609$):**
   * Across the entire 2017–2025 longitudinal baseline, Downtown counts exhibit an essentially zero parametric correlation ($r = -0.0609, p = 0.8861$) and weak rank correlation ($\rho = +0.2143, p = 0.6103$) with county-wide unsheltered counts.
   * This aggregate non-correlation is driven by a massive **structural divergence in 2024–2025**, following enforcement of the City of San Diego's July 2023 Unsafe Camping Ordinance: County unsheltered homelessness reached an all-time record of 6,110 (2024), while Downtown counts simultaneously contracted by nearly 50% from their peak (dropping from 1,939 to 1,018).
2. **Decisive Rejection of Constant-Ratio Hypothesis ($F = 66.51, p < 0.0002$):**
   * A One-Way ANOVA across three distinct policy regimes reveals that the downtown-to-county ratio ($R_t$) has undergone profound structural shifts:
     - **Regime 1 (Pre-Pandemic Baseline, 2017–2020):** Downtown share averaged **$17.93\% \pm 2.27\%$** of county unsheltered population.
     - **Regime 2 (Peak Crisis Convergence, 2022–2023):** Downtown concentration surged to **$36.34\% \pm 1.63\%$** of county unsheltered population (and $59.0\%$ of the City of San Diego).
     - **Regime 3 (Post-Ordinance Spatial Dispersion, 2024–2025):** Downtown concentration dropped back to **$15.78\% \pm 1.25\%$** of county unsheltered population.
   * The ANOVA effect size is extraordinarily large ($\eta^2 = 0.9638$), indicating that **$96.4\%$ of all variance in the downtown-to-county share is attributable to policy and historical regime shifts**, rather than random sampling noise.
3. **Constant-Methodology Footprint Moderates Ratio Volatility:**
   * Evaluating the **Core 6 Constant-Methodology** series (Tasks 3.3 and 6.3) reduces the coefficient of variation (CV) from $41.2\%$ down to $27.2\%$, confirming that footprint expansion (adding Barrio Logan, Sherman Heights, and Golden Hill in 2022) artificially amplified reported crisis-era downtown totals.
4. **Small-Sample Statistical Power Constraints ($N=8$):**
   * With only 8 paired annual observations, statistical power to detect a moderate correlation ($|r| = 0.50$) is only **$23.3\%$** ($\beta = 76.7\%$ risk of Type II error).
   * The **Minimum Detectable Effect Size (MDES)** at standard $80\%$ power is **$|r| \ge 0.850$** ($|r| \ge 0.896$ at $90\%$ power). To reliably detect moderate correlation ($r=0.50$), a minimum sample size of **$N = 30$ annual censuses** would be mathematically required.
   * Consequently, lack of statistical significance in correlation tests cannot be construed as evidence of no underlying systemic relationship.

---

## 2. Paired Dataset Architecture & Verification

The analysis ingests canonical data compiled in Task 8.1 ([`data/Downtown_County_PairedCounts.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Downtown_County_PairedCounts.csv)), aligning RTFH PIT annual counts with corresponding January/February Downtown counts.

### Table 1: Canonical Paired Longitudinal Counts (2017–2025)
| Year | PIT Date | County Unsheltered | City SD Unsheltered | Downtown Reported Adj | Downtown Core 6 Const | Downtown Share of County (%) | Downtown Share of City (%) | Policy Regime Classification |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **2017** | 2017-01-27 | 5,621 | 3,231 | 882.00 | 853.17 | 15.69% | 27.30% | Pre-Pandemic Baseline |
| **2018** | 2018-01-26 | 4,990 | 3,066 | 803.49 | 808.67 | 16.10% | 26.21% | Pre-Pandemic Baseline |
| **2019** | 2019-01-25 | 4,476 | 2,600 | 897.21 | 897.21 | 20.04% | 34.51% | Pre-Pandemic Baseline |
| **2020** | 2020-01-23 | 3,971 | 2,283 | 789.14 | 789.14 | 19.87% | 34.57% | Pre-Pandemic Baseline |
| **2021** | *Waived* | *NaN* | *NaN* | 714.40 | 714.40 | *NaN* | *NaN* | COVID-19 HUD Waiver |
| **2022** | 2022-02-24 | 4,106 | 2,494 | 1,444.31 | 1,174.31 | 35.18% | 57.91% | Peak Crisis Convergence |
| **2023** | 2023-01-26 | 5,171 | 3,285 | 1,938.74 | 1,298.74 | 37.49% | 59.02% | Peak Crisis Convergence |
| **2024** | 2024-01-25 | 6,110 | 3,365 | 1,018.14 | 981.14 | 16.66% | 30.26% | Post-Ordinance Dispersion |
| **2025** | 2025-01-30 | 5,714 | 2,897 | 851.02 | 767.02 | 14.89% | 29.38% | Post-Ordinance Dispersion |

---

## 3. Ratio Formulation & Distributional Metrics

For each valid PIT count year $t \in \{2017, \dots, 2025\} \setminus \{2021\}$, the scaling ratio $R_t$ is defined as:
$$R_t = \frac{\text{Downtown Count}_t}{\text{County Unsheltered Count}_t} \times 100\%$$

To evaluate the sensitivity of this ratio to footprint expansions and methodology changes, four distinct operational definitions were evaluated alongside the municipal City share.

### Table 2: Comparative Distributional Metrics Across Ratio Definitions ($N=8$)
| Ratio Definition | Mean (%) | Std (%) | Median (%) | IQR (%) | Min (%) | Max (%) | CV (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Reported Adjusted / County Unsheltered** | **21.99%** | 9.07% | 18.27% | 7.83% | 14.89% | 37.49% | 41.23% |
| **Core 6 Constant / County Unsheltered** | **19.31%** | 5.25% | 18.04% | 5.47% | 13.42% | 28.60% | **27.17%** |
| **Reported Constant / County Unsheltered** | 21.94% | 9.11% | 18.27% | 7.88% | 14.89% | 37.49% | 41.52% |
| **Raw Published / County Unsheltered** | 21.98% | 9.08% | 18.27% | 7.84% | 14.75% | 37.48% | 41.31% |
| **Reported Adjusted / City SD Unsheltered** | **37.39%** | 13.35% | 32.38% | 11.55% | 26.21% | 59.02% | 35.70% |

### Key Distributional Insights:
* **Footprint Stability Dividend:** When holding geographic boundaries strictly constant across time using the 261-block Core 6 panel (**Core 6 Constant**), the maximum crisis concentration in 2023 is $25.12\%$ (vs. $37.49\%$ reported), and the Coefficient of Variation drops from $41.23\%$ to $27.17\%$.
* **Downtown Concentration in City of San Diego:** Over the entire 9-year study window, Downtown accounts for over one-third of all unsheltered individuals in California's second largest city (mean $37.39\%$), reaching nearly $60\%$ during the 2022–2023 crisis.

---

## 4. Correlation & Regression Modeling

Parametric Pearson correlation ($r$), non-parametric Spearman rank correlation ($\rho$), and Kendall rank correlation ($\tau$) were computed across both the full longitudinal sample and structural sub-regimes.

### Table 3: Parametric & Non-Parametric Association Metrics
| Analytical Sample / Series | N | Pearson $r$ | Pearson $p$ | 95% CI (Fisher $z$) | Spearman $\rho$ | Spearman $p$ | 95% Bootstrap CI | OLS Slope | OLS $R^2$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Full Sample (2017–2025) [Reported Adj]** | 8 | **-0.0609** | 0.8861 | [-0.734, 0.673] | +0.2143 | 0.6103 | [-0.684, 0.919] | -0.0317 | 0.0037 |
| **Pre-Ordinance Era (2017–2023) [Reported Adj]** | 6 | **+0.1142** | 0.8294 | [-0.769, 0.847] | +0.3143 | 0.5441 | [-0.935, 1.000] | +0.0826 | 0.0130 |
| **Pre-Pandemic Baseline (2017–2020) [Reported Adj]** | 4 | **+0.4464** | 0.5536 | [-0.901, 0.985] | +0.4000 | 0.6000 | [-0.778, 1.000] | +0.0345 | 0.1993 |
| **Full Sample (2017–2025) [Core 6 Const]** | 8 | **-0.0957** | 0.8216 | [-0.750, 0.653] | 0.0000 | 1.0000 | [-0.797, 0.836] | -0.0238 | 0.0092 |
| **Pre-Ordinance Era (2017–2023) [Core 6 Const]** | 6 | +0.0395 | 0.9408 | [-0.798, 0.825] | +0.3143 | 0.5441 | [-0.935, 1.000] | +0.0130 | 0.0016 |
| **Full Sample (2017–2025) [Downtown vs City SD]** | 8 | **+0.2416** | 0.5642 | [-0.558, 0.809] | +0.4286 | 0.2894 | [-0.579, 0.951] | +0.2441 | 0.0584 |

### Mathematical Diagnosis of Correlation Behavior:
1. **The 2024–2025 Suppression Effect:**
   * Prior to 2024, downtown and county counts shared positive co-movement (pre-pandemic $r = +0.45$).
   * In 2024, County unsheltered hit an all-time record of 6,110 while Downtown fell to 1,018. In 2025, County unsheltered remained elevated at 5,714 while Downtown decreased further to 851.
   * This counter-directional shock acts as high-leverage divergence points in OLS space, pulling the full-sample slope negative ($\beta = -0.0317$).
2. **Municipal vs. Regional Association:**
   * Downtown counts correlate more strongly with City of San Diego unsheltered counts ($\rho = +0.43$) than with County-wide counts ($\rho = +0.21$). This aligns with urban geography: municipal policy, law enforcement, and shelter investments operate primarily at the City boundary.

---

## 5. Statistical Stability & Hypothesis Testing

A critical question for Task 8.3 is whether the ratio $R_t$ can be treated as a stationary or constant parameter over time:
$$H_0: R_{2017} = R_{2018} = \dots = R_{2025} = \bar{R}$$

### Table 4: Formal Hypothesis Testing Suite
| Hypothesis Test | Test Stat | Stat Symbol | Degrees of Freedom | $p$-value | Effect Size Metric | Effect Value | Statistical Conclusion |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **One-Way ANOVA (3 Regimes)** | **66.5057** | $F$ | $df_1=2, df_2=5$ | **0.0002** | $\eta^2$ | **0.9638** | **Reject $H_0$ (p < 0.001)**; profound regime divergence |
| **Kruskal-Wallis Non-Parametric** | 4.5000 | $H$ | $df=2$ | 0.1054 | — | — | Marginal under small sample ($n_i \le 4$) |
| **Linear Trend OLS on Year** | 0.6651 | $t$ | $df=6$ | 0.5307 | $R^2$ | 0.0687 | Fail to reject; trajectory is non-linear surge/drop |
| **Chow Structural Break Test (2024)** | 0.1462 | $F$ | $df_1=2, df_2=4$ | 0.8684 | RSS ratio | — | High within-regime variance in small post-sample |

### Detailed ANOVA Regime Breakdown:
* **Pre-Pandemic Baseline (2017–2020, $n=4$):** Mean $= 17.93\%$, Std $= 2.27\%$ ($95\%\text{ CI: }[14.32\%, 21.54\%]$)
* **Peak Crisis Convergence (2022–2023, $n=2$):** Mean $= 36.34\%$, Std $= 1.63\%$ ($95\%\text{ CI: }[21.68\%, 51.00\%]$)
* **Post-Ordinance Dispersion (2024–2025, $n=2$):** Mean $= 15.78\%$, Std $= 1.25\%$ ($95\%\text{ CI: }[4.53\%, 27.03\%]$)

The between-group sum of squares ($SS_{\text{between}} = 555.70$) dwarfs within-group residual variation ($SS_{\text{within}} = 20.89$), yielding an eta-squared of **$\eta^2 = 0.9638$**. This formally proves that **$96.4\%$ of observed ratio variation is driven by macroscopic structural shifts**, directly invalidating any unadjusted static ratio estimation model.

---

## 6. Small-Sample Statistical Power & Sensitivity Analysis

A primary technical requirement of Task 8.2 is documenting the severe mathematical limits imposed by an $N=8$ annual sample size.

### Table 5: Statistical Power ($1 - \beta$) as a Function of True Population Correlation ($|r|$)
| Correlation Magnitude ($|r|$) | Power ($N=6$) | Power ($N=8$) [Study Sample] | Power ($N=12$) | Power ($N=20$) | Type II Error Risk ($\beta$ at $N=8$) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $0.10$ | 0.0535 | **0.0558** | 0.0604 | 0.0698 | 94.42% |
| $0.20$ | 0.0642 | **0.0739** | 0.0933 | 0.1331 | 92.61% |
| $0.30$ | 0.0835 | **0.1064** | 0.1531 | 0.2477 | 89.36% |
| $0.40$ | 0.1136 | **0.1574** | 0.2460 | 0.4157 | 84.26% |
| $0.50$ | 0.1584 | **0.2329** | 0.3777 | 0.6198 | **76.71%** |
| $0.60$ | 0.2246 | **0.3411** | 0.5476 | 0.8154 | 65.89% |
| $0.70$ | 0.3238 | **0.4918** | 0.7395 | 0.9470 | 50.82% |
| $0.80$ | 0.4773 | **0.6903** | 0.9092 | 0.9949 | 30.97% |
| **0.85 (MDES)** | 0.5840 | **0.8000** | 0.9632 | 0.9993 | **20.00%** |
| $0.90$ | 0.7224 | **0.9086** | 0.9930 | 1.0000 | 9.14% |
| $0.95$ | 0.8874 | **0.9837** | 0.9998 | 1.0000 | 1.63% |

### Critical Analytical Boundaries:
1. **Severe Under-Powering for Plausible Effect Sizes:**
   * In social science and urban analytics, correlations between sub-regional and regional populations typically range from $r = 0.40$ to $r = 0.60$. At $N=8$, detecting a true correlation of $r = 0.50$ has a statistical power of only **$23.3\%$**, translating to a **$76.7\%$ probability of committing a Type II error** (failing to detect a real relationship).
2. **Minimum Detectable Effect Size (MDES):**
   * To achieve standard statistical power ($1 - \beta = 0.80$) at $\alpha = 0.05$ with $N=8$ observations, the true underlying correlation must be:
     $$|r| \ge 0.850$$
   * For $90\%$ power ($1 - \beta = 0.90$), $|r| \ge 0.896$.
3. **Required Sample Size for Moderate Association:**
   * To detect an association of magnitude $r = 0.50$ at standard $80\%$ power, a sample size of **$N = 30$ annual censuses** is required—representing three decades of annual PIT data that do not currently exist.

---

## 7. Policy Interpretation: The Anatomy of Spatial Decoupling

The quantitative findings reflect two historic real-world policy dynamics in San Diego County:

```text
[2017–2020 Baseline]         [2022–2023 Crisis]          [2024–2025 Post-Ordinance]
Downtown: 789–897           Downtown: 1,444–1,939        Downtown: 851–1,018
County: 3,971–5,621         County: 4,106–5,171          County: 5,714–6,110
Share: ~16%–20%             Share: ~35%–37%              Share: ~15%–17%
--------------------        --------------------         --------------------------
Geographic stability        Extreme concentration        Spatial displacement into
in downtown core.           driven by East Village.      riverbeds & outer cities.
```

1. **The Crisis Concentration Surge (2022–2023):**
   * During the pandemic recovery and inflation spike, homelessness concentrated intensely in the downtown urban core (specifically East Village blocks around Imperial Ave and 16th/17th Streets, as documented in Task 5.2's Getis-Ord Gi* analysis). Downtown absorbed **$37.5\%$ of the entire county's unsheltered population** and **$59.0\%$ of the City of San Diego's unsheltered population**.
2. **The Camping Ordinance Displacement Break (2024–2025):**
   * In July 2023, the City of San Diego passed the Unsafe Camping Ordinance, aggressively prohibiting encampments in public spaces near schools, transit hubs, and sidewalks if shelter beds are available.
   * **The Empirical Paradox:** Downtown monthly counts fell sharply from 1,939 to 1,018 in 2024 and 851 in 2025. However, RTFH's county-wide PIT count reached an **all-time record high of 6,110 in 2024**.
   * **Substantive Conclusion:** Individuals were not primarily transitioned into permanent housing; rather, enforcement physically displaced the unhoused population out of Downtown into freeway corridors (Caltrans property), the San Diego Riverbed, Balboa Park, and adjacent municipalities (National City, Chula Vista, El Cajon, Escondido).
   * As a result, the historical downtown-to-county ratio collapsed back to **$14.89\%$**, breaking simple longitudinal linear predictability.

---

## 8. Technical Guidance for Task 8.3 Estimation Modeling

Based on the empirical findings of Task 8.2, Task 8.3 cannot deploy a naive global OLS regression or fixed scalar ratio. The following modeling protocols are established:

1. **Regime-Conditioned Ratio Estimation:**
   * Models must incorporate regime dummy variables or state-space formulations:
     $$\widehat{\text{County}}_t = \frac{\text{Downtown}_t}{\bar{R}_{\text{regime}}}$$
     where $\bar{R}_{\text{baseline}} \approx 17.9\%$, $\bar{R}_{\text{peak}} \approx 36.3\%$, and $\bar{R}_{\text{post}} \approx 15.8\%$.
2. **Preference for Core 6 Constant-Methodology Series:**
   * Modelers should test [`data/BlockPanel_Balanced_261.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/BlockPanel_Balanced_261.csv) inputs, where ratio volatility is $34\%$ lower than published unadjusted totals.
3. **Leave-One-Out Cross-Validation (LOOCV):**
   * Given $N=8$, $k$-fold cross-validation is inappropriate. Task 8.3 must validate models via LOOCV ($8$ folds of $7$ train / $1$ test) and compute cumulative Mean Absolute Percentage Error (MAPE).
4. **Honest Uncertainty Quantification:**
   * Prediction intervals must account for small-sample Student's $t$ degrees of freedom ($t_{6, 0.975} = 2.447$, substantially wider than standard normal $z = 1.96$) to avoid misleading decision-makers regarding model precision.

---

## 9. Output Deliverables & Inventory

All statistical scripts, output tables, and publication-quality figures have been generated and archived:

### Deliverable Files:
1. **Analysis Script:** [`build_correlation_analysis.py`](file:///D:/Projects/Downtown-Homeless-Analysis/build_correlation_analysis.py) (fully reproducible).
2. **Canonical Metric CSVs:**
   * [`data/Downtown_County_CorrelationMetrics.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Downtown_County_CorrelationMetrics.csv) (Pearson, Spearman, Kendall, OLS slopes, CIs across all samples).
   * [`data/Downtown_County_RatioStability.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Downtown_County_RatioStability.csv) (ANOVA, Kruskal-Wallis, linear trend, and Chow test statistics).
   * [`data/Downtown_County_PowerAnalysis.csv`](file:///D:/Projects/Downtown-Homeless-Analysis/data/Downtown_County_PowerAnalysis.csv) (Power curves and Type II error rates for $N=6, 8, 12, 20$).
3. **Publication Figures (`figures/task8_2/`):**
   * `county_vs_downtown_scatter.png`: Scatter plot with OLS regression fit lines, 95% confidence intervals, sequential year labels, and regime coloring.
   * `ratio_stability_regimes.png`: Longitudinal ratio series displaying three policy regimes, ANOVA callouts, and policy annotations.
   * `statistical_power_curve.png`: Small-sample power curves illustrating MDES ($|r| \ge 0.85$) at $N=8$.
   * `downtown_vs_city_vs_county_shares.png`: Multi-panel comparison of Downtown concentration within County vs. City boundaries.
4. **Google Drive Cloud Location:**
   * `Shared with me > Downtown Homelessness > Deliverables > Assignment 8 - County-Level Estimation Model` (`1D8ffMhicVMGPcGRKxNtvlNnLGXXSSSws`).
