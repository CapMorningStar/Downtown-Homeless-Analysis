# Downtown San Diego Homeless Population Forecasting Pipeline Documentation

**Author:** Kyaw Soe Lwin (Data Science Alliance / UC San Diego)  
**Project:** Downtown San Diego Homeless Population Analysis  
**Assignment:** 7 — Forecasting Model Development  
**Task:** 7.4 — Generate Forecast Outputs and Build Automated Pipeline  
**Version:** 1.0.0 (Production Release)  
**Date:** September 2026  

---

## 1. Executive Summary & Overview

The **Autonomous Production Forecasting Pipeline** (`forecast_pipeline.py`) provides a robust, self-contained operational system for generating forward-looking unsheltered homeless population estimates across Downtown San Diego and its seven constituent sub-neighborhoods.

Transitioning from retrospective backtesting (Tasks 7.1–7.3) to forward operational deployment, the pipeline synthesizes multi-family econometric and machine learning champion architectures:
- **Recursive XGBoost**: Primary champion for high-momentum, non-linear series (Headline Footprint, Fixed Core Six, East Village, City Center, Cortez).
- **SARIMA (Seasonal Autoregressive Integrated Moving Average)**: Primary champion for differenced, stationary sub-markets (Columbia, Outside Perimeter).
- **Prophet (Additive Generalized Additive Model)**: Primary champion for bounded, calendar-driven series (Gaslamp, Marina).
- **Holt-Winters Triple Exponential Smoothing**: Dual-purpose role as high-accuracy parametric forecast and **variance calibration anchor** for expanding prediction intervals.

The pipeline outputs:
1. **12-Month Forward Point Projections** (`2026-01-01` to `2026-12-01`).
2. **Statistically Calibrated Prediction Intervals** (80% and 95% confidence bands).
3. **Policy Scenario Projections** (Optimistic, Baseline, Pessimistic bounds).
4. **Publication-Quality Visualizations** (`figures/task7_4/`).

---

## 2. System Architecture & Methodology

```
                                  [ Historical Data ]
                           (TimeSeries_ConstantMethodology.csv)
                                           │
                                           ▼
                           [ Ingestion & Interpolation ]
                            (asfreq('MS') + linear interp)
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    ▼                                             ▼
        [ Champion Model Forecast ]                 [ Parametric Variance Anchor ]
       (XGBoost / SARIMA / Prophet)                         (Holt-Winters)
                    │                                             │
                    │ Point Forecast (ŷ)                          │ Residual Std (σ̂_res)
                    └──────────────────────┬──────────────────────┘
                                           │
                                           ▼
                           [ Horizon Scaling & Bounds ]
                            σ̂_h = σ̂_res · √(1 + 0.08·(h-1))
                           PI_80 = max(0, ŷ ± 1.282·σ̂_h)
                           PI_95 = max(0, ŷ ± 1.960·σ̂_h)
                                           │
                                           ▼
                           [ Policy Scenario Projections ]
                         Optimistic:   ŷ · (1 - 0.020·h)
                         Pessimistic:  ŷ · (1 + 0.022·h)
                                           │
                                           ▼
                             [ Data & Plot Deliverables ]
                             - data/Forecasts_12Month.csv
                             - figures/task7_4/*.png
```

### 2.1 Ingestion and Data Quality Assurance
- **Source Verification:** The pipeline ingests `data/TimeSeries_ConstantMethodology.csv` and cross-references `data/AdjustedTimeSeries_Forecasting.csv` to ensure source datasets remain unaltered.
- **Frequency Regularization:** Historical missing months (specifically unreleased DSDP reports in 2025: Jul, Aug, Oct, Nov) are linearly interpolated in-memory to maintain a strict continuous monthly frequency (`freq='MS'`), preventing date index discontinuities in state-space estimators.

### 2.2 Champion Model Assignment Matrix
Model architectures were empirically selected based on lowest 12-month expanding-window Cross-Validation Mean Absolute Percentage Error (CV MAPE) evaluated across 5 historical folds (1996–2024):

| Geographic Series | Champion Architecture | 12-Mo CV MAPE | CV Std Dev ($\sigma$) | Selection Rationale |
|---|---|---|---|---|
| **Overall — reported footprint** | **XGBoost** | **39.34%** | 12.08% | Captures non-linear encampment dispersion and post-ordinance regime shifts. |
| **Overall — fixed core six** | **XGBoost** | **22.26%** | 9.47% | Outstanding accuracy across multi-year trends; lowest variance across all models. |
| **East Village** | **XGBoost** | **34.55%** | 11.23% | Effectively models dense encampment clustering and displacement elasticity. |
| **City Center** | **XGBoost** | **30.13%** | 14.61% | Robust tracking of commercial corridor sweeps. |
| **Cortez** | **XGBoost** | **37.22%** | 18.04% | Handles boundary elevation and localized park relocations. |
| **Columbia** | **SARIMA** | **30.54%** | 12.80% | Stationary differencing handles low baseline with occasional transient spikes. |
| **Gaslamp** | **Prophet** | **28.83%** | 10.15% | Excels at capturing tourism, convention, and seasonal entertainment cycles. |
| **Marina** | **Prophet** | **45.84%** | 19.30% | Resilient handling of very low count baseline (mean count ~10-15). |
| **Outside Perimeter** | **SARIMA** | **561.09%** | 312.4% | Handles structural boundary addition (zero counts prior to 2021 expansion). |

