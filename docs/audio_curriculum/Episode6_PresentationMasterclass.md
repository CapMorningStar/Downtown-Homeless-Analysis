# Episode 6: Presentation Masterclass & 30-Minute Defense Script
## Downtown San Diego Homeless Population Analysis (DSA Briefing & Internship Defense)

**Target Audience:** Adir Mancebo Jr. (Project Lead), Data Science Alliance (DSA) technical team, municipal stakeholders (City/RTFH/DSDP).  
**Format:** Bilingual Executive Script (English Technical Speaking Points + Burmese Deep-Dive Conceptual Explanations).  
**Total Presentation Time:** 30 Minutes (20–22 min slide walkthrough + 8–10 min technical Q&A).  
**Accompanying Visuals:** [`Assignment9_StrategicSynthesis.pptx`](../../Assignment9_StrategicSynthesis.pptx) and [`Assignment9_StrategicSynthesis.html`](../../Assignment9_StrategicSynthesis.html).  

---

### Master Slide Timing & Agenda (30 Minutes Total)

| Slide # | Slide Title & Focus Area | Target Time | Cumulative |
| :---: | :--- | :---: | :---: |
| **01** | Title & Project Governance Foundation | 1.5 min | 1.5 min |
| **02** | Executive KPI Dashboard: The 4 Core Truths | 2.0 min | 3.5 min |
| **03** | The 9-Year Trajectory & Three Macro Policy Epochs | 2.0 min | 5.5 min |
| **04** | Debunking Seasonality: Econometric Proof | 2.0 min | 7.5 min |
| **05** | The 2022 Footprint Expansion Wedge (+121 Blocks) | 1.5 min | 9.0 min |
| **06** | Geographic Concentration: The East Village Epicenter | 1.5 min | 10.5 min |
| **07** | Hotspot Dynamics: The 120-Meter Centroid Migration | 1.5 min | 12.0 min |
| **08** | Machine Learning Benchmark: 5-Fold Walk-Forward CV | 2.0 min | 14.0 min |
| **09** | 2026 Prospective Outlook & Scenario Stress Testing | 1.5 min | 15.5 min |
| **10** | Regional Divergence: Downtown vs. County PIT | 2.0 min | 18 min |
| **11** | County Estimation Model & The 4 Communication Rules | 2.0 min | 20 min |
| **12** | Municipal Policy Action Roadmap (Memo R1–R8) | 1.5 min | 21 min |
| **13** | Interactive Decision-Support Dashboard (7 Tabs) | 1.0 min | 22 min |
| **14** | Executive Synthesis & Strategic Next Steps | 1.0 min | 23 min |
| **Q&A** | Technical Committee & Stakeholder Defense | 7.0 min | 30 min |

---

## Slide-by-Slide Presentation Scripts

---

### Slide 1: Title Slide & Analytical Foundation
* **Slide File:** Slide 1 of 14  
* **Visual Anchor:** Blue and White Modern Data Analytics title card with DSA partnership metadata.  
* **Target Timing:** 1:30 min (0:00 – 1:30)

#### 🎙️ English Speaking Points (Say this verbatim):
> "Good morning, Adir, and esteemed members of the Data Science Alliance team. I am Kyaw Soe Lwin, Lead Analyst on this project. Today, I am proud to present our comprehensive strategic synthesis on Downtown San Diego Unsheltered Homelessness from 2017 through 2026.
>
> This analysis is grounded in nine years of monthly physical field censuses across 382 blocks from the Downtown San Diego Partnership, combined with annual Point-in-Time counts from the Regional Task Force on Homelessness. Our analytical framework bridges spatial statistics, non-parametric econometrics, 5-fold walk-forward machine learning, and policy-regime regression. Crucially, every finding is governed by our Four Public Communication Rules to ensure empirical rigor without false certainty. Let's examine the core findings."

#### 🇲🇲 Burmese Explanation (မြန်မာဘာသာဖြင့် အသေးစိတ် သဘောပေါက်ရန်):
> အာဒီ (Adir) နဲ့ DSA ဒေတာဆိုင်းယန့်စ် အဖွဲ့ဝင်များကို နှုတ်ခွန်းဆက်သပြီး ဒီပရောဂျက်ရဲ့ အနှစ်ချုပ်ကို မိတ်ဆက်ရပါမယ်။ မိမိကိုယ်ကို Lead Analyst Kyaw Soe Lwin အဖြစ် မိတ်ဆက်ပြီး ၂၀၁၇ မှ ၂၀၂၆ အထိ ၉ နှစ်တာ စစ်တမ်းဒေတာတွေ (လစဉ် ကွင်းဆင်းကောက်ယူမှု ၁၀၈ လအနက် ထုတ်ပြန်ထားသော ၁၀၄ လဒေတာ နှင့် ဘလောက်ပေါင်း ၃၈၂ ဘလောက်) ကို အခြေခံထားကြောင်း တင်ပြရပါမယ်။ 
>
> အဓိက သုံးထားတဲ့ မူဘောင်တွေဖြစ်တဲ့ Spatial Econometrics (Getis-Ord Gi*)၊ 5-Fold Walk-Forward Machine Learning၊ Policy Regime OLS နဲ့ အများပြည်သူသို့ ဆက်သွယ်ထုတ်ပြန်ရာတွင် လိုက်နာရမည့် မဖြစ်မနေ စည်းမျဉ်း ၄ ချက် (The 4 Public Communication Rules) ကို အလေးထား တင်ပြရပါမယ်။

---

