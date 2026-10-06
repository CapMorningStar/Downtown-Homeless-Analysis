"""
Automated Alerting Engine & Persistent Alert Store (Task 10.4)
Generates:
1. Multi-tier severity notifications (CRITICAL, WARNING, INFO)
2. Slack Block Kit webhook payloads with actionable recommended responses
3. Email notification payloads (HTML & Plain Text)
4. Persistent Audit Store (CSV and JSON) tracking review lifecycle
5. Delivery (dispatch) to Slack and/or email, configured through environment variables:
     SLACK_WEBHOOK_URL                          Slack incoming-webhook URL
     SMTP_HOST, SMTP_PORT (default 587),        SMTP server (STARTTLS)
     SMTP_USER, SMTP_PASSWORD,                  credentials (optional for open relays)
     ALERT_EMAIL_FROM, ALERT_EMAIL_TO           sender and comma-separated recipients
   Nothing is sent unless dispatch(..., dry_run=False) is called (CLI: --send). Each alert is
   delivered at most once; the delivery time is stored in its `notified_at` field.
"""

from datetime import datetime
from enum import Enum
import json
import logging
import os
import smtplib
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd

logger = logging.getLogger(__name__)


class AlertSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    INFO = "INFO"


class AlertStatus(str, Enum):
    NEW = "NEW"
    REVIEWED = "REVIEWED"
    DISMISSED = "DISMISSED"


