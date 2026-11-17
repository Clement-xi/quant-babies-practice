# Quant for Babies 学习练习

本仓库记录《Quant for Babies》量化投资课程的章节挑战、Python 实验代码、结果图表与学习笔记。每一章都提供介绍、复现脚本和对应成果链接，方便按章节查看与运行。

- 教程仓库：[ThreshoLdnnis/Quant-for-babies](https://github.com/ThreshoLdnnis/Quant-for-babies)
- 本仓库：[Clement-xi/quant-babies-practice](https://github.com/Clement-xi/quant-babies-practice)

## 作业导航

### 第一期：量化入门

| 章节 | 内容 | 作业介绍 | 代码 | 图表与数据 |
|---|---|---|---|---|
| 第 2 章 | 收益率与波动对比（Meta） | [作业说明](phase1/ch02/README.md) | [实验脚本](phase1/ch02/run_experiment.py) | [收益率 Histogram](phase1/ch02/META_daily_return_histogram.png) · [三票波动率比较](phase1/ch02/volatility_comparison.png) · [统一区间价格快照](phase1/ch02/common_period_adjusted_close.csv) |
| 第 3 章 | TSLA 双均线策略信号 | [作业说明](phase1/ch03/README.md) | [实验脚本](phase1/ch03/run_experiment.py) | [金叉/死叉信号图](phase1/ch03/TSLA_MA5_MA20_signals.png) · [信号次数表](phase1/ch03/signal_counts.csv) · [原始收盘价快照](phase1/ch03/TSLA_daily_close.csv) |
| 第 4 章 | NVDA 策略回测 | [作业说明](phase1/ch04/README.md) | [回测脚本](phase1/ch04/run_backtest.py) | [策略与大盘净值图](phase1/ch04/NVDA_5y_strategy_vs_market.png) · [回撤对比数据](phase1/ch04/drawdown_comparison.csv) |

### 第二期：风险与组合

| 章节 | 内容 | 作业介绍 | 代码 | 图表与数据 |
|---|---|---|---|---|
| 第 5 章 | 年化波动率与收益分布 | [作业说明](phase2/ch05/README.md) | [挑战脚本](phase2/ch05/run_volatility_challenge.py) | [四只股票波动率比较](phase2/ch05/four_stock_volatility.png) · [MSFT 收益率 Histogram](phase2/ch05/MSFT_return_histogram.png) · [八只股票波动率排名](phase2/ch05/annualized_volatility.csv) |

## 如何复现实验

脚本使用 Python 运行，并从 Yahoo Finance 获取近期行情数据，因此需要可访问网络。常用依赖为 `pandas`、`numpy` 和 `matplotlib`；运行每章说明页链接的脚本即可重新计算并生成图表/数据表。例如：

```bash
python phase1/ch02/run_experiment.py
python phase1/ch03/run_experiment.py
python phase1/ch04/run_backtest.py
python phase2/ch05/run_volatility_challenge.py
```

每章的作业说明页包含该章数据区间、计算口径、主要结果和思考题结论。历史数据结果会随运行时间与数据源更新而变化；图表和统计结果仅用于学习，不代表未来表现。

## 目录结构

```text
phase1/
  ch02/  收益率与波动对比
  ch03/  双均线策略信号
  ch04/  策略回测
phase2/
  ch05/  波动率与收益分布
```
