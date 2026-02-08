"""
EPV 与 WACC 表格组件（参考 Lecture 3 第13页、第35页）
"""
import streamlit as st
import pandas as pd
from typing import Dict, List, Optional
import plotly.graph_objects as go


# 部分公司已知的营业利润率转折/事件（可扩展）
OPERATING_MARGIN_ANNOTATIONS = {
    'WMT': [
        {'year_index': 14, 'text': 'Competition from Aldi, dollar stores, e-commerce'},
        {'year_index': 10, 'text': 'Investment in online / Walmart+'},
        {'year_index': 4, 'text': 'International exits (Brazil, UK, Japan)'},
    ],
    'SBUX': [
        {'year_index': 8, 'text': 'Kraft arbitration charge'},
    ],
}


def render_epv_formula_and_adjustments(breakdown: Dict, key_prefix: str = "epv") -> Dict:
    """
    展示 EPV 公式与各调整分项（依据 + 可手动输入）。
    返回用户输入覆盖值 { key: value } 供计算器使用。
    """
    st.markdown("### 核心公式")
    st.latex(r"EPV = \frac{Adjusted\ NOPAT}{r} = \frac{NOPAT_{t+1}^a}{WACC}")
    st.markdown("**Adjusted NOPAT** = (1 - 税率) × { 营业利润 ± 非经常项 + 折旧调整 + 增长性支出 }")
    
    st.markdown("---")
    st.markdown("### 原始营业利润与调整分项")
    
    revenue = breakdown.get('revenue', 0)
    smoothed_margin = breakdown.get('smoothed_margin', 0)
    original_op = breakdown.get('original_operating_income', 0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("营业收入 ($)", f"{revenue/1e9:.2f}B")
    with col2:
        st.metric("平滑营业利润率", f"{smoothed_margin:.2%}")
    with col3:
        st.metric("原始营业利润 (平滑)", f"{original_op/1e9:.2f}B")
    
    overrides = {}
    for item in breakdown.get('adjustments_detail', []):
        suggested = item.get('suggested_value', item['adjustment_value'])
        default_val = float(suggested) if suggested is not None else float(item['adjustment_value'])
        label_suggest = f"建议值: ${default_val/1e9:.2f}B" if default_val != 0 else "建议值: 根据年报附注填写后手动输入"
        with st.expander(f"✏️ {item['name']} — 报表/原值: ${item['original_value']/1e9:.2f}B | {label_suggest}"):
            st.markdown("**依据**: " + item['rationale'])
            val = st.number_input(
                "调整额 (美元，正=加回营业利润)；可修改建议值",
                value=default_val,
                step=1e8,
                key=f"{key_prefix}_adj_{item['key']}",
            )
            overrides[item['key']] = val
    
    return overrides


def render_wacc_table_lecture3_p13(wacc_breakdown: Dict, key_prefix: str = "wacc") -> Dict:
    """
    WACC 计算表（Lecture 3 第13页格式），用标准表格展示，各项可手动输入。
    """
    st.markdown("### WACC 计算过程（参考 Lecture 3 第13页）")
    
    w = wacc_breakdown
    
    with st.expander("✏️ 手动覆盖 WACC 各项"):
        c1, c2 = st.columns(2)
        with c1:
            r1 = st.number_input("1. Market equity ($US mn)", value=float(w['market_equity_mn']), step=1000.0, key=f"{key_prefix}_mkt_equity")
            r2 = st.number_input("2. Debt ($US mn)", value=float(w['debt_mn']), step=100.0, key=f"{key_prefix}_debt")
            r3 = st.number_input("3. Debt due within year ($US mn)", value=float(w['debt_current_portion_mn']), step=10.0, key=f"{key_prefix}_debt_cur")
            r4 = st.number_input("4. Leases ($US mn)", value=float(w['leases_mn']), step=10.0, key=f"{key_prefix}_leases")
            r5 = st.number_input("5. Leases due within year ($US mn)", value=float(w['leases_current_mn']), step=1.0, key=f"{key_prefix}_leases_cur")
        with c2:
            beta = st.number_input("9. CAPM Beta", value=float(w['beta']), step=0.05, key=f"{key_prefix}_beta")
            mkt_prem = st.number_input("10. Market Premium (%)", value=float(w['market_premium_pct']), step=0.5, key=f"{key_prefix}_mkt_prem")
            tr10 = st.number_input("11. Treasury 10yr (%)", value=float(w['treasury_10y_pct']), step=0.1, key=f"{key_prefix}_tr10")
            nbc = st.number_input("13. Net borrowing cost (%)", value=float(w['net_borrowing_cost_pct']), step=0.1, key=f"{key_prefix}_nbc")
            t = st.number_input("14. Tax rate (%)", value=float(w['tax_rate_pct']), step=1.0, key=f"{key_prefix}_tax")
    
    r6 = r2 + r3 + r4 + r5
    total_val = r1 * 1e6 + r6 * 1e6
    we = (r1 * 1e6) / total_val if total_val > 0 else 1.0
    wd = (r6 * 1e6) / total_val if total_val > 0 else 0.0
    re = tr10 + beta * mkt_prem
    rd = nbc * (1 - t / 100)
    wacc_pct = we * re + wd * rd
    
    # 用 DataFrame 渲染为正常表格，避免 markdown 表格错位/截断
    wacc_rows = [
        (1, "Market equity ($US mn)", "", f"{r1:,.0f}"),
        (2, "Debt ($US mn)", "", f"{r2:,.0f}"),
        (3, "Portion of LT debt due within a year ($US mn)", "", f"{r3:,.0f}"),
        (4, "Leases ($US mn)", "", f"{r4:,.0f}"),
        (5, "Leases due within a year ($US mn)", "", f"{r5:,.0f}"),
        (6, "Total debt ($US mn)", "6=2+3+4+5", f"{r6:,.0f}"),
        (7, "Share of equity (we)", "7=1/(1+6)", f"{we:.2f}"),
        (8, "Share of debt (wd)", "8=6/(1+6)", f"{wd:.2f}"),
        (9, "CAPM β (5yr; monthly)", "", f"{beta:.2f}"),
        (10, "Market Premium (%)", "", f"{mkt_prem:.2f}"),
        (11, "Treasury 10yr rate (%)", "", f"{tr10:.2f}"),
        (12, "Cost of equity (%; re)", "12=11+9×10", f"{re:.2f}"),
        (13, "Net borrowing cost (%)", "", f"{nbc:.2f}"),
        (14, "Tax Rate (%; t)", "", f"{t:.2f}"),
        (15, "Cost of debt (%; rd)", "15=13×(1-t)", f"{rd:.2f}"),
        (16, "WACC (%)", "16=7×12+8×15", f"{wacc_pct:.2f}"),
    ]
    wacc_df = pd.DataFrame(wacc_rows, columns=["行", "项目", "公式", "数值"])
    st.dataframe(wacc_df, use_container_width=True, hide_index=True)
    
    return {"wacc_pct": wacc_pct, "wacc": wacc_pct / 100}


def create_operating_margin_chart(
    years_or_labels: List[str],
    margins: List[float],
    smoothed_margin: float,
    ticker: str = "",
    smoothing_years: int = 3,
) -> go.Figure:
    """营业利润率折线图，含平滑线及可选事件标注"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years_or_labels,
        y=[m * 100 for m in margins],
        mode='lines+markers',
        name='Operating margin (%)',
        line=dict(color='#1f77b4', width=2),
    ))
    
    fig.add_hline(
        y=smoothed_margin * 100,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Smoothed ({smoothed_margin*100:.1f}%)",
    )
    
    # 事件标注
    events = OPERATING_MARGIN_ANNOTATIONS.get(ticker.upper().split('.')[0], [])
    for ev in events:
        idx = ev['year_index']
        if 0 <= idx < len(years_or_labels) and idx < len(margins):
            fig.add_annotation(
                x=years_or_labels[idx],
                y=margins[idx] * 100,
                text=ev['text'],
                showarrow=True,
                arrowhead=2,
                ax=-40,
                ay=-30,
                font=dict(size=10),
                bgcolor="lightyellow",
            )
    
    fig.update_layout(
        title=f"Operating margins and smoothed ({smoothing_years}-year average)",
        xaxis_title="Fiscal year",
        yaxis_title="Operating margin (%)",
        template="plotly_white",
        height=450,
        showlegend=True,
    )
    return fig


def render_growth_expense_method_selector(
    current_method: str,
    revenue: float,
    marketing_expense: float,
    brand_value: float,
) -> str:
    """Growth expense 两种算法（Lecture 3 第28页）可选项"""
    st.markdown("### 增长性支出调整方法（Lecture 3 第28页）")
    
    method = st.radio(
        "选择计算方法",
        options=['method1', 'method2'],
        format_func=lambda x: {
            'method1': 'Method 1: 品牌价值摊销法 — 品牌价值/15年=维持性摊销，Growth = 营销费用 - 维持性摊销',
            'method2': 'Method 2: 营收占比法 — 国际扩张后营销占比提升部分视为品牌增长，Growth = 营收 × 0.35%',
        }[x],
        index=0 if current_method == 'method1' else 1,
        key="growth_expense_method",
    )
    
    with st.expander("Method 1 说明"):
        st.markdown("""
        - 品牌价值（来自 AV 计算）按 15 年摊销，得到维持性营销摊销。
        - 当期营销费用减去该摊销，差额为品牌增长投入，加回营业利润。
        - **WMT 例**: 品牌价值 $47bn，维持性 = 47/15 ≈ $3.1bn；当期营销 $5.1bn → Growth expense = $2.0bn。
        """)
        if brand_value > 0:
            maint = brand_value / 15
            growth_m1 = max(0, marketing_expense - maint)
            st.metric("维持性摊销 ($B)", f"{maint/1e9:.2f}")
            st.metric("Method 1 增长支出 ($B)", f"{growth_m1/1e9:.2f}")
    
    with st.expander("Method 2 说明"):
        st.markdown("""
        - 国际扩张前营销占营收约 0.25%，扩张后约 0.60%，差额 0.35% 视为品牌增长投入。
        - Growth expense = 营收 × 0.35%。
        - **WMT 例**: 648 × 0.0035 ≈ $2.4bn。
        """)
        growth_m2 = revenue * 0.0035 if revenue > 0 else 0
        st.metric("Method 2 增长支出 ($B)", f"{growth_m2/1e9:.2f}")
    
    return method


def render_epv_final_table_lecture3_p35(
    revenue: float,
    operating_margin: float,
    op_income: float,
    adj_over_dep: float,
    adj_growth_marketing: float,
    adj_growth_product: float,
    adj_growth_lease: float,
    adj_growth_workforce: float,
    extraordinary: float,
    adjusted_op_income: float,
    tax_pct: float,
    adjusted_nopat: float,
    wacc_pct: float,
    epv_operating: float,
    non_op_cash: float,
    debt: float,
    epv_equity: float,
    r_star_pct: Optional[float] = None,
    epvc_operating: Optional[float] = None,
    epvc_equity: Optional[float] = None,
) -> None:
    """完整 EPV 计算表（Lecture 3 第35页）：原值、调整额、调整后对比；r* 与 EPVc；有调整项高亮。"""
    st.markdown("### EPV 完整计算过程（参考 Lecture 3 第35页）")
    
    tax_rate = tax_pct / 100
    orig_nopat = op_income * (1 - tax_rate)
    total_growth = adj_growth_marketing + adj_growth_product + adj_growth_lease + adj_growth_workforce
    total_adj = adj_over_dep + total_growth + extraordinary
    orig_epv = orig_nopat / (wacc_pct / 100) if wacc_pct else 0
    
    def _b(x: float) -> str:
        return f"{x/1e9:.1f}" if x is not None and abs(x) < 1e15 else (f"{x:.1f}" if x is not None else "")
    
    rows: List[tuple] = [
        ("1", "Revenue", "", revenue, 0, revenue, False),
        ("2", "Operating margin", "", operating_margin, 0, operating_margin, False),
        ("3=1×2", "Operating income", "", op_income, 0, op_income, False),
        ("4", "Adjustments", "", None, None, None, False),
        ("5", "Over/under depreciation", "", 0, adj_over_dep, adj_over_dep, abs(adj_over_dep) > 1e6),
        ("6", "Growth expenses", "", 0, total_growth, total_growth, abs(total_growth) > 1e6),
        ("6a", "  Marketing", "", 0, adj_growth_marketing, adj_growth_marketing, abs(adj_growth_marketing) > 1e6),
        ("6b", "  Product", "", 0, adj_growth_product, adj_growth_product, abs(adj_growth_product) > 1e6),
        ("6c", "  Lease", "", 0, adj_growth_lease, adj_growth_lease, abs(adj_growth_lease) > 1e6),
        ("6d", "  Workforce", "", 0, adj_growth_workforce, adj_growth_workforce, abs(adj_growth_workforce) > 1e6),
        ("7", "Extraordinary items", "", 0, extraordinary, extraordinary, abs(extraordinary) > 1e6),
        ("8=3+5+6+7", "Adjusted Op. Income", "", op_income, total_adj, adjusted_op_income, abs(total_adj) > 1e6),
        ("9", "Taxes (%)", "", tax_pct, 0, tax_pct, False),
        ("10=8×(1-9)", "Adjusted NOPAT", "", orig_nopat, adjusted_nopat - orig_nopat, adjusted_nopat, abs(adjusted_nopat - orig_nopat) > 1e6),
        ("11", "WACC (%)", "", wacc_pct, 0, wacc_pct, False),
        ("12=10/11", "EPV Operating business", "", orig_epv, epv_operating - orig_epv, epv_operating, abs(epv_operating - orig_epv) > 1e6),
    ]
    if r_star_pct is not None and epvc_operating is not None:
        rows.append(("11b", "r* (%)", "r*≈r+p", r_star_pct, 0, r_star_pct, False))
        rows.append(("12b=10/11b", "EPVc (corrected)", "NOPAT/r*", epvc_operating, 0, epvc_operating, False))
    orig_epv_equity = orig_epv + non_op_cash - debt
    rows.extend([
        ("13", "Non-operational cash", "", non_op_cash, 0, non_op_cash, False),
        ("14", "Debt", "", debt, 0, debt, False),
        ("15=12+13-14", "EPV Equity", "", orig_epv_equity, epv_equity - orig_epv_equity, epv_equity, abs(epv_equity - orig_epv_equity) > 1e6),
    ])
    if epvc_equity is not None and r_star_pct is not None:
        rows.append(("15b", "EPVc Equity", "12b+13-14", epvc_equity, 0, epvc_equity, False))
    
    def _cell(val, is_pct: bool = False) -> str:
        if val is None:
            return ""
        if is_pct:
            return f"{val*100:.2f}" if 0 < abs(val) <= 1 else f"{val:.2f}"
        if abs(val) >= 1e9 or (abs(val) < 0.01 and val != 0):
            return _b(val) if val >= 0 else f"-{_b(-val)}"
        return f"{val:.3f}" if 0 < abs(val) < 100 else f"{val:.1f}"
    
    line_list, concept_list, formula_list, orig_list, adj_amt_list, after_list, highlight_list = [], [], [], [], [], [], []
    for line, concept, formula, orig, adj_amt, after, highlight in rows:
        line_list.append(line)
        concept_list.append(concept)
        formula_list.append(formula)
        is_pct = "(%" in concept or "margin" in concept.lower()
        orig_list.append(_cell(orig, is_pct) if orig is not None else "")
        adj_amt_list.append(_cell(adj_amt, False) if adj_amt is not None else "")
        after_list.append(_cell(after, is_pct) if after is not None else "")
        highlight_list.append(highlight)
    
    df = pd.DataFrame({
        "Line": line_list,
        "Concept": concept_list,
        "公式": formula_list,
        "原始/报表 ($B 或 %)": orig_list,
        "调整额 Adjusted amount": adj_amt_list,
        "调整后 ($B 或 %)": after_list,
    })
    
    # 用 HTML 表格实现高亮（Streamlit dataframe 不支持 Styler）
    html = '<table class="dataframe" style="border-collapse: collapse; width: 100%;">'
    html += "<thead><tr>" + "".join(f'<th style="border: 1px solid #ddd; padding: 6px; text-align: left;">{c}</th>' for c in df.columns) + "</tr></thead><tbody>"
    for i in range(len(df)):
        tr_style = "background-color: #fff3cd;" if highlight_list[i] else ""
        html += f'<tr style="{tr_style}">'
        for c in df.columns:
            html += f'<td style="border: 1px solid #ddd; padding: 6px;">{df.iloc[i][c]}</td>'
        html += "</tr>"
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)
    st.caption("高亮行：该项有调整额。")
