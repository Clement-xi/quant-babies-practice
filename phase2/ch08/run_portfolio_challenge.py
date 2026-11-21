"""Chapter 8 portfolio challenge: correlation, diversification, and benchmarks."""
import datetime as dt,json,urllib.request,csv,math,time
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
OUT=Path(__file__).parent; SYMBOLS=["TSLA","NVDA","KO","SPY","AAPL","MSFT","JPM","XLE"]; TRADING_DAYS=252
prices={}
for ticker in SYMBOLS:
    url=f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=5y&interval=1d&events=div%2Csplits"
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    for attempt in range(5):
        try:
            obj=json.load(urllib.request.urlopen(req,timeout=30))["chart"]["result"][0]; break
        except Exception:
            if attempt==4: raise
            time.sleep(2*(attempt+1))
    vals=obj["indicators"].get("adjclose",[{}])[0].get("adjclose") or obj["indicators"]["quote"][0]["close"]
    pairs=[(dt.datetime.fromtimestamp(t,dt.timezone.utc).date(),float(v)) for t,v in zip(obj["timestamp"],vals) if v is not None]
    prices[ticker]=pd.Series([v for _,v in pairs],index=pd.to_datetime([d for d,_ in pairs]),name=ticker)
price=pd.concat(prices.values(),axis=1).dropna(); returns=price.pct_change().dropna()
price.to_csv(OUT/"adjusted_close_common_5y.csv",index_label="Date")
# Core changed ticker selection + period sensitivity
core=["TSLA","NVDA","KO","SPY"]; corr3=returns[core].tail(756).corr(); corr1=returns[core].tail(252).corr()
corr3.to_csv(OUT/"correlation_3y.csv"); corr1.to_csv(OUT/"correlation_1y.csv")
fig,axs=plt.subplots(1,2,figsize=(11,4.8),dpi=180)
for ax,corr,title in [(axs[0],corr3,"3 years"),(axs[1],corr1,"1 year")]:
    im=ax.imshow(corr.values,vmin=-1,vmax=1,cmap="RdYlBu_r"); ax.set_xticks(range(len(core)),core,rotation=30); ax.set_yticks(range(len(core)),core); ax.set_title(title)
    for i in range(len(core)):
        for j in range(len(core)):ax.text(j,i,f"{corr.iloc[i,j]:.2f}",ha="center",va="center",fontsize=9)
