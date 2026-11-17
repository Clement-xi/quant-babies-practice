# 第二期第 5 章挑战：波动率进阶

完成教程的四级挑战：用 AMD 作为额外标的计算年化波动率；在 AAPL/TSLA/NVDA 三票中加入 MSFT；绘制 MSFT 日收益率 Histogram（叠加正态拟合）；在教程给定的 8 只候选股中找近一年年化波动率最高者。

## 口径与结果

使用 Yahoo Finance 最近一年调整收盘价，计算日简单收益率，年化波动率 = 日收益率样本标准差 × √252。每只股票有 250 个日收益观测。截止 2026-11-17 的数据：AMD 年化波动率 **73.75%**；四票比较中 MSFT 为 **34.03%**；八只股票中 AMD 最高（73.75%），其次 Coinbase（72.13%）。完整排序见 [annualized_volatility.csv](annualized_volatility.csv)，四票对比见 [four_stock_volatility.png](four_stock_volatility.png)，MSFT 分布图见 [MSFT_return_histogram.png](MSFT_return_histogram.png)。

波动率排名只反映所选的一年历史区间，不代表未来风险排序；正态拟合仅作分布参照，真实收益可能有偏度和厚尾。

## 复现

运行 `python run_volatility_challenge.py`（需 numpy、matplotlib 和网络连接），会重算近一年数据并生成图表及 CSV。
