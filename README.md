# Downtown San Diego Homeless Population Analysis

Public interest analytics and data engineering volunteer project with the **Data Science Alliance**, analyzing unsheltered homeless population trends across Downtown San Diego (2012–present) using monthly count data from the Downtown San Diego Partnership (DSDP).

---

## Quick Reference & Links

* **Master Context & Memory File:** [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) *(Read this file in new chat sessions!)*
* **Asana Project:** [Downtown San Diego Homeless Population Analysis](https://app.asana.com/1/1211227519522850/project/1218064298575500/list)
* **Google Drive Deliverables:** [Shared Deliverables Folder](https://drive.google.com/drive/u/2/folders/1LUWFhKsbER-XSY8VJFVdt0cgVeuaQ6Ek)
  * [📁 Assignment 1 Deliverables Folder](https://drive.google.com/drive/u/2/folders/1qkwbmPe87IRlsnm1cJMub5NNMsWvukLH)
* **Source Reports Archive:** [DSDP Unhoused Care Reports](https://downtownsandiego.org/clean-and-safe/unhoused-care/)

---

## Current Status

* **Assignment 1: Data Validation, Cleaning & Standardization** — 100% COMPLETE (Tasks 1.1–1.4)
  * **Task 1.1:** Complete. Verified 45-cell audit against 32 source PDFs; created & uploaded [`DataValidation_SourceCheck.md`](DataValidation_SourceCheck.md).
  * **Task 1.2:** Complete. Standardized month strings (`Jan`–`Dec`), added ISO `date` (`YYYY-MM-01`), resolved `BlockLevel_Counts` single null, generated [`Neighborhood_Crosswalk.csv`](data/Neighborhood_Crosswalk.csv), and uploaded all 5 clean datasets (`_clean.csv`) to Drive.
  * **Task 1.3:** Complete. Rebuilt canonical adjusted totals $\rightarrow$ [`MasterCounts_Adjusted_v2.csv`](data/MasterCounts_Adjusted_v2.csv).
  * **Task 1.4:** Complete. Data dictionary, methodology log, and quality report published to `docs/` and Drive.
* **Assignment 2: Exploratory Data Analysis (EDA)** — CURRENT FOCUS
  * **Task 2.1:** Complete. Built & executed [`EDA_DowntownCounts.ipynb`](EDA_DowntownCounts.ipynb) — summary statistics, monthly seasonality, YoY % change, and top-3-neighborhood rankings by count and by growth rate.
  * **Task 2.2:** Complete. Added 10 required charts (time series, seasonality, neighborhood composition, EV sub-areas, methodology before/after, YoY comparisons, COVID period, adjustment gap, distribution) with titles, labels, legends, source attribution, and commentary — same notebook.
  * **Task 2.3:** In progress. [`EDA_SummaryReport.md`](EDA_SummaryReport.md) written (7 required sections + 4 hypotheses), uploaded as a Google Doc to Drive; notebook exported to [`EDA_DowntownCounts.pdf`](EDA_DowntownCounts.pdf) and uploaded to Drive. Slide deck (6-8 slides) being built in Canva.
  * **Task 2.3:** Queued (summary report & presentation).

See [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) for full architectural documentation, schemas, and historical logs.
