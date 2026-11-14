# 第二章通关：Meta 波动对比

- **标的**：Meta Platforms（NASDAQ: META）
- **区间**：近一年日线，2025-11-10 至 2026-11-13
- **价格口径**：Yahoo Finance 调整收盘价；日收益率按相邻交易日收盘价百分比变化计算。
- **样本数**：254 个日收益率观测
- **平均日收益率**：0.041%
- **日收益率标准差（波动率）**：2.615%
- **Histogram**：见 [META_daily_return_histogram.png](META_daily_return_histogram.png)
- **波动对比图**：见 [META_volatility.png](META_volatility.png)

## 思考题：Histogram 尾巴很长说明什么？

长尾意味着极端涨跌出现的概率高于正态分布等薄尾模型的预期，日常波动之外仍可能发生大幅跳涨或跳跌。这类股票的收益分布具有较高尾部风险，常见于对消息、财报、监管或行业变化敏感、价格波动较大的公司。标准差只概括典型波动，不能单独描述尾部风险；评估时还应关注极端收益、偏度、峰度和最大回撤。历史分布不保证未来表现。

## 可复现方法

取 META 近一年 Yahoo Finance 日线调整收盘价，计算 `Close.pct_change().dropna()`；以样本标准差衡量日波动，以 35 个区间绘制收益率直方图。
