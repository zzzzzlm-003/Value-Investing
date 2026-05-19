"""
Nike Homework Q1-Q2: Industry revenue shares and operating margins.
- Q1: Plot revenue share of each company (Nike, Adidas, Puma, Under Armour, Lululemon, Asics) from 2014
- Q2: Plot operating margins of these companies
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_PATH = os.path.join(BASE, "NKE-Homework-2026-1.xlsx")
IMG_DIR = os.path.join(BASE, "images")
OUTPUT_CSV = os.path.join(BASE, "Output", "nke_industry_q1_q2.csv")

COMPANIES = ["Nike", "Adidas", "Puma", "Under Armour", "Lululemon", "Asics"]
COMPANIES_OP = ["Nike", "Adidas", "Puma", "Under Armour", "Lululemon"]  # Asics has no Op Income
COLORS = ["#111111", "#0066cc", "#d5002b", "#ff6600", "#2e5090", "#999999"]


def load_industry(df_raw):
    """Parse Industry sheet: revenues and operating income by year."""
    # Revenue: rows 5-24 (0-indexed), year in col 1, Nike col 2, Adidas col 3, Puma col 4, UA col 5, LULU col 6, Asics col 7
    # FX: col 10 = JPY/USD, col 11 = USD/EUR (dollars per euro)
    data = []
    for i in range(20):  # 2006-2025
        row_idx = 5 + i
        year = df_raw.iloc[row_idx, 1]
        if pd.isna(year):
            continue
        year = int(year)
        jpy_usd = df_raw.iloc[row_idx, 10]
        usd_eur = df_raw.iloc[row_idx, 11]
        if pd.isna(jpy_usd):
            jpy_usd = 120  # fallback
        if pd.isna(usd_eur):
            usd_eur = 1.2

        def safe_float(x):
            if pd.isna(x):
                return np.nan
            try:
                return float(x)
            except (TypeError, ValueError):
                return np.nan

        nike_usd = safe_float(df_raw.iloc[row_idx, 2])
        adidas_eur = safe_float(df_raw.iloc[row_idx, 3])
        puma_eur = safe_float(df_raw.iloc[row_idx, 4])
        ua_usd = safe_float(df_raw.iloc[row_idx, 5])
        lulu_usd = safe_float(df_raw.iloc[row_idx, 6])
        asics_jpy = safe_float(df_raw.iloc[row_idx, 7])

        adidas_usd = adidas_eur * usd_eur if not np.isnan(adidas_eur) else np.nan
        puma_usd = puma_eur * usd_eur if not np.isnan(puma_eur) else np.nan
        asics_usd = asics_jpy / jpy_usd if not np.isnan(asics_jpy) else np.nan  # JPY bn -> USD bn

        data.append({
            "Year": year,
            "Nike": nike_usd,
            "Adidas": adidas_usd,
            "Puma": puma_usd,
            "Under Armour": ua_usd,
            "Lululemon": lulu_usd,
            "Asics": asics_usd,
        })
    rev_df = pd.DataFrame(data)

    # Operating Income: rows 29-48
    op_data = []
    for i in range(20):
        row_idx = 29 + i
        year = df_raw.iloc[row_idx, 1]
        if pd.isna(year):
            continue
        year = int(year)
        jpy_usd = df_raw.iloc[5 + i, 10]
        usd_eur = df_raw.iloc[5 + i, 11]
        if pd.isna(jpy_usd):
            jpy_usd = 120
        if pd.isna(usd_eur):
            usd_eur = 1.2

        def safe_float(x):
            if pd.isna(x):
                return np.nan
            try:
                return float(x)
            except (TypeError, ValueError):
                return np.nan

        nike = safe_float(df_raw.iloc[row_idx, 2])
        adidas_eur = safe_float(df_raw.iloc[row_idx, 3])
        puma_eur = safe_float(df_raw.iloc[row_idx, 4])
        ua = safe_float(df_raw.iloc[row_idx, 5])
        lulu = safe_float(df_raw.iloc[row_idx, 6])
        adidas = adidas_eur * usd_eur if not np.isnan(adidas_eur) else np.nan
        puma = puma_eur * usd_eur if not np.isnan(puma_eur) else np.nan

        op_data.append({
            "Year": year,
            "Nike": nike,
            "Adidas": adidas,
            "Puma": puma,
            "Under Armour": ua,
            "Lululemon": lulu,
        })
    op_df = pd.DataFrame(op_data)

    return rev_df, op_df


def calc_shares_and_margins(rev_df, op_df):
    """Compute revenue shares (from 2014) and operating margins."""
    rev_cols = ["Nike", "Adidas", "Puma", "Under Armour", "Lululemon", "Asics"]
    op_cols = ["Nike", "Adidas", "Puma", "Under Armour", "Lululemon"]

    df = rev_df.merge(op_df, on="Year", suffixes=("_rev", "_op"))
    out = df[["Year"]].copy()
    for c in rev_cols:
        out[c] = df[f"{c}_rev"] if c != "Asics" else df["Asics"]
    for c in op_cols:
        out[f"{c}_margin"] = (df[f"{c}_op"] / df[f"{c}_rev"] * 100).round(1)

    df_14 = out[out["Year"] >= 2014].copy()
    total = df_14[rev_cols].sum(axis=1)
    for c in rev_cols:
        df_14[f"{c}_share"] = (df_14[c] / total * 100).round(1)
    out = out.merge(df_14[["Year"] + [f"{c}_share" for c in rev_cols]], on="Year", how="left")
    return out, df_14


def plot_revenue_shares(df_14, out_path):
    """Stacked bar chart of revenue shares from 2014."""
    years = df_14["Year"].astype(int).values
    share_cols = [f"{c}_share" for c in COMPANIES]
    fig, ax = plt.subplots(figsize=(12, 6))
    bottom = np.zeros(len(years))
    for i, (comp, col) in enumerate(zip(COMPANIES, share_cols)):
        vals = df_14[col].fillna(0).values
        ax.bar(years, vals, bottom=bottom, label=comp, color=COLORS[i])
        bottom = bottom + vals
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue Share (%)")
    ax.set_title("Athletic Apparel & Footwear Industry: Revenue Shares (2014–2025)\nSix companies; Asics data from 2014")
    ax.legend(loc="upper right", ncol=2)
    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45)
    ax.set_ylim(0, 100)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved: {out_path}")


def plot_operating_margins(df, out_path):
    """Line chart of operating margins for 5 companies."""
    years = df["Year"].astype(int).values
    fig, ax = plt.subplots(figsize=(12, 6))
    for i, c in enumerate(COMPANIES_OP):
        margin_col = f"{c}_margin"
        vals = df[margin_col].values
        ax.plot(years, vals, marker="o", linewidth=2, markersize=5, label=c, color=COLORS[i])
    ax.axhline(0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("Year")
    ax.set_ylabel("Operating Margin (%)")
    ax.set_title("Athletic Apparel & Footwear: Operating Margins by Company\n(Adidas/Puma converted from EUR; COVID impacted 2020-2021)")
    ax.legend(loc="best")
    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved: {out_path}")


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

    df_raw = pd.read_excel(EXCEL_PATH, sheet_name="Industry", header=None)
    rev_df, op_df = load_industry(df_raw)
    result, df_14 = calc_shares_and_margins(rev_df, op_df)

    plot_revenue_shares(df_14, os.path.join(IMG_DIR, "industry_revenue_shares.png"))
    plot_operating_margins(result, os.path.join(IMG_DIR, "industry_operating_margins.png"))

    result.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved: {OUTPUT_CSV}")

    print("\n--- Revenue Shares (2014-2025) ---")
    print(df_14[["Year"] + [f"{c}_share" for c in COMPANIES]].to_string(index=False))
    print("\n--- Operating Margins (%) ---")
    print(result[["Year"] + [f"{c}_margin" for c in COMPANIES_OP]].to_string(index=False))

    return result, df_14


if __name__ == "__main__":
    main()
