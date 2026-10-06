"""Assignment 5 (Tasks 5.1-5.2) — global Moran's I and Getis-Ord Gi* hotspots (rebuilt Oct 2026).

Rebuilt from docs/reports/Hotspot_TechnicalReport.md because the original build script was
not preserved. Method:
  * balanced 261-block panel (data/BlockPanel_Balanced_261.csv), 12 count dates
  * outcome = individuals + 1.75 * tents_structures + v * vehicles,
    v = 1.66 before the MAY2018 regime (count dates before 2018-05-01), 2.03 after
  * queen contiguity on data/Downtown_BlockGrid.geojson, row-standardized
  * global Moran's I per date (9,999 permutations)
  * Gi* (star=True) per date, 9,999 conditional permutations, seed 12345
  * hotspot_99: z >= 2.576 and p_sim < 0.01; hotspot_95: z >= 1.96 and p_sim < 0.05;
    coldspot_99 / coldspot_95 symmetric; otherwise not_significant
  * persistence = number of dates classified hotspot_95 or hotspot_99

Outputs:
  data/SpatialAutocorrelation_Results.csv   (Task 5.1 deliverable)
  data/Hotspot_Classifications.geojson      (Task 5.2 deliverable; one feature per block-date)
  data/Hotspot_Persistence_Ranking_rebuilt.csv  (validation against the Drive original)

Usage: python scripts/hotspot_analysis.py [--permutations 9999]
"""
import argparse
import json

import geopandas as gpd
import numpy as np
import pandas as pd
from esda.getisord import G_Local
from esda.moran import Moran
from libpysal.weights import Queen

SEED = 12345
TENT = 1.75


def load(panel_path="data/BlockPanel_Balanced_261.csv", grid_path="data/Downtown_BlockGrid.geojson"):
    panel = pd.read_csv(panel_path, parse_dates=["count_date"])
    v = np.where(panel["count_date"] < pd.Timestamp("2018-05-01"), 1.66, 2.03)
    panel["adjusted_count"] = (panel["individuals"] + TENT * panel["tents_structures"].fillna(0)
                               + v * panel["vehicles"])
    grid = gpd.read_file(grid_path)
    grid = grid[grid.block_id.isin(panel.block_id.unique())].sort_values("block_id").reset_index(drop=True)
    return panel, grid


def classify(z, p):
    if z >= 2.576 and p < 0.01:
        return "hotspot_99"
    if z >= 1.96 and p < 0.05:
        return "hotspot_95"
    if z <= -2.576 and p < 0.01:
        return "coldspot_99"
    if z <= -1.96 and p < 0.05:
        return "coldspot_95"
    return "not_significant"


def run(permutations=9999):
    panel, grid = load()
    w = Queen.from_dataframe(grid, ids=grid.block_id.tolist(), use_index=False)
    w.transform = "r"
    moran_rows, gi_rows = [], []
    for date, sub in panel.groupby("count_date"):
        y = sub.set_index("block_id").reindex(grid.block_id)["adjusted_count"].values.astype(float)
        mi = _moran(y, w, permutations)
        moran_rows.append({"count_date": date.date(), "n_blocks": len(y), "total_adjusted": round(y.sum(), 2),
                           "morans_I": mi.I, "expected_I": mi.EI, "z_norm": mi.z_norm, "p_norm": mi.p_norm,
                           "z_sim": mi.z_sim, "p_sim": mi.p_sim, "permutations": permutations,
                           "weights": "queen contiguity, row-standardized", "panel": "balanced 261"})
        g = G_Local(y, w, transform="R", star=True, permutations=permutations, seed=SEED)
        for bid, val, z, p in zip(grid.block_id, y, g.Zs, g.p_sim):
            gi_rows.append({"block_id": bid, "count_date": date.date(), "adjusted_count": val,
                            "gi_star_z": z, "p_sim": p, "classification": classify(z, p)})
    return grid, pd.DataFrame(moran_rows), pd.DataFrame(gi_rows)


def _moran(y, w, permutations):
    np.random.seed(SEED)
    return Moran(y, w, permutations=permutations)


def persistence(gi, grid):
    gi = gi.copy()
    gi["is_hot"] = gi.classification.str.startswith("hotspot")
    agg = gi.groupby("block_id").agg(hotspot_dates=("is_hot", "sum"), mean_gi_z=("gi_star_z", "mean"),
                                     mean_adjusted=("adjusted_count", "mean")).reset_index()
    agg = agg.merge(grid[["block_id", "neighborhood"]], on="block_id")
    agg = agg.sort_values(["hotspot_dates", "mean_gi_z", "mean_adjusted"], ascending=False).reset_index(drop=True)
    agg.insert(0, "persistence_rank", np.arange(1, len(agg) + 1))
    agg["hotspot_rate"] = (agg.hotspot_dates / gi.count_date.nunique()).round(2)
    return agg


def migration(gi, grid):
    """Adjusted-count-weighted centroid of hotspot block-dates, early vs recent period.
    Uses each block's representative point in UTM 11N (EPSG:32611), matching the original Task 5.4."""
    pts = grid.to_crs("EPSG:32611").set_index("block_id").geometry.representative_point()
    hot = gi[gi.classification.str.startswith("hotspot")].copy()
    hot["x"], hot["y"] = hot.block_id.map(pts.x), hot.block_id.map(pts.y)
    hot["count_date"] = pd.to_datetime(hot.count_date)
    out = {}
    for label, lo, hi in (("early_2018_2020", "2018-01-01", "2020-12-31"), ("recent_2022_2025", "2022-01-01", "2025-12-31")):
        h = hot[(hot.count_date >= lo) & (hot.count_date <= hi)]
        out[label] = (np.average(h.x, weights=h.adjusted_count), np.average(h.y, weights=h.adjusted_count))
    dx = out["recent_2022_2025"][0] - out["early_2018_2020"][0]
    dy = out["recent_2022_2025"][1] - out["early_2018_2020"][1]
    return out, float(np.hypot(dx, dy)), float((np.degrees(np.arctan2(dx, dy)) + 360) % 360)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--permutations", type=int, default=9999)
    a = ap.parse_args()
    grid, moran, gi = run(a.permutations)
    moran.to_csv("data/SpatialAutocorrelation_Results.csv", index=False)

    gi_geo = gi.merge(grid[["block_id", "neighborhood", "geometry"]], on="block_id")
    gi_geo = gpd.GeoDataFrame(gi_geo, geometry="geometry", crs=grid.crs)
    gi_geo["count_date"] = gi_geo.count_date.astype(str)
    gi_geo.to_file("data/Hotspot_Classifications.geojson", driver="GeoJSON")

    rank = persistence(gi, grid)
    rank.to_csv("data/Hotspot_Persistence_Ranking_rebuilt.csv", index=False)
    cents, dist, bearing = migration(gi, grid)

    print(moran[["count_date", "morans_I", "p_sim"]].round(4).to_string(index=False))
    print(f"Moran's I range {moran.morans_I.min():.3f}-{moran.morans_I.max():.3f}, max p_sim {moran.p_sim.max():.4f}")
    print(rank.head(10)[["persistence_rank", "block_id", "neighborhood", "hotspot_dates"]].to_string(index=False))
    print(f"Weighted hotspot centroid moved {dist:.0f} m, bearing {bearing:.1f} deg; centroids {json.dumps(cents)}")
    print(gi.classification.value_counts().to_string())


if __name__ == "__main__":
    main()
