"""
Anomaly Detection & Automated Alerting Package (Assignment 10, Task 10.4)
Downtown San Diego Homeless Population Analysis

Provides:
- Statistical Surveillance: Shewhart Control Charts (2σ/3σ) & Tabular CUSUM
- Model-Based Surveillance: Multivariate Isolation Forest & Conformal Residual Bounds
- 4-Quadrant Anomaly Taxonomy Classification (Count Spike, Count Drop, Spatial Shift, Data Quality)
- Historical Validation Benchmarking against COVID-19, 2022 Surge, and Camping Ban
- Automated Alerting Engine (Slack Block Kit, Email HTML, Persistent CSV Store)
"""

from .control_charts import ShewhartControlChart, TabularCUSUM
from .model_detectors import IsolationForestDetector, ConformalResidualDetector
from .classifier import AnomalyClassifier, AnomalyTypology
from .historical_validator import HistoricalBenchmarkValidator
from .alerting import AlertEngine, AlertSeverity, AlertStatus
from .pipeline import AnomalySurveillancePipeline

__all__ = [
    "ShewhartControlChart",
    "TabularCUSUM",
    "IsolationForestDetector",
    "ConformalResidualDetector",
    "AnomalyClassifier",
    "AnomalyTypology",
    "HistoricalBenchmarkValidator",
    "AlertEngine",
    "AlertSeverity",
    "AlertStatus",
    "AnomalySurveillancePipeline",
]
