# Unit Converter Service

A stateless, in-memory REST API service built with FastAPI and uvicorn.
Provides temperature (Celsius to Fahrenheit/Kelvin) and distance (Kilometers to Miles/Meters) conversions.

## Endpoints

- `GET /health` – Returns `{"status": "ok"}`
- `GET /convert/temperature?celsius=<number>` – Temperature conversion (Celsius must be ≥ -273.15)
- `GET /convert/distance?km=<number>` – Distance conversion (km must be ≥ 0)

## Getting Started

### Install dependencies
bash
pip install -r requirements.txt


### Run the server
bash
uvicorn app.main:app --reload


### Run tests
bash
pytest


## Project Structure


├── app
│   ├── __init__.py
│   ├── main.py
│   └── models.py
├── tests
│   ├── __init__.py
│   └── test_api.py
├── requirements.txt
└── README.md

