import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize("celsius, expected_f, expected_k", [
    (0, 32.0, 273.15),
    (100, 212.0, 373.15),
    (-40, -40.0, 233.15),
    (-273.15, -459.67, 0.0),
])
def test_temperature_success(celsius, expected_f, expected_k):
    response = client.get("/convert/temperature", params={"celsius": celsius})
    assert response.status_code == 200
    data = response.json()
    assert data["celsius"] == celsius
    assert data["fahrenheit"] == expected_f
    assert data["kelvin"] == expected_k


def test_temperature_validation():
    # missing celsius parameter
    response = client.get("/convert/temperature")
    assert response.status_code == 422

    # non-numeric value
    response = client.get("/convert/temperature?celsius=abc")
    assert response.status_code == 422

    # value below absolute zero
    response = client.get("/convert/temperature", params={"celsius": -300})
    assert response.status_code == 422


@pytest.mark.parametrize("km, expected_miles, expected_meters", [
    (0, 0.0, 0.0),
    (1, 0.62, 1000.0),
    (10, 6.21, 10000.0),
    (100, 62.14, 100000.0),
])
def test_distance_success(km, expected_miles, expected_meters):
    response = client.get("/convert/distance", params={"km": km})
    assert response.status_code == 200
    data = response.json()
    assert data["kilometers"] == km
    assert data["miles"] == expected_miles
    assert data["meters"] == expected_meters


def test_distance_validation():
    # missing km parameter
    response = client.get("/convert/distance")
    assert response.status_code == 422

    # negative distance
    response = client.get("/convert/distance", params={"km": -5})
    assert response.status_code == 422