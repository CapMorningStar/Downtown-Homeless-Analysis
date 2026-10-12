# NotebookLM Audio Briefing — Episode 3
## အပိုင်း (၃) - ရာသီအလိုက် ပြောင်းလဲမှု၊ ဖွဲ့စည်းပုံ အချိုးအကွေ့ နှင့် Hotspots (Assignments 2, 4 & 5)

> **NotebookLM customize prompt (copy & paste):**
> *"Create a deep-dive conversation in Burmese (မြန်မာဘာသာ) between two hosts about this briefing on seasonality, structural breaks, and spatial hotspots. Keep technical terms in English (STL decomposition, Kruskal-Wallis, Chow test, FDR correction, Moran's I, Getis-Ord Gi*) and explain each in Burmese with simple analogies. Use only the numbers in this document and clearly state the limitations."*

> **Source of truth:** `docs/FullTechnicalReport.md` §3, §4, §6 (v3.0).

---

### ၁။ Assignment 2 - ဖော်ပြချက်ဆိုင်ရာ ခွဲခြမ်းစိတ်ဖြာမှု (Descriptive Analysis)

**လစဉ် counts အနှစ်ချုပ် (2017–2025, published months only):**

| Series | Months | Mean | Min | Max |
|---|---:|---:|---:|---:|
| Citywide total | 104 | 1,022.9 | 529.1 (Mar 2020) | 2,103.3 (May 2023) |
| East Village | 104 | 552.0 | 260.6 | 921.0 |
| City Center | 104 | 170.7 | 91.0 | 342.3 |
| Cortez | 104 | 59.6 | 16.0 | 170.5 |
| Gaslamp | 104 | 48.2 | 18.5 | 93.0 |
| Columbia | 104 | 44.5 | 13.8 | 84.5 |
| Marina | 104 | 30.7 | 4.1 | 79.0 |
| Outside Perimeter | 56 | 217.6 | 0.0 | 640.0 |

* **East Village** သည် ကာလတစ်လျှောက် ရေတွက်ခဲ့သူ အားလုံး၏ **54.0%** ဖြစ်သည် - မြို့လယ်ခေါင် အိုးမဲ့အိမ်မဲ့ အများစု စုပြုံရာ။
* Year-over-year ပြောင်းလဲမှု (citywide total basis) - 2021 **+46.8%**၊ 2022 **+57.6%**။
* ⚠️ Neighborhood ပြောင်းလဲမှုများ၏ unweighted mean (2021: +25.9%) နှင့် citywide basis ကို **ရောမပြောပါနှင့်** - တွက်နည်း မတူပါ။

---

### ၂။ Assignment 4 (Tasks 4.1–4.2) - ရာသီဥတုက အရေးကြီးသလား? (Is There Seasonality?)

**လူအများ ယူဆချက်:** "ဆောင်းတွင် လမ်းပေါ်တွင် နည်းပြီး နွေတွင် များမည်" ဟု ထင်ကြသည်။ ဒေတာက မည်သို့ ပြောသနည်း။

**(က) STL decomposition**
* ဒေတာကို trend + seasonal + residual ဟု ခွဲထုတ်ခြင်း။
* Seasonal strength (0 = ရာသီပုံစံ လုံးဝမရှိ၊ 1 = အပြည့်) -
  * Overall series - **0.07**
  * Core six - 0.32
  * East Village - 0.26
  * City Center - 0.01
  * ကျန် neighborhoods - 0.10–0.21

**(ခ) Kruskal-Wallis test (primary test)**
* လ ၁၂ လ၏ de-trended တန်ဖိုးများ သိသိသာသာ ကွဲပြားခြင်း ရှိ/မရှိ စစ်သည်။ Normal distribution မလိုသဖြင့် ဤဒေတာအတွက် သင့်တော်သည်။

