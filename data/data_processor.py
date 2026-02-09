"""
数据处理模块 - 清洗和预处理财务数据
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple


class DataProcessor:
    """财务数据处理类"""
    
    def __init__(self, financial_data: Dict):
        """
        初始化数据处理器
        
        Args:
            financial_data: 从DataFetcher获取的财务数据字典
        """
        self.data = financial_data
        self.balance_sheet = financial_data.get('balance_sheet', pd.DataFrame())
        self.income_statement = financial_data.get('income_statement', pd.DataFrame())
        self.cash_flow = financial_data.get('cash_flow', pd.DataFrame())
        self.company_info = financial_data.get('company_info', {})
        self.market_data = financial_data.get('market_data', {})
    
    def get_value(self, df: pd.DataFrame, row_name: str, col_idx: int = 0, default: float = 0) -> float:
        """
        从DataFrame中安全获取值
        
        Args:
            df: DataFrame
            row_name: 行名（支持部分匹配）
            col_idx: 列索引
            default: 默认值
            
        Returns:
            float: 获取的值
        """
        if df.empty:
            return default
        
        try:
            # 尝试精确匹配
            if row_name in df.index:
                value = df.loc[row_name].iloc[col_idx]
                return float(value) if pd.notna(value) else default
            
            # 尝试模糊匹配
            matching_rows = [idx for idx in df.index if row_name.lower() in str(idx).lower()]
            if matching_rows:
                value = df.loc[matching_rows[0]].iloc[col_idx]
                return float(value) if pd.notna(value) else default
            
            return default
        except Exception as e:
            return default
    
    def extract_balance_sheet_items(self, year_idx: int = 0) -> Dict:
        """
        提取资产负债表关键项目
        
        Args:
            year_idx: 年份索引（0=最新年份）
            
        Returns:
            Dict: 资产负债表关键项目
        """
        bs = self.balance_sheet
        # PPE（课件：调整后净值 - 报表净值 = 调整额，WMT 约 +46B）
        # yfinance 常把 Gross 填在 Net PPE 行，导致调整额 -78B。必须校验：净值不能 >= 原值。
        ppe_gross_val = self.get_value(bs, 'Gross PPE', year_idx) or self.get_value(bs, 'Properties', year_idx)
        acc_dep = self.get_value(bs, 'Accumulated Depreciation', year_idx) or 0
        # 累计折旧在很多报表/数据源中以负数（contra-asset）呈现；统一转为正数幅度
        if acc_dep and acc_dep < 0:
            acc_dep = abs(acc_dep)
        ppe_net_val = self.get_value(bs, 'Net PPE', year_idx)
        # 无 Net PPE 或 API 误把 Gross 当 Net（净>=原）时，用 Gross - 累计折旧；无累计折旧时用经验比例
        if ppe_gross_val is not None and ppe_gross_val > 0:
            if acc_dep is not None and acc_dep > 0:
                estimated_net = max(0, ppe_gross_val - acc_dep)
            else:
                estimated_net = ppe_gross_val * 0.55  # 无累计折旧时：零售/重资产净/原约 0.5~0.6
            if not ppe_net_val:
                ppe_net_val = estimated_net
            elif ppe_net_val >= ppe_gross_val * 0.98:
                # 报表“净值”接近或大于原值，必为数据错误，用估算净值
                ppe_net_val = estimated_net

        return {
            # 资产
            'total_assets': self.get_value(bs, 'Total Assets', year_idx),
            'current_assets': self.get_value(bs, 'Current Assets', year_idx),
            'cash': self.get_value(bs, 'Cash', year_idx),
            'accounts_receivable': self.get_value(bs, 'Accounts Receivable', year_idx),
            'inventory': self.get_value(bs, 'Inventory', year_idx),
            'ppe_gross': ppe_gross_val,
            'accumulated_depreciation': acc_dep,
            'ppe_net': ppe_net_val if ppe_net_val else None,
            # 无形资产
            'goodwill': self.get_value(bs, 'Goodwill', year_idx),
            'intangible_assets': self.get_value(bs, 'Intangible Assets', year_idx) or \
                               self.get_value(bs, 'Other Intangible Assets', year_idx),
            # 经营租赁使用权资产 (ASC 842)
            'right_of_use_assets': self.get_value(bs, 'Operating Lease Right Of Use Asset', year_idx) or
                                  self.get_value(bs, 'Right Of Use Asset', year_idx) or
                                  self.get_value(bs, 'Operating Lease Right-Of-Use Asset', year_idx),
            # 经营租赁负债（用于缺失 ROU 时的估算）
            'operating_lease_liabilities_current': self.get_value(bs, 'Current Operating Lease Liabilities', year_idx) or
                                                  self.get_value(bs, 'Operating Lease Liabilities Current', year_idx) or
                                                  self.get_value(bs, 'Current Lease Liabilities', year_idx),
            'operating_lease_liabilities_long_term': self.get_value(bs, 'Long Term Operating Lease Liabilities', year_idx) or
                                                    self.get_value(bs, 'Non Current Operating Lease Liabilities', year_idx) or
                                                    self.get_value(bs, 'Operating Lease Liabilities Non Current', year_idx),
            'operating_lease_liabilities': self.get_value(bs, 'Operating Lease Liabilities', year_idx),
            
            # 负债
            'total_liabilities': self.get_value(bs, 'Total Liabilities', year_idx),
            'current_liabilities': self.get_value(bs, 'Current Liabilities', year_idx),
            # 部分数据源可能以负号表示负债（contra-sign），这里统一取正数幅度，避免 ROIC 分母被错误缩小
            'accounts_payable': abs(self.get_value(bs, 'Accounts Payable', year_idx) or 0),
            'accrued_liabilities': abs(
                self.get_value(bs, 'Accrued Liabilities', year_idx) or
                self.get_value(bs, 'Other Current Liabilities', year_idx) or 0
            ),
            'long_term_debt': self.get_value(bs, 'Long Term Debt', year_idx),
            'short_term_debt': self.get_value(bs, 'Current Debt', year_idx),
            
            # 权益
            'total_equity': self.get_value(bs, 'Total Equity', year_idx) or \
                          self.get_value(bs, 'Stockholders Equity', year_idx),
            'retained_earnings': self.get_value(bs, 'Retained Earnings', year_idx),
        }
    
    def extract_income_statement_items(self, years: int = 7) -> Dict:
        """
        提取利润表关键项目（多年）
        
        Args:
            years: 提取年数
            
        Returns:
            Dict: 利润表关键项目（包含历史数据）
        """
        income = self.income_statement
        
        # 获取可用的年数
        available_years = min(years, income.shape[1] if not income.empty else 0)
        
        result = {
            'years_available': available_years,
            'revenue': [],
            'cogs': [],
            'operating_income': [],
            'ebit': [],
            'net_income': [],
            'depreciation': [],
            'rd_expense': [],
            'sg_and_a': [],
        }
        
        for i in range(available_years):
            result['revenue'].append(self.get_value(income, 'Total Revenue', i))
            result['cogs'].append(self.get_value(income, 'Cost Of Revenue', i))
            result['operating_income'].append(self.get_value(income, 'Operating Income', i))
            result['ebit'].append(self.get_value(income, 'EBIT', i))
            result['net_income'].append(self.get_value(income, 'Net Income', i))
            # 利润表折旧：优先 Reconciled Depreciation，再 Depreciation And/& Amortization，再 Depreciation
            result['depreciation'].append(
                self.get_value(income, 'Reconciled Depreciation', i) or
                self.get_value(income, 'Depreciation', i) or
                self.get_value(income, 'Depreciation And Amortization', i) or
                self.get_value(income, 'Depreciation & Amortization', i)
            )
            result['rd_expense'].append(self.get_value(income, 'Research And Development', i))
            result['sg_and_a'].append(self.get_value(income, 'Selling General And Administration', i))
        
        return result
    
    def extract_cash_flow_items(self, years: int = 5) -> Dict:
        """
        提取现金流量表关键项目
        
        Args:
            years: 提取年数
            
        Returns:
            Dict: 现金流量表关键项目
        """
        cf = self.cash_flow
        
        available_years = min(years, cf.shape[1] if not cf.empty else 0)
        
        result = {
            'years_available': available_years,
            'operating_cash_flow': [],
            'capex': [],
            'free_cash_flow': [],
            'depreciation_cf': [],
            'dividends_paid': [],
            'stock_repurchase': [],
            'common_stock_issuance': [],
        }
        
        for i in range(available_years):
            result['operating_cash_flow'].append(
                self.get_value(cf, 'Operating Cash Flow', i)
            )
            capex = self.get_value(cf, 'Capital Expenditure', i)
            result['capex'].append(abs(capex) if capex else 0)
            result['free_cash_flow'].append(
                self.get_value(cf, 'Free Cash Flow', i)
            )
            # 现金流表折旧：yfinance 可能用 "Depreciation & Amortization" 或 "Depreciation And Amortization"
            result['depreciation_cf'].append(
                self.get_value(cf, 'Depreciation And Amortization', i) or
                self.get_value(cf, 'Depreciation & Amortization', i) or
                self.get_value(cf, 'Depreciation', i)
            )
            result['dividends_paid'].append(
                abs(self.get_value(cf, 'Dividends Paid', i) or
                   self.get_value(cf, 'Cash Dividends Paid', i) or 0)
            )
            result['stock_repurchase'].append(
                abs(self.get_value(cf, 'Common Stock Repurchased', i) or
                   self.get_value(cf, 'Repurchase Of Capital Stock', i) or
                   self.get_value(cf, 'Purchase Of Equity', i) or 0)
            )
            result['common_stock_issuance'].append(abs(self.get_value(cf, 'Common Stock Issuance', i) or
                                                       self.get_value(cf, 'Sale Purchase Of Stock', i) or 0))
        
        return result
    
    def calculate_operating_margins(self, years: int = 7) -> List[float]:
        """
        计算历年营业利润率
        
        Args:
            years: 计算年数
            
        Returns:
            List[float]: 营业利润率列表
        """
        income_items = self.extract_income_statement_items(years)
        
        margins = []
        for i in range(income_items['years_available']):
            revenue = income_items['revenue'][i]
            operating_income = income_items['operating_income'][i]
            
            if revenue and revenue > 0:
                margin = operating_income / revenue
                margins.append(margin)
            else:
                margins.append(0)
        
        return margins
    
    def get_operating_margin_history(self, years: int = 7) -> tuple:
        """
        获取历年营业利润率及年份标签，用于折线图
        
        Returns:
            tuple: (year_labels, margins, smoothed_margin)
        """
        income = self.income_statement
        if income.empty or income.shape[1] == 0:
            return [], [], 0.0
        n = min(years, income.shape[1])
        labels = []
        margins = []
        for i in range(n):
            rev = self.get_value(income, 'Total Revenue', i)
            oi = self.get_value(income, 'Operating Income', i)
            if rev and rev > 0:
                margins.append(oi / rev)
            else:
                margins.append(0.0)
            try:
                col = income.columns[i]
                if hasattr(col, 'year'):
                    labels.append(str(col.year))
                else:
                    labels.append(f"T-{i}")
            except Exception:
                labels.append(f"T-{i}")
        smoothed = float(np.mean(margins)) if margins else 0.0
        return labels, margins, smoothed
    
    def get_smoothed_operating_margin(self, years: int = 7) -> float:
        """
        获取平滑后的营业利润率（多年平均）
        
        Args:
            years: 平滑年数
            
        Returns:
            float: 平滑后的营业利润率
        """
        margins = self.calculate_operating_margins(years)
        
        if not margins:
            return 0
        
        # 计算平均值
        return np.mean(margins)
    
    def calculate_revenue_growth(self, years: int = 5) -> List[float]:
        """
        计算历年营收增长率
        
        Args:
            years: 计算年数
            
        Returns:
            List[float]: 增长率列表
        """
        income_items = self.extract_income_statement_items(years + 1)
        revenues = income_items['revenue']
        
        growth_rates = []
        for i in range(min(years, len(revenues) - 1)):
            if revenues[i] and revenues[i+1] and revenues[i+1] > 0:
                growth = (revenues[i] - revenues[i+1]) / revenues[i+1]
                growth_rates.append(growth)
            else:
                growth_rates.append(0)
        
        return growth_rates
    
    def get_latest_year_data(self, year_idx: int = 0) -> Dict:
        """
        获取指定年度的完整财务数据（用于 AV/EPV 计算）。
        year_idx: 0=最新财年(T), 1=T-1, 2=T-2；确保与侧边栏「AV/EPV 使用报表年份」一致。
        """
        bs_items = self.extract_balance_sheet_items(year_idx)
        income_items = self.extract_income_statement_items(7)
        cf_items = self.extract_cash_flow_items(5)

        def safe_get_value(lst, idx=0, default=0):
            if lst and len(lst) > idx:
                val = lst[idx]
                return float(val) if val and not pd.isna(val) else default
            return default

        def _depreciation_fallback():
            cf_dep = safe_get_value(cf_items.get('depreciation_cf', []), year_idx)
            if cf_dep and cf_dep != 0:
                return cf_dep
            return safe_get_value(income_items.get('depreciation', []), year_idx)

        cash_flow = {
            'capex': safe_get_value(cf_items.get('capex', []), year_idx),
            'operating_cash_flow': safe_get_value(cf_items.get('operating_cash_flow', []), year_idx),
            'depreciation': _depreciation_fallback(),
            'dividends_paid': safe_get_value(cf_items.get('dividends_paid', []), year_idx),
            'stock_repurchase': safe_get_value(cf_items.get('stock_repurchase', []), year_idx),
            'common_stock_issuance': safe_get_value(cf_items.get('common_stock_issuance', []), year_idx),
        }

        return {
            'balance_sheet': bs_items,
            'income_statement': {
                'revenue': safe_get_value(income_items.get('revenue', []), year_idx),
                'operating_income': safe_get_value(income_items.get('operating_income', []), year_idx),
                'net_income': safe_get_value(income_items.get('net_income', []), year_idx),
                'depreciation': safe_get_value(income_items.get('depreciation', []), year_idx),
                'rd_expense': safe_get_value(income_items.get('rd_expense', []), year_idx),
                'sg_and_a': safe_get_value(income_items.get('sg_and_a', []), year_idx),
                'cogs': safe_get_value(income_items.get('cogs', []), year_idx),
            },
            'cash_flow': cash_flow,
            'company_info': self.company_info,
            'market_data': self.market_data,
        }

    @staticmethod
    def check_critical_data_completeness(processed_data: Dict, year_idx: int = 0) -> Dict:
        """
        检查关键字段是否为 0 或 None，用于前端「数据完整性检查与手动修正」。
        返回各字段当前值及是否缺失（缺失则建议用户从年报手动补充）。
        """
        def _is_missing(val) -> bool:
            if val is None:
                return True
            try:
                return float(val) == 0
            except (TypeError, ValueError):
                return True

        def _get_income(key: str):
            inc = processed_data.get('income_statement') or {}
            arr = inc.get(key)
            if isinstance(arr, list) and len(arr) > year_idx:
                return arr[year_idx]
            return inc.get(key) if not isinstance(arr, list) else None

        def _get_cf(key: str):
            cf = processed_data.get('cash_flow') or {}
            arr = cf.get(key)
            if isinstance(arr, list) and len(arr) > year_idx:
                return arr[year_idx]
            return cf.get(key) if not isinstance(arr, list) else None

        bs = processed_data.get('balance_sheet') or {}
        # 折旧：利润表或现金流量表（任一非零即不缺失）
        dep_income = _get_income('depreciation')
        dep_cf = _get_cf('depreciation_cf') or _get_cf('depreciation')
        depreciation = dep_income if (dep_income and float(dep_income) != 0) else dep_cf
        # 资本支出
        capex = _get_cf('capex')
        # 经营租赁使用权资产
        rou = bs.get('right_of_use_assets')
        # 研发费用（0 对非科技公司正常，仍上报供用户确认）
        rd = _get_income('rd_expense')

        return {
            'depreciation': {
                'value': float(depreciation) if depreciation is not None else 0,
                'missing': _is_missing(depreciation),
                'label': 'Depreciation & Amortization',
                'hint': '来自年报 Cash Flow Statement（对 ROIC / Growth 至关重要）',
            },
            'capex': {
                'value': float(capex) if capex is not None else 0,
                'missing': _is_missing(capex),
                'label': 'Capital Expenditure',
                'hint': '来自年报 Cash Flow Statement',
            },
            'right_of_use_assets': {
                'value': float(rou) if rou is not None else 0,
                'missing': _is_missing(rou),
                'label': 'Operating Lease Right-of-Use Assets',
                'hint': '来自年报 Balance Sheet（ASC 842）',
            },
            'rd_expense': {
                'value': float(rd) if rd is not None else 0,
                'missing': _is_missing(rd),
                'label': 'R&D Expenses',
                'hint': '来自年报 Income Statement（科技公司必填）',
            },
        }
