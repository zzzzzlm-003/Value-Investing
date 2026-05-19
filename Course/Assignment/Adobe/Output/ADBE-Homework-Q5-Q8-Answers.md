# Adobe Homework Q5–Q8 Answers

**Data source:** ADBE-Homework-Data-2026-2.xlsx  
**Fiscal year:** FY2025 (ended November 2025)

---

## Q5. Asset Value

### 5.1 Product Portfolio (Permanent Inventory, d = 0.2)

Formula: P_prod = R&D_2025 + 0.8×R&D_2024 + 0.6×R&D_2023 + 0.4×R&D_2022 + 0.2×R&D_2021

With R&D ($mn): 4,294, 3,944, 3,473, 2,987, 2,540 → **P_prod ≈ $11,236 mn ($11.2B)**

**Analysis:** The permanent-inventory method treats R&D as an investment in product/technology stock. The d=0.2 assumption implies a 5-year economic life. Adobe’s product portfolio value exceeds book intangibles because much R&D is expensed under GAAP.

### 5.2 Customer Portfolio

Model: C(t) = (1−a)×C(t−1) + β(t)×i_marketing(t), with a = 0.1.  
From this: β(t) = [C(t) − 0.9×C(t−1)] ÷ i_marketing(t).

- β(2025) ≈ 0.001187
- Cost per account = 1/β ≈ $843
- Customer portfolio value = (1/β) × C(2025) = 843 × 41 mn accounts ≈ **$34.5B**

*Chart: images/adbe_cost_per_customer.png*

**Analysis:** Cost per account has risen over time (from ~$150–200 in the early 2010s to ~$843 in 2025). Spikes in 2020 (pandemic) and 2024 (AI competition) reflect temporary shocks. The underlying trend reflects market maturation and lower marketing efficiency. If this continues, profitability and customer-portfolio value deserve a more conservative view.

### 5.3 Asset Value of Equity

Asset Value of Equity = Book Equity + Product Portfolio + Customer Portfolio = 11,623 + 11,236 + 34,546 = **57,405 ($mn)**

**Analysis:** Adjusted asset value is about 5× book equity. The gap comes from expensed intangibles (R&D, customer acquisition) that are not on the balance sheet.

---

## Q6. EPV (Earnings Power Value)

### Adjustments

1. **Product portfolio:** Maintenance R&D = P_prod × 0.2 = 2,247. Growth R&D = 4,294 − 2,247 = **$2,047 mn**
2. **Customer portfolio:** Maintenance marketing = a×C(2025)/β(2025) = 3,455. Growth marketing = 6,488 − 3,455 = **$3,033 mn**

Both adjustments add back expensed growth investment to obtain sustainable operating income.

### Calculation

Adjusted EBIT = EBIT + Growth R&D + Growth marketing = 8,712 + 2,047 + 3,033 = 13,792 ($mn)  
Sustainable NOPAT = Adjusted EBIT × (1 − 18.4%) = 13,792 × 0.816 = 11,259 ($mn)  
EPV = Sustainable NOPAT ÷ WACC = 11,259 ÷ 7% = **160,846 ($mn)**

**Analysis:** EPV assumes zero growth and uses only sustainable earnings. The large gap between EPV and current market cap implies the market either expects lower sustainable earnings or assigns higher risk (e.g., AI disruption).

---

## Q7. Growth

### 7.1 D/V – Distribution Yield

| Year | Distribution yield |
|------|--------------------|
| 2024 | 4.8% |
| 2025 | 11.1% |

**What happened?** Yield almost doubled in 2025. Main drivers: (1) Stock price fell on AI/SaaS fears, so the same buybacks produced a higher yield. (2) Adobe pays no dividends (10-K: “We do not anticipate paying any cash dividends”); distribution is from repurchases. (3) In March 2024, the Board authorized up to $25B in buybacks through March 2028.

**Implications:** A higher yield can mean the market expects weaker fundamentals, or that it overreacted. Management’s continued buybacks suggest they view the stock as undervalued.

### 7.2 g – Historical Earnings Growth

| Horizon | EBIT CAGR |
|---------|-----------|
| 5-year (2020→2025) | 15.5% |
| 10-year (2015→2025) | 26.2% |

*Source: Sales & EBIT sheet.*

### 7.3 EV/EBIT Multiple & Risk

*Chart: images/adbe_ev_ebit_and_yield.png*

- 2025Q4 EV/EBIT: ~15.2x  
- 2020–2021 peak: ~50x

**Analysis:** The multiple collapsed from ~50x to ~15x. This reflects concerns about AI disruption to creative and document software. If AI materially erodes Adobe’s economics, the lower multiple is justified. If the threat is overstated, current multiples leave room for upside.

---

## Valuation Benchmark: Adjusted vs. Book vs. Market

| Metric | Value ($B) | Source |
|--------|------------|--------|
| Book Equity | 11.6 | Balance Sheet |
| Asset Value (adjusted) | 57.4 | Q5 |
| EPV | 160.8 | Q6 |
| Market cap (May 2025) | 144.9 | 10-K |
| Implied market cap (2025Q4) | ~133 | EV/EBIT 15.2x |
| Historical EV/EBIT peak | ~50x | 2020–2021 |

**Interpretation**

- Book equity understates value because R&D and customer acquisition are expensed. Adjusted asset value is about 5× book.
- EPV exceeds current market. The market is discounting either lower sustainable earnings or higher risk.
- Market cap fell from ~$145B (May) to ~$133B (2025Q4) as the multiple compressed.
- EPV is ~21% above the May level. Management’s buybacks are consistent with a view that the stock is cheap relative to earnings power.

---

## Q8. Would You Invest?

**Summary**

| Metric | Value | Implication |
|--------|-------|-------------|
| Asset Value | ~$57B | Floor; asset support |
| EPV | ~$161B | Strong earnings power |
| Current market cap | ~$133B | Below EPV |
| EV/EBIT 2025Q4 | ~15x | Compressed vs. ~30–50x history |

**Reasons to invest**

- EPV well above market cap.
- Asset value adds downside support.
- High distribution yield and buybacks suggest management confidence.
- Historical EBIT growth strong (15%+ over 5 years).

**Reasons for caution**

- AI/SaaS disruption risk.
- Rising customer acquisition cost.
- Macro and tech-cycle uncertainty.

**Conclusion**

On a value basis, Adobe appears attractively valued. Investment hinges on whether AI materially disrupts its model. If not, current multiples offer room for upside. A position is defensible for investors who believe Adobe’s moat and AI strategy are underappreciated.

---

## Data & Files

- **Input:** ADBE-Homework-Data-2026-2.xlsx
- **Output:** ADBE-Homework-Output.xlsx
- **Charts:** images/adbe_cost_per_customer.png, images/adbe_ev_ebit_and_yield.png
