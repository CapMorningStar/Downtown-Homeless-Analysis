# NotebookLM Audio Briefing — Episode 1
## အပိုင်း (၁) - အမှုဆောင် အနှစ်ချုပ် နှင့် အဓိက ရလဒ်များ (Executive Narrative & Core Findings)

> **NotebookLM customize prompt (copy & paste):**
> *"Create a deep-dive conversation in Burmese (မြန်မာဘာသာ) between two hosts about this briefing. Keep technical terms in English (for example Point-in-Time count, prediction interval, policy regime, R-squared) and explain each one in Burmese. Use only the numbers in this document. Be careful to distinguish what the data shows from what it does not prove."*

> **Source of truth:** `docs/FullTechnicalReport.md` (v3.0, October 2026), `docs/ExecutiveSummary_NonTechnical.md`, `docs/StrategicRecommendations_Memo.md`.

---

### ၁။ စီမံကိန်း နောက်ခံ (Project Context)

ဤစီမံကိန်းကို **Data Science Alliance (DSA)** အတွက် **Kyaw Soe Lwin** က lead analyst အဖြစ် ဆောင်ရွက်ခဲ့ပြီး project lead နှင့် reviewer မှာ **Adir Mancebo Jr.** ဖြစ်သည်။

မေးခွန်း သုံးခု ရှိသည် -
1. ဆန်ဒီယေဂို မြို့လယ်ခေါင် (Downtown San Diego) ၏ လမ်းပေါ်နေ အိုးမဲ့အိမ်မဲ့ အရေအတွက်သည် အချိန်နှင့်အမျှ မည်သို့ ပြောင်းလဲခဲ့သနည်း။
2. မည်သည့် နေရာများတွင် စုပြုံနေသနည်း။
3. Downtown လစဉ် ကိန်းဂဏန်းဖြင့် ကောင်တီတစ်ခုလုံး၏ အရေအတွက်ကို ခန့်မှန်းနိုင်သလား။

**ဒေတာ အရင်းအမြစ် နှစ်ခု:**
* **DSDP Clean & Safe monthly count** - Downtown San Diego Partnership က မြို့လယ်ခေါင်တွင်သာ လစဉ် တစ်ည ရေတွက်သည်။ ဤစီမံကိန်းတွင် **January 2017 – December 2025** (လ ၁၀၈ လ၊ ထုတ်ပြန်ပြီးသား ၁၀၄ လ) ကို အသုံးပြုသည်။ 2025 ၏ July, August, October, November လများကို data ထုတ်ယူချိန်တွင် မထုတ်ပြန်ရသေးပါ။
* **RTFH Point-in-Time (PIT) count** - Regional Task Force on Homelessness က ဇန်နဝါရီလတွင် ကောင်တီတစ်ခုလုံး တစ်ညတည်း ရေတွက်သည်။ Paired years **၈ နှစ်** (2017–2020, 2022–2025)။ 2021 unsheltered count ကို ဖျက်သိမ်းခဲ့သည်။

---

### ၂။ အချိန်နှင့်အမျှ ပြောင်းလဲမှု (How the Count Changed)

**နှစ်စဉ် ပျမ်းမျှ (annual citywide averages):**

| နှစ် | ပျမ်းမျှ / လ |
|---|---:|
| 2017 | 1,057.8 |
| 2018 | 843.0 |
| 2019 | 810.4 |
| 2020 | 654.1 |
| 2021 | 960.4 |
| 2022 | 1,513.1 |
| 2023 | 1,563.1 |
| 2024 | 886.9 |
| 2025 | 864.3 |

**အဓိက အချက်များ:**
* 2017 မှ 2020 သို့ **−38.2%** ကျခဲ့သည်။
* အနိမ့်ဆုံး လစဉ်တန်ဖိုး - **529.1 (March 2020)**။
* အမြင့်ဆုံး လစဉ်တန်ဖိုး - **2,103.3 (May 2023)** - စီမံကိန်း ကာလတစ်လျှောက် အမြင့်ဆုံး။
* 2023 နှစ်စဉ်ပျမ်းမျှ မှ 2024 သို့ **−43.3%** ကျခဲ့သည်။
* PIT နှင့် ကိုက်ညီသော **January 2025** downtown count မှာ **851** ဖြစ်သည်။ နောက်ဆုံးလ **December 2025** မှာ **985.4** ဖြစ်သည်။

> ⚠️ **ပြောရာတွင် သတိပြုရန်:** "851" သည် **January 2025** ကိန်းဖြစ်ပြီး December 2025 မဟုတ်ပါ။

