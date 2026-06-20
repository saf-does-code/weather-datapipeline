import requests
import psycopg2
import os

def get_weather(city, latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max&timezone=auto"
    response = requests.get(url)
    data = response.json()
    dates = data['daily']['time']
    temps = data['daily']['temperature_2m_max']
    return dates, temps

def save_to_db(city, dates, temps):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()
    for date, temp in zip(dates, temps):
        cursor.execute("""
            INSERT INTO weather (date, temperature_max_c, city)
            VALUES (%s, %s, %s)
            ON CONFLICT (date, city) DO NOTHING
        """, (date, temp, city))
    conn.commit()
    cursor.close()
    conn.close()

cities = [
    {"name": "Dubai", "latitude": 25.07, "longitude": 55.14},
    {"name": "London", "latitude": 51.51, "longitude": -0.13},
    {"name": "New York", "latitude": 40.71, "longitude": -74.01},
    {"name": "Warsaw", "latitude": 52.23, "longitude": 21.01},
    {"name": "Lisbon", "latitude": 38.72, "longitude": -9.14},
    {"name": "Madrid", "latitude": 40.42, "longitude": -3.70},
    {"name": "Cairo", "latitude": 30.06, "longitude": 31.25},
    {"name": "Nairobi", "latitude": -1.29, "longitude": 36.82},
    {"name": "Khartoum", "latitude": 15.55, "longitude": 32.53},
    {"name": "Toronto", "latitude": 43.65, "longitude": -79.38},
    {"name": "Beijing", "latitude": 39.91, "longitude": 116.39},
    {"name": "Tokyo", "latitude": 35.69, "longitude": 139.69},
    {"name": "Mumbai", "latitude": 19.08, "longitude": 72.88},
    {"name": "Rio de Janeiro", "latitude": -22.91, "longitude": -43.17},
    {"name": "Sydney", "latitude": -33.87, "longitude": 151.21},
    {"name": "Amsterdam", "latitude": 52.37, "longitude": 4.90},
    {"name": "Abuja", "latitude": 9.07, "longitude": 7.40},
    {"name": "Mbabane", "latitude": -26.32, "longitude": 31.13},
    {"name": "Tbilisi", "latitude": 41.69, "longitude": 44.83},
    {"name": "Istanbul", "latitude": 41.01, "longitude": 28.95},
    {"name": "Paris", "latitude": 48.85, "longitude": 2.35},
    {"name": "Rome", "latitude": 41.90, "longitude": 12.50},
    {"name": "Dublin", "latitude": 53.33, "longitude": -6.25},
    {"name": "Doha", "latitude": 25.29, "longitude": 51.53},
    {"name": "Riyadh", "latitude": 24.69, "longitude": 46.72},
    {"name": "Tehran", "latitude": 35.69, "longitude": 51.42},
    {"name": "Islamabad", "latitude": 33.72, "longitude": 73.04},
    {"name": "Seoul", "latitude": 37.57, "longitude": 126.98},
    {"name": "Athens", "latitude": 37.98, "longitude": 23.73},
]

for city in cities:
    dates, temps = get_weather(city["name"], city["latitude"], city["longitude"])
    save_to_db(city["name"], dates, temps)
    print(f"Saved {city['name']} data successfully!")
