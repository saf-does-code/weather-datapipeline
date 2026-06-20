import os
import psycopg2
from fastapi import FastAPI

app = FastAPI()

def get_conn():
    return psycopg2.connect(os.environ["DATABASE_URL"])

@app.get("/weather/latest")
def latest():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, temperature_max_c 
        FROM weather 
        ORDER BY date DESC 
        LIMIT 1
    """)
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return {"date": str(row[0]), "temperature_max_c": row[1]}

@app.get("/weather/history")
def history():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, temperature_max_c 
        FROM weather 
        ORDER BY date DESC
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"date": str(r[0]), "temperature_max_c": r[1]} for r in rows]

@app.get("/weather/stats")
def stats():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            MAX(temperature_max_c) as hottest,
            MIN(temperature_max_c) as coldest,
            ROUND(AVG(temperature_max_c)::numeric, 1) as average
        FROM weather
    """)
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return {
        "hottest": row[0],
        "coldest": row[1],
        "average": row[2]
    }