**July 2023 Unsafe Camping Ordinance:**
City of San Diego က July 2023 တွင် အများပြည်သူ လူသွားလမ်းများပေါ် တဲထိုးခြင်းကို ကန့်သတ်သည့် Unsafe Camping Ordinance ကို ပြဋ္ဌာန်းခဲ့သည်။ ကိန်းဂဏန်းများ ကျဆင်းခဲ့သည်မှာ ထို ordinance ကာလနှင့် တစ်ပြိုင်နက် ဖြစ်သည်။

> ⚠️ **အရေးကြီး ကန့်သတ်ချက်:** စီမံကိန်းတွင် **July 2023 ကို structural break test ဖြင့် မစစ်ခဲ့ပါ**။ Chow test စစ်ခဲ့သော ရက်စွဲများမှာ April 2017၊ May 2018 နှင့် March 2020 (COVID) သာ ဖြစ်သည်။ ထို့ကြောင့် "ordinance ကြောင့် ကျသွားသည်" ဟု သက်သေပြထားခြင်း မရှိပါ။ "ordinance ကာလနှင့် တစ်ပြိုင်နက် ကျဆင်းခဲ့သည်" ဟုသာ ပြောရမည်။

---

### ၃။ Downtown နှင့် ကောင်တီ ကွဲပြားလာခြင်း (The Downtown–County Divergence)

ဤသည်မှာ စီမံကိန်း၏ အစိတ်ဝင်စားဖွယ် အကောင်းဆုံး တွေ့ရှိချက် ဖြစ်သည်။

| PIT year | Downtown (January) | County unsheltered | Downtown share |
|---|---:|---:|---:|
| 2017 | 882.0 | 5,621 | 15.7% |
| 2018 | 803.5 | 4,990 | 16.1% |
| 2019 | 897.2 | 4,476 | 20.0% |
| 2020 | 789.1 | 3,971 | 19.9% |
| 2022 | 1,444.3 | 4,106 | 35.2% |
| 2023 | 1,938.7 | 5,171 | **37.5%** |
| 2024 | 1,018.1 | **6,110** | 16.7% |
| 2025 | 851.0 | 5,714 | **14.9%** |

**ဆိုလိုရင်း:**
* 2023 မှ 2025 သို့ downtown share သည် **37.5% မှ 14.9%** သို့ ကျခဲ့သည်။
* တစ်ချိန်တည်းတွင် ကောင်တီ unsheltered count သည် 2024 တွင် **6,110** (ဤ paired years ၈ နှစ်အတွင်း အမြင့်ဆုံး) ဖြစ်ပြီး 2025 တွင် **5,714** ဖြစ်သည်။
* Downtown share ၏ တည်ငြိမ်မှုကို ANOVA ဖြင့် စစ်ရာ **F = 66.51, p = 0.0002** - ကာလ ၃ ခု (2017–2020, 2022–2023, 2024–2025) အကြား အချိုး မတည်ငြိမ်ပါ။

**ဤအရာကို မည်သို့ အဓိပ္ပာယ်ကောက်ရမည်နည်း။**
* Downtown ကျဆင်းမှုသည် ကောင်တီတစ်ခုလုံး ကျဆင်းမှုနှင့် **မတူပါ**။ Downtown တွင် နည်းသွားသော်လည်း ကောင်တီတွင် မြင့်နေဆဲ။
* ဤပုံစံသည် လူများ downtown မှ အခြားနေရာများသို့ ရွှေ့သွားခြင်း (**displacement**) နှင့် **ကိုက်ညီသည်**။
* ⚠️ သို့သော် စီမံကိန်းသည် displacement ကို **သက်သေမပြပါ**။ Report ကိုယ်တိုင်က "The model describes the post-2023 divergence between downtown and county counts. It does not prove that the ordinance displaced people." ဟု ရေးထားသည်။
* ထို့ကြောင့် Memo ၏ **Recommendation R5** သည် "displacement explanation ကို တိုက်ရိုက် စမ်းသပ်ပါ" ဖြစ်သည် - ဥပမာ outreach contact records ဖြင့် downtown မှ ထွက်သွားသူများကို ခြေရာခံခြင်း။

---

### ၄။ ကောင်တီ ခန့်မှန်းချက် (County Estimate)

Leave-one-year-out cross-validation (LOOCV) တွင် အကောင်းဆုံး model မှာ **OLS + policy-regime indicator** ဖြစ်သည် -

**Y = 4,513.26 + 0.1859·X + 1,225.04·D_post**
(X = January downtown count၊ D_post = 1 for PIT years 2024 and 2025)

| အချက် | တန်ဖိုး |
|---|---|
| LOOCV RMSE | 815 |
| LOOCV MAPE | 14.9% |
| R² (in-sample) | **0.504** (adjusted 0.306) |
| Downtown slope p-value | 0.78 |
| Regime term p-value | 0.075 |

