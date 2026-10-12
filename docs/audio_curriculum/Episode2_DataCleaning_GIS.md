# NotebookLM Audio Briefing — Episode 2
## အပိုင်း (၂) - ဒေတာ သန့်စင်ခြင်း၊ ဘလောက်အဆင့် ဒေတာ နှင့် နည်းစနစ် ပြောင်းလဲမှုများ (Assignments 1, 3 & 6)

> **NotebookLM customize prompt (copy & paste):**
> *"Create a deep-dive conversation in Burmese (မြန်မာဘာသာ) between two hosts about this briefing on data cleaning, block-level data, and methodology changes. Keep technical terms in English (data validation, multiplier, balanced panel, footprint expansion, constant-methodology series) and explain each in Burmese. Use only the numbers in this document."*

> **Source of truth:** `docs/FullTechnicalReport.md` §2, §5, §7 (v3.0); `docs/DataQualityReport.md`.

---

### ၁။ ဘာကြောင့် ဒေတာ သန့်စင်ခြင်းက အရေးကြီးသလဲ (Why Data Cleaning Comes First)

"Garbage in, garbage out" - မူရင်း ဒေတာ မှားနေလျှင် model ဘယ်လောက် ကောင်းကောင်း ရလဒ် မှားမည်။ Assignment 1 တွင် forecasting မလုပ်ခင် DSDP ဒေတာကို အသေးစိတ် စစ်ဆေးခဲ့သည်။

---

### ၂။ Assignment 1 - ဒေတာ စစ်ဆေးခြင်း နှင့် သန့်စင်ခြင်း (Data Validation & Cleaning)

**(က) ဒေတာ အရွယ်အစား**
* `RawCounts_AllYears_clean.csv` - စာကြောင်း **2,814** ကြောင်း၊ area နှင့် component (total, individuals, tents, vehicles) အလိုက် လစဉ် published counts။

**(ခ) Validation (မူရင်း PDF နှင့် တိုက်စစ်ခြင်း)**
* **45-cell random sample (Task 1.1):** published cells **41** ခုအနက် **40** ခု မူရင်း PDF နှင့် ကိုက်ညီ (**97.6%**)။ မကိုက်ညီသော တစ်ခု (April 2025, South East EV) သည် DSDP ၏ ကိုယ်ပိုင် breakout table က East Village total နှင့် ပေါင်းမကိုက်ခြင်းကြောင့် ဖြစ်သည်။
* **Full re-check (October 2026):** 2017–2025 neighborhood monthly totals **945** ခုလုံး DSDP report စာမျက်နှာ ၁ ရှိ summary tables နှင့် ကိုက်ညီသည်။

**(ဂ) Label များကို စံညှိခြင်း (Standardization)**
* လအမည်များ (Jan, June, July, Sept ...) ကို ISO date (`YYYY-MM-01`) သို့ ပြောင်းခဲ့သည်။
* **"Core"** label သည် 2017 – early 2019 reports တွင် **City Center** ကို ခေါ်သော နာမည်ဟောင်း ဖြစ်သည်။
* `Neighborhood_Crosswalk.csv` တွင် source label တိုင်းကို canonical neighborhood နှင့် sub-area သို့ map လုပ်ထားသည်။

**(ဃ) Multiplier logic (မြှောက်ဖော်ကိန်း)**

Adjusted count = individuals + μ_tent × tents + μ_veh × vehicles

| Regime | စတင်သည့်လ | Tent × | Vehicle × | မှတ်ချက် |
|---|---|---:|---:|---|
| PRE2017 | Jan 2017 | 2.00 | 2.00 | component breakdown မရှိ; total = raw |
| APR2017 | Apr 2017 | 1.75 | 1.66 | Clean & Safe က RTFH method ကို 27 Apr 2017 တွင် စတင်သုံး |
| MAY2018 | May 2018 | 1.75 | 2.03 | 31 May 2018 count ညတွင် စတင် |
| POST2020 | Jan 2020 | 1.75 | 2.03 | RTFH က HUD အတွက် multiplier မသုံးတော့; DSDP ဆက်သုံး |

* Component data သည် **January 2018** မှသာ ရှိသည်။ ထို့ကြောင့် 2017 လများ၏ adjusted total = published total။

