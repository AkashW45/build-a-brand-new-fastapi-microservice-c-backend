from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Happy path: health endpoint returns 200 and a JSON body."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


def test_convert_temperature_happy_path():
    """Happy path: convert 100°C to Fahrenheit and Kelvin."""
    response = client.get("/convert/temperature?celsius=100")
    assert response.status_code == 200
    data = response.json()
    assert data["celsius"] == 100
    assert data["fahrenheit"] == 212.0
    assert data["kelvin"] == 373.15


def test_convert_temperature_edge_minimum():
    """Edge case: convert exactly -273.15°C (absolute zero)."""
    response = client.get("/convert/temperature?celsius=-273.15")
    assert response.status_code == 200
    data = response.json()
    assert data["celsius"] == -273.15
    assert data["fahrenheit"] == -459.67
    assert data["kelvin"] == 0.0


def test_convert_temperature_error_below_absolute_zero():
    """Error path: temperature below absolute zero returns validation error."""
    response = client.get("/convert/temperature?celsius=-300")
    assert response.status_code == 422


def test_root_get():
    """Happy path: the home page returns an HTML form."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    content = response.text
    assert "Celsius to Fahrenheit Converter" in content


def test_root_post_happy():
    """Happy path: submitting the form with a valid temperature shows the conversion result."""
    response = client.post("/", data={"celsius": "25"})
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    content = response.text
    assert "25.0°C = 77.0°F = 298.15K" in content