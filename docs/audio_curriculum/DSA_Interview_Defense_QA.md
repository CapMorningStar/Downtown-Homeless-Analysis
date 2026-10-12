# Data Science Alliance (DSA) Interview & Technical Defense Guide
## Tough Technical Questions, Empirical Boundaries & Methodological Justifications

**Purpose:** Comprehensive defense manual for Kyaw Soe Lwin for the DSA technical presentation to Adir Mancebo Jr. and prospective winter internship technical interviews.  
**Tone:** Empirically humble, methodologically rigorous, and completely transparent regarding data boundaries, non-significance, and model limitations.  

---

### Table of Questions

1. [Why conclude zero seasonality when civic intuition assumes weather cycles?](#q1-seasonality-debunking)
2. [Why was a Chow structural break test NOT run at July 2023 for the camping ordinance?](#q2-chow-structural-break)
3. [Why does the simple lag-1 baseline beat your complex machine learning ensemble in Assignment 10?](#q3-baseline-vs-ensemble)
4. [Your County model has R² = 0.504 and neither predictor is significant (p < 0.05). How can you recommend it?](#q4-county-estimation-fit)
5. [Did the July 2023 Unsafe Camping Ordinance CAUSE the downtown reduction and county displacement?](#q5-causal-claims-and-displacement)
6. [Why crown XGBoost as forecasting champion when 12-month CV MAPE is a statistical tie with Holt-Winters and SARIMA?](#q6-xgboost-champion-selection)
7. [Why did you choose 5-fold walk-forward cross-validation instead of standard randomized k-fold CV?](#q7-walk-forward-validation)
8. [How does the 2022 footprint expansion (+121 blocks) distort longitudinal comparisons?](#q8-footprint-expansion-distortion)
9. [Why are the 2026 forecast prediction intervals labeled 'approximate'?](#q9-prediction-interval-approximation)
10. [What is the issue with the shelter capacity data in Assignment 10?](#q10-shelter-capacity-placeholders)
11. [Why is Marina the only neighborhood with statistically significant Kruskal-Wallis seasonality?](#q11-marina-seasonality-exception)
12. [How exactly was the 120-meter hotspot centroid migration vector calculated?](#q12-centroid-migration-math)
13. [Why did Meta's Prophet perform so poorly across all forecasting horizons?](#q13-prophet-failure-analysis)
14. [How does the dual-layer anomaly detection surveillance engine in Tab 7 operate?](#q14-anomaly-detection-mechanics)
15. [What is the single most valuable technical investment the project can make next?](#q15-highest-value-investment)

---

### Detailed Questions & Rigorous Defense Answers

---

#### Q1: Seasonality Debunking
**Question:** *"Everyone in local government assumes homeless numbers drop in winter or surge in summer due to weather. How can your analysis claim that 8 of 9 series have zero seasonality?"*

**Technical Defense:**
* **Methodology:** We applied the Kruskal-Wallis non-parametric one-way ANOVA by calendar month across 108 months (Jan 2017–Dec 2025, df = 11), followed by classical STL decomposition.
* **Empirical Result:** For the headline overall series, Kruskal-Wallis yields $H = 2.66$ with $p = 0.995$ (and parametric ANOVA yields $p = 0.998$). East Village yields $H = 14.16, p = 0.224$, and City Center yields $H = 4.86, p = 0.938$.
* **Analytical Interpretation:** In time series decomposition, the seasonal component accounts for less than 5% of monthly variance. Downtown homeless counts are driven by multi-year structural shifts—pandemic emergency housing, shelter openings/closures, and enforcement operations—not ambient temperature.
* **Caveat:** The only borderline series is Marina ($H = 19.88, p = 0.047$), but parametric ANOVA is non-significant ($p = 0.162$). This is localized to convention center buffer sweeps and summer tourist activations, not an organic seasonal migration.

---

#### Q2: Chow Structural Break
**Question:** *"Why did you not report a Chow structural break test at July 2023 when the Unsafe Camping Ordinance was enacted?"*

**Technical Defense:**
* **Scope & Design:** Task 4.3 explicitly tested three historical structural break candidates defined in the research plan: April 2017 (DSDP methodology change), May 2018 (second methodology change), and March 2020 (COVID-19 onset).
* **Honest Boundary:** July 2023 was not included in the Chow candidate test battery. While visually obvious in the longitudinal chart, formal Chow testing at July 2023 was outside the defined scope of Task 4.3.
* **Defense Statement:** *"We do not present invented F-statistics. Any prior draft mentioning 'July 2023 F = 28.64' was an unverified hallucination that has been fully excised. In our v3.0 technical report, we disclose transparently that July 2023 was not tested under Task 4.3."*

---

#### Q3: Baseline vs. Ensemble
**Question:** *"In Assignment 10, your lag-1 naive baseline achieved an MAE of 119.6, while your sophisticated multi-model ensemble had an MAE of 248.0. Why did your advanced ensemble perform worse than a naive baseline?"*

**Technical Defense:**
* **Empirical Reality:** The downtown monthly time series exhibits very high autoregressive persistence ($\text{AR}(1) > 0.85$). Under high persistence, a naive lag-1 predictor ($y_t = y_{t-1}$) is an extremely formidable benchmark.
* **Overparameterization & Shift:** The ensemble model (BSTS weight 0.812, MLP weight 0.188, LightGBM weight 0) struggled during rapid structural transition windows (post-July 2023 enforcement). Complex neural networks and gradient boosting regressors trained on historical levels overfit to higher pre-ordinance regimes.
* **Ablation Insight:** In our ablation study, expanding features from 12 to 68 actually degraded out-of-fold performance by 1.6%.
* **Executive Humility:** *"As data scientists, our job is empirical truth, not model vanity. We report this transparently: in stable months, simple persistence beats complex non-linear regressors unless large external administrative datasets are integrated."*

---

#### Q4: County Estimation Fit
**Question:** *"Your Policy Regime OLS model for county unsheltered estimation has an R² of only 0.504, and neither the downtown slope (p = 0.78) nor the regime term (p = 0.075) is significant at α = 0.05. How can you recommend this model to city leaders?"*

**Technical Defense:**
* **Sample Size & Power Constraints:** The RTFH Point-in-Time census is conducted only once per year in late January. Over 2017–2025, excluding the canceled 2021 count, we have exactly $N = 8$ paired historical observations. With $N = 8$, the statistical power to detect even a moderate effect ($r = 0.5$) is only ~23%.
* **Rejection of Constant Multiplier:** Before this model, agencies used constant multipliers (e.g. downtown is ~20% of county). We proved that constant ratio assumption is completely invalid: One-Way ANOVA across regimes gives $F = 66.51, p = 0.0002, \eta^2 = 0.964$. Naive ratio extrapolation creates up to 42.2% LOOCV MAPE and +39.3% signed bias!
* **Role as a Bridging Indicator:** Our Policy Regime OLS model ($Y = 4,513.26 + 0.1859 \cdot X + 1,225.04 \cdot D_{\text{post}}$) is a directional bridging tool between annual censuses, not an official HUD submission tool.
* **The 4 Public Communication Rules:** Because of this statistical uncertainty, we prohibit single-point quotes like '5,921'. We mandate reporting the calibrated Student's t ($df = 5$) interval: **5,900 [3,900 to 8,000]** (a margin of ±2,050 individuals, ±35%).

---

#### Q5: Causal Claims and Displacement
**Question:** *"Does your report prove that the City's July 2023 Unsafe Camping Ordinance caused homeless people to leave downtown and spread into the county?"*

**Technical Defense:**
* **Correlation vs. Causation:** We do **not** claim causal proof. Our longitudinal data establish macro divergence: downtown unsheltered counts dropped by 56% between Jan 2023 and Jan 2025, while countywide unsheltered counts reached 6,110 (2024) and 5,714 (2025).
* **Absence of Microdata:** Because DSDP field counts are anonymous headcount aggregates by block, we possess no biometric, HMIS, or individual tracking data. We cannot observe whether individual persons moved from 16th Street into the San Diego Riverbed, entered shelters, or exited homelessness.
* **Recommendation R5:** We explicitly recommend that the City and County launch coordinated cross-jurisdictional outreach tracking to empirically test the displacement hypothesis directly.

---

#### Q6: XGBoost Champion Selection
**Question:** *"Looking at your 12-month cross-validation MAPE, XGBoost (38.3%), Holt-Winters (38.4%), and SARIMA (39.6%) are practically identical. Why did you name XGBoost the champion?"*

**Technical Defense:**
* **Statistical Tie Acknowledged:** In Table 8.1, fold-to-fold standard deviations range between 26.0% and 35.5%. Statistically, XGBoost, Holt-Winters, and SARIMA are in a tie at the 12-month horizon.
* **Selection Criteria:** XGBoost was retained because it had the lowest numerical mean (38.3%) across all five walk-forward folds, and achieved superior performance on the 2025 hold-out year (8.5% MAPE vs 20.4% for HW and 22.8% for SARIMA).
* **Dual Architecture Approach:** Non-linear decision trees capture rapid velocity shifts without exploding linearly. However, because recursive XGBoost cannot generate analytical prediction intervals, we use Holt-Winters as our parametric anchor to derive closed-form prediction intervals.

---

#### Q7: Walk-Forward Validation
**Question:** *"Why did you use 5-fold walk-forward cross-validation instead of standard 5-fold cross-validation or randomized train-test splits?"*

**Technical Defense:**
* **Temporal Ordering & Zero Leakage:** In time series econometrics, observations are serially correlated. Standard randomized cross-validation uses future data to predict the past, causing severe lookahead bias and artificially deflating error metrics.
* **Simulation of Real Deployment:** Our 5-fold walk-forward design trains sequentially on expanding windows (Fold 1: 2017–2020 predicting 2021; through Fold 5: 2017–2024 predicting 2025). This exactly mirrors how municipal analysts must deploy models in production.

---

#### Q8: Footprint Expansion Distortion
**Question:** *"Why was the 2022 DSDP footprint expansion so significant, and how did your pipeline address it?"*

**Technical Defense:**
* **The Expansion Wedge:** In January 2022, DSDP expanded survey coverage from 261 blocks to 382 blocks by adding 121 peripheral blocks across Golden Hill (52), Barrio Logan (35), and Sherman Heights (34).
* **Headcount Impact:** On the five digitized dates following the expansion, these added blocks contributed between 3.7% and 32.8% of reported headline totals. In January 2023, 640.6 of 1,955.1 individuals were in the expansion area.
* **Engineering Solution:** We constructed `BlockPanel_Balanced_261.csv`, isolating the 261 core blocks across all 12 digitized dates. On this constant spatial panel, counts still surged +71% in 2022, proving that while crisis growth was genuine, unadjusted public reports exaggerated the surge by nearly one-third.

---

#### Q9: Prediction Interval Approximation
**Question:** *"Why are the 2026 forecast prediction intervals described as 'approximate' in the technical report?"*

**Technical Defense:**
* **Recursive Error Propagation:** The champion forecast is generated recursively using an XGBoost regressor (predicting $t+1$, feeding that into $t+2$, up to $t+12$). Recursive machine learning models do not have closed-form parametric predictive distributions.
* **Analytical Derivation:** To provide decision-makers with necessary uncertainty bounds, we extracted the residual variance $\sigma^2$ from the parametric Holt-Winters model, scaled by a horizon-expansion factor $\sqrt{1 + 0.08(h - 1)}$.
* **Honest Disclosure:** Rather than presenting these bands as exact parametric bounds, we explicitly label them as approximate calibrated envelopes.

---

#### Q10: Shelter Capacity Placeholders
**Question:** *"In Assignment 10, what was discovered regarding the shelter capacity features, and what are the implications?"*

**Technical Defense:**
* **Audit Finding:** The multi-source feature matrix incorporated constructed shelter-capacity time series as placeholders rather than live administrative bed-census records.
* **Policy Implication:** In our ablation study, shelter features showed minimal marginal gain. We explicitly warn in Recommendation R7 that no civic leader should draw capacity-exhaustion conclusions from the Assignment 10 model until these placeholders are replaced with official HUD Housing Inventory Count (HIC) data.

---

#### Q11: Marina Seasonality Exception
**Question:** *"Why did Marina exhibit a Kruskal-Wallis p-value of 0.047 when every other neighborhood was non-significant?"*

**Technical Defense:**
* **Local Environmental Context:** Marina borders the San Diego Convention Center and Embarcadero marina parks. Unlike residential or industrial East Village, Marina experiences massive summer tourist activations (e.g., Comic-Con in July) and concentrated city park buffer sweeps.
* **Statistical Disagreement:** While non-parametric Kruskal-Wallis was borderline significant ($H = 19.88, p = 0.047$), parametric ANOVA yielded $p = 0.162$ (non-significant). Individual month tests showed elevated counts in August and November, reflecting episodic local events rather than a broader meteorological cycle.

---

#### Q12: Centroid Migration Math
**Question:** *"How did you compute the 120-meter centroid migration vector, and why did previous reports cite 121 meters?"*

**Technical Defense:**
* **Coordinate Mathematics:** Using `Hotspot_Classifications.geojson` and `Downtown_BlockGrid.geojson`, we computed representative points for all statistically significant Getis-Ord Gi* hotspot blocks ($p < 0.05$) in UTM Zone 11N.
* **Weighted Migration:** Weighting each representative point by its `adjusted_count`:
  * Early Period (2018–2020, $n = 10$ block-dates) vs Recent Period (2022–2025, $n = 20$ block-dates).
  * Shift: The count-weighted centroid moved **about 120 m on a bearing of 160° (south-south-east)**. The unweighted centroid moved about 62 m.
* **Correction Note:** Earlier drafts cited 121 m and hallucinated fake transit distances (e.g. '52m from station'). We report the verified technical report figures: **about 120 m on a bearing of 160°**, emphasizing that this reflects cluster locations, not individual tracking.

---

#### Q13: Prophet Failure Analysis
**Question:** *"Why did Meta's Prophet model fail so drastically, achieving an error of 64.2% at the 12-month horizon?"*

**Technical Defense:**
* **Bayesian Changepoints:** Prophet fits a piecewise linear or logistic growth curve with Bayesian priors on changepoints.
* **Failure Mechanism:** The historical downtown surge was rapid and steep from 2021 to mid-2023. Prophet's automated changepoint selection placed trends during this steep ascent. When the July 2023 camping ordinance caused an immediate structural inflection, Prophet had no forward mechanism to anticipate the downturn, projecting linear continuation of the peak into 2024 and 2025.
* **Lesson:** Fixed Bayesian trend models should never be used for forecasting under sharp regulatory or policy inflection regimes.

---

#### Q14: Anomaly Detection Mechanics
**Question:** *"How does the Tab 7 / Assignment 10 anomaly surveillance engine work in practice?"*

**Technical Defense:**
* **Dual-Layer Statistical Process Control:**
  1. **Shewhart Control Charts:** Measures short-term volatility against rolling mean $\pm 2\sigma$ (Warning Limit) and $\pm 3\sigma$ (Action Limit) to catch transient, single-month shocks.
  2. **Tabular CUSUM ($k = 0.5, h = 4.0$):** Accumulates consecutive small deviations from the target mean:
     $$S_t^+ = \max(0, S_{t-1}^+ + (z_t - k)), \quad S_t^- = \max(0, S_{t-1}^- - (z_t + k))$$
     Triggers an alarm when $S_t \ge 4.0$, detecting persistent regime shifts.
* **Historical Validation:** Successfully flagged all 4 macro regime inflections: April 2017 (Methodology), March 2020 (COVID Low), May 2023 (Crisis Peak), and July 2023 (Ordinance Contraction). Month-level precision is 68.8% with an F1 score of 0.55.

---

#### Q15: Highest-Value Investment
**Question:** *"If the Data Science Alliance and City of San Diego have budget for only one analytical initiative next year, where should it go?"*

**Technical Defense:**
* **Recommendation R8 (Block Map Digitization):**
  * Of roughly 90 historical monthly counts conducted by DSDP that possess usable block maps, **only 12 dates have ever been digitized** (all in January or February).
  * 85% of historical spatial data remains locked inside static scanned PDF maps.
  * Digitizing the remaining ~78 monthly block maps is vastly more valuable than fitting more machine learning algorithms. Full spatial digitization would allow:
    1. Direct testing of whether the 120-meter southward migration holds during summer months.
    2. Precise month-by-month spatial panel econometrics around the July 2023 ordinance.
    3. Block-level causal evaluation of Safe Sleeping sites and shelter openings.
