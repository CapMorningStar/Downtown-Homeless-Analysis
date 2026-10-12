# Master Bilingual Glossary: English – Burmese (မြန်မာဘာသာ)
## Downtown San Diego Homeless Population Analysis

> **Source of truth / အချက်အလက် အရင်းအမြစ်:** ဤဖိုင်ရှိ ကိန်းဂဏန်းအားလုံးကို `docs/FullTechnicalReport.md` (Version 3.0, October 2026)၊ `docs/Ensemble_PerformanceReport.md`၊ `docs/AnomalyDetection_Methodology.md` နှင့် `docs/MultiSource_DataDocumentation.md` တို့မှ တိုက်ရိုက် ယူထားပါသည်။ ကိန်းဂဏန်း တစ်ခုခု မသေချာပါက ထိုအစီရင်ခံစာများကိုသာ ပြန်ကြည့်ပါ။

ဤဝေါဟာရကျမ်းကို NotebookLM တွင် Episode ဖိုင်များနှင့်အတူ upload လုပ်ပါ။ အင်္ဂလိပ် နည်းပညာ ဝေါဟာရကို မူရင်းအတိုင်း ထားပြီး မြန်မာလို ရှင်းပြထားပါသည်။

---

## ၁။ ဒေတာ နှင့် စစ်တမ်း ဝေါဟာရများ (Data & Survey Terms)

1. **DSDP Clean & Safe Monthly Count (လစဉ် ညဘက် လမ်းပေါ် စစ်တမ်း)**
   * Downtown San Diego Partnership က မြို့လယ်ခေါင်တွင်သာ လစဉ် တစ်ည ရေတွက်သော စစ်တမ်း။ ဤစီမံကိန်းတွင် **January 2017 – December 2025 (လ ၁၀၈ လ၊ ထုတ်ပြန်ပြီး ၁၀၄ လ)** ကို အသုံးပြုသည်။
2. **RTFH Point-in-Time (PIT) Count (နှစ်စဉ် ကောင်တီ တစ်ညတည်း သန်းခေါင်စာရင်း)**
   * Regional Task Force on Homelessness က ဇန်နဝါရီလ နှောင်းပိုင်းတွင် ကောင်တီတစ်ခုလုံး တစ်ညတည်း ရေတွက်ခြင်း။ စီမံကိန်းတွင် **paired years ၈ နှစ်** (2017–2020 နှင့် 2022–2025) ရှိသည်။ 2021 unsheltered count ကို ဖျက်သိမ်းခဲ့သည်။
3. **Adjusted Count & Multiplier (ချိန်ညှိထားသော အရေအတွက်နှင့် မြှောက်ဖော်ကိန်း)**
   * Adjusted count = individuals + (tent multiplier × tents) + (vehicle multiplier × vehicles)။
   * Multiplier regimes: PRE2017 (2.00 / 2.00)၊ APR2017 (1.75 / 1.66)၊ MAY2018 နှင့် POST2020 (1.75 / 2.03)။
   * Component data (individuals/tents/vehicles ခွဲထားမှု) သည် **January 2018** မှသာ ရှိသည်။
4. **Data Validation (ဒေတာ မှန်ကန်ကြောင်း စစ်ဆေးခြင်း)**
   * 45-cell sample တွင် published cells ၄၁ ခုအနက် ၄၀ ခု မူရင်း PDF နှင့် ကိုက်ညီ (97.6%)။ October 2026 full re-check တွင် neighborhood monthly totals ၉၄၅ ခုလုံး ကိုက်ညီသည်။
5. **Source Correction (မူရင်း အမှား ပြင်ဆင်ချက်)**
   * ဥပမာ - 2019 East Village quadrant cells ၄၈ ခုသည် 2020 တန်ဖိုးများကို ကူးထားခြင်း ဖြစ်နေသဖြင့် January 2020 report ပါ 2019 breakout ဖြင့် အစားထိုးခဲ့သည်။ Neighborhood totals များကို မထိခိုက်ခဲ့ပါ။

---

## ၂။ စာရင်းအင်း နှင့် အချိန်စီးရီး ဝေါဟာရများ (Statistics & Time-Series Terms)