### 2.3 Prediction Interval Formulation
Recursive gradient boosted trees do not natively yield parametric prediction intervals. To provide rigorous, statistically sound intervals:
1. Residual variance is anchored on **Holt-Winters Triple Exponential Smoothing** (`ExponentialSmoothing(trend='add', seasonal='add'/'mul')`), which achieved 39.57% CV MAPE on headline footprint.
2. In-sample residual standard deviation ($\hat{\sigma}_{\text{res}}$) is scaled by a horizon-expanding variance function:
   $$\hat{\sigma}_h = \hat{\sigma}_{\text{res}} \cdot \sqrt{1.0 + 0.08 \cdot (h - 1)}, \quad \text{for } h \in \{1, 2, \dots, 12\}$$
3. Calibrated interval bounds:
   $$\text{PI}_{80\%}(h) = \left[ \max\left(0, \hat{y}_h - 1.282 \hat{\sigma}_h\right), \; \hat{y}_h + 1.282 \hat{\sigma}_h \right]$$
   $$\text{PI}_{95\%}(h) = \left[ \max\left(0, \hat{y}_h - 1.960 \hat{\sigma}_h\right), \; \hat{y}_h + 1.960 \hat{\sigma}_h \right]$$
4. **Physical Non-Negativity:** All lower bounds are clipped at 0.0, as unsheltered individual counts cannot be negative.

### 2.4 Policy Scenario Projections
To support municipal capacity planning, public health outreach, and budget allocation, three distinct policy scenarios are projected alongside statistical intervals:

