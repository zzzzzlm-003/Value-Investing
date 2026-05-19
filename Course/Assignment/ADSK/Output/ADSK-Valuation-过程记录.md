# ADSK Valuation 过程记录

**作业**：ADSK-Final-2026 (Valuation Q5–Q7)  
**方法论参考**：Transcript S11/S12、Lecture-8 Adobe 笔记、Adobe 作业脚本

---

## 数据来源总表

| 数据项 | 来源文件 | 具体位置 | 备注 |
|--------|----------|----------|------|
| R&D、Marketing、Op. Income、Revenues、Debt、Cash、Share repurchases | ADSK-Data-February-2026-Students.xlsx | Basic data 表，第2行表头，第3–12行年度 2017–2026，列 C–J | 课程提供 consolidated 表 |
| Subscriptions (百万) | 同上 | Basic data 表，第15行表头，第16–25行，列 E | 对应 10-K Item 7 MD&A 的订阅/付费用户口径 |
| Shares outstanding、Stock price | 同上 | Basic data 第16–25行，列 C、D | 股数可对照 10-K 验证 |
| Churn rate 5%、Tax rate 21% | 同上 | Basic data 第3行，列 L–M (Parameters) | 作业指定 |
| Book Equity | ADSK-Data-February-2026-Students.xlsx | Balance Sheet 表 | 见下 |
| 详细利润表/资产负债/现金流 | 同上 | Income Statement、Balance Sheet、Cash Flow statement | FactSet 数据 |
| 股数、市值口径 | Form 10-K (ADSK_2025_Annual_Report.pdf) | Part I 封面附近、Item 5 | 见下 |

### 年报 (Form 10-K) 引用

| 数据 | 年报位置 | 原文/摘要 |
|------|----------|-----------|
| 股数 (213 million) | **Page 1**, "As of July 31, 2025..." | "there were approximately 213 million shares of the registrant's common stock outstanding that were held by non-affiliates" |
| 股数 (211 million, 2026年2月) | **Page 2** (Table of Contents 后) | "As of February 23, 2026, the registrant had outstanding 211 million shares of common stock" |
| 市值约 $64.5B | **Page 1** | "aggregate market value ... was approximately $64.5 billion" (基于 2025年7月31日股价) |
|  subscription 定义 | **Part I Item 1** (Business), Glossary | "Subscription Plan: Comprises our term-based product subscriptions, cloud service offerings, and EBAs" |
| 经营与订阅相关描述 | **Part II Item 7** (MD&A), 约 p.41 起 | "operational and key metrics and subscriptions"; 订阅数通常在此或投资者材料中披露 |
| 财务数据 (GAAP) | **Part II Item 8** (Financial Statements), 约 p.65 起 | 合并财报 |

> **说明**：Basic data 中的 Subscriptions (百万人) 为课程整理的 consolidated 数据，通常对应 10-K Item 7 (MD&A) 中的 "key metrics" 或投资者演示中的付费订阅口径。年报正文未给出逐年 7.79、7.53 等精确序列，课程 Excel 已整理完毕，本估值以该表为准。

---

## Q5 Asset Value

### 5.1 产品组合 (Product Portfolio)

**公式**（永久库存法，d=0.2）：
$$P_{prod} = R\&D_{2026} + 0.8 R\&D_{2025} + 0.6 R\&D_{2024} + 0.4 R\&D_{2023} + 0.2 R\&D_{2022}$$

**数据来源**：Basic data 列 C (R&D)，行 8–12 对应 2022–2026。

| 年份 | R&D ($mn) |
|------|-----------|
| 2022 | 1,113.6 |
| 2023 | 1,214 |
| 2024 | 1,372 |
| 2025 | 1,485 |
| 2026 | 1,643 |

**计算**：1,643 + 0.8×1,485 + 0.6×1,372 + 0.4×1,214 + 0.2×1,113.6 = **$4,363 mn**

---

### 5.2 客户组合 (Customer Portfolio)

**模型**（Cohort，churn = 5%）：
$$C_t = (1-a) C_{t-1} + \beta_t \cdot i_{mkt,t}, \quad a=0.05$$
$$\beta_t = \frac{C_t - 0.95 C_{t-1}}{i_{mkt,t}}, \quad CAC_t = \frac{1}{\beta_t}$$

**数据来源**：
- C(t)：Basic data 列 E "Subscriptions (in millions)"，行 16–25
- i_marketing：Basic data 列 D "Marketing and sales"，行 3–12

**β 与 CAC 结果**（部分）：

| FY | C(t) (mn) | i_mkt ($mn) | β | CAC ($) |
|----|-----------|-------------|---|---------|
| 2018 | 2.9 | 1,087 | ... | ... |
| ... | ... | ... | ... | ... |
| 2024 | 6.74 | 1,823 | ... | 1,819 |
| 2025 | 7.53 | 2,000 | ... | 1,775 |
| 2026 | 7.79 | 2,373 | ... | 3,728 |

