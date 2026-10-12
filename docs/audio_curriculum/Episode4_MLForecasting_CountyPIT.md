# NotebookLM Audio Briefing — Episode 4
## အပိုင်း (၄) - ၁၂ လ ခန့်မှန်းချက် နှင့် ကောင်တီ ခန့်မှန်းချက် (Assignments 7 & 8)

> **NotebookLM customize prompt (copy & paste):**
> *"Create a deep-dive conversation in Burmese (မြန်မာဘာသာ) between two hosts about this briefing on forecasting and county estimation. Keep technical terms in English (walk-forward cross-validation, MAPE, SARIMA, Holt-Winters, XGBoost, Prophet, prediction interval, LOOCV, R-squared, p-value) and explain each in Burmese. Emphasize why honest uncertainty matters. Use only the numbers in this document."*

> **Source of truth:** `docs/FullTechnicalReport.md` §8, §9, §10 (v3.0); `data/Forecasts_12Month.csv`.

---

## အပိုင်း က - Assignment 7: ၁၂ လ ခန့်မှန်းချက် (12-Month Forecasting)

### ၁။ Validation design (model ကို မည်သို့ စစ်ခဲ့သနည်း)

* **Hold-out test:** 2025 (ထုတ်ပြန်ပြီး ၈ လသာ)။
* **Cross-validation:** **5-fold walk-forward** - training window ကို 2020 မှ 2024 အထိ တဖြည်းဖြည်း ချဲ့၍ နောက်ပိုင်းကာလဖြင့် test လုပ်သည်။
* **ဘာကြောင့် random K-fold မသုံးတာလဲ:** အချိန်စီးရီးတွင် random shuffle လုပ်လျှင် အနာဂတ် အချက်အလက်ဖြင့် အတိတ်ကို ခန့်မှန်းသလို ဖြစ်သွားသည် (**data leakage**)။ Walk-forward သည် လက်တွေ့ forecasting အခြေအနေကို တုပသည်။

**စမ်းသပ်ခဲ့သော models ငါးမျိုး:**
1. **Naive seasonal (t−12)** - "ယခုနှစ် ဤလ = ယမန်နှစ် ဤလ" ဟူသော အရိုးရှင်းဆုံး baseline။
2. **SARIMA** - ACF/PACF candidates ပတ်လည် grid search။
3. **Holt-Winters** - exponential smoothing (level + trend + seasonal)။
4. **Prophet** - multiplier changes နှင့် COVID တွင် changepoints သတ်မှတ်ထား။
5. **XGBoost** - lags 1, 2, 3, 6, 12 + rolling means + month terms၊ recursive forecasting။

### ၂။ ရလဒ်များ (Results)

**Table - Cross-validation MAPE (%), overall series; mean (SD) across 5 folds:**

| Model | 1-month | 3-month | 6-month | 12-month |
|---|---:|---:|---:|---:|
| SARIMA | **5.4** (4.1) | **14.3** (10.3) | **24.7** (20.9) | 39.6 (35.5) |
| Holt-Winters | 13.0 (9.2) | 17.6 (10.4) | 25.2 (18.2) | 38.4 (28.5) |
| XGBoost | 14.0 (8.9) | 19.9 (14.8) | 26.7 (18.5) | **38.3** (26.0) |
| Naive seasonal | 39.5 (31.9) | 40.1 (31.3) | 48.5 (35.4) | 51.7 (24.5) |
| Prophet | 42.9 (26.0) | 42.7 (26.0) | 51.3 (31.9) | 64.2 (35.4) |

