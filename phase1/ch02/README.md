# 第二章通关：META、AAPL、TSLA 波动比较

## 统一区间的三票比较

使用 2025-11-10 至 2026-11-13 的三只股票调整收盘价，计算相邻收盘价日收益率，按样本标准差比较日波动。META、AAPL、TSLA 各有 254 个收益率观测。比较图见 [volatility_comparison.png](volatility_comparison.png)，精确数据见 [volatility_comparison.csv](volatility_comparison.csv)，对齐后的调整收盘价见 [common_period_adjusted_close.csv](common_period_adjusted_close.csv)。

META 的日收益率 Histogram 见 [META_daily_return_histogram.png](META_daily_return_histogram.png)。横轴是日收益率，纵轴是交易日频数。长尾表示样本中有少量极端涨跌观测；它提示尾部风险，不能据此保证未来走势。

## 计算口径与复现

日收益率为 `Close.pct_change()`，波动率为收益率的样本标准差（`std()`）。三票使用完全相同的日期区间。运行 [run_experiment.py](run_experiment.py) 可重新下载并生成三票比较图、Histogram 和 CSV；脚本同步保存最新结果文件。META 日波动率为 2.615%，低于 TSLA 的 2.880%，高于 AAPL 的 1.567%。
