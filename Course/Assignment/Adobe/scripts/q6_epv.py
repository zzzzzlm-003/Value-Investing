"""
Q6: EPV (Earnings Power Value)
Adjustments: (1) Growth R&D, (2) Growth marketing (customer acquisition)
Maintenance marketing: i_marketing_maintenance = a * C(t) / β(t)
"""
import os
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_PATH = os.path.join(BASE, "ADBE-Homework-Data-2026-2.xlsx")
OUTPUT_XLSX = os.path.join(BASE, "ADBE-Homework-Output.xlsx")

WACC = 0.07
A_CHURN = 0.1
D_AMORT = 0.2


def load_income_statement():
    """Extract EBIT, Tax Provision, Income Before Tax for FY2025 (col 1 = NOV '25)."""
    df = pd.read_excel(EXCEL_PATH, sheet_name="Income Statement", header=None)
    # Row labels in col 0, values in col 1 (NOV '25)
    out = {}
    for i in range(df.shape[0]):
        label = str(df.iloc[i, 0]).strip()
        val = df.iloc[i, 1]
        if "EBIT (Operating Income)" in label:
            out["ebit"] = float(val) if pd.notna(val) else None
        if "Pretax Income" in label or "Income Before Tax" in label:
            out["income_before_tax"] = float(val) if pd.notna(val) else None
        if label == "Income Taxes" or "Tax Provision" in label:
            out["tax_provision"] = float(val) if pd.notna(val) else None
    return out


def load_rd():
    df = pd.read_excel(EXCEL_PATH, sheet_name="R&D", header=None)
    for i in range(3, 24):
        if df.iloc[i, 2] == 2025:
            return float(df.iloc[i, 3])
    return None


def load_cc_and_beta():
    """Load C(2025), i_marketing(2025), and compute β(2025)."""
    df = pd.read_excel(EXCEL_PATH, sheet_name="CC Accounts & Sales", header=None)
    rows = []
    for i in range(3, 17):
        y = df.iloc[i, 1]
        c = df.iloc[i, 2]
        im = df.iloc[i, 3]
        if pd.notna(y) and pd.notna(c) and pd.notna(im):
            rows.append({"year": int(y), "C": float(c), "i_marketing": float(im)})
    df2 = pd.DataFrame(rows).sort_values("year").reset_index(drop=True)
    # β(2025) from C(2025) - 0.9*C(2024) over i_marketing(2025)
    row_2025 = df2[df2["year"] == 2025].iloc[0]
    row_2024 = df2[df2["year"] == 2024].iloc[0]
    numer = row_2025["C"] - (1 - A_CHURN) * row_2024["C"]
    beta = numer / row_2025["i_marketing"] if row_2025["i_marketing"] > 0 else None
    return {
        "C_2025": row_2025["C"],
        "i_marketing_2025": row_2025["i_marketing"],
        "beta_2025": beta,
    }


def product_portfolio_value(rd):
    df = pd.read_excel(EXCEL_PATH, sheet_name="R&D", header=None)
    rd_dict = {}
    for i in range(3, 24):
        y = df.iloc[i, 2]
        v = df.iloc[i, 3]
        if pd.notna(y) and pd.notna(v):
            rd_dict[int(y)] = float(v)
    return (
        rd_dict[2025]
        + 0.8 * rd_dict[2024]
        + 0.6 * rd_dict[2023]
        + 0.4 * rd_dict[2022]
        + 0.2 * rd_dict[2021]
    )


def main():
    print("=" * 70)
    print("Q6: Earnings Power Value (EPV)")
    print("=" * 70)

    inc = load_income_statement()
    rd_2025 = load_rd()
    cc = load_cc_and_beta()
    p_prod = product_portfolio_value(rd_2025)

    ebit = inc["ebit"]
    tax_prov = inc.get("tax_provision")
    income_bt = inc.get("income_before_tax")
    if income_bt and income_bt != 0:
        tax_rate = tax_prov / income_bt if tax_prov else 0.21
    else:
        tax_rate = 0.21

    # 1. Product portfolio adjustment
    maint_rd = p_prod * D_AMORT  # d=0.2
    growth_rd = max(0, rd_2025 - maint_rd)

    # 2. Customer portfolio adjustment
    maint_marketing = (A_CHURN * cc["C_2025"]) / cc["beta_2025"]
    growth_marketing = max(0, cc["i_marketing_2025"] - maint_marketing)

    adjusted_ebit = ebit + growth_rd + growth_marketing
    sustainable_nopat = adjusted_ebit * (1 - tax_rate)
    epv = sustainable_nopat / WACC

    print("\n【1. Base EBIT】")
    print(f"  EBIT (FY2025): ${ebit:,.0f} mn")

    print("\n【2. Growth Expense Adjustments】")
    print(f"  Product portfolio: Maintenance R&D = P_prod × 0.2 = {p_prod:,.0f} × 0.2 = ${maint_rd:,.0f} mn")
    print(f"  Growth R&D = R&D_2025 - Maintenance = {rd_2025:,.0f} - {maint_rd:,.0f} = ${growth_rd:,.0f} mn")
    print(f"  Customer portfolio: Maintenance marketing = a×C(2025)/β(2025) = {A_CHURN}×{cc['C_2025']}/{cc['beta_2025']:.6f} = ${maint_marketing:,.0f} mn")
    print(f"  Growth marketing = i_marketing - Maintenance = {cc['i_marketing_2025']:,.0f} - {maint_marketing:,.0f} = ${growth_marketing:,.0f} mn")

    print("\n【3. Adjusted Operating Income】")
    print(f"  Adj EBIT = EBIT + Growth R&D + Growth marketing")
    print(f"  Adj EBIT = {ebit:,.0f} + {growth_rd:,.0f} + {growth_marketing:,.0f} = ${adjusted_ebit:,.0f} mn")

    print("\n【4. Sustainable NOPAT & EPV】")
    print(f"  Tax rate: {tax_rate*100:.1f}%")
    print(f"  Sustainable NOPAT = Adj EBIT × (1-t) = {adjusted_ebit:,.0f} × (1-{tax_rate:.3f}) = ${sustainable_nopat:,.0f} mn")
    print(f"  WACC = {WACC*100:.0f}%")
    print(f"  EPV = NOPAT / WACC = {sustainable_nopat:,.0f} / {WACC} = ${epv:,.0f} mn")

    # Save
    epv_df = pd.DataFrame([
        {"Item": "EBIT ($mn)", "Value": round(ebit, 1)},
        {"Item": "Growth R&D ($mn)", "Value": round(growth_rd, 1)},
        {"Item": "Growth Marketing ($mn)", "Value": round(growth_marketing, 1)},
        {"Item": "Adjusted EBIT ($mn)", "Value": round(adjusted_ebit, 1)},
        {"Item": "Tax Rate", "Value": round(tax_rate, 4)},
        {"Item": "Sustainable NOPAT ($mn)", "Value": round(sustainable_nopat, 1)},
        {"Item": "WACC", "Value": WACC},
        {"Item": "EPV ($mn)", "Value": round(epv, 1)},
    ])
    if os.path.exists(OUTPUT_XLSX):
        with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl", mode="a", if_sheet_exists="replace") as w:
            epv_df.to_excel(w, sheet_name="Q6_EPV", index=False)
    else:
        with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl", mode="w") as w:
            epv_df.to_excel(w, sheet_name="Q6_EPV", index=False)
    print(f"\nResults saved: {OUTPUT_XLSX}")


if __name__ == "__main__":
    main()
