# Deere Homework 1 — Final Submission

Value Investing MBA Spring 2026
Luomeng Zhou (uni:lz3064) MSBA

---

## One-Sentence Conclusion

Deere is now a typical "high-quality cyclical": strong industry position and customer stickiness, but 2025 was hit by tariffs and the demand cycle, so short-term earnings face pressure. The EPV calculated under the assignment assumptions is still clearly higher than what current depressed profits would suggest, which shows that core operating capability has not been impaired.

---

## Part A: Business Economics

### Q1. What does Deere do? How does the financial statement reflect this? Is there customer captivity and moat?

Deere is an integrated "farm equipment + financial services" company. Its main businesses are:

- **Production & Precision Agriculture (PPA)**: large farm equipment and precision agriculture systems
- **Small Agriculture & Turf (SAT)**: small tractors, lawn and turf equipment
- **Construction & Forestry (CF)**: construction and forestry equipment
- **Financial Services (FS)**: retail/wholesale financing, leasing, insurance

In the financials, Equipment Operations and Financial Services have distinct balance-sheet structures: the equipment side emphasizes inventories, PPE, and manufacturing operating profit; the financial side emphasizes receivables from financing, securitized liabilities, and credit risk management.

**Customer captivity** mainly comes from: (1) brand, (2) dealer network, (3) hardware and software ecosystem plus data platform, (4) financing lock-in—once a customer buys equipment they enter Deere’s financial system, and (5) parts and service—difficult to self-service or rely on third parties for repairs.

**Moat** mainly includes R&D, channel/dealer network, and a full product-lifecycle approach (financing, solutions tailored to the farm production cycle, after-sales service)—not just the machine itself.

![Deere: Segment Revenue Share and Operating Margin by Year](images/segment_stacked_pct_margin_lines.png)

---

### Q2. Main Competitors + 2006–2024 Revenue Shares

Main rivals: **CNH, AGCO, Kubota, Claas**.
Using course data (Industry) and currency conversion, Deere has long been the strongest in the top tier, with a noticeable share gain after 2021.

**2024 shares (total revenue)**:

| Company | Share |
| ------- | ----: |
| Deere   | 47.3% |
| Kubota  | 18.8% |
| CNH     | 14.8% |
| AGCO    | 13.4% |
| Claas   |  5.7% |

**2024 shares (Farm-only)**:

| Company | Share |
| ------- | ----: |
| Deere   | 43.0% |
| Kubota  | 19.0% |
| AGCO    | 16.3% |
| CNH     | 14.6% |
| Claas   |  7.2% |

![Farm Equipment Revenue Shares - Total](images/industry_revenue_shares.png)
![Farm Equipment Revenue Shares - Pure Farm](images/industry_revenue_shares_farm_only.png)

Conclusion: **There is no single competitor at Deere’s scale.** The other four rivals split roughly 60% of the remaining market.

---

### Q3. Drivers of Farm Equipment Demand (Short-term vs Long-term)

Per the annual report, farm equipment demand is driven by crop prices, farm cash income, financing costs, policy environment, and used equipment conditions.

**Short-term drivers**: crop prices, interest rates, weather, subsidies, trade policy shocks.
**Long-term drivers**: replacement cycles, technology adoption (precision agriculture), land and farm balance-sheet health.

We used FRED variables (corn, soybeans, oil, natural gas, energy index, farmland assets, farm wages), converted to YoY, and compared them with Deere equipment sales:

![Demand Variables vs Deere Sales](images/demand_deere_combined.png)

The chart supports the view that demand is not driven by a single factor, but by a combination of crop prices, input costs, financing conditions, and policy.

---

## Part B: Current Challenges

### Q4. How is Deere exposed to tariff risk? What does the annual report say?

Per FY2025 10-K (Risk Factors + MD&A):

- Deere states that tariffs and retaliatory tariffs affect sourcing, manufacturing costs, and pricing power on imports/exports
- ~80% of domestic sales are assembled in the U.S., the rest from Europe, Mexico, India, and Japan
- 2025 incremental tariffs have a **direct impact of ~$600M** (excluding pass-through and second-order demand effects)
- As a net exporter of U.S. farm and turf equipment, retaliatory tariffs compress export margins
- The company also mentions uncertainty around potential relief from the IEEPA tariff case

So the question is not whether tariffs matter, but that the impact is already in place and still evolving.

---

### Q5. How did the stock react after Trump’s tariff announcements?

Trump announced tariffs multiple times. Using the `Deere in 2024 and 2025` table, we compute “low within two weeks of announcement” and “subsequent high”:

| Announcement | Low within 2 weeks | Subsequent high | Return |
| ------------ | -----------------: | --------------: | -----: |
| 2025-01-20   |             459.75 |          531.48 | 15.60% |
| 2025-02-01   |             464.98 |          531.48 | 14.30% |
| 2025-02-10   |             466.22 |          531.48 | 14.00% |
| 2025-03-26   |             412.99 |          531.48 | 28.69% |
| 2025-04-02   |             412.99 |          531.48 | 28.69% |
| 2025-04-09   |             441.56 |          531.48 | 20.36% |
| 2025-08-07   |             478.84 |          495.99 |  3.58% |

