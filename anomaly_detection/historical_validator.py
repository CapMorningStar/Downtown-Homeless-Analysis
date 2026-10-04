"""
Historical Ground-Truth Validation Harness (Task 10.4)
Benchmarks detection sensitivity against known historical policy events and shocks:
1. April 2020: COVID-19 onset & Convention Center "Operation Shelter to Home" demobilization
2. May–December 2022: Unprecedented surge to 1,800+ & Downtown Partnership block grid expansion
3. June–August 2023: Historical peak (2,100+) & City Unsafe Camping Ordinance passage
4. October 2023 – April 2024: O Street Safe Sleeping Site opening & street count contraction
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd


class HistoricalBenchmarkValidator:
    """
    Evaluates True Positive Rate, False Positive Rate, and classification alignment
    against verified historical ground-truth regimes.
    """

    BENCHMARK_EVENTS = [
        {
            "name": "COVID-19 Shelter Demobilization",
            "start": "2020-04-01",
            "end": "2020-09-01",
            "expected_typology": "Count Drop",
            "description": "Convention Center emergency shelter opened; street counts plummeted to ~323.",
        },
        {
            "name": "2022 Surge & Footprint Expansion",
            "start": "2022-05-01",
            "end": "2022-12-01",
            "expected_typology": ["Count Spike", "Spatial Shift"],
            "description": "Rapid escalation across East Village; counts surged from 1,000 to 1,800+.",
        },
        {
            "name": "Historical Peak & Camping Ban",
            "start": "2023-06-01",
            "end": "2023-08-01",
            "expected_typology": ["Count Spike", "Count Drop"],
            "description": "All-time peak of 2,100+ followed by Unsafe Camping Ordinance enforcement.",
        },
        {
            "name": "Safe Sleeping Site Contraction",
            "start": "2023-10-01",
            "end": "2024-04-01",
            "expected_typology": "Count Drop",
            "description": "Safe sleeping sites opened at 29th & Commercial and O Street, absorbing hundreds.",
        },
    ]

    def validate(self, classified_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, float]]:
        """
        Computes detection alignment per benchmark event and calculates global TPR, FPR, and Precision.
        """
        df = classified_df.copy()
        df["date"] = pd.to_datetime(df["date"])

        event_summaries = []
        is_known_event_month = np.zeros(len(df), dtype=bool)

        for event in self.BENCHMARK_EVENTS:
            start_dt = pd.to_datetime(event["start"])
            end_dt = pd.to_datetime(event["end"])

            mask = (df["date"] >= start_dt) & (df["date"] <= end_dt)
            is_known_event_month |= mask

            event_rows = df[mask]
            detected_anoms = event_rows[event_rows["is_classified_anomaly"]]
            num_detected = len(detected_anoms)
            num_total = len(event_rows)

            expected_types = (
                event["expected_typology"]
                if isinstance(event["expected_typology"], list)
                else [event["expected_typology"]]
            )
            type_matches = detected_anoms["anomaly_typology"].isin(expected_types).sum()

            event_summaries.append({
                "event_name": event["name"],
                "period": f"{start_dt.strftime('%b %Y')} – {end_dt.strftime('%b %Y')}",
                "event_months": num_total,
                "detected_months": num_detected,
                "detection_rate_pct": round((num_detected / max(1, num_total)) * 100.0, 1),
                "expected_typology": ", ".join(expected_types),
                "type_match_count": int(type_matches),
                "status": "VERIFIED DETECTED" if num_detected > 0 else "MISSED",
            })

        event_df = pd.DataFrame(event_summaries)

        # Global Confusion Matrix
        y_true_event = is_known_event_month
        y_pred_anom = df["is_classified_anomaly"].values

        tp = int(np.sum(y_true_event & y_pred_anom))
        fp = int(np.sum((~y_true_event) & y_pred_anom))
        fn = int(np.sum(y_true_event & (~y_pred_anom)))
        tn = int(np.sum((~y_true_event) & (~y_pred_anom)))

        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        f1 = (2 * precision * tpr) / (precision + tpr) if (precision + tpr) > 0 else 0.0

        global_metrics = {
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "true_negatives": tn,
            "tpr_sensitivity_pct": round(tpr * 100.0, 1),
            "fpr_false_alarm_pct": round(fpr * 100.0, 1),
            "precision_pct": round(precision * 100.0, 1),
            "f1_score": round(f1, 4),
        }

        return event_df, global_metrics
