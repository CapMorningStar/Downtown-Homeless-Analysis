# Dashboard Maintenance Guide
## Downtown San Diego Homeless Population Analysis (Task 9.4)

**Audience:** whoever maintains the dashboard and data pipelines after handoff
**Repository:** `CapMorningStar/Downtown-Homeless-Analysis` (branch `main`)
**Entry point:** `app.py` (Streamlit)
**Version:** October 2026
**Related:** [`ProjectHandoff_OperationalRunbook.md`](ProjectHandoff_OperationalRunbook.md) (original runbook), [`FutureEnhancement_Roadmap.md`](FutureEnhancement_Roadmap.md), [`FullTechnicalReport.md`](FullTechnicalReport.md) §10

This guide replaces the maintenance parts of the September runbook. Script names, paths and parameters below were checked against the repository in October 2026.

---

## 1. Environment

| Item | Value |
|---|---|
| Cloud runtime | Python 3.11 (`runtime.txt`) |
| Local development | Python 3.13 virtual environment in `.venv/` (the test suite passes on it) |
| Dependencies | `requirements.txt` (minimum versions, not pinned) |
| Theme and server settings | `.streamlit/config.toml` (port 8501) |
| Dashboard configuration and model constants | `src/config.py` |

Set up locally:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py        # http://localhost:8501
```

> **Deployment status.** `docs/Dashboard_DeploymentInfo.md` names `https://downtown-sd-homelessness.streamlit.app` as the target URL. Confirm that it loads in a logged-out browser before quoting it anywhere.

---

## 2. Dashboard structure

| Tab | File | Main data |
|---|---|---|
| Header | `src/components/header.py` | — |
| 1. Historical trends | `src/components/tab1_historical.py` | `data/MasterCounts_Adjusted_v2.csv` |
| 2. Forecast | `src/components/tab2_forecast.py` | `data/Forecasts_12Month.csv` |
| 3. Hotspots | `src/components/tab3_hotspots.py` | `data/Hotspot_Classifications.geojson`, persistence ranking, `data/Downtown_BlockGrid.geojson` |
| 4. Decomposition | `src/components/tab4_decomposition.py` | time-series outputs |
| 5. County calculator | `src/components/tab5_calculator.py` | constants in `src/config.py` |
| 6. About | `src/components/tab6_about.py` | — |
| 7. Anomalies | `src/components/tab7_anomalies.py` | `data/Anomaly_Surveillance_Matrix.csv`, `data/Alerts_History.*` |

All file loading goes through `src/data_loader.py`.

---

## 3. Routine procedures

### 3.1 Monthly: new DSDP count report

**Trigger:** DSDP publishes a monthly Unhoused Care report.

1. Download the PDF from the DSDP Unhoused Care page into `data/pdfs/`, and add its link to `data/dsdp_pdf_links.csv`.
2. For each area, enter the individual, tent, vehicle and total counts into `data/RawCounts_AllYears_clean.csv`. Use the canonical names in `data/Neighborhood_Crosswalk.csv` (for example `Core` → `City Center`).
3. Check the figures against the PDF:
   * The neighborhood total must match the published headline.
   * The East Village quadrants should add up to the East Village total.
   * If DSDP's own pages disagree with each other, record the month in `data/MasterCounts_QA_Flags.csv` rather than changing values.
4. If a published value is a proven typo, add a row to `data/source_corrections.csv` (with PDF file, page and note). Then rebuild:
   ```bash
   .venv/bin/python scripts/apply_source_corrections.py
   ```
   Current multipliers (May 2018 onward): individual 1.00, tent 1.75, vehicle 2.03.
5. Re-run the downstream steps in order:
   ```bash
   .venv/bin/python scripts/seasonal_indices.py
   .venv/bin/python scripts/structural_breaks.py
   .venv/bin/python scripts/constant_methodology.py
   .venv/bin/python forecast_pipeline.py --horizon 12
   ```
   The Assignment 4 and 7 notebooks (`TimeSeries_Decomposition.ipynb`, `Stationarity_Autocorrelation.ipynb`, `Forecasting_Models.ipynb`) must be re-executed if their outputs are needed.
6. Run the checks in §4, commit, and push to `main`.

### 3.2 Annual: new RTFH Point-in-Time count

**Trigger:** RTFH publishes the January PIT results (usually May–June).

