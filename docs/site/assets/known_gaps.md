# 已知边界与限制

1. 数据源限制
- yfinance 字段命名与完整性在不同公司间差异较大。
- 某些字段可能需要手工覆盖（折旧、CapEx、ROU、Lease/Interest 等）。

2. 模型假设敏感性
- WACC、ROIC、增长率 `g` 对估值结果高度敏感。
- 不同口径（lecture / net）会导致 ROIC 与 FV 差异。

3. 课件对标与工程实用性
- 项目同时支持“strict course mode（课件优先）”和“heuristic mode（工程容错）”。
- 面向教学复现建议优先 strict 模式；面向实务快速筛选可用 heuristic 模式。

4. 非投资建议
- 本项目用于学习研究和方法演示，不构成投资建议。
