# ADSK Valuation Q5–Q7 Answers

**Data sources**: ADSK-Data-February-2026-Students.xlsx (Basic data, Balance Sheet, Income Statement, Cash Flow), Form 10-K FY2026 (filed Jan 31, 2026).  
**Methodology**: Transcripts S11/S12, Lecture-8 Adobe notes.

---

## Data Source Summary

| Item | Source | Location |
|------|--------|----------|
| R&D, Marketing, Op. Income, Revenues, Debt, Cash, Share repurchases | Excel Basic data | Rows 3–12 (FY2017–2026), cols C–J |
| Subscriptions (millions) | Excel Basic data | Rows 16–25, col E; maps to 10-K Item 7 MD&A "key metrics" |
| Shares, Stock price | Excel Basic data | Rows 16–25, cols C–D; verified vs 10-K p.1 |
| Churn 5%, Tax 21% | Excel Basic data | Row 3, Parameters cols L–M (assignment specified) |
| Book Equity | Excel Balance Sheet | Total Shareholders' Equity, JAN '26 col; 10-K Item 8 p.65 |
| Share count 213M | 10-K p.1 | "approximately 213 million shares ... held by non-affiliates" (as of Jul 31, 2025) |

---

## Q5. Asset Value (25 points)

### 5.1 Cost of Acquiring One Customer (churn rate 5%)

**Model**: Cohort dynamics  
$$C_t = (1-a) C_{t-1} + \beta_t \cdot i_{mkt,t}, \quad a = 0.05$$  
From this: $\beta_t = [C(t) - 0.95 \cdot C(t-1)] / i_{mkt}(t)$, and **CAC = 1/β**.

**Data**: Subscriptions (col E) and Marketing and sales (col D) from Basic data.

**Chart**: `images/adsk_cost_per_customer.png` — CAC over time.  
CAC has moved around; in FY2026 it spikes (≈$3,728) because marketing spend jumped ($2,373 mn) while net subscription growth was relatively modest. Earlier years (2024–25) had CAC around $1,775–1,819.

**Interpretation**: The 2026 spike may reflect a shift in go-to-market or a push to convert/maintain customers in a tougher AI/SaaS environment. The rising CAC suggests either market maturation or more expensive acquisition.

---

### 5.2 Value of Reproducing the Customer Portfolio

Per the assignment, the value of the customer base is estimated using the **average of the last three years’ CAC** (not just the latest year):

- Last three years’ CAC: $1,819 (FY2024), $1,775 (FY2025), $3,728 (FY2026)  
- 3-year average: **$2,441**  
- C(2026) = 7.79 mn subscriptions  

**Customer portfolio value** = 2,441 × 7.79 = **$19,013 mn ($19.0 bn)**

---

### 5.3 Product Portfolio

**Method**: Permanent inventory (amortization rate d = 0.2):

$$P_{prod} = R\&D_{2026} + 0.8 \cdot R\&D_{2025} + 0.6 \cdot R\&D_{2024} + 0.4 \cdot R\&D_{2023} + 0.2 \cdot R\&D_{2022}$$

| FY | R&D ($mn) |
|----|-----------|
| 2022 | 1,113.6 |
| 2023 | 1,214 |
| 2024 | 1,372 |
| 2025 | 1,485 |
| 2026 | 1,643 |

**Calculation**: 1,643 + 0.8×1,485 + 0.6×1,372 + 0.4×1,214 + 0.2×1,113.6 = **$4,363 mn**

---

### 5.4 Asset Value of Equity

| Component | Amount ($mn) | Source |
|-----------|--------------|--------|
| Book Equity | 3,045 | Balance Sheet, JAN '26 |
| Product Portfolio | 4,363 | Permanent inventory (above) |
| Customer Portfolio | 19,013 | 3-yr avg CAC × C(2026) |
| **Asset Value of Equity** | **26,421** | |

**Asset Value of Equity ≈ $26.4 bn**

---

## Q6. EPV (25 points)

### 6.1 Adjustments to Calculate Earnings Power Value

EBIT must be adjusted for growth investments that are expensed (R&D and marketing growth) but should be treated as capital outlays:

**(a) Product portfolio**  
- Maintenance R&D = P_prod × 0.2 = 4,363 × 0.2 = $873 mn  
- Growth R&D = R&D_2026 − Maintenance = 1,643 − 873 = **$770 mn**  
- This $770 mn is added back to EBIT.

**(b) Customer portfolio**  
- Maintenance marketing = a × C / β = 0.05 × 7.79 / β_2026 ≈ $1,452 mn  
- Growth marketing = Marketing_2026 − Maintenance = 2,373 − 1,452 = **$921 mn**  
- This $921 mn is added back to EBIT.

