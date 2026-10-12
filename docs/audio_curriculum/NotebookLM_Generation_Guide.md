# NotebookLM Generation Guide: 6-Episode Burmese Audio Overview Curriculum
## Downtown San Diego Homeless Population Analysis (DSA Presentation & Internship Prep)

This guide provides exact, step-by-step instructions for uploading our curriculum documents into **Google NotebookLM** and generating six production-grade **Burmese Deep Dive Audio Overviews** (မြန်မာဘာသာဖြင့် သဘာဝကျသော အသံဖိုင် ၆ ပိုင်း ထုတ်လုပ်နည်းလမ်းညွှန်)။

---

### Overview of Curriculum Episodes

| Episode | Title & Topic | Primary Markdown Source | Key Target Knowledge |
| :---: | :--- | :--- | :--- |
| **01** | **Executive Narrative & Governance** | `Episode1_ExecutiveNarrative.md` | Crisis arc, 3 epochs, The 4 Communication Rules, Regional Divergence |
| **02** | **Data Cleaning & GIS Pipeline** | `Episode2_DataCleaning_GIS.md` | A1 ingestion, A3 polygon audit, A6 multiplier regimes, 2022 expansion |
| **03** | **Seasonality Proof & Hotspot Dynamics** | `Episode3_Seasonality_Hotspots.md` | A2 EDA, A4 Kruskal-Wallis proof, A5 Getis-Ord Gi* & 120m migration |
| **04** | **ML Forecasting & County Estimation** | `Episode4_MLForecasting_CountyPIT.md` | A7 Walk-Forward CV, XGBoost champion, A8 Policy Regime OLS, Student's t |
| **05** | **Dashboard Architecture & Anomaly Engine** | `Episode5_Dashboard_AnomalySurveillance.md` | A9.1 Streamlit 7 tabs, A10 Shewhart ±2σ/±3σ, CUSUM (k=0.5, h=4.0) |
| **06** | **30-Min Presentation Masterclass & Defense** | `Episode6_PresentationMasterclass.md` + `DSA_Interview_Defense_QA.md` | 14-slide talk track, exact timings, tough technical interview defense |

---

### Phase 1: Setting Up Your NotebookLM Workspace

