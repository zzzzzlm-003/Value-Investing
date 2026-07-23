# 课件公式与实现对照（WMT 样例）

## AV（Asset Value）
- 课件思路：
  - AV = Book Equity + 各项调整（PPE、商誉、流动资产、品牌、员工等）
- 代码入口：
  - `valuation/asset_value.py` → `AssetValueCalculator.calculate()`

## EPV（Earning Power Value）
- 课件公式：
  - $EPV = \dfrac{Adjusted\ NOPAT}{WACC}$
  - $Adjusted\ NOPAT=(1-T)\times(\text{Smoothed OI}+\Delta_{extra}+\Delta_{dep}+\Delta_{growth})$
- 代码入口：
  - `valuation/earning_power.py` → `EarningPowerCalculator.calculate()`

## WACC（Lecture 3 p13 口径）
- 课件公式：
  - $WACC=w_e\cdot r_e+w_d\cdot r_d\cdot(1-T)$
  - $r_e=r_f+\beta\cdot MRP$
- 代码入口：
  - `valuation/earning_power.py` → `get_wacc_breakdown()` / `_calculate_wacc()`

## ROIC（lecture 口径）
- 课件口径：
  - $ROIC_{lecture}=\dfrac{(1-T)\cdot(OI + D\&A + Lease/Interest)}{TA + AccDep - AP - Accrued}$
- 代码入口：
  - `valuation/franchise_value.py` → `calculate_roic(method='lecture')`

## FV（Franchise Value）
- 课件主式：
  - $FV = GrowthInvestment\times\dfrac{ROIC-WACC}{WACC}\times\dfrac{1}{WACC-g}$
  - $V = EPV + FV$
- 代码入口：
  - `valuation/franchise_value.py` → `calculate_franchise_value()`
- 本站样例：开启 strict course mode（允许 `ROIC < WACC` 时 `FV < 0`）

## 备注
- 网站样例数据来自本地真实运行（`WMT`），并附假设与一致性检查。
- 仅用于学习研究与方法展示，不构成投资建议。
