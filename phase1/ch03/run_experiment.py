"""Reproduce the Chapter 3 TSLA moving-average signal exercise."""
import datetime as dt, json, urllib.request, csv
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

TICKER = "TSLA"
OUT = Path(__file__).parent
start = int(dt.datetime(2024, 11, 14, tzinfo=dt.timezone.utc).timestamp())
end = int(dt.datetime(2026, 11, 14, tzinfo=dt.timezone.utc).timestamp())
url = f"https://query1.finance.yahoo.com/v8/finance/chart/{TICKER}?period1={start}&period2={end}&interval=1d&events=div%2Csplits"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
obj = json.load(urllib.request.urlopen(req, timeout=30))["chart"]["result"][0]
rows = [(dt.datetime.fromtimestamp(t, dt.timezone.utc).date(), float(p)) for t,p in zip(obj["timestamp"], obj["indicators"]["quote"][0]["close"]) if p is not None]
df = pd.DataFrame(rows, columns=["Date", "Close"]).set_index("Date")
df.to_csv(OUT / "TSLA_daily_close.csv", index_label="Date")
for n in (5,20,10,30): df[f"MA{n}"] = df.Close.rolling(n).mean()
def crossings(short, long):
    spread = df[f"MA{short}"] - df[f"MA{long}"]
    # Keep the moving-average warm-up period missing. A missing MA is not
    # equivalent to a negative spread and must not create an initial cross.
    signs = spread.apply(lambda x: float("nan") if pd.isna(x) else (1 if x>0 else (-1 if x<0 else 0)))
    return spread, signs.diff()
spread, cross = crossings(5,20)
df["signal"] = (spread > 0).astype("Int64")
df["trade"] = cross.where(cross.abs()>0,0)
buys, sells = df[df.trade>0], df[df.trade<0]
fig,axes=plt.subplots(2,1,figsize=(14,8),sharex=True,gridspec_kw={"height_ratios":[3,1]},dpi=170)
ax,pos=axes
ax.plot(df.index,df.Close,color="gray",alpha=.45,lw=1,label="Close")
ax.plot(df.index,df.MA5,color="tab:orange",lw=1.5,label="MA5")
ax.plot(df.index,df.MA20,color="tab:blue",lw=2,label="MA20")
ax.scatter(buys.index,buys.Close,marker="^",s=115,color="limegreen",edgecolors="darkgreen",zorder=6,label="Golden cross / Buy ▲")
ax.scatter(sells.index,sells.Close,marker="v",s=115,color="salmon",edgecolors="darkred",zorder=6,label="Death cross / Sell ▼")
ax.set_title("TSLA Dual Moving Average Signals · MA5 vs MA20 (2 years)")
ax.set_ylabel("Close (USD)"); ax.legend(loc="upper left",ncol=2); ax.grid(alpha=.25)
pos.fill_between(df.index,0,df.signal.fillna(0).astype(int),step="post",alpha=.35,color="steelblue")
pos.set_ylim(-.1,1.2); pos.set_yticks([0,1],["Flat (0)","Invested (1)"]); pos.set_ylabel("Position"); pos.set_xlabel("Date"); pos.grid(alpha=.25)
fig.tight_layout(); fig.savefig(OUT/"TSLA_MA5_MA20_signals.png",bbox_inches="tight")
with open(OUT/"signal_counts.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["MA pair","Golden crosses","Death crosses","Total signals"])
    for short,long in ((5,20),(10,30)):
        _,c=crossings(short,long); w.writerow([f"MA{short}/MA{long}",int((c>0).sum()),int((c<0).sum()),int((c.abs()>0).sum())])
print(f"{TICKER}: {len(df)} sessions, {df.index[0]} to {df.index[-1]}")
