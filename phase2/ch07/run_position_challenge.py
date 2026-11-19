"""Chapter 7: AAPL MA10/30 drawdown and 30% position challenge."""
import datetime as dt,json,urllib.request,csv
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
OUT=Path(__file__).parent; TICKER="AAPL"
url=f"https://query1.finance.yahoo.com/v8/finance/chart/{TICKER}?range=3y&interval=1d&events=div%2Csplits";req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"});obj=json.load(urllib.request.urlopen(req,timeout=30))["chart"]["result"][0]
q=obj["indicators"]["quote"][0];adj=obj["indicators"].get("adjclose",[{}])[0].get("adjclose") or q["close"];rows=[(dt.datetime.fromtimestamp(t,dt.timezone.utc).date(),float(v)) for t,v in zip(obj["timestamp"],adj) if v is not None]
with open(OUT/"AAPL_3y_adjusted_close.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f);w.writerow(["Date","Adjusted Close"]);w.writerows(rows)
prices=pd.Series([v for _,v in rows],index=pd.to_datetime([d for d,_ in rows]));ret=prices.pct_change();d=pd.DataFrame({"Close":prices,"Return":ret});d["MA10"]=d.Close.rolling(10).mean();d["MA30"]=d.Close.rolling(30).mean();d["Signal"]=(d.MA10>d.MA30).astype(float);d["StrategyReturn"]=d.Signal.shift(1)*d.Return;d=d.dropna()
d["Equity100"]=(1+d.StrategyReturn).cumprod();d["Equity30"]=(1+d.StrategyReturn*.3).cumprod();d["BuyHold"]=(1+d.Return).cumprod()
def drawdown(e):return e/e.cummax()-1
results=[]
for label,col in [("MA10/30 100%","Equity100"),("MA10/30 30%","Equity30"),("Buy and hold","BuyHold")]:
    dd=drawdown(d[col]);trough=dd.idxmin();idx=d.index.get_loc(trough);peak=d[col].cummax().loc[trough];next60=d[col].iloc[idx+1:idx+61];recovery=next60[next60>=peak]
    results.append([label,float(dd.min()),trough.date(),"Yes" if len(recovery) else "No",recovery.index[0].date() if len(recovery) else ""])
with open(OUT/"drawdown_recovery.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f);w.writerow(["Scenario","Max drawdown","Trough date","Recovered within next 60 sessions","Recovery date"]);w.writerows(results)
fig,ax=plt.subplots(figsize=(11,5.5),dpi=180)
for col,label,color in [("Equity100","MA10/30 · 100%","#1c7ed6"),("Equity30","MA10/30 · 30%","#2f9e44"),("BuyHold","AAPL buy & hold","#868e96")]:ax.plot(d.index,d[col],label=label,color=color,lw=1.8)
ax.set_title("AAPL · MA10/30 position sizing comparison · 3 years");ax.set_ylabel("Equity (start = 1)");ax.set_xlabel("Date");ax.grid(alpha=.25);ax.legend();fig.tight_layout();fig.savefig(OUT/"AAPL_MA10_30_equity.png",bbox_inches="tight");plt.close(fig)
fig,ax=plt.subplots(figsize=(11,4.5),dpi=180)
for col,label,color in [("Equity100","100%","#1c7ed6"),("Equity30","30%","#2f9e44")]:ax.plot(d.index,drawdown(d[col])*100,label=label,color=color,lw=1.5)
ax.axhline(-15,color="#e03131",ls="--",label="−15% drawdown limit");ax.set_title("AAPL MA10/30 · Underwater curves");ax.set_ylabel("Drawdown (%)");ax.set_xlabel("Date");ax.grid(alpha=.25);ax.legend();fig.tight_layout();fig.savefig(OUT/"AAPL_MA10_30_underwater.png",bbox_inches="tight");plt.close(fig)
