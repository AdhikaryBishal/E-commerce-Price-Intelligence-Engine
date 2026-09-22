import psycopg2  # type: ignore[import-not-found]
import os

def get_conn():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

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