| Series | Kruskal-Wallis H | p | ANOVA p |
|---|---:|---:|---:|
| Overall — reported footprint | 2.66 | **0.995** | 0.998 |
| Overall — fixed core six | 9.00 | 0.622 | 0.670 |
| East Village | 14.16 | 0.224 | 0.219 |
| City Center | 4.86 | 0.938 | 0.913 |
| Columbia | 8.76 | 0.644 | 0.473 |
| Cortez | 12.73 | 0.312 | 0.047 |
| Gaslamp | 14.57 | 0.203 | 0.087 |
| Marina | 19.88 | **0.047** | 0.162 |
| Outside Perimeter | 11.45 | 0.406 | 0.440 |

**ရလဒ်:**
* **Series ၉ ခုအနက် ၈ ခုတွင် significant seasonality မရှိပါ** (Kruskal-Wallis)။
* Test နှစ်ခု သဘောမတူသော အခြေအနေ - Marina (KW significant, ANOVA မဟုတ်)၊ Cortez (ANOVA significant, KW မဟုတ်)။
* တစ်လချင်း significant လများ - Gaslamp September (မြင့်)၊ Marina August နှင့် November (မြင့်)၊ Outside Perimeter September (နိမ့်)။ ⚠️ ဤ per-month tests တွင် multiple-comparison correction မလုပ်ထားပါ။

**ရိုးရိုး ဥပမာ:** ရာသီဥတုသည် ပင်လယ်ပြင်ရှိ လှိုင်းငယ်လေးများ သာဖြစ်ပြီး၊ နှစ်ပေါင်းများစွာ ကြာသော ဒီရေ (multi-year swings) က အဓိက ဖြစ်သည်။ 2017 မှ 2020 သို့ −38.2%၊ ထို့နောက် 2023 peak၊ ထို့နောက် 2023 မှ 2024 သို့ −43.3% - ဤကြီးမားသော လှိုင်းများသည် ရာသီဥတုနှင့် မသက်ဆိုင်ပါ။

> ⚠️ **သတိ:** "Weather explains less than 5% of variance" ဟူသော စကားကို **မပြောပါနှင့်** - ထိုကိန်းဂဏန်းကို စီမံကိန်းတွင် မတွက်ခဲ့ပါ။ "Kruskal-Wallis tests found no significant calendar-month effect in 8 of 9 series" ဟုသာ ပြောပါ။

---

### ၃။ Assignment 4 (Task 4.3) - ဖွဲ့စည်းပုံ အချိုးအကွေ့များ (Structural Breaks)

**Chow test ဆိုသည်မှာ:** ရက်စွဲတစ်ခု မတိုင်မီ နှင့် နောက်ပိုင်းတွင် regression line ၏ level (အမြင့်) သို့မဟုတ် slope (လမ်းကြောင်း) ကွဲပြားခြင်း ရှိ/မရှိ စစ်ခြင်း။

Model: y = β₀ + β₁τ + β₂D + β₃D(τ − τ_break) - β₂ = β₃ = 0 ကို ပူးတွဲ စစ်သည်။ **Benjamini-Hochberg FDR correction** ကို event တစ်ခုချင်းအတွင်း သုံးပြီး **HAC(12)** check လည်း လုပ်သည်။

**စစ်ခဲ့သော ရက်စွဲများ နှင့် ရလဒ်:**

1. **April 2017 (multiplier change):** break မတိုင်မီ **၃ လ** သာ ရှိသဖြင့် exploratory သာ။ Columbia တစ်ခုသာ တွေ့ (F = 12.17, p = 0.001)။
2. **May 2018 (multiplier change):** eligible series ၈ ခုအနက် **၅ ခု** significant (East Village, Cortez, core six, Columbia, Gaslamp)။ ⚠️ **Overall reported-footprint series က significant မဖြစ်ပါ** (F = 1.46, p = 0.237)။ `raw_count` ဖြင့် စစ်လည်း series ၅ ခုတည်း significant ဖြစ်သဖြင့် multiplier ဂဏန်းသင်္ချာ သက်သက် မဟုတ်ပါ။
3. **COVID-19 onset (March 2020):** series ၈ ခုအနက် **၇ ခု** significant (City Center မှလွဲ၍)။ FDR correction ပြီးနောက်လည်း ၇ ခု ကျန်သည်။ Reported-footprint total ၏ level shift **+318** (p = 0.020)။ Series အလိုက် mechanism မတူပါ - level only, trend only, နှစ်ခုလုံး, သို့မဟုတ် indeterminate။