### Slide 2: Executive KPI Dashboard (The 4 Core Metrics)
* **Slide File:** Slide 2 of 14  
* **Visual Anchor:** 4 Top KPI Cards (2,103 / 851 / 54.0% / 120 m) + Lower Strategic Synthesis Box.  
* **Target Timing:** 2:00 min (1:30 – 3:30)

#### 🎙️ English Speaking Points:
> "To understand downtown San Diego's homelessness dynamics, we must anchor our discussion in four verified empirical metrics:
> 1. **Peak Count (2,103.3 in May 2023):** The all-time headline peak, capping a three-year post-pandemic escalation.
> 2. **Recent Count (851 in January 2025):** A 59.5% reduction from that peak following the July 2023 Unsafe Camping Ordinance and Safe Sleeping site rollouts. The series closed at 985.4 in December 2025.
> 3. **Spatial Concentration (54.0% in East Village):** East Village remains the historic epicenter, averaging 552.0 individuals per month.
> 4. **Hotspot Migration (~120 meters SSE):** The count-weighted cluster centroid shifted about 120 meters south-south-east toward South East Village between 2018–2020 and 2022–2025.
>
> But here is the critical strategic takeaway: while downtown unsheltered counts fell by over 56% between January 2023 and January 2025, countywide unsheltered homelessness rose to an all-time record of 6,110 in 2024. A localized downtown reduction did not translate to a regional solution."

#### 🇲🇲 Burmese Explanation:
> ဒုတိယဆလိုက်မှာ KPI ၄ ခုကို တိကျစွာ ပြောရပါမယ် - (၁) အမြင့်ဆုံးစံချိန် ၂,၁၀၃ (မေလ ၂၀၂၃)၊ (၂) လတ်တလော ကျဆင်းသွားတဲ့ စစ်တမ်း ၈၅၁ (ဇန်နဝါရီ ၂၀၂၅)၊ (၃) East Village မှာ ၅၄.၀% စုပြုံနေမှု (တစ်လ ပျမ်းမျှ ၅၅၂ ယောက်)၊ (၄) ဟော့စပေါ့ ဗဟိုချက် ၁၂၀ မီတာ တောင်ဘက်သို့ ရွေ့လျားမှု။
>
> ⚠️ အဓိက သတိပြုရမည့် အချက်မှာ Downtown မှာ ၅၆% ကျဆင်းသွားသော်လည်း တစ်ခရိုင်လုံး (Countywide) တွင် ၂၀၂၄ ခုနှစ်၌ အမြင့်ဆုံး စံချိန် ၆,၁၁၀ အထိ တက်သွားခြင်း ဖြစ်သည်။ ဒေါင်းတောင်း ရှင်းလင်းမှုသည် အိုးမဲ့အိမ်မဲ့ပြဿနာကို ပြီးပြတ်စေခြင်း မဟုတ်ဘဲ အခြားနေရာများသို့ နေရာပြောင်းရွှေ့သွားခြင်း (Regional Divergence / Displacement) ဖြစ်နိုင်ခြေကို မီးမောင်းထိုးပြရပါမည်။

---

### Slide 3: The 9-Year Trajectory & Three Macro Epochs
* **Slide File:** Slide 3 of 14  
* **Visual Anchor:** `slide_assets/task93_trajectory_9year.png` with color-shaded epochs and data gap callouts.  
* **Target Timing:** 2:00 min (3:30 – 5:30)

#### 🎙️ English Speaking Points:
> "Turning to Slide 3, we see the full 108-month historical trajectory from January 2017 through December 2025. This timeline divides neatly into three macro policy epochs:
> * **Epoch 1: Baseline Contraction (2017–2020):** Annual averages fell from 1,057.8 to 654.1—a 38.2% drop—hitting a historical series low of 529.1 in March 2020 during early COVID shelter initiatives.
> * **Epoch 2: The Crisis Surge (2021–2023):** Escalated dramatically to an annual mean of 1,563.1 in 2023, peaking at 2,103 in May 2023. This was driven by shelter de-densification, economic pressures, and post-moratoria vulnerability.
> * **Epoch 3: Enforcement & Stabilization (2024–2025):** Annual averages contracted to 886.9 in 2024 and 864.3 in 2025.
>
> Note an important data governance fact: four months in 2025 (July, August, October, and November) were unpublished by DSDP. Our production chart plots these honestly as gaps rather than distorting the timeline with zeros."

#### 🇲🇲 Burmese Explanation:
> ဆလိုက် ၃ တွင် ၉ နှစ်တာ လိုင်းဂရပ်ကို ရှင်းပြရပါမယ်။ Macro Epoch ၃ ခု ရှိပါတယ်-
> ၁။ ပထမခေတ် (၂၀၁၇-၂၀၂၀): တစ်နှစ်ပျမ်းမျှ ၁,၀၅၈ မှ ၆၅၄ သို့ ၃၈.၂% ကျဆင်းခဲ့ပြီး၊ မတ်လ ၂၀၂၀ တွင် သမိုင်းတစ်လျှောက် အနိမ့်ဆုံး ၅၂၉.၁ အထိ ကျဆင်းခဲ့သည်။
> ၂။ ဒုတိယခေတ် (၂၀၂၁-၂၀၂၃): မတ်လ ၂၀၂၀ အနိမ့်ဆုံးမှ မေလ ၂၀၂၃ အမြင့်ဆုံး ၂,၁၀၃ အထိ +၂၉၇% ခုန်တက်ခဲ့သည်။
> ၃။ တတိယခေတ် (၂၀၂၄-၂၀၂၅): စခန်းချမှုတားမြစ်ရေး ဥပဒေ (Camping Ordinance) ကြောင့် ၈၈၇ နှင့် ၈၆၄ သို့ ပြန်လည်ကျဆင်း ငြိမ်သက်သွားသည်။
> ⚠️ ၂၀၂၅ တွင် DSDP မှ မထုတ်ပြန်ရသေးသော လ ၄ လ (ဇူလိုင်၊ သြဂုတ်၊ အောက်တိုဘာ၊ နိုဝင်ဘာ) ကို သုည (zero) အဖြစ် မဆွဲဘဲ ကွက်လပ် (gap) အဖြစ် အမှန်အတိုင်း ပြသထားကြောင်း ဒေတာသမာဓိကို ထည့်သွင်းပြောကြားပါ။

