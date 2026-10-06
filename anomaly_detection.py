#!/usr/bin/env python3
"""
Anomaly Detection & Automated Alerting System (Task 10.4)
Downtown San Diego Homeless Population Analysis

Implements:
1. Statistical Surveillance: Shewhart Control Charts (2σ/3σ) & Tabular CUSUM
2. Model-Based Surveillance: Multivariate Isolation Forest & Conformal Residual Bounds
3. 4-Quadrant Anomaly Taxonomy (Count Spike, Count Drop, Spatial Shift, Data Quality)
4. Historical Ground-Truth Validation (COVID-19 demobilization, 2022 surge, Camping Ban)
5. Automated Multi-Tier Alert Dispatch (Slack Block Kit, Email HTML, Persistent CSV Store)

Usage:
    python anomaly_detection.py --detect --alert --validate --plot
    python anomaly_detection.py --schedule
    python anomaly_detection.py
"""

import argparse
import json
import logging
from pathlib import Path
import sys
import pandas as pd

from anomaly_detection.pipeline import AnomalySurveillancePipeline
from anomaly_detection.alerting import AlertEngine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("anomaly_detection")


def print_banner(text: str):
    print("\n" + "=" * 75)
    print(text.center(75))
    print("=" * 75)


def main():
    parser = argparse.ArgumentParser(description="Task 10.4 Anomaly Detection & Automated Alerting System")
    parser.add_argument("--detect", action="store_true", help="Run dual detection engines and classify anomalies")
    parser.add_argument("--alert", action="store_true", help="Generate Slack Block Kit and Email alert payloads")
    parser.add_argument("--validate", action="store_true", help="Run benchmark validation against known historical shocks")
    parser.add_argument("--plot", action="store_true", help="Export publication charts to slide_assets/")
    parser.add_argument("--schedule", action="store_true", help="Headless scheduled execution mode (cron / Airflow)")
    parser.add_argument("--send", action="store_true",
                        help="Deliver new alerts to Slack/email (needs SLACK_WEBHOOK_URL and/or SMTP_* env vars); "
                             "without it, deliveries are only listed (dry run)")
    parser.add_argument("--min-severity", default="WARNING", choices=["INFO", "WARNING", "CRITICAL"],
                        help="Lowest severity to deliver (default WARNING)")
    parser.add_argument("--data", type=str, default="data/FeatureMatrix_Comprehensive_68.csv", help="Input feature matrix")
    parser.add_argument("--output-dir", type=str, default="data", help="Output directory for matrix and alert logs")

    args = parser.parse_args()

    # Default to running all if no flags given or --schedule given
    if not (args.detect or args.alert or args.validate or args.plot or args.schedule):
        args.detect = True
        args.alert = True
        args.validate = True
        args.plot = True

    if args.schedule:
        args.detect = True
        args.alert = True
        args.validate = True
        args.plot = True

    data_path = Path(args.data)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    pipeline = AnomalySurveillancePipeline(feature_data_path=data_path)

    print_banner("1. EXECUTING DUAL-ENGINE ANOMALY SURVEILLANCE")
    classified_df, event_df, summary = pipeline.run_surveillance()

    # Save full surveillance matrix
    matrix_path = out_dir / "Anomaly_Surveillance_Matrix.csv"
    classified_df.to_csv(matrix_path, index=False)
    logger.info(f"Saved full surveillance matrix to {matrix_path}")

    print("\n--- ANOMALY SURVEILLANCE SUMMARY ---")
    print(f"Total Monitored Months       : {summary['total_months']}")
    print(f"Total Anomalous Months Found : {summary['total_anomalies_detected']}")
    print(f"  • Count Spikes             : {summary['count_spikes']}")
    print(f"  • Count Drops              : {summary['count_drops']}")
    print(f"  • Spatial Shifts           : {summary['spatial_shifts']}")
    print(f"  • Potential Data Quality   : {summary['data_quality_issues']}")
    print(f"Active Alerts in Store       : {summary['total_active_alerts']}")

    if args.validate:
        print_banner("2. HISTORICAL BENCHMARK POLICY SHOCK VALIDATION")
        pd.set_option("display.max_columns", 10)
        pd.set_option("display.width", 120)
        print(event_df[["event_name", "period", "event_months", "detected_months", "detection_rate_pct", "status"]].to_string(index=False))

        print("\nGlobal Validation Performance:")
        v_met = summary["validation_metrics"]
        print(f"  • True Positive Rate (Sensitivity): {v_met['tpr_sensitivity_pct']}%")
        print(f"  • False Positive Rate (FPR)        : {v_met['fpr_false_alarm_pct']}%")
        print(f"  • Precision                        : {v_met['precision_pct']}%")
        print(f"  • F1-Score                         : {v_met['f1_score']}")

    if args.alert:
        print_banner("3. ALERT DISPATCH & NOTIFICATION PAYLOAD GENERATION")
        alert_engine = AlertEngine()
        alerts = alert_engine.load_alerts_store()

        critical_alerts = [a for a in alerts if a.get("severity") == "CRITICAL"]
        print(f"Total Stored Alerts: {len(alerts)} ({len(critical_alerts)} CRITICAL)")

        if critical_alerts:
            latest_crit = critical_alerts[-1]
            print(f"\n--- SAMPLE SLACK BLOCK KIT PAYLOAD ({latest_crit['alert_id']}) ---")
            slack_payload = alert_engine.build_slack_payload(latest_crit)
            print(json.dumps(slack_payload, indent=2)[:650] + "\n... [truncated for display]")

            print(f"\n--- SAMPLE EMAIL NOTIFICATION ({latest_crit['alert_id']}) ---")
            subj, html, plain = alert_engine.build_email_payload(latest_crit)
            print(f"Subject: {subj}")
            print(plain[:450] + "...")

        results = alert_engine.dispatch(min_severity=args.min_severity, dry_run=not args.send)
        mode = "SENT" if args.send else "DRY RUN (use --send to deliver)"
        print(f"\n--- DELIVERY: {mode} ---")
        for r in results:
            status = "sent" if r["sent"] else ("pending" if not r["error"] else r["error"])
            print(f"  {r['alert_id']}: channels={r['channels'] or 'none'} -> {status}")

    if args.plot:
        print_banner("4. HIGH-RESOLUTION PUBLICATION VISUALIZATIONS")
        plot1 = pipeline.plot_control_charts(classified_df, Path("slide_assets/task10_control_charts.png"))
        plot2 = pipeline.plot_anomaly_classification(classified_df, event_df, Path("slide_assets/task10_anomaly_classification.png"))
        print(f"✓ Control Charts exported to        : {plot1}")
        print(f"✓ Anomaly Classification exported to: {plot2}")

    print_banner("TASK 10.4 EXECUTION COMPLETE")


if __name__ == "__main__":
    main()
