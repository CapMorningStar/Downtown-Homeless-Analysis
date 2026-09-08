"""
Task 3.3: Document and correct the unbalanced spatial panel.

Confirmed issue: block-level coverage is not constant over time.
  - 2018-01-24 through 2021-02-25 (7 dates): 261 blocks each.
  - 2022-01-27 through 2025-01-31 (5 dates): 382 blocks each.
The 121 blocks added from 2022 onward are exactly Golden Hill (52),
Barrio Logan (35), and Sherman Heights (34) -- three neighborhoods
absent from every count date before 2022.

This script:
  1. Quantifies how much of the post-2021 total is attributable to the
     expanded footprint vs. a real change in counts, by comparing the
     full 382-block total against a 261-block-restricted total for
     every post-2021 date.
  2. Builds and saves a balanced 261-block panel spanning all 12 dates
     for valid temporal comparison (data/BlockPanel_Balanced_261.csv).
  3. Leaves the full 382-block file untouched for recent-period analysis.

Weighted "adjusted total" per block-date uses the documented multiplier
schedule (docs/MethodologyChangeLog.md):
  individuals x 1.00 + tents_structures x 1.75 + vehicles x (vehicle_mult)
  vehicle_mult = 1.66 for dates before 2018-06-01 (APR2017 regime)
              = 2.03 for dates on/after 2018-06-01 (MAY2018/POST2020 regime)
"""
import pandas as pd

SRC = "data/BlockLevel_Counts_clean.csv"
OUT_PANEL = "data/BlockPanel_Balanced_261.csv"
OUT_SUMMARY = "data/SpatialPanel_FootprintEffect.csv"

NEW_NEIGHBORHOODS = {"Golden Hill", "Barrio Logan", "Sherman Heights"}

df = pd.read_csv(SRC, parse_dates=["count_date"])

# --- Sanity: confirm the known coverage split ---
counts_per_date = df.groupby("count_date")["block_id"].nunique().sort_index()
assert set(counts_per_date[counts_per_date.index < "2022-01-01"].unique()) == {261}
assert set(counts_per_date[counts_per_date.index >= "2022-01-01"].unique()) == {382}

# --- Identify the balanced 261-block set (present on every date) ---
n_dates = df["count_date"].nunique()
block_date_counts = df.groupby("block_id")["count_date"].nunique()
balanced_block_ids = set(block_date_counts[block_date_counts == n_dates].index)
assert len(balanced_block_ids) == 261, f"expected 261, got {len(balanced_block_ids)}"

# Cross-check: the excluded blocks are exactly the 3 new neighborhoods
excluded = df.loc[~df["block_id"].isin(balanced_block_ids), "neighborhood"].unique()
assert set(excluded) == NEW_NEIGHBORHOODS, excluded

# --- Weighted adjusted total per block-date (per documented multipliers) ---
vehicle_mult = df["count_date"].apply(lambda d: 1.66 if d < pd.Timestamp("2018-06-01") else 2.03)
df["adjusted_total"] = (
    df["individuals"] * 1.00
    + df["tents_structures"] * 1.75
    + df["vehicles"] * vehicle_mult
)

# --- 1. Quantify the footprint-expansion effect for post-2021 dates ---
post = df[df["count_date"] >= "2022-01-01"].copy()
full_totals = post.groupby("count_date")["adjusted_total"].sum().rename("full_382_total")
balanced_totals = (
    post[post["block_id"].isin(balanced_block_ids)]
    .groupby("count_date")["adjusted_total"]
    .sum()
    .rename("balanced_261_total")
)
footprint = pd.concat([full_totals, balanced_totals], axis=1)
footprint["expansion_delta"] = footprint["full_382_total"] - footprint["balanced_261_total"]
footprint["expansion_pct_of_full"] = (
    footprint["expansion_delta"] / footprint["full_382_total"] * 100
).round(2)
footprint = footprint.round(2).reset_index()
footprint.to_csv(OUT_SUMMARY, index=False)

print("=== Footprint-expansion effect (post-2021 dates) ===")
print(footprint.to_string(index=False))

# --- 2. Build and save the balanced 261-block panel (all 12 dates) ---
balanced_panel = df[df["block_id"].isin(balanced_block_ids)].drop(columns=["adjusted_total"]).copy()
balanced_panel = balanced_panel.sort_values(["count_date", "block_id"]).reset_index(drop=True)
assert balanced_panel.shape[0] == 261 * n_dates, balanced_panel.shape

balanced_panel.to_csv(OUT_PANEL, index=False)
print(f"\nSaved balanced panel: {OUT_PANEL} ({balanced_panel.shape[0]} rows, "
      f"{balanced_panel['block_id'].nunique()} blocks x {n_dates} dates)")
print(f"Saved footprint-effect summary: {OUT_SUMMARY}")