---

### Slide 4: Debunking the Seasonality Myth
* **Slide File:** Slide 4 of 14  
* **Visual Anchor:** Kruskal-Wallis Test Results Table (9 series) + Municipal Budgeting Implications.  
* **Target Timing:** 2:00 min (5:30 – 7:50)

#### 🎙️ English Speaking Points:
> "Slide 4 addresses one of the most widespread misconceptions in civic planning: the belief that homelessness is driven by weather cycles.
>
> We conducted rigorous Kruskal-Wallis non-parametric testing across all nine geographic series over the full 108 months. The result is decisive: eight of the nine series exhibit **zero statistically significant seasonality**. For the overall reported footprint, the H-statistic is 2.66 with a p-value of 0.995 (ANOVA p = 0.998).
>
> The only series showing borderline significance was Marina with H = 19.88, p = 0.047, but ANOVA was non-significant at p = 0.162. That reflects localized convention center buffer sweeps and summer tourism events, not a seasonal homeless influx.
>
> **The Municipal Budgeting Implication:** Setting shelter bed budgets or outreach staffing on 'winter surges' or 'summer peaks' is unsupported by the data. Variance is governed by multi-year policy regimes and shelter capacity shocks, not temperature."

#### 🇲🇲 Burmese Explanation:
> ဆလိုက် ၄ ကတော့ "ရာသီဥတုကြောင့် အိုးမဲ့အိမ်မဲ့ အရေအတွက် ပြောင်းလဲသည်" ဆိုတဲ့ အယူအဆမှား (Seasonality Myth) ကို သင်္ချာနည်းအရ ချေပခြင်း ဖြစ်ပါတယ်။
> Kruskal-Wallis non-parametric စစ်ဆေးမှုအရ ၉ ခုမှာ ၈ ခုသည် ရာသီအလိုက် ကွာခြားမှု လုံးဝမရှိပါ (Overall series H=2.66, p=0.995)။ Marina ရပ်ကွက်တစ်ခုတည်းသာ p=0.047 ဖြင့် အနည်းငယ် ထူးခြားသော်လည်း ANOVA အရ p=0.162 ဖြင့် မထူးခြားပါ။
> ဒါကြောင့် မြို့တော်စည်ပင်အနေနဲ့ "ဆောင်းတွင်းယာယီအိပ်ဆောင်" ဖွင့်တာမျိုးမဟုတ်ဘဲ၊ တစ်နှစ်ပတ်လုံး ပုံသေထားရှိသော Year-Round Shelter Bed ဘတ်ဂျက်ကိုသာ ချထားသင့်ကြောင်း မူဝါဒအကြံပြုချက် ပေးရပါမယ်။

---

### Slide 5: The 2022 Footprint Expansion Wedge (+121 Blocks)
* **Slide File:** Slide 5 of 14  
* **Visual Anchor:** `slide_assets/task93_footprint_wedge.png` (Stacked bars: 261 balanced vs 121 expansion).  
* **Target Timing:** 1:30 min (7:50 – 9:20)

#### 🎙️ English Speaking Points:
> "On Slide 5, we uncover a crucial spatial accounting artifact. In January 2022, DSDP expanded its survey footprint from 261 blocks to 382 blocks, adding 121 peripheral blocks across Golden Hill (52), Barrio Logan (35), and Sherman Heights (34).
>
> Across the five subsequent digitized dates, these added blocks accounted for between **3.7% and 32.8%** of the reported downtown total. At the peak in January 2023, 640.6 out of 1,955.1 individuals—nearly one-third of the count—were located in the expansion zone.
>
> Now, the underlying crisis was still real: on the constant 261-block panel, counts still surged +71% in 2022. However, naive comparisons across the 2021/2022 threshold conflated drawing a larger map with population growth. We built the balanced 261-block panel to isolate true longitudinal changes."

#### 🇲🇲 Burmese Explanation:
> ဆလိုက် ၅ တွင် ၂၀၂၂ ခုနှစ် မြေပုံချဲ့ထွင်မှု (+၁၂၁ ဘလောက်) ကို ရှင်းပြရပါမယ်။ DSDP သည် မူလ ၂၆၁ ဘလောက်မှ ၃၈၂ ဘလောက်သို့ ချဲ့ထွင်ခဲ့ရာ၊ ရရှိလာသော လူဦးရေတိုးတက်မှု၏ ၃.၇% မှ ၃၂.၈% အထိသည် မြေပုံချဲ့လိုက်သောကြောင့် ပါလာခြင်း ဖြစ်သည်။
> မူလ ၂၆၁ ဘလောက်တည်းမှာလည်း ၇၁% တိုးခဲ့သဖြင့် အိုးမဲ့အိမ်မဲ့ တကယ်တိုးခဲ့သည်မှာ မှန်သော်လည်း၊ မြေပုံချဲ့မှုကြောင့် ပိုတိုးသယောင် ဖြစ်ခဲ့ရခြင်းကို ခွဲခြားသိမြင်စေရန် `BlockPanel_Balanced_261.csv` ကို ဒေတာအင်ဂျင်နီယာအဖြစ် တည်ဆောက်ခဲ့ရကြောင်း တင်ပြပါ။