1. Navigate to **[https://notebooklm.google.com](https://notebooklm.google.com)** in Google Chrome.
2. Click **"+ New Notebook"**.
3. Name your notebook: **`Downtown San Diego Homelessness - DSA Curriculum (Burmese)`**.
4. **Source Upload Protocol:**
   * Always upload **`Master_Bilingual_Glossary.md`** first as an anchor source. NotebookLM uses this glossary to pronounce English technical terms correctly and keep Burmese explanations consistent.
   * Then upload the specific episode file you want to generate (e.g., `Episode1_ExecutiveNarrative.md`).
   * *Tip:* For Episode 6, upload both `Episode6_PresentationMasterclass.md` and `DSA_Interview_Defense_QA.md`.

---

### Phase 2: Generating Audio Overviews (Step-by-Step)

1. Open the **Notebook Guide** / **Studio** panel on the right-hand side.
2. Locate the **Audio Overview** section.
3. Click the **Customize** (pencil icon) button.
4. Set the options:
   * **Format:** Select **Deep Dive** (two AI hosts engaging in a rich, explanatory dialogue).
   * **Language:** Ensure output language is set to **Burmese (မြန်မာ)**.
5. In the **"What should the hosts focus on?"** prompt box, copy and paste the corresponding **Custom Prompt Template** below.
6. Click **Generate**.
7. Allow 3–5 minutes for Google NotebookLM to synthesize the audio file.
8. Click **Download** to save the `.wav` or `.mp3` file to your computer or phone for listening on the go.

---

### Phase 3: Exact Custom Prompt Templates for Each Episode

---

#### 🎧 Episode 1: Executive Narrative & Macro Governance
* **Sources to Check in NotebookLM:** `Master_Bilingual_Glossary.md` + `Episode1_ExecutiveNarrative.md`
* **Custom Instructions Prompt:**
```text
Please generate a comprehensive, highly engaging Deep Dive Audio Overview in Burmese (မြန်မာဘာသာ). 

Roles & Style:
The two hosts should converse naturally like two expert data science partners discussing a high-stakes municipal report for the Data Science Alliance. Speak in fluent, professional Burmese, but pronounce all technical terms in English (e.g., 'Unsheltered Homelessness', 'Point-in-Time PIT Count', 'Multi-Year Epochs', 'Spatial Divergence', 'Policy Regime', 'Student's t Distribution').

Key Points to Cover:
1. The 9-year arc of Downtown San Diego unsheltered homelessness from 2017 to 2025 across 108 monthly censuses.
2. The Three Macro Policy Epochs: Baseline Contraction (2017-2020, series low 529 in Mar 2020), Crisis Surge (2021-2023, all-time peak 2,103 in May 2023), and Enforcement Pullback (2024-2025, Jan 2025 count 851).
3. The Regional Displacement Paradox: Why downtown unsheltered counts fell by 56% while countywide unsheltered counts reached an all-time record of 6,110 in 2024. Emphasize that downtown reduction did not mean regional elimination.
4. The 4 Mandatory Public Communication Rules: Rule 1 (No single-point precision), Rule 2 (Round to nearest 100), Rule 3 (Always publish 95% interval: '5,900 [3,900 to 8,000]'), and Rule 4 (Mandatory policy regime disclosure).

Tone: Analytical, objective, empathetic, and strictly evidence-based. No causal claims.
```

---

#### 🎧 Episode 2: Data Cleaning, GIS Geometry & Multipliers
* **Sources to Check in NotebookLM:** `Master_Bilingual_Glossary.md` + `Episode2_DataCleaning_GIS.md`
* **Custom Instructions Prompt:**
```text
Please generate a technical Deep Dive Audio Overview in Burmese (မြန်မာဘာသာ) explaining the data engineering and spatial foundation.

Style:
Conversational Burmese dialogue with precise English technical terminology (e.g., 'PDF Ingestion', 'Polygon Validity', 'Spatial Join', 'Multiplier Regimes', 'Balanced Panel', 'Expansion Wedge').

Key Points to Cover:
1. Assignment 1: Extracting 108 months of DSDP monthly PDFs (104 published, 4 missing in 2025), handling layout changes and verifying total counts.
2. Assignment 3: GIS verification of 382 downtown blocks. Confirm 380 of 382 centroids fall inside their polygons, with 2 concave freeway interchange exceptions. Street adjacency checks across 326 interior blocks.
3. Assignment 6: Multiplier regime history (PRE2017 2.0x, APR2017 1.75x/1.66x, MAY2018 1.75x/2.03x, POST2020). Why constant methodology was constructed.
4. The 2022 Footprint Expansion Wedge (+121 peripheral blocks in Golden Hill, Barrio Logan, Sherman Heights). Explain why the balanced 261-block panel was required to prove that while 2022 surged +71%, up to 32.8% of reported headline counts in Jan 2023 was administrative map expansion.
```

---

#### 🎧 Episode 3: Debunking Seasonality & Hotspot Migration
* **Sources to Check in NotebookLM:** `Master_Bilingual_Glossary.md` + `Episode3_Seasonality_Hotspots.md`
* **Custom Instructions Prompt:**
```text
Please generate an insightful Deep Dive Audio Overview in Burmese (မြန်မာဘာသာ) focusing on econometric seasonality testing and spatial cluster migration.

Style:
Engaging discussion between two data scientists debunking common municipal myths using rigorous mathematics. Technical terms in English (e.g., 'Kruskal-Wallis Test', 'STL Decomposition', 'Global Moran's I', 'Getis-Ord Gi*', 'Centroid Migration Vector', 'Bearing').

Key Points to Cover:
1. Assignment 4: Debunking the seasonality myth. Explain that 8 of 9 series have no statistically significant seasonality under Kruskal-Wallis (Overall series H=2.66, p=0.995). Explain why weather accounts for <5% of variance and why municipal seasonal emergency budgeting is flawed. Explain Marina's borderline p=0.047 exception due to convention center buffer sweeps.
2. Assignment 5: Spatial autocorrelation. Global Moran's I is positive on all 12 dates (0.063 to 0.239). Local Getis-Ord Gi* identifies 16 at 99% and 22 at 95% hotspot block-dates.
3. Top persistent hotspot blocks: #1 16th & Imperial (9/12 dates), #2 I-5 SB & Imperial (8/12 dates). 100% of top 10 are in South East Village.
4. The centroid migration vector of about 120 meters on a bearing of 160° SSE between 2018-2020 and 2022-2025. Emphasize that this tracks cluster locations, not individual people.
```

---

#### 🎧 Episode 4: Machine Learning Forecasting & County Estimation
* **Sources to Check in NotebookLM:** `Master_Bilingual_Glossary.md` + `Episode4_MLForecasting_CountyPIT.md`
* **Custom Instructions Prompt:**
```text
Please generate an executive Deep Dive Audio Overview in Burmese (မြန်မာဘာသာ) on predictive machine learning and econometric macro modeling.

Style:
Clear, professional Burmese dialogue discussing machine learning validation, avoiding data leakage, and macro policy modeling. English technical terms (e.g., 'Walk-Forward Cross-Validation', 'XGBoost', 'SARIMA', 'Holt-Winters', 'Prophet', 'Leave-One-Out Cross-Validation LOOCV', 'Policy Regime OLS').

Key Points to Cover:
1. Assignment 7: 5-Fold walk-forward cross-validation across 96 months. SARIMA wins short horizons (1-month MAPE 5.4%). At 12 months, XGBoost (38.3%), Holt-Winters (38.4%), and SARIMA (39.6%) are in a statistical tie due to 26-36 point fold variance. Explain why XGBoost was kept as champion and why Prophet failed (64.2%). Explain why the naive seasonal baseline won the 2025 hold-out (6.3%).
2. 2026 Prospective Outlook: 816 to 896 range (Month 12 Dec 2026: 888, 95% PI 539-1,237). Explain that optimistic (-24%, ~675) and pessimistic (+26%, ~1,123) paths are fixed stress-test scenarios, not policy simulations.
3. Assignment 8: Countywide estimation model. Constant ratio fails (ANOVA F=66.51, p=0.0002, eta^2=0.964, Pearson r=-0.061). Policy Regime OLS model achieves R^2=0.504 and LOOCV RMSE=815.3. Explain the small sample size (N=8) and power limits (23%).
4. Current county estimate: 5,900 [3,900 to 8,000] (margin of error +/- 35%). Strict adherence to The 4 Public Communication Rules.
```

---

#### 🎧 Episode 5: Interactive Dashboard & Anomaly Surveillance
* **Sources to Check in NotebookLM:** `Master_Bilingual_Glossary.md` + `Episode5_Dashboard_AnomalySurveillance.md`
* **Custom Instructions Prompt:**
```text
Please generate an operational Deep Dive Audio Overview in Burmese (မြန်မာဘာသာ) covering system deployment and real-time surveillance algorithms.

Style:
Dynamic Burmese conversation exploring software engineering, quality testing, and statistical process control. English technical terms (e.g., 'Streamlit Decision-Support System', 'Pytest Regression Suite', 'Statistical Process Control', 'Shewhart Control Chart', 'CUSUM', 'Early Warning Alerts').

Key Points to Cover:
1. Assignment 9.1: Streamlit Executive Dashboard architecture across all 7 specialized tabs (Trends, Forecast, Hotspots, Neighborhoods, County Calculator, Methodology, Anomaly Surveillance). Mention live deployment at https://downtown-sd-homelessness.streamlit.app with 46 passing pytest tests.
2. Assignment 10: Multi-source ensemble modeling. Explain that the lag-1 naive baseline (MAE 119.6) outperformed the complex ML ensemble (MAE 248.0) due to strong autoregressive persistence. Highlight the audit finding that shelter capacity data were constructed placeholders and must not be used for capacity policy (Recommendation R7).
3. Statistical Surveillance Engine: Dual-layer SPC using Shewhart charts (+/-2 sigma warning, +/-3 sigma action) and tabular CUSUM (k=0.5, h=4.0). Explain how it caught all 4 major historical policy breaks with 68.8% precision.
```

---

#### 🎧 Episode 6: Presentation Masterclass & Technical Defense
* **Sources to Check in NotebookLM:** `Master_Bilingual_Glossary.md` + `Episode6_PresentationMasterclass.md` + `DSA_Interview_Defense_QA.md`
* **Custom Instructions Prompt:**
```text
Please generate an executive-coaching Deep Dive Audio Overview in Burmese (မြန်မာဘာသာ) preparing the analyst for a 30-minute high-stakes technical presentation and defense before Adir Mancebo Jr. and the Data Science Alliance team.

Style:
Mentoring dialogue between a senior data science mentor and Kyaw Soe Lwin. The mentor coaches the analyst on delivery, exact slide timing, slide-by-slide transitions, and how to defend difficult technical questions with empirical confidence and humility. English technical terms and talking points embedded seamlessly.

Key Points to Cover:
1. Walk through the 14-slide presentation structure, highlighting target timings (total 22 min presentation + 8 min Q&A).
2. Key verbal points for Slide 2 (KPIs: 2,103, 851, 54.0%, 120m), Slide 4 (Seasonality H=2.66 p=0.995), Slide 8 (XGBoost 38.3% tie with HW/SARIMA), Slide 10 (Regional divergence 6,110), and Slide 11 (Policy Regime OLS R^2=0.504 and Rules 1-4).
3. Tough Defense Prep: How to answer tough questions honestly:
   - Why simple baseline beat complex ensemble (persistence, regime shift).
   - Why R^2=0.504 county model is still useful as a bridging range [3,900 to 8,000], not an exact HUD count.
   - Why July 2023 was not tested under Chow break tests (scope limitation, not falsification).
   - Why we do not claim causal displacement (lack of micro-tracking data).
   - Why Recommendation R8 (digitizing ~78 remaining block maps) is the highest-ROI investment.
```

---

### Phase 4: Study & Rehearsal Workflow for Kyaw Soe Lwin

1. **Daily Listening Routine:**
   * Download the 6 audio episodes to your smartphone.
   * Listen to Episode 1 through Episode 5 during your commute or evening review.
   * Listen to **Episode 6** with the PowerPoint deck open in front of you on your laptop, practicing speaking the English bullet points aloud.
2. **Rehearsal Drill:**
   * Time yourself speaking through Slide 1 to 14 using the English speaking points. Aim for exactly 21 to 23 minutes.
   * Have a friend or colleague ask you 3 random questions from `DSA_Interview_Defense_QA.md`.
   * Practice delivering the calm, confident, and honest responses.
