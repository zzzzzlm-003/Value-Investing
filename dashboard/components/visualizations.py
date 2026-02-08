"""
可视化组件模块
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List


class ValuationVisualizer:
    """估值可视化类"""
    
    @staticmethod
    def create_market_cap_history(dates: List, market_caps: List, 
                                  current_date: str = "") -> go.Figure:
        """
        创建市值历史走势图
        
        Args:
            dates: 日期列表
            market_caps: 市值列表
            current_date: 当前日期
            
        Returns:
            plotly Figure
        """
        fig = go.Figure()
        
        # 转换为十亿
        market_caps_b = [mc/1e9 for mc in market_caps]
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=market_caps_b,
            mode='lines',
            name='市值',
            line=dict(color='#3498db', width=2),
            fill='tozeroy',
            fillcolor='rgba(52, 152, 219, 0.1)',
            hovertemplate='日期: %{x}<br>市值: $%{y:.2f}B<extra></extra>'
        ))
        
        title = f'市值历史走势 (截至 {current_date})' if current_date else '市值历史走势'
        
        fig.update_layout(
            title=title,
            xaxis_title='日期',
            yaxis_title='市值 (十亿美元)',
            template='plotly_white',
            height=400,
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def create_beta_history(dates: List, betas: List, 
                           current_beta: float = None,
                           method: str = "历史Beta") -> go.Figure:
        """
        创建Beta历史走势图
        
        Args:
            dates: 日期列表
            betas: Beta值列表
            current_beta: 当前Beta
            method: 计算方法
            
        Returns:
            plotly Figure
        """
        fig = go.Figure()
        
        # Beta走势线（注意：此为 60 日滚动 Beta，与下方「全样本 Beta」口径不同）
        fig.add_trace(go.Scatter(
            x=dates,
            y=betas,
            mode='lines',
            name='60日滚动Beta',
            line=dict(color='#e74c3c', width=2),
            hovertemplate='日期: %{x}<br>60日滚动Beta: %{y:.3f}<extra></extra>'
        ))
        
        # Beta=1.0参考线
        fig.add_hline(
            y=1.0,
            line_dash="dash",
            line_color="gray",
            annotation_text="市场Beta=1.0",
            annotation_position="right"
        )
        
        # 全样本/当前Beta：用于 WACC 的 CAPM Beta（5年月度全样本），与红线口径不同
        if current_beta is not None and dates:
            fig.add_hline(
                y=current_beta,
                line_dash="dot",
                line_color="#2ecc71",
                annotation_text=f"全样本Beta(用于WACC)={current_beta:.2f}",
                annotation_position="left"
            )
            fig.add_trace(go.Scatter(
                x=[dates[-1]],
                y=[current_beta],
                mode='markers',
                name=f'当前Beta(全样本)={current_beta:.2f}',
                marker=dict(size=12, color='#2ecc71', symbol='star'),
                hovertemplate=f'当前Beta(全样本,用于估值): {current_beta:.3f}<extra></extra>'
            ))
        
        fig.update_layout(
            title=f'Beta历史走势 - {method}（红线=60日滚动，绿星=全样本CAPM）',
            xaxis_title='日期',
            yaxis_title='Beta值',
            template='plotly_white',
            height=400,
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def create_av_epv_comparison(av: float, epv: float, market_cap: float,
                                  company_name: str = "") -> go.Figure:
        """
        创建AV vs EPV vs 市值对比图
        
        Args:
            av: Asset Value
            epv: Earning Power Value
            market_cap: 市值
            company_name: 公司名称
            
        Returns:
            plotly Figure
        """
        fig = go.Figure()
        
        categories = ['Asset Value\n(AV)', 'Earning Power\nValue (EPV)', '当前市值']
        def _finite(x):
            return x is not None and x == x and abs(x) != float('inf')
        values = [(v / 1e9) if _finite(v) else 0 for v in [av, epv, market_cap]]
        colors = ['#3498db', '#2ecc71', '#e74c3c']
        
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            text=[f'${v:.1f}B' for v in values],
            textposition='auto',
            marker_color=colors,
            hovertemplate='<b>%{x}</b><br>估值: $%{y:.1f}B<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'{company_name} 估值对比' if company_name else '估值对比',
            yaxis_title='估值 (十亿美元)',
            xaxis_title='',
            template='plotly_white',
            height=500,
            showlegend=False,
            font=dict(size=14)
        )
        
        return fig
    
    @staticmethod
    def create_av_components_breakdown(components: Dict) -> go.Figure:
        """
        创建AV组成部分分解图
        
        Args:
            components: AV组成部分字典
            
        Returns:
            plotly Figure
        """
        # 筛选正值和负值
        positive_items = {k: v for k, v in components.items() if v > 0}
        negative_items = {k: v for k, v in components.items() if v < 0}
        
        fig = go.Figure()
        
        # 正值（蓝色）
        if positive_items:
            fig.add_trace(go.Bar(
                name='增加项',
                x=list(positive_items.keys()),
                y=[v/1e9 for v in positive_items.values()],
                marker_color='#3498db',
                text=[f'${v/1e9:.1f}B' for v in positive_items.values()],
                textposition='auto',
            ))
        
        # 负值（红色）
        if negative_items:
            fig.add_trace(go.Bar(
                name='减少项',
                x=list(negative_items.keys()),
                y=[v/1e9 for v in negative_items.values()],
                marker_color='#e74c3c',
                text=[f'${v/1e9:.1f}B' for v in negative_items.values()],
                textposition='auto',
            ))
        
        fig.update_layout(
            title='Asset Value 组成分解',
            yaxis_title='金额 (十亿美元)',
            xaxis_title='',
            barmode='relative',
            template='plotly_white',
            height=500,
            font=dict(size=12)
        )
        
        return fig
    
    @staticmethod
    def create_epv_components_waterfall(components: Dict, total_epv: float) -> go.Figure:
        """
        创建EPV调整项瀑布图
        
        Args:
            components: EPV调整项字典
            total_epv: 最终EPV值
            
        Returns:
            plotly Figure
        """
        # 准备数据
        labels = list(components.keys()) + ['最终EPV']
        values = list(components.values()) + [total_epv]
        
        # 转换为十亿
        values_b = [v/1e9 for v in values]
        
        fig = go.Figure(go.Waterfall(
            name="EPV计算",
            orientation="v",
            measure=["relative"] * len(components) + ["total"],
            x=labels,
            textposition="outside",
            text=[f"${v:.1f}B" if v != 0 else "" for v in values_b],
            y=values_b,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        
        fig.update_layout(
            title="Earning Power Value 计算过程",
            yaxis_title="金额 (十亿美元)",
            template='plotly_white',
            height=500,
            showlegend=False,
            font=dict(size=12)
        )
        
        return fig
    
    @staticmethod
    def create_wacc_sensitivity(wacc_values: List[float], epv_values: List[float],
                               current_wacc: float, current_epv: float) -> go.Figure:
        """
        创建WACC敏感性分析图
        
        Args:
            wacc_values: WACC值列表
            epv_values: 对应的EPV值列表
            current_wacc: 当前WACC
            current_epv: 当前EPV
            
        Returns:
            plotly Figure
        """
        fig = go.Figure()
        
        # EPV曲线
        fig.add_trace(go.Scatter(
            x=[w*100 for w in wacc_values],
            y=[v/1e9 for v in epv_values],
            mode='lines+markers',
            name='EPV',
            line=dict(color='#2ecc71', width=3),
            marker=dict(size=8)
        ))
        
        # 当前点
        fig.add_trace(go.Scatter(
            x=[current_wacc*100],
            y=[current_epv/1e9],
            mode='markers',
            name='当前值',
            marker=dict(size=15, color='#e74c3c', symbol='star')
        ))
        
        fig.update_layout(
            title='WACC 敏感性分析',
            xaxis_title='WACC (%)',
            yaxis_title='EPV (十亿美元)',
            template='plotly_white',
            height=500,
            hovermode='x unified',
            font=dict(size=12)
        )
        
        return fig
    
    @staticmethod
    def create_margin_trend(revenues: List[float], margins: List[float],
                          years: List[str] = None) -> go.Figure:
        """
        创建营业利润率趋势图
        
        Args:
            revenues: 营收列表
            margins: 利润率列表
            years: 年份列表
            
        Returns:
            plotly Figure
        """
        if years is None:
            years = [f'Year {i+1}' for i in range(len(revenues))]
        
        # 创建双y轴图
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # 营收柱状图
        fig.add_trace(
            go.Bar(
                x=years,
                y=[r/1e9 for r in revenues],
                name='营业收入',
                marker_color='#3498db',
                yaxis='y',
            ),
            secondary_y=False,
        )
        
        # 利润率折线图
        fig.add_trace(
            go.Scatter(
                x=years,
                y=[m*100 for m in margins],
                name='营业利润率',
                mode='lines+markers',
                line=dict(color='#e74c3c', width=3),
                marker=dict(size=10),
                yaxis='y2',
            ),
            secondary_y=True,
        )
        
        # 更新坐标轴
        fig.update_xaxes(title_text="年份")
        fig.update_yaxes(title_text="营业收入 (十亿美元)", secondary_y=False)
        fig.update_yaxes(title_text="营业利润率 (%)", secondary_y=True)
        
        fig.update_layout(
            title='营业收入与利润率趋势',
            template='plotly_white',
            height=500,
            hovermode='x unified',
            font=dict(size=12)
        )
        
        return fig
    
    @staticmethod
    def create_valuation_summary_table(av_summary: Dict, epv_summary: Dict) -> pd.DataFrame:
        """
        创建估值摘要表格
        
        Args:
            av_summary: AV摘要
            epv_summary: EPV摘要
            
        Returns:
            DataFrame
        """
        def _finite(x):
            return x is not None and x == x and abs(x) != float('inf')
        av = av_summary.get('total_av', 0) or 0
        epv = epv_summary.get('epv', 0) or 0
        mcap = av_summary.get('market_cap', 0) or 0
        arat = av_summary.get('av_to_market_cap', 0)
        erat = epv_summary.get('epv_to_market_cap', 0)
        data = {
            '指标': [
                'Asset Value (AV)',
                'Earning Power Value (EPV)',
                '当前市值',
                'AV/市值',
                'EPV/市值',
                'EPV-AV价差',
            ],
            '金额': [
                f"${av/1e9:.1f}B" if _finite(av) else 'N/A',
                f"${epv/1e9:.1f}B" if _finite(epv) else 'N/A',
                f"${mcap/1e9:.1f}B" if _finite(mcap) else 'N/A',
                f"{arat:.1%}" if _finite(arat) else 'N/A',
                f"{erat:.1%}" if _finite(erat) else 'N/A',
                f"${(epv-av)/1e9:.1f}B" if _finite(epv - av) else 'N/A',
            ]
        }
        return pd.DataFrame(data)
    
    @staticmethod
    def create_pie_chart(components: Dict, title: str = "组成分析") -> go.Figure:
        """
        创建饼图
        
        Args:
            components: 组成部分字典
            title: 标题
            
        Returns:
            plotly Figure
        """
        # 只显示正值
        positive_items = {k: v for k, v in components.items() if v > 0}
        
        fig = go.Figure(data=[go.Pie(
            labels=list(positive_items.keys()),
            values=list(positive_items.values()),
            hole=.3,
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>金额: $%{value/1e9:.1f}B<br>占比: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title=title,
            template='plotly_white',
            height=500,
            font=dict(size=12)
        )
        
        return fig
    
    @staticmethod
    def create_franchise_value_waterfall(fv_analysis: Dict) -> go.Figure:
        """
        创建Franchise Value瀑布图
        
        展示从EPV到Total Value的价值构成
        
        Args:
            fv_analysis: Franchise Value分析结果
            
        Returns:
            plotly Figure
        """
        epv = fv_analysis.get('epv', 0) / 1e9  # 转换为十亿
        fv = fv_analysis.get('franchise_value', 0) / 1e9
        total = fv_analysis.get('total_value', 0) / 1e9
        market_cap = fv_analysis.get('market_cap', 0) / 1e9
        
        fig = go.Figure(go.Waterfall(
            name = "价值组成",
            orientation = "v",
            measure = ["absolute", "relative", "total", "absolute"],
            x = ["盈利能力价值<br>(EPV)", "特许权价值<br>(FV)", "内在价值", "当前市值"],
            textposition = "outside",
            text = [f"${epv:.1f}B", f"${fv:.1f}B", f"${total:.1f}B", f"${market_cap:.1f}B"],
            y = [epv, fv, total, market_cap],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
        ))
        
        fig.update_layout(
            title = "估值分解：从EPV到总价值",
            showlegend = False,
            template='plotly_white',
            height=500,
            yaxis_title="价值 (十亿美元)",
            font=dict(size=12)
        )
        
        return fig
    
    @staticmethod
    def create_roic_vs_wacc_scatter(roic: float, wacc: float, 
                                     company_name: str = "") -> go.Figure:
        """
        创建ROIC vs WACC散点图
        
        Args:
            roic: 投资资本回报率
            wacc: 加权平均资本成本
            company_name: 公司名称
            
        Returns:
            plotly Figure
        """
        fig = go.Figure()
        
        # 添加45度线（ROIC = WACC）
        max_val = max(roic, wacc) * 1.2
        fig.add_trace(go.Scatter(
            x=[0, max_val],
            y=[0, max_val],
            mode='lines',
            name='ROIC = WACC<br>(无经济利润)',
            line=dict(color='gray', dash='dash'),
            showlegend=True
        ))
        
        # 添加公司数据点
        fig.add_trace(go.Scatter(
            x=[wacc],
            y=[roic],
            mode='markers+text',
            name=company_name or '目标公司',
            marker=dict(
                size=20,
                color='green' if roic > wacc else 'red',
                line=dict(width=2, color='white')
            ),
            text=[company_name or '目标公司'],
            textposition='top center',
            showlegend=True
        ))
        
        # 添加价值创造/摧毁区域
        fig.add_shape(
            type="rect",
            x0=0, y0=0,
            x1=max_val, y1=max_val,
            fillcolor="lightgreen",
            opacity=0.1,
            layer="below",
            line_width=0,
        )
        
        fig.add_annotation(
            x=max_val * 0.7,
            y=max_val * 0.9,
            text="价值创造区<br>(ROIC > WACC)",
            showarrow=False,
            font=dict(size=14, color="green")
        )
        
        fig.add_annotation(
            x=max_val * 0.9,
            y=max_val * 0.5,
            text="价值摧毁区<br>(ROIC < WACC)",
            showarrow=False,
            font=dict(size=14, color="red")
        )
        
        fig.update_layout(
            title=f"ROIC vs WACC 分析<br>ROIC: {roic:.1%} | WACC: {wacc:.1%} | 差额: {(roic-wacc):.1%}",
            xaxis_title="WACC (加权平均资本成本)",
            yaxis_title="ROIC (投资资本回报率)",
            template='plotly_white',
            height=500,
            xaxis=dict(tickformat='.0%'),
            yaxis=dict(tickformat='.0%'),
            font=dict(size=12)
        )
        
        return fig
    
    @staticmethod
    def create_growth_decomposition(growth_analysis: Dict) -> go.Figure:
        """
        创建增长率分解图
        
        Args:
            growth_analysis: 增长分析结果
            
        Returns:
            plotly Figure
        """
        investment_growth = growth_analysis.get('investment_growth', 0)
        organic_growth = growth_analysis.get('organic_growth', 0)
        total_growth = growth_analysis.get('total_growth', 0)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='投资驱动增长<br>(k × ROIC)',
            x=['增长率分解'],
            y=[investment_growth * 100],
            marker_color='steelblue',
            text=[f'{investment_growth:.1%}'],
            textposition='inside',
        ))
        
        fig.add_trace(go.Bar(
            name='有机增长<br>(同店/生产率)',
            x=['增长率分解'],
            y=[organic_growth * 100],
            marker_color='lightseagreen',
            text=[f'{organic_growth:.1%}'],
            textposition='inside',
        ))
        
        fig.add_shape(
            type="line",
            x0=-0.5, x1=0.5,
            y0=total_growth * 100, y1=total_growth * 100,
            line=dict(color="red", width=3, dash="dash"),
        )
        
        fig.add_annotation(
            x=0,
            y=total_growth * 100,
            text=f"总增长率: {total_growth:.1%}",
            showarrow=False,
            yshift=20,
            font=dict(size=14, color="red", family="Arial Black")
        )
        
        fig.update_layout(
            title="盈利增长率分解",
            yaxis_title="增长率 (%)",
            barmode='stack',
            template='plotly_white',
            height=400,
            showlegend=True,
            font=dict(size=12)
        )
        
        return fig
    
    @staticmethod
    def create_return_scenarios_heatmap(return_analysis: Dict) -> go.Figure:
        """
        创建预期收益率情景热力图
        
        根据不同的g和h组合展示收益率
        
        Args:
            return_analysis: 收益率分析结果
            
        Returns:
            plotly Figure
        """
        # 获取基础参数
        dist_yield = return_analysis.get('distribution_yield', 0)
        base_g = return_analysis.get('growth_rate', 0)
        
        # 创建g和h的范围
        g_range = np.linspace(base_g - 0.10, base_g + 0.10, 11)
        h_range = np.linspace(-0.15, 0.15, 11)
        
        # 计算收益率矩阵
        # R = D/V + g + (1+g) × h
        returns_matrix = np.zeros((len(g_range), len(h_range)))
        
        for i, g in enumerate(g_range):
            for j, h in enumerate(h_range):
                returns_matrix[i, j] = (dist_yield + g + (1 + g) * h) * 100
        
        fig = go.Figure(data=go.Heatmap(
            z=returns_matrix,
            x=[f'{h:.1%}' for h in h_range],
            y=[f'{g:.1%}' for g in g_range],
            colorscale='RdYlGn',
            text=[[f'{val:.1f}%' for val in row] for row in returns_matrix],
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="收益率 (%)"),
            hoverongaps=False,
            hovertemplate='g: %{y}<br>h: %{x}<br>收益率: %{z:.1f}%<extra></extra>'
        ))
        
        # 标记当前点
        current_g_idx = len(g_range) // 2
        current_h_idx = len(h_range) // 2
        
        fig.add_trace(go.Scatter(
            x=[f'{h_range[current_h_idx]:.1%}'],
            y=[f'{g_range[current_g_idx]:.1%}'],
            mode='markers',
            marker=dict(size=15, color='blue', symbol='x', line=dict(width=3, color='white')),
            name='当前预期',
            showlegend=True
        ))
        
        fig.update_layout(
            title=f"预期收益率情景分析<br>分配收益率: {dist_yield:.1%} | 基准增长率: {base_g:.1%}",
            xaxis_title="h (市盈率年化变化率)",
            yaxis_title="g (盈利增长率)",
            template='plotly_white',
            height=600,
            font=dict(size=11)
        )
        
        return fig
    
    @staticmethod
    def create_value_bridge(av: float, epv: float, fv: float, 
                           market_cap: float) -> go.Figure:
        """
        创建价值桥接图
        
        从AV到EPV到FV到市值的完整价值链
        
        Args:
            av: Asset Value
            epv: Earnings Power Value  
            fv: Franchise Value
            market_cap: 市值
            
        Returns:
            plotly Figure
        """
        # 转换为十亿
        av_b = av / 1e9
        epv_b = epv / 1e9
        fv_b = fv / 1e9
        mc_b = market_cap / 1e9
        total_b = epv_b + fv_b
        
        # 计算差额
        epv_premium = epv_b - av_b
        market_premium = mc_b - total_b
        
        fig = go.Figure(go.Waterfall(
            name = "价值演进",
            orientation = "v",
            measure = ["absolute", "relative", "total", "relative", "total", "absolute"],
            x = ["资产价值<br>(AV)", "EPV溢价", "盈利能力<br>(EPV)", 
                 "特许权<br>(FV)", "内在价值", "当前市值"],
            textposition = "outside",
            text = [f"${av_b:.1f}B", f"+${epv_premium:.1f}B", f"${epv_b:.1f}B",
                   f"+${fv_b:.1f}B", f"${total_b:.1f}B", f"${mc_b:.1f}B"],
            y = [av_b, epv_premium, epv_b, fv_b, total_b, mc_b],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
        ))
        
        # 添加注释说明市场溢价/折价
        if market_premium > 0:
            annotation_text = f"市场溢价: ${market_premium:.1f}B (+{market_premium/total_b:.1%})"
            annotation_color = "green"
        else:
            annotation_text = f"市场折价: ${abs(market_premium):.1f}B ({market_premium/total_b:.1%})"
            annotation_color = "red"
        
        fig.add_annotation(
            x=5,
            y=mc_b,
            text=annotation_text,
            showarrow=True,
            arrowhead=2,
            font=dict(size=12, color=annotation_color),
            bgcolor="white",
            bordercolor=annotation_color,
            borderwidth=2
        )
        
        fig.update_layout(
            title = "完整价值链：从资产到市值",
            showlegend = False,
            template='plotly_white',
            height=500,
            yaxis_title="价值 (十亿美元)",
            font=dict(size=12)
        )
        
        return fig
