import pandas as pd  # pyright: ignore[reportMissingModuleSource]

def build_df(rows):
    df = pd.DataFrame(rows, columns=["product", "source", "price", "date"])
    df["date"] = pd.to_datetime(df["date"])
    return df

def detect_drops(df, threshold=0.05):
    alerts = []
    for (product, source), group in df.groupby(["product", "source"]):
        group = group.sort_values("date")
        group["pct_change"] = group["price"].pct_change()
        drops = group[group["pct_change"] <= -threshold]
        for _, row in drops.iterrows():
            alerts.append(f"🔻 {product} ({source}): dropped {row['pct_change']*100:.1f}% on {row['date'].date()}")
    return alerts