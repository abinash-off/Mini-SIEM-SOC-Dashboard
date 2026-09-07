import json
from database.db import get_connection
from detection.rules import detect_event


def process_event(event):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO events
        (timestamp, source, source_ip, username, event_type, message, severity)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        event.get("timestamp"),
        event.get("source"),
        event.get("source_ip"),
        event.get("username"),
        event.get("event_type"),
        event.get("message"),
        event.get("severity", "LOW")
    ))

    event_id = cursor.lastrowid
    alerts = detect_event(event)

    for alert in alerts:
        cursor.execute("""
            INSERT INTO alerts
            (event_id, timestamp, alert_type, severity, source_ip, description, mitre_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            event_id,
            alert["timestamp"],
            alert["alert_type"],
            alert["severity"],
            alert["source_ip"],
            alert["description"],
            alert["mitre_id"]
        ))

    connection.commit()
    connection.close()
    return {"event_id": event_id, "alerts_created": len(alerts)}


def process_json_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        events = json.load(file)
    return [process_event(event) for event in events]
