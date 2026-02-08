# 价值投资分析工具

基于 Graham & Dodd / Columbia 价值投资方法论的自动化分析工具，计算 Asset Value (AV)、Earning Power Value (EPV) 与 Franchise Value (FV)。

## 快速开始

```bash
# 安装依赖（首次）
pip install -r requirements.txt

# 启动（推荐）
./run.sh

# 或直接
python3 -m streamlit run dashboard/app_enhanced.py
```

浏览器打开 http://localhost:8501，输入股票代码（如 WMT、AAPL）或公司名（如 starbuck），选择市场后点击「开始分析」。

## 功能概览

- **数据**：自动获取财报（yfinance），支持美股/港股/A股；可输入公司名自动解析为代码
- **AV**：PPE 分项调整、商誉（当前−未消化）、品牌三种方法（营销费用折现/特许权/营销公司法）、员工与产品组合
- **EPV**：营业利润平滑（默认 3 年）、折旧/增长支出/非经常项调整、WACC、EPV/EPVc、与课件一致的完整表格
- **ROIC**：课件口径（Op+D&A+Lease/Interest，IC=TA+AccDep−AP−Accr），可选填写 Lease/Interest 以复现 WMT 12.5%
- **FV**：ROIC vs WACC、增长率 g=k×ROIC+有机增长、Franchise Value、预期收益率与安全边际
- **Beta**：CAPM / Blume / FF3·FF5 / 基本面，60 日滚动图与全样本对比说明
- **其他**：P/E、P/B、EV/EBIT、EPV/市值、AV/市值对比；导出报告

## 项目结构

```
├── config/           # 配置（参数、PPE 系数、Beta 方法等）
├── data/             # 数据获取与处理（api_fetcher, data_processor）
├── valuation/        # 估值引擎（asset_value, earning_power, franchise_value, beta_calculator, adjustments）
├── dashboard/        # 界面（app_enhanced.py + components）
├── docs/             # 说明（见本 README）
├── run.sh            # 启动脚本
├── requirements.txt
└── README.md
```

## 方法论

基于 Columbia Business School 估值课程（Heilbrunn Center for Graham & Dodd Investment）：AV 调整后资产价值，EPV 可持续盈利能力价值，EPVc 考虑终止风险，FV 增长价值（ROIC > WACC 时）。

仅供学习与研究使用。
