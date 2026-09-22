from importlib import import_module

# Load Streamlit dynamically so environments without its type stubs do not
# report a static "Import streamlit could not be resolved" error.
st = import_module("streamlit")
px = import_module("plotly.express")
from db import fetch_all, create_table
from analysis import build_df, detect_drops
from scraper import scrape_amazon, scrape_flipkart
from db import insert_price

create_table()

st.title("📦 Price Intelligence Engine")

# Manual trigger
if st.button("🔄 Scrape Now"):
    TARGETS = [
        {"fn": scrape_amazon, "url": "YOUR_AMAZON_URL", "name": "iPhone 15"},
        {"fn": scrape_flipkart, "url": "YOUR_FLIPKART_URL", "name": "iPhone 15"},
    ]
    for t in TARGETS:
        data = t["fn"](t["url"], t["name"])
        if data["price"]:
            insert_price(data)
    st.success("Scraped & saved!")

rows = fetch_all()
if rows:
    df = build_df(rows)

    # Price trend chart
    fig = px.line(df, x="date", y="price", color="source",
                  facet_col="product", title="Price Trends")
    st.plotly_chart(fig)

    # Alerts
    st.subheader("⚠️ Price Drop Alerts")
    alerts = detect_drops(df)
    for a in alerts:
        st.warning(a)

    # Raw table
    st.dataframe(df)