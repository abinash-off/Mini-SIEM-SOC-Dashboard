from detection.rules import detect_event

def test_powershell_detection():
    alerts=detect_event({"event_type":"process_execution","message":"powershell -EncodedCommand x","timestamp":"2026-01-01T00:00:00Z"})
    assert any(a["mitre_id"]=="T1059.001" for a in alerts)

def test_clean_event():
    assert detect_event({"event_type":"login","message":"successful login"})==[]