6. **Time-Series Decomposition / STL (အချိန်စီးရီး ခွဲခြမ်းခြင်း)**
   * ဒေတာကို trend (ရေရှည် လမ်းကြောင်း)၊ seasonal (ရာသီအလိုက်)၊ residual (ကျန်ရှိ ဆူညံမှု) ဟူ၍ ခွဲထုတ်ခြင်း။ Overall series ၏ seasonal strength မှာ **0.07** သာ ဖြစ်သည် (0–1 စကေး)။
7. **Seasonality (ရာသီအလိုက် အတက်အကျ)**
   * လအလိုက် ပုံမှန် ထပ်ခါထပ်ခါ ဖြစ်သော ပုံစံ။
8. **Kruskal-Wallis Test (ကရပ်စကယ်-ဝေါလစ် စမ်းသပ်မှု)**
   * ပုံမှန်ဖြန့်ဝေမှု (normal distribution) မလိုအပ်သော non-parametric test။ လ ၁၂ လ၏ တန်ဖိုးများ သိသိသာသာ ကွဲပြားခြင်း ရှိ/မရှိ စစ်သည်။
   * ရလဒ်: **series ၉ ခုအနက် ၈ ခုတွင် significant seasonality မရှိ။** Overall series: **H = 2.66, p = 0.995**။ Marina တစ်ခုသာ significant (H = 19.88, p = 0.047) ဖြစ်ပြီး ANOVA ဖြင့် စစ်သောအခါ မ significant ပါ (p = 0.162)။
9. **Structural Break & Chow Test (ဖွဲ့စည်းပုံ အချိုးအကွေ့ နှင့် ချော့ စမ်းသပ်မှု)**
   * သတ်မှတ်ထားသော ရက်စွဲတစ်ခုတွင် level (အဆင့်) သို့မဟုတ် trend (လမ်းကြောင်း) ရုတ်တရက် ပြောင်းသွားခြင်း ရှိ/မရှိ စစ်သည့် regression test။
   * စစ်ခဲ့သော ရက်စွဲများ: April 2017၊ May 2018၊ **COVID-19 onset (March 2020)**။ COVID တွင် series ၈ ခုအနက် ၇ ခု significant ဖြစ်သည်။
   * ⚠️ **July 2023 (Unsafe Camping Ordinance) ကို structural break အဖြစ် မစစ်ခဲ့ပါ။**
10. **Benjamini-Hochberg FDR Correction (မှားယွင်း ရှာဖွေတွေ့ရှိမှုနှုန်း ထိန်းချုပ်ခြင်း)**
    * Test အများအပြား တစ်ပြိုင်နက် လုပ်သောအခါ "ကံကောင်း၍ significant ဖြစ်သွားခြင်း" ကို လျှော့ချသည့် နည်းလမ်း။
11. **CUSUM Stability Test (စုဆောင်းပေါင်းလဒ် တည်ငြိမ်မှု စမ်းသပ်ချက်)**
    * Regression residuals များကို စုပေါင်း၍ model တည်ငြိမ်မှု ရှိ/မရှိ စစ်ခြင်း (Assignment 4)။ Series ၉ ခုအနက် ၇ ခု မတည်ငြိမ်။ (Assignment 10 ၏ CUSUM control chart နှင့် ရည်ရွယ်ချက် မတူပါ - အမှတ် ၂၆ ကိုကြည့်ပါ။)
12. **Stationarity – ADF & KPSS Tests (တည်ငြိမ်မှု စမ်းသပ်ချက်များ)**
    * Mean နှင့် variance သည် အချိန်နှင့်အမျှ တည်ငြိမ်ခြင်း။ Levels တွင် မတည်ငြိမ်သော်လည်း first difference ယူပြီးနောက် series ၉ ခုလုံး stationary ဖြစ်သည်။
13. **Autocorrelation – ACF / PACF (ကိုယ်တိုင် ဆက်စပ်မှု)**
    * ယခုလ တန်ဖိုးသည် ယခင်လများ၏ တန်ဖိုးနှင့် ဆက်စပ်မှု။ ARIMA model order ရွေးရာတွင် အသုံးပြုသည်။

---

