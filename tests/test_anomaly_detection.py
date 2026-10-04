"""
Unit & Integration Tests for Task 10.4: Anomaly Detection & Automated Alerting
Downtown San Diego Homeless Population Analysis
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

from anomaly_detection.control_charts import ShewhartControlChart, TabularCUSUM
from anomaly_detection.model_detectors import IsolationForestDetector, ConformalResidualDetector
from anomaly_detection.classifier import AnomalyClassifier, AnomalyTypology
from anomaly_detection.historical_validator import HistoricalBenchmarkValidator
from anomaly_detection.alerting import AlertEngine, AlertSeverity, AlertStatus
from anomaly_detection.pipeline import AnomalySurveillancePipeline


def test_shewhart_control_limits_ordering():
    """Asserts LCL3 <= LCL2 < CL < UCL2 < UCL3."""
    chart = ShewhartControlChart(window=12, min_periods=6, warning_sigma=2.0, critical_sigma=3.0)
    data = pd.Series([800, 850, 900, 920, 880, 870, 950, 980, 1000, 1050, 1100, 1150] * 3)
    res = chart.fit_detect(data)

    assert len(res) == len(data)
    # Check bounds ordering
    assert (res["lcl_critical"] <= res["lcl_warning"]).all()
    assert (res["lcl_warning"] <= res["center_line"]).all()
    assert (res["center_line"] <= res["ucl_warning"]).all()
    assert (res["ucl_warning"] <= res["ucl_critical"]).all()
    assert (res["lcl_critical"] >= 0.0).all()


def test_cusum_accumulation_and_reset():
    """Verifies positive and negative CUSUM accumulation and reset on alarm."""
    cusum = TabularCUSUM(slack_k=0.5, threshold_h=4.0, window=12, reset_on_alarm=True)
    # Series with a massive positive surge in the middle
    data = pd.Series([1000] * 12 + [2500] * 6 + [1000] * 12)
    res = cusum.fit_detect(data)

    assert (res["cusum_s_pos"] >= 0.0).all()
    assert (res["cusum_s_neg"] >= 0.0).all()
    assert res["cusum_is_anomaly"].sum() > 0
    # Confirms reset occurred
    assert (res.loc[12:17, "cusum_s_pos"] <= 5.0).all()


def test_isolation_forest_detector():
    """Verifies IsolationForest produces valid anomaly scores and flags outliers."""
    detector = IsolationForestDetector(contamination=0.10, random_state=42)
    np.random.seed(42)
    normal_data = np.random.randn(90, 5)
    outliers = np.random.randn(10, 5) * 8.0
    X = pd.DataFrame(np.vstack([normal_data, outliers]), columns=[f"f_{i}" for i in range(5)])

    res = detector.fit_detect(X)
    assert len(res) == 100
    assert res["iso_is_anomaly"].sum() >= 5
    assert (res["iso_anomaly_score"] >= 0.0).all()
    assert (res["iso_anomaly_score"] <= 1.0).all()


def test_conformal_residual_detector():
    """Verifies residuals exceeding calibrated bound trigger anomalies."""
    detector = ConformalResidualDetector(conformal_margin=500.0)
    y_true = np.array([1000.0, 1100.0, 2200.0, 800.0])
    y_pred = np.array([1020.0, 1080.0, 1200.0, 850.0])  # index 2 has error = 1000 > 500

    res = detector.detect_residuals(y_true, y_pred)
    assert len(res) == 4
    assert res.loc[2, "conformal_is_anomaly"] == True
    assert res.loc[2, "conformal_status"] == "RESIDUAL_SURGE"
    assert res.loc[0, "conformal_is_anomaly"] == False


def test_anomaly_classification_taxonomy():
    """Verifies that signals correctly map to the 4 required typologies."""
    classifier = AnomalyClassifier(hhi_delta_sigma=2.0, ev_share_delta_thresh=10.0)

    # 1. Count Spike
    df_spike = pd.DataFrame({
        "value": [1800.0], "center_line": [1000.0],
        "shewhart_is_anomaly": [True], "shewhart_status": ["CRITICAL_HIGH"],
        "cusum_is_anomaly": [True], "cusum_status": ["UPWARD_DRIFT"],
        "iso_is_anomaly": [True], "conformal_is_anomaly": [True], "conformal_status": ["RESIDUAL_SURGE"],
    })
    c1 = classifier.classify(df_spike)
    assert c1.loc[0, "anomaly_typology"] == AnomalyTypology.COUNT_SPIKE.value

    # 2. Count Drop
    df_drop = pd.DataFrame({
        "value": [350.0], "center_line": [1000.0],
        "shewhart_is_anomaly": [True], "shewhart_status": ["CRITICAL_LOW"],
        "cusum_is_anomaly": [True], "cusum_status": ["DOWNWARD_DRIFT"],
        "iso_is_anomaly": [False], "conformal_is_anomaly": [False], "conformal_status": ["NORMAL"],
    })
    c2 = classifier.classify(df_drop)
    assert c2.loc[0, "anomaly_typology"] == AnomalyTypology.COUNT_DROP.value

    # 3. Data Quality (Zero count)
    df_zero = pd.DataFrame({
        "value": [0.0], "center_line": [800.0],
        "shewhart_is_anomaly": [True], "shewhart_status": ["CRITICAL_LOW"],
        "cusum_is_anomaly": [False], "cusum_status": ["NORMAL"],
        "iso_is_anomaly": [False], "conformal_is_anomaly": [False], "conformal_status": ["NORMAL"],
    })
    c3 = classifier.classify(df_zero)
    assert c3.loc[0, "anomaly_typology"] == AnomalyTypology.DATA_QUALITY.value


def test_historical_validator():
    """Verifies that benchmark events are evaluated with valid metrics."""
    validator = HistoricalBenchmarkValidator()
    dates = pd.date_range("2020-01-01", periods=60, freq="MS")
    mock_df = pd.DataFrame({
        "date": dates,
        "is_classified_anomaly": [False] * 60,
        "anomaly_typology": ["Normal"] * 60,
    })
    # Add true positives for COVID demobilization (Apr 2020)
    mock_df.loc[3:5, "is_classified_anomaly"] = True
    mock_df.loc[3:5, "anomaly_typology"] = "Count Drop"

    event_df, metrics = validator.validate(mock_df)
    assert len(event_df) == 4
    covid_row = event_df[event_df["event_name"].str.contains("COVID")]
    assert covid_row["detected_months"].values[0] == 3
    assert covid_row["status"].values[0] == "VERIFIED DETECTED"
    assert metrics["tpr_sensitivity_pct"] > 0


def test_alert_engine_lifecycle(tmp_path):
    """Verifies alert ingestion, Slack/Email payloads, and Mark as Reviewed action."""
    csv_file = tmp_path / "test_alerts.csv"
    json_file = tmp_path / "test_alerts.json"

    engine = AlertEngine(store_csv_path=csv_file, store_json_path=json_file)

    dates = pd.date_range("2023-01-01", periods=3, freq="MS")
    classified_df = pd.DataFrame({
        "date": dates,
        "value": [1000.0, 2150.0, 1100.0],
        "center_line": [980.0, 1000.0, 1020.0],
        "is_classified_anomaly": [False, True, False],
        "anomaly_typology": ["Normal", "Count Spike", "Normal"],
        "anomaly_severity": ["NONE", "CRITICAL", "NONE"],
        "shewhart_status": ["NORMAL", "CRITICAL_HIGH", "NORMAL"],
        "cusum_status": ["NORMAL", "UPWARD_DRIFT", "NORMAL"],
        "anomaly_description": ["Normal", "Major surge", "Normal"],
    })

    alerts = engine.ingest_anomalies(classified_df)
    assert len(alerts) == 1
    alert_id = alerts[0]["alert_id"]
    assert alert_id == "ALT-202302-CS"
    assert alerts[0]["status"] == AlertStatus.NEW.value

    # Verify Slack payload formatting
    slack = engine.build_slack_payload(alerts[0])
    assert "attachments" in slack
    assert slack["attachments"][0]["color"] == "#DC2626"

    # Verify Email payload formatting
    subj, html, plain = engine.build_email_payload(alerts[0])
    assert "CRITICAL" in subj
    assert "Count Spike" in plain
    assert "Emergency Shelter Activation" in html

    # Verify Mark as Reviewed
    success = engine.mark_as_reviewed(alert_id, reviewer="Kyaw Soe Lwin", notes="Confirmed surge in East Village.")
    assert success == True

    reloaded = engine.load_alerts_store()
    assert reloaded[0]["status"] == "REVIEWED"
    assert reloaded[0]["reviewer"] == "Kyaw Soe Lwin"
    assert "East Village" in reloaded[0]["reviewer_notes"]


def test_pipeline_end_to_end():
    """Runs end-to-end anomaly detection pipeline on actual project data."""
    matrix_path = Path("data/FeatureMatrix_Comprehensive_67.csv")
    if not matrix_path.exists():
        pytest.skip("Feature matrix missing.")

    pipeline = AnomalySurveillancePipeline()
    classified_df, event_df, summary = pipeline.run_surveillance()

    assert len(classified_df) == 96
    assert summary["total_anomalies_detected"] > 0
    assert summary["count_spikes"] > 0
    assert summary["count_drops"] > 0
    assert "validation_metrics" in summary
    assert summary["validation_metrics"]["tpr_sensitivity_pct"] > 0
