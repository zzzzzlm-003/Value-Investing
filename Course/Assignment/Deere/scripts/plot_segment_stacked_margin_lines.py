"""
读取 Deere-Homework-Output.xlsx（Seg_By_Year）：堆叠柱状图 = 各 segment 收入占比（%），次轴 = 四条 Margin 折线（时间趋势）。
"""
import os
import sys

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("请先安装: pip install pandas matplotlib numpy")
    sys.exit(1)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL = os.path.join(BASE, "Deere-Homework-Output.xlsx")
OUT = os.path.join(BASE, "images", "segment_stacked_pct_margin_lines.png")

COLORS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
SEG_ORDER = [
    "Production & Precision AG",
    "Small AG & Turf",
    "Construction and Forestry",
    "Financial Services",
]


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    if not os.path.isfile(EXCEL):
        print("未找到", EXCEL)
        sys.exit(1)
    df = pd.read_excel(EXCEL, sheet_name="Seg_By_Year")
    years = sorted(df["Year"].unique())
    segments = [s for s in SEG_ORDER if s in df["Segment"].unique()]
    if not segments:
        segments = df["Segment"].unique().tolist()

    # 每年各 segment 收入占比（堆叠柱）
    rev_pct = {}
    for seg in segments:
        rev_pct[seg] = df[df["Segment"] == seg].set_index("Year").reindex(years)["Revenue"]
    total_rev = sum(rev_pct[s] for s in segments)
    pct = {s: (rev_pct[s] / total_rev * 100).fillna(0) for s in segments}

    # 各 segment 的 margin 时间序列
    margin_series = {}
    for seg in segments:
        sub = df[df["Segment"] == seg].set_index("Year").reindex(years)
        margin_series[seg] = sub["Margin_%"].values

    x = np.arange(len(years))
    width = 0.6

    fig, ax1 = plt.subplots(figsize=(10, 6))
    bottom = np.zeros(len(years))
    for i, seg in enumerate(segments):
        vals = pct[seg].values
        ax1.bar(x, vals, width, bottom=bottom, color=COLORS[i % len(COLORS)], label=seg, alpha=0.9)
        bottom = bottom + vals

    ax1.set_xlabel("Fiscal Year", fontsize=11)
    ax1.set_ylabel("Revenue Share (%)", fontsize=11)
    ax1.set_xticks(x)
    ax1.set_xticklabels(years)
    ax1.set_ylim(0, 100)
    ax1.legend(loc="upper left", fontsize=9)

    ax2 = ax1.twinx()
    for i, seg in enumerate(segments):
        ax2.plot(x, margin_series[seg], color=COLORS[i % len(COLORS)], marker="o", linewidth=2, markersize=5, linestyle="--", label=f"{seg} (margin)")

    ax2.set_ylabel("Operating Margin (%)", fontsize=11)
    ax2.set_ylim(0, max(35, df["Margin_%"].max() * 1.15))
    ax2.legend(loc="upper right", fontsize=8)

    ax1.set_title("Deere: Segment Revenue Share (Stacked %) and Operating Margin by Year", fontsize=12)
    fig.tight_layout()
    plt.savefig(OUT, dpi=150, bbox_inches="tight")
    plt.close()
    print("已保存:", OUT)


if __name__ == "__main__":
    main()