## ၃။ ပထဝီဝင် ဝေါဟာရများ (Geospatial Terms)

14. **Block Grid (လမ်းဘလောက် ဇယားကွက်)**
    * `Downtown_BlockGrid.geojson` တွင် ဘလောက် **382** ခု ရှိသည်။ Polygon ၃၈၂ ခုလုံး valid ဖြစ်ပြီး overlap မရှိ။
15. **Footprint Expansion (စစ်တမ်း နယ်နိမိတ် ချဲ့ထွင်ခြင်း)**
    * **2022** တွင် ဘလောက် **121** ခု ထပ်တိုးခဲ့သည် - Golden Hill (52)၊ Barrio Logan (35)၊ Sherman Heights (34)။
    * ထပ်တိုးဘလောက်များသည် post-2021 count date ၅ ခုတွင် စုစုပေါင်း၏ **3.7% မှ 32.8%** အထိ ပါဝင်သည်။
16. **Balanced Panel – 261 Blocks (မျှတသော ဘလောက် ၂၆၁ ခု panel)**
    * Digitized date တိုင်းတွင် ရေတွက်ခဲ့သော ဘလောက် ၂၆၁ ခုသာ သုံး၍ နှစ်အလိုက် တရားမျှတစွာ နှိုင်းယှဉ်ခြင်း။ ဤ panel ပေါ်တွင်ပင် 2021 မှ 2022 သို့ **71%** တိုးခဲ့သဖြင့် footprint ကြောင့်ရော တကယ့် တိုးလာမှုကြောင့်ပါ ဖြစ်သည်။
17. **Global Moran's I (ပထဝီဝင် အစုအဝေး တိုင်းတာချက်)**
    * နီးစပ်သော ဘလောက်များသည် ဆင်တူသော တန်ဖိုး ရှိ/မရှိ (clustering) တိုင်းသည်။ Digitized date **၁၂** ခုလုံးတွင် positive (0.063–0.239, permutation p ≤ 0.034)။
18. **Getis-Ord Gi\* (ဂီတစ်-အော့ဒ် ဂျီစတား - ဒေသတွင်း hotspot ရှာဖွေခြင်း)**
    * ဘလောက်တစ်ခုနှင့် ၎င်း၏ အိမ်နီးချင်းများ စုပေါင်း၍ ထူးခြားစွာ မြင့်နေခြင်း ရှိ/မရှိ စစ်သည်။ **95% နှင့် 99%** class နှစ်မျိုးသာ သုံးသည် (90% class မရှိပါ)။
    * အမြဲ hotspot ဖြစ်နေဆုံး: **16th St & Imperial Ave** (date ၁၂ ခုအနက် ၉ ခု)။ Top ten အားလုံး **South East Village** တွင် ရှိသည်။
19. **Hotspot Centroid Migration (hotspot ဗဟိုချက် ရွှေ့လျားမှု)**
    * Count-weighted centroid သည် 2018–2020 မှ 2022–2025 သို့ **ခန့်မှန်း ၁၂၀ မီတာ၊ bearing 160° (တောင်-တောင်-အရှေ့)** ရွေ့သည်။
    * ⚠️ ဤအရာသည် significant cluster များ ရှိရာနေရာကို ဖော်ပြခြင်းသာ ဖြစ်ပြီး **လူများ ရွှေ့ပြောင်းသွားခြင်းကို တိုင်းတာခြင်း မဟုတ်ပါ**။ Date ၁၂ ခုသာ ရှိ၍ follow-up လုပ်ရန် အရိပ်အမြွက်သာ ဖြစ်သည်။

---

## ၄။ နည်းစနစ် ပြောင်းလဲမှု ဝေါဟာရများ (Methodology Terms – Assignment 6)

20. **Theoretical vs. Observed Ratio (သီအိုရီ အချိုး နှင့် တကယ် တွေ့ရသော အချိုး)**
    * Multiplier ပြောင်းလဲမှုကြောင့်သာ ဖြစ်မည့် အပြောင်းအလဲ (theoretical) - April 2017: 0.964၊ May 2018: 1.007။
    * တကယ် လစဉ် ပြောင်းလဲမှု (observed) - 0.792 နှင့် 1.141။ ဆိုလိုသည်မှာ လစဉ် အတက်အကျသည် multiplier အကျိုးသက်ရောက်မှုထက် အများကြီး ပိုကြီးသည်။
