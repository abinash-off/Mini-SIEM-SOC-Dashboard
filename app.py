from flask import Flask, jsonify, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import SECRET_KEY
from database.db import get_connection, initialize_database
from collector.log_collector import process_event

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024

limiter = Limiter(key_func=get_remote_address, app=app, default_limits=["100 per minute"])
initialize_database()


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/api/stats")
def stats():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM events")
    total_events = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM alerts")
    total_alerts = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity = 'CRITICAL'")
    critical = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity = 'HIGH'")
    high = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity = 'MEDIUM'")
    medium = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity = 'LOW'")
    low = cursor.fetchone()[0]
    connection.close()
    return jsonify({
        "total_events": total_events,
        "total_alerts": total_alerts,
        "critical_alerts": critical,
        "high_alerts": high,
        "medium_alerts": medium,
        "low_alerts": low
    })


@app.route("/api/alerts")
def alerts():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, timestamp, alert_type, severity, source_ip,
               description, mitre_id, status
        FROM alerts ORDER BY id DESC LIMIT 100
    """)
    rows = cursor.fetchall()
    connection.close()
    return jsonify([dict(row) for row in rows])


@app.route("/api/events")
def events():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, timestamp, source, source_ip, username,
               event_type, message, severity
        FROM events ORDER BY id DESC LIMIT 100
    """)
    rows = cursor.fetchall()
    connection.close()
    return jsonify([dict(row) for row in rows])


@app.route("/api/events", methods=["POST"])
@limiter.limit("30 per minute")
def receive_event():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON object"}), 400

    required_fields = ["timestamp", "source", "event_type"]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    for field in ("source", "event_type", "message", "username", "source_ip"):
        if field in data and len(str(data[field])) > 500:
            return jsonify({"error": f"Field too long: {field}"}), 400

    result = process_event(data)
    return jsonify({"success": True, "result": result}), 201


@app.route("/api/alerts/<int:alert_id>/status", methods=["PUT"])
@limiter.limit("30 per minute")
def update_alert_status(alert_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON object"}), 400

    status = data.get("status")
    allowed_statuses = ["OPEN", "INVESTIGATING", "RESOLVED"]
    if status not in allowed_statuses:
        return jsonify({"error": "Invalid status"}), 400

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE alerts SET status = ? WHERE id = ?", (status, alert_id))
    connection.commit()
    updated = cursor.rowcount
    connection.close()

    if not updated:
        return jsonify({"error": "Alert not found"}), 404
    return jsonify({"success": True, "status": status})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
