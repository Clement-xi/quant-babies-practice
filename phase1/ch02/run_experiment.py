"""Chapter 2: compare META with AAPL and TSLA over one fixed common interval."""
import datetime as dt, json, urllib.request, csv
from pathlib import Path
import statistics
import matplotlib.pyplot as plt

TICKERS={"META":"Meta","AAPL":"Apple","TSLA":"Tesla"}
# Match the original META histogram interval so all three stocks are compared fairly.
START=dt.date(2025,11,10); END=dt.date(2026,11,13)
OUT=Path(__file__).parent; prices={}
for ticker in TICKERS:
    p1=int(dt.datetime.combine(START,dt.time(),dt.timezone.utc).timestamp())
    p2=int(dt.datetime.combine(END+dt.timedelta(days=1),dt.time(),dt.timezone.utc).timestamp())
    url=f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={p1}&period2={p2}&interval=1d&events=div%2Csplits"
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    obj=json.load(urllib.request.urlopen(req,timeout=30))["chart"]["result"][0]
    adj=obj["indicators"].get("adjclose",[{}])[0].get("adjclose") or obj["indicators"]["quote"][0]["close"]
    prices[ticker]=[(dt.datetime.fromtimestamp(ts,dt.timezone.utc).date(),float(x)) for ts,x in zip(obj["timestamp"],adj) if x is not None]
with open(OUT/"common_period_adjusted_close.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["Date",*TICKERS])
    maps={t:dict(prices[t]) for t in TICKERS}
    for day in sorted(set.intersection(*(set(m) for m in maps.values()))): w.writerow([day,*[maps[t][day] for t in TICKERS]])
returns={t:[prices[t][i][1]/prices[t][i-1][1]-1 for i in range(1,len(prices[t]))] for t in TICKERS}
vol={t:statistics.stdev(r) for t,r in returns.items()}
for t in TICKERS: print(f"{t} ({TICKERS[t]}): {len(returns[t])} returns; daily volatility={vol[t]:.3%}")
with open(OUT/"volatility_comparison.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["Ticker","Company","Return observations","Daily volatility (sample std)"]); [w.writerow([t,TICKERS[t],len(returns[t]),f"{vol[t]:.8f}"]) for t in TICKERS]
fig,ax=plt.subplots(figsize=(8,5),dpi=180); colors=["#4263eb","#007AFF","#E82127"]
ax.bar([TICKERS[t] for t in TICKERS],[vol[t]*100 for t in TICKERS],color=colors)
ax.set_title("Daily return volatility comparison · common one-year interval"); ax.set_ylabel("Daily return standard deviation (%)"); ax.grid(axis="y",alpha=.25); fig.tight_layout(); fig.savefig(OUT/"volatility_comparison.png",bbox_inches="tight"); fig.savefig(OUT/"META_volatility.png",bbox_inches="tight"); plt.close(fig)
r=returns["META"]; mean=statistics.mean(r)
fig,ax=plt.subplots(figsize=(9,5),dpi=180); ax.hist(r,bins=35,color="#4263eb",edgecolor="white",alpha=.9); ax.axvline(0,color="#222",ls="--",label="0%"); ax.axvline(mean,color="#f08c00",lw=2,label=f"Mean {mean:.2%}")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x,_:f"{x:.0%}")); ax.set_title("META daily return Histogram · 2025-11-10 to 2026-11-13"); ax.set_xlabel("Daily return"); ax.set_ylabel("Trading days"); ax.grid(axis="y",alpha=.2); ax.legend(); fig.tight_layout(); fig.savefig(OUT/"META_daily_return_histogram.png",bbox_inches="tight")
