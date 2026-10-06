"""Task 4.3 — structural break analysis (rebuilt Oct 2026 from StructuralBreak_Analysis.md).

Chow test as a dummy-variable regression on each analysis series:
    y = b0 + b1*tau + b2*D + b3*D*(tau - tau_break) + e
joint F-test of b2 = b3 = 0; b2 = level shift at the break, b3 = slope change.
April 2017 has only 3 pre-break months, so it uses the reduced level-shift model
(y = b0 + b1*tau + b2*D) and is exploratory only. Benjamini-Hochberg FDR p-values are
computed across the eight eligible series within each event/target; HAC(12) p-values are
added for May 2018 and COVID. May 2018 (and April) are re-run on raw_count as a
multiplier sensitivity. A full-series OLS-residual CUSUM (ddof=2) runs once per series.
Outside Perimeter starts Jan 2021, so it is excluded from all Chow tests.

Usage: python scripts/structural_breaks.py [--source ...] [--out data/StructuralBreaks.csv]
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import breaks_cusumolsresid
from statsmodels.stats.multitest import multipletests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ts_series import build_series  # noqa: E402

ALPHA = 0.05
EVENTS = {"Apr 2017 method": "2017-04-01", "May 2018 method": "2018-05-01", "COVID-19 onset": "2020-03-01"}


def classify(joint_p, level_p, trend_p):
    if joint_p >= ALPHA:
        return "Not significant"
    lv, tr = level_p < ALPHA, (trend_p is not None and trend_p < ALPHA)
    if lv and tr:
        return "Level shift and trend change"
    if lv:
        return "Level shift only"
    if tr:
        return "Trend change only"
    return "Significant (joint), neither term individually significant"


def chow(series, break_date, reduced=False, hac=False):
    y = series.values.astype(float)
    tau = np.arange(len(y), dtype=float)
    d = (series.index >= pd.Timestamp(break_date)).astype(float)
    kb = int(np.argmax(d))
    cols = [tau, d] if reduced else [tau, d, d * (tau - kb)]
    X = sm.add_constant(np.column_stack(cols))
    fit = sm.OLS(y, X).fit()
    hypothesis = "x2 = 0" if reduced else "x2 = 0, x3 = 0"
    ft = fit.f_test(hypothesis)
    out = {
        "n_pre": kb, "n_post": len(y) - kb,
        "F": float(np.squeeze(ft.fvalue)), "p": float(ft.pvalue),
        "level_shift": fit.params[2], "level_p": fit.pvalues[2],
        "trend_shift": None if reduced else fit.params[3],
        "trend_p": None if reduced else fit.pvalues[3],
    }
    if hac:
        h = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 12})
        out["hac_p"] = float(h.f_test(hypothesis).pvalue)
        out["hac_level_p"] = h.pvalues[2]
        out["hac_trend_p"] = None if reduced else h.pvalues[3]
    return out


def run(source):
    rows = []
    for target in ("total_count", "raw_count"):
        series_map = build_series(source, value=target)
        eligible = {k: v for k, v in series_map.items() if k != "Outside Perimeter"}
        for event, date in EVENTS.items():
            if target == "raw_count" and event == "COVID-19 onset":
                continue
            variants = [("reduced_level_model", True)]
            if event != "Apr 2017 method":
                variants = [("full_chow", False)]
            elif target == "total_count":
                variants.append(("full_chow_unreliable", False))
            for model, reduced in variants:
                block = []
                for name, s in eligible.items():
                    r = chow(s, date, reduced=reduced, hac=(event != "Apr 2017 method"))
                    r.update({"test": "chow", "target": target, "event": event, "break_date": date,
                              "model": model, "series": name})
                    r["classification"] = classify(r["p"], r["level_p"], r["trend_p"])
                    block.append(r)
                fdr = multipletests([b["p"] for b in block], method="fdr_bh")[1]
                for b, q in zip(block, fdr):
                    b["p_fdr"] = q
                rows.extend(block)
    fdr_rows = []
    for name, s in build_series(source).items():
        tau = np.arange(len(s), dtype=float)
        resid = sm.OLS(s.values, sm.add_constant(tau)).fit().resid
        stat, p, _ = breaks_cusumolsresid(resid, ddof=2)
        fdr_rows.append({"test": "cusum_olsresid", "target": "total_count", "series": name,
                         "F": stat, "p": p, "classification": "Significant" if p < ALPHA else "Not significant"})
    qs = multipletests([r["p"] for r in fdr_rows], method="fdr_bh")[1]
    for r, q in zip(fdr_rows, qs):
        r["p_fdr"] = q
    cols = ["test", "target", "event", "break_date", "model", "series", "n_pre", "n_post", "F", "p", "p_fdr",
            "level_shift", "level_p", "trend_shift", "trend_p", "hac_p", "hac_level_p", "hac_trend_p", "classification"]
    df = pd.DataFrame(rows + fdr_rows).reindex(columns=cols)
    df = df.rename(columns={"F": "statistic"})
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="data/MasterCounts_Adjusted_v2.csv")
    ap.add_argument("--out", default="data/StructuralBreaks.csv")
    a = ap.parse_args()
    df = run(a.source)
    df.to_csv(a.out, index=False)
    print(f"{len(df)} rows -> {a.out}")


if __name__ == "__main__":
    main()
