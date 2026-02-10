"""
读取 Deere-Homework-Output.xlsx 的 Seg_By_Year 表，画各 segment 的 Margin % 及 YoY 折线图。
"""
import os
import sys

try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as e:
    print("请先安装: pip install pandas matplotlib")
    sys.exit(1)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL = os.path.join(BASE, "Deere-Homework-Output.xlsx")
OUT = os.path.join(BASE, "images", "segment_margin_yoy_chart.png")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    if not os.path.isfile(EXCEL):
        print("未找到", EXCEL, "请先运行 scripts/segment_margins_from_capiq.py")
        sys.exit(1)
    df = pd.read_excel(EXCEL, sheet_name="Seg_By_Year")
    df = df.sort_values(["Segment", "Year"])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
    for i, seg in enumerate(df["Segment"].unique()):
        sub = df[df["Segment"] == seg]
        c = colors[i % len(colors)]
        ax1.plot(sub["Year"], sub["Margin_%"], marker="o", label=seg, color=c, linewidth=2, markersize=5)
        ax2.plot(sub["Year"], sub["Margin_YoY_pp"], marker="s", label=seg, color=c, linewidth=2, markersize=5)

    ax1.set_ylabel("Operating Margin (%)", fontsize=11)
    ax1.set_title("Deere: Operating Margin by Segment", fontsize=12)
    ax1.legend(loc="best", fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(bottom=0)

    ax2.set_ylabel("Margin YoY (percentage points)", fontsize=11)
    ax2.set_xlabel("Fiscal Year", fontsize=11)
    ax2.set_title("Deere: Operating Margin YoY by Segment", fontsize=12)
    ax2.legend(loc="best", fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.axhline(0, color="gray", linestyle="--", linewidth=0.8)

    plt.tight_layout()
    plt.savefig(OUT, dpi=150, bbox_inches="tight")
    plt.close()
    print("已保存:", OUT)


if __name__ == "__main__":
    main()
