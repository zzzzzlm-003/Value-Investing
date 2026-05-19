# Deere & Company – Homework 1 | Value Investing MBA Spring 2026

## 文件结构

```
Assignment/
├── 我的初步思考-Q1.md       # 主报告（完整答案）
├── Homework 1_ Deere.pdf     # 作业要求
├── Homework-Data-2026.xlsx   # 课程数据（勿删）
├── Deere-Homework-Output.xlsx # 汇总输出（所有 sheet）
├── Deere Company NYSE DE Financials.xls
├── images/                   # 图表
│   ├── industry_revenue_shares.png
│   ├── industry_revenue_shares_farm_only.png
│   ├── demand_deere_combined.png
│   └── ...
├── scripts/
│   ├── run_all.py            # 一键运行
│   ├── q2_industry_revenue_shares.py  # Q2 竞品份额
│   ├── q3_demand_variables.py         # Q3 需求变量 (需 FRED)
│   ├── q5_tariff_reaction_calc.py     # Q5 关税股价
│   ├── epv_calculation.py             # Q6/Q7 EPV
│   ├── build_balance_sheet_comparison.py # 直接写入 Output 的 BS_* sheet
│   └── ...
└── requirements.txt
```

## 运行方式

```bash
pip install -r requirements.txt

# 一键运行（Q2, Q5, BS, EPV；Q3 需 FRED）
python scripts/run_all.py

# 或单独运行
python scripts/q2_industry_revenue_shares.py
python scripts/q5_tariff_reaction_calc.py
```

**Q3 需求变量**：需 `FRED_API_KEY`，见 https://fred.stlouisfed.org/docs/api/api_key.html  
`export FRED_API_KEY=xxx` 后运行 `python scripts/q3_demand_variables.py`

## Deere-Homework-Output.xlsx 的 Sheet 说明

| Sheet | 内容 |
|-------|------|
| Revenue_Shares_Total | Q2 总营收份额 |
| Revenue_Shares_Farm | Q2 纯 Farm 份额 |
| Demand_Variables | Q3 需求变量 (FRED) |
| Q5_Tariff_Reaction | Q5 关税股价反应 |
| Q5_Quarterly_Rev | Q5 季度收入 |
| BS_* | 资产负债表对比 |
| Seg_* | 分板块 Margin |
| EPV_Summary | EPV 结果 |

## 导出 PDF

从 `我的初步思考-Q1.md` 导出 PDF：VS Code Markdown PDF 扩展 / pandoc / 浏览器打印。