**ရိုးရိုးသားသား အဓိပ္ပာယ်:**
* Predictor နှစ်ခုလုံး **5% level တွင် significant မဖြစ်ပါ**။ N = 8 သာ ရှိသည်။
* D_post = 1 ဖြစ်သော နှစ် **နှစ်နှစ်** သာ ရှိသဖြင့် regime term သည် ထိုနှစ်နှစ်အတွက် indicator နီးပါး ဖြစ်နေသည်။
* ထို့ကြောင့် ကောင်တီ ခန့်မှန်းချက်သည် **directional only** (လမ်းကြောင်းပြ သက်သက်) ဖြစ်သည်။

**လက်ရှိ ခန့်မှန်းချက်:** **ခန့်မှန်း 5,900 [95% PI: 3,900 – 8,000]** - margin ±2,050 (±35%)။

> ⚠️ **ပြောရာတွင် သတိပြုရန်:** R² ကို **0.504** ဟုသာ ပြောပါ။ 0.9638 / 0.964 သည် ANOVA ၏ η² ဖြစ်ပြီး model R² မဟုတ်ပါ။

---

### ၅။ အများပြည်သူ ဆက်သွယ်ရေး စည်းမျဉ်း ၄ ချက် (The 4 Public Communication Rules)

ကောင်တီ ခန့်မှန်းချက်သည် မသေချာမှု ကြီးမားသဖြင့် စည်းမျဉ်း ၄ ချက် သတ်မှတ်ခဲ့သည် -

1. **Rule 1 – Single-point precision မထုတ်ပြန်ရ:** "5,921" ကဲ့သို့ မဝိုင်းထားသော ကိန်းကို မထုတ်ပြန်ရ။
2. **Rule 2 – အနီးဆုံး ရာဂဏန်းသို့ ဝိုင်းရမည်:** "5,900"။
3. **Rule 3 – 95% prediction interval ကို အမြဲ ပြရမည်:** "5,900 [3,900 to 8,000]"။
4. **Rule 4 – Policy regime ကို ဖော်ပြရမည်:** ဤခန့်မှန်းချက်သည် downtown counts မှ ဆင်းသက်လာပြီး post-July 2023 Unsafe Camping Ordinance enforcement ပတ်ဝန်းကျင် ဆက်ရှိနေမည်ဟု ယူဆထားကြောင်း ဖော်ပြရမည်။

**သင့်လျော်သော အသုံးပြုမှု vs မသင့်လျော်သော အသုံးပြုမှု:**

| သင့်လျော် (Appropriate) | မသင့်လျော် (Not appropriate) |
|---|---|
| PIT count နှစ်ခုကြား directional tracking | HUD Continuum of Care submissions |
| Scenario planning နှင့် capacity stress tests | Formula funding / sub-regional allocations |
| Hotspot များတွင် outreach နှင့် field validation ဦးစားပေးခြင်း | Interval မပါသော single-number media statements |

---

### ၆။ DSA အဖွဲ့ရှေ့ တင်ပြရာတွင် အဓိက ပြောရမည့် အချက်များ (Key Talking Points)

* "Downtown count က May 2023 မှာ 2,103 နဲ့ အမြင့်ဆုံးရောက်ပြီး January 2025 မှာ 851 ထိ ကျသွားပါတယ်။ ဒါပေမဲ့ county count က 2024 မှာ 6,110 နဲ့ မြင့်နေပါတယ်။"
* "Downtown share က 37.5% ကနေ 14.9% ထိ ကျသွားတာဟာ displacement နဲ့ ကိုက်ညီပါတယ်။ ဒါပေမဲ့ ကျွန်တော့် analysis က အကြောင်းရင်းကို သက်သေမပြပါဘူး။ ဒါကြောင့် outreach records နဲ့ တိုက်ရိုက် စမ်းသပ်ဖို့ အကြံပြုထားပါတယ်။"
* "County model ရဲ့ R² က 0.504 ပဲ ရှိပြီး data point ၈ ခုပဲ ရှိလို့ estimate ကို 5,900 [3,900–8,000] ဆိုတဲ့ range အနေနဲ့ပဲ သုံးသင့်ပါတယ်။ ဒါကြောင့် communication rules ၄ ချက် ချမှတ်ခဲ့တာပါ။"
* ဤ honesty သည် senior data scientist များ အထူးတန်ဖိုးထားသော အရည်အချင်း ဖြစ်သည် - **ဒေတာ ပြနိုင်သည့်အရာ နှင့် မပြနိုင်သည့်အရာကို ခွဲခြားပြောနိုင်ခြင်း**။
