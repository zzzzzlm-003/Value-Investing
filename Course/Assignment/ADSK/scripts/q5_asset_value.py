"""
Q5: Asset Value - Product Portfolio and Customer Portfolio
Data: ADSK-Data-February-2026-Students.xlsx, Basic data sheet
- Product portfolio: Permanent inventory method, d=0.2
- Customer portfolio: C(t) = (1-a)*C(t-1) + β(t)*i_marketing(t), a=0.05 (churn 5%)
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_PATH = os.path.join(BASE, "ADSK-Data-February-2026-Students.xlsx")
IMG_DIR = os.path.join(BASE, "images")
OUTPUT_XLSX = os.path.join(BASE, "Output", "ADSK-Valuation-Output.xlsx")

A_CHURN = 0.05  # churn rate 5% per assignment
D_AMORT = 0.2  # product portfolio amortization rate


def load_basic_data():
    """Load R&D, Marketing, Subscriptions from Basic data sheet."""
    df = pd.read_excel(EXCEL_PATH, sheet_name="Basic data", header=None)
    # Block 1: rows 3-12, col 1=year, 2=R&D, 3=Marketing and sales
    rd, mkt, years1 = {}, {}, []
    for i in range(3, 13):
        y = df.iloc[i, 1]
        if pd.notna(y):
            y = int(y)
            years1.append(y)
            rd[y] = float(df.iloc[i, 2]) if pd.notna(df.iloc[i, 2]) else None
            mkt[y] = float(df.iloc[i, 3]) if pd.notna(df.iloc[i, 3]) else None
    # Block 2: rows 16-25, col 1=year, 4=Subscriptions (millions)
    sub = {}
    for i in range(16, 26):
        y = df.iloc[i, 1]
        if pd.notna(y):
            y = int(y)
            v = df.iloc[i, 4]
            sub[y] = float(v) if pd.notna(v) else None
    return rd, mkt, sub


def load_balance_sheet():
    """Load book equity from Balance Sheet. JAN '26 = col 1."""
    df = pd.read_excel(EXCEL_PATH, sheet_name="Balance Sheet", header=None)
    for i in range(df.shape[0]):
        label = str(df.iloc[i, 0])
        if "Total Shareholders" in label or "Total Equity" in label or " stockholders" in label.lower():
            val = df.iloc[i, 1]
            if pd.notna(val):
                try:
                    return float(val)
                except (TypeError, ValueError):
                    pass
    return None


def product_portfolio_value(rd):
    """P_prod = R&D_t + 0.8*R&D_{t-1} + 0.6*R&D_{t-2} + 0.4*R&D_{t-3} + 0.2*R&D_{t-4}"""
    t = 2026
    v = [rd.get(t - k) for k in range(5)]
    weights = [1.0, 0.8, 0.6, 0.4, 0.2]
    p = sum((x or 0) * w for x, w in zip(v, weights))
    return p


def compute_beta_and_cost(rd, mkt, sub):
    """β(t) = [C(t) - (1-a)*C(t-1)] / i_marketing(t), CAC = 1/β"""
    years = sorted([y for y in sub if sub[y] is not None and mkt.get(y)])
    years = [y for y in years if y > min(years)]  # need t-1
    beta_list, cost_list, years_out = [], [], []
    for y in years:
        c_cur = sub[y]
        c_prev = sub.get(y - 1)
        i_m = mkt.get(y)
        if c_prev is not None and i_m and i_m > 0:
            numer = c_cur - (1 - A_CHURN) * c_prev
            if numer > 0:
                beta = numer / i_m
                cost = 1 / beta
                years_out.append(y)
                beta_list.append(beta)
                cost_list.append(cost)
    return years_out, beta_list, cost_list


def customer_portfolio_value_3yr_avg(costs, c_latest):
    """Use average of last 3 years CAC × C(latest) per assignment."""
    avg_cac = sum(costs[-3:]) / 3 if len(costs) >= 3 else costs[-1]
    return avg_cac * c_latest


