"""
Question 6 & 7: Asset Value (product portfolio) and Earnings Power Value.
Uses data from Deere Annual Report Supplemental Consolidating Data.
"""
import os
import pandas as pd

# R&D from Equipment Operations ( Supplemental Consolidating Data + Selected Financial Data)
RND = {
    2025: 2311, 2024: 2290, 2023: 2177, 2022: 1912, 2021: 1587,
    2020: 1644, 2019: 1783, 2018: 1658, 2017: 1373, 2016: 1394,
}

# Equipment Operations Income Statement FY2025 (from Supplemental Consolidating Data)
NET_SALES = 38917
COST_OF_SALES = 28190
RND_2025 = 2311
SAG = 3856
INTEREST_EXPENSE = 372
INTEREST_TO_FS = 414
OTHER_OP = -29
INCOME_BEFORE_TAX = 5145
TAX_PROVISION = 1020
INCOME_AFTER_TAX = 4125

WACC = 0.07
BRAND_VALUE = 8800  # Interbrand 2025, $mn

def product_portfolio_value():
    """Perpetual inventory: P = R&D_t + 0.8*R&D_t-1 + 0.6*R&D_t-2 + 0.4*R&D_t-3 + 0.2*R&D_t-4"""
    p = RND[2025] + 0.8*RND[2024] + 0.6*RND[2023] + 0.4*RND[2022] + 0.2*RND[2021]
    return p

def epv_sustainable_nopat():
    """EPV: follow Lecture 3 / markdown assumptions."""
    # 1) Operating income (EBIT)
    ebit = INCOME_BEFORE_TAX + INTEREST_EXPENSE + INTEREST_TO_FS

    # 2) Growth expense adjustments (intangibles)
    p_prod = product_portfolio_value()                  # product portfolio, $mn
    maint_rd = p_prod / 5                               # 5-year linear amortization
    growth_rd = max(0, RND_2025 - maint_rd)

    marketing_proxy = 0.35 * SAG                        # marketing proxy from SG&A
    brand_maint = BRAND_VALUE / 15                      # 15-year brand amortization
    growth_brand = max(0, marketing_proxy - brand_maint)

    adjusted_op_income = ebit + growth_rd + growth_brand
    tax_rate = TAX_PROVISION / INCOME_BEFORE_TAX if INCOME_BEFORE_TAX else 0.21
    sustainable_nopat = adjusted_op_income * (1 - tax_rate)
    return sustainable_nopat

def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    p_prod = product_portfolio_value()
    print(f"--- Product Portfolio Value (Perpetual Inventory) ---")
    print(f"P_prod = R&D_2025 + 0.8*R&D_2024 + 0.6*R&D_2023 + 0.4*R&D_2022 + 0.2*R&D_2021")
    print(f"P_prod = {RND[2025]} + 0.8*{RND[2024]} + 0.6*{RND[2023]} + 0.4*{RND[2022]} + 0.2*{RND[2021]}")
    print(f"P_prod = ${p_prod:,.0f}M")
    
    nopat = epv_sustainable_nopat()
    epv = nopat / WACC
    print(f"\n--- Earnings Power Value (Equipment Operations) ---")
    print(f"Sustainable NOPAT: ${nopat:,.0f}M")
    print(f"WACC: {WACC*100}%")
    print(f"EPV = NOPAT / WACC = {nopat:,.0f} / 0.07 = ${epv:,.0f}M")
    
    out_path = os.path.join(base, "epv_results.txt")
    with open(out_path, "w") as f:
        f.write(f"Product Portfolio Value: ${p_prod:,.0f}M\n")
        f.write(f"Sustainable NOPAT: ${nopat:,.0f}M\n")
        f.write(f"EPV: ${epv:,.0f}M\n")
    print(f"\nResults saved: {out_path}")

    out_xlsx = os.path.join(base, "Deere-Homework-Output.xlsx")
    epv_df = pd.DataFrame([
        {"Item": "Product Portfolio Value ($mn)", "Value": round(p_prod, 1)},
        {"Item": "Sustainable NOPAT ($mn)", "Value": round(nopat, 1)},
        {"Item": "WACC", "Value": WACC},
        {"Item": "EPV ($mn)", "Value": round(epv, 1)},
    ])
    if os.path.exists(out_xlsx):
        with pd.ExcelWriter(out_xlsx, engine="openpyxl", mode="a", if_sheet_exists="replace") as w:
            epv_df.to_excel(w, sheet_name="EPV_Summary", index=False)
    else:
        with pd.ExcelWriter(out_xlsx, engine="openpyxl", mode="w") as w:
            epv_df.to_excel(w, sheet_name="EPV_Summary", index=False)
    print(f"EPV sheet updated: {out_xlsx}")

if __name__ == "__main__":
    main()