**(င) တွေ့ရှိ၍ ပြင်ဆင်ခဲ့သော source errors (October 2026)**
1. **2019 East Village quadrants:** cells **48** ခုလုံးသည် **2020 တန်ဖိုးများကို ကူးထားခြင်း** ဖြစ်နေသည်။ January 2020 report ပါ 2019 breakout ဖြင့် အစားထိုးခဲ့သည်။ **Neighborhood totals များကို ဘယ်တုန်းကမှ မထိခိုက်ခဲ့ပါ** (quadrant ခွဲထားမှုသာ မှားခဲ့သည်)။
2. **Scanned maps နှင့် တိုက်၍ တွေ့သော component typos:**
   * Feb 2018 City Center: tents 100 → 10၊ vehicles 0 → 1။ Adjusted total သည် 156.16 ဖြစ်ရမည့်နေရာတွင် **312.00** ဖြစ်နေခဲ့သည် - နှစ်ဆနီးပါး။
   * Jul 2018 East Village: vehicles 32 → 26။
   * Jul 2022 Cortez: tents 20 → 26။
   * Nov 2022 Marina: individuals 49 → 29 (map total မှ ကောက်ချက်ချ)။
   * Mar 2024 City Center: tents 8 → 18။
3. **Missing values:** cells **134** ခု - 116 ခုသည် 2025 (မထုတ်ပြန်ရသေးသော ၄ လ)၊ 18 ခုသည် November 2018 (component breakdown မပါ)။
4. **ကျန်ရှိ flags:** adjusted နှင့် published totals 2 ထက်ပို ကွာသော area-months **22** ခုကို `MasterCounts_QA_Flags.csv` တွင် စာရင်းသွင်းထားသည်။

> 💡 **ပြောစရာ:** "အမှားတွေကို ဖုံးကွယ်ခြင်း မဟုတ်ဘဲ correction log (`source_corrections.csv`) မှာ PDF နဲ့ စာမျက်နှာ နံပါတ်ပါ ရေးမှတ်ထားလို့ ဘယ်သူမဆို ပြန်စစ်နိုင်ပါတယ်။"

---

### ၃။ Assignment 3 - ဘလောက်အဆင့် ဒေတာ နှင့် 2022 Footprint ပြောင်းလဲမှု (Block-Level Data & Footprint Change)

**(က) Block grid**
* `Downtown_BlockGrid.geojson` တွင် ဘလောက် **382** ခု။
* Polygon ၃၈၂ ခုလုံး valid၊ overlap မရှိ၊ zero-area မရှိ။
* Centroid ၃၈၂ ခုအနက် **380** ခု မိမိ polygon အတွင်း ကျသည်။ ခြွင်းချက် နှစ်ခုမှာ freeway interchange ပုံသဏ္ဌာန် concave parcels ဖြစ်သည်။
* Block-level ဒေတာသည် January/February count date **12** ခုကိုသာ digitize လုပ်ထားသည် (usable maps ရှိသော လ ~90 အနက်)။

**(ခ) 2022 footprint expansion (နယ်နိမိတ် ချဲ့ထွင်မှု)**
* **2022** တွင် ဘလောက် **121** ခု ထပ်တိုးခဲ့သည် - **Golden Hill (52)၊ Barrio Logan (35)၊ Sherman Heights (34)**။
* ဆိုလိုသည်မှာ 2022 နောက်ပိုင်း total တွင် ယခင်က မရေတွက်သော နေရာများ ပါလာသည်။

| Count date | Full 382 | Balanced 261 | ထပ်တိုး blocks | Full total ၏ ရာခိုင်နှုန်း |
|---|---:|---:|---:|---:|
| 2022-01-27 | 1,408.5 | 1,149.1 | 259.5 | 18.4% |
| 2022-03-01 | 1,392.5 | 1,158.2 | 234.3 | 16.8% |
| 2023-01-31 | 1,955.1 | 1,314.5 | 640.6 | **32.8%** |
| 2024-01-25 | 1,019.0 | 981.8 | 37.2 | **3.7%** |
| 2025-01-31 | 847.3 | 762.9 | 84.4 | 10.0% |

