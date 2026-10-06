"""Regression tests for the Oct 2026 source corrections (scripts/apply_source_corrections.py)."""
import csv
import os
from collections import Counter

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SUB_AREAS = ("North East EV", "North West EV", "South East EV", "South West EV")
MULTIPLIERS = {
    "APR2017": {"tent": 1.75, "vehicle": 1.66},
    "MAY2018": {"tent": 1.75, "vehicle": 2.03},
    "POST2020": {"tent": 1.75, "vehicle": 2.03},
}


def _read(name):
    with open(os.path.join(DATA, name), newline="") as f:
        return list(csv.DictReader(f))


def _num(x):
    return None if x in ("", "nan", "NaN") else float(x)


RAW = _read("RawCounts_AllYears_clean.csv")
MASTER = _read("MasterCounts_Adjusted_v2.csv")
CORRECTIONS = _read("source_corrections.csv")


def test_row_counts_unchanged():
    assert len(RAW) == 2814
    assert len(MASTER) == 2814
    by_year = Counter(r["year"] for r in RAW)
    assert by_year == {"2017": 72, "2018": 336, "2019": 336, "2020": 336, "2021": 342,
                       "2022": 348, "2023": 348, "2024": 348, "2025": 348}


def test_2019_sub_areas_no_longer_copy_2020():
    def cells(year):
        return {(r["month"], r["area"]): r["count"] for r in RAW
                if r["year"] == year and r["area"] in SUB_AREAS}
    y2019, y2020 = cells("2019"), cells("2020")
    identical = sum(1 for k, v in y2019.items() if y2020.get(k) == v)
    assert identical < 5, f"{identical} of 48 sub-area cells still equal 2020"


def test_sub_areas_sum_to_east_village_total():
    totals = {(r["date"]): _num(r["count"]) for r in RAW
              if r["area"] == "East Village" and r["component"] == "total"}
    sums = Counter()
    for r in RAW:
        if r["area"] in SUB_AREAS and _num(r["count"]) is not None:
            sums[r["date"]] += _num(r["count"])
    # Documented source-side gaps (DataValidation_SourceCheck, Section 3):
    # Feb 2018 DSDP table adds to 504 vs 474; Mar 2023 -8; Sep 2025 -38.
    known = {"2018-02-01", "2023-03-01", "2025-09-01"}
    bad = [(d, s, totals.get(d)) for d, s in sums.items()
           if d not in known and totals.get(d) is not None and abs(s - totals[d]) > 2]
    assert not bad, bad


def test_component_multipliers():
    for r in MASTER:
        mult = MULTIPLIERS.get(r["method"], {}).get(r["component"])
        raw, adj = _num(r["raw_count"]), _num(r["total_count"])
        if mult is None or raw is None or adj is None:
            continue
        assert abs(adj - round(raw * mult, 2)) < 0.011, (r["date"], r["area"], r["component"])


def test_totals_equal_component_sums_unless_overridden():
    overrides = {(c["date"], c["area"]) for c in CORRECTIONS if c["action"] == "use_published_total"}
    idx = {(r["date"], r["area"], r["component"]): r for r in MASTER}
    checked = 0
    for r in MASTER:
        if r["component"] != "total" or (r["date"], r["area"]) in overrides:
            continue
        comps = [idx.get((r["date"], r["area"], c)) for c in ("individual", "tent", "vehicle")]
        if not all(comps) or any(_num(c["total_count"]) is None for c in comps):
            continue
        checked += 1
        assert abs(_num(r["total_count"]) - sum(_num(c["total_count"]) for c in comps)) < 0.011
    assert checked >= 535


def test_verified_corrections_present():
    idx = {(r["date"], r["area"], r["component"]): _num(r["count"]) for r in RAW}
    assert idx[("2018-02-01", "City Center", "tent")] == 10
    assert idx[("2018-02-01", "City Center", "vehicle")] == 1
    assert idx[("2018-07-01", "East Village", "vehicle")] == 26
    assert idx[("2024-03-01", "City Center", "tent")] == 18
    feb18 = {(r["date"], r["area"], r["component"]): r for r in MASTER}[("2018-02-01", "City Center", "total")]
    assert abs(_num(feb18["total_count"]) - 156.16) < 0.011


if __name__ == "__main__":
    import sys
    failed = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("PASS", name)
            except AssertionError as e:
                failed += 1
                print("FAIL", name, e)
    sys.exit(1 if failed else 0)
