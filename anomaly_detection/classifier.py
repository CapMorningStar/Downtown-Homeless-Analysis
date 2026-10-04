"""
4-Quadrant Anomaly Taxonomy Classifier (Task 10.4)
Categorizes every detected signal into:
1. Count Spike: Unexpected upward surges beyond control or prediction limits
2. Count Drop: Sudden downward contractions (shelter absorption or displacement)
3. Spatial Shift: Significant spatial concentration changes (HHI, neighborhood redistributions)
4. Potential Data Quality Issue: Physically implausible jumps, zero values, or reporting artifacts
"""

from enum import Enum
from typing import Dict, List, Optional
import numpy as np
import pandas as pd


class AnomalyTypology(str, Enum):
    COUNT_SPIKE = "Count Spike"
    COUNT_DROP = "Count Drop"
    SPATIAL_SHIFT = "Spatial Shift"
    DATA_QUALITY = "Potential Data Quality Issue"
    NORMAL = "Normal"


class AnomalyClassifier:
    """
    Synthesizes signals from Shewhart, CUSUM, Isolation Forest, and Conformal residuals
    into the 4-quadrant taxonomy.
    """

    def __init__(self, hhi_delta_sigma: float = 2.5, ev_share_delta_thresh: float = 12.0):
        self.hhi_delta_sigma = hhi_delta_sigma
        self.ev_share_delta_thresh = ev_share_delta_thresh

    def classify(
        self,
        merged_signals_df: pd.DataFrame,
        feature_df: Optional[pd.DataFrame] = None,
    ) -> pd.DataFrame:
        """
        Classifies each row into an AnomalyTypology and assigns severity.
        """
        df = merged_signals_df.copy()
        n = len(df)

        typologies: List[str] = []
        severities: List[str] = []
        descriptions: List[str] = []
        is_anomaly_list: List[bool] = []

        # Calculate spatial metrics if present in feature_df or df
        hhi_diff = None
        ev_diff = None
        if feature_df is not None:
            if "spatial_hhi_concentration_index_lag1" in feature_df.columns:
                hhi = feature_df["spatial_hhi_concentration_index_lag1"].values
                hhi_diff = np.abs(np.diff(hhi, prepend=hhi[0]))
                hhi_std = np.nanstd(hhi_diff)
                if hhi_std < 1e-4:
                    hhi_std = 1.0
                hhi_z = hhi_diff / hhi_std
            else:
                hhi_z = np.zeros(n)

            if "spatial_east_village_share_pct_lag1" in feature_df.columns:
                ev = feature_df["spatial_east_village_share_pct_lag1"].values
                ev_diff = np.abs(np.diff(ev, prepend=ev[0]))
            else:
                ev_diff = np.zeros(n)
        else:
            hhi_z = np.zeros(n)
            ev_diff = np.zeros(n)

        for i in range(n):
            row = df.iloc[i]
            val = float(row.get("value", row.get("actual_count", 0.0)))
            shew_anom = bool(row.get("shewhart_is_anomaly", False))
            shew_stat = str(row.get("shewhart_status", "NORMAL"))
            cusum_anom = bool(row.get("cusum_is_anomaly", False))
            cusum_stat = str(row.get("cusum_status", "NORMAL"))
            iso_anom = bool(row.get("iso_is_anomaly", False))
            conf_anom = bool(row.get("conformal_is_anomaly", False))
            conf_stat = str(row.get("conformal_status", "NORMAL"))

            has_any_signal = shew_anom or cusum_anom or iso_anom or conf_anom

            if not has_any_signal:
                typologies.append(AnomalyTypology.NORMAL.value)
                severities.append("NONE")
                descriptions.append("Count and features within normal statistical variance.")
                is_anomaly_list.append(False)
                continue

            is_anomaly_list.append(True)

            # Rule 1: Potential Data Quality Issue
            if val <= 0.0 or np.isnan(val):
                typologies.append(AnomalyTypology.DATA_QUALITY.value)
                severities.append("WARNING")
                descriptions.append("Zero count or missing observation recorded (potential reporting hiatus).")
                continue

            # Check single-month jump without precedent (step-jump > 750)
            if i > 0:
                prev_val = float(df.iloc[i - 1].get("value", df.iloc[i - 1].get("actual_count", val)))
                if abs(val - prev_val) > 850:
                    typologies.append(AnomalyTypology.DATA_QUALITY.value)
                    severities.append("CRITICAL")
                    descriptions.append(f"Unprecedented single-month shift (Δ={val - prev_val:+.0f}) indicating methodology boundary artifact.")
                    continue

            # Rule 2: Spatial Shift
            if hhi_z[i] > self.hhi_delta_sigma or ev_diff[i] > self.ev_share_delta_thresh:
                typologies.append(AnomalyTypology.SPATIAL_SHIFT.value)
                severities.append("WARNING" if shew_stat.startswith("CRITICAL") else "INFO")
                descriptions.append(f"Spatial redistribution detected: HHI concentration shift z={hhi_z[i]:.2f}, EV share delta={ev_diff[i]:.1%}.")
                continue

            # Rule 3: Directional Count Anomalies (Spike vs Drop)
            is_high = (
                "HIGH" in shew_stat
                or cusum_stat == "UPWARD_DRIFT"
                or conf_stat == "RESIDUAL_SURGE"
            )
            is_low = (
                "LOW" in shew_stat
                or cusum_stat == "DOWNWARD_DRIFT"
                or conf_stat == "RESIDUAL_PLUNGE"
            )

            # Determine severity
            is_critical = (
                "CRITICAL" in shew_stat
                or conf_anom
                or (shew_anom and cusum_anom)
            )
            sev = "CRITICAL" if is_critical else "WARNING"

            if is_high and not is_low:
                typologies.append(AnomalyTypology.COUNT_SPIKE.value)
                severities.append(sev)
                descriptions.append(f"Unscheduled upward count surge detected ({shew_stat}, CUSUM: {cusum_stat}).")
            elif is_low and not is_high:
                typologies.append(AnomalyTypology.COUNT_DROP.value)
                severities.append(sev)
                descriptions.append(f"Sharp downward count contraction detected ({shew_stat}, CUSUM: {cusum_stat}).")
            else:
                # Disambiguate using value relative to center line
                cl = float(row.get("center_line", val))
                if val >= cl:
                    typologies.append(AnomalyTypology.COUNT_SPIKE.value)
                    severities.append(sev)
                    descriptions.append(f"Count spike above rolling baseline ({val:.0f} vs CL {cl:.0f}).")
                else:
                    typologies.append(AnomalyTypology.COUNT_DROP.value)
                    severities.append(sev)
                    descriptions.append(f"Count drop below rolling baseline ({val:.0f} vs CL {cl:.0f}).")

        df["anomaly_typology"] = typologies
        df["anomaly_severity"] = severities
        df["anomaly_description"] = descriptions
        df["is_classified_anomaly"] = is_anomaly_list

        return df
