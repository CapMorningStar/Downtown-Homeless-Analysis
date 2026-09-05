# Data Dictionary: Downtown San Diego Homeless Population Analysis

**Project Title:** Downtown San Diego Homeless Population Analysis  
**Organization:** Data Science Alliance (Volunteer / Public Interest Analytics)  
**Author / Analyst:** Kyaw Soe Lwin (`kylwin@ucsd.edu`)  
**Project Lead:** Adir Mancebo Jr. (`adir@datasciencealliance.org`)  
**Scope:** Covers all 6 cleaned and validated project datasets in `data/`.

---

## 1. Overview of Delivered Files

| File Name | Record Count | Column Count | Primary Granularity | Description |
| :--- | :---: | :---: | :--- | :--- |
| **`MasterCounts_Adjusted_v2.csv`** | 2,814 | 10 | Area × Month × Component | Canonical reconciled adjusted monthly counts (2017–2025) with rebuilt totals. |
| **`RawCounts_AllYears_clean.csv`** | 2,814 | 8 | Area × Month × Component | Cleaned raw observed monthly counts directly from DSDP count packets. |
| **`BlockLevel_Counts_clean.csv`** | 3,737 | 7 | Block × Date | Digitized block-by-block counts across 12 monthly sample maps (2018–2020). |
| **`Downtown_BlockGrid_clean.csv`** | 382 | 9 | Block Polygon | Geospatial reference grid of all 382 Downtown San Diego census blocks with centroid coordinates and bounding streets. |
| **`BlockMap_Coverage_clean.csv`** | 843 | 7 | Area × Month | Inventory of monthly count PDF map availability and digitization quality (2018–2025). |
| **`Neighborhood_Crosswalk.csv`** | 18 | 6 | Mapping Lookup | Crosswalk standardizing 18 historical source labels to 7 canonical neighborhoods. |

---

## 2. Dataset Data Dictionaries

### 2.1. `MasterCounts_Adjusted_v2.csv` (Canonical Adjusted Counts)
* **Primary Key:** `(date, area, component)`
* **Row Count:** 2,814 rows | **Column Count:** 10 columns

| Column Name | Data Type | Valid Value Range | Description & Context | Source File / Provenance | Known Issues / Caveats |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `date` | `string` (ISO) | `2017-01-01` to `2025-12-01` | First day of the count month (`YYYY-MM-01`). Standard time series index. | Standardized from `year` and `month` | Counts occur on the final Wednesday/Thursday of the month. |
| `year` | `int64` | `2017` to `2025` | Calendar year of the count. | `MasterCounts_Adjusted.csv` | Series commences in 2017, not 2012. |
| `month` | `string` | `Jan`, `Feb`, `Mar`, `Apr`, `May`, `Jun`, `Jul`, `Aug`, `Sep`, `Oct`, `Nov`, `Dec` | Standardized 3-letter month abbreviation. | Standardized from irregular source months | None. |
| `area` | `string` | 7 Neighborhoods + 4 EV Sub-areas | Canonical neighborhood or sub-area name. | Mapped via `Neighborhood_Crosswalk.csv` | Core mapped to City Center. |
| `source_area` | `string` | 12 unique values | Original area string from DSDP raw reports. | `MasterCounts_Adjusted.csv` | Preserved for auditing. |
| `component` | `string` | `total`, `individual`, `tent`, `vehicle` | Count component layer. | `MasterCounts_Adjusted.csv` | Sub-areas only have `total`. |
| `area_type` | `string` | `neighborhood`, `sub-area` | Geographic classification of the row. | `MasterCounts_Adjusted.csv` | Sub-areas belong to East Village. |
| `method` | `string` | `PRE2017`, `APR2017`, `MAY2018`, `POST2020` | Multiplier regime in effect for this observation. | DSDP / RTFH methodology schedule | Fully audited in Task 1.3. |
| `raw_count` | `float64` | `[0.0, 921.0]` (134 nulls) | Directly observed count from field sheets before weighting. | DSDP monthly count tables | 116 nulls in 2025; 18 in Nov 2018. |
| `total_count` | `float64` | `[0.0, 921.05]` (134 nulls) | Adjusted count applying tent and vehicle multipliers. | Rebuilt in Task 1.3 ($\sum 	ext{components}$) | 0.00 residual diff against components. |

---

### 2.2. `RawCounts_AllYears_clean.csv` (Raw Field Counts)
* **Primary Key:** `(date, area, component)`
* **Row Count:** 2,814 rows | **Column Count:** 8 columns

| Column Name | Data Type | Valid Value Range | Description & Context | Source File / Provenance | Known Issues / Caveats |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `date` | `string` (ISO) | `2017-01-01` to `2025-12-01` | First day of count month (`YYYY-MM-01`). | Derived | None. |
| `year` | `int64` | `2017` to `2025` | Calendar year. | `RawCounts_AllYears.csv` | None. |
| `month` | `string` | 12 standardized months | Standard 3-letter month code. | Cleaned | None. |
| `area` | `string` | 11 canonical areas | Canonical neighborhood or sub-area. | Mapped via crosswalk | Core converted to City Center. |
| `source_area` | `string` | 12 original names | Original area string from report. | `RawCounts_AllYears.csv` | Preserved for line audit. |
| `component` | `string` | `total`, `individual`, `tent`, `vehicle` | Count component layer. | `RawCounts_AllYears.csv` | Component breakouts start in 2018. |
| `count` | `float64` | `[0.0, 921.0]` (134 nulls) | Raw unweighted count from DSDP packet. | `RawCounts_AllYears.csv` | Identical null distribution to master. |
| `area_type` | `string` | `neighborhood`, `sub-area` | Geographic classification. | `RawCounts_AllYears.csv` | 384 sub-area rows total. |

