"""Task 4.2 — seasonal indices with significance tests (rebuilt Oct 2026).

For each of the 9 analysis series: detrend with the same robust STL fit as Task 4.1
(detrended = observed - trend), take each calendar month's mean detrended value as its
seasonal index, give a t-distribution 95% CI, a one-sample t-test against 0 with
Cohen's d, and test overall seasonality with Kruskal-Wallis (primary) and one-way ANOVA.

Usage: python scripts/seasonal_indices.py [--source data/MasterCounts_Adjusted_v2.csv] [--out data/SeasonalIndices.csv]
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.seasonal import STL

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ts_series import build_series, SEASONAL_PERIOD  # noqa: E402

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
ALPHA = 0.05


def seasonal_table(series_map):
    rows = []
    for name, s in series_map.items():
        trend = STL(s, period=SEASONAL_PERIOD, robust=True).fit().trend
        detr = s - trend
        groups = [detr[detr.index.month == m].values for m in range(1, 13)]
        kw_h, kw_p = stats.kruskal(*groups)
        an_f, an_p = stats.f_oneway(*groups)
        for m, g in enumerate(groups, start=1):
            n = len(g)
            mean = g.mean()
            sd = g.std(ddof=1)
            se = sd / np.sqrt(n)
            tcrit = stats.t.ppf(1 - ALPHA / 2, n - 1)
            t_stat, p = stats.ttest_1samp(g, 0.0)
            sig = p < ALPHA
            rows.append({
                "series": name, "month": m, "month_name": MONTHS[m - 1], "n_years": n,
                "seasonal_index": mean, "ci_lower": mean - tcrit * se, "ci_upper": mean + tcrit * se,
                "t_stat": t_stat, "p_value": p, "effect_size_d": mean / sd if sd > 0 else np.nan,
                "significant_month": bool(sig),
                "direction": ("higher" if mean > 0 else "lower") if sig else "not significant",
                "kw_H": kw_h, "kw_p": kw_p, "anova_F": an_f, "anova_p": an_p,
                "seasonality_significant_overall": bool(kw_p < ALPHA),
            })
    return pd.DataFrame(rows).sort_values(["series", "month"]).reset_index(drop=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="data/MasterCounts_Adjusted_v2.csv")
    ap.add_argument("--out", default="data/SeasonalIndices.csv")
    a = ap.parse_args()
    table = seasonal_table(build_series(a.source))
    table.to_csv(a.out, index=False)
    overall = table.drop_duplicates("series")[["series", "kw_H", "kw_p", "anova_p", "seasonality_significant_overall"]]
    print(overall.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