**အဓိပ္ပာယ်:**
* **Short horizons (1–6 months):** **SARIMA** သည် ရှင်းရှင်းလင်းလင်း အကောင်းဆုံး။
* **12 months:** XGBoost (38.3%)၊ Holt-Winters (38.4%)၊ SARIMA (39.6%) တို့သည် **statistically ခွဲခြား၍ မရပါ** - fold-to-fold variation (26–36 points) သည် model အကြား ကွာခြားချက်ထက် အများကြီး ပိုကြီးသည်။ XGBoost ကို 12-month mean အနိမ့်ဆုံး ဖြစ်သဖြင့် overall series champion အဖြစ် ထားခဲ့သည်။
* **Prophet:** horizon တိုင်းတွင် အဆိုးဆုံး။ ၎င်း၏ fixed changepoints များတွင် 2022–2023 peak အနီး changepoint မရှိသဖြင့် တက်နေသော လမ်းကြောင်းကို ဆက်ဆွဲသွားသည်။
* **2025 hold-out (12-month horizon):** XGBoost MAPE **8.5%**၊ Holt-Winters 20.4%၊ SARIMA 22.8%။ ⚠️ သို့သော် **naive seasonal က 6.3%** ဖြင့် အကောင်းဆုံး ဖြစ်ခဲ့သည် - 2025 သည် 2024 ကို နီးကပ်စွာ ထပ်ခဲ့သောကြောင့်။ ထို့ကြောင့် single hold-out year ကို အလွန်အကျွံ အဓိပ္ပာယ် မကောက်ရ။

**Per-series champions:**
* XGBoost - overall, core six, East Village, City Center, Cortez, Outside Perimeter
* SARIMA - Columbia
* Prophet - Gaslamp, Marina
* ⚠️ Outside Perimeter ၏ CV MAPE သည် model တိုင်းအတွက် **500% ကျော်** သဖြင့် ၎င်း၏ forecasts ကို **မသုံးသင့်ပါ**။

> ⚠️ **ပြောရာတွင် သတိပြုရန်:** "XGBoost clearly won" ဟု မပြောပါနှင့်။ "At 12 months, XGBoost, Holt-Winters and SARIMA were statistically tied; XGBoost had the lowest mean so it was kept as champion. At short horizons SARIMA was clearly best." ဟု ပြောပါ။ (Slide deck တွင် ရှိသော 39.34% / 38.48% / 39.57% တို့သည် ဟောင်းနေသော ကိန်းများ ဖြစ်သည်။)

### ၃။ 2026 ခန့်မှန်းချက် (2026 Forecast, overall series)

`forecast_pipeline.py` မှ output (`data/Forecasts_12Month.csv`):

| Month | Forecast | 80% PI | 95% PI | Optimistic | Pessimistic |
|---|---:|---|---|---:|---:|
| Jan 2026 | 863 | 697–1,029 | 609–1,117 | 846 | 882 |
| Mar 2026 | 816 | 637–995 | 542–1,090 | 767 | 870 |
| Jun 2026 | 850 | 653–1,047 | 549–1,151 | 748 | 962 |
| Sep 2026 | 844 | 631–1,057 | 518–1,169 | 692 | 1,011 |
| Dec 2026 | 888 | 660–1,116 | 539–1,237 | 675 | 1,123 |

* Status-quo forecast range - **816–896 per month**။
* **Prediction intervals သည် approximate** ဖြစ်သည် - Holt-Winters residual variance ကို √(1 + 0.08(h−1)) ဖြင့် ချဲ့၍ တွက်သည်။ Champion model တစ်ခုချင်း၏ ကိုယ်ပိုင် error distribution မှ မဟုတ်ပါ။
* **Scenarios** သည် **fixed percentage paths** (လစဉ် −2% နှင့် +2.2%၊ month 12 တွင် −24% / +26%) ဖြစ်ပြီး **model-based scenarios မဟုတ်ပါ**။
* XGBoost ရလဒ်များသည် library version မတူလျှင် bit-for-bit မတူနိုင်ပါ - မတူသော environment တွင် ပြန် run လျှင် လစဉ် ~58 အထိ ပြောင်းနိုင်သည်။

> ⚠️ **ပြောရာတွင် သတိပြုရန်:** "800 shelter beds will bring counts to 670" ကဲ့သို့ မပြောပါနှင့် - optimistic path သည် −24% fixed path သာ ဖြစ်ပြီး shelter beds model မဟုတ်ပါ။

