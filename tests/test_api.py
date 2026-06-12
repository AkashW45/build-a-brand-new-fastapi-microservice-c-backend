from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_temperature_conversion():
    response = client.get("/convert/temperature?celsius=100")
    assert response.status_code == 200
    data = response.json()
    assert data["celsius"] == 100.0
    assert data["fahrenheit"] == 212.0
    assert data["kelvin"] == 373.15


def test_distance_conversion():
    response = client.get("/convert/distance?km=1")
    assert response.status_code == 200
    data = response.json()
    assert data["kilometers"] == 1.0
    assert data["miles"] == 0.62  # rounding to 2 decimals gives 0.62
    assert data["meters"] == 1000.0


def test_temperature_below_absolute_zero_returns_422():
    response = client.get("/convert/temperature?celsius=-300")
    assert response.status_code == 422


def test_distance_negative_km_returns_422():
    response = client.get("/convert/distance?km=-5")
    assert response.status_code == 422


def test_missing_celsius_returns_422():
    response = client.get("/convert/temperature")
    assert response.status_code == 422


def test_missing_km_returns_422():
    response = client.get("/convert/distance")
    assert response.status_code == 422


def test_admin_not_available_on_fastapi():
    response = client.get("/admin")
    # Admin page is served by a separate Flask service (port 8001), not FastAPI
    assert response.status_code == 404


def test_admin_page_via_flask():
    from app.admin_flask import app as flask_app
    flask_client = flask_app.test_client()
    response = flask_client.get("/admin")
    assert response.status_code == 200
    html = response.text
    assert "Unit Converter Service" in html
    assert "Uptime" in html
    assert "seconds" in html or "minutes" in html


def test_root_html_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    html = response.text
    assert "Fahrenheit to Celsius" in html
    assert "Convert" in html


def test_fahrenheit_conversion_via_api():
    response = client.get("/convert/temperature?fahrenheit=212")
    assert response.status_code == 200
    data = response.json()
    assert data["celsius"] == 100.0
    assert data["fahrenheit"] == 212.0
    assert data["kelvin"] == 373.15
