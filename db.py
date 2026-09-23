import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # ← must be called BEFORE os.getenv

def get_conn():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise Exception("DATABASE_URL is not set. Check your .env file.")
    return psycopg2.connect(url)

def create_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id SERIAL PRIMARY KEY,
            product TEXT,
            source TEXT,
            price NUMERIC,
            date DATE
        )
    """)
    conn.commit()
    cur.close(); conn.close()

def insert_price(data):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO prices (product, source, price, date)
        VALUES (%s, %s, %s, %s)
    """, (data["product"], data["source"], data["price"], data["date"]))
    conn.commit()
    cur.close(); conn.close()

def fetch_all():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT product, source, price, date FROM prices ORDER BY date")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows
