"""
Beta计算模块 - 实现多种资产定价模型
"""
import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class BetaCalculator:
    """Beta计算类 - 支持多种模型"""
    
    def __init__(self, ticker: str, market: str = 'US'):
        """
        初始化Beta计算器
        
        Args:
            ticker: 股票代码
            market: 市场（用于选择市场指数）
        """
        self.ticker = ticker
        self.market = market
        self.market_index = self._get_market_index()
        
    def _get_market_index(self) -> str:
        """根据市场选择指数"""
        indices = {
            'US': '^GSPC',      # S&P 500
            'HK': '^HSI',       # 恒生指数
            'CN': '000001.SS',  # 上证指数
        }
        return indices.get(self.market, '^GSPC')
    
    def calculate_capm_beta(self, period: str = '5y') -> Dict:
        """
        计算CAPM Beta（业界最常用）
        
        Args:
            period: 数据周期（默认5年）
            
        Returns:
            Dict: Beta和相关统计数据
        """
        try:
            # 获取股票和市场数据
            stock = yf.Ticker(self.ticker)
            market = yf.Ticker(self.market_index)
            
            # 获取历史价格（月度数据）
            stock_hist = stock.history(period=period, interval='1mo')
            market_hist = market.history(period=period, interval='1mo')
            
            if stock_hist.empty or market_hist.empty:
                return self._default_beta_result("数据不足")
            
            # 计算收益率
            stock_returns = stock_hist['Close'].pct_change().dropna()
            market_returns = market_hist['Close'].pct_change().dropna()
            
            # 对齐数据
            combined = pd.DataFrame({
                'stock': stock_returns,
                'market': market_returns
            }).dropna()
            
            if len(combined) < 24:  # 至少需要24个月数据
                return self._default_beta_result("数据点不足")
            
            # 计算Beta
            covariance = combined['stock'].cov(combined['market'])
            variance = combined['market'].var()
            
            beta = covariance / variance if variance != 0 else 1.0
            
            # 计算R²（解释力）
            correlation = combined['stock'].corr(combined['market'])
            r_squared = correlation ** 2
            
            # 计算标准误差
            residuals = combined['stock'] - (beta * combined['market'])
            std_error = residuals.std() / np.sqrt(len(combined))
            
            # Beta合理性检查
            warning = self._check_beta_validity(beta)
            
            return {
                'beta': beta,
                'r_squared': r_squared,
                'std_error': std_error,
                'observations': len(combined),
                'period': period,
                'method': 'CAPM',
                'warning': warning,
                'formula': f'β = Cov(R_stock, R_market) / Var(R_market) = {beta:.3f}'
            }
            
        except Exception as e:
            return self._default_beta_result(f"计算失败: {str(e)}")
    
    def calculate_blume_adjusted_beta(self, historical_beta: float = None) -> Dict:
        """
        Blume调整Beta（Bloomberg方法）
        
        Args:
            historical_beta: 历史Beta（如不提供则先计算CAPM）
            
        Returns:
            Dict: 调整后的Beta
        """
        if historical_beta is None:
            capm_result = self.calculate_capm_beta()
            historical_beta = capm_result.get('beta', 1.0)
        
        # Blume调整公式
        adjusted_beta = 0.67 * historical_beta + 0.33 * 1.0
        
        warning = self._check_beta_validity(adjusted_beta)
        
        return {
            'beta': adjusted_beta,
            'historical_beta': historical_beta,
            'method': 'Blume调整',
            'formula': f'β_adj = 0.67 × {historical_beta:.3f} + 0.33 = {adjusted_beta:.3f}',
            'warning': warning,
            'explanation': 'Bloomberg等金融终端常用方法，Beta向1.0回归'
        }
    
    def calculate_fundamental_beta(self, debt_to_equity: float, 
                                   tax_rate: float = 0.21,
                                   unlevered_beta: float = None) -> Dict:
        """
        基本面Beta（基于财务杠杆）
        
        Args:
            debt_to_equity: 负债权益比 (D/E)
            tax_rate: 企业税率
            unlevered_beta: 无杠杆Beta（如不提供，使用行业平均1.0）
            
        Returns:
            Dict: 基本面Beta
        """
        if unlevered_beta is None:
            unlevered_beta = 1.0  # 默认行业Beta
        
        # Hamada公式：考虑财务杠杆
        levered_beta = unlevered_beta * (1 + (1 - tax_rate) * debt_to_equity)
        
        warning = self._check_beta_validity(levered_beta)
        
        return {
            'beta': levered_beta,
            'unlevered_beta': unlevered_beta,
            'debt_to_equity': debt_to_equity,
            'tax_rate': tax_rate,
            'method': '基本面Beta',
            'formula': f'β_L = {unlevered_beta:.2f} × [1 + (1-{tax_rate:.0%}) × {debt_to_equity:.2f}] = {levered_beta:.3f}',
            'warning': warning,
            'explanation': '基于Hamada公式，通过财务杠杆调整行业Beta'
        }
    
    def estimate_ff3_beta(self) -> Dict:
        """
        估算Fama-French三因子Beta（简化版）
        
        注：完整实现需要FF因子数据，这里提供估算
        
        Returns:
            Dict: FF3 Beta估算结果
        """
        # 先计算CAPM Beta
        capm_result = self.calculate_capm_beta()
        market_beta = capm_result['beta']
        
        # 获取公司信息估算SMB和HML
        try:
            stock = yf.Ticker(self.ticker)
            info = stock.info
            
            market_cap = info.get('marketCap', 0)
            pb_ratio = info.get('priceToBook', 1.0)
            
            # 估算SMB Beta（基于市值）
            # 小盘股 SMB > 0，大盘股 SMB < 0
            if market_cap > 200e9:  # 大于2000亿
                smb_beta = -0.3
            elif market_cap > 10e9:  # 100-2000亿
                smb_beta = 0.0
            else:  # 小于100亿
                smb_beta = 0.5
            
            # 估算HML Beta（基于P/B）
            # 价值股 HML > 0，成长股 HML < 0
            if pb_ratio > 3.0:
                hml_beta = -0.3  # 成长股
            elif pb_ratio > 1.5:
                hml_beta = 0.0
            else:
                hml_beta = 0.4  # 价值股
            
            warning = '⚠️ 这是基于市值和估值的简化估算，完整计算需要FF因子数据'
            
            return {
                'beta_market': market_beta,
                'beta_smb': smb_beta,
                'beta_hml': hml_beta,
                'market_cap': market_cap,
                'pb_ratio': pb_ratio,
                'method': 'FF3估算',
                'warning': warning,
                'explanation': '需要完整FF因子数据才能精确计算',
                'data_source': 'Kenneth French Data Library: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html'
            }
            
        except Exception as e:
            return self._default_beta_result(f"FF3估算失败: {str(e)}")
    
    def _check_beta_validity(self, beta: float) -> str:
        """
        检查Beta合理性
        
        Args:
            beta: Beta值
            
        Returns:
            str: 警告信息（如果有）
        """
        if beta < 0:
            return '⚠️ Beta为负值！这极为罕见，通常只出现在对冲资产（如黄金）。请检查数据是否正确。'
        elif beta < 0.1:
            return '⚠️ Beta极低（<0.1），该股票几乎不受市场影响，请检查数据。'
        elif beta > 3.0:
            return '⚠️ Beta极高（>3.0），该股票波动性极大，风险很高。'
        elif beta > 2.0:
            return 'ℹ️ Beta较高（>2.0），该股票为高风险/高波动性股票。'
        elif beta < 0.3:
            return 'ℹ️ Beta很低（<0.3），该股票为防御性股票。'
        else:
            return ''
    
    def _default_beta_result(self, error_msg: str) -> Dict:
        """返回默认Beta结果"""
        return {
            'beta': 1.0,
            'method': '默认',
            'warning': f'⚠️ {error_msg}，使用默认Beta=1.0',
            'error': error_msg
        }
    
    def get_beta_comparison(self) -> pd.DataFrame:
        """
        获取多种方法的Beta对比
        
        Returns:
            DataFrame: Beta对比表
        """
        results = []
        
        # 1. CAPM Beta
        capm = self.calculate_capm_beta()
        results.append({
            '方法': 'CAPM',
            'Beta': f"{capm.get('beta', 1.0):.3f}",
            'R²': f"{capm.get('r_squared', 0):.3f}",
            '说明': '业界标准方法',
            '适用': '通用'
        })
        
        # 2. Blume调整
        blume = self.calculate_blume_adjusted_beta(capm.get('beta', 1.0))
        results.append({
            '方法': 'Blume调整',
            'Beta': f"{blume.get('beta', 1.0):.3f}",
            'R²': '-',
            '说明': 'Bloomberg方法',
            '适用': '预测未来'
        })
        
        # 3. 基本面Beta（需要杠杆数据）
        results.append({
            '方法': '基本面Beta',
            'Beta': '需要D/E数据',
            'R²': '-',
            '说明': '基于财务杠杆',
            '适用': '新公司/重组'
        })
        
        # 4. FF3（简化估算）
        results.append({
            '方法': 'FF3估算',
            'Beta': '需要因子数据',
            'R²': '-',
            '说明': '三因子模型',
            '适用': '学术/专业'
        })
        
        return pd.DataFrame(results)
    
    def get_industry_beta_reference(self) -> Dict:
        """
        获取行业Beta参考值（用于基本面Beta）
        
        Returns:
            Dict: 行业Beta参考
        """
        # 主要行业的典型Beta范围
        industry_betas = {
            'Technology': {'beta': 1.3, 'range': (1.1, 1.6)},
            'Financial Services': {'beta': 1.2, 'range': (1.0, 1.4)},
            'Healthcare': {'beta': 0.9, 'range': (0.7, 1.1)},
            'Consumer Cyclical': {'beta': 1.1, 'range': (0.9, 1.3)},
            'Consumer Defensive': {'beta': 0.6, 'range': (0.4, 0.8)},
            'Energy': {'beta': 1.2, 'range': (1.0, 1.5)},
            'Utilities': {'beta': 0.5, 'range': (0.3, 0.7)},
            'Industrials': {'beta': 1.0, 'range': (0.8, 1.2)},
            'Real Estate': {'beta': 0.8, 'range': (0.6, 1.0)},
            'Communication': {'beta': 1.0, 'range': (0.8, 1.3)},
            'Basic Materials': {'beta': 1.1, 'range': (0.9, 1.3)},
        }
        
        return industry_betas


