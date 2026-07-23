# WMT 样例过程说明（2026-03-31）

## 1) 数据输入
- 标的：`WMT`（US）
- 数据源：`yfinance`
- 报表年份：T（最新财年）

## 2) 计算流程
1. 拉取公司信息、市场数据、三大报表
2. 数据标准化（字段映射、符号修正、缺失容错）
3. 计算 AV（资产重估）
4. 计算 EPV（平滑利润 + 调整项 + WACC）
5. 计算 FV（ROIC、g、WACC）并得到总估值

## 3) 本次课件对标设置
- 平滑利润：3 年 simple
- Growth expense：Method2（营收 × 0.35%）
- FV：strict course mode = ON
- ROIC（展示）：lecture 与 net 两口径同时展示

## 4) 样例结果摘要（见 sample_results.json）
- Market Cap: 987.42B
- AV: 176.77B
- EPV（FV 基准口径）: 427.92B
- FV: 284.01B
- Total Value: 711.93B
- WACC: 8.13%
- ROIC(lecture): 10.17%
- ROIC(net): 13.34%

## 5) 一致性检查
- EPV + FV 与 Total Value（四舍五入）一致
- ROIC-WACC spread 为正，FV 应为正

## 6) 说明
- 结果受市场数据日期、无风险利率与报表更新影响，会随时间变化。