**客户组合价值**（作业要求：过去三年 CAC 平均）：
- 最近三年 CAC：$1,819、$1,775、$3,728  
- 三年平均：$2,441  
- C(2026) = 7.79 mn  
- 客户组合价值 = 2,441 × 7.79 = **$19,013 mn**

**图表**：`images/adsk_cost_per_customer.png` —— CAC 随时间变化。

---

### 5.3 股权资产价值 (Asset Value of Equity)

**公式**：AV = Book Equity + Product Portfolio + Customer Portfolio

**Book Equity 来源**：
- Excel：`ADSK-Data-February-2026-Students.xlsx`，Balance Sheet 表，Total Shareholders' Equity 行，JAN '26 列（col B）
- 年报对照：Form 10-K **Part II Item 8** (Financial Statements)，Consolidated Balance Sheets，约第 65 页起
- **结果**：$3,045 mn（课程 Excel FactSet 口径，JAN '26 Preliminary）

**计算**：
- Book Equity：$3,045 mn
- Product Portfolio：$4,363 mn
- Customer Portfolio：$19,013 mn  
- **Asset Value of Equity ≈ $26,421 mn**

---

## Q6 EPV (Earnings Power Value)

### 6.1 调整项

**产品组合**：
- Maintenance R&D = P_prod × 0.2 = 4,363 × 0.2 = $873 mn
- Growth R&D = R&D_2026 − Maintenance = 1,643 − 873 = **$770 mn**

**客户组合**：
- Maintenance marketing = a×C/β = 0.05×7.79 / β_2026  
- Growth marketing = 2,373 − 1,452 = **$921 mn**

### 6.2 EPV 计算

- Adj EBIT = 1,794 + 770 + 921 = **$3,485 mn**
- NOPAT = 3,485 × (1 − 0.21) = **$2,753 mn**
- WACC = 9%
- EPV (op) = 2,753 / 0.09 = $30,594 mn
- Cash：$2,597 mn（Basic data 列 I）
- Debt：$2,682 + $52 = $2,734 mn（Basic data 列 F、G）
- **EPV Equity ≈ $30,457 mn**

### 6.3 AV vs EPV

- EPV ($30.5B) > AV ($26.4B) → 显示存在护城河
- 若用最近一年 CAC ($3,728) 代替三年平均 ($2,441)：客户组合价值 = 3,728×7.79 = $29,031 mn，AV 上升，护城河判断不变（EPV 仍 > AV）
- EPV vs 市值：EPV 约 $30.5B，市值约 $54.7B（213×$257），当前市值高于 EPV，与 ADBE 情形不同（ADBE 市值低于 EPV）

---

## Q7 Growth

### 7.1 分配率 D/V

- 公式：Share repurchases / EV
- Repurchases：$1,402 mn（Basic data 列 J，FY2026）
- EV = Market Cap + Debt − Cash = 213×257 + 2,734 − 2,597 = **$54,878 mn**
- **Distribution yield = 1,402 / 54,878 = 2.55%**
- 与 ADBE 相比：ADBE 分配率曾达约 11%，ADSK 较低，说明回购力度相对 EV 较小。

### 7.2 历史 g（疫情以来）

- EBIT 2020：$357 mn；2026：$1,794 mn
- 6 年 CAGR = (1,794/357)^(1/6) − 1 = **30.9%**

### 7.3 边际 ROIC (FY2022–FY2026)

- Δ Adj NOPAT = 2,753 − 1,715 = $1,038 mn
- Σ Growth Capex（税后）≈ $7,047 mn
- **Marginal ROIC = 14.7%**

### 7.4 由 ROIC 推算的 g

- Plowback ≈ 1 − (Repurch/NOPAT) = 1 − 1,402/2,753 = 0.49
- **g = 0.49 × 14.7% ≈ 7.2%**

### 7.5 EV/EBIT

- EV/EBIT = 54,878 / 1,794 ≈ **30.6x**

---

## 关键公式汇总

| 模块 | 公式 |
|------|------|
| β(t) | [C(t) − 0.95×C(t−1)] / i_marketing(t) |
| CAC | 1/β |
| 客户组合价值 | 三年平均 CAC × C(latest) |
| Maintenance S&M | a×C/β |
| Maintenance R&D | 0.2 × P_prod |
| 边际 ROIC | Δ Adj NOPAT / Σ Growth Capex |
| g (ROIC) | Plowback × ROIC |

---

## 文件与脚本

| 文件 | 说明 |
|------|------|
| `scripts/q5_asset_value.py` | Q5 资产价值 |
| `scripts/q6_epv.py` | Q6 EPV |
| `scripts/q7_growth.py` | Q7 增长 |
| `scripts/run_all.py` | 一次性运行全部 |
| `Output/ADSK-Valuation-Output.xlsx` | 数值结果 |
| `images/adsk_cost_per_customer.png` | CAC 图 |
