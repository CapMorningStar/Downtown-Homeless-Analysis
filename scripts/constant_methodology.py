"""Task 6.2 — constant-methodology (hybrid) time series (rebuilt Oct 2026 from TimeSeries_ConstantMethodology.md).

Rescales every neighborhood monthly total onto the POST2020 multiplier baseline
(individual 1.00, tent 1.75, vehicle 2.03):
  identity                 MAY2018 / POST2020 rows: factor 1.0
  exact                    APR2017 rows with component data (Jan-Apr 2018): row's own composition
  proxied_APR2017_pre2018  Apr-Dec 2017: per-neighborhood Jan-Apr 2018 pooled composition vs APR2017 multipliers
  proxied_PRE2017          Jan-Mar 2017: same proxy composition vs PRE2017 multipliers (2.00 / 2.00)
Aggregates are sums of their constituents' already-adjusted counts.

Also writes data/AdjustmentFactors_RatioComparison.csv (observed vs theoretical ratios at both breaks).

Usage: python scripts/constant_methodology.py [--source ...] [--out data/TimeSeries_ConstantMethodology.csv]
"""
import argparse

import numpy as np
import pandas as pd

MULT = {
    "PRE2017": (1.00, 2.00, 2.00),
    "APR2017": (1.00, 1.75, 1.66),
    "MAY2018": (1.00, 1.75, 2.03),
    "POST2020": (1.00, 1.75, 2.03),
}
BASE = "POST2020"
SIX = ["East Village", "City Center", "Columbia", "Marina", "Cortez", "Gaslamp"]
ALL = SIX + ["Outside Perimeter"]
OVERALL, CORE = "Overall - reported footprint", "Overall - fixed core six"


def composite(comp, regime):
    i, t, v = comp
    mi, mt, mv = MULT[regime]
    return i * mi + t * mt + v * mv


def load(source):
    df = pd.read_csv(source, parse_dates=["date"])
    df = df[(df.area_type == "neighborhood") & df.area.isin(ALL)]
    tot = df[df.component == "total"].set_index(["area", "date"])
    comps = df[df.component.isin(["individual", "tent", "vehicle"])].pivot_table(
        index=["area", "date"], columns="component", values="raw_count", aggfunc="first")
    return tot, comps


def proxy_composition(comps, area, start, end):
    """Mean of the monthly individual/tent/vehicle shares over the window (as in Task 6.1)."""
    w = comps.loc[area]
    w = w[(w.index >= start) & (w.index <= end)][["individual", "tent", "vehicle"]]
    shares = w.div(w.sum(axis=1), axis=0).mean()
    return (shares["individual"], shares["tent"], shares["vehicle"])


def build(source):
    tot, comps = load(source)
    rows = []
    for area in ALL:
        proxy = proxy_composition(comps, area, "2018-01-01", "2018-04-01") if area in SIX else None
        for date, r in tot.loc[area].sort_index().iterrows():
            method = r["method"]
            if method in ("MAY2018", "POST2020"):
                factor, basis, src = 1.0, "identity", "none"
            elif method == "APR2017" and (area, date) in comps.index and date >= pd.Timestamp("2018-01-01"):
                c = tuple(comps.loc[(area, date), ["individual", "tent", "vehicle"]])
                factor, basis, src = composite(c, BASE) / composite(c, method), "exact", "row components"
            else:
                factor = composite(proxy, BASE) / composite(proxy, method)
                basis = "proxied_PRE2017" if method == "PRE2017" else "proxied_APR2017_pre2018"
                src = "Jan-Apr 2018 pooled composition"
            rows.append({"date": date, "series": area, "method": method, "raw_count": r["raw_count"],
                         "total_count": r["total_count"], "adjustment_factor": factor,
                         "constant_methodology_count": r["total_count"] * factor if pd.notna(r["total_count"]) else np.nan,
                         "factor_basis": basis, "composition_source": src, "baseline_regime": BASE})
    out = pd.DataFrame(rows)
    for name, members in ((CORE, SIX), (OVERALL, ALL)):
        sub = out[out.series.isin(members)]
        g = sub.groupby("date")
        need = len(members) if name == CORE else 1
        agg = pd.DataFrame({
            "raw_count": g.raw_count.sum(min_count=need),
            "total_count": g.total_count.sum(min_count=need),
            "constant_methodology_count": g.constant_methodology_count.sum(min_count=need),
            "method": g.method.first(),
            "factor_basis": g.factor_basis.agg(lambda s: "+".join(sorted(set(s)))),
        }).reset_index()
        agg["series"] = name
        agg["adjustment_factor"] = agg.constant_methodology_count / agg.total_count
        agg["composition_source"] = "sum of adjusted constituents"
        agg["baseline_regime"] = BASE
        out = pd.concat([out, agg], ignore_index=True)
    cols = ["date", "series", "method", "raw_count", "total_count", "adjustment_factor",
            "constant_methodology_count", "factor_basis", "composition_source", "baseline_regime"]
    return out[cols].sort_values(["series", "date"]).reset_index(drop=True), tot, comps


def ratio_table(tot, comps):
    rows = []
    for event, pre, post, old, new, comp_window in (
        ("Apr 2017", "2017-03-01", "2017-04-01", "PRE2017", "APR2017", ("2018-01-01", "2018-04-01")),
        ("May 2018", "2018-04-01", "2018-05-01", "APR2017", "MAY2018", ("2018-04-01", "2018-04-01")),
    ):
        pooled = np.zeros(3)
        obs_pre = obs_post = 0.0
        for area in SIX:
            comp = proxy_composition(comps, area, *comp_window)
            w = comps.loc[area]
            w = w[(w.index >= comp_window[0]) & (w.index <= comp_window[1])]
            pooled += w[["individual", "tent", "vehicle"]].sum().values  # count-pooled across the six
            a = tot.loc[(area, pd.Timestamp(pre)), "total_count"]
            b = tot.loc[(area, pd.Timestamp(post)), "total_count"]
            obs_pre += a
            obs_post += b
            theo = composite(comp, new) / composite(comp, old)
            rows.append({"event": event, "series": area, "observed_ratio": b / a, "theoretical_ratio": theo,
                         "gap_pct": (b / a / theo - 1) * 100})
        theo = composite(tuple(pooled), new) / composite(tuple(pooled), old)
        rows.append({"event": event, "series": "All six (pooled)", "observed_ratio": obs_post / obs_pre,
                     "theoretical_ratio": theo, "gap_pct": (obs_post / obs_pre / theo - 1) * 100})
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="data/MasterCounts_Adjusted_v2.csv")
    ap.add_argument("--out", default="data/TimeSeries_ConstantMethodology.csv")
    ap.add_argument("--ratios", default="data/AdjustmentFactors_RatioComparison.csv")
    a = ap.parse_args()
    series, tot, comps = build(a.source)
    series.to_csv(a.out, index=False)
    ratios = ratio_table(tot, comps)
    ratios.to_csv(a.ratios, index=False)
    print(series.factor_basis.value_counts().to_string())
    print(ratios.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
