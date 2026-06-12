import pytest
from pydantic import ValidationError

from app.models import TemperatureResponse, DistanceResponse, HealthResponse, AdminInfo, CelsiusInput


class TestTemperatureResponse:
    def test_valid_creation(self):
        resp = TemperatureResponse(celsius=100.0, fahrenheit=212.0, kelvin=373.15)
        assert resp.celsius == 100.0
        assert resp.fahrenheit == 212.0
        assert resp.kelvin == 373.15

    def test_int_coercion(self):
        resp = TemperatureResponse(celsius=0, fahrenheit=32, kelvin=273)
        assert isinstance(resp.celsius, float)
        assert resp.celsius == 0.0


class TestDistanceResponse:
    def test_valid_creation(self):
        resp = DistanceResponse(kilometers=1.0, miles=0.621371, meters=1000.0)
        assert resp.kilometers == 1.0
        assert resp.miles == 0.621371
        assert resp.meters == 1000.0


class TestHealthResponse:
    def test_default_status(self):
        resp = HealthResponse()
        assert resp.status == "ok"

    def test_custom_status(self):
        resp = HealthResponse(status="healthy")
        assert resp.status == "healthy"


class TestAdminInfo:
    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            AdminInfo()
        with pytest.raises(ValidationError):
            AdminInfo(service_name="test")  # missing uptime_seconds


class TestCelsiusInput:
    def test_valid_float(self):
        inp = CelsiusInput(celsius=25.0)
        assert inp.celsius == 25.0

    def test_valid_int(self):
        inp = CelsiusInput(celsius=25)
        assert isinstance(inp.celsius, float)
        assert inp.celsius == 25.0

    def test_negative_value(self):
        inp = CelsiusInput(celsius=-10.0)
        assert inp.celsius == -10.0

    def test_zero_value(self):
        inp = CelsiusInput(celsius=0.0)
        assert inp.celsius == 0.0

    def test_missing_required(self):
        with pytest.raises(ValidationError):
            CelsiusInput()

    def test_invalid_type(self):
        with pytest.raises(ValidationError):
            CelsiusInput(celsius="hot")