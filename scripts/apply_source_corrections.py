"""Apply source-verified corrections to the monthly count files.

Reads data/source_corrections.csv and updates, in place:
  - data/RawCounts_AllYears_clean.csv   (count column)
  - data/MasterCounts_Adjusted_v2.csv   (raw_count / total_count columns)

Then writes data/MasterCounts_QA_Flags.csv listing every area-month whose
adjusted total still differs from the DSDP published total by more than 2.

Actions in the corrections file:
  set_count            replace one cell (old_value -> new_value), then rebuild
                       that area-month's adjusted component and total rows
  use_published_total  set the adjusted total equal to the published total
                       (used where no source exists to verify the components)
  annotate             no data change; records why a flagged area-month was
                       left as-is (e.g. map verified but DSDP summary differs)

Safe to re-run: a row already at new_value is skipped; a row matching neither
old_value nor new_value stops the script.

Usage:  python scripts/apply_source_corrections.py
"""
import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
RAW = os.path.join(DATA, "RawCounts_AllYears_clean.csv")
MASTER = os.path.join(DATA, "MasterCounts_Adjusted_v2.csv")
CORR = os.path.join(DATA, "source_corrections.csv")
FLAGS = os.path.join(DATA, "MasterCounts_QA_Flags.csv")

# Documented multiplier schedule (Task 1.3 / MethodologyChangeLog)
MULTIPLIERS = {
    "APR2017": {"individual": 1.0, "tent": 1.75, "vehicle": 1.66},
    "MAY2018": {"individual": 1.0, "tent": 1.75, "vehicle": 2.03},
    "POST2020": {"individual": 1.0, "tent": 1.75, "vehicle": 2.03},
}
COMPONENTS = ("individual", "tent", "vehicle")
FLAG_THRESHOLD = 2.0


def num(x):
    return None if x in ("", "nan", "NaN", None) else float(x)


def fmt(x):
    return "" if x is None else repr(round(float(x), 2))


def read(path):
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def line_ending(path):
    """Keep each file's existing line ending so diffs show only real changes."""
    if not os.path.exists(path):
        return "\n"
    with open(path, "rb") as f:
        return "\r\n" if b"\r\n" in f.readline() else "\n"


def write(path, fields, rows):
    ending = line_ending(path)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator=ending)
        w.writeheader()
        w.writerows(rows)


def rebuild_area_month(master_idx, date, area):
    """Recompute adjusted component values and the adjusted total for one area-month."""
    comps = [master_idx.get((date, area, c)) for c in COMPONENTS]
    for row in comps:
        if row is None:
            continue
        mult = MULTIPLIERS.get(row["method"], {}).get(row["component"])
        raw = num(row["raw_count"])
        if mult is not None and raw is not None:
            row["total_count"] = fmt(raw * mult)
    total = master_idx.get((date, area, "total"))
    if total is None:
        return
    if all(c is not None and num(c["total_count"]) is not None for c in comps):
        total["total_count"] = fmt(sum(num(c["total_count"]) for c in comps))
    else:
        total["total_count"] = total["raw_count"]


def main():
    raw_fields, raw_rows = read(RAW)
    master_fields, master_rows = read(MASTER)
    _, corrections = read(CORR)

    raw_idx = {(r["date"], r["area"], r["component"]): r for r in raw_rows}
    master_idx = {(r["date"], r["area"], r["component"]): r for r in master_rows}

    applied = skipped = 0
    touched = set()
    published_override = []
    for c in corrections:
        key = (c["date"], c["area"], c["component"])
        if key not in raw_idx or key not in master_idx:
            sys.exit(f"Correction target not found: {key}")
        if c["action"] == "use_published_total":
            published_override.append((c["date"], c["area"], c["note"]))
            continue
        if c["action"] == "annotate":
            continue
        if c["action"] != "set_count":
            sys.exit(f"Unknown action {c['action']!r} for {key}")
        old, new = float(c["old_value"]), float(c["new_value"])
        current = num(raw_idx[key]["count"])
        if current == new:
            skipped += 1
        elif current == old:
            raw_idx[key]["count"] = repr(new)
            master_idx[key]["raw_count"] = repr(new)
            applied += 1
        else:
            sys.exit(f"{key}: file has {current}, expected old {old} or new {new}")
        touched.add((c["date"], c["area"]))

    for date, area in sorted(touched):
        rebuild_area_month(master_idx, date, area)

    notes = {}
    for date, area, note in published_override:
        row = master_idx[(date, area, "total")]
        row["total_count"] = row["raw_count"]
        notes[(date, area)] = ("published_total_used", note)

    by_corr = {(c["date"], c["area"]): c["note"] for c in corrections if c["action"] == "set_count"}
    for c in corrections:
        if c["action"] == "annotate":
            notes[(c["date"], c["area"])] = ("map_verified_source_conflict", c["note"])
    flags = []
    for r in master_rows:
        if r["component"] != "total":
            continue
        raw, adj = num(r["raw_count"]), num(r["total_count"])
        key = (r["date"], r["area"])
        if key in notes:
            status, note = notes[key]
        elif raw is not None and adj is not None and abs(adj - raw) > FLAG_THRESHOLD:
            status = "source_conflict_or_unverified"
            note = by_corr.get(key, "Adjusted total (from components) differs from DSDP published total; not verified against map")
        else:
            continue
        flags.append({
            "date": r["date"], "area": r["area"], "method": r["method"],
            "published_total": r["raw_count"], "adjusted_total": r["total_count"],
            "difference": fmt((adj or 0) - (raw or 0)) if raw is not None and adj is not None else "",
            "status": status, "note": note,
        })

    write(RAW, raw_fields, raw_rows)
    write(MASTER, master_fields, master_rows)
    write(FLAGS, ["date", "area", "method", "published_total", "adjusted_total",
                  "difference", "status", "note"], flags)
    print(f"applied {applied}, already applied {skipped}, area-months rebuilt {len(touched)}, "
          f"published-total overrides {len(published_override)}, QA flags {len(flags)}")


if __name__ == "__main__":
    main()
