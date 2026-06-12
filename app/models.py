from pydantic import BaseModel, Field


class TemperatureResponse(BaseModel):
    celsius: float
    fahrenheit: float
    kelvin: float


class DistanceResponse(BaseModel):
    kilometers: float
    miles: float
    meters: float


class HealthResponse(BaseModel):
    status: str = Field(default="ok")


class AdminInfo(BaseModel):
    service_name: str
    uptime_seconds: float


class CelsiusInput(BaseModel):
    celsius: float


class FahrenheitInput(BaseModel):
    fahrenheit: float


def fahrenheit_to_celsius(f: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (f - 32) * 5.0 / 9.0
