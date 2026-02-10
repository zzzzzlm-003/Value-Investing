"""
导出模块 - Excel和PDF报告生成
"""
import pandas as pd
from datetime import datetime
from typing import Dict, Optional
import io


class ReportExporter:
    """报告导出类"""
    
    @staticmethod
    def export_to_excel(company_info: Dict, av_results: Dict, epv_results: Dict,
                       av_summary: Dict, epv_summary: Dict,
                       fv_analysis: Optional[Dict] = None,
                       extra_tables: Optional[Dict[str, pd.DataFrame]] = None) -> bytes:
        """
        导出详细Excel报告
        
        Args:
            company_info: 公司信息
            av_results: AV计算结果
            epv_results: EPV计算结果
            av_summary: AV摘要
            epv_summary: EPV摘要
            
        Returns:
            bytes: Excel文件内容
        """
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # 1. 公司信息页
            company_df = pd.DataFrame([
                ['公司名称', company_info.get('name', 'N/A')],
                ['行业', company_info.get('industry', 'N/A')],
                ['国家', company_info.get('country', 'N/A')],
                ['货币', company_info.get('currency', 'USD')],
                ['市值', f"${company_info.get('market_cap', 0)/1e9:.2f}B"],
                ['Beta', f"{company_info.get('beta', 1.0):.2f}"],
                ['员工数', company_info.get('employees', 'N/A')],
                ['分析日期', datetime.now().strftime('%Y-%m-%d')],
            ])
            company_df.columns = ['项目', '值']
            company_df.to_excel(writer, sheet_name='公司信息', index=False)
            
            # 2. Asset Value详细页
            av_detail_df = pd.DataFrame([
                ['账面权益', av_results.get('book_equity', 0) / 1e9],
                ['PPE调整', av_results.get('ppe_adjustment', 0) / 1e9],
                ['商誉调整', av_results.get('goodwill_adjustment', 0) / 1e9],
                ['品牌价值', av_results.get('brand_value', 0) / 1e9],
                ['员工价值', av_results.get('workforce_value', 0) / 1e9],
                ['产品组合价值', av_results.get('product_portfolio_value', 0) / 1e9],
                ['总Asset Value', av_results.get('total_av', 0) / 1e9],
            ], columns=['项目', '金额(十亿)'])
            av_detail_df.to_excel(writer, sheet_name='Asset Value', index=False)
            
            # 3. EPV详细页
            epv_detail_df = pd.DataFrame([
                ['营业收入', epv_results.get('current_revenue', 0) / 1e9],
                ['平滑利润率', epv_results.get('smoothed_margin', 0)],
                ['平滑营业利润', epv_results.get('smoothed_operating_income', 0) / 1e9],
                ['非经常项调整', epv_results.get('extraordinary_adjustment', 0) / 1e9],
                ['折旧调整', epv_results.get('depreciation_adjustment', 0) / 1e9],
                ['增长支出调整', epv_results.get('growth_expense_adjustment', 0) / 1e9],
                ['调整后营业利润', epv_results.get('adjusted_operating_income', 0) / 1e9],
                ['税率', epv_results.get('tax_rate', 0)],
                ['调整后NOPAT', epv_results.get('adjusted_nopat', 0) / 1e9],
                ['WACC', epv_results.get('wacc', 0)],
                ['总EPV', epv_results.get('epv', 0) / 1e9],
            ], columns=['项目', '值'])
            epv_detail_df.to_excel(writer, sheet_name='Earning Power Value', index=False)
            
            # 4. 估值摘要对比页
            summary_df = pd.DataFrame([
                ['Asset Value (AV)', av_summary.get('total_av', 0) / 1e9, '-'],
                ['Earning Power Value (EPV)', epv_summary.get('epv', 0) / 1e9, '-'],
                ['Franchise Value (FV)', (fv_analysis or {}).get('franchise_value', 0) / 1e9, '-'],
                ['当前市值', av_summary.get('market_cap', 0) / 1e9, '-'],
                ['AV/市值', av_summary.get('av_to_market_cap', 0), '%'],
                ['EPV/市值', epv_summary.get('epv_to_market_cap', 0), '%'],
                ['EPV-AV价差', (epv_summary.get('epv', 0) - av_summary.get('total_av', 0)) / 1e9, '十亿'],
            ], columns=['指标', '值', '单位'])
            summary_df.to_excel(writer, sheet_name='估值摘要', index=False)
            
            # 5. PPE调整明细（如果有）
            if 'ppe_details' in av_results and av_results['ppe_details']:
                ppe_details = av_results['ppe_details']
                ppe_rows = []
                for component, details in ppe_details.items():
                    if not isinstance(details, dict):
                        continue
                    ppe_rows.append([
                        component,
                        details.get('original', 0) / 1e9,
                        details.get('factor', 1.0),
                        details.get('adjusted', 0) / 1e9,
                        details.get('adjustment', 0) / 1e9,
                    ])
                
                ppe_df = pd.DataFrame(ppe_rows, 
                                     columns=['资产类型', '原值(十亿)', '调整系数', '调整后(十亿)', '调整额(十亿)'])
                ppe_df.to_excel(writer, sheet_name='PPE调整明细', index=False)

            # 6. FV 结果（如果有）
            if fv_analysis:
                fv_df = pd.DataFrame([
                    ['EPV', fv_analysis.get('epv', 0) / 1e9],
                    ['Franchise Value', fv_analysis.get('franchise_value', 0) / 1e9],
                    ['Total Value', fv_analysis.get('total_value', 0) / 1e9],
                    ['ROIC', fv_analysis.get('roic', 0)],
                    ['WACC', fv_analysis.get('wacc', 0)],
                    ['Growth rate', fv_analysis.get('growth_rate', 0)],
                    ['Margin of Safety', fv_analysis.get('margin_of_safety', 0)],
                ], columns=['项目', '值'])
                fv_df.to_excel(writer, sheet_name='Franchise Value', index=False)

            # 7. 额外明细表（原始值/调整值/过程）
            if extra_tables:
                for name, df in extra_tables.items():
                    try:
                        df.to_excel(writer, sheet_name=name[:31], index=False)
                    except Exception:
                        pass
        
        output.seek(0)
        return output.getvalue()
    
    @staticmethod
    def create_summary_text(company_info: Dict, av_summary: Dict, epv_summary: Dict) -> str:
        """
        创建文本摘要
        
        Args:
            company_info: 公司信息
            av_summary: AV摘要
            epv_summary: EPV摘要
            
        Returns:
            str: 文本摘要
        """
        market_cap = av_summary.get('market_cap', 0)
        av = av_summary.get('total_av', 0)
        epv = epv_summary.get('epv', 0)
        
        summary = f"""
价值投资分析报告
================

公司信息
--------
公司名称: {company_info.get('name', 'N/A')}
行业: {company_info.get('industry', 'N/A')}
当前市值: ${market_cap/1e9:.1f}B
分析日期: {datetime.now().strftime('%Y-%m-%d')}

估值结果
--------
Asset Value (AV):          ${av/1e9:.1f}B
Earning Power Value (EPV): ${epv/1e9:.1f}B
当前市值:                  ${market_cap/1e9:.1f}B

估值比率
--------
AV/市值:  {av_summary.get('av_to_market_cap', 0):.1%}
EPV/市值: {epv_summary.get('epv_to_market_cap', 0):.1%}
EPV/AV:   {epv/av if av > 0 else 0:.2f}x

分析结论
--------
"""
        
        epv_to_market = epv_summary.get('epv_to_market_cap', 0)
        
        if epv_to_market > 1.0:
            summary += f"✓ EPV ({epv_to_market:.0%}) 高于市值，可能存在低估\n"
        elif epv_to_market > 0.7:
            summary += f"→ EPV ({epv_to_market:.0%}) 接近市值，估值合理\n"
        else:
            summary += f"⚠ EPV ({epv_to_market:.0%}) 显著低于市值，包含大量增长预期\n"
        
        if epv > av:
            summary += f"✓ EPV 高于 AV ${(epv-av)/1e9:.1f}B，表明业务存在壁垒和竞争优势\n"
        else:
            summary += "⚠ EPV 低于或等于 AV，可能存在资产效率问题\n"
        
        summary += """
================
本报告基于 Graham & Dodd 价值投资方法论
仅供学习和研究使用
"""
        
        return summary

    @staticmethod
    def export_to_pdf(company_info: Dict, av_summary: Dict, epv_summary: Dict, fv_analysis: Optional[Dict] = None) -> bytes:
        """
        导出简易 PDF 报告（全文本）
        依赖 reportlab（requirements 已包含）
        """
        from reportlab.pdfgen import canvas

        output = io.BytesIO()
        c = canvas.Canvas(output)
        y = 800
        line_h = 16
        def _line(text):
            nonlocal y
            c.drawString(40, y, text)
            y -= line_h
        _line("Value Investing Report")
        _line(f"Company: {company_info.get('name', 'N/A')}")
        _line(f"Industry: {company_info.get('industry', 'N/A')}")
        _line(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        y -= line_h
        _line(f"AV: ${av_summary.get('total_av', 0)/1e9:.2f}B")
        _line(f"EPV: ${epv_summary.get('epv', 0)/1e9:.2f}B")
        if fv_analysis:
            _line(f"FV: ${fv_analysis.get('franchise_value', 0)/1e9:.2f}B")
        _line(f"Market Cap: ${av_summary.get('market_cap', 0)/1e9:.2f}B")
        y -= line_h
        _line(f"AV/Market: {av_summary.get('av_to_market_cap', 0):.1%}")
        _line(f"EPV/Market: {epv_summary.get('epv_to_market_cap', 0):.1%}")
        if fv_analysis:
            _line(f"Margin of Safety: {fv_analysis.get('margin_of_safety', 0):.1%}")
        c.showPage()
        c.save()
        output.seek(0)
        return output.getvalue()
    
    @staticmethod
    def get_filename(ticker: str, file_type: str = 'excel') -> str:
        """
        生成文件名
        
        Args:
            ticker: 股票代码
            file_type: 文件类型 ('excel' 或 'pdf')
            
        Returns:
            str: 文件名
        """
        date_str = datetime.now().strftime('%Y%m%d')
        
        if file_type == 'excel':
            return f"{ticker}_valuation_{date_str}.xlsx"
        elif file_type == 'pdf':
            return f"{ticker}_report_{date_str}.pdf"
        else:
            return f"{ticker}_summary_{date_str}.txt"