class FFFactorCalculator:
    """Fama-French因子计算器（简化版）"""
    
    @staticmethod
    def get_ff_factors_from_web() -> pd.DataFrame:
        """
        从Kenneth French网站获取因子数据
        
        注：这需要网络访问和数据解析
        实际使用时应该从本地缓存或API获取
        
        Returns:
            DataFrame: FF因子数据
        """
        # 实际URL: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
        # 这里返回空DataFrame，实际使用时需要实现完整下载逻辑
        
        return pd.DataFrame()
    
    @staticmethod
    def calculate_ff3_regression(stock_returns: pd.Series,
                                 market_returns: pd.Series,
                                 smb_returns: pd.Series,
                                 hml_returns: pd.Series) -> Dict:
        """
        FF3因子回归
        
        Args:
            stock_returns: 股票超额收益
            market_returns: 市场超额收益
            smb_returns: SMB因子收益
            hml_returns: HML因子收益
            
        Returns:
            Dict: 回归结果
        """
        # 需要使用statsmodels或sklearn进行多元回归
        # 这里提供框架，实际需要实现
        
        from scipy import stats
        
        # 简化：只计算市场Beta（完整版需要多元回归）
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            market_returns, stock_returns
        )
        
        return {
            'beta_mkt': slope,
            'beta_smb': 0.0,  # 需要多元回归
            'beta_hml': 0.0,  # 需要多元回归
            'alpha': intercept,
            'r_squared': r_value ** 2,
            'p_value': p_value
        }