---

### Slide 6: Geospatial Concentration: The East Village Epicenter
* **Slide File:** Slide 6 of 14  
* **Visual Anchor:** Persistent Hotspot Ranking Table (Getis-Ord Gi*) + Built-Environment Infrastructure.  
* **Target Timing:** 1:30 min (9:20 – 10:50)

#### 🎙️ English Speaking Points:
> "Slide 6 examines where unsheltered homelessness physically concentrates. East Village historically represents 54.0% of all downtown homelessness, averaging 552.0 individuals a month. Within East Village, the South East quadrant accounts for over 317 people—more than the other three quadrants combined.
>
> Using local Getis-Ord Gi* across all 12 digitized dates, we identified the top persistent hotspot blocks:
> * **#1:** 16th St & Imperial Ave (significant on 9 of 12 dates, 75%)
> * **#2:** I-5 Southbound at Imperial Ave (8 of 12 dates, 67%)
> * **#3:** I-5 Southbound Off-Ramp (6 of 12 dates, 50%)
> * **#4 & #5:** I-5 Southbound On-Ramp and 17th & Imperial (4 of 12 dates each)
>
> Notice that 100% of the top ten blocks are in South East Village. They cluster around three infrastructure pillars: the 12th & Imperial Transit Center, social service intake hubs, and Caltrans freeway underpasses providing overhead shelter."

#### 🇲🇲 Burmese Explanation:
> ဆလိုက် ၆ တွင် East Village မှာ တစ်မြို့လုံး၏ ၅၄.၀% (လစဉ် ပျမ်းမျှ ၅၅၂ ယောက်) စုပြုံနေပြီး၊ အထူးသဖြင့် South East Village တွင် ၃၁၇ ယောက်ကျော် ရှိနေကြောင်း ရှင်းပြပါ။
> Getis-Ord Gi* တွက်ချက်မှုအရ အမြဲတစေ ဟော့စပေါ့ဖြစ်နေသော ဘလောက် ၅ ခုမှာ (၁) 16th & Imperial (၉ ကြိမ်/၁၂ ကြိမ်)၊ (၂) I-5 SB at Imperial (၈ ကြိမ်)၊ (၃) I-5 SB Off-Ramp (၆ ကြိမ်)၊ (၄) I-5 On-Ramp (၄ ကြိမ်)၊ (၅) 17th & Imperial (၄ ကြိမ်) တို့ ဖြစ်ပြီး အားလုံး South East Village တွင် ရှိနေပါသည်။ ကားဂိတ်ကြီးများ၊ ဝန်ဆောင်မှုပေးသည့်ရုံးများနှင့် အဝေးပြေးတံတားအောက်များတွင် စုပြုံနေခြင်း ဖြစ်သည်။

---

### Slide 7: Hotspot Dynamics: The 120-Meter Centroid Migration
* **Slide File:** Slide 7 of 14  
* **Visual Anchor:** `slide_assets/task93_hotspot_migration.png` (Left: Centroid Vector Diagram; Right: Persistence Bar Chart).  
* **Target Timing:** 1:30 min (10:50 – 12:20)

#### 🎙️ English Speaking Points:
> "On Slide 7, we track the spatial evolution of these clusters over time. Comparing the Early Period (2018–2020, 10 dates) to the Recent Period (2022–2025, 20 dates), the count-weighted hotspot centroid migrated **about 120 meters on a bearing of 160°—south-south-east**.
>
> The unweighted centroid moved 62 meters, proving that both the physical positioning and the density weighting shifted southward.
>
> What drove this? Sidewalk enforcement in northern commercial corridors (Gaslamp, Core/City Center, North East Village) pushed encampments southward toward Commercial Street and the Interstate 5 industrial buffer.
>
> We must emphasize an empirical boundary: this vector describes where statistically significant clusters sit across count dates. It is a spatial cluster trajectory, not direct tracking of individual persons."

#### 🇲🇲 Burmese Explanation:
> ဆလိုက် ၇ တွင် အစောပိုင်းကာလ (၂၀၁၈-၂၀၂၀) မှ မကြာသေးမီကာလ (၂၀၂၂-၂၀၂၅) အထိ ဟော့စပေါ့ဗဟိုချက်သည် **မီတာ ၁၂၀ ခန့်၊ အရှေ့တောင်ဘက် (၁၆၀ ဒီဂရီ bearing)** သို့ ရွေ့လျားသွားခဲ့ကြောင်း ရှင်းပြပါ။
> လူဦးရေမပါသော ပထဝီဗဟိုချက်သည်လည်း ၆၂ မီတာ ရွေ့ခဲ့သည်။ မြောက်ဘက် စီးပွားရေးဇုန်များ (Gaslamp, City Center) တွင် လမ်းဘေးရှင်းလင်းရေးများ တင်းကျပ်လာသောကြောင့် တောင်ဘက်စက်မှုဇုန်နှင့် I-5 အဝေးပြေးလမ်းဆီသို့ အစုအပြုံလိုက် တွန်းပို့ခံရသကဲ့သို့ ဖြစ်ခဲ့သည်။ 
> ⚠️ အရေးကြီးသော ကန့်သတ်ချက် - ဤရွှေ့လျားမှုသည် လူတစ်ဦးချင်းစီနောက် လိုက်လံစောင့်ကြည့်ထားခြင်း မဟုတ်ဘဲ အစုအဝေးတည်နေရာများ (Cluster Locations) ၏ ရွေ့လျားမှုသာ ဖြစ်သည်။

---

