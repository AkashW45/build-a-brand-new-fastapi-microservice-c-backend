import pytest
from pydantic import ValidationError
from app.models import TemperatureResponse, DistanceResponse, HealthResponse, AdminInfo


def test_temperature_response_valid():
    data = {"celsius": 100.0, "fahrenheit": 212.0, "kelvin": 373.15}
    obj = TemperatureResponse(**data)
    assert obj.celsius == 100.0
    assert obj.fahrenheit == 212.0
    assert obj.kelvin == 373.15


def test_temperature_response_missing_field():
    with pytest.raises(ValidationError):
        TemperatureResponse(celsius=0)


def test_distance_response_valid():
    obj = DistanceResponse(kilometers=1.0, miles=0.621371, meters=1000.0)
    assert obj.kilometers == 1.0
    assert obj.miles == 0.621371
    assert obj.meters == 1000.0


def test_health_response_default():
    obj = HealthResponse()
    assert obj.status == "ok"


def test_admin_info_valid():
    obj = AdminInfo(service_name="Unit Converter", uptime_seconds=3600.5)
    assert obj.service_name == "Unit Converter"
    assert obj.uptime_seconds == 3600.5


def test_admin_info_missing_service_name():
    with pytest.raises(ValidationError):
        AdminInfo(uptime_seconds=100)


def test_temperature_response_zero_values():
    obj = TemperatureResponse(celsius=0.0, fahrenheit=32.0, kelvin=273.15)
    assert obj.celsius == 0.0
    assert obj.fahrenheit == 32.0
    assert obj.kelvin == 273.15