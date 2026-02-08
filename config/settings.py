"""
配置文件 - 全局参数设置
"""

# 默认估值参数
DEFAULT_PARAMS = {
    # 品牌估值参数
    'brand_royalty_rate': 0.05,        # 品牌特许费率 (5%)
    'brand_role': 0.15,                # 品牌作用比 (15%)
    'discount_rate': 0.07,             # 折现率 (7%)
    'growth_rate': 0.02,               # 永续增长率 (2%)
    
    # 无形资产参数
    'workforce_cost_ratio': 0.10,      # 员工培训成本比例 (10%)
    'brand_amortization_years': 15,    # 品牌摊销年限
    'product_cycle_years': 5,          # 产品周期年数
    'rd_depreciation_rate': 0.20,      # R&D折旧率 (20%)
    
    # WACC参数
    'market_risk_premium': 0.06,       # 市场风险溢价 (6%)
    'tax_rate_us': 0.21,               # 美国企业税率 (21%)
    'tax_rate_china': 0.25,            # 中国企业税率 (25%)
    'tax_rate_hk': 0.165,              # 香港企业税率 (16.5%)
    
    # EPV计算参数
    'smoothing_years': 3,              # 利润平滑年数（默认3年，与课件推荐一致）
    'min_years_data': 3,               # 最少需要的历史数据年数
}

# PPE调整默认参数（Lecture 2 口径：调整后净值 - 报表净值 = 调整额；WMT 约 +46b）
# 分项系数应用于 Gross 各组成部分，再得调整后净值
PPE_ADJUSTMENT_PARAMS = {
    'us': {
        'land_factor': 0.50,           # Land
        'building_factor': 0.864,      # Buildings & Improv (101888/117973)
        'fixture_factor': 0.50,       # Fixtures
        'equipment_factor': 0.50,     # Transportation & Equip
        'cip_factor': 1.0,            # Construction in progress 不变
    },
    'china': {
        'land_factor': 0.60,
        'building_factor': 0.80,
        'fixture_factor': 0.45,
        'equipment_factor': 0.45,
        'cip_factor': 1.0,
    }
}
# PPE Gross 组成比例（无分项数据时用，与 WMT 2025 接近）
PPE_GROSS_RATIOS = {
    'land': 0.084,      # 19342/231617
    'building': 0.509,   # 117973/231617
    'fixtures': 0.329,  # 76226/231617
    'equipment': 0.012, # 2673/231617
    'cip': 0.066,       # 15403/231617
}

# API配置
API_CONFIG = {
    'yfinance': {
        'enabled': True,
        'timeout': 30,
    },
    'cache_enabled': True,
    'cache_expiry_days': 1,            # 缓存过期天数
}

# 市场配置
MARKETS = {
    'US': {
        'name': '美股',
        'suffix': '',                   # 股票代码后缀
        'currency': 'USD',
        'tax_rate': 0.21,
        'index': '^GSPC',              # 市场指数 (S&P 500)
    },
    'HK': {
        'name': '港股',
        'suffix': '.HK',
        'currency': 'HKD',
        'tax_rate': 0.165,
        'index': '^HSI',               # 恒生指数
    },
    'CN': {
        'name': 'A股',
        'suffix': '',                   # 自动判断 .SS 或 .SZ
        'currency': 'CNY',
        'tax_rate': 0.25,
        'index': '000001.SS',          # 上证指数
    }
}

# Beta计算方法 - 基于不同资产定价模型
BETA_METHODS = {
    'capm': {
        'name': 'CAPM Beta',
        'description': '''标准资本资产定价模型
Beta = Cov(Ri, Rm) / Var(Rm)
业界最常用方法，使用5年月度数据计算''',
        'formula': 're = rf + β × (E[Rm] - rf)',
        'usage': '最常用，适合大多数情况'
    },
    'ff3': {
        'name': 'Fama-French 3因子Beta',
        'description': '''Fama-French三因子模型
Ri - rf = α + β_MKT(Rm-rf) + β_SMB×SMB + β_HML×HML + ε
考虑市场、规模、价值三个风险因子''',
        'formula': 're = rf + β_MKT×MRP + β_SMB×SMB + β_HML×HML',
        'usage': '学术界广泛使用，更精确'
    },
    'ff5': {
        'name': 'Fama-French 5因子Beta',
        'description': '''Fama-French五因子模型
在三因子基础上增加盈利能力和投资模式因子
更全面的风险调整''',
        'formula': 're = rf + β_MKT×MRP + β_SMB×SMB + β_HML×HML + β_RMW×RMW + β_CMA×CMA',
        'usage': '最新模型，对某些股票更准确'
    },
    'adjusted_blume': {
        'name': 'Blume调整Beta',
        'description': '''向1.0回归调整
实证发现Beta会向市场均值回归
调整Beta = 0.67 × 历史Beta + 0.33 × 1.0''',
        'formula': 'β_adjusted = 0.67×β_historical + 0.33',
        'usage': 'Bloomberg等终端常用'
    },
    'fundamental': {
        'name': '基本面Beta',
        'description': '''基于财务杠杆和业务风险估算
β_levered = β_unlevered × [1 + (1-税率) × (D/E)]
适用于历史数据不足或公司结构变化大的情况''',
        'formula': 'β_L = β_U × [1 + (1-T) × (D/E)]',
        'usage': '新上市公司或重组后'
    }
}

# Beta合理范围
BETA_RANGES = {
    'typical': (0.5, 1.5),      # 大多数股票
    'defensive': (0.0, 0.7),    # 公用事业、消费必需品
    'cyclical': (0.8, 1.5),     # 周期性行业
    'aggressive': (1.5, 2.5),   # 科技、生物科技
    'warning_low': 0.0,         # 低于此值需警告
    'warning_high': 3.0,        # 高于此值需警告
}

# 界面配置
UI_CONFIG = {
    'page_title': '价值投资分析工具',
    'page_icon': '📊',
    'layout': 'wide',
    'sidebar_state': 'expanded',
}

# 导出配置
EXPORT_CONFIG = {
    'excel_filename_template': '{ticker}_valuation_{date}.xlsx',
    'pdf_filename_template': '{ticker}_report_{date}.pdf',
}
