from backend.services.troubleshooting_service import analyze


def test_detects_admin_down():
    summary, findings = analyze("GigabitEthernet0/0 is administratively down, line protocol is down")
    assert "Interface administratively down" in findings[0][1]


def test_detects_no_default_route():
    _, findings = analyze("Gateway of last resort is not set")
    assert any("No default route" in item[1] for item in findings)