21. **Constant-Methodology Series (နည်းစနစ် တစ်သမတ်တည်း စီးရီး)**
    * သမိုင်းဒေတာ အားလုံးကို POST2020 multipliers (1.75 / 2.03) သို့ ပြန်ညှိထားသော စီးရီး (`TimeSeries_ConstantMethodology.csv`)။ **Hybrid approach** ကို အကြံပြုသည် (pre-2020 mean gap +0.10%)။

---

## ၅။ ခန့်မှန်းချက် ဝေါဟာရများ (Forecasting Terms – Assignments 7 & 10)

22. **Walk-Forward / Expanding-Window Cross-Validation (အချိန်အစဉ်လိုက် တိုးချဲ့ စစ်ဆေးခြင်း)**
    * အတိတ်ဒေတာဖြင့်သာ train ပြီး နောက်ပိုင်း ကာလဖြင့် test လုပ်ခြင်း။ Fold ၅ ခု။ အနာဂတ် အချက်အလက် ပေါက်ကြားခြင်း (data leakage) ကို ကာကွယ်သည်။
23. **MAPE – Mean Absolute Percentage Error (ပျမ်းမျှ ရာခိုင်နှုန်း အမှား)**
    * 12-month horizon တွင် **XGBoost 38.3% နှင့် Holt-Winters 38.4%** - အလွန်နီးစပ်၍ statistically ခွဲမရ (fold SD ≈ 26–28 points)။ 1-month horizon တွင် **SARIMA 5.4%** ဖြင့် အကောင်းဆုံး။
24. **Prediction Interval (ခန့်မှန်းချက် အကွာအဝေး)**
    * Assignment 7 ၏ 2026 forecast intervals များကို Holt-Winters residual variance မှ တွက်ထားသဖြင့် **approximate** သာ ဖြစ်သည်။
    * Assignment 10 ensemble တွင် **conformal prediction** (distribution-free) ကို သုံးသည်။ 95% half-width **±607.9**။
    * County estimate ၏ 95% interval [3,900–8,000] ကို **Student's t (df = 5)** ဖြင့် တွက်သည် (conformal မဟုတ်ပါ)။
25. **Lag-1 Baseline / Persistence (ယခင်လ တန်ဖိုးကို ခန့်မှန်းချက်အဖြစ် သုံးခြင်း)**
    * Assignment 10 တွင် ဤရိုးရှင်းသော baseline (MAE 119.6) သည် stacked ensemble (MAE 248.0) ကို fold တိုင်းတွင် အနိုင်ရသည်။
26. **Ablation Study (feature အုပ်စု တစ်ခုချင်း ထည့်/ဖြုတ် စမ်းသပ်ခြင်း)**
    * 311၊ weather၊ economic features ထည့်ခြင်းဖြင့် MAE ပြောင်းလဲမှု −0.4% မှ +0.8% သာ။ Feature ၆၈ ခုလုံး ပါသော model သည် lags-only ထက် 1.6% ပိုဆိုးသည်။
27. **Stacking with NNLS (အလေးချိန် အနုတ်မရှိ ပေါင်းစပ်ခြင်း)**
    * Base models သုံးခု (LightGBM, BSTS, MLP) ကို weight ≥ 0 နှင့် ပေါင်းလဒ် = 1 ဖြင့် ပေါင်းသည်။ ရလဒ် - BSTS 0.812၊ MLP 0.188၊ LightGBM 0.000။

---

## ၆။ ကောင်တီ ခန့်မှန်းချက် ဝေါဟာရများ (County Estimation – Assignment 8)

28. **OLS with Policy-Regime Indicator (မူဝါဒ ကာလ ညွှန်ပြကိန်း ပါသော linear regression)**
    * Y = 4,513.26 + 0.1859·X + 1,225.04·D_post (D_post = 1 for PIT 2024, 2025)။
    * **R² = 0.504** (adjusted 0.306)။ Downtown slope p = 0.78၊ regime term p = 0.075 - **5% level တွင် မည်သည့် predictor မှ significant မဖြစ်ပါ** (N = 8)။
