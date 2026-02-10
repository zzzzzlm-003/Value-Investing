"""
Run all homework scripts: Q2 竞品份额, Q3 需求变量, Q5 关税股价, EPV, 资产负债表, 合并输出.
依赖: Homework-Data-2026.xlsx, Deere Company NYSE DE Financials.xls (segment)
Q3 需 FRED_API_KEY; Q2/Q5 仅需课程 Excel。
"""
import os
import sys
import importlib.util

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)
sys.path.insert(0, BASE)


def main():
    print("=== Q2: 竞品收入份额 ===")
    from scripts.q2_industry_revenue_shares import main as q2
    q2()

    print("\n=== Q5: 关税股价反应 ===")
    from scripts.q5_tariff_reaction_calc import main as q5
    q5()

    print("\n=== 资产负债表对比 ===")
    from scripts.build_balance_sheet_comparison import main as bs
    bs()

    # Q3 需 FRED API
    if os.environ.get("FRED_API_KEY"):
        print("\n=== Q3: 需求变量 (FRED) ===")
        from scripts.q3_demand_variables import main as q3
        q3()
    else:
        print("\n(Q3 跳过: 需设置 FRED_API_KEY)")

    # Segment 可选（需 xlrd）
    capiq = os.path.join(BASE, "Deere Company NYSE DE Financials.xls")
    has_xlrd = importlib.util.find_spec("xlrd") is not None
    if os.path.isfile(capiq) and has_xlrd:
        try:
            print("\n=== Segment Margins ===")
            from scripts.segment_margins_from_capiq import extract_segment_margins
            extract_segment_margins(capiq)
            from scripts.plot_segment_margin_yoy import main as seg_yoy
            seg_yoy()
        except Exception as e:
            print(f"(Segment 跳过: {e})")
    elif os.path.isfile(capiq):
        print("\n(Segment 跳过: 未安装 xlrd，运行 `pip install xlrd` 后可启用)")

    print("\n=== EPV 计算 ===")
    from scripts.epv_calculation import main as epv
    epv()

    print("\n完成。输出: Deere-Homework-Output.xlsx, images/")


if __name__ == "__main__":
    main()
