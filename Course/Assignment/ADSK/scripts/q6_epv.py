"""
Q6: EPV (Earnings Power Value)
Data: ADSK-Data-February-2026-Students.xlsx
- Tax rate 21% (Basic data)
- Adjustments: Growth R&D, Growth marketing
"""
import os
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_PATH = os.path.join(BASE, "ADSK-Data-February-2026-Students.xlsx")
OUTPUT_XLSX = os.path.join(BASE, "Output", "ADSK-Valuation-Output.xlsx")

WACC = 0.09  # typical for SaaS
A_CHURN = 0.05
D_AMORT = 0.2
TAX_RATE = 0.21


def load_basic_data():
    """Load R&D, Marketing, Op. Income, Subscriptions from Basic data."""
    df = pd.read_excel(EXCEL_PATH, sheet_name="Basic data", header=None)
    rd, mkt, opinc, sub = {}, {}, {}, {}
    for i in range(3, 13):
        y = df.iloc[i, 1]
        if pd.notna(y):
            y = int(y)
            rd[y] = float(df.iloc[i, 2]) if pd.notna(df.iloc[i, 2]) else None
            mkt[y] = float(df.iloc[i, 3]) if pd.notna(df.iloc[i, 3]) else None
            opinc[y] = float(df.iloc[i, 4]) if pd.notna(df.iloc[i, 4]) else None
    for i in range(16, 26):
        y = df.iloc[i, 1]
        if pd.notna(y):
            y = int(y)
            v = df.iloc[i, 4]
            sub[y] = float(v) if pd.notna(v) else None
    return rd, mkt, opinc, sub


def compute_beta(c_cur, c_prev, i_m):
    """β = [C(t) - (1-a)*C(t-1)] / i_marketing"""
    numer = c_cur - (1 - A_CHURN) * c_prev
    return numer / i_m if i_m and numer > 0 else None


def product_portfolio_value(rd):
    t, weights = 2026, [1.0, 0.8, 0.6, 0.4, 0.2]
    return sum((rd.get(t - k) or 0) * w for k, w in zip(range(5), weights))


def main():
    print("=" * 70)
    print("Q6: Earnings Power Value (EPV)")
    print("=" * 70)

    rd, mkt, opinc, sub = load_basic_data()
    ebit_2026 = opinc.get(2026)
    rd_2026 = rd.get(2026)
    mkt_2026 = mkt.get(2026)
    c_2026 = sub.get(2026)
    c_2025 = sub.get(2025)
    beta_2026 = compute_beta(c_2026, c_2025, mkt_2026) if c_2025 and mkt_2026 else None

    p_prod = product_portfolio_value(rd)
    maint_rd = p_prod * D_AMORT
    growth_rd = max(0, (rd_2026 or 0) - maint_rd)

    maint_mkt = (A_CHURN * c_2026) / beta_2026 if beta_2026 and c_2026 else 0
    growth_mkt = max(0, (mkt_2026 or 0) - maint_mkt)

    adj_ebit = (ebit_2026 or 0) + growth_rd + growth_mkt
    nopat = adj_ebit * (1 - TAX_RATE)
    epv_op = nopat / WACC

    # Cash and debt from Basic data
    df = pd.read_excel(EXCEL_PATH, sheet_name="Basic data", header=None)
    cash_2026 = float(df.iloc[12, 8]) if pd.notna(df.iloc[12, 8]) else 0
    lt_debt = float(df.iloc[12, 6]) if pd.notna(df.iloc[12, 6]) else 0
    st_debt = float(df.iloc[12, 7]) if pd.notna(df.iloc[12, 7]) else 0
    total_debt = lt_debt + (st_debt or 0)

    epv_equity = epv_op + cash_2026 - total_debt

    print("\n【1. Base EBIT】")
    print(f"  EBIT (FY2026): ${ebit_2026:,.0f} mn")

    print("\n【2. Adjustments】")
    print(f"  Maintenance R&D = P_prod × 0.2 = {p_prod:,.0f} × 0.2 = ${maint_rd:,.0f} mn")
    print(f"  Growth R&D = {rd_2026:,.0f} - {maint_rd:,.0f} = ${growth_rd:,.0f} mn")
    print(f"  Maintenance marketing = a×C/β = ${maint_mkt:,.0f} mn")
    print(f"  Growth marketing = {mkt_2026:,.0f} - {maint_mkt:,.0f} = ${growth_mkt:,.0f} mn")

    print("\n【3. EPV】")
    print(f"  Adj EBIT = ${adj_ebit:,.0f} mn")
    print(f"  NOPAT (1-21%) = ${nopat:,.0f} mn")
    print(f"  EPV (op) = NOPAT / WACC = {nopat:,.0f} / {WACC} = ${epv_op:,.0f} mn")
    print(f"  + Cash ${cash_2026:,.0f} - Debt ${total_debt:,.0f}")
    print(f"  EPV Equity ≈ ${epv_equity:,.0f} mn")

    epv_df = pd.DataFrame([
        {"Item": "EBIT ($mn)", "Value": round(ebit_2026, 1)},
        {"Item": "Growth R&D ($mn)", "Value": round(growth_rd, 1)},
        {"Item": "Growth Marketing ($mn)", "Value": round(growth_mkt, 1)},
        {"Item": "Adjusted EBIT ($mn)", "Value": round(adj_ebit, 1)},
        {"Item": "NOPAT ($mn)", "Value": round(nopat, 1)},
        {"Item": "EPV Equity ($mn)", "Value": round(epv_equity, 1)},
    ])

    with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl", mode="a", if_sheet_exists="replace") as w:
        epv_df.to_excel(w, sheet_name="Q6_EPV", index=False)

    print(f"\nSaved: {OUTPUT_XLSX}")


if __name__ == "__main__":
    main()
