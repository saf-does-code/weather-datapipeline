# Weather Data Pipeline
An automated data pipeline that collects daily maximum temperature data for Dubai and exposes it through a REST API.

## What does it do?
- Fetches daily weather data of 31 cities across 6 continents from the Open-Meteo API  
- Stores historical records in a PostgreSQL database (Neon)
- Runs automatically every day at 10am Dubai time via GitHub Actions
- Serves the data through a FastAPI REST API

## Tech stack
- Python 3.9
- PostgreSQL (Neon)
- FastAPI + Uvicorn
- GitHub Actions (automated scheduling)

## API endpoints
| Endpoint | Description |
|----------|-------------|
| `GET /weather/latest` | Returns the most recent day's temperature |
| `GET /weather/history` | Returns all historical temperature records |
| `GET /weather/stats` | Returns hottest, coldest, and average temperature for a city |
| `GET /weather/cities` | Returns a list of all available cities |
All endpoints (except `/weather/cities`) accept an optional `?city=` parameter. Defaults to Dubai if not specified.

## How to run locally
1. Clone the repo
2. Install dependencies:
pip install fastapi uvicorn psycopg2-binary requests
3. Set your database connection string:
set DATABASE_URL=your-neon-connection-string
4. Start the API:
python -m uvicorn main:app --reload
5. Visit `http://127.0.0.1:8000/docs` for interactive API documentation
