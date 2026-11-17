"""Chapter 4 challenge: NVDA MA5/MA20 backtest versus SPY."""
import datetime as dt, json, urllib.request, csv
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

OUT=Path(__file__).parent
def download(ticker):
    url=f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=5y&interval=1d&events=div%2Csplits"
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    obj=json.load(urllib.request.urlopen(req,timeout=30))["chart"]["result"][0]
    q=obj["indicators"]["quote"][0]
    prices=obj["indicators"].get("adjclose",[{}])[0].get("adjclose") or q["close"]
    rows=[(pd.to_datetime(t,unit="s",utc=True).date(),float(p)) for t,p in zip(obj["timestamp"],prices) if p is not None]
    return pd.Series([p for _,p in rows],index=[d for d,_ in rows],name=ticker)
prices=pd.concat([download("NVDA"),download("SPY")],axis=1).dropna()
results=[]
for period,n in (("1y",253),("5y",1260)):
    df=prices.tail(n).copy(); df["MA5"]=df.NVDA.rolling(5).mean(); df["MA20"]=df.NVDA.rolling(20).mean()
    df["signal"]=(df.MA5>df.MA20).astype(int); df["position"]=df.signal.shift(1).fillna(0)
    df["ret"]=df.NVDA.pct_change().fillna(0); df["strategy_ret"]=df.position*df.ret; df["spy_ret"]=df.SPY.pct_change().fillna(0)
    df["nav_strategy"]=(1+df.strategy_ret).cumprod(); df["nav_nvda"]=(1+df.ret).cumprod(); df["nav_spy"]=(1+df.spy_ret).cumprod()
    mdd_strategy=(df.nav_strategy/df.nav_strategy.cummax()-1).min(); mdd_nvda=(df.nav_nvda/df.nav_nvda.cummax()-1).min()
    results.append((period,df,mdd_strategy,mdd_nvda))
_,df,_,_=results[-1]
fig,ax=plt.subplots(figsize=(12,6),dpi=180)
ax.plot(df.index,df.nav_strategy,lw=2.2,color="tab:purple",label="MA5/MA20 Strategy (NVDA)")
ax.plot(df.index,df.nav_nvda,lw=1.7,color="tab:blue",label="Buy & Hold (NVDA)")
ax.plot(df.index,df.nav_spy,lw=1.7,color="gray",ls="--",label="Buy & Hold (SPY benchmark)")
ax.axhline(1,color="black",lw=.6,ls=":"); ax.set_title("NVDA Backtest NAV: Strategy vs Stock vs S&P 500 ETF (5 years)")
ax.set_xlabel("Date"); ax.set_ylabel("NAV (start = 1)"); ax.legend(); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(OUT/"NVDA_5y_strategy_vs_market.png",bbox_inches="tight")
with open(OUT/"drawdown_comparison.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["Period","Trading days","Start","End","Strategy return","NVDA buy-hold return","SPY return","Strategy max drawdown","NVDA max drawdown"])
    for period,d,ms,mn in results: w.writerow([period,len(d),d.index[0],d.index[-1],d.nav_strategy.iloc[-1]-1,d.nav_nvda.iloc[-1]-1,d.nav_spy.iloc[-1]-1,ms,mn])
