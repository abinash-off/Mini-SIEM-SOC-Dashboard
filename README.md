# Mini SIEM + SOC Dashboard

A defensive cybersecurity project that ingests security events, stores them in SQLite, applies detection rules, generates alerts, maps detections to MITRE ATT&CK technique IDs, and displays results in a web-based SOC dashboard.

## Features

- Flask REST API for event ingestion
- SQLite event and alert storage
- Detection rules for failed-login/brute-force indicators, suspicious PowerShell, possible port scanning, privilege changes, and malware indicators
- Severity levels: LOW, MEDIUM, HIGH, CRITICAL
- MITRE ATT&CK technique mapping
- SOC dashboard with statistics, alerts, and recent events
- Automatic dashboard refresh every 10 seconds
- Basic API rate limiting and input validation
- Parameterized SQL queries
- Environment-based Flask secret configuration
- Sample security events for demonstration

## Architecture

```text
Security Logs / Test Events
          |
          v
     Event Collector
          |
          v
     SQLite Database
          |
          v
    Detection Engine
          |
          v
       Alerts
          |
          v
     Flask REST API
          |
          v
     SOC Dashboard
```

## Requirements

- Python 3.10+
- pip

## Installation

```bash
git clone https://github.com/abinash-off/Mini-SIEM-SOC-Dashboard.git
cd Mini-SIEM-SOC-Dashboard
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

Linux/macOS/Kali:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set a strong `FLASK_SECRET_KEY`.

Run:

```bash
python app.py
```

Open `http://127.0.0.1:5000`.

## Load sample logs

From the project root:

```bash
python -c "from collector.log_collector import process_json_file; print(process_json_file('sample_logs/security_events.json'))"
```

Refresh the dashboard. The sample data demonstrates failed logins, suspicious PowerShell, network scanning indicators, privilege changes, and a malware indicator.

## API

- `GET /api/stats` - dashboard statistics
- `GET /api/alerts` - recent alerts
- `GET /api/events` - recent events
- `POST /api/events` - submit a security event
- `PUT /api/alerts/<alert_id>/status` - update alert status

Example event:

```json
{
  "timestamp": "2026-09-07T10:00:00Z",
  "source": "linux-server",
  "source_ip": "192.168.1.99",
  "username": "root",
  "event_type": "failed_login",
  "message": "Failed SSH login",
  "severity": "MEDIUM"
}
```

Allowed alert statuses: `OPEN`, `INVESTIGATING`, `RESOLVED`.

## Project Structure

```text
Mini-SIEM-SOC-Dashboard/
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── collector/
│   ├── __init__.py
│   └── log_collector.py
├── database/
│   ├── __init__.py
│   └── db.py
├── detection/
│   ├── __init__.py
│   └── rules.py
├── sample_logs/
│   └── security_events.json
├── static/
│   ├── app.js
│   └── style.css
└── templates/
    └── index.html
```

## Security Notes

This project is intended for defensive learning, SOC practice, and controlled lab environments. It does not perform offensive actions or automatic destructive response.

Do not commit `.env`, credentials, API keys, production databases, or sensitive logs. The built-in Flask development server is not intended for production deployment.

## Future Enhancements

- Windows Event Log collector
- Linux auth.log collector
- WebSocket-based live updates
- Rule correlation and threshold-based brute-force detection
- IOC enrichment and threat intelligence
- MITRE ATT&CK technique browser
- Incident management workflow
- Analyst authentication and RBAC
- Audit logging
- PostgreSQL support
- Docker deployment
- AI-assisted alert explanation and triage recommendations

## License

For educational and portfolio use.