For the canonical 1/20 event, the rebound is 15.6%; for the 3–4 April shock, the rebound is ~29%.

Relative to quarterly revenue, the market rebounded faster than fundamentals, suggesting valuation reflects “expectations repair” rather than only realized earnings—consistent with the classroom discussion of markets freaking out.

![Deere Stock Price vs Tariff Events](images/de_stock_tariff.png)

---

## Part C: Asset Value + EPV

> Per assignment: treat Equipment Operations as the main entity; Financial Services on the equity method (move Financial Services equity from EO equity to the asset side for analysis).

### Q6. Asset Value

#### 6.1 Tangibles (first three items)

**(1) Inventories: Adjustment warranted**

- Annual report discloses LIFO/FIFO difference
- FY2025: LIFO inventory 7,406, FIFO excess 2,721 ($mn)
- For asset value, FIFO better approximates replacement cost; equivalent to adding back 2,721 to inventory

**(2) PPE: Adjustment warranted, but qualitative only per assignment**

- Land is not depreciated; book value tends to be conservative
- Buildings are only impaired, not revalued; may diverge from actual rents/land values
- Equipment and tools often have economic life beyond accounting depreciation

PPE should not be mechanically carried at book value in asset-value analysis.

**(3) Financial Services equity: Need to assess “default resilience”**

Without gathering extra data, we only make a framework judgment:

- Key question: whether FS equity can cover losses on receivables under stress
- For rigorous modeling, one would need default rates, LGD, portfolio correlation, industry/region concentration, securitization structure
- On “whether the parent is liable for JD Capital debt”: **no automatic joint liability in principle**, unless there is explicit guarantee or contractual support

---

#### 6.2 Intangibles (Brand + Product Portfolio)

**Brand**
Per assignment, using consultant valuation: Interbrand 2025 values John Deere brand at **$8.8B** (Interbrand Best Global Brands: https://interbrand.com/best-global-brands/global/).

**Product Portfolio**
Using the assignment’s perpetual-inventory model (5-year linear amortization):

| R&D Exp. | 1,589.0 | 1,587.0 | 1,912.0 | 2,177.0 | 2,257.0 | 2,311.0 |
| -------- | ------- | ------- | ------- | ------- | ------- | ------- |

$P_{prod}=R\&D_{2025}+0.8R\&D_{2024}+0.6R\&D_{2023}+0.4R\&D_{2022}+0.2R\&D_{2021}$

With course R&D ($mn):
$P_{prod}=2311+0.8\times2257+0.6\times2177+0.4\times1912+0.2\times1587\approx6505$

→ **Product portfolio value ≈ $6.51B**

---

### Q7. EPV (per Lecture, WACC = 7%)

Following Lecture 3: adjust operating income, compute NOPAT, divide by WACC.

**Step 1: Base EBIT (Equipment Operations)**

$EBIT = \text{Income before tax} + \text{Interest expense} + \text{Interest to FS}$
$=5145+372+414=5931$

$ \quad (\$mn)$

**Step 2: Growth expense adjustment (intangible-related growth expenses)**

1) **R&D adjustment**

- Maintenance R&D = \(P_{prod}/5 = 6531.4/5=1306.3\)
- Growth R&D = \(2311-1306.3=1004.7\)

2) **Brand adjustment (per lecture approximation)**

- Marketing proxy in SG&A: \(0.35\times 3856=1349.6\)
- Brand maintenance amortization: \(8800/15=586.7\)
- Growth brand expense: \(1349.6-586.7=762.9\)

Total growth adjustment ≈ \(1004.7+762.9=1767.6\) ($mn).

**Step 3: Adjusted Operating Income**

$Adj.\ Op.\ Income = 5931 + 1767.6 = 7698.6$

**Step 4: Sustainable NOPAT after tax**

Using effective tax rate approximation:
$t=1020/5145\approx19.8\%$
$Adj.\ NOPAT=7698.6\times(1-19.8\%)\approx6172.4$

**Step 5: EPV**

$EPV=\frac{Adj.\ NOPAT}{WACC}=\frac{6172.4}{0.07}=88177$

→ **EPV (Operating) ≈ $88.2B**

---

## Summary

1. Deere’s competitive position and customer captivity remain; short-term volatility mainly reflects cycle and policy shocks.
2. For asset value, inventories (LIFO/FIFO) and intangibles (especially product portfolio) are key adjustments.
3. Under the assignment assumptions, EPV still provides support: “short-term profit pressure ≠ collapse of long-term operating capability.”

---

## Data and Files

- **Course input**: `Homework-Data-2026.xlsx`
- **Output (final)**: `Deere-Homework-Output.xlsx`
- **Charts**: `images/`
- **Run script**: `scripts/run_all.py`