1. Add the new year to `data/Downtown_County_PairedCounts.csv`, using the January downtown count from `data/MasterCounts_Adjusted_v2.csv`.
2. Re-run the county model build. It runs LOOCV, refits the model, and regenerates `data/CountyEstimate_Current.csv`:
   ```bash
   .venv/bin/python scripts/county_estimation_build.py
   ```
3. Copy the new coefficients and error terms into `src/config.py`: `BETA_0`, `BETA_1`, `BETA_2`, `SIGMA_EPSILON`, `X_BAR`, `VAR_X`, and `STUDENT_T_CRITICAL_95` (df = N − 3).
4. Re-test whether the post-2023 regime term is still justified. Add a new regime indicator only when there is a documented policy change.
5. Update the county figures in `docs/ExecutiveSummary_NonTechnical.md` and `docs/FullTechnicalReport.md`. Every published estimate must follow the four communication rules: no single exact number, round to 100, give the 95% range, and disclose the policy regime.

### 3.3 Multi-source system (Assignment 10)

Run when new external data are available, or monthly after §3.1:

```bash
.venv/bin/python scripts/run_ingestion_pipeline.py --all --validate
.venv/bin/python feature_engineering.py --generate --analyze
.venv/bin/python ensemble_model.py --train --evaluate --ablation --plot
.venv/bin/python anomaly_detection.py --detect --validate --plot
```

For scheduled runs (cron or Airflow), use `scripts/run_scheduled_anomaly_detection.sh`. It writes logs to `data/logs/` and calls `anomaly_detection.py --schedule --send`.

> **Known data limitation.** Shelter-capacity inputs are placeholders written in `data_ingestion/sources/shelter_capacity.py`, not administrative records. The 311 `mean_resolution_days` field is unreliable. See `docs/MultiSource_DataDocumentation.md`.

### 3.4 Hotspots (Assignment 5)

Re-run only when new block-level maps are digitized:

```bash
.venv/bin/python scripts/hotspot_analysis.py --permutations 9999
```

* Use the balanced 261-block panel for any comparison across 2021/2022.
* Hotspot classes are 95% and 99% only.
* Add any newly digitized date to `DIGITIZED_COUNT_DATES` in `src/config.py`.

---

## 4. Checks before every push to `main`

```bash
.venv/bin/pytest                                  # all tests must pass
.venv/bin/python scripts/validate_reports.py      # Task 9.2 report checks
.venv/bin/python scripts/validate_presentation.py # Task 9.3 deck checks
.venv/bin/python scripts/validate_handoff.py      # Task 9.4 handoff checks
```

Every command must exit with code 0. Also confirm that `git status` shows no stray outputs (`data/_pre_fix_snapshot/` and logs are git-ignored).

---

## 5. Deploying and refreshing the cloud app

1. Push to `main`. Streamlit Community Cloud redeploys automatically.
2. If the app shows stale data, open the app's menu in Streamlit Cloud and choose **Reboot app**.
3. If a build fails, check the cloud logs for dependency errors. Libraries that need system compilers (for example some `geopandas` back-ends) are the usual cause. Keep `requirements.txt` compatible with the standard Linux image.
4. If you change `runtime.txt`, test locally on that Python version first.

---

## 6. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Tab shows old numbers after a data update | Streamlit cache | Press `C` in the app or reboot the cloud app |
| Hotspot map is empty for a date | Date in `DIGITIZED_COUNT_DATES` does not match a `count_date` in `Hotspot_Classifications.geojson` | Make the config list match the dates in the GeoJSON |
| County calculator disagrees with the report | `src/config.py` constants not updated after §3.2 | Copy values from the latest `county_estimation_build.py` output |
| `forecast_pipeline.py` fails on a new month | Missing or unreleased months | Leave unreleased months as `NaN` (never 0); the pipeline interpolates them in memory |
| Ingestion uses synthetic weather or events | Offline with no cache | Re-run with network access; check `data/raw/` caches |

---

## 7. Data rules that must not be broken

1. Never overwrite the original source CSVs. Corrections go through `data/source_corrections.csv`.
2. Unreleased months stay `NaN`, never 0.
3. Comparisons across 2021/2022 use the balanced 261-block panel or report the footprint share.
4. County estimates are published only as rounded ranges under the four communication rules.
5. Do not use the county estimate for HUD submissions, formula funding, or sub-regional allocations.