**Memo recommendation:** 12-month forecasts ကို **planning range** အဖြစ် သုံးပါ၊ target အဖြစ် မသုံးပါနှင့်။ နှစ်စဉ် CV ပြန် run ပြီး naive seasonal baseline ကို comparison တွင် ထားပါ (2025 hold-out တွင် အတိကျဆုံး ဖြစ်ခဲ့သဖြင့်)။

---

## အပိုင်း ခ - Assignment 8: ကောင်တီ ခန့်မှန်းချက် (County-Level Estimation)

### ၄။ မေးခွန်း နှင့် ဒေတာ

**မေးခွန်း:** "Downtown လစဉ် count ကို သုံး၍ PIT count နှစ်ခုကြားတွင် ကောင်တီ unsheltered အရေအတွက်ကို ခန့်မှန်းနိုင်သလား။"

* X = January downtown adjusted total၊ Y = county unsheltered PIT count။
* Paired years **၈ နှစ်** (2017–2020, 2022–2025)။ 2022 PIT ကို Omicron ကြောင့် **24 February** သို့ ရွှေ့ခဲ့၍ February downtown count နှင့် တွဲထားသည်။

### ၅။ ဆက်စပ်မှု (Relationship, Task 8.2)

* **Correlation:** Pearson r = **−0.061** (p = 0.886)၊ Spearman ρ = 0.214 (p = 0.610) - **ဆက်စပ်မှု မရှိသလောက်**။
* **Ratio stability ANOVA:** F = 66.51, p = 0.0002, **η² = 0.964** - downtown share သည် ကာလ ၃ ခုအကြား **မတည်ငြိမ်ပါ**။
* **Power:** N = 8 ဖြင့် r = 0.5 ကို ရှာတွေ့နိုင်ခြေ **~23%** သာ။

> ⚠️ **η² = 0.964 ကို R² ဟု ဘယ်တော့မှ မခေါ်ပါနှင့်။** ယခင် version (slide deck အပါအဝင်) တွင် ဤအမှား ရှိခဲ့သည်။

### ၆။ Models နှင့် validation (Task 8.3)

**Leave-one-year-out cross-validation (8 folds):**

| Model | RMSE | MAE | MAPE | Signed bias |
|---|---:|---:|---:|---:|
| **OLS + policy-regime indicator** | **815.3** | **721.2** | **14.9%** | −0.3% |
| OLS | 960.5 | 879.7 | 18.2% | +1.4% |
| OLS + time trend | 1,050.4 | 943.2 | 19.3% | −1.3% |
| Pooled ratio | 2,392.6 | 1,917.4 | 38.2% | +5.0% |
| Mean of ratios | 2,482.5 | 1,777.4 | 35.9% | +14.0% |
| Post-ordinance ratio | 3,142.6 | 1,976.4 | 42.2% | +39.3% |

**Selected model:** Y = 4,513.26 + 0.1859·X + 1,225.04·D_post (D_post = 1 for PIT 2024, 2025)

| Term | Estimate | p |
|---|---:|---:|
| Intercept | 4,513.26 | 0.002 |
| Slope (X) | 0.186 | **0.78** |
| D_post | 1,225.0 | **0.075** |

* **Fit:** **R² = 0.504**, adjusted R² = 0.306, residual SE 652 on 5 df။

**Caveats (ကန့်သတ်ချက်များ):**
* D_post = 1 ဖြစ်သော observations **နှစ်ခု** သာ ရှိ၍ regime term သည် ထိုနှစ်နှစ်အတွက် indicator နီးပါး ဖြစ်သည်။
* Model သည် post-2023 downtown–county divergence ကို **ဖော်ပြသည် (describes)**၊ ordinance က လူများကို displace လုပ်ကြောင်း **သက်သေမပြပါ**။
* 2024 နှင့် 2025 LOOCV errors (−6.05% နှင့် +6.47%) တစ်ခုချင်းကို post-ordinance year တစ်နှစ်တည်းဖြင့် ခန့်မှန်းထားသည်။

