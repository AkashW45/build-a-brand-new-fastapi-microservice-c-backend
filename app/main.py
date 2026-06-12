from fastapi import FastAPI, Query, HTMLResponse, Form
from datetime import datetime, timezone
from app.models import TemperatureResponse, DistanceResponse, HealthResponse

app = FastAPI(title="Unit Converter Service", description="Temperature and distance conversion API", version="1.0.0")
start_time = datetime.now(timezone.utc)


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


@app.get("/admin", response_class=HTMLResponse)
async def admin_page():
    uptime = datetime.now(timezone.utc) - start_time
    html_content = f"""
    <html>
        <head><title>Admin - Unit Converter</title></head>
        <body>
            <h1>Unit Converter Service</h1>
            <p>Service Name: Unit Converter Service</p>
            <p>Uptime: {uptime}</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/", response_class=HTMLResponse)
async def home_page():
    html_content = """
    <html>
        <head><title>Celsius to Fahrenheit Converter</title></head>
        <body>
            <h1>Celsius to Fahrenheit Converter</h1>
            <form method="post" action="/">
                <label for="celsius">Celsius:</label>
                <input type="number" name="celsius" step="any" required>
                <input type="submit" value="Convert">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/", response_class=HTMLResponse)
async def convert_home(celsius: float = Form(...)):
    fahrenheit = (celsius * 9/5) + 32
    kelvin = celsius + 273.15
    html_content = f"""
    <html>
        <head><title>Celsius to Fahrenheit Converter</title></head>
        <body>
            <h1>Celsius to Fahrenheit Converter</h1>
            <form method="post" action="/">
                <label for="celsius">Celsius:</label>
                <input type="number" name="celsius" step="any" required>
                <input type="submit" value="Convert">
            </form>
            <p>{celsius}°C = {round(fahrenheit, 2)}°F = {round(kelvin, 2)}K</p>
            <p><a href="/">Convert another</a></p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


# Flask admin page on port 5000
from flask import Flask

flask_app = Flask(__name__)

@flask_app.route('/admin')
def flask_admin():
    uptime = datetime.now(timezone.utc) - start_time
    html = f"""<html><head><title>Admin - Unit Converter</title></head><body><h1>Unit Converter Service</h1><p>Service Name: Unit Converter Service</p><p>Uptime: {uptime}</p></body></html>"""
    return html

if __name__ == '__main__':
    print("Starting Flask admin server on port 5000...")
    flask_app.run(host='0.0.0.0', port=5000)