### 6.2 EPV Calculation

| Item | Amount ($mn) |
|------|--------------|
| Reported EBIT (FY2026) | 1,794 |
| + Growth R&D | 770 |
| + Growth marketing | 921 |
| **Adjusted EBIT** | **3,485** |
| Tax (21%) | 732 |
| **Sustainable NOPAT** | **2,753** |
| WACC | 9% |
| EPV (operating) = 2,753 / 0.09 | 30,594 |
| + Cash | 2,597 |
| − Debt (LT + ST) | 2,734 |
| **EPV Equity** | **30,457** |

**EPV Equity ≈ $30.5 bn**

### 6.3 AV vs EPV and Barriers to Entry

- EPV ($30.5 bn) > Asset Value ($26.4 bn) → indicates **barriers to entry**. Sustainable earnings exceed the cost to reproduce assets.  
- **Sensitivity**: If we used the **most recent year’s CAC** ($3,728) instead of the 3-year average, customer portfolio value = 3,728 × 7.79 = $29,031 mn. Asset Value would rise to ≈ $36.4 bn, still below EPV, so the barrier-to-entry conclusion holds.

### 6.4 EPV vs Market Cap and Comparison to ADBE

- ADSK market cap ≈ 213 × $257 ≈ $54.7 bn  
- EPV ($30.5 bn) < market cap ($54.7 bn).  
- **Unlike ADBE**: ADBE traded below EPV when the market worried about AI terminal-value risk. ADSK currently trades above EPV, which suggests the market is pricing in growth or a different risk profile. Possible explanations: (1) ADSK’s design/engineering software is seen as more defensible vs AI; (2) different stage of AI fear; (3) stronger growth expectations for ADSK.

---

## Q7. Growth (25 points)

### 7.1 Distribution Yield

ADSK returns cash mainly via share repurchases.

- **Formula**: Distribution yield = Share repurchases / Enterprise Value  
- Repurchases (FY2026) = $1,402 mn (Basic data, col J)  
- EV = Market cap + Debt − Cash = 54,741 + 2,734 − 2,597 = **$54,878 mn**  
- **Distribution yield = 1,402 / 54,878 = 2.55%**

**vs ADBE**: ADBE’s distribution yield reached ~11% during the selloff. ADSK’s 2.55% is lower, so repurchases as a share of EV are smaller. That may reflect less aggressive buybacks or a higher valuation multiple for ADSK.

### 7.2 Historical g (Earnings Growth Since the Pandemic)

Using EBIT from the pandemic period:

- EBIT FY2020: $357 mn  
- EBIT FY2026: $1,794 mn  
- 6-year CAGR: (1,794 / 357)^(1/6) − 1 = **30.9%**

This high growth partly reflects recovery and operational leverage post-pandemic; it is not a good long-term g assumption.

### 7.3 Marginal ROIC (FY2022–FY2026)

- Δ Adj NOPAT = 2,753 − 1,715 = **$1,038 mn**  
- Σ Growth capex (after-tax, cust + prod) ≈ **$7,047 mn**  
- **Marginal ROIC = 1,038 / 7,047 = 14.7%**

So incremental capital earns about 15%, above a typical WACC, which supports the presence of barriers to entry.

### 7.4 g from Marginal ROIC

- Plowback = 1 − (Repurchases / NOPAT) = 1 − 1,402/2,753 ≈ **0.49**  
- g = Plowback × ROIC = 0.49 × 14.7% ≈ **7.2%**

A g of ~7% is more plausible than the 30.9% historical CAGR for forward estimates.

### 7.5 EV/EBIT and Multiple Compression

- **EV/EBIT = 54,878 / 1,794 ≈ 30.6x**

If the multiple stays at ~30x, total return ≈ Distribution yield + g ≈ 2.55% + 7.2% ≈ 9.7%. If the multiple compresses toward a lower level (e.g., 20x), returns would be lower; if it expands, returns would be higher. Risk management for the multiple requires judging how sustainable ADSK’s growth and moat are in an AI/SaaS environment.

---

## Key Formulas Summary

| Module | Formula |
|--------|---------|
| β(t) | [C(t) − 0.95×C(t−1)] / i_marketing(t) |
| CAC | 1/β |
| Customer portfolio value | 3-yr avg CAC × C(latest) |
| Maintenance S&M | a×C/β |
| Maintenance R&D | 0.2 × P_prod |
| Marginal ROIC | Δ Adj NOPAT / Σ Growth Capex |
| g (ROIC) | Plowback × ROIC |