### ၇။ လက်ရှိ ခန့်မှန်းချက်များ (Current Estimates, Student's t, df = 5)

| Scenario | Downtown X₀ | Estimate | 95% PI |
|---|---:|---:|---|
| Dec 2025 (latest month) | 985.4 | 5,921 | 3,867–7,976 |
| Jan 2025 (PIT-matched) | 851.0 | 5,896 | 3,839–7,954 |
| Jan 2026 forecast | 862.9 | 5,899 | 3,843–7,955 |

Reporting rules အရ သုံးခုလုံး **5,900 [3,900–8,000]** သို့ ဝိုင်းသည် - margin **±2,050 (±35%)**။

**စိတ်ဝင်စားဖွယ် အချက်:** Downtown X₀ သည် 851 မှ 985 သို့ ပြောင်းသော်လည်း estimate သည် 5,896 မှ 5,921 သို့သာ ပြောင်းသည်။ Slope 0.186 သေးငယ်ပြီး significant မဖြစ်သဖြင့် estimate ကို အဓိက ဆုံးဖြတ်သည်မှာ intercept နှင့် regime term ဖြစ်သည်။ ဤအရာက "downtown count ဖြင့် county ကို ခန့်မှန်းနိုင်စွမ်း အကန့်အသတ်ရှိကြောင်း" ကို ပြသည်။

### ၈။ Governance - အသုံးပြုပုံ စည်းမျဉ်းများ (Task 8.4)

**Public communication rules ၄ ချက်** (Episode 1 ကို ကြည့်ပါ) - no single-point precision၊ round to 100၊ always 95% PI၊ disclose the policy regime။

**နှစ်စဉ် update လုပ်ငန်းစဉ်:**
1. PIT year အသစ်ကို `data/Downtown_County_PairedCounts.csv` တွင် ထည့်ပါ။
2. `python scripts/county_estimation_build.py` ကို run ပါ (LOOCV ပြန်လုပ်၊ refit၊ `CountyEstimate_Current.csv` ပြန်ထုတ်)။
3. Regime stability ကို ပြန်စစ်ပါ။
4. `src/config.py` constants ကို update လုပ်ပါ။
5. `pytest` ကို run ပါ။

**Memo recommendation:** County estimates ကို Rules 1–4 အောက်တွင် rounded ranges အဖြစ်သာ သုံးပါ။ RTFH က PIT count အသစ် ထုတ်တိုင်း model ကို ပြန်ခန့်မှန်းပါ။ Documented policy change ရှိမှသာ regime indicator ထည့်ပါ။

---

### ၉။ DSA အဖွဲ့ရှေ့ ပြောရမည့် အဓိက အချက်များ (Key Talking Points)

* "Forecasting မှာ model 5 မျိုးကို 5-fold walk-forward CV နဲ့ စစ်ခဲ့ပါတယ်။ Short horizon မှာ SARIMA အကောင်းဆုံး (1-month MAPE 5.4%)။ 12 months မှာ XGBoost, Holt-Winters, SARIMA တို့ statistically tie ဖြစ်ပါတယ်။"
* "2025 hold-out မှာ naive seasonal က 6.3% နဲ့ အကောင်းဆုံးဖြစ်ခဲ့လို့ simple baselines ကို အမြဲ comparison ထဲ ထားသင့်ပါတယ်။"
* "2026 forecast က လစဉ် 816–896 ဝန်းကျင်ဖြစ်ပြီး intervals တွေက approximate ပါ။ Scenarios တွေက fixed paths ပဲ ဖြစ်ပါတယ်။"
* "County model ရဲ့ R² က 0.504 ပဲ ရှိပြီး predictor တစ်ခုမှ 5% မှာ significant မဖြစ်ပါဘူး။ ဒါကြောင့် 5,900 [3,900–8,000] ကို directional range အနေနဲ့ပဲ သုံးဖို့ governance rules ချမှတ်ခဲ့ပါတယ်။"
