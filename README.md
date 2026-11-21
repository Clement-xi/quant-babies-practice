# Quant for Babies 学习练习

本仓库记录《Quant for Babies》量化投资课程的章节挑战、Python 实验代码、结果图表与学习笔记。每一章都提供介绍、复现脚本和对应成果链接，方便按章节查看与运行。

- 教程仓库：[ThreshoLdnnis/Quant-for-babies](https://github.com/ThreshoLdnnis/Quant-for-babies)
- 本仓库：[Clement-xi/quant-babies-practice](https://github.com/Clement-xi/quant-babies-practice)

## 作业导航

### 第一期：量化入门

| 章节 | 内容 | 作业介绍 | 代码 | 图表与数据 |
|---|---|---|---|---|
| 第 1 章 | TSLA 真实行情体验 | [作业说明](phase1/ch01/README.md) | [实验脚本](phase1/ch01/run_experiment.py) | [价格与成交量图](phase1/ch01/TSLA_price_volume_6mo.png) · [六个月行情快照](phase1/ch01/TSLA_6mo_ohlcv.csv) |
| 第 2 章 | 收益率与波动对比（Meta） | [作业说明](phase1/ch02/README.md) | [实验脚本](phase1/ch02/run_experiment.py) | [收益率 Histogram](phase1/ch02/META_daily_return_histogram.png) · [三票波动率比较](phase1/ch02/volatility_comparison.png) · [统一区间价格快照](phase1/ch02/common_period_adjusted_close.csv) |
| 第 3 章 | TSLA 双均线策略信号 | [作业说明](phase1/ch03/README.md) | [实验脚本](phase1/ch03/run_experiment.py) | [金叉/死叉信号图](phase1/ch03/TSLA_MA5_MA20_signals.png) · [信号次数表](phase1/ch03/signal_counts.csv) · [原始收盘价快照](phase1/ch03/TSLA_daily_close.csv) |
| 第 4 章 | NVDA 策略回测 | [作业说明](phase1/ch04/README.md) | [回测脚本](phase1/ch04/run_backtest.py) | [策略与大盘净值图](phase1/ch04/NVDA_5y_strategy_vs_market.png) · [回撤对比数据](phase1/ch04/drawdown_comparison.csv) |

### 第二期：风险与组合

| 章节 | 内容 | 作业介绍 | 代码 | 图表与数据 |
|---|---|---|---|---|
| 第 5 章 | 年化波动率与收益分布 | [作业说明](phase2/ch05/README.md) | [挑战脚本](phase2/ch05/run_volatility_challenge.py) | [四只股票波动率比较](phase2/ch05/four_stock_volatility.png) · [MSFT 收益率 Histogram](phase2/ch05/MSFT_return_histogram.png) · [八只股票波动率排名](phase2/ch05/annualized_volatility.csv) |
| 第 6 章 | Sharpe 与 Beta | [作业说明](phase2/ch06/README.md) | — | [Sharpe 排名图](phase2/ch06/sharpe_ranking.png) · [十标的指标与 Beta](phase2/ch06/sharpe_beta_results.csv) · [三年价格快照](phase2/ch06/adjusted_close_3y.csv) |
| 第 7 章 | 最大回撤与仓位管理 | [作业说明](phase2/ch07/README.md) | [挑战脚本](phase2/ch07/run_position_challenge.py) | [仓位净值比较](phase2/ch07/AAPL_MA10_30_equity.png) · [水下曲线](phase2/ch07/AAPL_MA10_30_underwater.png) · [回撤与恢复数据](phase2/ch07/drawdown_recovery.csv) · [AAPL 行情快照](phase2/ch07/AAPL_3y_adjusted_close.csv) |
| 第 8 章 | 多标的组合与相关性 | [作业说明](phase2/ch08/README.md) | [挑战脚本](phase2/ch08/run_portfolio_challenge.py) | [相关性热力图](phase2/ch08/correlation_heatmaps.png) · [波动对比图](phase2/ch08/volatility_comparison.png) · [组合与 SPY 净值](phase2/ch08/portfolio_vs_spy.png) · [统计汇总](phase2/ch08/challenge_metrics.csv) · [五年价格快照](phase2/ch08/adjusted_close_common_5y.csv) |

## 如何复现实验

脚本使用 Python 运行，并从 Yahoo Finance 获取近期行情数据，因此需要可访问网络。常用依赖为 `pandas`、`numpy` 和 `matplotlib`；运行每章说明页链接的脚本即可重新计算并生成图表/数据表。例如：

```bash
python phase1/ch01/run_experiment.py
python phase1/ch02/run_experiment.py
python phase1/ch03/run_experiment.py
python phase1/ch04/run_backtest.py
python phase2/ch05/run_volatility_challenge.py
python phase2/ch07/run_position_challenge.py
python phase2/ch08/run_portfolio_challenge.py
```

每章的作业说明页包含该章数据区间、计算口径、主要结果和思考题结论。历史数据结果会随运行时间与数据源更新而变化；图表和统计结果仅用于学习，不代表未来表现。

## 目录结构

```text
phase1/
  ch01/  真实股票价格与成交量
  ch02/  收益率与波动对比
  ch03/  双均线策略信号
  ch04/  策略回测
phase2/
  ch05/  波动率与收益分布
  ch06/  Sharpe 与 Beta
  ch07/  最大回撤与仓位管理
  ch08/  多标的组合与相关性
```
