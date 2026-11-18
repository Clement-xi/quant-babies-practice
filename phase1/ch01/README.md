# 第一期第 1 章挑战：TSLA 真实行情

按挑战要求将标的从 AAPL 换成 TSLA，下载近六个月日线并绘制收盘价与成交量。

- 数据区间：2026-05-18 至 2026-11-17，共 128 个交易日。
- 最新收盘价：2026-11-17 为 **$380.11**。
- 六个月方向：首个收盘价为 $409.99，最新为 $380.11，按区间起止收盘价比较整体下跌约 **7.29%**。
- 图表：[TSLA 价格与成交量](TSLA_price_volume_6mo.png)；原始行情：[TSLA_6mo_ohlcv.csv](TSLA_6mo_ohlcv.csv)。
- 复现代码：[run_experiment.py](run_experiment.py)，运行 `python run_experiment.py` 可重新下载并生成数据与图。

行情来源为 Yahoo Finance。收盘价按原始收盘价展示，非分红调整价；历史区间结论只描述该样本。