class AlertEngine:
    """
    Manages alerting dispatch formats, notification generation, and the persistent alert lifecycle store.
    """

    def __init__(
        self,
        store_csv_path: Optional[Path] = None,
        store_json_path: Optional[Path] = None,
    ):
        self.store_csv_path = store_csv_path or Path("data/Alerts_History.csv")
        self.store_json_path = store_json_path or Path("data/Alerts_History.json")
        self.store_csv_path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_actionable_recommendation(typology: str, severity: str) -> str:
        """Assigns municipal policy and operational playbook recommendations."""
        if typology == "Count Spike":
            if severity == "CRITICAL":
                return "Immediate Emergency Shelter Activation: Deploy rapid-response outreach teams to East Village and evaluate emergency overflow capacity."
            return "Enhanced Outreach Deployment: Schedule targeted neighborhood health teams to identify emerging encampment clusters."
        elif typology == "Count Drop":
            return "Shelter Intake & Displacement Verification: Verify whether drop reflects successful shelter placement or displacement to outlying city perimeters."
        elif typology == "Spatial Shift":
            return "Spatial Redistricting: Rebalance district sanitation schedules, portable restroom resources, and community police beat patrols."
        elif typology == "Potential Data Quality Issue":
            return "Data Quality Audit: Verify source collection logs, validate against raw field maps, and check for reporting boundary changes."
        return "Standard Operational Monitoring: Maintain normal monthly surveillance."

    def build_slack_payload(self, alert: Dict[str, Any]) -> Dict[str, Any]:
        """Constructs a production-grade Slack Block Kit payload."""
        sev = alert.get("severity", "WARNING")
        icon = "🚨" if sev == "CRITICAL" else ("⚠️" if sev == "WARNING" else "ℹ️")
        color = "#DC2626" if sev == "CRITICAL" else ("#F59E0B" if sev == "WARNING" else "#3B82F6")

        typology = alert.get("classification", "Count Spike")
        date_str = alert.get("month_date", "N/A")
        val = alert.get("metric_value", 0.0)
        cl = alert.get("baseline_center_line", 0.0)
        rec = alert.get("recommendation", self.get_actionable_recommendation(typology, sev))

        return {
            "attachments": [
                {
                    "color": color,
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": f"{icon} [{sev}] Homeless Surveillance Alert: {typology}",
                                "emoji": True,
                            },
                        },
                        {
                            "type": "section",
                            "fields": [
                                {"type": "mrkdwn", "text": f"*Observed Month:*\n{date_str}"},
                                {"type": "mrkdwn", "text": f"*Observed Count:*\n{val:,.0f} (Baseline: {cl:,.0f})"},
                                {"type": "mrkdwn", "text": f"*Anomaly Class:*\n`{typology}`"},
                                {"type": "mrkdwn", "text": f"*Severity Level:*\n`{sev}`"},
                            ],
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*Recommended Municipal Response:*\n>{rec}",
                            },
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"Alert ID: `{alert.get('alert_id', 'ALT-NEW')}` | Downtown San Diego Homeless Analysis Dashboard (Tab 7)",
                                }
                            ],
                        },
                    ],
                }
            ]
        }

    def build_email_payload(self, alert: Dict[str, Any]) -> Tuple[str, str, str]:
        """Generates Subject, HTML Body, and Plain Text Body for email notifications."""
        sev = alert.get("severity", "WARNING")
        typology = alert.get("classification", "Count Spike")
        date_str = alert.get("month_date", "N/A")
        val = alert.get("metric_value", 0.0)
        cl = alert.get("baseline_center_line", 0.0)
        rec = alert.get("recommendation", self.get_actionable_recommendation(typology, sev))
        alert_id = alert.get("alert_id", "ALT-NEW")

        subject = f"[{sev}] Alert: {typology} Detected in Downtown San Diego ({date_str})"

        plain_text = f"""
ALERT NOTIFICATION: {typology} [{sev}]
------------------------------------------------------------
Alert ID: {alert_id}
Month: {date_str}
Observed Count: {val:,.0f} (Rolling Center Line: {cl:,.0f})
Anomaly Description: {alert.get('description', '')}

Recommended Action:
{rec}

View full surveillance details in Dashboard Tab 7.
"""
        html_body = f"""
<div style="font-family: Arial, sans-serif; max-width: 600px; border: 1px solid #CBD5E1; border-radius: 8px; overflow: hidden;">
    <div style="background-color: {'#DC2626' if sev=='CRITICAL' else '#D97706'}; color: white; padding: 16px 20px;">
        <h2 style="margin: 0; font-size: 1.25rem;">[{sev}] Homeless Population Surveillance Alert</h2>
        <div style="font-size: 0.9rem; opacity: 0.9;">Downtown San Diego Partnership & DSA Monitoring</div>
    </div>
    <div style="padding: 20px; background-color: #F8FAFC;">
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 16px;">
            <tr><td style="padding: 6px 0; color: #64748B;">Alert ID:</td><td><strong>{alert_id}</strong></td></tr>
            <tr><td style="padding: 6px 0; color: #64748B;">Reporting Month:</td><td><strong>{date_str}</strong></td></tr>
            <tr><td style="padding: 6px 0; color: #64748B;">Classification:</td><td><span style="background-color: #E2E8F0; padding: 2px 6px; border-radius: 4px;">{typology}</span></td></tr>
            <tr><td style="padding: 6px 0; color: #64748B;">Observed Count:</td><td><strong>{val:,.0f}</strong> (Baseline: {cl:,.0f})</td></tr>
        </table>
        <div style="background-color: white; border-left: 4px solid {'#DC2626' if sev=='CRITICAL' else '#D97706'}; padding: 12px 16px; border-radius: 4px; margin-top: 12px;">
            <strong style="color: #0F172A;">Recommended Response:</strong>
            <p style="margin: 6px 0 0 0; color: #334155; font-size: 0.95rem;">{rec}</p>
        </div>
    </div>
    <div style="background-color: #F1F5F9; padding: 12px 20px; font-size: 0.8rem; color: #64748B; text-align: center;">
        Generated by Task 10.4 Anomaly Surveillance System | UC San Diego
    </div>
</div>
"""
        return subject, html_body, plain_text

    def ingest_anomalies(self, classified_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Extracts classified anomalies, assigns unique IDs, and stores in persistent store.
        """
        existing_alerts = self.load_alerts_store()
        existing_ids = {a["alert_id"] for a in existing_alerts}

        new_alerts = []
        now_str = datetime.now().isoformat()

        anom_rows = classified_df[classified_df["is_classified_anomaly"]].copy()

        for _, row in anom_rows.iterrows():
            dt = pd.to_datetime(row["date"])
            dt_str = dt.strftime("%Y-%m-%d")
            typology = str(row["anomaly_typology"])
            sev = str(row["anomaly_severity"])

            # Deterministic Alert ID: ALT-YYYYMM-TYPE_PREFIX
            prefix = "".join([w[0] for w in typology.split()]).upper()
            alert_id = f"ALT-{dt.strftime('%Y%m')}-{prefix}"

            # If already exists, keep existing status
            if alert_id in existing_ids:
                continue

            alert_obj = {
                "alert_id": alert_id,
                "timestamp": now_str,
                "month_date": dt_str,
                "classification": typology,
                "severity": sev,
                "metric_value": round(float(row.get("value", row.get("actual_count", 0.0))), 1),
                "baseline_center_line": round(float(row.get("center_line", 0.0)), 1),
                "shewhart_status": str(row.get("shewhart_status", "NORMAL")),
                "cusum_status": str(row.get("cusum_status", "NORMAL")),
                "description": str(row.get("anomaly_description", "")),
                "recommendation": self.get_actionable_recommendation(typology, sev),
                "status": AlertStatus.NEW.value,
                "reviewer": "",
                "reviewer_notes": "",
                "reviewed_at": "",
                "notified_at": "",
            }
            existing_alerts.append(alert_obj)
            new_alerts.append(alert_obj)

        self.save_alerts_store(existing_alerts)
        return existing_alerts

    SEVERITY_RANK = {"INFO": 0, "WARNING": 1, "CRITICAL": 2}

    def dispatch(self, min_severity: str = "WARNING", dry_run: bool = True,
                 env: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """
        Deliver alerts that are NEW, at or above `min_severity`, and not yet notified, to every
        configured channel. With dry_run=True (default) nothing is sent; the planned deliveries
        are returned. Returns one record per alert: alert_id, channels, sent, error.
        """
        env = dict(os.environ) if env is None else env
        slack_url = env.get("SLACK_WEBHOOK_URL", "").strip()
        smtp_host = env.get("SMTP_HOST", "").strip()
        email_to = [a.strip() for a in env.get("ALERT_EMAIL_TO", "").split(",") if a.strip()]
        email_ok = bool(smtp_host and email_to and env.get("ALERT_EMAIL_FROM", "").strip())
        threshold = self.SEVERITY_RANK.get(min_severity, 1)

        alerts = self.load_alerts_store()
        results = []
        for alert in alerts:
            if alert.get("status", "NEW") != AlertStatus.NEW.value or alert.get("notified_at"):
                continue
            if self.SEVERITY_RANK.get(str(alert.get("severity")), 0) < threshold:
                continue
            channels = (["slack"] if slack_url else []) + (["email"] if email_ok else [])
            record = {"alert_id": alert["alert_id"], "channels": channels, "sent": False, "error": ""}
            if not channels:
                record["error"] = "no channel configured (set SLACK_WEBHOOK_URL and/or SMTP_* / ALERT_EMAIL_*)"
            elif not dry_run:
                try:
                    if slack_url:
                        self._send_slack(slack_url, self.build_slack_payload(alert))
                    if email_ok:
                        self._send_email(env, email_to, *self.build_email_payload(alert))
                    alert["notified_at"] = datetime.now().isoformat()
                    record["sent"] = True
                except Exception as exc:  # report and continue with the next alert
                    record["error"] = f"{type(exc).__name__}: {exc}"
                    logger.error("Alert %s delivery failed: %s", alert["alert_id"], exc)
            results.append(record)
        if not dry_run:
            self.save_alerts_store(alerts)
        return results

    @staticmethod
    def _send_slack(url: str, payload: Dict[str, Any]) -> None:
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status >= 300:
                raise RuntimeError(f"Slack webhook returned HTTP {resp.status}")

    @staticmethod
    def _send_email(env: Dict[str, str], recipients: List[str], subject: str, html: str, plain: str) -> None:
        msg = MIMEMultipart("alternative")
        msg["Subject"], msg["From"], msg["To"] = subject, env["ALERT_EMAIL_FROM"], ", ".join(recipients)
        msg.attach(MIMEText(plain, "plain"))
        msg.attach(MIMEText(html, "html"))
        with smtplib.SMTP(env["SMTP_HOST"], int(env.get("SMTP_PORT", "587")), timeout=20) as server:
            server.starttls()
            if env.get("SMTP_USER"):
                server.login(env["SMTP_USER"], env.get("SMTP_PASSWORD", ""))
            server.sendmail(env["ALERT_EMAIL_FROM"], recipients, msg.as_string())

    def load_alerts_store(self) -> List[Dict[str, Any]]:
        if self.store_json_path.exists():
            try:
                with open(self.store_json_path, "r") as f:
                    return json.load(f)
            except Exception:
                pass

        if self.store_csv_path.exists():
            try:
                df = pd.read_csv(self.store_csv_path)
                return df.fillna("").to_dict(orient="records")
            except Exception:
                pass

        return []

    def save_alerts_store(self, alerts: List[Dict[str, Any]]):
        # Save JSON
        with open(self.store_json_path, "w") as f:
            json.dump(alerts, f, indent=2)

        # Save CSV
        if alerts:
            df = pd.DataFrame(alerts)
            df.to_csv(self.store_csv_path, index=False)

    def mark_as_reviewed(
        self, alert_id: str, reviewer: str, notes: str, new_status: str = "REVIEWED"
    ) -> bool:
        """Updates alert status and logs reviewer audit trail."""
        alerts = self.load_alerts_store()
        updated = False

        for a in alerts:
            if a["alert_id"] == alert_id:
                a["status"] = new_status
                a["reviewer"] = reviewer
                a["reviewer_notes"] = notes
                a["reviewed_at"] = datetime.now().isoformat()
                updated = True
                break

        if updated:
            self.save_alerts_store(alerts)
            logger.info(f"Alert {alert_id} marked as {new_status} by {reviewer}.")

        return updated
