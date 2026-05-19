# ADSK — Value Investing Final, Spring 2026

[Your Name], MBA 2026

Data: ADSK-Data-February-2026-Students.xlsx; Form 10-K FY2026 (filed Jan 31, 2026).

---

## The Business Operations of the Firm

### Q1. What does Autodesk do?

Autodesk is the global leader in 3D design, engineering, and entertainment technology solutions. Per its 10-K (Item 1, Business, p.5):

> "We are a global leader in 3D design, engineering and entertainment technology solutions, spanning architecture, engineering, construction, product design, manufacturing, media, and entertainment. Our customers design, fabricate, manufacture, and build anything by visualizing, simulating, and analyzing real-world performance early in the design process."

The company operates across four product families: (1) **AECO** (Architecture, Engineering, Construction & Operations) — anchored by Revit, AutoCAD Civil 3D, and the Autodesk Construction Cloud; (2) **AutoCAD/AutoCAD LT** — the foundational 2D/3D drafting platform; (3) **Manufacturing** — Fusion, Inventor, and the Product Design & Manufacturing Collection; (4) **Media & Entertainment** — Maya, 3ds Max, and Flow Production Tracking. Revenue is overwhelmingly subscription-based (~98% recurring), delivered via a hybrid desktop-plus-cloud model. The company has invested heavily in AI, machine learning, and generative design to deliver automation and efficiency gains (10-K Item 1, p.8).

### Q2. Main competitors by segment and barriers to entry

The 10-K (Item 1, Competition, p.11) lists key global competitors including Bentley, Dassault Systèmes, Hexagon, Nemetschek, Oracle, Procore, PTC, Siemens PLM, Trimble, Adobe, and 3D Systems.

**By segment**:

- **AECO**: Bentley, Procore, Trimble, Nemetschek
- **AutoCAD/LT**: Broad CAD competition (partial overlap with Dassault, PTC, Siemens)
- **Manufacturing**: Dassault (SolidWorks), Siemens PLM, PTC, Hexagon/MSC
- **M&E**: Adobe, and other digital-content/VFX tools

**Barriers to entry**: Autodesk's moat rests on **workflow lock-in, deep enterprise relationships, and high switching costs** — not single-feature superiority. Enterprise customers depend on file-format compatibility (DWG, RVT), team collaboration infrastructure, historical project archives, and extensive training investment. Replacing the entire toolchain is extremely expensive and disruptive to ongoing projects. AI lowers the barrier for lightweight tools, but it is much harder to replicate the integrated, enterprise-grade ecosystem.

### Q3. Operating margins — any slump? Is AI visible in profitability?

Operating margin (Op. Income / Revenue, Basic data sheet):

| FY2022 | FY2023 | FY2024 | FY2025 | FY2026 |
|--------|--------|--------|--------|--------|
| 15.0% | 20.1% | 20.5% | 22.9% | 24.9% |

**No slump.** Margins have steadily improved from 15% to 25% over five years. This is consistent with operational leverage as Autodesk scales its subscription base. The 10-K (Item 7, p.57) confirms: GAAP operating margin 21%→22%→22% (FY2024–26); Non-GAAP 36%→36%→38%.

There is no evidence that AI has materially impaired ADSK's profitability to date. Revenue growth remains strong (18% YoY in FY2026), and margins are expanding.

### Q4. Will AI threaten ADSK's business model?

AI poses a real long-term strategic risk, but it is more likely to **reshape** Autodesk's delivery and product architecture than to destroy its business model in the short-to-medium term:

1. **Workflow lock-in is strong**: Enterprise design/build/make processes involve long collaboration chains, regulatory compliance, and deep integrations. Switching costs remain high.
2. **Product ecosystem depth**: Autodesk sells not a single tool but interconnected product families across the full project lifecycle. AI tools that automate one task still depend on the broader platform.
3. **Evidence of resilience**: Recurring revenue ~98%, operating margins expanding, RPO growing (10-K Item 7, p.45).
4. **IP governance**: The 10-K (Item 1, Intellectual Property, p.12) emphasizes patents, copyrights, and licensing protections. However, ADSK's IP moat is more about process/workflow than the "permissioned content library" advantage that Adobe possesses in generative creative content.

---

## Valuation

### Q5. Asset Value (25 points)

#### 5.1 Customer Acquisition Cost (churn = 5%)

**Cohort model** (per Transcript S11 methodology):

$$C_t = (1 - a) \cdot C_{t-1} + \beta_t \cdot i_{mkt,t}, \quad a = 0.05$$

Solving for $\beta$: $\beta_t = [C_t - 0.95 \cdot C_{t-1}] / i_{mkt,t}$; CAC = $1/\beta$.