### Slide 8: Machine Learning Forecasting Benchmark
* **Slide File:** Slide 8 of 14  
* **Visual Anchor:** 5-Fold Walk-Forward Cross-Validation Performance Table (Table 8.1).  
* **Target Timing:** 2:00 min (12:20 – 14:20)

#### 🎙️ English Speaking Points:
> "Slide 8 presents our multi-model machine learning benchmark across 96 training months using 5-fold walk-forward cross-validation with zero lookahead leakage.
>
> Looking at Table 8.1:
> * At short horizons (1-month), SARIMA dominates with a 5.4% MAPE.
> * At the critical 12-month policy horizon, XGBoost (38.3%), Holt-Winters (38.4%), and SARIMA (39.6%) are in a statistical tie, given fold-to-fold standard deviations of 26 to 36 percentage points.
> * XGBoost was selected as the overall champion because it achieved the lowest 12-month mean (38.3%) and demonstrated strong 2025 hold-out performance (8.5%).
> * Crucially, our naive seasonal baseline (t-12) achieved 6.3% on the 2025 hold-out because 2025 closely mirrored 2024. This proves why naive baselines must never be discarded.
> * Prophet failed across all horizons (64.2% at 12 months) because fixed changepoints cannot capture sudden policy inflections."

#### 🇲🇲 Burmese Explanation:
> ဆလိုက် ၈ တွင် မော်ဒယ် ၅ ခုကို 5-Fold Walk-Forward Cross-Validation ဖြင့် စမ်းသပ်ထားမှုကို ရှင်းပြပါ။
> * ၁ လကြိုတင်ခန့်မှန်းမှုတွင် SARIMA က ၅.၄% MAPE ဖြင့် အကောင်းဆုံး ဖြစ်သည်။
> * ၁၂ လ ခန့်မှန်းမှုတွင် XGBoost (၃၈.၃%)၊ Holt-Winters (၃၈.၄%) နှင့် SARIMA (၃၉.၆%) တို့သည် ကိန်းဂဏန်းအရ တူညီလုနီးပါး သရေကျခဲ့သည်။
> * ပျမ်းမျှအမှားအနည်းဆုံး ဖြစ်သောကြောင့် XGBoost ကို Champion အဖြစ် ရွေးချယ်ခဲ့သည်။
> * ၂၀၂၅ Hold-out စမ်းသပ်မှုတွင် Naive Seasonal (ယခင်နှစ်ကာလတူအတိုင်းခန့်မှန်းချက်) က ၆.၃% ဖြင့် အမှားအနည်းဆုံး ဖြစ်ခဲ့သည်။ (အဘယ်ကြောင့်ဆိုသော် ၂၀၂၅ သည် ၂၀၂၄ နှင့် အလွန်ဆင်တူသောကြောင့် ဖြစ်သည်)။
> * Prophet မော်ဒယ်သည် မူဝါဒအပြောင်းအလဲများကို မလိုက်နိုင်သဖြင့် ၆၄.၂% အထိ အမှားများခဲ့သည်။

---

### Slide 9: 2026 Forward Outlook & Scenario Planning
* **Slide File:** Slide 9 of 14  
* **Visual Anchor:** `slide_assets/task93_forecast_2026.png` (Prospective fan envelope with optimistic/pessimistic paths).  
* **Target Timing:** 1:30 min (14:20 – 15:50)

#### 🎙️ English Speaking Points:
> "Slide 9 displays our prospective 12-month forecast for 2026.
>
> Under our status-quo XGBoost baseline, monthly counts are projected to remain range-bound between 816 and 896 individuals, closing at 888 in December 2026.
>
> We also stress-test two fixed policy scenarios:
> * **Optimistic Path (-24% at M12):** Street counts fall to ~675 individuals by December 2026 if shelter expansion and placement velocity accelerate.
> * **Pessimistic Path (+26% at M12):** Street counts rebound to ~1,123 individuals if shelter capacity exhausts and housing stress increases.
>
> **Methodological Note:** The scenarios are fixed what-if trajectories (-2% and +2.2% monthly), not structural policy simulations. Furthermore, our prediction intervals (539 to 1,237 at Month 12) are derived from Holt-Winters residual variance. Decision-makers must budget for ranges, never single numbers."

#### 🇲🇲 Burmese Explanation:
> ဆလိုက် ၉ တွင် ၂၀၂၆ ခုနှစ်အတွက် ၁၂ လ ကြိုတင်ခန့်မှန်းချက်ကို ပြသထားပါသည်။
> ပုံမှန်အခြေအနေ (Status Quo Baseline) တွင် လစဉ်လူဦးရေသည် ၈၁၆ မှ ၈၉၆ ကြားရှိမည်ဖြစ်ပြီး ဒီဇင်ဘာ ၂၀၂၆ တွင် ၈၈၈ ခန့် ရှိပါမည်။
> စိတ်ကြိုက်ဖန်တီးထားသော အခြေအနေ ၂ ခု (Stress-Test Scenarios):
> * Optimistic (အကောင်းမြင်လမ်းကြောင်း -၂၄%): ဒီဇင်ဘာ ၂၀၂၆ တွင် ၆၇၅ ခန့်သို့ ကျဆင်းမည်။
> * Pessimistic (အဆိုးမြင်လမ်းကြောင်း +၂၆%): ဒီဇင်ဘာ ၂၀၂၆ တွင် ၁,၁၂၃ ခန့်သို့ ပြန်တက်မည်။
> ⚠️ သတိပြုရန် - ဤ Scenarios များသည် ပုံသေရာခိုင်နှုန်းဖြင့် တွက်ထားသော Stress-test များသာဖြစ်ပြီး မူဝါဒကြောင့် ဖြစ်ပေါ်လာမည့် တိကျသော ရလဒ်များ မဟုတ်ပါ။ ၉၅% ယုံကြည်စိတ်ချရမှု အတိုင်းအတာ (PI) သည် ၅၃၉ မှ ၁,၂၃၇ အထိ ကျယ်ပြန့်သဖြင့် အစိုးရအနေဖြင့် ကိန်းဂဏန်းတစ်ခုတည်း မဟုတ်ဘဲ ဘောင်အတွင်း စဉ်းစားရပါမည်။