def plot_cost_per_customer(years, costs, out_path):
    """Plot cost of acquiring one customer over time."""
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax1.bar(years, costs, color="steelblue", edgecolor="navy", alpha=0.8, label="CAC ($)")
    ax1.set_xlabel("Fiscal Year")
    ax1.set_ylabel("Cost per Subscription ($)")
    ax1.tick_params(axis="x", rotation=45)
    ax1.set_title("ADSK: Cost of Acquiring One Customer (churn=5%)")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"  Chart saved: {out_path}")


def main():
    print("=" * 70)
    print("Q5: Asset Value - Product Portfolio & Customer Portfolio")
    print("=" * 70)

    rd, mkt, sub = load_basic_data()
    book_equity = load_balance_sheet()

    # 1. Product Portfolio
    p_prod = product_portfolio_value(rd)
    print("\n【1. Product Portfolio (Permanent Inventory, d=0.2)】")
    print(f"  P_prod = R&D_2026 + 0.8*R&D_2025 + ... + 0.2*R&D_2022")
    print(f"  P_prod = ${p_prod:,.0f} mn")

    # 2. Customer Portfolio
    years_b, betas, costs = compute_beta_and_cost(rd, mkt, sub)
    c_2026 = sub.get(2026, sub.get(2025))
    v_cust = customer_portfolio_value_3yr_avg(costs, c_2026)
    cac_3yr_avg = sum(costs[-3:]) / 3 if len(costs) >= 3 else costs[-1]

    print("\n【2. Customer Portfolio】")
    print(f"  Model: C(t) = (1-a)*C(t-1) + β(t)*i_marketing(t), a={A_CHURN}")
    print(f"  Last 3 years CAC: {[round(c,1) for c in costs[-3:]]}")
    print(f"  3-year average CAC: ${cac_3yr_avg:,.0f}")
    print(f"  C(2026) = {c_2026:.2f} mn subscriptions")
    print(f"  Customer portfolio value = Avg CAC × C = ${v_cust:,.0f} mn")

    plot_path = os.path.join(IMG_DIR, "adsk_cost_per_customer.png")
    plot_cost_per_customer(years_b, costs, plot_path)

    # 3. Asset Value of Equity
    asset_value = (book_equity or 0) + p_prod + v_cust
    print("\n【3. Asset Value of Equity】")
    print(f"  Book Equity (FY2026): ${book_equity:,.0f} mn")
    print(f"  + Product Portfolio: ${p_prod:,.0f} mn")
    print(f"  + Customer Portfolio: ${v_cust:,.0f} mn")
    print(f"  Asset Value of Equity ≈ ${asset_value:,.0f} mn")

    # Save
    os.makedirs(os.path.dirname(OUTPUT_XLSX), exist_ok=True)
    results_df = pd.DataFrame([
        {"Item": "Product Portfolio ($mn)", "Value": round(p_prod, 1)},
        {"Item": "Customer Portfolio ($mn)", "Value": round(v_cust, 1)},
        {"Item": "3-yr Avg CAC ($)", "Value": round(cac_3yr_avg, 1)},
        {"Item": "C(2026) (mn subs)", "Value": c_2026},
        {"Item": "Book Equity ($mn)", "Value": round(book_equity, 1) if book_equity else None},
        {"Item": "Asset Value of Equity ($mn)", "Value": round(asset_value, 1)},
    ])
    cost_df = pd.DataFrame({"year": years_b, "cost_per_account": [round(c, 1) for c in costs]})

    with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl", mode="w") as w:
        results_df.to_excel(w, sheet_name="Q5_Asset_Value", index=False)
        cost_df.to_excel(w, sheet_name="Q5_Cost_Per_Customer", index=False)

    print(f"\nResults saved: {OUTPUT_XLSX}")


if __name__ == "__main__":
    main()
