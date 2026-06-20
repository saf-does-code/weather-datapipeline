import os
import psycopg2
from fastapi import FastAPI, Query

app = FastAPI()

def get_conn():
    return psycopg2.connect(os.environ["DATABASE_URL"])

@app.get("/weather/latest")
def latest(city: str = Query(default="Dubai")):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, temperature_max_c, city
        FROM weather
        WHERE city = %s
        ORDER BY date DESC
        LIMIT 1
    """, (city,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return {"date": str(row[0]), "temperature_max_c": row[1], "city": row[2]}

@app.get("/weather/history")
def history(city: str = Query(default="Dubai")):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, temperature_max_c, city
        FROM weather
        WHERE city = %s
        ORDER BY date DESC
    """, (city,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"date": str(r[0]), "temperature_max_c": r[1], "city": r[2]} for r in rows]

@app.get("/weather/stats")
def stats(city: str = Query(default="Dubai")):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            MAX(temperature_max_c) as hottest,
            MIN(temperature_max_c) as coldest,
            ROUND(AVG(temperature_max_c)::numeric, 1) as average
        FROM weather
        WHERE city = %s
    """, (city,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return {
        "city": city,
        "hottest": row[0],
        "coldest": row[1],
        "average": row[2]
    }

@app.get("/weather/cities")
def cities():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT city
        FROM weather
        ORDER BY city
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [r[0] for r in rows]