---

### Slide 10: The Regional Displacement Paradox
* **Slide File:** Slide 10 of 14  
* **Visual Anchor:** `slide_assets/task93_regional_divergence.png` (Paired bars: Downtown vs County PIT unsheltered).  
* **Target Timing:** 2:00 min (15:50 – 17:50)

#### 🎙️ English Speaking Points:
> "Slide 10 highlights what we call the Regional Displacement Paradox.
>
> Between January 2023 and January 2025, Downtown San Diego's share of countywide unsheltered homelessness plunged from 37.5% down to 14.9%. In absolute terms, downtown counts dropped from 1,939 to 851.
>
> Yet over that exact same window, the RTFH Countywide Unsheltered PIT count surged to an all-time record of 6,110 individuals in 2024, and remained high at 5,714 in 2025.
>
> This empirical decoupling is consistent with encampment displacement: individuals cleared from downtown commercial corridors were pushed into riverbeds, freeway borders, and neighboring jurisdictions.
>
> However, our data cannot confirm individual destinations because no tracking data exists. The finding is macro divergence: downtown reductions must not be celebrated as regional victories."

#### 🇲🇲 Burmese Explanation:
> ဆလိုက် ၁၀ သည် အလွန်အရေးကြီးသော Regional Displacement Paradox (ဒေါင်းတောင်းတွင် လူနည်းသွားသော်လည်း နယ်မြေတစ်ခုလုံးတွင် ပိုများလာသော ဆန့်ကျင်ဘက်ဖြစ်စဉ်) ဖြစ်သည်။
> ၂၀၂၃ မှ ၂၀၂၅ အတွင်း Downtown ၏ ဝေစုသည် ၃၇.၅% မှ ၁၄.၉% သို့ ထိုးဆင်းသွားခဲ့သည်။ ဒေါင်းတောင်းတွင် ၁,၉၃၉ မှ ၈၅၁ သို့ ကျဆင်းခဲ့သည်။
> သို့သော် တစ်ခရိုင်လုံး အတိုင်းအတာဖြင့် ၂၀၂၄ ခုနှစ်တွင် ၆,၁၁၀ အထိ သမိုင်းတစ်လျှောက် အမြင့်ဆုံး စံချိန်တင်ခဲ့သည်။
> ဆိုလိုသည်မှာ ဒေါင်းတောင်းမှ လူများ အိုးမဲ့အိမ်မဲ့ဘဝမှ လွတ်မြောက်သွားခြင်းမဟုတ်ဘဲ အခြားမြို့နယ်များနှင့် ချောင်းကမ်းပါးများဆီသို့ ရွှေ့ပြောင်းသွားခြင်း (Displacement) ဖြစ်နိုင်ခြေကို ညွှန်ပြနေသည်။ သို့သော် လူတစ်ဦးချင်း လိုက်လံမှတ်တမ်းတင်ထားခြင်း မရှိသဖြင့် အကြောင်းရင်းမှန်ဟု အတည်မပြုဘဲ ကိန်းဂဏန်းကွဲပြားမှု (Divergence) အဖြစ်သာ အစီရင်ခံရပါမည်။

---

### Slide 11: County Estimation Model & The 4 Communication Rules
* **Slide File:** Slide 11 of 14  
* **Visual Anchor:** Policy Regime OLS Specification Box + The 4 Mandatory Public Communication Rules Card.  
* **Target Timing:** 2:00 min (17:50 – 19:50)

#### 🎙️ English Speaking Points:
> "On Slide 11, we address estimating countywide unsheltered homelessness from downtown counts.
>
> First, a constant-ratio model fails completely. One-Way ANOVA across regimes gives F = 66.51, p = 0.0002, η² = 0.964, and Pearson r is -0.061 over eight paired years. Downtown is not a constant fixed fraction of the county.
>
> Our best model is an OLS regression with a post-ordinance policy regime shift:
> $$Y = 4,513.26 + 0.1859 \cdot X + 1,225.04 \cdot D_{\text{post}}$$
> This model achieves an R² of 0.504 and a LOOCV MAPE of 14.9%. Because N = 8, statistical power is low (23%), and neither slope (p = 0.78) nor regime (p = 0.075) reaches 5% significance.
>
> Our current estimate is **5,900 [95% PI: 3,900 to 8,000]**—a margin of ±2,050 individuals (±35%) using Student's t with 5 degrees of freedom.
>
> Because of this wide uncertainty, we established **The 4 Public Communication Rules**:
> 1. **No Single-Point Precision:** Never state raw numbers like '5,921'.
> 2. **Mandate Rounding:** Always round to the nearest 100 (e.g., '5,900').
> 3. **Always Publish the 95% Interval:** '5,900 [3,900 to 8,000]'.
> 4. **Mandatory Regime Disclosure:** State clearly that the estimate derives from downtown counts and assumes the post-July 2023 enforcement environment continues."

