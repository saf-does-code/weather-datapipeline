import requests
import csv
import psycopg2
import os

# fetch data
url = "https://api.open-meteo.com/v1/forecast?latitude=25.07&longitude=55.14&daily=temperature_2m_max&timezone=Asia%2FDubai"
response = requests.get(url)
data = response.json()

dates = data['daily']['time']
temps = data['daily']['temperature_2m_max']

# insert into database
conn = psycopg2.connect(os.environ["DATABASE_URL"])
cursor = conn.cursor()

for date, temp in zip(dates, temps):
    cursor.execute("""
        INSERT INTO weather (date, temperature_max_c)
        VALUES (%s, %s)
        ON CONFLICT (date) DO NOTHING
    """, (date, temp))

conn.commit()
cursor.close()
conn.close()

print("Pipeline ran successfully!")