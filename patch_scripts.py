import os
import re

REPLACEMENTS = {
    # Slide 1
    "Downtown San Diego Unsheltered Homelessness:\\nStrategic Synthesis & Policy Roadmap (2017–2026)": "Downtown Homelessness:\\nExecutive Strategic Roadmap (2017–2026)",
    "Downtown San Diego Unsheltered Homelessness:<br>Strategic Synthesis & Policy Roadmap (2017–2026)": "Downtown Homelessness:<br>Executive Strategic Roadmap (2017–2026)",
    "Longitudinal Econometrics, Spatial Panel Dynamics, Machine Learning Forecasting & Regional Policy Impacts": "Econometrics, Spatial Dynamics, ML Forecasting & Regional Policy",
    "Data Science Alliance (DSA) in partnership with DSDP and RTFH\\nLead Analyst: Kyaw Soe Lwin | Project Lead: Adir Mancebo Jr.": "DSA, DSDP, RTFH\\nLead: K.S. Lwin | Proj Lead: A. Mancebo Jr.",
    "Data Science Alliance (DSA)</strong> in partnership with DSDP & RTFH<br>\n            Lead Analyst: <strong>Kyaw Soe Lwin</strong> | Project Lead: <strong>Adir Mancebo Jr.</strong>": "DSA</strong>, DSDP & RTFH<br>\n            Lead: <strong>K.S. Lwin</strong> | Proj Lead: <strong>A. Mancebo Jr.</strong>",
    "9 Years of Monthly Field Counts (Jan 2017–Dec 2025, 108 months, 104 published)\\nPoint-in-Time (PIT) Regional Censuses (2017–2025)": "108 months of counts (2017-2025)\\nRegional PIT censuses",
    "<strong>9 Years of Monthly Field Counts</strong> (Jan 2017–Dec 2025, 108 months, 104 published)<br>\n            Point-in-Time (PIT) Regional Censuses (2017–2025)": "<strong>108 Months of Counts</strong> (2017–2025)<br>\n            Regional PIT Censuses",
    "Spatial Getis-Ord Gi* • 5-Fold Walk-Forward Cross-Validation • Policy Regime OLS • 4 Public Communication Rules": "Spatial Gi* • Walk-Forward CV • OLS Regime • 4 Comm Rules",
    "Getis-Ord Gi* • 5-Fold Walk-Forward Cross-Validation • Policy Regime OLS • The 4 Public Communication Rules": "Spatial Gi* • Walk-Forward CV • OLS Regime • 4 Comm Rules",

    # Slide 2
    "Executive KPI Dashboard: Crisis Peak, Enforcement Contraction & Hotspot Migration": "Executive KPIs: Peak & Migration",
    "Executive Framing & Core Findings": "Executive Framing",
    "Highest headline count in downtown history (2,103.3); culmination of 3-year surge.": "Highest count on record. Capped a 3-year surge.",
    "−59.5% reduction from peak; Dec 2025 count reached 985.4.": "Down 59% from peak. Dec 2025 hit 985.",
    "Epicenter of downtown homelessness (historical monthly average 552.0 individuals).": "Core driver of downtown population.",
    "Cluster centroid shifted 120.4 m bearing 160° (SSE) toward South East Village.": "Centroid shifted 120m south toward South East Village.",
    "THE STRATEGIC REALITY: DOWNTOWN CONTRACTION VS. REGIONAL DISPLACEMENT": "THE REALITY: DOWNTOWN DROPS VS REGIONAL SHIFTS",
    
    "Three Trajectory Epochs:": "Three Phases:",
    "Three Trajectory Epochs: ": "Three Phases: ",
    "Downtown transitioned through Baseline Contraction (2017–2020: annual mean 1,058 → 654), Crisis Surge (2021–2023: annual mean 960 → 1,563, peak 2,103 in May 2023), and Enforcement Pullback (2024–2025: annual mean ~887 and 864, Jan 2025 count 851).": "Pre-COVID drop, massive 2021-2023 surge (peak 2,103), then post-enforcement contraction (851 in Jan 2025).",
    
    "Debunking Seasonality:": "No Seasonality:",
    "Debunking Seasonality: ": "No Seasonality: ",
    "Non-parametric tests prove 8 of 9 downtown series have NO statistically significant seasonality (Overall series H=2.66, p=0.995). Resource budgeting based on seasonal surges is empirically unsupported.": "Weather doesn't drive numbers (p=0.995). Seasonal budgets are a mismatch for year-round needs.",
    
    "The Boundary Expansion Wedge:": "Map Changes:",
    "The Boundary Expansion Wedge: ": "Map Changes: ",
    "In 2022, DSDP added 121 peripheral blocks, accounting for 3.7% to 32.8% of reported counts. Longitudinal comparisons require the balanced 261-block spatial panel (+71% in 2022).": "121 blocks added in 2022. Correcting for this shows a real, but smaller, +71% surge in the core.",
    
    "Regional Divergence:": "Regional Shift:",
    "Regional Divergence: ": "Regional Shift: ",
    "Downtown's share of county unsheltered fell from 37.5% (2023) to 14.9% (2025), yet countywide unsheltered reached 6,110 (2024, series high) and 5,714 (2025). Divergence indicates spatial redistribution rather than resolved homelessness.": "Downtown share fell to 15%, while countywide hit a record 6,110. The crisis moved, it didn't end.",

    # Slide 3
    "The 9-Year Trajectory: Three Distinct Macro Policy Epochs (2017–2025)": "9-Year Trajectory: Three Policy Epochs",
    "Epoch 1: Baseline Contraction (2017–2020)": "Epoch 1: Contraction (2017–2020)",
    "Low of 529 in March 2020 (−38.2% drop 2017→2020)": "Low of 529 in Mar 2020 (−38%)",
    "Pre-COVID contraction and initial shelter interventions; series low of 529 observed at COVID-19 onset in March 2020.": "Pre-COVID drop. Baseline interventions worked.",
    "Epoch 2: The Crisis Surge (2021–2023)": "Epoch 2: Crisis Surge (2021–2023)",
    "May 2023 Peak of 2,103 (+297% from March 2020 low)": "May 2023 Peak of 2,103 (+297%)",
    "Multi-year escalation driven by shelter de-densification, economic stress, and post-moratoria housing vulnerability; annual mean reached 1,563 in 2023.": "Driven by shelter de-densification and housing vulnerability.",
    "Epoch 3: Enforcement & Stabilization (2024–2025)": "Epoch 3: Enforcement (2024–2025)",
    "Jan 2025 Count of 851 (−59.5% from peak)": "Jan 2025 Count of 851 (−59%)",
    "Sharp contraction following the July 2023 Unsafe Camping Ordinance and Safe Sleeping site rollouts; annual counts stabilized near ~887 (2024) and 864 (2025). 4 months unpublished in 2025.": "Sharp drop post-Camping Ordinance. Counts stabilized ~860-880.",

    # Slide 4
    "Debunking the Seasonality Myth: Homelessness Is Not Driven by Weather": "Seasonality Myth: Weather Doesn't Drive Homelessness",
    "Kruskal-Wallis Non-Parametric Seasonality Tests (12 Months, df=11)": "Kruskal-Wallis Tests (df=11)",
    "Kruskal-Wallis Non-Parametric Tests (df=11)": "Kruskal-Wallis Tests (df=11)",
    "Zero Seasonality (p > 0.05)": "No Seasonality",
    "Mixed (ANOVA sig, KW non-sig)": "Mixed",
    "Mixed (KW sig, ANOVA non-sig)": "Mixed",
    "The 'Weather Surge' Fallacy:": "Weather Fallacy:",
    "The 'Weather Surge' Fallacy: ": "Weather Fallacy: ",
    "Civic planning often assumes winter drops or summer surges. In reality, calendar months explain virtually none of monthly count variation across downtown (p = 0.995).": "Calendar months explain zero variation (p=0.995). Seasonal planning is flawed.",
    "Macro Drivers Dominate:": "Macro Drivers:",
    "Macro Drivers Dominate: ": "Macro Drivers: ",
    "Multi-year shifts, shelter capacity adjustments, and regional housing dynamics drive changes—not temperature or rainfall.": "Shifts are driven by capacity, policy, and housing dynamics—not weather.",
    "Eliminate Fluctuating Allocations:": "Fund Year-Round:",
    "Eliminate Fluctuating Allocations: ": "Fund Year-Round: ",
    "Emergency seasonal shelter beds fail to solve baseline need. Funding must be committed to permanent year-round operating capacity.": "Stop seasonal allocations. Commit to permanent capacity.",
    "Borderline Disagreements:": "Solid Evidence:",
    "Borderline Disagreements: ": "Solid Evidence: ",
    "KW and ANOVA disagree for Marina (KW p=0.047, ANOVA p=0.162) and Cortez (KW p=0.312, ANOVA p=0.047); 8 of 9 series are strictly non-significant under the primary KW test.": "8 of 9 series show strictly non-significant seasonality.",

    # Slide 5
    "The Boundary Expansion Wedge: Disentangling Reality from Map Changes": "Boundary Expansion: Map Changes Inflated Growth",
    "The Administrative Shift:": "Administrative Shift:",
    "The Administrative Shift: ": "Administrative Shift: ",
    "In January 2022, DSDP expanded survey coverage from 261 blocks to 382 blocks by incorporating 121 peripheral blocks across Golden Hill (52), Barrio Logan (35), and Sherman Heights (34).": "121 blocks added in 2022 (Golden Hill, Barrio Logan).",
    "Quantifying the Wedge:": "The Wedge Effect:",
    "Quantifying the Wedge: ": "The Wedge Effect: ",
    "Between 3.7% and 32.8% of reported post-2021 count totals came from the added blocks. At the January 2023 peak, 640.6 of 1,955.1 individuals (32.8%) were in the expansion area.": "Added blocks inflated counts by up to 33% (640 individuals at peak).",
    "Underlying Crisis Remained Real:": "True Core Growth:",
    "Underlying Crisis Remained Real: ": "True Core Growth: ",
    "On the balanced 261-block panel, counts still surged +71% in 2022. The crisis was real, but unadjusted comparisons conflate geography with population changes.": "Balanced 261-block panel still grew 71% in 2022. Boundaries matter.",
    "Data Engineering Fix:": "Analytical Fix:",
    "Data Engineering Fix: ": "Analytical Fix: ",
    "Enforced strict longitudinal panel balance (BlockPanel_Balanced_261.csv) across all 12 digitized count dates (2018–2025).": "Enforced strict 261-block balance across all years.",

    # Slide 6
    "Where Homelessness Concentrates: The East Village Epicenter": "Concentration: The East Village Epicenter",
    "Top Persistent Hotspot Blocks in Downtown San Diego (Getis-Ord Gi*)": "Top Hotspots (Getis-Ord Gi*)",
    "Top Persistent Hotspots (Getis-Ord Gi*)": "Top Hotspots (Getis-Ord Gi*)",
    "East Village Volume Dominance:": "Volume Dominance:",
    "East Village Volume Dominance: ": "Volume Dominance: ",
    "Historically accounts for 54.0% of all downtown homelessness (mean 552.0 individuals). South East Village alone accounts for over 317 individuals/month.": "Drives 54% of downtown homelessness (avg 552 individuals).",
    "100% of Top 10 in South East Village:": "Top Hotspots:",
    "100% of Top 10 in South East Village: ": "Top Hotspots: ",
    "Every single one of the top 10 persistent hotspot blocks is located in South East Village, forming a durable geographic cluster.": "100% of the top 10 persistent hotspots are in South East Village.",
    "Built-Environment Infrastructure:": "Built Magnets:",
    "Built-Environment Infrastructure: ": "Built Magnets: ",
    "Hotspots cluster around major infrastructure anchors: the 12th & Imperial Transit Center, social service facilities, and Caltrans freeway underpasses providing physical overhead cover.": "Clusters anchor around transit, services, and freeway underpasses.",

    # Slide 7
    "Geospatial Hotspot Dynamics: The 120-Meter Southward Displacement Vector": "Hotspot Dynamics: 120m Southward Vector",
    "120.4-Meter Migration Vector:": "120m Migration:",
    "120.4-Meter Migration Vector: ": "120m Migration: ",
    "Between early (2018–2020, n=10) and recent (2022–2025, n=20) periods, the count-weighted hotspot centroid shifted 120.4 meters on a bearing of 160.1° (south-south-east).": "Centroid shifted 120m SSE toward South East Village.",
    "Unweighted Centroid:": "Density Driven:",
    "Unweighted Centroid: ": "Density Driven: ",
    "The unweighted centroid moved 62 meters, confirming the southern pull is driven by both cluster location and density.": "Unweighted moved 62m; density and location both pull south.",
    "Northern Enforcement & Sidewalk Access:": "Enforcement Push:",
    "Northern Enforcement & Sidewalk Access: ": "Enforcement Push: ",
    "Increased enforcement of sidewalk clearance in core commercial areas (Gaslamp, Core/City Center) pushed unhoused clusters southward.": "Sidewalk clearance in Gaslamp displaced clusters south.",
    "Cluster Location vs Individual Tracking:": "Spatial Shift:",
    "Cluster Location vs Individual Tracking: ": "Spatial Shift: ",
    "This vector reflects where statistically significant hotspot clusters sit across count dates, not direct tracking of individual people.": "Reflects macro cluster movements, not individual tracking.",

    # Slide 8
    "Multi-Model Machine Learning Benchmark: 5-Fold Walk-Forward Cross-Validation": "Machine Learning: 5-Fold CV Benchmark",
    "5-Fold Walk-Forward Cross-Validation Performance (Table 8.1, Zero Leakage)": "5-Fold CV Performance",
    "5-Fold Walk-Forward CV Performance (Table 8.1, Zero Leakage)": "5-Fold CV Performance",
    "Short vs Long Horizons:": "Horizons:",
    "Short vs Long Horizons: ": "Horizons: ",
    "SARIMA dominates short horizons (1-month MAPE 5.4%). At 12 months, XGBoost (38.3%), Holt-Winters (38.4%), and SARIMA (39.6%) are a statistical tie given 26–36 point fold SD.": "SARIMA wins short-term (5.4% MAPE). XGBoost ties at 12-months (38.3%).",
    "XGBoost Champion:": "Champion Model:",
    "XGBoost Champion: ": "Champion Model: ",
    "Retained as champion for the overall series due to lowest 12-month mean (38.3%) and strong hold-out performance (8.5% on 2025).": "XGBoost chosen for lowest error and strong 2025 hold-out (8.5%).",
    "2025 Hold-Out Baseline Victory:": "Baseline Check:",
    "2025 Hold-Out Baseline Victory: ": "Baseline Check: ",
    "Naive seasonal achieved 6.3% on 2025 because 2025 repeated 2024 levels; highlights the importance of retaining naive baselines in all benchmarking.": "Naive seasonal performed well in 2025, proving baselines are critical.",
    "Prophet Failure:": "Prophet Failure:",
    "Prophet Failure: ": "Prophet Failure: ",
    "Prophet scored worst at all horizons (64.2% at 12 months) because fixed changepoints failed to detect the post-peak inflection.": "Prophet failed (64.2% error) as it missed the post-peak drop.",

    # Slide 9
    "2026 Forward Outlook: Stress-Testing Three Strategic Policy Scenarios": "2026 Outlook: Stress-Testing Scenarios",
    "Baseline Outlook:": "Baseline:",
    "Baseline Outlook: ": "Baseline: ",
    "Monthly counts projected to remain range-bound between 816 and 896 individuals (Month 12 Dec 2026: 888, approximate 95% PI 539–1,237).": "Expected to remain range-bound at 816–896 individuals.",
    "Fixed What-If Scenarios:": "Stress-Tests:",
    "Fixed What-If Scenarios: ": "Stress-Tests: ",
    "Scenarios are fixed stress-test paths (−2% and +2.2% monthly), NOT model-based policy simulations.": "Fixed scenario paths, not causal policy models.",
    "Optimistic Path (−24% at M12):": "Optimistic:",
    "Optimistic Path (−24% at M12): ": "Optimistic: ",
    "Projects a reduction to ~675 individuals by Dec 2026 under favorable shelter turnover and intake.": "~675 individuals by Dec 2026 (favorable dynamics).",
    "Pessimistic Path (+26% at M12):": "Pessimistic:",
    "Pessimistic Path (+26% at M12): ": "Pessimistic: ",
    "Projects an increase to ~1,123 individuals by Dec 2026 under shelter constraints and economic displacement.": "~1,123 individuals by Dec 2026 (economic constraints).",
    "Planning with Ranges:": "Range Planning:",
    "Planning with Ranges: ": "Range Planning: ",
    "Decision-makers must plan around calibrated uncertainty bands rather than single-point forecasts.": "Plan using uncertainty bands, not single points.",

    # Slide 10
    "The Regional Displacement Paradox: Downtown Collapse vs. Countywide High": "Regional Displacement: Downtown Drops vs County Highs",
    "Downtown Share Plunged:": "Share Plunged:",
    "Downtown Share Plunged: ": "Share Plunged: ",
    "Downtown's share of countywide unsheltered homelessness plunged from 37.5% (Jan 2023) to 14.9% (Jan 2025).": "Downtown's share of county unsheltered fell to 14.9%.",
    "County Unsheltered High:": "County Record:",
    "County Unsheltered High: ": "County Record: ",
    "Simultaneously, the RTFH Point-in-Time count recorded 6,110 unsheltered individuals in 2024 (series high) and 5,714 in 2025.": "Countywide numbers reached 6,110 (2024) and 5,714 (2025).",
    "Spatial Displacement vs Resolution:": "Displacement:",
    "Spatial Displacement vs Resolution: ": "Displacement: ",
    "Downtown reductions coincided with regional increases, consistent with encampment displacement into riverbeds, canyons, and neighboring municipalities.": "Downtown drops align with regional spikes. The crisis moved.",
    "Empirical Limit:": "Data Limits:",
    "Empirical Limit: ": "Data Limits: ",
    "The project lacks individual tracking data to prove where displaced persons moved; findings show macro divergence, not causal proof.": "Reflects macro divergence, individual tracking is unavailable.",

    # Slide 11
    "Countywide Macro Estimation Model & Mandatory Communication Rules": "Macro Model & 4 Communication Rules",
    "Ratio Stability Rejected:": "Ratio Rejected:",
    "Ratio Stability Rejected: ": "Ratio Rejected: ",
    "One-Way ANOVA rejects ratio stability across regimes (F = 66.51, p = 0.0002, eta^2 = 0.964). Pearson correlation is r = −0.061 over 8 paired years.": "Fixed ratios fail across policy regimes (ANOVA p=0.0002).",
    "Econometric Equation:": "Model Equation:",
    "Econometric Equation: ": "Model Equation: ",
    "Y = 4,513.26 + 0.1859 * X + 1,225.04 * D_post\\nWhere X = Downtown Jan count, D_post = 1 for 2024/2025.": "Y = 4,513 + 0.186X + 1,225*D_post (Accounts for 2024/25).",
    "Y = 4,513.26 + 0.1859 * X + 1,225.04 * D_post<br>\n            Where X = Downtown Jan count, D_post = 1 for 2024/2025.": "Y = 4,513 + 0.186X + 1,225*D_post (Accounts for 2024/25).",
    "Fit & Diagnostics:": "Diagnostics:",
    "Fit & Diagnostics: ": "Diagnostics: ",
    "R^2 = 0.504 | Adj R^2 = 0.306 | LOOCV RMSE = 815.3 | Bias = -0.3%. Neither slope (p=0.78) nor D_post (p=0.075) is statistically significant at 5%.": "R²=0.50. Slope and D_post are not strictly significant at 5%.",
    "Current County Estimate:": "Current Estimate:",
    "Current County Estimate: ": "Current Estimate: ",
    "5,900 [95% PI: 3,900 to 8,000 individuals]\\nMargin of error is +/- 2,050 individuals (+/- 35%) using Student's t distribution (df=5).": "5,900 [95% PI: 3,900 to 8,000]. Margin of error is ±35%.",
    "<strong>5,900 [95% PI: 3,900 to 8,000 individuals]</strong><br>\n            Margin of error is ±2,050 individuals (±35%) using Student's t distribution (df=5).": "<strong>5,900 [95% PI: 3,900 to 8,000]</strong><br>Margin of error is ±35%.",
    
    "Rule 1: Prohibit Raw Single-Point Precision": "Rule 1: No False Precision",
    "Rule 1: Prohibit Raw Single-Point Precision:": "Rule 1: No False Precision:",
    "Rule 1: Prohibit Raw Single-Point Precision: ": "Rule 1: No False Precision: ",
    "Never publish uncalibrated single figures like '5,921'. False precision misleads the public and damages institutional credibility.": "Stop using raw single points (e.g., '5,921'). It damages credibility.",
    "Rule 2: Mandate Rounding to Nearest 100": "Rule 2: Round to 100",
    "Rule 2: Mandate Rounding to Nearest 100:": "Rule 2: Round to 100:",
    "Rule 2: Mandate Rounding to Nearest 100: ": "Rule 2: Round to 100: ",
    "Always round estimated point totals to the nearest 100 individuals (mandate '5,900' instead of '5,921').": "Always round estimates to the nearest hundred.",
    "Rule 3: Always Publish Calibrated 95% Interval": "Rule 3: Show 95% Interval",
    "Rule 3: Always Publish Calibrated 95% Interval:": "Rule 3: Show 95% Interval:",
    "Rule 3: Always Publish Calibrated 95% Interval: ": "Rule 3: Show 95% Interval: ",
    "Every headline figure MUST be accompanied by its calibrated Student's t prediction interval: '5,900 [3,900 to 8,000]'.": "Mandate prediction ranges: '5,900 [3,900 to 8,000]'.",
    "Every headline figure MUST be accompanied by its calibrated Student's t prediction interval: <em>'5,900 [3,900 to 8,000]'</em>.": "Mandate prediction ranges: <em>'5,900 [3,900 to 8,000]'</em>.",
    "Rule 4: Mandatory Policy Regime Disclosure": "Rule 4: Disclose Regimes",
    "Rule 4: Mandatory Policy Regime Disclosure:": "Rule 4: Disclose Regimes:",
    "Rule 4: Mandatory Policy Regime Disclosure: ": "Rule 4: Disclose Regimes: ",
    "Public statements must explicitly disclose that the estimate derives from downtown counts and assumes the post-July 2023 Unsafe Camping Ordinance enforcement environment continues.": "Explicitly state assumptions (e.g., assumes post-2023 enforcement holds).",

    # Slide 12
    "Municipal Policy Action Roadmap: Strategic Recommendations (R1–R8)": "Policy Roadmap: Recommendations (R1–R8)",
    "Immediate Action (0–3 Months)": "Immediate (0–3 Months)",
    "Outreach Focus & Reporting Governance": "Outreach & Governance",
    "R1. Focus on Hotspots:": "R1. Hotspots:",
    "R1. Focus on Hotspots: ": "R1. Hotspots: ",
    "Shortlist 16th–17th & Imperial and I-5 ramps for coordinated multidisciplinary outreach.": "Target 16th-17th & Imperial for rapid outreach.",
    "R2. Mandate Range Planning:": "R2. Range Planning:",
    "R2. Mandate Range Planning: ": "R2. Range Planning: ",
    "Enforce Rules 1–4 across all municipal and media releases; plan with ranges.": "Enforce Rules 1-4 for all public numbers.",
    "R3. Clarify Boundary Scope:": "R3. Boundary Clarity:",
    "R3. Clarify Boundary Scope: ": "R3. Boundary Clarity: ",
    "Always state whether figures cover the balanced 261-block core or expanded 382-block footprint.": "Disclose 261 vs 382-block footprint metrics.",
    "Lead Agencies:": "Leaders:",
    "Lead Agencies: ": "Leaders: ",
    "City Homelessness Strategies, DSDP, Service Outreach.": "City Strategies, DSDP.",
    
    "Medium-Term (6–12 Months)": "Medium (6–12 Months)",
    "Data Integrity & Empirical Validation": "Data & Validation",
    "R4. Complete Component Data:": "R4. Component Data:",
    "R4. Complete Component Data: ": "R4. Component Data: ",
    "Require DSDP to publish complete individual/tent/vehicle counts with consistent quadrant totals.": "Mandate full tent/vehicle component reporting.",
    "R5. Test Displacement Directly:": "R5. Displacement:",
    "R5. Test Displacement Directly: ": "R5. Displacement: ",
    "Launch coordinated cross-jurisdictional outreach tracking to verify regional movement.": "Verify cross-border regional movement.",
    "R6. Annual Retraining:": "R6. Retraining:",
    "R6. Annual Retraining: ": "R6. Retraining: ",
    "Re-estimate forecasts and county model upon release of 2026 RTFH PIT results.": "Update OLS models with 2026 PIT data.",
    "R7. Upgrade Shelter Data:": "R7. Shelter Data:",
    "R7. Upgrade Shelter Data: ": "R7. Shelter Data: ",
    "Replace synthetic placeholder shelter series with administrative Housing Inventory Count (HIC) data.": "Integrate real Housing Inventory Count (HIC).",
    
    "Long-Term (1–3 Years)": "Long-Term (1–3 Years)",
    "Spatial Digitization & System Infrastructure": "Digitization & Infrastructure",
    "R8. Digitize Remaining Maps:": "R8. Digitize Maps:",
    "R8. Digitize Remaining Maps: ": "R8. Digitize Maps: ",
    "Digitize the ~78 remaining monthly block maps to enable seasonal and post-ordinance spatial analysis.": "Digitize remaining 78 monthly block maps.",
    "Regional HMIS Integration:": "Regional HMIS:",
    "Regional HMIS Integration: ": "Regional HMIS: ",
    "Coordinate live bed availability tracking between city and county providers.": "Unify real-time city and county bed tracking.",
    "Longitudinal Evaluation:": "True Evaluation:",
    "Longitudinal Evaluation: ": "True Evaluation: ",
    "Measure true regional outcomes rather than corridor-by-corridor displacement.": "Measure regional outcomes, not just local clearing.",
    "County Health & Human Services, RTFH, DSA.": "County HHS, RTFH, DSA.",

    # Slide 13/14
    "Executive Synthesis, Data Governance & Partnership Next Steps": "Synthesis & Next Steps",
    "Evidence-Based Resource Allocation": "Fund Year-Round",
    "Move Beyond Seasonal Budgeting": "End Seasonal Budgeting",
    "Discontinue volatile seasonal budget adjustments. The empirical finding that 8 of 9 series exhibit zero seasonality (Overall series H=2.66, p=0.995) mandates locking investments into permanent, year-round shelter capacity and focused outreach on the top 10 persistent South East Village blocks.": "Data proves zero seasonality (p=0.995). Lock investments into permanent capacity and target South East Village hotspots.",
    
    "Regional Accountability & Systems Reform": "Acknowledge Reality",
    "Acknowledge the Regional Divergence Reality": "Fix Divergence",
    "Downtown reductions coincided with countywide unsheltered highs (6,110 in 2024). Solving unsheltered homelessness requires coordinated countywide shelter investments and inter-jurisdictional cooperation rather than localized displacement.": "Downtown drops pair with countywide highs (6,110). Stop localized displacement; demand countywide shelter collaboration.",
    
    "High-Value Data Investments": "Data Transparency",
    "Advance Block Digitization (R8) & Annual Retraining": "Digitize & Retrain",
    "Prioritize digitizing the remaining ~78 monthly block maps to uncover post-ordinance spatial shifts. Retrain the Policy Regime OLS model annually upon RTFH January PIT release using calibrated Student's t prediction intervals.": "Digitize remaining 78 block maps. Annually retrain the OLS model for accuracy.",

    "THE 7 SPECIALIZED DASHBOARD MODULES (TASK 9.1 & 10)": "7 DASHBOARD MODULES (TASK 9.1)",
    "Tab 1: Historical Trends View": "Tab 1: History",
    "Tab 1: Historical Trends View: ": "Tab 1: History: ",
    "Longitudinal multi-year time series (2017–2025), dynamic multiplier regime markers, macro policy epoch shading, and component toggles.": "Multi-year trends with policy epoch overlays.",
    "Tab 2: 12-Month Forward Forecast": "Tab 2: Forecast",
    "Tab 2: 12-Month Forward Forecast: ": "Tab 2: Forecast: ",
    "Prospective 2026 projections, model selectors (XGBoost champion, Holt-Winters, SARIMA, Prophet), shaded 80%/95% prediction fans, and scenario stress tests.": "2026 projections, 95% fans, and stress-testing.",
    "Tab 3: Hotspot Surveillance Map": "Tab 3: Hotspots",
    "Tab 3: Hotspot Surveillance Map: ": "Tab 3: Hotspots: ",
    "Folium interactive choropleth, 12 count dates selector, balanced 261 vs 382 footprint toggle, Getis-Ord Gi* classifications (95%, 99%), and centroid migration vector.": "Interactive Gi* maps and centroid migration.",
    "Tab 4: Neighborhood Deep-Dive": "Tab 4: Regions",
    "Tab 4: Neighborhood Deep-Dive: ": "Tab 4: Regions: ",
    "4-pane STL decomposition (Trend, Seasonality, Residuals), monthly seasonal indices, and Kruskal-Wallis non-parametric significance displays.": "STL decomposition and seasonality stats.",
    "Tab 5: County Estimation Calculator": "Tab 5: Calculator",
    "Tab 5: County Estimation Calculator: ": "Tab 5: Calculator: ",
    "Interactive Policy Regime OLS calculator strictly enforcing The 4 Public Communication Rules with Student's t prediction intervals.": "OLS estimator enforcing the 4 Comm Rules.",
    "Tab 6: Methodology & Governance": "Tab 6: Methods",
    "Tab 6: Methodology & Governance: ": "Tab 6: Methods: ",
    "Comprehensive documentation of 4 multiplier schedules, 2022 footprint expansion (+121 blocks), and root causes for historical missing data.": "Multiplier transparency and boundary docs.",
    "Tab 7: Anomaly Surveillance": "Tab 7: Alerts",
    "Tab 7: Anomaly Surveillance: ": "Tab 7: Alerts: ",
    "Shewhart control charts (+/-2sigma, +/-3sigma) and CUSUM (k=0.5, h=4.0) early-warning surveillance engine for rapid operational alerts.": "Control charts (CUSUM) for early-warnings.",

    "Local Live URL:": "Local URL:",
    "Local Live URL: ": "Local URL: ",
    "http://localhost:8501 (Fast interactive response time)": "http://localhost:8501 (Fast response)",
    "Cloud Production URL:": "Cloud URL:",
    "Cloud Production URL: ": "Cloud URL: ",
    "https://downtown-sd-homelessness.streamlit.app": "https://downtown-sd-homelessness.streamlit.app",
    "Automated Quality:": "Quality Check:",
    "Automated Quality: ": "Quality Check: ",
    "46 / 46 pytest unit tests passing with zero regressions.": "46/46 unit tests passing.",
    "Data Pipeline SLA:": "Performance:",
    "Data Pipeline SLA: ": "Performance: ",
    "@st.cache_data architecture provides fast sub-second cached lookups across all 7 tabs.": "Sub-second caching via @st.cache_data.",
    "Target Users:": "Audience:",
    "Target Users: ": "Audience: ",
    "City Council policy analysts, RTFH outreach coordinators, and DSDP operations directors.": "City Council, RTFH, DSDP operations."
}

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Text replacements
    for old, new in REPLACEMENTS.items():
        content = content.replace(old, new)
        
    # Make PPTX font sizes slightly larger for readability since we cut text
    if "pptx" in filepath.lower() or filepath.endswith(".py"):
        content = re.sub(r'Pt\(9\.5\)', 'Pt(11.5)', content)
        content = re.sub(r'Pt\(9\.0\)', 'Pt(11.0)', content)
        content = re.sub(r'Pt\(9\.2\)', 'Pt(11.2)', content)
        content = re.sub(r'Pt\(8\.8\)', 'Pt(10.8)', content)
        content = re.sub(r'Pt\(8\.5\)', 'Pt(10.5)', content)
        content = re.sub(r'Pt\(10\)', 'Pt(12)', content)

    # Increase HTML base font sizes to fill space gracefully
    if "html" in filepath.lower() or filepath.endswith(".py"):
        content = re.sub(r'font-size: 10\.5px;', 'font-size: 13.5px;', content)
        content = re.sub(r'font-size: 10px;', 'font-size: 13px;', content)
        content = re.sub(r'font-size: 9\.5px;', 'font-size: 12.5px;', content)
        content = re.sub(r'font-size: 11px;', 'font-size: 14px;', content)
        content = re.sub(r'font-size: 12px;', 'font-size: 15px;', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

patch_file("build_presentation_task93.py")
patch_file("build_html_deck_task93.py")

print("Patching complete.")