Data: Subscriptions (Basic data col E) and Marketing and sales (col D).

| FY | Subscriptions (mn) | Marketing ($mn) | CAC ($) |
|----|-------------------|-----------------|---------|
| 2024 | 6.74 | 1,823 | 1,819 |
| 2025 | 7.53 | 2,000 | 1,775 |
| 2026 | 7.79 | 2,373 | 3,728 |

**Comment**: CAC was relatively stable around $1,800 in FY2024–25 but spiked to ~$3,728 in FY2026. The jump is driven by a large increase in marketing spend (+$373 mn YoY) while net subscription additions slowed (only +0.26 mn vs +0.79 mn in FY2025). This may signal market maturation, a shift in go-to-market strategy (e.g., the new transaction model described in the 10-K, Item 1, p.8), or a more competitive environment. The rising trend is a concern.

Chart: `images/adsk_cost_per_customer.png`

#### 5.2 Customer Portfolio Value

Using the **average CAC of the last three years** (per assignment):

- 3-year average CAC = (1,819 + 1,775 + 3,728) / 3 = **$2,441**
- C(2026) = 7.79 mn subscriptions
- **Customer portfolio value = 2,441 × 7.79 = $19,013 mn**

#### 5.3 Product Portfolio (Permanent Inventory, d = 0.2)

$$P_{prod} = R\&D_{2026} + 0.8 \cdot R\&D_{2025} + 0.6 \cdot R\&D_{2024} + 0.4 \cdot R\&D_{2023} + 0.2 \cdot R\&D_{2022}$$

= 1,643 + 0.8×1,485 + 0.6×1,372 + 0.4×1,214 + 0.2×1,113.6 = **$4,363 mn**

(R&D data: Basic data col C, FY2022–2026.)

#### 5.4 Asset Value of Equity

| Component | $mn | Source |
|-----------|-----|--------|
| Book Equity | 3,045 | Balance Sheet, JAN '26 |
| + Product Portfolio | 4,363 | Permanent inventory |
| + Customer Portfolio | 19,013 | 3-yr avg CAC × C |
| **Asset Value of Equity** | **26,421** | |

---

### Q6. EPV (25 points)

#### 6.1 Adjustments

GAAP expenses R&D and marketing entirely, but part of each is growth investment (capital expenditure on intangibles). We add back the growth portion:

**(a) Product portfolio**
- Maintenance R&D = P_prod × d = 4,363 × 0.2 = $873 mn
- Growth R&D = 1,643 − 873 = **$770 mn** (added back)

**(b) Customer portfolio**
- Maintenance marketing = a × C(2026) / β(2026) = 0.05 × 7.79 / β ≈ **$1,452 mn**
- Growth marketing = 2,373 − 1,452 = **$921 mn** (added back)

#### 6.2 EPV Calculation

| Line | Item | $mn |
|------|------|-----|
| 1 | Reported EBIT (FY2026) | 1,794 |
| 2 | + Growth R&D | 770 |
| 3 | + Growth marketing | 921 |
| 4 | **Adjusted EBIT** | **3,485** |
| 5 | Tax (21%) | (732) |
| 6 | **Sustainable NOPAT** | **2,753** |
| 7 | ÷ WACC (9%) | |
| 8 | EPV (operating business) | 30,594 |
| 9 | + Cash | 2,597 |
| 10 | − Debt (LT $2,682 + ST $52) | (2,734) |
| 11 | **EPV Equity** | **30,457** |

#### 6.3 AV vs EPV — Barriers to Entry

