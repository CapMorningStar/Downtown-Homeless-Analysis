"""
Task 3.4: Reconcile coverage table and document digitization methodology.

This script:
  1. Confirms the "block" column mislabeling identified in the task notes was
     already corrected in Task 1.2: BlockMap_Coverage_clean.csv holds the raw
     label as `source_area` and the crosswalk-mapped canonical parent as
     `neighborhood`. Verifies every source_area value has a crosswalk entry.
  2. Quantifies the digitization gap: BlockMap_Coverage_clean.csv spans 96
     year-months (2018-2025) across up to 10 source areas, but only 12
     year-months were ever digitized into BlockLevel_Counts_clean.csv.
  3. Confirms every digitized count date has a corresponding coverage row
     marked "Yes", and flags any digitized year-month drawn from a map rated
     "Unclear".

Outputs:
  - data/BlockMapCoverage_GapAnalysis.csv: per-year-month digitization status
  - Console summary used to write BlockMapCoverage_GapAnalysis.md
"""
import pandas as pd

COV = "data/BlockMap_Coverage_clean.csv"
BLOCKS = "data/BlockLevel_Counts_clean.csv"
CROSSWALK = "data/Neighborhood_Crosswalk.csv"
OUT = "data/BlockMapCoverage_GapAnalysis.csv"

cov = pd.read_csv(COV, parse_dates=["date"])
bl = pd.read_csv(BLOCKS, parse_dates=["count_date"])
xwalk = pd.read_csv(CROSSWALK)

# --- 1. Confirm the column-rename fix from Task 1.2 and crosswalk completeness ---
assert "source_area" in cov.columns and "neighborhood" in cov.columns and "block" not in cov.columns, (
    "Expected BlockMap_Coverage_clean.csv to already have source_area/neighborhood, not block"
)
cov_areas = set(cov["source_area"].unique())
xwalk_labels = set(xwalk["source_label"].unique())
unmapped = cov_areas - xwalk_labels
print(f"=== Column-rename & crosswalk check ===")
print(f"source_area values in coverage table: {sorted(cov_areas)}")
print(f"Unmapped source_area values (not in crosswalk): {sorted(unmapped) if unmapped else 'NONE — all mapped'}")

# --- 2. Quantify the digitization gap ---
cov["year_month"] = cov["date"].dt.to_period("M")
bl["year_month"] = bl["count_date"].dt.to_period("M")
digitized_ym = set(bl["year_month"].unique())

total_ym = cov["year_month"].nunique()
avail_ym = set(cov.loc[cov["block_map"] == "Yes", "year_month"].unique())
undigitized_available = sorted(avail_ym - digitized_ym)

print(f"\n=== Digitization gap ===")
print(f"Total year-months in coverage table: {total_ym}")
print(f"Year-months with >=1 map present (Yes): {len(avail_ym)}")
print(f"Year-months actually digitized: {len(digitized_ym)}")
print(f"Year-months with a usable map but NOT digitized: {len(undigitized_available)}")
print(f"Digitization rate (of available maps): {len(digitized_ym)/len(avail_ym)*100:.1f}%")

# Per-year breakdown of available-but-undigitized months
gap_by_year = pd.Series([ym.year for ym in undigitized_available]).value_counts().sort_index()
print(f"\nUndigitized-but-available months by year:\n{gap_by_year.to_string()}")

# --- 3. Validate digitized dates against coverage, flag Unclear maps used ---
rows = []
for ym in sorted(digitized_ym):
    sub = cov[cov["year_month"] == ym]
    n_rows = len(sub)
    n_yes = (sub["block_map"] == "Yes").sum()
    n_unclear_used = ((sub["block_map"] == "Yes") & (sub["map_quality"] == "Unclear")).sum()
    unclear_areas = sub.loc[(sub["block_map"] == "Yes") & (sub["map_quality"] == "Unclear"), "source_area"].tolist()
    all_yes = n_yes == n_rows and n_rows > 0
    rows.append({
        "year_month": str(ym),
        "coverage_rows": n_rows,
        "rows_marked_yes": n_yes,
        "all_rows_yes": all_yes,
        "unclear_maps_used": n_unclear_used,
        "unclear_source_areas": ", ".join(unclear_areas) if unclear_areas else "",
    })
digitized_check = pd.DataFrame(rows)
print(f"\n=== Digitized-date coverage validation ===")
print(digitized_check.to_string(index=False))

# --- Build the full per-year-month gap analysis output ---
summary = (
    cov.groupby("year_month")
    .agg(
        coverage_rows=("block_map", "size"),
        maps_present=("block_map", lambda s: (s == "Yes").sum()),
        maps_clear=("map_quality", lambda s: (s == "Clear").sum()),
        maps_unclear=("map_quality", lambda s: (s == "Unclear").sum()),
    )
    .reset_index()
)
summary["digitized"] = summary["year_month"].isin(digitized_ym)
summary["year_month"] = summary["year_month"].astype(str)
summary = summary.sort_values("year_month")
summary.to_csv(OUT, index=False)
print(f"\nSaved: {OUT} ({len(summary)} year-months)")
