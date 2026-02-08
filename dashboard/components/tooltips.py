"""
工具提示和说明文本模块
"""

# AV调整说明
AV_ADJUSTMENTS_INFO = {
    'ppe_adjustment': {
        'title': 'PPE调整 (固定资产调整)',
        'theory': '''
**理论依据：历史成本 vs 现实成本**

财务报表中的固定资产(PPE)按历史成本记账，随时间推移：
- 土地：市场价值通常上升，账面价值低估
- 建筑物：可能贬值或升值，取决于地段和维护
- 设备：技术进步导致价值变化

**调整方法：**
```
调整后价值 = 各类资产 × 市场价格系数
PPE调整额 = 调整后价值 - 账面净值
```
        ''',
        'formula': '''
```python
# 土地调整
土地调整价值 = 土地面积(平方英尺) × 当地地价($/平方英尺)

# 建筑物调整  
建筑调整价值 = 建筑面积 × 当地房价 × 折旧系数

# 设备调整
设备调整价值 = 账面价值 × 市场价格指数
```
        ''',
        'data_sources': [
            '房地产数据: Zillow, Realtor.com',
            '商业地产: CoStar, LoopNet',
            '设备市场: 二手设备交易平台',
        ]
    },
    
    'goodwill_adjustment': {
        'title': '商誉调整',
        'theory': '''
**理论依据：收购溢价的处理**

商誉 = 收购价格 - 被收购公司可辨认净资产公允价值

**调整原则：**
1. **完全整合的收购**：商誉应剔除，因为已融入公司运营
2. **近期收购**：保留商誉，因为尚未充分整合
3. **减值测试**：关注历年商誉减值情况

**调整方法：**
```
商誉调整 = -(需剔除的商誉)
一般剔除3年以上的收购商誉
```
        ''',
        'formula': '''
```python
# 识别历年收购
for year, acquisition in acquisitions:
    if year < current_year - 3:  # 3年前的收购
        remove_goodwill += acquisition_goodwill
    
# 最终调整
goodwill_adjustment = -remove_goodwill
```
        '''
    },
    
    'brand_value': {
        'title': '品牌价值估算',
        'theory': '''
**理论依据：品牌作为无形资产**

品牌为公司带来定价权和客户忠诚度，但不在资产负债表中体现。

**方法1: 特许权费法 (Royalty Relief)**
```
品牌价值 = 特许费率 × 营业收入 × 永续价值因子
永续价值因子 = 1 / (折现率 - 增长率)
```

特许费率参考：
- 强品牌(可口可乐): 5-8%
- 中等品牌(沃尔玛): 3-5%  
- 弱品牌: 1-3%

**方法2: 营销公司法 (EVA × 品牌作用比)**
```
EVA = (ROIC - WACC) × 投资资本
品牌价值 = EVA × 品牌作用比 × 永续价值因子
```

品牌作用比参考：
- 消费品牌: 20-30%
- 零售品牌: 10-20%
- 工业品牌: 5-15%
        ''',
        'formula': '''
```python
# 特许权费法
brand_value = royalty_rate × revenue × (1 / (r - g))

# 营销公司法  
eva = (roic - wacc) × invested_capital
brand_value = eva × brand_role × (1 / (r - g))
```
        '''
    },
    
    'workforce_value': {
        'title': '员工队伍价值',
        'theory': '''
**理论依据：人力资本投资**

招聘和培训员工需要成本，这些投入创造了有价值的人力资本。

**估值方法：**
```
员工价值 = 总薪酬 × 培训成本比例
```

**培训成本比例参考：**
- 蓝领工人: 10-15%
- 白领员工: 15-25%  
- 技术/专业人员: 20-30%
- 管理层: 30-50%
        ''',
        'formula': '''
```python
# 分类计算
普通员工价值 = 普通员工数 × 平均薪酬 × 10%
管理层价值 = 管理层数 × 平均薪酬 × 30%

# 或简化计算
员工价值 = 总薪酬支出 × 15%
```
        '''
    },
    
    'product_portfolio': {
        'title': '产品组合价值',
        'theory': '''
**理论依据：R&D资本化**

R&D支出创造产品组合，但在损益表中被费用化。
应将其视为资产，按产品周期折旧。

**估值方法：**
```
产品组合价值 = Σ(过去n年R&D × 折旧率^年数)
```

**产品周期参考：**
- 软件/互联网: 2-3年
- 消费电子: 3-5年
- 制药: 8-12年
- 汽车: 5-8年
        ''',
        'formula': '''
```python
portfolio_value = 0
for i, rd_expense in enumerate(past_rd_expenses):
    depreciation_factor = (1 - depreciation_rate) ** i
    portfolio_value += rd_expense × depreciation_factor

# 例如: 20%折旧率
# 今年: RD × 1.0
# 去年: RD × 0.8
# 2年前: RD × 0.64
```
        '''
    }
}

# EPV调整说明
EPV_ADJUSTMENTS_INFO = {
    'smoothing': {
        'title': '利润平滑',
        'description': '''
使用7年移动平均平滑营业利润率，消除周期性波动，
获得可持续的盈利能力。
        '''
    },
    
    'depreciation': {
        'title': '折旧调整',
        'description': '''
**过度折旧识别：**

维护性资本支出 vs 折旧费用
如果折旧 > 维护性支出，说明过度折旧，应加回。

```
维护性Capex = 总Capex - 增长性Capex
增长性Capex = PPE × 营收增长率
过度折旧 = 折旧 - 维护性Capex
```
        '''
    },
    
    'growth_expense': {
        'title': '增长性支出调整',
        'description': '''
**营销增长支出：**
当期营销费用 - 品牌摊销 = 增长性支出

**R&D增长支出：**  
当期R&D - 维持性R&D = 增长性支出

这些支出应加回营业利润，因为它们创造未来价值。
        '''
    }
}

