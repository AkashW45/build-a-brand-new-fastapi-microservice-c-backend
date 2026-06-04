from fastapi import FastAPI, Query
from app.models import TemperatureResponse, DistanceResponse, HealthResponse

app = FastAPI(title="Unit Converter Service", description="Temperature and distance conversion API", version="1.0.0")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse()


@app.get("/convert/temperature", response_model=TemperatureResponse)
async def convert_temperature(celsius: float = Query(..., ge=-273.15, description="Temperature in Celsius (must be >= -273.15)")):
    fahrenheit = (celsius * 9 / 5) + 32
    kelvin = celsius + 273.15
    return TemperatureResponse(celsius=celsius, fahrenheit=round(fahrenheit, 2), kelvin=round(kelvin, 2))


@app.get("/convert/distance", response_model=DistanceResponse)
async def convert_distance(km: float = Query(..., ge=0, description="Distance in kilometers (must be >= 0)")):
    miles = km * 0.621371
    meters = km * 1000
    return DistanceResponse(kilometers=km, miles=round(miles, 2), meters=round(meters, 2))
