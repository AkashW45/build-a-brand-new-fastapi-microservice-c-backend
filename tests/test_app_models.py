import pytest
from pydantic import ValidationError
from app.models import (
    FahrenheitInput,
    HealthResponse,
    TemperatureResponse,
    DistanceResponse,
    CelsiusInput,
)


def test_fahrenheit_input_valid():
    f_input = FahrenheitInput(fahrenheit=32.0)
    assert f_input.fahrenheit == 32.0
    f_input_int = FahrenheitInput(fahrenheit=0)
    assert f_input_int.fahrenheit == 0.0  # int coerced to float


def test_fahrenheit_input_zero():
    f_input = FahrenheitInput(fahrenheit=0)
    assert f_input.fahrenheit == 0.0


def test_fahrenheit_input_negative():
    f_input = FahrenheitInput(fahrenheit=-40)
    assert f_input.fahrenheit == -40.0


def test_fahrenheit_input_invalid_string():
    with pytest.raises(ValidationError):
        FahrenheitInput(fahrenheit="invalid")


def test_health_response_default_status():
    response = HealthResponse()
    assert response.status == "ok"