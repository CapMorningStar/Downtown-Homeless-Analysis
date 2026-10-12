# NotebookLM Audio Briefing — Episode 5
## အပိုင်း (၅) - Dashboard၊ Multi-Source စနစ် နှင့် မူမမှန်မှု စောင့်ကြည့်ရေး (Assignments 9.1 & 10)

> **NotebookLM customize prompt (copy & paste):**
> *"Create a deep-dive conversation in Burmese (မြန်မာဘာသာ) between two hosts about this briefing on the dashboard, the multi-source data system, the ensemble model, and anomaly detection. Keep technical terms in English (Streamlit, data ingestion, feature engineering, ablation study, stacking, conformal prediction, Shewhart chart, CUSUM, Isolation Forest, false positive rate) and explain each in Burmese. Highlight the honest negative results as a strength. Use only the numbers in this document."*

> **Source of truth:** `app.py`; `docs/MultiSource_DataDocumentation.md`; `docs/Feature_Library_Documentation.md`; `docs/Ensemble_PerformanceReport.md`; `docs/AnomalyDetection_Methodology.md` (all October 2026 corrected versions).

---

### ၁။ Assignment 9.1 - Interactive Dashboard (Streamlit)

* **Live URL:** https://downtown-sd-homelessness.streamlit.app
* **Tabs ၇ ခု** (`app.py`):
  1. **Historical Trends** - 2017–2025 လစဉ် counts၊ component toggles (individuals, tents, vehicles)။
  2. **12-Month Forecast** - 2026 forecasts၊ 80%/95% prediction bands၊ optimistic/pessimistic paths။
  3. **Hotspot Surveillance** - block-level map၊ count date ၁၂ ခု၊ balanced 261 vs full 382 footprint။
  4. **Neighborhood Deep-Dive** - neighborhood အလိုက် time-series decomposition။
  5. **County Estimation** - county estimate calculator (Rules 1–4 ပါ)။
  6. **Methodology & About** - နည်းစနစ် နှင့် ကန့်သတ်ချက်များ။
  7. **Anomaly Surveillance** - control charts၊ CUSUM၊ alert review form (Assignment 10)။

> 💡 **Presentation tip:** Live demo လုပ်ပါက Tab 1 (trend) → Tab 3 (16th & Imperial hotspot) → Tab 5 (5,900 [3,900–8,000]) → Tab 7 (alerts) အစဉ်အတိုင်း ပြပါ။

---

### ၂။ Task 10.1 - Multi-Source Data Ingestion (ဒေတာ အရင်းအမြစ် အများအပြား ပေါင်းစပ်ခြင်း)

**ရည်ရွယ်ချက်:** Downtown counts ကို ပြင်ပ အချက်အလက်များနှင့် လအလိုက် ပေါင်းစပ်၍ forecasting နှင့် anomaly detection အတွက် အသုံးပြုရန်။

**Output:** `data/MultiSource_Master_Monthly.csv` - **108 rows (2017-01 မှ 2025-12) × 40 columns**။

**ပြင်ပ ဒေတာ အရင်းအမြစ် ၅ ခု နှင့် ၎င်းတို့၏ အခြေအနေ (provenance):**

| Source | အခြေအနေ | ကန့်သတ်ချက် |
|---|---|---|
| **311 Get It Done** | City of San Diego open data - **real records** (DOWNTOWN community plan) | Encampment-type requests သည် **August 2018** မှသာ ရှိသည်။ `mean_resolution_days` သည် လ ၁၂၆ လအနက် ၃၂ လတွင် negative ဖြစ်နေ၍ **မယုံကြည်ရ** |
| **Weather** | Open-Meteo historical archive - **real daily data** | Offline fallback code ရှိသော်လည်း cached file သည် real data |
| **Events** (Padres, holidays, Comic-Con) | MLB Stats API cache + calendar rules - **real** | — |
| **Economics** | FRED နှင့် Zillow ZORI cached downloads | Semi-annual CPI ကို monthly သို့ interpolate လုပ်ထား |
| **Shelter capacity** | ⚠️ **Administrative data မဟုတ်ပါ** - code ထဲတွင် ရေးထားသော rounded placeholder timeline (1,350 / 1,750 / 2,100 …) | SDHC/RTFH Housing Inventory Count records ဖြင့် **အစားထိုးရမည်**။ ၎င်းကို သုံးသော feature/model ရလဒ်အားလုံး ဤကန့်သတ်ချက်ကို ဆက်ခံသည် |

