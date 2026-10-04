#!/usr/bin/env python3
"""
CLI Runner for Multi-Source Data Ingestion Pipeline (Task 10.1)
Downtown San Diego Homeless Population Analysis

Usage:
    python scripts/run_ingestion_pipeline.py --all --validate
    python scripts/run_ingestion_pipeline.py --source weather
    python scripts/run_ingestion_pipeline.py --source 311
    python scripts/run_ingestion_pipeline.py --source events
    python scripts/run_ingestion_pipeline.py --source economic
    python scripts/run_ingestion_pipeline.py --source shelter
"""

import argparse
import json
import logging
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data_ingestion.aligner import MultiSourceAligner
from data_ingestion.validator import DataQualityValidator
from data_ingestion.sources.weather_noaa import WeatherIngestionPipeline
from data_ingestion.sources.major_events import MajorEventsIngestionPipeline
from data_ingestion.sources.economic_indicators import EconomicIngestionPipeline
from data_ingestion.sources.shelter_capacity import ShelterCapacityIngestionPipeline
from data_ingestion.sources.get_it_done_311 import GetItDone311IngestionPipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("run_ingestion_pipeline")


def main():
    parser = argparse.ArgumentParser(description="Multi-Source Data Ingestion Pipeline Runner (Task 10.1)")
    parser.add_argument("--all", action="store_true", help="Execute all pipelines, merge, and output master matrix")
    parser.add_argument(
        "--source",
        choices=["weather", "events", "economic", "shelter", "311"],
        help="Execute a specific source pipeline only",
    )
    parser.add_argument("--validate", action="store_true", help="Run automated data quality validation audit")
    parser.add_argument("--no-cache", action="store_true", help="Bypass local cache and force live network download")
    parser.add_argument("--output", type=str, default="data/MultiSource_Master_Monthly.csv", help="Output CSV path")

    args = parser.parse_args()
    use_cache = not args.no_cache

    if not args.all and not args.source and not args.validate:
        parser.print_help()
        sys.exit(0)

    if args.source:
        logger.info("Executing single pipeline for source: %s", args.source)
        if args.source == "weather":
            p = WeatherIngestionPipeline()
        elif args.source == "events":
            p = MajorEventsIngestionPipeline()
        elif args.source == "economic":
            p = EconomicIngestionPipeline()
        elif args.source == "shelter":
            p = ShelterCapacityIngestionPipeline()
        elif args.source == "311":
            p = GetItDone311IngestionPipeline()
        else:
            raise ValueError(f"Unknown source: {args.source}")

        df = p.run(use_cache=use_cache)
        print(f"\n--- {args.source.upper()} Pipeline Output Summary ---")
        print(f"Total Rows: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst 3 rows:")
        print(df.head(3))
        print("\nLast 3 rows:")
        print(df.tail(3))

    if args.all:
        logger.info("Executing full Multi-Source Alignment workflow...")
        aligner = MultiSourceAligner(output_path=Path(args.output))
        aligned_df = aligner.run_all(use_cache=use_cache)
        print("\n=======================================================")
        print("✓ MULTI-SOURCE MASTER MATRIX GENERATED SUCCESSFULLY")
        print("=======================================================")
        print(f"Destination: {args.output}")
        print(f"Total Observations: {len(aligned_df)} months (2017-01-01 to 2025-12-01)")
        print(f"Total Features: {len(aligned_df.columns)} columns")
        print(f"Columns List:\n{aligned_df.columns.tolist()}\n")

    if args.validate:
        logger.info("Running Data Quality & Schema Contract Validator...")
        validator = DataQualityValidator(data_path=Path(args.output))
        audit = validator.run_full_audit()
        print("\n=======================================================")
        print(f"DATA QUALITY AUDIT REPORT: {audit['status']}")
        print("=======================================================")
        print(f"Row Count: {audit['row_count']} (Expected: 108)")
        print(f"Date Span: {audit['date_range'][0]} to {audit['date_range'][1]}")
        print(f"Temporal Continuity: {'PASS' if audit['temporal_continuity_ok'] else 'FAIL'}")
        null_summary = 'PASS (0 nulls)' if audit['null_check_ok'] else f"FAIL ({audit['columns_with_nulls']})"
        bounds_summary = 'PASS' if audit['domain_bounds_ok'] else f"FAIL ({audit['domain_bound_violations']})"
        print(f"Null Checks: {null_summary}")
        print(f"Physical Domain Bounds: {bounds_summary}")
        if audit["status"] != "PASSED":
            sys.exit(1)


if __name__ == "__main__":
    main()