**CUSUM stability test:** OLS residuals ပေါ်တွင် - series ၉ ခုအနက် **၇ ခု** ကာလတစ်လျှောက် မတည်ငြိမ်ပါ (Gaslamp နှင့် Marina တည်ငြိမ်)။

> ⚠️ **အလွန်အရေးကြီး:** **July 2023 (Unsafe Camping Ordinance) ကို break test မလုပ်ခဲ့ပါ။** Ordinance ကြောင့် monthly series တွင် break ရှိသည်ဟု ပြောလျှင် Task 4.3 scope ပြင်ပ ဖြစ်သည်။ DSA က "Did you test the ordinance?" ဟု မေးလျှင် - "No, I tested April 2017, May 2018 and March 2020. A July 2023 test is a natural next step." ဟု ရိုးသားစွာ ဖြေပါ။

**Stationarity (Task 4.4):** Levels တွင် ADF/KPSS - series ၇ ခု mixed evidence၊ ၂ ခု jointly non-stationary။ Transformation (series ၈ ခုအတွက် first difference၊ Outside Perimeter အတွက် log1p) ပြီးနောက် **၉ ခုလုံး stationary** ဖြစ်သည်။ ဤအရာက ARIMA models အတွက် အခြေခံ ဖြစ်သည်။

---

### ၄။ Assignment 5 - Hotspot ခွဲခြမ်းစိတ်ဖြာမှု (Spatial Hotspot Analysis)

**Settings:** balanced **261-block panel** (Episode 2 ကို ကြည့်ပါ)၊ outcome = individuals + 1.75·tents + 1.66 or 2.03·vehicles၊ **queen contiguity** (ထောင့်ချင်း ထိလျှင်လည်း အိမ်နီးချင်း)၊ row-standardized weights၊ **9,999 permutations**။

**(က) Global Moran's I (Task 5.1) - "ဒေတာ တစ်ခုလုံးတွင် အစုအဝေး ရှိသလား"**
* Digitized date **၁၂** ခုလုံးတွင် **positive** - 0.063 (Jan 2019) မှ 0.239 (Feb 2018)၊ permutation p ≤ 0.034။
* ဆိုလိုသည်မှာ - အိုးမဲ့အိမ်မဲ့ အများ ရှိသော ဘလောက်များသည် အချင်းချင်း နီးကပ်စွာ စုနေတတ်သည်။ ကျပန်း ပြန့်ကျဲနေခြင်း မဟုတ်ပါ။

**(ခ) Local Getis-Ord Gi\* (Task 5.2) - "ဘယ်ဘလောက်တွေမှာ စုနေသလဲ"**
* Block-date တစ်ခုကို hotspot အဖြစ် သတ်မှတ်ရန် **z-score နှင့် permutation p နှစ်ခုလုံး** ကိုက်ရမည် -
  * 99% hotspot: z ≥ 2.576 **နှင့်** p < 0.01
  * 95% hotspot: z ≥ 1.96 **နှင့်** p < 0.05
* Block-dates **3,132** ခုအနက် - **99% hotspots 16 ခု**၊ **95% hotspots 22 ခု**။
* ⚠️ **90% class မရှိပါ** - 95% နှင့် 99% သာ သုံးသည်။

**(ဂ) Persistence (Task 5.4) - "ဘယ်ဘလောက်က အမြဲ hotspot ဖြစ်နေလဲ"**

