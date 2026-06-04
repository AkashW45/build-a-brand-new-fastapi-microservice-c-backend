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
