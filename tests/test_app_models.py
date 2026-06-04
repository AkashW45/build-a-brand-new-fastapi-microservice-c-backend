import pytest
from pydantic import ValidationError
from app.models import TemperatureResponse, DistanceResponse, HealthResponse


class TestTemperatureResponse:
    def test_valid_instantiation(self):
        """Happy path: valid float values produce expected object."""
        t = TemperatureResponse(celsius=100.0, fahrenheit=212.0, kelvin=373.15)
        assert t.celsius == 100.0
        assert t.fahrenheit == 212.0
        assert t.kelvin == 373.15

    def test_zero_values(self):
        """Edge case: zero Celsius still valid."""
        t = TemperatureResponse(celsius=0.0, fahrenheit=32.0, kelvin=273.15)
        assert t.celsius == 0.0
        assert t.fahrenheit == 32.0
        assert t.kelvin == 273.15

    def test_large_numbers(self):
        """Edge case: large float values accepted without issue."""
        large = 1e30
        t = TemperatureResponse(celsius=large, fahrenheit=large * 9 / 5 + 32, kelvin=large + 273.15)
        assert t.celsius == large
        assert t.fahrenheit == large * 9 / 5 + 32
        assert t.kelvin == large + 273.15

    def test_missing_field_raises_validation_error(self):
        """Error path: missing required field raises ValidationError."""
        with pytest.raises(ValidationError):
            TemperatureResponse(celsius=20.0, kelvin=293.15)  # missing fahrenheit


class TestDistanceResponse:
    def test_valid_instantiation(self):
        """Happy path: valid km produces correct miles and meters."""
        d = DistanceResponse(kilometers=1.0, miles=0.621371, meters=1000.0)
        assert d.kilometers == 1.0
        assert d.miles == 0.621371
        assert d.meters == 1000.0

    def test_invalid_type_raises_validation_error(self):
        """Error path: string instead of float raises ValidationError."""
        with pytest.raises(ValidationError):
            DistanceResponse(kilometers="abc", miles=0.0, meters=0.0)


class TestHealthResponse:
    def test_default_status(self):
        """Happy path: HealthResponse defaults status to 'ok'."""
        h = HealthResponse()
        assert h.status == "ok"

    def test_custom_status(self):
        """Edge case: status can be overridden."""
        h = HealthResponse(status="degraded")
        assert h.status == "degraded"