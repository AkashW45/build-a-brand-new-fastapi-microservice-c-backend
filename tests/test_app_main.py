import re
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_admin_returns_200_and_html():
    response = client.get("/admin")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_admin_contains_service_name_and_uptime():
    response = client.get("/admin")
    body = response.text
    assert "Unit Converter Service" in body
    assert "Uptime:" in body


def test_admin_uptime_positive():
    response = client.get("/admin")
    # Extract the uptime value from the HTML. The format is something like: uptime = timedelta → "0:00:00.000001"
    match = re.search(r"Uptime:\s*([\d:.]+)", response.text)
    assert match, "Uptime value not found"
    uptime_str = match.group(1)
    # Should be a positive timedelta string, e.g., "0:00:00.000001" – not zero or negative. 
    # We'll check it's non-empty and contains at least one non-zero digit.
    assert any(c.isdigit() and c != '0' for c in uptime_str), f"Uptime seems zero: {uptime_str}"


def test_admin_method_not_allowed_post():
    response = client.post("/admin")
    assert response.status_code == 405


def test_admin_with_extra_query_params_ignored():
    response = client.get("/admin?foo=bar")
    assert response.status_code == 200
    assert "Unit Converter Service" in response.text