| Rank | Block | Hotspot dates (of 12) |
|---:|---|---:|
| 1 | 16th St & Imperial Ave | **9** |
| 2 | I-5 SB & Imperial Ave | 8 |
| 3 | I-5 SB off-ramp (map border) | 6 |
| 4 | I-5 SB on-ramp (map border) | 4 |
| 5 | 17th St & Imperial Ave | 4 |
| 6–8 | 16th St & J St, 17th St & J St, 16th St & Island Ave | 2 each |

* **Top ten အားလုံး South East Village တွင် ရှိသည်** - 16th/17th St & Imperial Ave နှင့် I-5 southbound ramps အစုအဝေး။

**(ဃ) Migration - hotspot ဗဟိုချက် ရွှေ့လျားမှု**
* Count-weighted centroid of hotspot block-dates သည် 2018–2020 မှ 2022–2025 သို့ **ခန့်မှန်း ၁၂၀ မီတာ၊ bearing 160° (south-south-east)** ရွေ့သည်။
* Unweighted centroid ရွေ့လျားမှုမှာ **~62 မီတာ** သာ ဖြစ်သည်။
* ⚠️ **ကန့်သတ်ချက်များ:**
  * ဤအရာသည် **significant clusters ရှိရာနေရာ** ကို ဖော်ပြခြင်းသာ ဖြစ်ပြီး **လူများ၏ ရွှေ့ပြောင်းမှုကို တိုင်းတာခြင်း မဟုတ်ပါ**။
  * Date ၁၂ ခုသာ ရှိ၍ follow-up လုပ်ရန် **pointer** သာ ဖြစ်ပြီး trend estimate မဟုတ်ပါ။
  * Date ၁၂ ခုလုံး January/February snapshots ဖြစ်သည်။

> ⚠️ **ပြောရာတွင် သတိပြုရန်:** "Enforcement pushed people south" ကဲ့သို့ အကြောင်းရင်း မပြောပါနှင့်။ "The hotspot centroid sits about 120 m further south-south-east in 2022–2025 than in 2018–2020" ဟုသာ ပြောပါ။

**ဤ hotspots ကို မည်သို့ အသုံးချသင့်သနည်း (Memo recommendation):**
* Persistent hotspot blocks များကို **field validation နှင့် outreach coordination အတွက် shortlist** အဖြစ် သုံးပါ။
* ⚠️ ၎င်းတို့ တစ်ခုတည်းဖြင့် unmet need ၏ သက်သေ သို့မဟုတ် service ထားရမည့်နေရာ၏ သက်သေ **မဟုတ်ပါ**။
* **အဖိုးတန်ဆုံး data investment:** block digitization ကို January/February date ၁၂ ခုထက် ကျော်၍ ချဲ့ပါ - ဤသို့ဆိုလျှင် block-level seasonal နှင့် post-ordinance spatial analysis လုပ်နိုင်မည်။

---

### ၅။ DSA အဖွဲ့ရှေ့ ပြောရမည့် အဓိက အချက်များ (Key Talking Points)

* "Kruskal-Wallis tests မှာ series 9 ခုအနက် 8 ခု significant seasonality မရှိပါဘူး။ Overall series က H = 2.66, p = 0.995 ပါ။ ဒါကြောင့် multi-year swings က အဓိကပါ။"
* "Chow tests မှာ COVID onset က series 8 ခုအနက် 7 ခုမှာ significant ဖြစ်ပါတယ်။ July 2023 ordinance ကိုတော့ မစစ်ခဲ့ရသေးလို့ next step အဖြစ် ထားပါတယ်။"
* "Moran's I က date 12 ခုလုံးမှာ positive ဖြစ်ပြီး persistent hotspot က 16th & Imperial ပါ (date 12 ခုအနက် 9 ခု)။ Top ten အားလုံး South East Village မှာပါ။"
* "Hotspot centroid က 120 m လောက် south-south-east ရွေ့ပေမဲ့ ဒါက cluster location ပဲ ဖြစ်ပြီး လူတွေရဲ့ movement ကို မတိုင်းတာပါဘူး။"
