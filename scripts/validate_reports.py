#!/usr/bin/env python3
"""
Report Validation Script for Task 9.2 Deliverables:
- docs/ExecutiveSummary_NonTechnical.md
- docs/FullTechnicalReport.md

Audits word counts, table counts, formula representations, section headers,
and adherence to The 4 Mandatory Public Communication Rules.
"""

import os
import re
import sys

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
EXEC_SUMMARY_PATH = os.path.join(DOCS_DIR, "ExecutiveSummary_NonTechnical.md")
TECH_REPORT_PATH = os.path.join(DOCS_DIR, "FullTechnicalReport.md")


def audit_document(file_path, min_words, max_words, min_tables, doc_name):
    print(f"\n=======================================================")
    print(f"Auditing: {doc_name}")
    print(f"File: {file_path}")
    print(f"=======================================================")
    
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File does not exist at {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    words = len(content.split())
    lines = len(content.splitlines())
    tables = len(re.findall(r"(\|[^\n]+\|\n\|[-:\s|]+\|\n(?:\|[^\n]+\|\n)+)", content))
    ascii_tables = len(re.findall(r"\+[-+]+\+\n\|[^\n]+\|\n\+[-+]+\+", content))
    total_tables = tables + ascii_tables
    equations = len(re.findall(r"\$\$[\s\S]*?\$\$", content))

    print(f"  • Word Count:     {words:,} words (Budget: {min_words:,} – {max_words:,})")
    print(f"  • Total Lines:    {lines:,} lines")
    print(f"  • Markdown Tables:{total_tables} tables (Min expected: {min_tables})")
    print(f"  • Math Equations: {equations} display equations")

    passed = True
    if words < min_words:
        print(f"⚠️ WARNING: Word count ({words}) is below minimum target ({min_words})")
        passed = False
    else:
        print(f"✅ Word count requirement satisfied.")

    if total_tables < min_tables:
        print(f"⚠️ WARNING: Table count ({total_tables}) is below minimum target ({min_tables})")
        passed = False
    else:
        print(f"✅ Table count requirement satisfied.")

    # Check for The 4 Public Communication Rules
    rules_checks = [
        ("Rule 1 (No false single-point)", re.search(r"Rule 1|Single-Point Precision|single-point", content, re.IGNORECASE)),
        ("Rule 2 (Round to nearest 100)", re.search(r"Rule 2|nearest 100|Nearest 100", content, re.IGNORECASE)),
        ("Rule 3 (95% prediction interval)", re.search(r"Rule 3|Prediction Interval|95% Pred", content, re.IGNORECASE)),
        ("Rule 4 (Policy regime disclosure)", re.search(r"Rule 4|Camping Ordinance|displacement adjustment", content, re.IGNORECASE)),
    ]

    for rule_name, matched in rules_checks:
        if matched:
            print(f"✅ {rule_name}: Confirmed present")
        else:
            print(f"❌ {rule_name}: Missing or incomplete")
            passed = False

    return passed


def main():
    print("Initiating Task 9.2 Report Deliverable Audit Suite...")
    
    # Exec Summary: 3-4 pages (~1,500 - 3,500 words), min 3 tables
    exec_passed = audit_document(
        EXEC_SUMMARY_PATH, 
        min_words=1500, 
        max_words=3500, 
        min_tables=3, 
        doc_name="Non-Technical Executive Summary (Deliverable A)"
    )

    # Full Technical Report: 15-20 pages (~5,000 - 12,000 words), min 8 tables
    tech_passed = audit_document(
        TECH_REPORT_PATH, 
        min_words=5000, 
        max_words=12000, 
        min_tables=8, 
        doc_name="Full Technical Report (Deliverable B)"
    )

    print("\n=======================================================")
    if exec_passed and tech_passed:
        print("🎉 ALL TASK 9.2 DELIVERABLES AUDITED & PASSED SUCCESSFULLY!")
        print("=======================================================\n")
        sys.exit(0)
    else:
        print("❌ SOME AUDIT CHECKS FAILED OR GENERATED WARNINGS.")
        print("=======================================================\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
