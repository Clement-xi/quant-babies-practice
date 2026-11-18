"""Download six months of TSLA prices and volume and save the challenge chart."""
import datetime as dt, json, urllib.request, csv
from pathlib import Path
import matplotlib.pyplot as plt
OUT=Path(__file__).parent; TICKER="TSLA"
url=f"https://query1.finance.yahoo.com/v8/finance/chart/{TICKER}?range=6mo&interval=1d&events=div%2Csplits"
req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}); obj=json.load(urllib.request.urlopen(req,timeout=30))["chart"]["result"][0]
q=obj["indicators"]["quote"][0]; rows=[(dt.datetime.fromtimestamp(t,dt.timezone.utc).date(),float(c),int(v)) for t,c,v in zip(obj["timestamp"],q["close"],q["volume"]) if c is not None and v is not None]
with open(OUT/"TSLA_6mo_ohlcv.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["Date","Close","Volume"]); w.writerows(rows)
fig,axes=plt.subplots(2,1,figsize=(12,6),sharex=True,gridspec_kw={"height_ratios":[3,1]},dpi=180)
axes[0].plot([x[0] for x in rows],[x[1] for x in rows],color="tab:blue",lw=1.5); axes[0].set_title("Tesla (TSLA): Closing Price and Volume · 6 months"); axes[0].set_ylabel("Close (USD)"); axes[0].grid(alpha=.25)
axes[1].bar([x[0] for x in rows],[x[2] for x in rows],width=.8,color="gray",alpha=.6); axes[1].set_ylabel("Volume"); axes[1].set_xlabel("Date"); axes[1].grid(alpha=.25); fig.tight_layout(); fig.savefig(OUT/"TSLA_price_volume_6mo.png",bbox_inches="tight")
print(f"Latest close: ${rows[-1][1]:.2f} on {rows[-1][0]}; first close: ${rows[0][1]:.2f} on {rows[0][0]}")