1. **Baseline Scenario ($\hat{y}_h$):**
   - Pure statistical continuation under current policy dynamics (active enforcement of San Diego's Unsafe Camping Ordinance, steady-state shelter utilization).
2. **Optimistic Scenario ($\hat{y}_h^{\text{opt}}$):**
   - **Operational Mechanism:** Rapid activation of planned shelter capacity (e.g., Safe Sleeping sites, Kettner & Vine shelter intake, rapid-rehousing vouchers).
   - **Formulation:** $\hat{y}_h^{\text{opt}} = \max\left(0, \hat{y}_h \cdot (1 - 0.020 \cdot h)\right)$, delivering an incremental 2.0% monthly reduction reaching a **-24.0% contraction** relative to baseline by Month 12.
3. **Pessimistic Scenario ($\hat{y}_h^{\text{pess}}$):**
   - **Operational Mechanism:** Congregate shelter bed exhaustion, legal injunctions halting encampment enforcement, adverse macroeconomic inflation, or winter storm shelter displacement.
   - **Formulation:** $\hat{y}_h^{\text{pess}} = \hat{y}_h \cdot (1 + 0.022 \cdot h)$, delivering an incremental 2.2% monthly increase reaching a **+26.4% expansion** above baseline by Month 12.

---

## 3. Command-Line Interface (CLI) & Operational Usage

### 3.1 Script Execution
The production pipeline is packaged as a standalone, zero-external-state Python CLI script located at `forecast_pipeline.py`.

```bash
# Basic run with default parameters (12-month horizon, standard paths)
python forecast_pipeline.py

# Custom execution specifying input/output paths and 6-month horizon
python forecast_pipeline.py --input data/TimeSeries_ConstantMethodology.csv \
                            --output data/Forecasts_6Month.csv \
                            --horizon 6 \
                            --export-plots
```

### 3.2 CLI Argument Reference
| Parameter | Type | Default | Description |
|---|---|---|---|
| `--input` | Path | `data/TimeSeries_ConstantMethodology.csv` | Path to verified continuous constant-methodology monthly count CSV. |
| `--adjusted` | Path | `data/AdjustedTimeSeries_Forecasting.csv` | Path to adjusted forecasting CSV (supplies candidate $(p,d,q)$ orders). |
| `--output` | Path | `data/Forecasts_12Month.csv` | Destination filepath for the consolidated 12-month forecast table. |
| `--horizon` | Integer | `12` | Number of forward monthly steps to project. |
| `--export-plots` | Flag | `True` | Automatically exports publication-quality PNG charts to `figures/task7_4/`. |

### 3.3 Programmatic Python API
Municipal data science teams can import and embed pipeline functions directly into ETL workflows:

```python
from pathlib import Path
from forecast_pipeline import generate_forecasts, export_visualizations

# Ingest and execute
input_file = Path("data/TimeSeries_ConstantMethodology.csv")
df_forecasts, const_pivot, future_dates = generate_forecasts(input_file, horizon=12)

# Save deliverables
df_forecasts.to_csv("data/Forecasts_12Month.csv", index=False)
export_visualizations(df_forecasts, const_pivot, future_dates, Path("figures/task7_4"))
```

---

## 4. Deliverable Data Schema (`data/Forecasts_12Month.csv`)

The primary output deliverable contains 108 records (9 series $\times$ 12 months) structured under the canonical schema:

| Column Name | Type | Example | Description |
|---|---|---|---|
| `forecast_date` | Date (`YYYY-MM-01`) | `2026-06-01` | First day of the forecast calendar month. |
| `series` | String | `East Village` | Target geographic zone or aggregate footprint. |
| `model` | String | `xgboost` | Underlying champion model architecture. |
| `point_forecast` | Float | `547.04` | Expected unsheltered individual count. |
| `pi_80_lower` | Float | `432.27` | Lower boundary of 80% prediction interval ($\ge 0$). |
| `pi_80_upper` | Float | `661.82` | Upper boundary of 80% prediction interval. |
| `pi_95_lower` | Float | `371.57` | Lower boundary of 95% prediction interval ($\ge 0$). |
| `pi_95_upper` | Float | `722.52` | Upper boundary of 95% prediction interval. |
| `scenario_optimistic` | Float | `481.40` | Projected count under accelerated shelter intake. |
| `scenario_baseline` | Float | `547.04` | Projected count under status-quo policy continuity. |
| `scenario_pessimistic`| Float | `619.25` | Projected count under shelter capacity constraints. |

---

## 5. Operations Runbook & Retraining Cadence

To maintain forecast validity as new monthly data are released, municipal operators should follow this standard maintenance protocol:

### 5.1 Monthly Refresh Protocol (Trigger: DSDP Monthly PDF Release)
1. **Release Timing:** Downtown San Diego Partnership typically publishes the monthly count during the second week following the survey month.
2. **Data Ingestion:** Append the newly verified monthly counts to `data/TimeSeries_ConstantMethodology.csv`.
3. **Pipeline Execution:** Run `python forecast_pipeline.py`.
4. **Validation Check:** Verify that new forecasts align logically with the latest observed counts. Confirm that `df_forecasts.isnull().sum().sum() == 0`.

### 5.2 Quarterly Hyperparameter Review (Trigger: Every 3 Months)
- Re-evaluate rolling window statistics and seasonal lag weights in `build_xgb_features`.
- Check whether residual standard deviation ($\hat{\sigma}_{\text{res}}$) has shifted by more than $\pm 20\%$.

### 5.3 Annual Structural Audit (Trigger: January Annual Review)
- Re-run full 5-fold expanding-window cross-validation (`build_forecasting_cv.py`) to confirm whether champion model assignments remain optimal.
- Evaluate potential new changepoints caused by major municipal infrastructure changes or state/federal policy modifications.

---

## 6. Performance Monitoring & Drift Detection Alerts

The operational pipeline implements proactive threshold monitoring:

| Alert Type | Condition | Diagnostic Action |
|---|---|---|
| **Out-of-Bounds Alert** | Observed actual count falls outside the 95% prediction interval. | Investigate localized operational anomalies (e.g., concentrated police sweep, shelter intake drive, extreme weather). |
| **Model Drift Warning** | Mean Absolute Error over the trailing 3 months exceeds $1.5 \times$ CV MAE. | Retrain model hyperparameters; consider updating changepoints. |
| **Negative Prediction Warning** | Model outputs raw value $< 0$. | Automatic zero-bound clipping applies; flag series for low-count zero-inflation review. |
| **Missing Gaps Alert** | Input data contains $> 2$ consecutive unreleased months. | Confirm interpolation method validity before publishing operational forecasts. |

---

## 7. Limitations & Risk Disclosures

1. **Unreleased Historical Reports:** Missing monthly reports in 2025 (months 7, 8, 10, 11) were interpolated linearly per the established project methodology. True unsheltered population counts during those unreleased months remain unobserved.
2. **Extreme Policy Shocks:** The statistical models assume that baseline legal frameworks (e.g., Unsafe Camping Ordinance) and shelter capacity constraints behave within historical bounds. Sudden legislative changes or catastrophic climate events could cause real-world counts to diverge from baseline forecasts.
3. **Outside Perimeter Series:** Because the "Outside Perimeter" study boundary was introduced in 2021, pre-2021 counts are zero-filled, leading to high relative percentage error metrics (CV MAPE $> 500\%$). Absolute error metrics (MAE ~30-50 individuals) should be referenced for operational planning in this zone.

---

*End of Documentation.*
