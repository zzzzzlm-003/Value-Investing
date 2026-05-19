# Adobe Homework Q5-Q8 — 过程记录

记录做作业过程中的问题与解答。

---

## 1. Permanent Inventory Method 是什么？假设？数据在哪？

**我的问题：**  
Permanent inventory method 是啥，用了什么假设，product 的数据在哪里？

**解答：**

- **是什么：** 用历史 R&D 的加权和来估计当前「产品组合」存量的方法。把 R&D 当作对产品/技术存量的投资，按时间衰减（折旧）得到当前存量。
- **假设：** R&D 创造无形资产；每年按固定比例 d=20% 衰减；只考虑近 5 年。
- **数据在哪：** 在 Excel 的 **R&D** sheet，列 2 是年份，列 3 是 R&D 费用。需要 2021–2025 五年。

---

## 2. 客户组合部分：是不是只要解出 β 就行了？

**我的问题：**  
其实只要求解贝塔就对了是吧？

**解答：**  
**对，核心就是把 β(t) 解出来，后面都只是代入。**

模型是：
```
C(t) = (1−a)×C(t−1) + β(t)×i_marketing(t)
```
已知：C(t)、C(t−1)、i_marketing(t)、a=0.1。  
未知：β(t)。

移项得：
```
β(t) = [C(t) − 0.9×C(t−1)] ÷ i_marketing(t)
```

解出 β 之后：

| 所求 | 公式 |
|------|------|
| 单客户获取成本 | 1/β(t) |
| 客户组合价值 (Q5) | (1/β_2025) × C_2025 |
| EPV 中的 maintenance marketing (Q6) | a×C(t) / β(t) |

数据都在 **CC Accounts & Sales** sheet：C(t) = CC Subscriptions（百万账户），i_marketing(t) = Sales and marketing（百万美元）。

---

*（后续有问题可继续补充）*
