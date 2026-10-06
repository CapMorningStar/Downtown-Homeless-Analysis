# Methodology Change Log: Longitudinal Counting Rules (2017–2025)

**Downtown San Diego Homeless Population Analysis**  
*Data Science Alliance / Volunteer Analytics Project*  
**Author:** Kyaw Soe Lwin (`kylwin@ucsd.edu`)  
**Project Lead:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)  

---

## 1. Overview of Methodology Regimes

Outreach workers with the Downtown San Diego Partnership (DSDP) Clean & Safe program conduct monthly overnight censuses of individuals experiencing unsheltered homelessness across downtown streets, parks, sidewalks, and perimeter corridors. Because multiple persons frequently inhabit makeshift structures and vehicles, multiplying multipliers are applied to tents and vehicles to estimate the true unhoused headcount.

Between 2017 and 2025, four distinct methodology regimes governed how count data was collected, adjusted, and reported:

```text
2017-01        2017-04              2018-06        2020-01                        2025-12
   |--------------|--------------------|--------------|------------------------------|
      PRE2017           APR2017             MAY2018                     POST2020
   (2.00 / 2.00)     (1.75 / 1.66)       (1.75 / 2.03)               (1.75 / 2.03)
   [Totals Only]     [Breakouts Start]   [Vehicle Bump]              [RTFH PIT Stops;
                                                                      DSDP Continues]
```

---

## 2. Methodology Timeline & Regime Specifications

### Regime 1: `PRE2017` (Pre-April 2017)
* **Effective Date:** Historical baseline through March 31, 2017.
* **Documented Rule:** $2.00$ individuals per tent/structure; $2.00$ individuals per vehicle.
* **Empirical Multipliers in Dataset:** N/A (Only aggregate neighborhood totals exist in data; 0 component rows).
* **Source Reference:** Regional Task Force on Homelessness (RTFH) historical Point-in-Time guidelines.
* **Known Limitations in Delivered Data:** All 18 rows (Jan–Mar 2017 across 6 neighborhoods) carry only `component == 'total'`. No raw individual, tent, or vehicle breakdown was captured in DSDP digitized records.
* **Downstream Handling:** Preserved strictly as `total_count = raw_count`.

---

### Regime 2: `APR2017` (April 2017 – May 2018)
* **Effective Date:** April 1, 2017 – May 30, 2018.
* **Documented Rule:**
  * **Individuals:** $1.00$
  * **Tents / Structures:** $\mathbf{1.75}$ individuals per tent
  * **Vehicles:** $\mathbf{1.66}$ individuals per vehicle
* **Empirical Multipliers in Dataset:**
  * Individuals: $1.0000$ (24 rows audited, 100% match)
  * Tents: $1.7500$ (19 rows audited, 100% match)
  * Vehicles: $1.6600$ (12 rows audited, 100% match)
* **Rationale for Change:** RTFH updated demographic multiplier estimates following field surveys indicating smaller average vehicle occupancy ($1.66$).
* **Source Reference:** RTFH 2017 Methodology Revision Notice & DSDP April 2017 Monthly Packet.

---

### Regime 3: `MAY2018` (June 2018 – December 2019)
* **Effective Date:** May 31, 2018 – December 31, 2019 (marked as `MAY2018`).
* **Documented Rule:**
  * **Individuals:** $1.00$
  * **Tents / Structures:** $\mathbf{1.75}$ individuals per tent
  * **Vehicles:** $\mathbf{2.03}$ individuals per vehicle ($+0.37$ increase)
* **Empirical Multipliers in Dataset:**
  * Individuals: $1.0000$ (114 rows audited, 100% match)
  * Tents: $1.7500$ (107 rows audited, 100% match)
  * Vehicles: $2.0300$ (27 rows audited, 100% match)
* **Rationale for Change:** Updated RTFH survey data reflecting higher vehicle habitation densities (average of $2.03$ individuals per inhabited RV or vehicle).
* **Source Reference:** DSDP May 31, 2018 Monthly Report & RTFH 2018 PIT Guidelines.

---

### Regime 4: `POST2020` (January 2020 – Present)
* **Effective Date:** January 1, 2020 – Present.
* **The January 2020 Divergence:**
  * **RTFH Treatment:** Following federal HUD guidance, the Regional Task Force on Homelessness **ceased applying multipliers to tents and vehicles** during annual PIT counts, reporting raw counts only.
  * **DSDP Clean & Safe Treatment:** To prevent artificial multi-hundred-person drops and maintain longitudinal continuity for municipal budget planning and police/outreach resource allocation, DSDP **intentionally continued tracking and calculating adjusted counts** using the May 2018 multipliers ($1.75$ tent / $2.03$ vehicle).
* **Empirical Multipliers in Dataset:**
  * Individuals: $1.0000$ (405 rows audited, 100% match)
  * Tents: $1.7500$ (350 rows audited, 100% match)
  * Vehicles: $2.0300$ (147 rows audited, 100% match)
* **Confirmation:** Analysis confirms that DSDP's continued application of the $1.75$ / $2.03$ multiplier schedule is deliberate, valid, and fully documented across all monthly packets from 2020 through 2025.

---

## 3. Summary of Methodology Regimes

| Regime | Time Horizon | Indiv Multiplier | Tent Multiplier | Vehicle Multiplier | Source Documentation | Breakout Availability |
| :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| **`PRE2017`** | Jan 2017 – Mar 2017 | $1.00$ | $2.00$ | $2.00$ | RTFH PIT Baseline | No (Totals Only) |
| **`APR2017`** | Apr 2017 – May 2018 | $1.00$ | $1.75$ | $1.66$ | RTFH 2017 Adjustment | Yes (from Jan 2018) |
| **`MAY2018`** | Jun 2018 – Dec 2019 | $1.00$ | $1.75$ | $2.03$ | RTFH 2018 Adjustment | Yes |
| **`POST2020`** | Jan 2020 – Present | $1.00$ | $1.75$ | $2.03$ | DSDP Internal Continuity | Yes |

---

## 4. Modeling Implications & Recommendations for Assignments 2–10

1. **Longitudinal Time Series Consistency (Assignments 4 & 7):**
   * Multiplier shifts create artificial level shifts in `total_count` (e.g., May 2018 bump of $+0.37$ per vehicle).
   * **Recommendation:** Use `raw_count` as the primary target variable for structural break testing and time-series forecasting (ARIMA / Prophet). When presenting final community forecasts, scale forecasts by the contemporary multiplier structure.
2. **Sub-Area Spatial Modeling (Assignments 3 & 5):**
   * East Village quadrants only exist as unadjusted raw counts. Re-weight quadrants proportionally to East Village's adjusted total when evaluating fine-grained spatial density.