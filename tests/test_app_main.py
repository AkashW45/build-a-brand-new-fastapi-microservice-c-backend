import pytest
from fastapi.testclient import TestClient as FastAPITestClient
from app.main import app, flask_app

@pytest.fixture
def fastapi_client():
    return FastAPITestClient(app)

@pytest.fixture
def flask_client():
    return flask_app.test_client()

def test_health(fastapi_client):
    response = fastapi_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"  # assuming HealthResponse has status='healthy'
    # if the model is not accessible, just test status code and generic structure
    assert "version" in data

@pytest.mark.parametrize("celsius,expected_status", [
    (0, 200),
    (-273.15, 200),   # absolute zero, valid
    (-300, 422),      # below absolute zero, invalid
])
def test_convert_temperature(fastapi_client, celsius, expected_status):
    response = fastapi_client.get("/convert/temperature", params={"celsius": celsius})
    assert response.status_code == expected_status
    if expected_status == 200:
        data = response.json()
        assert "fahrenheit" in data
        assert "kelvin" in data
        assert data["celsius"] == celsius

@pytest.mark.parametrize("km,expected_status", [
    (10, 200),
    (0, 200),
    (-5, 422),
])
def test_convert_distance(fastapi_client, km, expected_status):
    response = fastapi_client.get("/convert/distance", params={"km": km})
    assert response.status_code == expected_status
    if expected_status == 200:
        data = response.json()
        assert "miles" in data
        assert "meters" in data
        assert data["kilometers"] == km

def test_fastapi_admin_page(fastapi_client):
    response = fastapi_client.get("/admin")
    assert response.status_code == 200
    html = response.text
    assert "Unit Converter Service" in html
    assert "Uptime:" in html

def test_flask_admin_page(flask_client):
    response = flask_client.get("/admin")
    assert response.status_code == 200
    html = response.data.decode()
    assert "Unit Converter Service" in html
    assert "Service Name:" in html
    assert "Uptime:" in html