- **EPV ($30.5 bn) > AV ($26.4 bn)** → indicates the existence of barriers to entry. The firm earns more from its assets than it would cost a new entrant to replicate them.
- **Sensitivity (last year's CAC)**: If we use only the FY2026 CAC of $3,728, customer portfolio = 3,728 × 7.79 = $29,031 mn, pushing AV up to ~$36.4 bn. In this case AV > EPV, which would suggest the moat is weaker or that the most recent CAC is an outlier. The 3-year average is more representative given the FY2026 spike. **The barrier-to-entry conclusion is robust under the smoothed estimate but sensitive to the latest data point.**

#### 6.4 EPV vs Market Cap — Comparison to ADBE

- ADSK market cap ≈ 213 mn shares × $257 = **$54.7 bn**
- EPV ($30.5 bn) is **well below** market cap.
- **This is the opposite of ADBE**: Adobe traded below its EPV (~$124 bn EPV vs ~$108 bn market cap), meaning the market was selling ADBE at a discount to sustainable earnings, implying AI terminal-value fear. ADSK trades at a large premium to EPV ($54.7 bn vs $30.5 bn), meaning the market is pricing in substantial future growth.
- **What explains the difference?** (1) ADSK's multiple has not compressed as severely as ADBE's (EV/EBIT ~30.6x vs ADBE ~15x); (2) the market may view design/engineering workflows as more defensible vs AI than creative content; (3) ADSK is at an earlier stage of SaaS transition and margin expansion, giving more "growth runway."

---

### Q7. Growth (25 points)

#### 7.1 Distribution Yield

- Share repurchases (FY2026) = $1,402 mn (Basic data col J)
- EV = Market cap + Debt − Cash = 54,741 + 2,734 − 2,597 = **$54,878 mn**
- **D/V = 1,402 / 54,878 = 2.55%**

**vs ADBE**: ADBE's distribution yield reached ~11% during the selloff because (a) the stock price dropped sharply, deflating EV, and (b) buybacks were aggressively ramped up. ADSK's 2.55% is much lower. This tells us ADSK's valuation has not been punished to nearly the same extent as ADBE — the CFO is buying back stock, but at a much smaller scale relative to EV. ADSK is not the same "cigar butt on a discount shelf" that ADBE appears to be.

#### 7.2 Historical g (Earnings Growth Since the Pandemic)

- EBIT FY2020: $357 mn; EBIT FY2026: $1,794 mn
- 6-year CAGR = (1,794 / 357)^(1/6) − 1 = **30.9%**

This is inflated by pandemic recovery and operational leverage from the subscription transition. A more structural estimate comes from the ROIC approach below.

#### 7.3 Marginal ROIC (FY2022–FY2026)

We compute the after-tax growth expenses (customer + product) for each year, then:

- Δ Adjusted NOPAT (FY2022→FY2026) = 2,753 − 1,715 = **$1,038 mn**
- Σ After-tax growth capex (FY2022–2026) = **$7,047 mn**
- **Marginal ROIC = 1,038 / 7,047 = 14.7%**

This is above WACC (9%), confirming that incremental investments create value and supporting the barrier-to-entry finding.

#### 7.4 g from Marginal ROIC

- Plowback ≈ 1 − (Repurchases / NOPAT) = 1 − 1,402 / 2,753 = **0.49**
- **g = Plowback × ROIC = 0.49 × 14.7% ≈ 7.2%**

#### 7.5 Expected Return and Multiple Risk

- **EV/EBIT = 54,878 / 1,794 ≈ 30.6x**

**If multiple stays constant**: Expected return ≈ D/V + g = 2.55% + 7.2% = **~9.7%**

**Multiple compression scenario**: If ADSK's multiple compresses from 30.6x to, say, 20x over 5 years (a ~34% decline), annualized multiple drag ≈ −8%. Net return ≈ 9.7% − 8% ≈ **~1.7%** — barely above risk-free. This is the key risk.

**Multiple expansion scenario**: If the market re-rates ADSK higher (e.g., toward historical highs ~40x), the return could be substantially higher. But given the current AI/SaaS overhang, expansion seems less likely than compression.

---

### Q8. Would you invest in this company?

**Recommendation: Cautious / Not at current prices.**

| Metric | ADSK | ADBE (for comparison) |
|--------|------|-----------------------|
| Asset Value | $26.4 bn | $57.4 bn |
| EPV Equity | $30.5 bn | $124 bn |
| Market Cap | $54.7 bn | ~$108 bn |
| EPV vs Market | EPV < Mkt (growth priced in) | EPV > Mkt (discount to earnings) |
| EV/EBIT | 30.6x | ~15x |
| Distribution yield | 2.55% | ~11% |
| Marginal ROIC | 14.7% | ~16% |

**Arguments against investing now**:
1. Market cap ($54.7 bn) far exceeds EPV ($30.5 bn). You are paying for growth that must materialize.
2. EV/EBIT of 30.6x leaves significant room for multiple compression if AI fears spread to ADSK or macro conditions deteriorate.
3. Distribution yield of only 2.55% provides limited downside support compared to ADBE's ~11%.
4. The sharp CAC spike in FY2026 is a warning sign about the cost of future growth.

**Arguments for investing**:
1. Barriers to entry exist (EPV > AV; marginal ROIC 14.7% > WACC).
2. Operating margins are expanding, not contracting.
3. Engineering/design workflows are arguably more defensible against AI disruption than creative-content workflows.
4. g from ROIC (~7.2%) is healthy and supported by structural demand for design automation.

**Bottom line**: ADSK is a high-quality franchise, but unlike ADBE, the market has not yet discounted it to a level where sustainable earnings alone justify the price. The expected return (~9.7% at constant multiple) is modest for the risk. I would wait for a more favorable entry point — either via multiple compression (perhaps toward 20x EV/EBIT) or a clearer signal that AI is not a terminal threat. ADBE, at its current valuation, presents a more compelling risk/reward.