29. **LOOCV – Leave-One-Out Cross-Validation (တစ်နှစ်ချင်း ဖယ်၍ စစ်ဆေးခြင်း)**
    * Paired year ၈ နှစ်မှ တစ်နှစ်ကို ဖယ်ထား၊ ကျန် ၇ နှစ်ဖြင့် fit လုပ်၊ ဖယ်ထားသောနှစ်ကို ခန့်မှန်း။ Selected model: **RMSE 815, MAPE 14.9%**။
30. **Ratio Stability ANOVA (အချိုး တည်ငြိမ်မှု စမ်းသပ်ချက်)**
    * Downtown share သည် ကာလ ၃ ခုတွင် တည်ငြိမ်ခြင်း ရှိ/မရှိ - F = 66.51, p = 0.0002, **η² = 0.964**။ အချိုး မတည်ငြိမ်ပါ။
    * ⚠️ 0.964 သည် ANOVA ၏ η² ဖြစ်ပြီး model ၏ R² မဟုတ်ပါ။
31. **Statistical Power (စာရင်းအင်း စွမ်းအား)**
    * N = 8 ဖြင့် r = 0.5 ကို ရှာတွေ့နိုင်ခြေ **ခန့်မှန်း 23%** သာ။

---

## ၇။ မူမမှန်မှု စောင့်ကြည့်ရေး ဝေါဟာရများ (Anomaly Detection – Assignment 10)

32. **Shewhart Control Chart (ရှူးဟတ် အရည်အသွေး ထိန်းချုပ်ဇယား)**
    * 12-month rolling mean ကို center line ထား၊ **±2σ warning**၊ **±3σ critical action** limits။
33. **Tabular CUSUM (တဖြည်းဖြည်း လမ်းကြောင်းပြောင်းခြင်း ရှာဖွေရေး)**
    * Shewhart မမိသော သေးငယ်ပြီး ဆက်တိုက် ဖြစ်သော drift ကို ဖမ်းသည်။ **k = 0.5, h = 4.0**။
34. **Isolation Forest (အထီးကျန် သစ်တော - multivariate outlier ရှာဖွေရေး)**
    * Feature ၆၈ ခု ပေါင်းစပ်မှု ထူးဆန်းသော လများကို ရှာသည် (trees 150, contamination 0.08)။
35. **Anomaly Taxonomy (မူမမှန်မှု အမျိုးအစား ၄ မျိုး)**
    * Count Spike၊ Count Drop၊ Spatial Shift၊ Potential Data Quality Issue။
36. **Sensitivity / False Positive Rate / Precision (ထောက်လှမ်းမှု တိုင်းတာချက်များ)**
    * Month level - sensitivity **45.8%**၊ false positive rate **7.4%**၊ precision **68.8%**၊ F1 **0.55**။ Event level - benchmark ကာလ ၄ ခုလုံးကို အနည်းဆုံး တစ်ကြိမ် ထောက်လှမ်းမိသည် (4 of 4)။

---

## ၈။ အများပြည်သူ ဆက်သွယ်ရေး စည်းမျဉ်း ၄ ချက် (The 4 Public Communication Rules)

* **Rule 1 – Single-point precision မထုတ်ပြန်ရ:** "5,921" ကဲ့သို့ မဝိုင်းထားသော ကိန်းကို မထုတ်ပြန်ရ။
* **Rule 2 – အနီးဆုံး ရာဂဏန်းသို့ ဝိုင်းရမည်:** "5,900"။
* **Rule 3 – 95% prediction interval ကို အမြဲ ပြရမည်:** "5,900 [3,900 to 8,000]"။
* **Rule 4 – Policy regime ကို ဖော်ပြရမည်:** ဤခန့်မှန်းချက်သည် downtown counts မှ ဆင်းသက်လာပြီး **post-July 2023 Unsafe Camping Ordinance enforcement ပတ်ဝန်းကျင် ဆက်ရှိနေမည်ဟု ယူဆထားကြောင်း** ဖော်ပြရမည်။