#### 🇲🇲 Burmese Explanation:
> ဆလိုက် ၁၁ တွင် ခရိုင်တစ်ခုလုံး အိုးမဲ့အိမ်မဲ့အရေအတွက်ကို Downtown ဒေတာမှ ခန့်မှန်းသော မော်ဒယ်ကို ရှင်းပြပါ။
> Constant-ratio (ပုံသေအချိုး) သုံးပါက ၉၆% အထိ မှားနိုင်ကြောင်း ANOVA အရ တွေ့ရသည်။
> ကျွန်ုပ်တို့ တည်ဆောက်ထားသော Policy Regime OLS မော်ဒယ်မှာ $Y = 4513.26 + 0.1859 \cdot X + 1225.04 \cdot D_{\text{post}}$ ဖြစ်ပြီး $R^2 = 0.504$ ရှိသည်။ စစ်တမ်းနှစ် ၈ နှစ်သာရှိ၍ $N=8$ ဖြစ်သဖြင့် စာရင်းအင်းစွမ်းအား (Power) နည်းပြီး predictor များမှာ p < 0.05 မရောက်ပါ။ ထို့ကြောင့် ခန့်မှန်းချက်သည် **၅,၉၀၀ [၃,၉၀၀ မှ ၈,၀၀၀ ကြား]** ဟူ၍ အနားသတ် ±၃၅% အထိ ကျယ်ပြန့်သည်။
>
> ⚠️ ထို့ကြောင့် ပြည်သူသို့ ထုတ်ပြန်ရာတွင် **မဖြစ်မနေ လိုက်နာရမည့် စည်းမျဉ်း ၄ ချက် (The 4 Rules)** ကို တင်းကျပ်စွာ ပြဋ္ဌာန်းထားသည်-
> စည်းမျဉ်း ၁ - အတိအကျ နံပါတ်တစ်ခုတည်း (ဥပမာ ၅,၉၂၁) မထုတ်ပြန်ရ။
> စည်းမျဉ်း ၂ - အနီးဆုံး ရာဂဏန်းသို့ အမြဲတမ်း ပတ်လည်ပြုရမည် (ဥပမာ ၅,၉၀၀)။
> စည်းမျဉ်း ၃ - ၉၅% ယုံကြည်စိတ်ချရမှု ဘောင်ကို အမြဲတမ်း ပူးတွဲဖော်ပြရမည် [၃,၉၀၀ မှ ၈,၀၀၀]။
> စည်းမျဉ်း ၄ - ဤခန့်မှန်းချက်သည် ဒေါင်းတောင်းစစ်တမ်းအပေါ် အခြေခံပြီး ၂၀၂၃ ဇူလိုင်နောက်ပိုင်း ဥပဒေတင်းကျပ်မှု ဆက်ရှိနေသည်ဟု ယူဆထားကြောင်း ထုတ်ဖော်ပြောကြားရမည်။

---

### Slide 12: Municipal Policy Action Roadmap (Memo R1–R8)
* **Slide File:** Slide 12 of 14  
* **Visual Anchor:** 3-Column Roadmap (Immediate 0–3 mo, Medium 6–12 mo, Long 1–3 yr).  
* **Target Timing:** 1:30 min (19:50 – 21:20)

#### 🎙️ English Speaking Points:
> "Slide 12 translates our findings into actionable recommendations, aligned directly with our Strategic Recommendations Memo:
> * **Immediate Action (0–3 Months):**
>   * **R1:** Use persistent hotspot blocks (16th–17th & Imperial and I-5 ramps) as a coordinated outreach shortlist.
>   * **R2:** Plan with ranges under Rules 1–4 across all municipal and media releases.
>   * **R3:** Clarify boundary scope—always state whether a figure covers the 261-block core or expanded 382-block footprint.
> * **Medium-Term (6–12 Months):**
>   * **R4:** Require DSDP to publish complete monthly component data (individuals, tents, vehicles) with consistent quadrant math.
>   * **R5:** Test the displacement hypothesis directly through regional outreach tracking.
>   * **R6:** Re-run the forecast and county model annually upon RTFH PIT release.
>   * **R7:** Replace synthetic shelter-capacity placeholders with administrative Housing Inventory Count data.
> * **Long-Term (1–3 Years):**
>   * **R8:** Digitize the remaining ~78 monthly block maps to enable true seasonal and post-ordinance spatial panel econometrics."

#### 🇲🇲 Burmese Explanation:
> ဆလိုက် ၁၂ တွင် မဟာဗျူဟာ မူဝါဒအကြံပြုချက် ၈ ချက် (R1 မှ R8) ကို ကာလ ၃ ခု ခွဲခြားတင်ပြပါ-
> * ချက်ချင်းဆောင်ရွက်ရန် (၀-၃ လ): R1 - ဟော့စပေါ့ ၅ ခုသို့ ကွင်းဆင်းကူညီမှု ဦးတည်ရန်၊ R2 - နံပါတ်တစ်ခုတည်းမပြောဘဲ Range ဖြင့်သာ အစီရင်ခံရန် (Rules 1-4)၊ R3 - ၂၆၁ ဘလောက်လား ၃၈၂ ဘလောက်လား ဧရိယာအတိုင်းအတာကို အမြဲထုတ်ဖော်ရန်။
> * ကာလလတ် (၆-၁၂ လ): R4 - DSDP မှ tent, vehicle အစုံအလင် လစဉ် ထုတ်ပြန်ပေးရန်၊ R5 - ဒေါင်းတောင်းမှ ရွှေ့ပြောင်းသွားသူများကို အခြားမြို့နယ်များနှင့် ပူးပေါင်း၍ တိုက်ရိုက် စောင့်ကြည့်စစ်တမ်းကောက်ရန်၊ R6 - နှစ်စဉ် PIT အသစ်ထွက်တိုင်း မော်ဒယ်များကို ပြန်လည်မွမ်းမံရန်၊ R7 - စမ်းသပ်ထားသော shelter data များကို အစိုးရတရားဝင် HIC ဒေတာဖြင့် အစားထိုးရန်။
> * ကာလရှည် (၁-၃ နှစ်): R8 - ကျန်ရှိနေသော လစဉ် ဘလောက်မြေပုံ ၇၈ စောင်ခန့်ကို ဒစ်ဂျစ်တယ်ဒေတာအဖြစ် အပြီးသတ် ပြောင်းလဲရန် (ဒါသည် အရေးကြီးဆုံး ဒေတာရင်းနှီးမြှုပ်နှံမှု ဖြစ်သည်)။

