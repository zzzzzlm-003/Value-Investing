"""
Q5: Asset Value - Product Portfolio and Customer Portfolio
Data: ADBE-Homework-Data-2026-2.xlsx
- Product portfolio: Permanent inventory method, d=0.2
- Customer portfolio: C(t) = (1-a)*C(t-1) + β(t)*i_marketing(t), a=0.1
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_PATH = os.path.join(BASE, "ADBE-Homework-Data-2026-2.xlsx")
IMG_DIR = os.path.join(BASE, "images")
OUTPUT_XLSX = os.path.join(BASE, "ADBE-Homework-Output.xlsx")

A_CHURN = 0.1  # churn rate a(t)
D_AMORT = 0.2  # product portfolio amortization rate


def load_rd():
    """Load R&D expenses from R&D sheet."""
    df = pd.read_excel(EXCEL_PATH, sheet_name="R&D", header=None)
    # rows 3-23: 2005-2025, col 2=year, col 3=R&D ($mn)
    rd = {}
    for i in range(3, 24):
        y = df.iloc[i, 2]
        v = df.iloc[i, 3]
        if pd.notna(y) and pd.notna(v):
            rd[int(y)] = float(v)
    return rd


def load_cc():
    """Load C(t) and i_marketing(t) from CC Accounts & Sales."""
    df = pd.read_excel(EXCEL_PATH, sheet_name="CC Accounts & Sales", header=None)
    # rows 3-16: 2012-2025, col 1=year, col 2=C(t), col 3=i_marketing
    years, c, i_mark = [], [], []
    for i in range(3, 17):
        y = df.iloc[i, 1]
        cv = df.iloc[i, 2]
        iv = df.iloc[i, 3]
        if pd.notna(y) and pd.notna(cv) and pd.notna(iv):
            years.append(int(y))
            c.append(float(cv))
            i_mark.append(float(iv))
    return pd.DataFrame({"year": years, "C": c, "i_marketing": i_mark})


def load_balance_sheet():
    """Load book equity from Balance Sheet."""
    df = pd.read_excel(EXCEL_PATH, sheet_name="Balance Sheet", header=None)
    for i in range(df.shape[0]):
        label = str(df.iloc[i, 0])
        if "Total Shareholders' Equity" in label or "Total Equity" in label:
            val = df.iloc[i, 1]  # NOV '25
            if pd.notna(val):
                return float(val)
    return None


def product_portfolio_value(rd):
    """P_prod = R&D_2025 + 0.8*R&D_2024 + 0.6*R&D_2023 + 0.4*R&D_2022 + 0.2*R&D_2021"""
    p = (
        rd[2025]
        + 0.8 * rd[2024]
        + 0.6 * rd[2023]
        + 0.4 * rd[2022]
        + 0.2 * rd[2021]
    )
    return p


def compute_beta_and_cost(cc_df):
    """β(t) = [C(t) - 0.9*C(t-1)] / i_marketing(t), cost_per_account = 1/β(t)"""
    cc_df = cc_df.sort_values("year").reset_index(drop=True)
    beta_list = []
    cost_list = []
    years_out = []
    for i in range(1, len(cc_df)):
        c_cur = cc_df.iloc[i]["C"]
        c_prev = cc_df.iloc[i - 1]["C"]
        i_m = cc_df.iloc[i]["i_marketing"]
        numerator = c_cur - (1 - A_CHURN) * c_prev
        if i_m > 0 and numerator > 0:
            beta = numerator / i_m
            cost = 1 / beta
            years_out.append(int(cc_df.iloc[i]["year"]))
            beta_list.append(beta)
            cost_list.append(cost)
    return years_out, beta_list, cost_list


def customer_portfolio_value(beta_2025, c_2025):
    """Value = (1/β(2025)) * C(2025) in millions of dollars (C in millions of accounts)"""
    return (1 / beta_2025) * c_2025


def plot_cost_per_customer(years, costs, out_path):
    """Plot cost of acquiring one customer over time, with YoY % line."""
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax1.bar(years, costs, color="steelblue", edgecolor="navy", alpha=0.8, label="Cost per Account ($)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Cost per Account ($)")
    ax1.tick_params(axis="x", rotation=45)

    # YoY % change
    yoy = []
    yoy_years = []
    for i in range(1, len(costs)):
        pct = (costs[i] - costs[i - 1]) / costs[i - 1] * 100 if costs[i - 1] > 0 else 0
        yoy.append(pct)
        yoy_years.append(years[i])
    ax2 = ax1.twinx()
    ax2.plot(yoy_years, yoy, color="coral", marker="o", linewidth=2, markersize=5, label="YoY (%)")
    ax2.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    ax2.set_ylabel("YoY Change (%)")
    ax2.set_ylim(bottom=min(min(yoy) - 10, -5) if yoy else -20, top=max(max(yoy) + 10, 5) if yoy else 20)

    ax1.set_title("Adobe: Cost of Acquiring One Customer/Account (1/β) with YoY")
    fig.legend(loc="upper left", bbox_to_anchor=(0.12, 0.88))
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"  Chart saved: {out_path}")


def main():
    print("=" * 70)
    print("Q5: Asset Value - Product Portfolio & Customer Portfolio")
    print("=" * 70)

    rd = load_rd()
    cc_df = load_cc()
    book_equity = load_balance_sheet()

    # 1. Product Portfolio
    p_prod = product_portfolio_value(rd)
    print("\n【1. Product Portfolio (Permanent Inventory, d=0.2)】")
    print(f"  P_prod = R&D_2025 + 0.8*R&D_2024 + 0.6*R&D_2023 + 0.4*R&D_2022 + 0.2*R&D_2021")
    print(f"  P_prod = {rd[2025]} + 0.8*{rd[2024]} + 0.6*{rd[2023]} + 0.4*{rd[2022]} + 0.2*{rd[2021]}")
    print(f"  P_prod = ${p_prod:,.0f} mn")

    # 2. Customer Portfolio - β and cost per account
    years_b, betas, costs = compute_beta_and_cost(cc_df)
    cc_2025 = cc_df[cc_df["year"] == 2025].iloc[0]
    beta_2025 = betas[-1]  # last year in series is 2025
    cost_2025 = 1 / beta_2025
    v_cust = customer_portfolio_value(beta_2025, cc_2025["C"])

    print("\n【2. Customer Portfolio】")
    print(f"  Model: C(t) = (1-a)*C(t-1) + β(t)*i_marketing(t), a={A_CHURN}")
    print(f"  β(2025) = {beta_2025:.6f}")
    print(f"  Cost per account 1/β(2025) = ${cost_2025:,.0f}")
    print(f"  C(2025) = {cc_2025['C']:.1f} mn accounts")
    print(f"  Customer portfolio value = (1/β)*C = ${v_cust:,.0f} mn")

    # Plot
    plot_path = os.path.join(IMG_DIR, "adbe_cost_per_customer.png")
    plot_cost_per_customer(years_b, costs, plot_path)

    # 3. Asset Value of Equity
    asset_value = book_equity + p_prod + v_cust if book_equity else None
    print("\n【3. Asset Value of Equity】")
    print(f"  Book Equity (FY2025): ${book_equity:,.0f} mn")
    print(f"  + Product Portfolio: ${p_prod:,.0f} mn")
    print(f"  + Customer Portfolio: ${v_cust:,.0f} mn")
    if asset_value:
        print(f"  Asset Value of Equity ≈ ${asset_value:,.0f} mn")

    # Save to Excel
    results_df = pd.DataFrame([
        {"Item": "Product Portfolio ($mn)", "Value": round(p_prod, 1)},
        {"Item": "Customer Portfolio ($mn)", "Value": round(v_cust, 1)},
        {"Item": "β(2025)", "Value": round(beta_2025, 6)},
        {"Item": "Cost per Account ($)", "Value": round(cost_2025, 1)},
        {"Item": "Book Equity ($mn)", "Value": round(book_equity, 1) if book_equity else None},
        {"Item": "Asset Value of Equity ($mn)", "Value": round(asset_value, 1) if asset_value else None},
    ])
    cost_df = pd.DataFrame({"year": years_b, "cost_per_account": [round(c, 1) for c in costs]})

    if os.path.exists(OUTPUT_XLSX):
        with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl", mode="a", if_sheet_exists="replace") as w:
            results_df.to_excel(w, sheet_name="Q5_Asset_Value", index=False)
            cost_df.to_excel(w, sheet_name="Q5_Cost_Per_Customer", index=False)
    else:
        with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl", mode="w") as w:
            results_df.to_excel(w, sheet_name="Q5_Asset_Value", index=False)
            cost_df.to_excel(w, sheet_name="Q5_Cost_Per_Customer", index=False)

    print(f"\nResults saved: {OUTPUT_XLSX}")


if __name__ == "__main__":
    main()