---

### 2.3. `BlockLevel_Counts_clean.csv` (Digitized Block Map Counts)
* **Primary Key:** `(block_id, count_date)`
* **Row Count:** 3,737 rows | **Column Count:** 7 columns

| Column Name | Data Type | Valid Value Range | Description & Context | Source File / Provenance | Known Issues / Caveats |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `block_id` | `string` | 382 unique blocks | Standardized block identifier code (`STREET1_STREET2`). | `BlockLevel_Counts.csv` | Foreign key to `Downtown_BlockGrid`. |
| `neighborhood` | `string` | 7 canonical neighborhoods | Canonical neighborhood where block is located. | Mapped via crosswalk | Matches official GIS boundaries. |
| `source_neighborhood`| `string` | 10 source labels | Original neighborhood label from digitized PDF map. | `BlockLevel_Counts.csv` | Preserved for audit. |
| `count_date` | `string` (ISO) | 12 count dates (`2018-01-24` to `2020-01-31`) | Exact calendar date on which field count was conducted. | Cleaned (escaped quotes stripped) | Covers 12 specific sampled months. |
| `individuals` | `int64` | `[0, 64]` (0 nulls) | Count of unsheltered individuals on sidewalks/structures. | Digitized map annotations | 0 nulls. |
| `tents_structures` | `int64` | `[0, 76]` (0 nulls) | Count of tents and makeshift structures on the block. | Digitized map annotations | Row 930 null imputed to 0. |
| `vehicles` | `int64` | `[0, 5]` (0 nulls) | Count of inhabited vehicles on the block. | Digitized map annotations | 0 nulls. |

---

### 2.4. `Downtown_BlockGrid_clean.csv` (Geospatial Reference Grid)
* **Primary Key:** `block_id`
* **Row Count:** 382 rows | **Column Count:** 9 columns

| Column Name | Data Type | Valid Value Range | Description & Context | Source File / Provenance | Known Issues / Caveats |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `block_id` | `string` | 382 unique blocks | Standardized block identifier code. | `Downtown_BlockGrid.csv` | Matches GeoJSON `block_id`. |
| `neighborhood` | `string` | 7 canonical neighborhoods | Canonical neighborhood. | Mapped via crosswalk | Core mapped to City Center. |
| `source_neighborhood`| `string` | 10 source labels | Original neighborhood string. | `Downtown_BlockGrid.csv` | Preserved for audit. |
| `lon` | `float64` | `[-117.1706, -117.1349]` | Longitude of block polygon centroid (WGS84). | Computed GIS centroid | CRS84 standard. |
| `lat` | `float64` | `[32.6958, 32.7228]` | Latitude of block polygon centroid (WGS84). | Computed GIS centroid | CRS84 standard. |
| `st_north` | `string` | 46 unique street names | Northern bounding street of the block. | GIS attribute table | None. |
| `st_east` | `string` | 52 unique street names | Eastern bounding street of the block. | GIS attribute table | None. |
| `st_south` | `string` | 47 unique street names | Southern bounding street of the block. | GIS attribute table | None. |
| `st_west` | `string` | 53 unique street names | Western bounding street of the block. | GIS attribute table | None. |

---

### 2.5. `BlockMap_Coverage_clean.csv` (Map Digitization Inventory)
* **Primary Key:** `(date, neighborhood)`
* **Row Count:** 843 rows | **Column Count:** 7 columns

| Column Name | Data Type | Valid Value Range | Description & Context | Source File / Provenance | Known Issues / Caveats |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `date` | `string` (ISO) | `2018-01-01` to `2025-12-01` | First day of count month (`YYYY-MM-01`). | Derived | Maps begin in 2018. |
| `year` | `int64` | `2018` to `2025` | Calendar year. | `BlockMap_Coverage.csv` | None. |
| `month` | `string` | 12 standardized months | Standard 3-letter month abbreviation. | Standardized | None. |
| `neighborhood` | `string` | 7 canonical neighborhoods | Canonical neighborhood. | Mapped via crosswalk | None. |
| `source_area` | `string` | 10 source labels | Original area name from coverage tracker. | `BlockMap_Coverage.csv` | Preserved for audit. |
| `block_map` | `string` | `Yes`, `No` | Indicates whether a block-level map exists in the monthly packet. | DSDP PDF inventory | Not all months include maps. |
| `map_quality` | `string` | `Clear`, `Unclear`, `NaN` (1 null) | Legibility of street numbers/dots on the PDF map. | Visual inspection log | 1 unrated map row. |

---

### 2.6. `Neighborhood_Crosswalk.csv` (Translation Crosswalk)
* **Primary Key:** `source_label`
* **Row Count:** 18 rows | **Column Count:** 6 columns

| Column Name | Data Type | Valid Value Range | Description & Context | Source File / Provenance | Known Issues / Caveats |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `source_file` | `string` | Dataset source references | Files where the historical label appears. | Codebase audit | None. |
| `source_label` | `string` | 17 unique strings | Exact string as recorded in raw CSVs and PDFs. | Historical files | Includes legacy typos. |
| `canonical_neighborhood`| `string`| 7 canonical neighborhoods | Target unified neighborhood for analysis. | Official DSDP / City GIS | Core $ightarrow$ City Center. |
| `sub_area` | `string` | 7 sub-areas / `NaN` | Sub-area designation where applicable. | East Village / Perimeter | 9 rows are city-wide / general. |
| `area_type` | `string` | `neighborhood`, `sub-area`, `perimeter` | Classification of the geographic unit. | Domain specification | Governs aggregation hierarchy. |
| `notes` | `string` | Text explanations | Historical and administrative context for mapping. | Project audit log | Explains rebranding history. |