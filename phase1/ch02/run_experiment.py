"""第二章：Meta 波动率与日收益率 Histogram 实验。"""
import datetime as dt
import json
import statistics
import urllib.request
from pathlib import Path
import matplotlib.pyplot as plt

TICKER = "META"  # 可替换为其他 Yahoo Finance 股票代码
PERIOD_DAYS = 370
OUT = Path(__file__).parent
end = int(dt.datetime.now(dt.timezone.utc).timestamp())
start = int((dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=PERIOD_DAYS)).timestamp())
url = f"https://query1.finance.yahoo.com/v8/finance/chart/{TICKER}?period1={start}&period2={end}&interval=1d&events=div%2Csplits"
request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
chart = json.load(urllib.request.urlopen(request, timeout=30))["chart"]["result"][0]
quote = chart["indicators"]["quote"][0]
adj = chart["indicators"].get("adjclose", [{}])[0].get("adjclose") or quote["close"]
prices = [float(price) for price in adj if price is not None]
returns = [prices[i] / prices[i - 1] - 1 for i in range(1, len(prices))]
mean, volatility = statistics.mean(returns), statistics.stdev(returns)
print(f"{TICKER}: {len(returns)} daily returns; mean={mean:.3%}; std={volatility:.3%}")
plt.figure(figsize=(9, 5), dpi=180)
plt.hist(returns, bins=35, color="#4263eb", edgecolor="white", alpha=.9)
plt.axvline(0, color="#222", linestyle="--", label="0%")
plt.axvline(mean, color="#f08c00", linewidth=2, label=f"Mean {mean:.2%}")
plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))
plt.title(f"{TICKER}: Daily Return Histogram\nAdjusted close · trailing one year")
plt.xlabel("Daily return"); plt.ylabel("Trading days"); plt.grid(axis="y", alpha=.2); plt.legend(); plt.tight_layout()
plt.savefig(OUT / f"{TICKER}_daily_return_histogram.png", bbox_inches="tight")