* **အရေးကြီး correction (October 2026):** DSDP မထုတ်ပြန်ရသေးသော 2025 လ ၄ လကို ယခင်က **0** ဖြင့် ဖြည့်ခဲ့သဖြင့် downstream models များ ပျက်စီးခဲ့သည်။ ယခု ၎င်းတို့ကို **missing** အဖြစ် ထားပြီး `downtown_count_released = 0` ဖြင့် အမှတ်အသား ပြုထားသည်။

> ⚠️ **ပြောရာတွင် သတိပြုရန်:** DSA က "Where did shelter capacity data come from?" ဟု မေးလျှင် - "It's a placeholder timeline, not administrative data. Replacing it with SDHC/RTFH Housing Inventory Count records is the first item on the roadmap." ဟု ရိုးသားစွာ ဖြေပါ။

---

### ၃။ Task 10.2 - Feature Engineering (အင်္ဂါရပ် တည်ဆောက်ခြင်း)

* Multi-source dataset မှ **features 68 ခု** (domain families ၇ ခု) တည်ဆောက်ခဲ့သည် (`data/FeatureMatrix_Comprehensive_68.csv`)။
* **Leakage ကာကွယ်ခြင်း:** calendar မဟုတ်သော feature အားလုံးကို အနည်းဆုံး ၁ လ (t−1) lag လုပ်ထားသည်။
* Model-ready training subset - **92 published months** (2018–2025 ၏ 96 လ ထဲမှ မထုတ်ပြန်ရသေးသော ၄ လ နုတ်)။

> ⚠️ Feature library doc တွင် Random Forest **in-sample** R² = 0.9631 ဟု ပါသည်။ ၎င်းသည် in-sample (train data ပေါ်တွင်ပင် စစ်ခြင်း) ဖြစ်၍ forecasting accuracy ကို **မဖော်ပြပါ**။ Out-of-fold ရလဒ်များ (အောက်တွင်) ကိုသာ ကိုးကားပါ။

---

### ၄။ Task 10.3 - Ensemble Prediction System (Model ပေါင်းစပ်စနစ်)

**Base models သုံးမျိုး:**
1. **LightGBM** - gradient boosted trees
2. **BSTS** - Bayesian structural time series (state-space, Kalman filter)
3. **MLP** - regularized neural network (top 5 features သာ သုံး)

**Stacking:** Non-negative least squares (weight ≥ 0, ပေါင်းလဒ် = 1)။ ရလဒ် weights - **BSTS 0.812, MLP 0.188, LightGBM 0.000**။

**Validation:** 5 annual expanding-window folds (test years 2021–2025)၊ published test months **56** လ။

**Overall out-of-fold performance:**

