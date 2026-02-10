"""
从 Capital IQ 导出的 Deere Financials .xls 的 Segments 表读取，按 segment、按年算 Operating Margin 及同比，写入 Excel。
依赖: pip install xlrd pandas openpyxl
"""
import os
import re
import sys

try:
    import pandas as pd
except ImportError:
    print("请先安装: pip install pandas")
    sys.exit(1)
try:
    import xlrd
except ImportError:
    print("读 .xls 需 xlrd，请安装: pip install xlrd")
    sys.exit(1)


def _to_num(x):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return None
    s = str(x).strip().replace(",", "").replace("(", "-").replace(")", "")
    s = re.sub(r"[^\d.\-]", "", s)
    if not s or s == "-":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _parse_year_from_header(val):
    """从表头单元格解析年份，如 '12 months\\nOct-31-2021' -> 2021"""
    if val is None or pd.isna(val):
        return None
    s = str(val)
    for y in range(2030, 2015, -1):
        if str(y) in s:
            return y
    return None


def extract_segment_margins(path: str, output_path: str = None) -> pd.DataFrame:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.abspath(path) if os.path.isabs(path) else os.path.join(base, path)
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    out_path = output_path or os.path.join(base, "Deere-Homework-Output.xlsx")
    if not os.path.isabs(out_path):
        out_path = os.path.join(base, out_path)

    xl = pd.ExcelFile(path, engine="xlrd")
    if "Segments" not in xl.sheet_names:
        raise ValueError("该文件中没有 'Segments' 表")

    df = pd.read_excel(xl, sheet_name="Segments", header=None)
    rev_start = op_start = None
    for r in range(min(35, len(df))):
        val = str(df.iloc[r, 0]).strip()
        if "Revenues" == val or (val and "revenue" in val.lower() and "total" not in val.lower()):
            rev_start = r
        if "Operating Profit Before Tax" in val or "Operating Profit" == val:
            op_start = r
        if rev_start is not None and op_start is not None:
            break
    if rev_start is None:
        rev_start = 15
    if op_start is None:
        op_start = 24

    ncol = df.shape[1]
    rows_rev = [rev_start + 2 + i for i in range(4)]
    rows_op = [op_start + 1 + i for i in range(4)]
    seg_names = [
        "Production & Precision AG",
        "Small AG & Turf",
        "Construction and Forestry",
        "Financial Services",
    ]

    # 解析年份：表头在 rev_start-2 或 13 行
    header_row = rev_start - 2
    if header_row < 0:
        header_row = 13
    years = []
    for c in range(1, ncol):
        y = _parse_year_from_header(df.iloc[header_row, c])
        if y is not None:
            years.append((c, y))
        else:
            years.append((c, 2019 + len(years) + 1))
    if not years:
        years = [(c, 2020 + c - 1) for c in range(1, min(7, ncol))]

    # 每个 segment 每年：Revenue, Operating_Income, Margin, Margin_YoY
    records = []
    for i in range(4):
        r_rev = rows_rev[i] if i < len(rows_rev) else rev_start + 2 + i
        r_op = rows_op[i] if i < len(rows_op) else op_start + 1 + i
        if r_rev >= len(df) or r_op >= len(df):
            continue
        label = str(df.iloc[r_rev, 0]).strip() or seg_names[i]
        margins_prev = None
        for j, (col, year) in enumerate(years):
            rev = _to_num(df.iloc[r_rev, col])
            op = _to_num(df.iloc[r_op, col])
            margin = None
            if rev is not None and rev != 0 and op is not None:
                margin = round(op / rev * 100, 2)
            yoy_pp = None
            if margin is not None and margins_prev is not None:
                yoy_pp = round(margin - margins_prev, 2)
            records.append({
                "Segment": label,
                "Year": year,
                "Revenue": rev,
                "Operating_Income": op,
                "Margin_%": margin,
                "Margin_YoY_pp": yoy_pp,
            })
            margins_prev = margin

    long = pd.DataFrame(records)

    # 宽表：Segment 一行，列 = 各年的 Revenue, OpInc, Margin, Margin_YoY
    wide_list = []
    for seg in long["Segment"].unique():
        sub = long[long["Segment"] == seg].sort_values("Year")
        row = {"Segment": seg}
        for _, r in sub.iterrows():
            y = int(r["Year"])
            row[f"{y}_Revenue"] = r["Revenue"]
            row[f"{y}_Operating_Income"] = r["Operating_Income"]
            row[f"{y}_Margin_%"] = r["Margin_%"]
            row[f"{y}_Margin_YoY_pp"] = r["Margin_YoY_pp"]
        wide_list.append(row)
    wide = pd.DataFrame(wide_list)

    if os.path.exists(out_path):
        with pd.ExcelWriter(out_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as w:
            long.to_excel(w, sheet_name="Seg_By_Year", index=False)
            wide.to_excel(w, sheet_name="Seg_By_Segment", index=False)
    else:
        with pd.ExcelWriter(out_path, engine="openpyxl", mode="w") as w:
            long.to_excel(w, sheet_name="Seg_By_Year", index=False)
            wide.to_excel(w, sheet_name="Seg_By_Segment", index=False)

    print("已写入:", out_path)
    print(long.to_string(index=False))
    return long


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", default="Deere Company NYSE DE Financials.xls")
    parser.add_argument("-o", "--output", default=None)
    args = parser.parse_args()
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = args.file if os.path.isabs(args.file) else os.path.join(base, args.file)
    try:
        extract_segment_margins(path, output_path=args.output)
    except Exception as e:
        print("错误:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