---

### Slide 13: Interactive Decision-Support Dashboard
* **Slide File:** Slide 13 of 14  
* **Visual Anchor:** 7 Specialized Dashboard Tabs Feature Matrix & Deployment SLA Card.  
* **Target Timing:** 1:00 min (21:20 – 22:20)

#### 🎙️ English Speaking Points:
> "Slide 13 showcases our operational decision-support tool deployed in Streamlit across seven specialized modules:
> * **Tab 1: Historical Trends:** Full 9-year series with multiplier regime shading.
> * **Tab 2: 12-Month Forecast:** 2026 prospective projections and scenario toggles.
> * **Tab 3: Hotspot Surveillance:** Interactive Folium choropleth with 261/382 footprint filters.
> * **Tab 4: Neighborhood Deep-Dive:** STL decomposition and Kruskal-Wallis significance.
> * **Tab 5: County Estimation Calculator:** Automated calculator strictly enforcing Rules 1–4.
> * **Tab 6: Methodology & Governance:** Data audits, QA flags, and multiplier documentation.
> * **Tab 7: Anomaly Surveillance:** Shewhart control charts and CUSUM early-warning monitoring.
>
> The application is live at `https://downtown-sd-homelessness.streamlit.app`, backed by 46 passing pytest unit tests and sub-second caching."

#### 🇲🇲 Burmese Explanation:
> ဆလိုက် ၁၃ တွင် တည်ဆောက်ထားသော Streamlit Dashboard ရှိ Tab ၇ ခုကို ရှင်းပြပါ-
> Tab 1 (သမိုင်းကြောင်းလမ်းကြောင်း)၊ Tab 2 (၁၂ လ ခန့်မှန်းချက်)၊ Tab 3 (ဟော့စပေါ့ မြေပုံစောင့်ကြည့်ရေး)၊ Tab 4 (ရပ်ကွက်အလိုက် ခွဲခြမ်းစိတ်ဖြာမှု)၊ Tab 5 (ခရိုင်ခန့်မှန်းချက် ဂဏန်းပေါင်းစက် - Rules 1-4 အလိုအလျောက်လိုက်နာသည်)၊ Tab 6 (သုတေသနနည်းလမ်းများနှင့် ဒေတာစစ်ဆေးချက်)၊ Tab 7 (ပုံမှန်မဟုတ်သော အခြေအနေများ စောင့်ကြည့်သတိပေးစနစ် - Shewhart / CUSUM)။
> Pytest ယူနစ်တက်စ် ၄၆ ခုစလုံး အောင်မြင်ထားပြီး အွန်လိုင်းတွင် အချိန်မရွေး အသုံးပြုနိုင်ကြောင်း တင်ပြပါ။

---

### Slide 14: Executive Synthesis & Strategic Next Steps
* **Slide File:** Slide 14 of 14  
* **Visual Anchor:** 3 Takeaway Pillar Cards (Evidence-Based Allocation / Regional Accountability / Data Investments).  
* **Target Timing:** 1:00 min (22:20 – 23:20)

#### 🎙️ English Speaking Points:
> "To conclude on Slide 14:
> 1. **Evidence-Based Budgeting:** Move away from seasonal budget fluctuations. Lock investments into year-round shelter capacity and focused hygiene on the top persistent South East Village blocks.
> 2. **Regional Systems Reform:** Acknowledge the regional divergence. Localized enforcement clears visible sidewalks, but regional unsheltered numbers reached historic highs. True solutions require regional shelter capacity and coordinated intake.
> 3. **High-Value Data Investments:** Prioritize digitizing the remaining ~78 monthly block maps (Recommendation R8) and retraining the policy-regime model annually.
>
> Thank you, Adir, and team. I am now open to your questions."

#### 🇲🇲 Burmese Explanation:
> နောက်ဆုံးဆလိုက်တွင် အနှစ်ချုပ် ၃ ချက်ဖြင့် နိဂုံးချုပ်ပါ-
> ၁။ ရာသီအလိုက် ဘတ်ဂျက်အတက်အကျ မလုပ်ဘဲ တစ်နှစ်ပတ်လုံး အိပ်ဆောင်များနှင့် ဟော့စပေါ့များသို့ တသမတ်တည်း ထောက်ပံ့ရန်။
> ၂။ ဒေါင်းတောင်းတွင် လူနည်းသွားသော်လည်း နယ်မြေတစ်ခုလုံးတွင် မကျသေးသဖြင့် ခရိုင်အဆင့် ပူးပေါင်းဆောင်ရွက်မှု မဖြစ်မနေ လိုအပ်ကြောင်း အသိအမှတ်ပြုရန်။
> ၃။ အရေးအကြီးဆုံး ဒေတာရင်းနှီးမြှုပ်နှံမှုဖြစ်သော ကျန်ရှိသည့် မြေပုံ ၇၈ စောင်ခန့်ကို ဒစ်ဂျစ်တယ်ပြောင်းလဲရန် (R8)။
> ထို့နောက် မေးခွန်းများကို ဝမ်းမြောက်စွာ ဖြေကြားရန် ဖိတ်ခေါ်ပါ။
