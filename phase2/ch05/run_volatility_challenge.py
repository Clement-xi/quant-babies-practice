"""Chapter 5 volatility challenge: annualized vol and MSFT return histogram."""
import datetime as dt, json, math, urllib.request, csv, statistics
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
OUT=Path(__file__).parent; TICKERS=["AMD","AAPL","TSLA","NVDA","MSFT","META","NFLX","COIN"]; DAYS=252
names={"AMD":"Advanced Micro Devices","AAPL":"Apple","TSLA":"Tesla","NVDA":"NVIDIA","MSFT":"Microsoft","META":"Meta Platforms","NFLX":"Netflix","COIN":"Coinbase"}
prices={}
for ticker in TICKERS:
    url=f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1y&interval=1d&events=div%2Csplits"
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    obj=json.load(urllib.request.urlopen(req,timeout=30))["chart"]["result"][0]
    values=obj["indicators"].get("adjclose",[{}])[0].get("adjclose") or obj["indicators"]["quote"][0]["close"]
    prices[ticker]=[float(x) for x in values if x is not None]
returns={t:[prices[t][i]/prices[t][i-1]-1 for i in range(1,len(prices[t]))] for t in TICKERS}
vol={t:statistics.stdev(r)*math.sqrt(DAYS) for t,r in returns.items()}
with open(OUT/"annualized_volatility.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["Ticker","Company","Observations","Annualized volatility"])
    for t,v in sorted(vol.items(),key=lambda x:-x[1]): w.writerow([t,names[t],len(returns[t]),f"{v:.8f}"])
fig,ax=plt.subplots(figsize=(9,5),dpi=180)
for t,c in zip(["AAPL","TSLA","NVDA","MSFT"],["#007AFF","#E82127","#76B900","#00A4EF"]): ax.bar(t,vol[t]*100,color=c)
ax.set_title("Annualized volatility comparison · trailing 1 year"); ax.set_ylabel("Annualized volatility (%)"); ax.grid(axis="y",alpha=.25); fig.tight_layout(); fig.savefig(OUT/"four_stock_volatility.png",bbox_inches="tight")
x=np.array(returns["MSFT"])*100; mu=x.mean(); sd=x.std(ddof=1)
fig,ax=plt.subplots(figsize=(8,5),dpi=180); ax.hist(x,bins=30,color="#00A4EF",alpha=.78,edgecolor="white",density=True,label="Observed daily returns")
xx=np.linspace(x.min(),x.max(),300); ax.plot(xx,np.exp(-.5*((xx-mu)/sd)**2)/(sd*np.sqrt(2*np.pi)),color="#e67700",lw=2,label=f"Normal fit (mean={mu:.3f}%, sd={sd:.3f}%)")
ax.axvline(0,color="black",ls="--",lw=.8); ax.set_title("MSFT daily return distribution · trailing 1 year"); ax.set_xlabel("Daily return (%)"); ax.set_ylabel("Density"); ax.legend(); ax.grid(alpha=.2); fig.tight_layout(); fig.savefig(OUT/"MSFT_return_histogram.png",bbox_inches="tight")
print("Top volatility:",max(vol,key=vol.get),f"{max(vol.values()):.2%}")
