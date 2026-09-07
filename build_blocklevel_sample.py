"""
Task 3.1: Validate block-level counts against source maps
Step 2 - Draw a reproducible stratified sample of block-date records for
visual re-audit against the source maps.

Originally drawn at 10% (372 rows / 87 map pages). After scoping the
visual-audit workload against actual page counts and per-block boundary
irregularity (freeway/park-adjacent parcels), reduced to a fixed n=4 rows
per count_date (48 rows total) -- same order of magnitude as Task 1.1's
45-cell precedent -- while still guaranteeing every one of the 12 count
dates is represented. Uses random_state=42, matching that precedent.
"""
import pandas as pd

SRC = "data/BlockLevel_Counts_clean.csv"
OUT = "data/sample_blocklevel_verification.csv"
SEED = 42
N_PER_DATE = 4

df = pd.read_csv(SRC)

sample = (
    df.groupby("count_date", group_keys=False)[df.columns]
    .apply(lambda g: g.sample(n=N_PER_DATE, random_state=SEED))
    .sort_values(["count_date", "block_id"])
    .reset_index(drop=True)
)

# Columns for the auditor to fill in during the visual re-read (Step 3)
sample["source_individuals"] = ""
sample["source_tents_structures"] = ""
sample["source_vehicles"] = ""
sample["match"] = ""  # Y/N/PARTIAL, filled in after comparison
sample["notes"] = ""

sample.to_csv(OUT, index=False)

print(f"Total population: {len(df)} rows across {df['count_date'].nunique()} count dates")
print(f"Sample drawn: {len(sample)} rows ({len(sample)/len(df):.1%} of population, n={N_PER_DATE}/date)")
print(sample.groupby("count_date").size())
print(f"\nSaved to {OUT}")
