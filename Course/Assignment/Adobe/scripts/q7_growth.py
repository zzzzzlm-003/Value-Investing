"""
Q7: Growth Analysis
- D/V: Distribution yield (given), discuss 2025 vs 2024
- g: Historical earnings growth rate
- EV/EBIT: Multiple compression, risk analysis
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_PATH = os.path.join(BASE, "ADBE-Homework-Data-2026-2.xlsx")
OUTPUT_XLSX = os.path.join(BASE, "ADBE-Homework-Output.xlsx")
IMG_DIR = os.path.join(BASE, "images")


def load_sales_ebit():
    """Load Sales & EBIT for historical growth."""
    df = pd.read_excel(EXCEL_PATH, sheet_name="Sales & EBIT", header=None)
    rows = []
    for i in range(2, df.shape[0]):
        y = df.iloc[i, 1]
        s = df.iloc[i, 2]
        e = df.iloc[i, 3]
        if pd.notna(y) and pd.notna(e):
            rows.append({"year": int(y), "sales": float(s), "ebit": float(e)})
    return pd.DataFrame(rows).sort_values("year").reset_index(drop=True)


def load_ev_ebit_and_yield():
    """Load EV/EBIT (quarterly) and Distribution yield (yearly)."""
    df = pd.read_excel(EXCEL_PATH, sheet_name="EV to EBIT", header=None)
    ev_ebit = []
    for i in range(2, min(120, df.shape[0])):  # EV/EBIT in col 1,2
        q = df.iloc[i, 1]
        v = df.iloc[i, 2]
        if pd.notna(q) and pd.notna(v):
            ev_ebit.append({"quarter": str(q), "ev_ebit": float(v)})
    yield_data = []
    for i in range(2, 45):  # Distribution yield: col 6=year, col 7=yield
        y = df.iloc[i, 6]
        v = df.iloc[i, 7]
        if pd.notna(y) and pd.notna(v):
            try:
                yield_data.append({"year": int(y), "dist_yield_pct": float(v)})
            except (ValueError, TypeError):
                pass
    return pd.DataFrame(ev_ebit), pd.DataFrame(yield_data)


def cagr(start_val, end_val, years):
    """CAGR = (end/start)^(1/years) - 1"""
    if start_val <= 0 or years <= 0:
        return None
    return (end_val / start_val) ** (1 / years) - 1


def main():
    print("=" * 70)
    print("Q7: Growth Analysis")
    print("=" * 70)

    se = load_sales_ebit()
    ev_df, yield_df = load_ev_ebit_and_yield()

    # 1. Distribution yield
    y_2024 = yield_df[yield_df["year"] == 2024]["dist_yield_pct"].values
    y_2025 = yield_df[yield_df["year"] == 2025]["dist_yield_pct"].values
    dy_2024 = y_2024[0] if len(y_2024) > 0 else None
    dy_2025 = y_2025[0] if len(y_2025) > 0 else None

    print("\n【1. D/V - Distribution Yield】")
    print(f"  2024: {dy_2024:.2f}%")
    print(f"  2025: {dy_2025:.2f}%")
    print("  → 2025 yield jumped vs 2024 (stock price decline + buybacks/dividends)")
    print("  → High yield may reflect management view that stock is undervalued")

    # 2. Historical earnings growth (EBIT)
    ebit_2015 = se[se["year"] == 2015]["ebit"].values[0]
    ebit_2020 = se[se["year"] == 2020]["ebit"].values[0]
    ebit_2025 = se[se["year"] == 2025]["ebit"].values[0]

    g_5y = cagr(ebit_2020, ebit_2025, 5)
    g_10y = cagr(ebit_2015, ebit_2025, 10)

    print("\n【2. g - Historical Earnings Growth】")
    print(f"  EBIT 2015: ${ebit_2015:,.0f} mn, 2020: ${ebit_2020:,.0f} mn, 2025: ${ebit_2025:,.0f} mn")
    print(f"  5-year CAGR (2020→2025): {g_5y*100:.1f}%")
    print(f"  10-year CAGR (2015→2025): {g_10y*100:.1f}%")

    # 3. EV/EBIT multiple
    recent = ev_df.tail(20)
    ev_2025q4 = ev_df.iloc[-1]["ev_ebit"] if len(ev_df) > 0 else None
    ev_2024q4 = ev_df[ev_df["quarter"].str.contains("2024Q4", na=False)]
    if len(ev_2024q4) > 0:
        ev_2024q4_val = ev_2024q4.iloc[0]["ev_ebit"]
    else:
        ev_2024q4_val = ev_df.iloc[-5]["ev_ebit"] if len(ev_df) >= 5 else None

    print("\n【3. EV/EBIT Multiple】")
    print(f"  Recent quarters: {list(recent['quarter'].tail(5).values)}")
    print(f"  2025Q4 EV/EBIT: {ev_2025q4:.2f}x")
    print("  → Multiple compression from ~50x (2020-21) to ~15x (2025)")
    print("  → Risk: AI disruption fears priced in; upside if SaaS holds")

    # Plot EV/EBIT over time (last 60 quarters)
    plot_ev = ev_df.tail(60)
    if len(plot_ev) > 0:
        os.makedirs(IMG_DIR, exist_ok=True)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=False)
        ax1.plot(range(len(plot_ev)), plot_ev["ev_ebit"].values, color="steelblue")
        ax1.set_ylabel("EV/EBIT")
        ax1.set_title("Adobe: EV/EBIT Multiple (Recent Quarters)")
        ax1.tick_params(axis="x", labelbottom=False)
        ax2.bar(yield_df["year"].tail(15), yield_df["dist_yield_pct"].tail(15), color="coral", alpha=0.8)
        ax2.set_xlabel("Year")
        ax2.set_ylabel("Distribution Yield (%)")
        ax2.set_title("Adobe: Distribution Yield")
        plt.tight_layout()
        plt.savefig(os.path.join(IMG_DIR, "adbe_ev_ebit_and_yield.png"), dpi=150)
        plt.close()
        print(f"\n  Chart saved: {IMG_DIR}/adbe_ev_ebit_and_yield.png")

    # Save to Excel
    growth_df = pd.DataFrame([
        {"Item": "Distribution Yield 2024 (%)", "Value": round(dy_2024, 2) if dy_2024 else None},
        {"Item": "Distribution Yield 2025 (%)", "Value": round(dy_2025, 2) if dy_2025 else None},
        {"Item": "EBIT 5yr CAGR (%)", "Value": round(g_5y * 100, 2) if g_5y else None},
        {"Item": "EBIT 10yr CAGR (%)", "Value": round(g_10y * 100, 2) if g_10y else None},
        {"Item": "EV/EBIT 2025Q4", "Value": round(ev_2025q4, 2) if ev_2025q4 else None},
    ])
    if os.path.exists(OUTPUT_XLSX):
        with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl", mode="a", if_sheet_exists="replace") as w:
            growth_df.to_excel(w, sheet_name="Q7_Growth", index=False)
    else:
        with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl", mode="w") as w:
            growth_df.to_excel(w, sheet_name="Q7_Growth", index=False)
    print(f"\nResults saved: {OUTPUT_XLSX}")


if __name__ == "__main__":
    main()
