import time
from datetime import datetime, timedelta
from scraper import scrape_amazon, scrape_flipkart
from db import insert_price, create_table

create_table()

TARGETS = [
    {"fn": scrape_amazon, "url": "YOUR_URL", "name": "iPhone 15"},
    {"fn": scrape_flipkart, "url": "YOUR_URL", "name": "iPhone 15"},
]

def run_scraper():
    for t in TARGETS:
        data = t["fn"](t["url"], t["name"])
        if data["price"]:
            insert_price(data)
    print("✅ Scraped & stored")

next_run = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
if next_run <= datetime.now():
    next_run += timedelta(days=1)

while True:
    now = datetime.now()
    if now >= next_run:
        run_scraper()
        next_run += timedelta(days=1)
    time.sleep(60)