**(ဂ) Balanced 261-block panel ဖြေရှင်းချက်**
* Date တိုင်းတွင် ရေတွက်ခဲ့သော ဘလောက် **261** ခုသာ သုံး၍ တရားမျှတစွာ နှိုင်းယှဉ်သည် (`BlockPanel_Balanced_261.csv`)။
* အရေးကြီး ရလဒ်: ဘလောက် ၂၆၁ ခုပေါ်တွင်ပင် 2021 မှ 2022 သို့ **71%** တိုးခဲ့သည်။
* **နိဂုံး:** 2022 တိုးလာမှုတွင် **footprint ကြီးလာခြင်း** ရော **တကယ့် တိုးလာမှု** ပါ နှစ်မျိုးလုံး ပါဝင်သည်။ 2021/2022 ကို ဖြတ်၍ နှိုင်းယှဉ်လိုလျှင် balanced panel ကို မဖြစ်မနေ သုံးရမည်။

---

### ၄။ Assignment 6 - Multiplier နည်းစနစ် ပြောင်းလဲမှု၏ အကျိုးသက်ရောက်မှု (Methodology Impact)

Multipliers သည် April 2017 နှင့် May 2018 တွင် ပြောင်းခဲ့သည်။ မေးခွန်းမှာ - "လစဉ် ကိန်းဂဏန်း ပြောင်းလဲမှုသည် တကယ့် လူဦးရေ ပြောင်းလဲမှုလား၊ multiplier ပြောင်းလိုက်ခြင်း၏ ဂဏန်းသင်္ချာ အကျိုးဆက်လား။"

**(က) Theoretical vs observed ratio**

| Break | Theoretical ratio (multiplier သက်သက်) | Observed adjacent-month ratio |
|---|---:|---:|
| April 2017 | 0.964 (−3.6%) | 0.792 |
| May 2018 | 1.007 (+0.7%) | 1.141 |

* တကယ် လစဉ် ပြောင်းလဲမှုသည် multiplier အကျိုးသက်ရောက်မှုထက် **အများကြီး ပိုကြီးသည်**။
* April 2017 တွင် 2018 မတိုင်မီ component data မရှိသဖြင့် observed ratio တွင် multiplier signal လုံးဝ မပါပါ။

**(ခ) Constant-methodology series**
* `TimeSeries_ConstantMethodology.csv` သည် သမိုင်းဒေတာ အားလုံးကို **POST2020 multipliers (1.75 / 2.03)** သို့ ပြန်ညှိထားသည် -
  * Jan–Apr 2018 (component data ရှိ) - exact factors။
  * 2017 - Jan–Apr 2018 composition proxy။
  * May 2018 နောက်ပိုင်း - factor 1.0။

**(ဂ) Approach နှိုင်းယှဉ်ချက် (Task 6.3)**
* Pre-2020 pooled mean gap vs raw counts - **hybrid +0.10%**၊ theoretical-only ~+0.1%၊ data-derived-only **+5.1%**။
* **Hybrid approach ကို အကြံပြုသည်။** Data-derived series ကို diagnostics အတွက်သာ သုံးသင့်သည်။

---

### ၅။ DSA အဖွဲ့ရှေ့ ပြောရမည့် အဓိက အချက်များ (Key Talking Points)

* "Model မဆောက်ခင် 2,814 rows ကို စစ်ပြီး neighborhood totals 945 ခုလုံး DSDP summary tables နဲ့ ကိုက်ညီကြောင်း အတည်ပြုခဲ့ပါတယ်။"
* "2019 East Village quadrant ဒေတာ 48 cells က 2020 ကို ကူးထားတာ ဖြစ်နေလို့ ပြင်ခဲ့ပါတယ်။ ဒါပေမဲ့ neighborhood totals ကို မထိခိုက်ခဲ့ပါဘူး။"
* "2022 မှာ ဘလောက် 121 ခု ထပ်တိုးခဲ့လို့ January 2023 total ရဲ့ 32.8% က ဘလောက်အသစ်တွေကနေ လာပါတယ်။ ဒါကြောင့် balanced 261-block panel ကို ဆောက်ခဲ့ပြီး အဲဒီမှာတောင် 71% တိုးတာ တွေ့ရလို့ တိုးလာမှုက တကယ်ပါ။"
* "Multiplier ပြောင်းလဲမှုရဲ့ သီအိုရီ အကျိုးသက်ရောက်မှုက −3.6% နဲ့ +0.7% လောက်ပဲ ရှိပြီး တကယ် လစဉ် ပြောင်းလဲမှုထက် အများကြီး သေးပါတယ်။"
