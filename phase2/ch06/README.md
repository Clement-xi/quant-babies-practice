# 第二期第 6 章挑战：Sharpe 与 Beta

## 计算区间与口径

教程中的 10 个标的（AAPL、MSFT、GOOGL、AMZN、META、NVDA、TSLA、AMD、JPM、SPY），近三年共同交易日区间为 2023-11-20 至 2026-11-17，共 750 个日收益观测。价格使用调整收盘价。年化收益按教程的日均收益复利外推 `(1 + mean_daily)^252 - 1`，年化波动率为样本标准差乘 √252，Sharpe = (年化收益 − 4% 无风险利率) / 年化波动率。

## Sharpe 前三名

1. **AMD：1.47**
2. **JPM：1.36**
3. **NVDA：1.25**

十标的排序图见 [sharpe_ranking.png](sharpe_ranking.png)，全量指标及 Beta 见 [sharpe_beta_results.csv](sharpe_beta_results.csv)。

## JPM 与 NVDA 的 Beta

相对 SPY 的 Beta：JPM **0.87**，NVDA **2.03**。JPM 更接近 1，因此本样本内它的日收益对大盘变动更接近一比一；NVDA 的历史敏感度更高。Beta 是历史线性关系的估计，不代表未来固定不变。

## 思考：Sharpe 高是否代表未来一定更好？

不代表。Sharpe 是基于历史收益和波动的风险调整指标，受样本区间、极端行情和参数选择影响；未来市场状态可能改变，交易成本和执行误差也会降低实际结果。高 Sharpe 只能说明所选历史样本中的风险收益比更高，不能保证未来表现。

原始调整收盘价快照见 [adjusted_close_3y.csv](adjusted_close_3y.csv)，可据此复核计算。
