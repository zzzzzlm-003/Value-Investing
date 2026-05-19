"""
Q7: Growth Analysis
- Distribution yield = Share repurchases / EV
- g from historical earnings (pandemic onward)
- Marginal ROIC FY2022-FY2026
- g from marginal ROIC
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_PATH = os.path.join(BASE, "ADSK-Data-February-2026-Students.xlsx")
OUTPUT_XLSX = os.path.join(BASE, "Output", "ADSK-Valuation-Output.xlsx")
IMG_DIR = os.path.join(BASE, "images")

A_CHURN = 0.05
D_AMORT = 0.2
TAX_RATE = 0.21


def load_basic_data():
    df = pd.read_excel(EXCEL_PATH, sheet_name="Basic data", header=None)
    data = {}
    for i in range(3, 13):
        y = int(df.iloc[i, 1]) if pd.notna(df.iloc[i, 1]) else None
        if y:
            data[y] = {
                "rd": float(df.iloc[i, 2]) if pd.notna(df.iloc[i, 2]) else 0,
                "mkt": float(df.iloc[i, 3]) if pd.notna(df.iloc[i, 3]) else 0,
                "opinc": float(df.iloc[i, 4]) if pd.notna(df.iloc[i, 4]) else 0,
                "rev": float(df.iloc[i, 5]) if pd.notna(df.iloc[i, 5]) else 0,
                "debt": float(df.iloc[i, 6]) if pd.notna(df.iloc[i, 6]) else 0,
                "st_debt": float(df.iloc[i, 7]) if pd.notna(df.iloc[i, 7]) else 0,
                "cash": float(df.iloc[i, 8]) if pd.notna(df.iloc[i, 8]) else 0,
                "repurch": float(df.iloc[i, 9]) if pd.notna(df.iloc[i, 9]) else 0,
            }
    for i in range(16, 26):
        y = int(df.iloc[i, 1]) if pd.notna(df.iloc[i, 1]) else None
        if y and y in data:
            data[y]["sub"] = float(df.iloc[i, 4]) if pd.notna(df.iloc[i, 4]) else 0
        elif y:
            data[y] = {"sub": float(df.iloc[i, 4]) if pd.notna(df.iloc[i, 4]) else 0}
    return data


def product_portfolio(rd_dict, t):
    weights = [1.0, 0.8, 0.6, 0.4, 0.2]
    return sum((rd_dict.get(t - k, 0) or 0) * w for k, w in zip(range(5), weights))


def beta_t(c, c_prev, i_m):
    numer = c - (1 - A_CHURN) * c_prev
    return numer / i_m if i_m and numer > 0 else None


def main():
    print("=" * 70)
    print("Q7: Growth Analysis")
    print("=" * 70)

    d = load_basic_data()
    years = sorted([y for y in d if "opinc" in d[y] and d[y]["opinc"]])

    # 1. Distribution yield = Share repurchases / EV
    # EV = Market cap + Debt - Cash. Use shares * price for market cap
    shares_2026 = 213  # million from 10-K
    price_2026 = 257  # Basic data row 25 col 3
    mcap = shares_2026 * price_2026
    row_2026 = d[2026]
    ev = mcap + row_2026["debt"] + (row_2026.get("st_debt") or 0) - row_2026["cash"]
    repurch = row_2026["repurch"]
    dist_yield = repurch / ev * 100

    print("\n【1. Distribution Yield D/V】")
    print(f"  Share repurchases FY2026: ${repurch:,.0f} mn")
    print(f"  EV ≈ Market Cap + Debt - Cash = {mcap:,.0f} + {row_2026['debt']+row_2026.get('st_debt',0):,.0f} - {row_2026['cash']:,.0f} = ${ev:,.0f} mn")
    print(f"  Distribution yield = Repurchases / EV = {repurch:,.0f} / {ev:,.0f} = {dist_yield:.2f}%")

    # 2. g from historical earnings (pandemic = 2020+)
    op_2020 = d[2020]["opinc"]
    op_2026 = d[2026]["opinc"]
    g_hist = (op_2026 / op_2020) ** (1 / 6) - 1

    print("\n【2. g - Historical Earnings Growth (Pandemic)】")
    print(f"  EBIT 2020: ${op_2020:,.0f} mn, 2026: ${op_2026:,.0f} mn")
    print(f"  6-year CAGR = ({op_2026}/{op_2020})^(1/6) - 1 = {g_hist*100:.1f}%")

    # 3. Marginal ROIC FY2022-FY2026
    # Adj NOPAT, Growth Capex (cust + prod)
    rd_d = {y: d[y]["rd"] for y in d if "rd" in d[y]}
    growth_capex = []
    adj_nopat = []

    for y in range(2022, 2027):
        if y not in d:
            continue
        p_prod = product_portfolio(rd_d, y)
        maint_rd = p_prod * D_AMORT
        gr_rd = max(0, d[y]["rd"] - maint_rd)

        c_cur = d[y].get("sub")
        c_prev = d.get(y - 1, {}).get("sub")
        beta = beta_t(c_cur, c_prev, d[y]["mkt"]) if c_prev else None
        maint_mkt = (A_CHURN * c_cur) / beta if beta and c_cur else 0
        gr_mkt = max(0, d[y]["mkt"] - maint_mkt)

        adj_ebit = d[y]["opinc"] + gr_rd + gr_mkt
        nopat = adj_ebit * (1 - TAX_RATE)
        adj_nopat.append((y, nopat))
        growth_capex.append(gr_rd * (1 - TAX_RATE) + gr_mkt * (1 - TAX_RATE))

    delta_nopat = adj_nopat[-1][1] - adj_nopat[0][1]
    sum_gc = sum(growth_capex)
    marginal_roic = delta_nopat / sum_gc if sum_gc > 0 else 0

    print("\n【3. Marginal ROIC FY2022-FY2026】")
    print(f"  Δ Adj NOPAT = {adj_nopat[-1][1]:,.0f} - {adj_nopat[0][1]:,.0f} = ${delta_nopat:,.0f} mn")
    print(f"  Σ Growth Capex (after-tax) = ${sum_gc:,.0f} mn")
    print(f"  Marginal ROIC = {marginal_roic*100:.1f}%")

    # g from marginal ROIC: g = plowback * ROIC
    # plowback = Growth Capex / NOPAT (approx)
    nopat_2026 = adj_nopat[-1][1]
    plowback = sum_gc / (nopat_2026 * 5) if nopat_2026 else 0  # avg over 5 years
    g_roic = plowback * marginal_roic
    # Simpler: plowback = 1 - payout, payout = repurchases / NOPAT
    payout = repurch / nopat_2026 if nopat_2026 else 0
    plowback2 = 1 - min(payout, 1)
    g_roic2 = plowback2 * marginal_roic

    print("\n【4. g from Marginal ROIC】")
    print(f"  Plowback ≈ 1 - (Repurch/NOPAT) = 1 - {repurch:.0f}/{nopat_2026:.0f} = {plowback2:.2f}")
    print(f"  g = Plowback × ROIC = {plowback2:.2f} × {marginal_roic*100:.1f}% = {g_roic2*100:.1f}%")

    # EV/EBIT
    ev_ebit = ev / op_2026 if op_2026 else 0
    print("\n【5. EV/EBIT】")
    print(f"  EV/EBIT = {ev:,.0f} / {op_2026:,.0f} = {ev_ebit:.1f}x")

    # Save
    results = pd.DataFrame([
        {"Item": "Distribution Yield (%)", "Value": round(dist_yield, 2)},
        {"Item": "Historical g 6yr CAGR (%)", "Value": round(g_hist * 100, 2)},
        {"Item": "Marginal ROIC (%)", "Value": round(marginal_roic * 100, 2)},
        {"Item": "g from ROIC (%)", "Value": round(g_roic2 * 100, 2)},
        {"Item": "EV/EBIT", "Value": round(ev_ebit, 1)},
    ])
    with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl", mode="a", if_sheet_exists="replace") as w:
        results.to_excel(w, sheet_name="Q7_Growth", index=False)

    print(f"\nSaved: {OUTPUT_XLSX}")


if __name__ == "__main__":
    main()