def get_recommended_beta_method(company_info: Dict) -> str:
    """
    根据公司特征推荐Beta计算方法
    
    Args:
        company_info: 公司信息
        
    Returns:
        str: 推荐的方法（必须匹配BETA_METHODS字典的键）
    """
    market_cap = company_info.get('market_cap', 0)
    sector = company_info.get('sector', '')
    
    # 新上市或小市值公司
    if market_cap < 1e9:
        return 'fundamental'
    
    # 金融、科技等复杂行业
    if sector in ['Technology', 'Financial Services']:
        return 'ff3'
    
    # 大多数情况使用CAPM + Blume调整
    return 'adjusted_blume'


# 业界实践参考
INDUSTRY_PRACTICE = '''
## 业界Beta使用实践

### 1. 投资银行（Investment Banks）
**方法**: CAPM + Blume调整
**数据**: 5年月度收益率
**来源**: Bloomberg, FactSet
**代表**: Goldman Sachs, Morgan Stanley, JP Morgan

**使用场景**: DCF估值、并购定价
**典型设置**:
- 历史周期: 60个月
- 回归频率: 月度
- 调整方法: Blume (0.67×历史+0.33×1.0)

### 2. 资产管理公司
**方法**: CAPM为主，FF3验证
**数据**: 彭博/路透终端
**代表**: BlackRock, Vanguard

**使用场景**: 组合风险管理
**典型设置**:
- 定期更新（季度/年度）
- 多周期验证（2年/5年对比）

### 3. 对冲基金
**方法**: Fama-French多因子
**数据**: Kenneth French Data Library
**代表**: AQR, Two Sigma

**使用场景**: 因子投资、风险归因
**典型设置**:
- FF3或FF5因子
- 高频数据（日度/周度）
- 滚动估计

### 4. 学术研究
**方法**: Fama-French系列
**数据**: CRSP + Compustat
**标准**: JFE, JF等顶级期刊

**要求**: 必须使用多因子模型
**数据频率**: 通常月度

### 5. 评级机构
**方法**: CAPM
**代表**: Moody's, S&P, Fitch

**使用场景**: 信用评级、违约概率
**优点**: 标准化，可比性强

---

## 推荐使用方案

### 快速分析
✅ **CAPM Beta** - 简单快速，足够大多数情况

### 专业分析  
✅ **CAPM + Blume调整** - 业界标准

### 学术研究
✅ **Fama-French 3因子** - 更高解释力

### 特殊情况
- 新上市公司 → **基本面Beta**
- 重组后 → **基本面Beta**  
- 小盘股 → **FF3（考虑SMB）**
- 价值股 → **FF3（考虑HML）**

---

## Beta数据来源

### 商业终端（付费）
- **Bloomberg**: 最全面，自动Blume调整
- **FactSet**: 专业投资数据
- **Capital IQ**: S&P旗下

### 免费来源
- **Yahoo Finance**: 基础Beta（已调整）
- **Kenneth French数据库**: FF因子（学术）
- **FRED**: 宏观和市场数据

### 学术数据库
- **CRSP**: 股票价格和收益
- **Compustat**: 财务数据
'''
