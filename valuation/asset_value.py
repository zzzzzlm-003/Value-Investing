"""
Asset Value (AV) 计算模块
基于 Graham & Dodd 方法论
"""
import numpy as np
from typing import Dict, List, Optional, Tuple
from .adjustments import AdjustmentCalculator


class AssetValueCalculator:
    """资产价值计算类"""
    
    def __init__(self, financial_data: Dict, params: Dict = None):
        """
        初始化AV计算器
        
        Args:
            financial_data: 处理后的财务数据
            params: 计算参数
        """
        self.data = financial_data
        self.params = params or {}
        self.adjuster = AdjustmentCalculator()
        
        # 从配置获取默认参数
        from config.settings import DEFAULT_PARAMS, PPE_ADJUSTMENT_PARAMS, PPE_GROSS_RATIOS
        self.default_params = DEFAULT_PARAMS
        self.ppe_params = PPE_ADJUSTMENT_PARAMS
        self.ppe_ratios = PPE_GROSS_RATIOS
        
        self.results = {}
    
    def calculate(self, user_adjustments: Dict = None) -> Dict:
        """
        计算Asset Value
        
        Args:
            user_adjustments: 用户自定义调整参数
            
        Returns:
            Dict: AV计算结果
        """
        adjustments = user_adjustments or {}
        
        # 1. 获取账面权益
        book_equity = self._get_book_equity()
        
        # 2. 流动资产调整（应收坏账、存货LIFO/FIFO等）
        current_assets_adjustment = self._calculate_current_assets_adjustment(adjustments)
        
        # 3. PPE调整
        ppe_adjustment, ppe_details = self._calculate_ppe_adjustment(adjustments)
        
        # 4. 商誉调整
        goodwill_adjustment, goodwill_explanation = self._calculate_goodwill_adjustment(adjustments)
        
        # 5. 经营租赁使用权资产（BS 有则直接计入，无则按租赁费用资本化估算）
        operating_lease_adj = self._calculate_operating_lease_adjustment(adjustments)
        
        # 6. 无形资产
        brand_value = self._calculate_brand_value(adjustments)
        workforce_value = self._calculate_workforce_value(adjustments)
        product_value = self._calculate_product_portfolio_value(adjustments)
        
        # 7. 权益法投资与养老金等负债调整
        equity_method_adjustment = self._calculate_equity_method_adjustment(adjustments)
        pension_adjustment = self._calculate_pension_adjustment(adjustments)
        
        # 8. 计算总AV
        total_av = (
            book_equity
            + current_assets_adjustment
            + ppe_adjustment
            + goodwill_adjustment
            + operating_lease_adj
            + equity_method_adjustment
            + pension_adjustment
            + brand_value
            + workforce_value
            + product_value
        )
        
        # 保存结果
        self.results = {
            'book_equity': book_equity,
            'current_assets_adjustment': current_assets_adjustment,
            'ppe_adjustment': ppe_adjustment,
            'ppe_details': ppe_details,
            'goodwill_adjustment': goodwill_adjustment,
            'goodwill_explanation': goodwill_explanation,
            'operating_lease_adjustment': operating_lease_adj,
            'equity_method_adjustment': equity_method_adjustment,
            'pension_adjustment': pension_adjustment,
            'brand_value': brand_value,
            'workforce_value': workforce_value,
            'product_portfolio_value': product_value,
            'total_av': total_av,
            'components': {
                '账面权益': book_equity,
                '流动资产调整': current_assets_adjustment,
                'PPE调整': ppe_adjustment,
                '商誉调整': goodwill_adjustment,
                '经营租赁(ROU)': operating_lease_adj,
                '权益法投资调整': equity_method_adjustment,
                '养老金/表外负债调整': pension_adjustment,
                '品牌价值': brand_value,
                '员工价值': workforce_value,
                '产品组合': product_value,
            }
        }
        
        return self.results
    
    def _get_book_equity(self) -> float:
        """获取账面权益"""
        bs = self.data.get('balance_sheet', {})
        return bs.get('total_equity', 0)
    
    def _calculate_current_assets_adjustment(self, adjustments: Dict) -> float:
        """
        计算流动资产调整（应收坏账、存货LIFO/FIFO等）。
        课堂口径强调需要人工判断，默认不做调整。
        """
        receivables_adj = adjustments.get('receivables_default_adjustment')
        inventory_adj = adjustments.get('inventory_lifo_fifo_adjustment')
        total = 0.0
        if receivables_adj is not None:
            total += float(receivables_adj)
        if inventory_adj is not None:
            total += float(inventory_adj)
        return total
    
    def _calculate_equity_method_adjustment(self, adjustments: Dict) -> float:
        """
        计算权益法投资调整（如关联企业公允价值调整）。
        默认不调整，需用户手动输入。
        """
        val = adjustments.get('equity_method_adjustment')
        return float(val) if val is not None else 0.0
    
    def _calculate_pension_adjustment(self, adjustments: Dict) -> float:
        """
        计算养老金/表外负债调整（例如 underfunded pension）。
        默认不调整，需用户手动输入（一般为负值）。
        """
        val = adjustments.get('underfunded_pension')
        return float(val) if val is not None else 0.0
    
    def _calculate_ppe_adjustment(self, adjustments: Dict) -> Tuple[float, Dict]:
        """
        计算PPE调整（Lecture 2：分项系数得调整后净值，调整额 = 调整后净值 - 报表净值，可为正如 +46b）
        """
        if adjustments.get('manual_ppe_adjustment') is not None:
            return float(adjustments['manual_ppe_adjustment']), {'manual': True}
        
        bs = self.data.get('balance_sheet', {})
        ppe_net = float(bs.get('ppe_net', 0) or 0)
        ppe_gross = float(bs.get('ppe_gross', 0) or 0)
        if ppe_net <= 0:
            return 0, {'reason': '无PPE净值数据'}
        if not ppe_gross or ppe_gross <= 0:
            ppe_gross = ppe_net * 1.5
        ratios = self.ppe_ratios
        if 'ppe_components' in adjustments:
            ppe_components = adjustments['ppe_components']
        else:
            ppe_components = {
                'land': ppe_gross * ratios.get('land', 0.08),
                'building': ppe_gross * ratios.get('building', 0.51),
                'fixtures': ppe_gross * ratios.get('fixtures', 0.33),
                'equipment': ppe_gross * ratios.get('equipment', 0.08),
                'cip': ppe_gross * ratios.get('cip', 0.06),
            }
        market = self.data.get('company_info', {}).get('country', 'US')
        market_code = 'us' if (market == 'United States' or market == 'US') else 'china'
        factors = self.ppe_params.get(market_code, self.ppe_params['us'])
        total_adj, details = self.adjuster.calculate_ppe_adjustment(
            ppe_components, factors, reported_ppe_net=ppe_net
        )
        # 防护：调整额不应严重为负（课件 WMT 约 +46B），-30B 以下视为数据错误，按 0 处理
        if total_adj < -30e9:
            details['capped'] = True
            details['original_adj'] = total_adj
            total_adj = 0
        return total_adj, details
    
    def _calculate_goodwill_adjustment(self, adjustments: Dict) -> Tuple[float, str]:
        """
        商誉调整（课件）：调整额 = -(当前商誉 - 未消化部分)；未消化 = 收购产生尚未整合/摊销的商誉
        """
        bs = self.data.get('balance_sheet', {})
        current_goodwill = float(bs.get('goodwill', 0) or 0)
        # 未消化商誉（可由用户输入或从收购历史推算）
        not_digested = adjustments.get('goodwill_not_digested')
        if not_digested is not None:
            not_digested = max(0, min(float(not_digested), current_goodwill))  # 限制在 [0, 当前商誉]，避免出现“加回”的困惑
            adj = -(current_goodwill - not_digested)
            return adj, f"当前商誉 ${current_goodwill/1e9:.1f}B，未消化 ${not_digested/1e9:.1f}B，调整额 ${adj/1e9:.1f}B"
        remove_goodwill = adjustments.get('remove_goodwill')
        if remove_goodwill is not None and remove_goodwill > 0:
            remove_goodwill = min(remove_goodwill, current_goodwill)  # 剔除额不超过当前商誉
            not_digested = current_goodwill - remove_goodwill
            adj = -(current_goodwill - not_digested)
            return adj, f"剔除收购商誉 ${remove_goodwill/1e9:.1f}B，调整额 ${adj/1e9:.1f}B"
        return 0, "未做商誉调整"
    
    def _calculate_operating_lease_adjustment(self, adjustments: Dict) -> float:
        """
        经营租赁使用权资产：BS 已有 ROU 则已含在账面权益（调整额 0）。
        课件未要求重估 ROU，默认不估算；仅允许手动输入调整额。
        """
        bs = self.data.get('balance_sheet', {})
        rou = float(bs.get('right_of_use_assets', 0) or 0)
        if rou > 0:
            return 0  # 已在账面，不重复计入
        if adjustments.get('operating_lease_asset') is not None:
            return float(adjustments['operating_lease_asset'])
        return 0
    
    def _calculate_brand_value(self, adjustments: Dict) -> float:
        """
        品牌价值：三种方法可选（课件图五）
        - discounted_marketing: 营销费用折现 = 年营销费用/折现率
        - royalty: 特许权费法
        - marketing: 营销公司法 EVA×RoB×PV
        """
        income = self.data.get('income_statement', {})
        revenue = self._safe_single(income.get('revenue', 0))
        discount_rate = adjustments.get('discount_rate', self.default_params['discount_rate'])
        growth_rate = adjustments.get('growth_rate', self.default_params['growth_rate'])
        method = adjustments.get('brand_method', 'marketing')
        market_cap = self.data.get('market_data', {}).get('market_cap', 0) or 0
        company_info = self.data.get('company_info', {})
        sector = company_info.get('sector', '')
        industry = company_info.get('industry', '')
        
        def _cap_brand_value(val: float) -> float:
            caps = []
            if market_cap and market_cap > 0:
                caps.append(market_cap * 0.20)
            if revenue and revenue > 0:
                caps.append(revenue * 0.50)
            if not caps:
                return val
            return min(val, min(caps))
        
        if method == 'discounted_marketing':
            sg = self._safe_single(income.get('sg_and_a', 0))
            marketing = sg * 0.35 if sg else 0  # 营销费用约为 SG&A 一部分
            if marketing <= 0 or discount_rate <= 0:
                return 0
            return _cap_brand_value(marketing / discount_rate)
        if method == 'royalty':
            if revenue <= 0:
                return 0
            royalty_rate = adjustments.get('brand_royalty_rate')
            if royalty_rate is None:
                low, high = self.adjuster.get_industry_royalty_rate_range(sector, industry)
                if low > 0 and high > 0:
                    royalty_rate = (low + high) / 2
                else:
                    royalty_rate = self.default_params['brand_royalty_rate']
            val = self.adjuster.calculate_brand_value_royalty(
                revenue, float(royalty_rate), discount_rate, growth_rate
            )
            return _cap_brand_value(val)
        # marketing: EVA × RoB × PV factor（课件 $47bn 量级）
        brand_role = adjustments.get('brand_role', self.default_params['brand_role'])
        bs = self.data.get('balance_sheet', {})
        oi = self._safe_single(income.get('operating_income', 0))
        total_assets = float(bs.get('total_assets', 0) or 0)
        acc_dep = float(bs.get('accumulated_depreciation', 0) or 0)
        ap = float(bs.get('accounts_payable', 0) or 0)
        accr = float(bs.get('accrued_liabilities', 0) or 0)
        wacc = adjustments.get('discount_rate', 0.07)
        ic = total_assets + acc_dep - ap - accr
        if ic <= 0:
            ic = max(total_assets * 0.5, 1)
        roic = oi / ic if ic else 0
        eva = (roic - wacc) * ic if roic else 0
        if discount_rate <= growth_rate or discount_rate < 0.01:
            pv_factor = 20
        else:
            pv_factor = 1 / (discount_rate - growth_rate)
        pv_factor = min(pv_factor, 50)  # 避免永续因子过大导致品牌价值远超市值
        return _cap_brand_value(max(0, eva * brand_role * pv_factor))
    
    def _safe_single(self, x):
        if isinstance(x, (list, tuple)) and len(x) > 0:
            x = x[0]
        return float(x or 0)
    
    def _calculate_workforce_value(self, adjustments: Dict) -> float:
        """
        计算员工队伍价值
        
        Args:
            adjustments: 用户调整参数
            
        Returns:
            float: 员工队伍价值
        """
        income = self.data.get('income_statement', {})
        
        # 估算员工薪酬（通常是SG&A的一部分）
        sg_and_a = income.get('sg_and_a', 0)
        cogs = income.get('cogs', 0)
        
        # 确保是数字类型
        if isinstance(sg_and_a, (list, tuple)) and len(sg_and_a) > 0:
            sg_and_a = sg_and_a[0]
        if isinstance(cogs, (list, tuple)) and len(cogs) > 0:
            cogs = cogs[0]
        
        sg_and_a = float(sg_and_a) if sg_and_a else 0
        cogs = float(cogs) if cogs else 0
        
        # 粗略估计：SG&A的40% + COGS的20% 是员工相关成本
        total_compensation = sg_and_a * 0.4 + cogs * 0.2
        
        # 如果用户提供了员工总数和平均工资
        if 'employee_count' in adjustments and 'avg_salary' in adjustments:
            total_compensation = (adjustments['employee_count'] *
                                adjustments['avg_salary'])
        
        training_ratio = adjustments.get('workforce_cost_ratio',
                                        self.default_params['workforce_cost_ratio'])
        
        return self.adjuster.calculate_workforce_value(total_compensation, training_ratio)
    
    def _calculate_product_portfolio_value(self, adjustments: Dict) -> float:
        """
        计算产品组合价值
        
        Args:
            adjustments: 用户调整参数
            
        Returns:
            float: 产品组合价值
        """
        income = self.data.get('income_statement', {})
        
        # 获取历年R&D支出
        rd_expenses = income.get('rd_expense', [])
        
        if not rd_expenses or sum(rd_expenses) == 0:
            return 0
        
        depreciation_rate = adjustments.get('rd_depreciation_rate',
                                           self.default_params['rd_depreciation_rate'])
        
        return self.adjuster.calculate_product_portfolio_value(rd_expenses, depreciation_rate)
    
    def get_av_per_share(self) -> float:
        """
        计算每股AV
        
        Returns:
            float: 每股AV
        """
        if not self.results:
            self.calculate()
        
        market_data = self.data.get('market_data', {})
        shares = market_data.get('shares_outstanding', 0)
        
        if shares > 0:
            return self.results['total_av'] / shares
        return 0
    
    def get_av_summary(self) -> Dict:
        """
        获取AV计算摘要
        
        Returns:
            Dict: 摘要信息
        """
        if not self.results:
            self.calculate()
        
        market_data = self.data.get('market_data', {})
        market_cap = market_data.get('market_cap', 0)
        
        return {
            'total_av': self.results['total_av'],
            'av_per_share': self.get_av_per_share(),
            'market_cap': market_cap,
            'av_to_market_cap': (self.results['total_av'] / market_cap
                                if market_cap > 0 else 0),
            'components': self.results['components'],
        }
