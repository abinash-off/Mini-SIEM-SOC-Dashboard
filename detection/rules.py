from datetime import datetime, timezone


def detect_event(event):
    alerts = []
    message = str(event.get("message", "")).lower()
    event_type = str(event.get("event_type", "")).lower()
    source_ip = event.get("source_ip")
    timestamp = event.get("timestamp", datetime.now(timezone.utc).isoformat())

    if event_type == "failed_login":
        alerts.append({
            "timestamp": timestamp,
            "alert_type": "Possible Brute Force",
            "severity": "HIGH",
            "source_ip": source_ip,
            "description": "Authentication failure detected; repeated failures may indicate brute force activity.",
            "mitre_id": "T1110"
        })

    powershell_keywords = ["powershell", "encodedcommand", "invoke-expression", "downloadstring"]
    if event_type == "process_execution" and any(k in message for k in powershell_keywords):
        alerts.append({
            "timestamp": timestamp,
            "alert_type": "Suspicious PowerShell",
            "severity": "HIGH",
            "source_ip": source_ip,
            "description": "Potentially suspicious PowerShell execution detected.",
            "mitre_id": "T1059.001"
        })

    if event_type == "network_connection" and "multiple ports" in message:
        alerts.append({
            "timestamp": timestamp,
            "alert_type": "Possible Port Scan",
            "severity": "MEDIUM",
            "source_ip": source_ip,
            "description": "Multiple destination ports contacted from a single source.",
            "mitre_id": "T1046"
        })

    if event_type == "privilege_change":
        alerts.append({
            "timestamp": timestamp,
            "alert_type": "Privilege Change",
            "severity": "HIGH",
            "source_ip": source_ip,
            "description": "User privilege modification detected.",
            "mitre_id": "T1098"
        })

    malware_keywords = ["malware", "trojan", "agenttesla", "ransomware"]
    if any(k in message for k in malware_keywords):
        alerts.append({
            "timestamp": timestamp,
            "alert_type": "Malware Indicator",
            "severity": "CRITICAL",
            "source_ip": source_ip,
            "description": "Potential malware indicator detected in event.",
            "mitre_id": "T1204"
        })

    return alerts