# Beta计算说明
BETA_INFO = {
    'definition': '''
**Beta定义：**
衡量股票系统性风险，即相对于市场组合的敏感度

```
Beta = Cov(Ri, Rm) / Var(Rm)
```

**Beta解读：**
- **Beta = 1.0**: 与市场同步波动（市场风险）
- **Beta > 1.0**: 比市场波动大（进攻型/高风险）
  - 例如：科技股 β ≈ 1.3-1.8
- **Beta < 1.0**: 比市场波动小（防御型/低风险）
  - 例如：公用事业 β ≈ 0.3-0.7
- **Beta ≈ 0**: 与市场无关（极罕见）
- **Beta < 0**: 与市场反向（对冲资产，如黄金）

**⚠️ Beta合理范围：**
- 绝大多数股票: 0.5-1.5
- 超过2.0或低于0：需要仔细检查数据
    ''',
    
    'models': {
        'capm': '''
**CAPM (资本资产定价模型)**

这是业界最常用的方法：

```
E[Ri] = rf + βi × (E[Rm] - rf)

其中:
- rf = 无风险利率（10年期国债）
- βi = 股票i的Beta
- E[Rm] - rf = 市场风险溢价（历史平均6-7%）
```

**计算步骤：**
1. 获取股票和市场指数的历史收益率（通常5年月度数据）
2. 计算协方差和方差
3. Beta = Cov(Ri, Rm) / Var(Rm)

**优点**: 简单直观，数据易得
**缺点**: 只考虑市场单一因子
        ''',
        
        'ff3': '''
**Fama-French 三因子模型**

考虑三个风险因子：

```
Ri - rf = α + β_MKT×(Rm-rf) + β_SMB×SMB + β_HML×HML + εi

因子说明:
- MKT (Market): 市场风险溢价
- SMB (Small Minus Big): 小盘股溢价
- HML (High Minus Low): 价值股溢价
```

**何时使用：**
- 小盘股：β_SMB显著
- 价值股：β_HML显著
- 学术研究和专业分析

**优点**: 解释力更强（R²更高）
**缺点**: 因子数据获取较复杂
        ''',
        
        'ff5': '''
**Fama-French 五因子模型**

在三因子基础上增加两个因子：

```
Ri - rf = α + β_MKT×MKT + β_SMB×SMB + β_HML×HML 
           + β_RMW×RMW + β_CMA×CMA + εi

新增因子:
- RMW (Robust Minus Weak): 盈利能力
- CMA (Conservative Minus Aggressive): 投资模式
```

**何时使用：**
- 最新的学术模型
- 对某些行业（如科技）解释力更好

**数据来源**: Kenneth French Data Library
        ''',
        
        'blume': '''
**Blume调整Beta**

实证研究发现Beta有向1.0回归的趋势：

```
β_adjusted = 0.67 × β_historical + 0.33 × 1.0
```

**理论依据：**
- 极端Beta值不稳定，会向市场平均回归
- Bloomberg终端默认使用此调整

**何时使用：**
- 预测未来Beta时
- Beta值波动较大时
        ''',
        
        'fundamental': '''
**基本面Beta（Bottom-Up）**

基于财务杠杆计算：

```
1. 获取无杠杆Beta (行业平均或可比公司)
   β_unlevered = β_levered / [1 + (1-T) × (D/E)]

2. 根据公司杠杆调整
   β_levered = β_unlevered × [1 + (1-T) × (D/E)]
```

**何时使用：**
- 历史数据不足（如新上市）
- 公司资本结构变化大
- 收购/重组后

**优点**: 反映当前资本结构
**缺点**: 需要行业参考Beta
        '''
    },
    
    'industry_practice': '''
**业界实践：**

1. **投资银行**: 主要用CAPM，辅以Blume调整
   - Goldman Sachs, Morgan Stanley
   - 5年月度数据 + Blume调整

2. **对冲基金**: FF3或FF5因子模型
   - 更精确的风险调整收益
   - AQR, Two Sigma等

3. **评级机构**: CAPM为主
   - Moody's, S&P
   - 标准化易比较

4. **学术界**: Fama-French模型
   - 发表研究必备
   - 因子数据公开可得

**推荐使用：**
- 快速分析：CAPM
- 深入研究：FF3
- 新公司/重组：Fundamental Beta
    '''
}

# WACC说明
WACC_INFO = '''
**加权平均资本成本 (WACC)**

```
WACC = (E/(E+D)) × re + (D/(E+D)) × rd × (1-税率)

其中:
re = 无风险利率 + Beta × 市场风险溢价
rd = 债务成本
```

**组成部分：**
1. **权益成本 (re)**: 通过CAPM模型计算
   - 无风险利率: 10年期国债收益率
   - Beta: 股票相对市场的波动性
   - 市场风险溢价: 6% (历史平均)

2. **债务成本 (rd)**: 公司借款的实际利率
   - 税盾效应: 利息可抵税

3. **权重**: 基于市值和债务的市场价值
'''
