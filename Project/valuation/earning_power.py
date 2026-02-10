"""
Earning Power Value (EPV) 计算模块
基于 Graham & Dodd 方法论
"""
import numpy as np
from typing import Dict, List, Optional, Tuple
from .adjustments import AdjustmentCalculator


class EarningPowerCalculator:
    """盈利能力价值计算类"""
    
    def __init__(self, financial_data: Dict, params: Dict = None):
        """
        初始化EPV计算器
        
        Args:
            financial_data: 处理后的财务数据
            params: 计算参数
        """
        self.data = financial_data
        self.params = params or {}
        self.adjuster = AdjustmentCalculator()
        
        # 从配置获取默认参数
        from config.settings import DEFAULT_PARAMS
        self.default_params = DEFAULT_PARAMS
        
        self.results = {}
    
    def calculate(self, user_adjustments: Dict = None) -> Dict:
        """
        计算Earning Power Value
        
        Args:
            user_adjustments: 用户自定义调整参数
            
        Returns:
            Dict: EPV计算结果
        """
        adjustments = user_adjustments or {}
        
        # 1. 获取平滑后的营业利润
        smoothed_margin = self._calculate_smoothed_operating_margin(adjustments)
        current_revenue = self._get_current_revenue()
        smoothed_operating_income = smoothed_margin * current_revenue
        
        # 2. 非经常性项目调整
        extraordinary_adj = self._calculate_extraordinary_adjustment(adjustments)
        
        # 3. 折旧调整
        depreciation_adj = self._calculate_depreciation_adjustment(adjustments)
        
        # 4. 增长性支出调整
        growth_expense_adj = self._calculate_growth_expense_adjustment(adjustments)
        
        # 5. 计算调整后营业利润
        adjusted_operating_income = (smoothed_operating_income +
                                    extraordinary_adj +
                                    depreciation_adj +
                                    growth_expense_adj)
        
        # 6. 计算税后NOPAT
        tax_rate = self._get_tax_rate(adjustments)
        adjusted_nopat = adjusted_operating_income * (1 - tax_rate)
        
        # 7. 计算WACC
        wacc = self._calculate_wacc(adjustments)
        
        # 8. 计算EPV
        epv = adjusted_nopat / wacc if wacc > 0 else 0
        
        # 保存结果
        self.results = {
            'current_revenue': current_revenue,
            'smoothed_margin': smoothed_margin,
            'smoothed_operating_income': smoothed_operating_income,
            'extraordinary_adjustment': extraordinary_adj,
            'depreciation_adjustment': depreciation_adj,
            'growth_expense_adjustment': growth_expense_adj,
            'adjusted_operating_income': adjusted_operating_income,
            'tax_rate': tax_rate,
            'adjusted_nopat': adjusted_nopat,
            'wacc': wacc,
            'epv': epv,
            'components': {
                '平滑营业利润': smoothed_operating_income,
                '非经常项调整': extraordinary_adj,
                '折旧调整': depreciation_adj,
                '增长支出调整': growth_expense_adj,
            }
        }
        
        return self.results
    
    def get_wacc_breakdown(self, adjustments: Dict = None) -> Dict:
        """
        返回WACC计算明细（Lecture 3 第13页格式）
        
        Returns:
            Dict: 包含 1-16 行各项数值，便于展示表格和手动覆盖
        """
        adj = adjustments or self.params or {}
        market_data = self.data.get('market_data', {})
        bs = self.data.get('balance_sheet', {})
        
        # 1. Market equity ($US mn)
        market_cap = adj.get('market_equity', market_data.get('market_cap', 0))
        if market_cap == 0:
            market_cap = market_data.get('market_cap', 0)
        
        # 2-5. Debt components
        long_term_debt = bs.get('long_term_debt', 0) or 0
        short_term_debt = bs.get('short_term_debt', 0) or 0
        debt_current_portion = adj.get('debt_current_portion', short_term_debt * 0.5)  # 估算
        leases = adj.get('leases', bs.get('long_term_debt', 0) * 0.0)  # 若无单独披露则为0
        leases_current = adj.get('leases_current', 0)
        
        total_debt = (adj.get('total_debt') or 
                     (long_term_debt + short_term_debt + float(leases) + float(leases_current)))
        
        # 若用户未覆盖，用 2+3+4+5
        if 'total_debt' not in adj:
            total_debt = long_term_debt + debt_current_portion + leases + leases_current
        
        # 6
        total_debt = max(0, total_debt)
        
        # 7-8. Weights
        total_val = market_cap + total_debt
        we = market_cap / total_val if total_val > 0 else 1.0
        wd = total_debt / total_val if total_val > 0 else 0.0
        
        # 9-12. Cost of equity (CAPM)
        beta = adj.get('beta', market_data.get('beta', 1.0))
        market_premium_pct = (adj.get('market_risk_premium') or self.default_params.get('market_risk_premium', 0.06)) * 100
        from data.api_fetcher import DataFetcher
        try:
            ticker = adj.get('ticker', 'WMT')
            fetcher = DataFetcher(ticker)
            treasury_10y = fetcher.get_risk_free_rate() * 100
        except Exception:
            treasury_10y = 4.3
        if 'treasury_10y' in adj:
            treasury_10y = adj['treasury_10y']
        if 'risk_free_rate' in adj:
            treasury_10y = adj['risk_free_rate'] * 100
        
        cost_of_equity_pct = treasury_10y + beta * market_premium_pct
        
        # 13-15. Cost of debt
        net_borrowing_cost_pct = adj.get('net_borrowing_cost', 3.9)
        tax_rate_pct = self._get_tax_rate(adj) * 100
        cost_of_debt_pct = net_borrowing_cost_pct * (1 - tax_rate_pct / 100)
        
        # 16. WACC
        wacc_pct = we * cost_of_equity_pct + wd * cost_of_debt_pct
        
        return {
            'market_equity_mn': market_cap / 1e6,
            'debt_mn': long_term_debt / 1e6,
            'debt_current_portion_mn': debt_current_portion / 1e6,
            'leases_mn': leases / 1e6,
            'leases_current_mn': leases_current / 1e6,
            'total_debt_mn': total_debt / 1e6,
            'we': we,
            'wd': wd,
            'beta': beta,
            'market_premium_pct': market_premium_pct,
            'treasury_10y_pct': treasury_10y,
            'cost_of_equity_pct': cost_of_equity_pct,
            'net_borrowing_cost_pct': net_borrowing_cost_pct,
            'tax_rate_pct': tax_rate_pct,
            'cost_of_debt_pct': cost_of_debt_pct,
            'wacc_pct': wacc_pct,
            'wacc': wacc_pct / 100,
        }
    
    def get_epv_detailed_breakdown(self, adjustments: Dict = None) -> Dict:
        """
        返回EPV各调整项的明细（原始值、调整值、依据），便于展示和手动输入
        """
        if not self.results:
            self.calculate(adjustments)
        
        adj = adjustments or {}
        income = self.data.get('income_statement', {})
        cf = self.data.get('cash_flow', {})
        
        def _single(v):
            if isinstance(v, (list, tuple)) and len(v) > 0:
                return float(v[0]) if v[0] else 0
            return float(v) if v else 0
        
        revenue = self.results['current_revenue']
        op_income = self.results['smoothed_operating_income']
        tax_rate = self.results['tax_rate']
        
        # 原始营业利润（平滑后）
        original_op_income = op_income
        
        # 各调整项明细
        extra_orig = 0
        extra_adj = self.results['extraordinary_adjustment']
        
        dep_report = _single(income.get('depreciation', 0))
        dep_adj = self.results['depreciation_adjustment']
        
        marketing_expense = _single(income.get('sg_and_a', 0)) * 0.35
        growth_adj = self.results['growth_expense_adjustment']
        
        # 非经常性：尝试从利润表取“其他/重组”等（若数据源有）；否则建议 0 并提示查阅年报
        suggested_extra = 0
        try:
            other_exp = income.get('other_operating_expenses') or income.get('other_expenses')
            if other_exp is not None:
                v = other_exp[0] if isinstance(other_exp, (list, tuple)) else other_exp
                if v and abs(float(v)) > 1e6:
                    suggested_extra = float(v)  # 加回一次性费用为正
        except Exception:
            pass
        
        adjustments_detail = [
            {
                'name': '非经常性项目',
                'original_value': extra_orig,
                'adjustment_value': extra_adj,
                'suggested_value': suggested_extra,
                'rationale': '加回一次性损失（如诉讼、重组、Settlement）；扣除一次性利得。参见年报附注 Other/(gains)/losses、Restructuring。',
                'key': 'extraordinary_adjustment',
            },
            {
                'name': '过度/不足折旧',
                'original_value': dep_report,
                'adjustment_value': dep_adj,
                'suggested_value': dep_adj,
                'rationale': 'Maintenance capex vs 报表折旧。过度折旧时加回（Buffett: 折旧是真实成本）。',
                'key': 'depreciation_adjustment',
            },
            {
                'name': '增长性支出（营销/品牌）',
                'original_value': marketing_expense,
                'adjustment_value': growth_adj,
                'suggested_value': growth_adj,
                'rationale': 'Method1: 品牌价值/15年=维持性摊销，超出部分为增长支出加回。Method2: 营收×0.35%为品牌增长投入（Lecture3 p28）。',
                'key': 'growth_expense_adjustment',
            },
        ]
        
        adjusted_op = self.results['adjusted_operating_income']
        adjusted_nopat = self.results['adjusted_nopat']
        wacc = self.results['wacc']
        epv = self.results['epv']
        
        market_data = self.data.get('market_data', {})
        bs = self.data.get('balance_sheet', {})
        cash = _single(bs.get('cash', 0)) if isinstance(bs, dict) else 0
        total_debt = (bs.get('long_term_debt', 0) or 0) + (bs.get('short_term_debt', 0) or 0)
        
        return {
            'formula': 'EPV = Adjusted NOPAT / r',
            'original_operating_income': original_op_income,
            'adjustments_detail': adjustments_detail,
            'adjusted_operating_income': adjusted_op,
            'tax_rate': tax_rate,
            'adjusted_nopat': adjusted_nopat,
            'wacc': wacc,
            'epv_operating': epv,
            'non_operational_cash': cash,
            'debt': total_debt,
            'epv_equity': epv + cash - total_debt,
            'revenue': revenue,
            'smoothed_margin': self.results['smoothed_margin'],
        }
    
    def _get_current_revenue(self) -> float:
        """获取最新年度营业收入"""
        income = self.data.get('income_statement', {})
        revenue = income.get('revenue', 0)
        
        # 确保是数字类型
        if isinstance(revenue, (list, tuple)) and len(revenue) > 0:
            revenue = revenue[0]
        
        return float(revenue) if revenue else 0
    
    def _calculate_smoothed_operating_margin(self, adjustments: Dict) -> float:
        """
        计算平滑后的营业利润率。支持 simple（算术平均）、weighted（近期权重大）、ttm（仅最近一年）。
        """
        income = self.data.get('income_statement', {})
        revenues = income.get('revenue', [])
        operating_incomes = income.get('operating_income', [])
        # 兼容单年标量：若为标量则转为单元素列表，避免 len()/索引报错
        if isinstance(revenues, (int, float)):
            revenues = [revenues] if revenues else []
        if isinstance(operating_incomes, (int, float)):
            operating_incomes = [operating_incomes] if operating_incomes else []
        if not revenues or not operating_incomes:
            return 0
        
        margins = []
        for i in range(min(len(revenues), len(operating_incomes))):
            if revenues[i] and revenues[i] > 0:
                margins.append(operating_incomes[i] / revenues[i])
            else:
                margins.append(0.0)
        
        if not margins:
            return 0
        
        smoothing_years = adjustments.get('smoothing_years', self.default_params['smoothing_years'])
        method = adjustments.get('smoothing_method', 'simple')
        n = min(smoothing_years, len(margins))
        relevant = margins[:n]
        
        if method == 'ttm':
            return float(relevant[0]) if relevant else 0
        if method == 'weighted':
            # 权重 [1, 2, ..., n]，越近年份权重越大
            weights = np.array(list(range(1, n + 1)), dtype=float)
            return float(np.average(relevant, weights=weights))
        return float(np.mean(relevant))
    
    def _calculate_extraordinary_adjustment(self, adjustments: Dict) -> float:
        """
        计算非经常性项目调整
        
        Args:
            adjustments: 用户调整参数
            
        Returns:
            float: 调整金额（正数=加回，负数=扣除）
        """
        # 用户可以手动输入非经常性项目
        extraordinary_items = adjustments.get('extraordinary_items', [])
        
        total_adjustment = sum(item.get('amount', 0) for item in extraordinary_items)
        
        return total_adjustment
    
    def _calculate_depreciation_adjustment(self, adjustments: Dict) -> float:
        """
        计算折旧调整（过度折旧）
        
        Args:
            adjustments: 用户调整参数
            
        Returns:
            float: 过度折旧额（加回到营业利润）
        """
        income = self.data.get('income_statement', {})
        cf = self.data.get('cash_flow', {})
        bs = self.data.get('balance_sheet', {})
        
        # 获取折旧：优先利润表，缺则现金流量表，再缺则 PPE_Net*0.08（约 12 年寿命），绝不能为 0 导致后续逻辑异常
        depreciation = income.get('depreciation', 0)
        if isinstance(depreciation, (list, tuple)) and len(depreciation) > 0:
            depreciation = depreciation[0]
        depreciation = float(depreciation) if depreciation else 0
        if depreciation <= 0:
            dep_cf = cf.get('depreciation', 0) or cf.get('depreciation_and_amortization', 0) or cf.get('Depreciation And Amortization', 0) or cf.get('Depreciation & Amortization', 0)
            if isinstance(dep_cf, (list, tuple)) and len(dep_cf) > 0:
                dep_cf = dep_cf[0]
            depreciation = float(dep_cf) if dep_cf else 0
        if depreciation <= 0:
            ppe_net = bs.get('ppe_net', 0)
            ppe_net = float(ppe_net) if ppe_net else 0
            if ppe_net > 0:
                depreciation = ppe_net * 0.08  # 假设 12.5 年寿命 ≈ 8%/年
        capex = cf.get('capex', 0)
        if isinstance(capex, (list, tuple)) and len(capex) > 0:
            capex = capex[0]
        capex = float(capex) if capex else 0
        ppe_net = float(bs.get('ppe_net', 0) or 0)
        
        # 计算营收增长率
        revenues = income.get('revenue', [])
        if len(revenues) >= 2:
            revenue_growth = ((revenues[0] - revenues[1]) / revenues[1]
                            if revenues[1] > 0 else 0)
        else:
            revenue_growth = 0
        
        # 使用adjustment calculator
        over_depreciation = self.adjuster.calculate_depreciation_adjustment(
            depreciation, capex, revenue_growth, ppe_net
        )
        
        # 用户可以覆盖
        if 'depreciation_adjustment' in adjustments:
            over_depreciation = adjustments['depreciation_adjustment']
        
        return over_depreciation
    
    def _get_sector_growth_ratios(self, sector: str) -> Tuple[float, float]:
        """按行业返回 (R&D视为增长的比例, Marketing视为增长的比例)。"""
        s = (sector or '').strip().lower()
        if 'technology' in s or 'tech' in s:
            return (0.80, 0.20)   # Technology: 80% R&D, 20% Marketing
        if 'consumer' in s or 'retail' in s:   # Consumer Cyclical/Defensive 或 Retail (e.g. WMT)
            return (0.20, 0.50)   # 50% Marketing
        return (0.20, 0.20)       # Manufacturing, Other: 保守 20%, 20%
    
    def _calculate_growth_expense_adjustment(self, adjustments: Dict) -> float:
        """
        增长性支出调整：按 Sector 动态比例（Technology 80% R&D/20% Mkt；Consumer 20% R&D/50% Mkt；其他 20%/20%）。
        用户可通过 growth_expense_adjustment 或 rd_growth_ratio 覆盖。
        """
        if 'growth_expense_adjustment' in adjustments:
            return float(adjustments['growth_expense_adjustment'])
        
        income = self.data.get('income_statement', {})
        company_info = self.data.get('company_info', {})
        sector = adjustments.get('sector') or company_info.get('sector', '') or company_info.get('industry', '')
        rd_pct, mkt_pct = self._get_sector_growth_ratios(sector)
        if adjustments.get('rd_growth_ratio') is not None and 0 <= adjustments['rd_growth_ratio'] <= 1:
            rd_pct = adjustments['rd_growth_ratio']
        
        revenue = self._get_current_revenue()
        sg_and_a = income.get('sg_and_a', 0)
        if isinstance(sg_and_a, (list, tuple)) and len(sg_and_a) > 0:
            sg_and_a = sg_and_a[0]
        marketing_expense = float(sg_and_a or 0) * 0.35
        
        rd_expenses = income.get('rd_expense', [])
        current_rd = rd_expenses[0] if (isinstance(rd_expenses, (list, tuple)) and rd_expenses) else (rd_expenses if isinstance(rd_expenses, (int, float)) else 0)
        current_rd = float(current_rd or 0)
        
        total_growth_expense = (current_rd * rd_pct) + (marketing_expense * mkt_pct)
        return total_growth_expense
    
    def _get_tax_rate(self, adjustments: Dict) -> float:
        """
        获取税率
        
        Args:
            adjustments: 用户调整参数
            
        Returns:
            float: 税率
        """
        # 用户指定税率
        if 'tax_rate' in adjustments:
            return adjustments['tax_rate']
        
        # 根据市场确定默认税率
        company_info = self.data.get('company_info', {})
        country = company_info.get('country', 'United States')
        
        if country == 'United States':
            return self.default_params['tax_rate_us']
        elif country == 'China':
            return self.default_params['tax_rate_china']
        elif country == 'Hong Kong':
            return self.default_params['tax_rate_hk']
        else:
            return self.default_params['tax_rate_us']
    
    def _calculate_wacc(self, adjustments: Dict) -> float:
        """
        计算加权平均资本成本(WACC)
        
        Args:
            adjustments: 用户调整参数（可含 'wacc' 直接覆盖）
            
        Returns:
            float: WACC
        """
        if 'wacc' in adjustments and adjustments['wacc'] is not None:
            w = adjustments['wacc']
            return float(w) if w <= 1 else w / 100  # 支持小数或百分数
        market_data = self.data.get('market_data', {})
        bs = self.data.get('balance_sheet', {})
        
        # 1. 获取市值和债务
        market_cap = market_data.get('market_cap', 0)
        long_term_debt = bs.get('long_term_debt', 0)
        short_term_debt = bs.get('short_term_debt', 0)
        total_debt = long_term_debt + short_term_debt
        
        if market_cap == 0:
            return self.default_params['discount_rate']
        
        # 2. 计算权重
        total_value = market_cap + total_debt
        weight_equity = market_cap / total_value if total_value > 0 else 1.0
        weight_debt = total_debt / total_value if total_value > 0 else 0.0
        
        # 3. 计算权益成本 (CAPM)
        # 优先使用用户选择的Beta
        beta = adjustments.get('beta', market_data.get('beta', 1.0))
        
        # 获取无风险利率
        if 'risk_free_rate' in adjustments:
            risk_free_rate = adjustments['risk_free_rate']
        else:
            # 从DataFetcher获取
            from data.api_fetcher import DataFetcher
            ticker = adjustments.get('ticker', 'WMT')
            fetcher = DataFetcher(ticker)
            risk_free_rate = fetcher.get_risk_free_rate()
        
        market_premium = adjustments.get('market_risk_premium',
                                        self.default_params['market_risk_premium'])
        
        cost_of_equity = risk_free_rate + beta * market_premium
        
        # 4. 计算债务成本
        # 简化：假设债务成本 = 无风险利率 + 信用利差
        credit_spread = 0.02  # 2%信用利差
        cost_of_debt = risk_free_rate + credit_spread
        
        # 用户可以指定
        if 'cost_of_debt' in adjustments:
            cost_of_debt = adjustments['cost_of_debt']
        
        # 5. 税率
        tax_rate = self._get_tax_rate(adjustments)
        
        # 6. 计算WACC
        wacc = (weight_equity * cost_of_equity +
               weight_debt * cost_of_debt * (1 - tax_rate))
        
        return wacc
    
    def get_epv_per_share(self) -> float:
        """
        计算每股EPV
        
        Returns:
            float: 每股EPV
        """
        if not self.results:
            self.calculate()
        
        market_data = self.data.get('market_data', {})
        shares = market_data.get('shares_outstanding', 0)
        
        if shares > 0:
            return self.results['epv'] / shares
        return 0
    
    def get_epv_summary(self) -> Dict:
        """
        获取EPV计算摘要
        
        Returns:
            Dict: 摘要信息
        """
        if not self.results:
            self.calculate()
        
        market_data = self.data.get('market_data', {})
        market_cap = market_data.get('market_cap', 0)
        
        return {
            'epv': self.results['epv'],
            'epv_per_share': self.get_epv_per_share(),
            'market_cap': market_cap,
            'epv_to_market_cap': (self.results['epv'] / market_cap
                                 if market_cap > 0 else 0),
            'wacc': self.results['wacc'],
            'adjusted_nopat': self.results['adjusted_nopat'],
            'components': self.results['components'],
        }
    
    def get_sensitivity_analysis(self, wacc_range: Tuple[float, float] = (0.05, 0.10),
                                steps: int = 6) -> Dict:
        """
        WACC敏感性分析
        
        Args:
            wacc_range: WACC范围 (最小值, 最大值)
            steps: 计算步数
            
        Returns:
            Dict: 敏感性分析结果
        """
        if not self.results:
            self.calculate()
        
        adjusted_nopat = self.results['adjusted_nopat']
        
        wacc_values = np.linspace(wacc_range[0], wacc_range[1], steps)
        epv_values = [adjusted_nopat / wacc for wacc in wacc_values]
        
        return {
            'wacc_values': wacc_values.tolist(),
            'epv_values': epv_values,
            'current_wacc': self.results['wacc'],
            'current_epv': self.results['epv'],
        }