| Model | MAE | RMSE | MAPE | R² |
|---|---:|---:|---:|---:|
| **Lag-1 baseline (last month's value)** | **119.6** | **150.0** | **10.6%** | **0.842** |
| BSTS | 223.6 | 285.9 | 19.3% | 0.424 |
| Neural net (MLP) | 238.3 | 312.6 | 18.8% | 0.312 |
| Stacked ensemble | 248.0 | 323.2 | 20.0% | 0.264 |
| LightGBM | 278.5 | 366.2 | 21.4% | 0.056 |

**ရိုးသားသော ရလဒ် (honest negative results):**
* **Lag-1 baseline ("ယခုလ = ယခင်လ") သည် ensemble ကို fold တိုင်းတွင် အနိုင်ရသည်။**
* Ensemble သည် ၎င်း၏ အကောင်းဆုံး base model (BSTS) ကိုပင် မကျော်ပါ။

**Ablation study (feature အုပ်စု တစ်ခုချင်း ထည့်ခြင်း, LightGBM):**

| Stage | Features | CV MAE | Stage 0 နှင့် နှိုင်းယှဉ် |
|---|---:|---:|---|
| 0 - Target lags only | 2 | 266.7 | — |
| 1 - + 311 signals | 7 | 265.6 | +0.4% better |
| 2 - + weather | 11 | 267.9 | 0.4% worse |
| 3 - + economic / rent | 17 | 264.5 | +0.8% better |
| 4 - Full multi-source | 68 | 271.0 | **1.6% worse** |

* ပြောင်းလဲမှုများ (2% အောက်) သည် fold-to-fold variation ထက် အများကြီး သေးသဖြင့် **မည်သည့် data source မှ တိုင်းတာနိုင်သော predictive benefit မပြပါ**။
* **ဘာကြောင့်လဲ:** လစဉ် observations ~90 သာ ရှိ၍ features အပိုများသည် variance ကိုသာ တိုးစေသည် (overfitting)။

**Conformal prediction intervals:**
* Out-of-fold residuals ဖြင့် calibrate လုပ်သည် - normal distribution ယူဆချက် မလို။
* 95% half-width **±607.9**၊ empirical coverage 92.9%–98.2%။
* ⚠️ Intervals များ **အလွန်ကျယ်** ပြီး residual ၅၆ ခုတည်းဖြင့် calibrate နှင့် evaluate နှစ်ခုလုံး လုပ်ထားသဖြင့် true out-of-sample coverage နိမ့်နိုင်သည်။

**2026 ensemble forecast:** လစဉ် ~866–897၊ 95% interval ~280 မှ ~1,500။ Assignment 7 forecast (816–896) နှင့် ကိုက်ညီသည်။

**နိဂုံး:** Lag-1 baseline (သို့မဟုတ် Assignment 7 models) ကို operational forecast အဖြစ် ဆက်သုံးသင့်သည်။ External data streams ၏ တန်ဖိုးမှာ **context ကို ဖော်ပြခြင်း** ဖြစ်ပြီး accuracy တိုးစေခြင်း မဟုတ်ပါ။

> 💡 **ဤအရာသည် အားနည်းချက် မဟုတ်ဘဲ အားသာချက် ဖြစ်သည်။** Senior data scientists များသည် "complex model က simple baseline ကို မနိုင်ကြောင်း ရိုးသားစွာ report လုပ်နိုင်သူ" ကို အထူး တန်ဖိုးထားသည်။

---

### ၅။ Task 10.4 - Anomaly Detection & Automated Alerting (မူမမှန်မှု စောင့်ကြည့်ရေး)

**ရည်ရွယ်ချက်:** လစဉ် count အသစ် ထွက်လာတိုင်း ပုံမှန်ထက် ထူးခြားခြင်း ရှိ/မရှိ အလိုအလျောက် စစ်ပြီး alert ပို့ရန်။

**(က) Statistical engine**
* **Shewhart control chart:** 12-month rolling mean ကို center line ထား။
  * **±2σ** = warning (WARNING_HIGH / WARNING_LOW)
  * **±3σ** = critical action (CRITICAL_HIGH / CRITICAL_LOW)
* **Tabular CUSUM:** Shewhart မမိသော သေးငယ်ပြီး ဆက်တိုက် ဖြစ်သော drift ကို ဖမ်းသည်။ **k = 0.5** (slack)၊ **h = 4.0** (decision threshold)။ Alarm ပြီးလျှင် accumulator ကို 0 သို့ reset လုပ်သည်။

**(ခ) Model-based engine**
* **Isolation Forest:** features 68 ခုပေါ်တွင် ထူးဆန်းသော ပေါင်းစပ်မှုများ ရှာသည် (trees 150, contamination 0.08)။
* **Conformal residual detector:** ensemble prediction error > **607.89** ဖြစ်လျှင် flag လုပ်သည်။

**(ဂ) Anomaly types ၄ မျိုး**
1. **Count Spike** - ရုတ်တရက် တက်ခြင်း
2. **Count Drop** - ရုတ်တရက် ကျခြင်း
3. **Spatial Shift** - neighborhood အကြား ပြန့်ကျဲ/စုပြုံမှု ပြောင်းခြင်း
4. **Potential Data Quality Issue** - zero counts၊ မထုတ်ပြန်ရသေးသော လများ စသည်

**(ဃ) Historical benchmark validation**

| Benchmark event | Window | Detected months | Rate |
|---|---|---:|---:|
| COVID-19 period | Apr–Sep 2020 | 1 of 6 | 16.7% |
| 2022 surge & footprint expansion | May–Dec 2022 | 2 of 8 | 25.0% |
| Peak & Unsafe Camping Ordinance | Jun–Aug 2023 | 3 of 3 | 100.0% |
| Post-ordinance contraction | Oct 2023 – Apr 2024 | 5 of 7 | 71.4% |

**Accuracy metrics (monitored months 92 လ):**
* **Event level:** benchmark ကာလ ၄ ခုလုံးကို အနည်းဆုံး တစ်ကြိမ် ထောက်လှမ်းမိသည် (**4 of 4**)။
* **Month level:**

| Metric | Value |
|---|---:|
| Sensitivity | 45.8% |
| False positive rate | 7.4% |
| Precision | 68.8% |
| F1 | 0.55 |
| Flagged months | 16 of 92 (+ data-gap alerts 4 ခု) |

* ⚠️ Benchmark windows များကို **နောက်မှ (after the fact)** သိပြီးသား events များမှ သတ်မှတ်ထားသဖြင့် ဤ metrics များသည် detectors များ ကြီးမားသော known shifts များကို တုံ့ပြန်ကြောင်းသာ ပြသည်။ **အနာဂတ် မသိသော events အပေါ် စွမ်းဆောင်ရည်ကို မခန့်မှန်းနိုင်ပါ။**
* ⚠️ "TPR 100%" ဟု ယခင် version က ပြောခဲ့သည်မှာ event-level rate ဖြစ်၍ month-level metrics များနှင့် ရောမပြောရ။

**(င) Alert delivery နှင့် automation**
* Slack (Block Kit) နှင့် email (HTML/plain-text) ဖြင့် ပို့နိုင်သည် - `python anomaly_detection.py --send`။ Channel ကို environment variables ဖြင့်သာ configure လုပ်သည် (repository ထဲ မထားပါ)။
* Alert တစ်ခုကို **တစ်ကြိမ်သာ** ပို့သည် (`notified_at`)။ Alert အားလုံး `data/Alerts_History.csv` တွင် audit trail အဖြစ် သိမ်းသည် (NEW → REVIEWED → DISMISSED)။
* `scripts/run_scheduled_anomaly_detection.sh` ဖြင့် cron သို့မဟုတ် Airflow တွင် schedule လုပ်နိုင်သည်။
* Dashboard **Tab 7** တွင် control charts၊ CUSUM bars၊ alert review form နှင့် sensitivity sliders ပါသည်။

---

### ၆။ Testing (စမ်းသပ်မှု)

* Repository ၏ **pytest suite - tests 46 ခု အားလုံး pass** (October 6, 2026 တွင် ပြန် run၍ အတည်ပြုပြီး)။
* Anomaly detection၊ ensemble၊ feature engineering၊ data ingestion၊ source corrections၊ county calculator နှင့် forecast logic တို့ကို cover လုပ်သည်။

---

### ၇။ DSA အဖွဲ့ရှေ့ ပြောရမည့် အဓိက အချက်များ (Key Talking Points)

* "Dashboard မှာ tabs 7 ခု ပါပြီး live ဖြစ်ပါတယ် - trends, forecasts, hotspots, neighborhoods, county calculator, methodology နဲ့ anomaly surveillance။"
* "Multi-source system မှာ 311, weather, events, economics နဲ့ shelter data ကို ပေါင်းခဲ့ပါတယ်။ Shelter capacity ကတော့ placeholder ဖြစ်လို့ HIC records နဲ့ အစားထိုးဖို့ လိုပါတယ်။"
* "Ensemble ကို ဆောက်ခဲ့ပေမဲ့ ရိုးရိုးသားသား ပြောရရင် last month's value baseline (MAE 119.6) က ensemble (MAE 248.0) ကို fold တိုင်းမှာ နိုင်ပါတယ်။ Ablation မှာ external data က accuracy ကို 2% ထက် ပိုမတိုးစေပါဘူး။ Data point ~90 ပဲ ရှိလို့ပါ။"
* "Anomaly system က Shewhart နဲ့ CUSUM ကို သုံးပြီး historical benchmark 4 ခုလုံးကို detect လုပ်နိုင်ပါတယ်။ Month-level false positive rate က 7.4% ပါ။ ဒါပေမဲ့ benchmarks က after-the-fact ဖြစ်လို့ future performance ကို guarantee မပေးပါဘူး။"