fig.colorbar(im,ax=axs.ravel().tolist(),shrink=.82,label="Pearson correlation");fig.suptitle("TSLA, NVDA, KO and SPY · return correlation");fig.savefig(OUT/"correlation_heatmaps.png",bbox_inches="tight");plt.close(fig)
core_vol=returns[core].tail(756).std()*np.sqrt(TRADING_DAYS); core_port=returns[core[:3]].tail(756).mean(axis=1); core_vol.loc["Equal-weight 3-stock"] = core_port.std()*np.sqrt(TRADING_DAYS)
fig,ax=plt.subplots(figsize=(8.5,4.8),dpi=180);ax.bar(core_vol.index,core_vol.values*100,color=["#ef4444","#76b900","#1f9d55","#f59f00","#4263eb"]);ax.set_ylabel("Annualized volatility (%)");ax.set_title("Volatility · 3-year sample");ax.grid(axis="y",alpha=.25);fig.tight_layout();fig.savefig(OUT/"volatility_comparison.png",bbox_inches="tight");plt.close(fig)
nav_core=(1+core_port).cumprod();nav_spy=(1+returns["SPY"].tail(756)).cumprod();nav_core.to_csv(OUT/"core_portfolio_nav.csv",header=["NAV"]);nav_spy.to_csv(OUT/"spy_nav.csv",header=["NAV"])
fig,ax=plt.subplots(figsize=(10,5),dpi=180);ax.plot(nav_core.index,nav_core,label="Equal weight TSLA/NVDA/KO",color="#4263eb");ax.plot(nav_spy.index,nav_spy,label="SPY buy & hold",ls="--",color="#f59f00");ax.set_title("Three-stock equal-weight portfolio vs SPY · 3 years");ax.set_ylabel("NAV (start = 1)");ax.grid(alpha=.25);ax.legend();fig.tight_layout();fig.savefig(OUT/"portfolio_vs_spy.png",bbox_inches="tight");plt.close(fig)
# Lowest pair of the core correlation matrix, excluding diagonal
low=corr3.where(~np.eye(len(core),dtype=bool)).stack().sort_values();low_pair=low.index[0];high=corr3.where(~np.eye(len(core),dtype=bool)).stack().sort_values(ascending=False).index[0]
# Original tutorial portfolio exercises, same common 3y sample
base=returns.tail(756); four=["AAPL","MSFT","JPM","XLE"]; three=["AAPL","JPM","XLE"]
vols=base.std()*np.sqrt(TRADING_DAYS); p4=base[four].mean(axis=1); p3=base[three].mean(axis=1); ptech=.5*base.AAPL+.5*base.MSFT
manual_var=(.5**2*vols.AAPL**2+.5**2*vols.MSFT**2+2*.5*.5*vols.AAPL*vols.MSFT*base.AAPL.corr(base.MSFT))
# Exact covariance quadratic form with annualized covariance; the expression above algebraically equals it.
cov_ann=base[["AAPL","MSFT"]].cov()*TRADING_DAYS; manual_matrix=float(np.array([.5,.5])@cov_ann.values@np.array([.5,.5])); actual=float(ptech.std()*np.sqrt(TRADING_DAYS))
roll=base.AAPL.rolling(60).corr(base.MSFT);roll.to_csv(OUT/"rolling_corr_60d.csv",header=["Correlation"]);fig,ax=plt.subplots(figsize=(10,4.8),dpi=180);ax.plot(roll.index,roll,color="#7c3aed",lw=1.2);ax.axhline(base.AAPL.corr(base.MSFT),color="gray",ls="--",label=f"Full-period corr {base.AAPL.corr(base.MSFT):.2f}");ax.set_ylim(-1,1);ax.set_title("AAPL/MSFT 60-trading-day rolling correlation");ax.set_ylabel("Correlation");ax.grid(alpha=.25);ax.legend();fig.tight_layout();fig.savefig(OUT/"rolling_correlation_AAPL_MSFT.png",bbox_inches="tight");plt.close(fig)
nav4=(1+p4).cumprod();spy= (1+base.SPY).cumprod();volp4=float(p4.std()*np.sqrt(TRADING_DAYS));volp3=float(p3.std()*np.sqrt(TRADING_DAYS));voltech=float(ptech.std()*np.sqrt(TRADING_DAYS));avg=float(vols[four].mean());volsingle=float(vols.AAPL)
summary={"sample_start":str(base.index[0].date()),"sample_end":str(base.index[-1].date()),"observations":len(base),"core_lowest_pair":f"{low_pair[0]}-{low_pair[1]}","core_lowest_corr":float(low.iloc[0]),"core_highest_pair":f"{high[0]}-{high[1]}","core_highest_corr":float(corr3.loc[high]),"AAPL_MSFT_corr_3y":float(base.AAPL.corr(base.MSFT)),"AAPL_MSFT_corr_1y":float(returns.tail(252).AAPL.corr(returns.tail(252).MSFT)),"AAPL_MSFT_50_50_vol":voltech,"four_stock_equal_vol":volp4,"three_stock_equal_vol":volp3,"four_stock_single_vol_average":avg,"AAPL_vol":volsingle,"manual_two_stock_vol":math.sqrt(manual_matrix),"calculated_two_stock_vol":actual,"portfolio_final_nav":float(nav4.iloc[-1]),"SPY_final_nav":float(spy.iloc[-1]),"cumulative_nav_difference":float(nav4.iloc[-1]-spy.iloc[-1]),"portfolio_vol":volp4,"SPY_vol":float(base.SPY.std()*np.sqrt(TRADING_DAYS)),"rolling_corr_min":float(roll.min()),"rolling_corr_max":float(roll.max())}
with open(OUT/"challenge_metrics.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f);w.writerow(["Metric","Value"]);w.writerows(summary.items())
print(summary)
