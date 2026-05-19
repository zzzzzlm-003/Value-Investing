# Session 06 Note

日期：2026年2月22日

目标：
- 记录 Session 06 的学习要点与问答

---

## 大纲
- 主题 1
- 主题 2
- 主题 3

## 问题与回答
1. 问题 1：
   - 回答：

2. 问题 2：
   - 回答：

---

（在此处我会把你的提问和我们的讨论逐条记录）

### Q1: 老师在提到这段是想说什么？
- 问：怎么会在估值最低的时候，expected return 也是最低？不应该那时候最便宜，之后股价扩张带来的回报最高吗？
- 答：要记住期望回报被分解为三部分：股息/收益率 (D/V) + 基本面增长 g + 估值倍数变动的影响 (1+g) * h，其中 h 是“倍数的预期变化率”。

   1. 低估值并不保证未来会有倍数扩张——倍数低可能反映市场对未来增长或风险的长期担忧（比如盈利能力下降、资本回报变差、可持续性问题或更高的风险溢价），因此历史上从“当前处于最低倍数”出发，后续平均的 h 可能仍为负或接近零。

   2. 即使倍数有回升，回报的另一部分还来自 g（营收/盈利增速）与当前收益率 D/V。如果在低倍数时 g 很低、股息也低，那么总回报仍可能不高。

   3. 表格里给出的 h 是“在不同起点倍数条件下，历史上观测到的平均倍数变化率”。所以当表中把“起点是历史最低倍数”时，对应的历史 h 可能是负的（表中就是这样），导致 R 也最低——说明那些时候伴随的是基本面恶化或更大的风险，而不是安全的低估值等待回升。

   4. 结论：低倍数是一个必要但不足够的“便宜”信号。要判断是否真的有高期望回报，需要判断（或估计）未来的 g、当前收益率 D/V，以及倍数是否有合理的回升理由（例如周期性回归 vs. 结构性衰退）。


   ---

   ## Plowback ratio / ΔIC over Adjusted NOPAT（解释）

   这页幻灯片右侧的柱状图展示的是公司的 plowback ratio（或 reinvestment ratio），通常计算为：

      plowback_k_t = ΔInvestedCapital_t / Adj_NOPAT_t

   其中：
   - ΔInvestedCapital（ΔIC）通常等于本期的“增长性再投资”或期末 Invested Capital 与期初 Invested Capital 的差值；在本讲义里也可用“Total Growth Capex”（有形的 growth capex + growth R&D）近似表示，因为它们度量的是年度的净扩张投入（流量）。
   - Adj_NOPAT 是把 expensed growth（被费用化的增长性支出）加回后的税后经营利润，使分子/分母在经济属性上可比。

   直观含义：plowback_k 表示每一元调整后经营利润被再投入到资本中的比例（或公司将多少比例的经营产出用于再投资以支撑增长）。在幻灯片中，Deere 的 plowback 大约在 0.4 左右（即将 ~40% 的 Adj NOPAT 再投入），因此若假定公司长期 ROIC=20%，则长期增长 g ≈ k × ROIC = 0.4 × 20% = 8%。

   为什么要这样计算／这个比率有什么用：
   - 它把“投入强度”（公司把利润重投入到资本中以推动增长的程度）与“资本效率”（ROIC）分离开来：长期增长 ≈ reinvestment_rate × ROIC。这比直接用 CapEx 或 R&D 更直观地把增长分为“多少投入 × 每单位投入产出多少”。

   实践细节与注意事项：
   - ΔIC 的定义要小心：可以用（NetInvestedCapital_t − NetInvestedCapital_{t-1}）或用当年 Total Growth Capex（列8）；若使用后者，注意是否包含 disposals / acquisitions 等一次性项目。
   - 常会对 plowback 做平滑（3–5 年移动平均或用中位数），因为单年波动大（受并购/处置、会计时点影响）；幻灯片右图是逐年柱状，观察趋势但建模时建议用平滑值作为长期假设 k。
   - 分子与分母的一致性：若你在分母把历史 R&D 资本化并把 product portfolio 纳入 Invested Capital，就必须在分子使用 Adj NOPAT（加回 expensed growth），否则分子/分母会不匹配导致 ROIC 失真。
   - 选择长期 ROIC：ROIC 可用历史平均或行业比较值，并且对 terminal 假设做敏感性分析；不要把最近异常高/低的单年 ROIC 直接当成长期值。
   - 图中 2004–2025 的柱子表示每年的 plowback（未平滑），用于观察 Deere 的 reinvestment 稳定性与周期性。

   建议的建模步骤：
   1. 计算每年 Total Growth Capex（列8），或直接计算净 Invested Capital 的年差（ΔIC）。
   2. 计算 Adj NOPAT（加回 expensed growth）。
   3. 计算 plowback_k_t = ΔIC / Adj_NOPAT_t，每年得一个比率。对长期假设用 3–5 年移动平均或 5 年中位数。
   4. 选一个长期 ROIC（历史或同行），然后 g = k_long × ROIC_long 得到长期经营性增长贡献。

   是否要我：
   - （A）把幻灯片右图的年度 plowback 用 `Deere` 的数据复现为一张小表并给 3/5 年移动平均示例，或
   - （B）把上面所有要点再简化为一段可直接发给 TA 的简短问题？

   请选择 A 或 B，我来继续。 

   ---

   ## 给 TA 的问题（请帮我确认 / 解释）

   1) 我对幻灯片上的期望回报分解式有些不确定：
      - 公式我理解为 R_{t,t+1} = D_t/V_t + g_{t,t+1} + (1+g_{t,t+1}) * h_{t,t+1}，其中 h 是“估值倍数的变化率”。请确认我的理解是否正确，并简要说明 h 正负值各代表什么？

   2) 幻灯片里显示“当起点倍数为最低值时，历史上 observed 的 expected return 也最低”。请帮我解释这是哪些因素共同造成的：
      - 是因为在起点倍数很低的样本中，后续的 h 往往为负（倍数继续下行或没有回归）？
      - 还是因为那些低倍数时期通常伴随基本面 g 很差或 D/V 很低？还是两者兼有？

   3) 表中按不同起点倍数给出的 h（和对应的 R）是如何计算的？
      - 用的是从那个起点向后固定 horizon（比如 5 年）观测到的平均倍数变化吗？
      - 是否做了样本筛选、对异常值处理或分行业/分周期加权？

   4) 实务上，当估值处于历史低位时，怎样区分“便宜（margin of safety）”和“价值陷阱（structural decline）”？有没有推荐的量化清单或顺序（比如先看 ROIC 趋势、利润率、资本开支、杠杆、需求展望等）？

   5) 如果我要用幻灯片里的数值做一次示例代入（计算一个 5 年 horizon 的 expected return），常见的做法是用历史平均 h 还是用条件在低分位时的 h？在选择 h 时有什么判别标准或经验法则？

   6) 在建模时，通常应该如何在“倍数回升”和“基本面改善”之间分配未来回报的来源？老师在课堂上对两者的相对重要性有没有偏好或建议的框架？

   7) 若要复现幻灯片中按起点倍数统计的表格（计算不同起点倍数下的平均 h 与 R），老师推荐使用哪些数据处理细节或代码实践（数据频率、取对数、样本长度、窗口设定、异常处理等）？

   请把这些问题帮我确认下要点，我会拿去问 TA（如果你建议删减或改写某些问题以更简洁明了，也请指出）。

   ---

   ### 我的理解（待确认）

   - 幻灯片里以“当前倍数 30”为起点，比较了若在未来 5 年内倍数达到过去十年中的平均/最低/最高值时的预期回报。
   - 期望回报由三部分构成：股利率 D/V、基本面增长 g、以及估值倍数变化贡献 (1+g)*h。即使 h 为负，只要 D/V 和 g 足够正，总回报仍然可以为正——因此“最低倍数对应最低 R”并不矛盾，可能因为同时伴随较差的 g 或负的 h。

   请 TA 帮忙确认上述描述是否准确，或者指出我理解中的具体错误或遗漏。

   ---

   ## CapEx 与 R&D（整理）

   简短结论先说：这里的 “CE” 应该是指 CapEx（资本支出）；CapEx 和 R&D 都是公司为未来增长做的投资，但会在财务报表上以不同项目出现、会计处理不同，建模/估值时需要把两者都当作“再投资”来处理，而不是只把 CapEx 当成投资、把 R&D 当成纯成本。

   关键点（简洁版）
   - CE = CapEx：买机器、厂房、设备等有形资产。出现在现金流量表的“投资活动现金流（Cash flow from investing）”里（通常为负值），在资产负债表上形成固定资产（PP&E），以后通过折旧流入利润表（非现金费用）。
   - R&D（研发）：通常在利润表里作为营业费用（OPEX），直接降低营业利润/税后利润；在现金流量表上通常体现在较低的经营现金流（因为净利润低），但不会像 CapEx 那样单独出现在“投资活动现金流”里（除非按照会计准则被资本化）。
   - 会计差异：在多数情况下（尤其 US GAAP），R&D 被当期费用化；在 IFRS 下，如果满足“开发阶段”条件可资本化为无形资产。会计处理不同会改变报表表现，但经济本质——都是为未来创造回报的投入——相同。

   为什么幻灯片说“二者都要考虑”
   - 讲者把两者都看作增长投资（growth investments）：CapEx 增强产能/实力，R&D 产生新产品/更高附加值，两者最终都可能提高未来利润率和现金流。
   - 在分解 expected return 时，不仅要看倍数变化 h（估值回归/扩张），还要看 g（基本面增长）和当前收益率 D/V。R&D 的效果往往体现在未来 g 的提升，CapEx 既影响 g 也影响资本基数和折旧。

   建模/估值时的常用处理（可选做法，按从简单到严谨排列）
   1. 最简单（保守、常见）：把 R&D 继续当作营业费用处理，CapEx 单独计入投资现金流；在计算再投资率（reinvestment）时，把 R&D 加入（reinvestment = CapEx + ΔNWC + R&D），说明把 R&D 也看成一项再投资支出。
   2. 资本化调整（更严谨）：将历史 R&D 资本化（把过去若干年的 R&D 累计计入 Invested Capital，按合理年限摊销），同时在利润表上把对应的摊销计入折旧/摊销项；优点是 ROIC/ROE 的分母反映了实际投入资本，避免把重要的增长性投入当作“当期成本”稀释盈利率。
   3. 区分维护 vs 增长：估计 maintenance CapEx / maintenance R&D（保持当前业务所需的最低投入），把超出的部分当成“增长投资”；这在预测长期增长和资本效率时很有用。

   实操步骤（你可以直接在模型里做）
   - 在报表里找：CapEx 在现金流量表的“购置固定资产/长期资产”项（CFI）；R&D 在利润表的“研发费用”或“研发”行；如果 IFRS 报表有“资本化研发”会在资产负债表或附注披露。
   - 若采用资本化法：把历史若干年的 R&D 累计（减去已摊销），加入期末 Invested Capital；把历史年报净利润里对应的 R&D 加回（以便 NOPAT 与 Invested Capital 匹配）。
   - 若采用简单法：预测期每年的 R&D 作为与 CapEx 同类的“再投资”流出，纳入 Reinvestment 计算（计算 expected return 时把它计入 g 的来源）。

   常见问 TA 的简短问题（你可以直接发问）
   - “课程里把 CE、R&D 都当成增长投资，请问在估值模型里推荐把 R&D 当期费用化还是资本化？有没有统一做法或推荐的资本化年限/摊销方法？”
   - “在计算 ROIC 与 Invested Capital 时，老师通常是否把历史 R&D 资本化进入投入资本？若是，常用多长摊销期？”
   - “在把 R&D 加入 reinvestment 时，是否需要区分 maintenance vs growth R&D？常用的经验比例或判断标准是什么？”

   要我帮你做的（选一项）
   - 把上面要问 TA 的三句问题压缩成一条邮件/Slack 文本；或
   - 在 `Session 06 Note.md` 里把 R&D 的资本化示例（含公式）补充进去；或
   - 用 `Deere` 的数据（工作区里有 Deere 资料）示范一次把 R&D 作为再投资代入 expected return 的快速计算。

   你选哪个，我来接着做。

   ---

   ## 说明：ROIC 表 — `Growth capex`（解读表格各列）

   这张表把有形资产的 CapEx/Depreciation 与无形/产品相关的 R&D 和 "product portfolio" 分开，最后合并成“Total Growth Capex”。关键行列解释如下：

   - 列 1 `Capex`：当年对有形固定资产（PPE）的现金支出（流量）。
   - 列 2 `Depreciation`：当期会计折旧（流量，非现金），对应有形资产被消耗的那部分。
   - 列 3 `Growth capex` = 列1 − 列2：用来近似“有形资产净增量（当年扩张性投资）”。当 CapEx 小于 Depreciation 时会为负，表示净存量在下降。

   - 列 4 `Product Portfolio`：代表公司的产品/无形资产存量（一个存量数字），通常是历年资本化的产品开发投入或与产品相关的无形资产（capitalized product assets）的余额。
   - 列 5 `R&D`：当年发生的研发费用（流量），大多数情况下在利润表中被费用化。

   - 列 6 `Maintenance expense`：表中假设为 `0.2 × Product Portfolio`（即每年产品存量有 20% 的消耗/维持成本），因此列标题里写的是 “6 = 2 × 4” 中的“2”并不是列2，而是系数 0.2 的简写。举例：Product Portfolio=1,735 → maintenance ≈ 0.2×1,735 = 347，与表格数字吻合。
      - 含义：把产品存量按某个比率“消耗”或摊销，作为维持性 R&D/维护性开支的代理。用比例而不是会计折旧，是因为无形产品/技术的经济消耗更适合按存量的一定比例表示（即每年有一定比例的产品需要更新维护或淘汰）。

   - 列 7 `Growth expenses` = 列5 − 列6：把当年 R&D 减掉为维持现有产品组合所需的 maintenance 部分后，剩下的就是“增长性研发投入”（投入到扩展或创造新产品上）。因此表头写 7 = 5 − 6。

   - 列 8 `Total Growth Capex` = 列3 + 列7：把有形资产的“净扩张”（列3）和无形/产品方面的“增长性开支”（列7）合并，得到公司总体的增长性再投资流量。

   为什么假设每年“lose 20% of product portfolio”？
   - 这是一个常见的简化假设，用来把无形资产/产品存量的经济消耗（obsolescence、产品退市、技术过时等）量化为年度维持开支的代理。20% 代表每年需要用 ~20% 的存量去维持或替换（即“摊销/维持率”）。具体比例可基于行业、公司寿命或管理层指引调整。

   为什么要这样分？
   - 会计把很多 R&D 当期费用化会把增长性投入掩盖掉，直接看利润表/CapEx 可能低估公司为增长实际投的资本。通过把 `product portfolio` 视为存量并用一个维持率计算 maintenance，再把超出部分计为增长性投入，可以把有形与无形投资统一计入“再投资/增长资本”口径，便于计算 ROIC 与 reinvestment。

   补充说明（实务注意事项）：
   - 表中 `product portfolio` 的初始来源可能来自历史资本化 R&D 或经营模型的假设，需要查附注或模型定义确认。
   - 维护率（20%）是假设，敏感性很大；在实际建模中应做情景分析或基于公司披露/行业经验调整。
   - 这种处理把 R&D 的“维持 vs 增长”分开，便于估算真正推动未来 g 的再投资部分。

   如果你要，我可以把这段整理成一段简短要发给 TA 的文本，或者用 `Deere/Output/epv_results.txt`（或其它 Deere 文件）里数据做一行行的示例计算来演示数值如何得到。你选一个。 

   ---

   ## Adjusted NOPAT（解释）

   这页表的核心目的：把会计上被当期费用化的、但经济上属于“增长性投资”的支出加回到营业利润，使分子（NOPAT）与分母（若把这些支出资本化后的 Invested Capital）在经济属性上匹配，从而计算更有意义的 ROIC。

   表中各列含义与计算：
   - `Op. Income`：营业利润（已包含折旧/摊销等）。
   - `Expensed Growth`：前表的 `Growth expenses`（R&D 减去 maintenance），即当年被费用化但属增长型的支出。因为会计把这部分直接计入营业费用，会把营业利润拉低；但从估值/ROIC 角度，这部分应视为投资并计入投入资本。
   - `Adj. Op. Income` = `Op. Income` + `Expensed Growth`：把增长性被费用化项目加回后的营业利润。
   - `Adj. NOPAT` = (1 - 税率) × `Adj. Op. Income`：对调整后的营业利润计算税后经营利润。

   为什么不把 `Growth Capex`（有形资产的增长性 CapEx）也直接加回到营业利润？
   - 有形增长性投入通常在现金流量表的投资活动中体现（CapEx），并在资产负债表上形成 Net PPE（或 Invested Capital）；其对利润表的影响是通过未来的折旧逐期体现。为了避免把同一项投资在分子与分母中重复计量，常见做法是：把有形增长投资计入分母（Invested Capital），而不把 CapEx 作为当期回到分子；相对地，把被当期费用化的无形增长投资加回分子，以与资本化处理保持一致。

   关于折旧：折旧是有形资产在利润表里的消耗表示，应保留在营业利润里（因为分母里包含了净存量）；我们通过把 R&D 的增长性部分加回分子来修正因会计政策（费用化）带来的不匹配。

   实务建议：
   - 如果你在分母把历史 R&D 资本化（或把 product portfolio 计入 Invested Capital），则在分子要把对应的 expensed growth 加回。否则分子/分母会不对称，导致 ROIC 低估。
   - 税率的选择可以用公司实际有效税率或模型需要的边际税率。

   简短例子：营业利润 3,000；当年 expensed growth = 600；税率 25% → Adj NOPAT = (3,000+600)×(1-0.25)=2,700；未调整时 NOPAT=(3,000)×0.75=2,250，会低估对资本的回报。

   如果你愿意，我可以把这一段再精简成发给 TA 的两三行问题，或者直接用 `Deere` 的数据（工作区里的文件）做一行示例计算。你选哪种？

   ---

   ## 规模效应与进入者能否匹配产量（整理）

   问题背景：课堂常说“规模带来成本优势（规模效应）”，因固定成本高、单位变动成本低， incumbents 在大产量下平均成本较低；但有时又说进入者可以匹配 incumbents 的产量并分割市场，你觉得前者也对，为什么后者还能成立？

   要点总结（并非矛盾，而是依赖不同假设）：
   - 规模优势的核心：当固定成本大、产能利用率高时，平均成本随产量下降——新进入者在初期规模小，平均成本通常较高，不能在同一价格下盈利地复制 incumbents 的产量。
   - 但进入者能“匹配/分割市场”的情形包括：
      1) 市场足够大或具有可分割的细分市场（incumbent 并不需要保持全市场份额），entrant 目标不同细分，双方并存；
      2) entrant 拥有不同的成本结构或技术（更低固定成本或更低变动成本），因此在某价格下也能盈利；
      3) entrant 通过外包、租赁产能或短期合作获得规模（绕开高前期固定投资），快速提供大产量；
      4) incumbent 受产能约束或战略性选择不扩产（例如维持高价），这为 entrant 留出空间；
      5) 产品/服务差异化（非完全同质），使得“匹配数量”变成市场细分与共享而非纯价格战；
      6) contestable market（可进入/退出）理论下，即使 entrant 没有长期规模优势，潜在入市也能影响 incumbents 的行为。
   - 另外，战略互动（如 limit pricing、价格歧视或短期补贴）会影响 entrant 能否进入并保持产量。

   结论：两种说法都对——规模效应说明了进入的难度与成本劣势；但在现实中存在许多机制（市场分割、技术差异、外包产能、产能约束、产品差异化、或政策/合约等）使得 entrant 能以较高平均成本进入并与 incumbents 分市场或共同存在。因此要看具体假设：是否存在高不可回收的 sunk cost、是否能获得外部规模、市场是否可细分、以及是否有技术/产品差异。

   建议发给 TA 的简短问题（可直接复制发问）：
   "在课堂上提到进入者可以匹配 incumbents 的产量并分割市场。请问这种结论基于哪些关键假设？在什么情况下规模优势会完全阻止分割市场的可能性（例如 sunk cost、产能不可租赁、完全同质产品）？"

   是否要我把这一段直接加入笔记（已加入），或把上面那句问题改写得更简短直接发 TA？

   ---

   ## 规模保护（scale protection）与客户束缚（customer captivity）

   原文摘录大意："A big scale that won't protect you. It only protects you if and only if bundled with some form of customer captivity — because even if an entrant matches your scale, they won't be able to peel customers away."

   解释要点（简洁）：
   - 规模（large scale）本身能够带来成本优势，但这种优势只有在客户无法或不愿轻易流失的情况下才真正保护 incumbents。换言之，规模是必要条件但非充分条件。
   - "Customer captivity" 指一切能让客户留在你体系里的机制：高切换成本（financial/operational/learning costs）、长期合约、捆绑/生态系统、网络效应、强品牌或专有服务/配件/售后保障（例如零件供应、维修网络、融资方案等）。

   为什么二者要同时存在：
   - 若 entrant 能以外包、租赁产能、预售或更低成本/新技术迅速复制产量，单纯的规模优势不再能阻止他们提供相似数量的产出；此时若没有客户束缚，客户可能会转向更便宜或更有吸引力的替代者。
   - 但若有客户束缚（例如买家长期合约、换厂成本高、核心系统深度嵌入客户运营、或必须通过指定经销商/服务网络），即便 entrant 能匹配产量，也无法轻易把客户“剥离”过去，规模保护才有效。

   实际例子：
   - 企业软件：供应商规模大但关键是 switching cost 与数据/集成锁定，客户难以迁移。
   - 工业设备（比如拖拉机）：规模＋广泛服务/零配件网络＋融资方案，使客户长期黏着；单纯有产能并不足以抢走客户。

   模型与实务建议：
   - 在判断“是否被规模保护”时，同时检查：切换成本、合同期、服务/配件网络、产品差异化与生态、网络效应强度、客户集中度。
   - 在估值中：若存在高客户束缚，可假设更低的需求弹性、更稳定的价格/利润和更高的可持续 ROIC；否则对入市竞争与逼迫利润的风险要更保守地建模（做情景）。

   一句可直接发 TA 的问法：
   "课堂提到：规模只有在配合 customer captivity 时才保护 incumbents。请问老师在实务上判断 customer captivity 强弱时最重视哪些证据（合约、切换成本、服务网络、生态/捆绑、还是其他）？"

   ---

   ## Decreasing marginal value of investment in technology platforms（追加解释）

   1) 含义（为什么会发生）
   - 初始投资能带来高边际价值：平台早期的投资（功能、用户获取、网络效应）通常快速提升用户价值和收入，边际 ROIC 高。
   - 随着规模与用户基数增长，边际收益递减：用户边际获取成本上升、可获得的高质量增量用户减少、网络效应接近饱和、功能/产品的增量改进产生的边际收益下降，导致每多投一元在长期产生的额外 NOPAT 下降。
   - 另外，维护/合规/安全成本可能随平台复杂度上升而上升，使净边际回报进一步降低。

   2) 竞争动态影响
   - 早期竞赛阶段：高边际回报吸引大量投资者/入局者，竞争主要围绕用户获取、补贴与速度（winner-takes-most）。
   - 饱和阶段：边际回报降低，竞争转为保留现有用户、提高单用户终身价值（LTV）、服务多样化与捆绑；价格/补贴战减缓但对利润压缩仍敏感。
   - 多边平台与多家多宿主（multi‑homing）：如果用户/开发者容易多平台并存（multi‑home），边际价值更快递减；若单边锁定强，边际价值衰减慢。
   - 对手反应：当边际价值下降时，竞争者更可能通过差异化、垂直化或提供互补服务来争夺剩余价值，而不是单纯价格战。

   3) 为什么这对估值/建模重要
   - 不要假设长期每一元再投资都有同样的 ROIC；应用递减函数（例如逐步下降的 marginal ROIC 或饱和型增长函数）。
   - 在预测 reinvestment 时，给出边际 ROIC 的路径（例如前 3 年高、后 5 年递减到长期平稳低值），并做敏感性分析。终值阶段建议采用更保守的 ROIC 与更低的 reinvestment rate。

   4) 对应的策略（企业层面）
   - 通过提高 switching costs、增加生态/捆绑、独占内容或增加平台深度来延缓边际回报递减。\
   - 将投资从纯用户数量转向提高单用户收益、企业客户合同或差异化高级服务。

   ---

   ## Quantity pre-commitments（数量预承诺）及其竞争作用

   1) 定义与形式
   - Quantity pre-commitment 指在竞争或谈判中，企业提前以可观察/可执行的方式锁定未来产能、采购或供给数量（例如建设产能、签长期供货合约、take-or-pay 合同、长期订单、或提前预定产能）。

   2) 战略逻辑与博弈论基础
   - 作为承诺（commitment）：预先承诺高产能或大采购能改变竞争博弈的策略空间（Stackelberg leader 的经典逻辑），迫使对手在后手受到更严格限制。\
   - 限制产能入侵：若 incumbents 承诺大产能并显示愿意以较低价格供应整个市场，entrant 将面临低价竞争与薄利，降低进入吸引力。\
   - 信号与信誉：长期合同或资本支出向市场与客户传递长期供给/服务的信号，增加 entrant 抢占客户的难度。

   3) 常见工具与例子
   - Take‑or‑pay 合同（能源、航空发动机、半导体晶圆预订）
   - 预售/定金、长期供货协议、备货协议
   - 大规模产能建设或长期租赁产能（使短期价格战成本高）

   4) 限制与风险
   - 预承诺需要付出真实成本（沉没成本或长期负担），若市场需求错误估计，承诺会带来长期负担。\
   - 在高度不确定或需求易变的行业，过度承诺可能被对手利用（诱导过度产能再压低价格）。

   5) 对估值与竞争分析的启示
   - 评估承诺的可信度：是否有真实投资/合同做担保？是否易被对手复制或买通？
   - 在模型中把由于承诺带来的短期价格/份额保护体现在更低的竞争折价或更高的可持续市场份额；但要建情景并考虑承诺失败/需求逆转的风险。

   简短结论：技术平台的再投资并非线性增值，边际收益会下降；企业用提高客户粘性、生态与前置数量承诺来维持或转移边际收益，但这些手段有成本与风险。建模时应明确边际 ROIC 路径、承诺的可信度，并做情景分析。

   ---

   ## Market power vs. Market share（补充说明）

   - Core point: Market share or large scale can be a precondition for market power, but it is not the same thing. Scale gives potential advantage (lower average cost, visibility, distribution) but market power means the firm can sustainably earn a markup over marginal cost or capture economic profits.

   - What market power means:
      - The practical ability to set price (or extract margin) above marginal cost without losing so many customers that profits disappear. In formal terms, a firm with market power can maintain a positive Lerner index (P - MC)/P or sustain ROIC > WACC over time.
      - It can also mean the ability to do something no other firm can do (unique capability, exclusive access, patent-protected product, or a bundled ecosystem) that creates a wedge between price and marginal cost.

   - Why share ≠ power:
      - High share without barriers: a large incumbent may still be vulnerable if customers can switch easily, inputs are contestable, or rivals can match product quality and service. Then scale alone won't prevent price competition.
      - Power requires durability: evidence of persistent pricing above marginal cost (long-run excess returns), not just a temporary markup from e.g. a one-off shock.

   - Typical sources of sustainable market power:
      - High switching costs, long-term contracts or ecosystem lock-in (customer captivity)
      - Proprietary technology, patents, or unique assets
      - Network effects that create winner‑take‑most dynamics and raise the cost of switching
      - Control over scarce inputs or distribution channels
      - Regulatory barriers or franchised monopolies

   - How to use this in analysis:
      - Look for evidence of durability (persistent margins, stable high ROIC, contractual protections).
      - Distinguish temporary markups (short-term pricing power) from sustainable market power. Use measures like Lerner index, persistent excess returns, or durability of margins across cycles.
      - When you see “scale” mentioned in class as a protection, check whether it is bundled with customer captivity or other barriers. If not, treat scale as necessary but not sufficient.

   Short example: a large manufacturer with low unit costs (scale) but no service network or switching costs may lose customers to a rival that rents capacity and offers lower upfront price. Conversely, a smaller firm with proprietary software and strong lock-in can exercise substantial market power despite lower scale.

   我已把这段加入笔记；需要我把上面某几句翻成中文或精简成一条可发给 TA 的问句吗？

   ---

   ## 租金分配：消费者剩余、生产者剩余 与 股东捕获（补充）

   1) 基本概念（简洁）
   - 消费者剩余（consumer surplus）：消费者愿意支付的价格（价值）减去实际支付价格，代表消费者从交易中获得的净福利。
   - 生产者剩余 / 经济租（producer surplus / economic rent）：市场价格减去边际成本（P − MC），再减去必须支付给其他要素的正常回报后，留下的超额收益。企业层面最终的可分配剩余要扣除运营成本、税收和再投资。
   - 股东捕获（shareholder capture）：企业在支付了工资、供应商费用、税收以及必须的维持性再投资之后，留给股东的净剩余（分红 + 留存收益），也就是股东实际能享有的经济租。

   2) 为什么课堂讨论会说“要考虑把租金归谁捕获（消费者还是股东）”？
   - 讨论不是只关乎“要不要付钱”，而是关于经济剩余如何在市场参与者之间分配：价格高于边际成本时，会产生生产者剩余；但这部分剩余可能被转移给消费者（通过较低价格/折扣）、被员工/供应商捕获（通过更高工资或更高采购价）、被政府通过税收捕获，或留给股东作为利润。是否能留给股东取决于竞争、合约、成本结构与企业再投资需求。

   3) 在建模/估值里如何分解（实用步骤）
      - 先估算市场价格 P 与边际成本 MC：生产者剩余 ≈ (P − MC) × Q（总量）。
      - 从生产者剩余中扣除必要的运营费用、税收以及维持性再投资（maintenance capex + maintenance R&D），剩余即为可分配给股东的自由利润（pretax）。
      - 再扣税及任何股东以外的分配（例如优先股利），剩下的是股东可得的经济租（分红或留存以增长公司价值）。

   4) 回到你写的那句（“consumer has rent of illness to pay minus the price and the firm has the prove of price minus cost and after stretching out the expenses, the leftover are for shareholders”）：
   - 这句话有道理——它描述了经济剩余如何从总量（价值）被拆分：消费者得到（愿付 − 实付），企业得到（实付 − 变动成本），但企业要先用这笔钱付运营成本、再投资和税，最终剩余才归股东。因此课堂上讨论的“who captures rent”是在问“创造的超额价值最终落到谁手里”，而不是指某个即时的额外付款。

   5) 实务上的判断要点（用于提问或模型假设）
   - 看是否有能力把价格持续设高于 MC（是否有市场权力）。
   - 看边际成本的可替代性与价格弹性：高弹性会把超额收益挤走给消费者，低弹性容易让厂商捕获。
   - 分析固定/变动成本结构与再投资需求：若企业需要大量增长性再投资，短期的生产者剩余会被再投资吞没，股东短期未必能捕获。长期股东捕获取决于 ROIC 与 reinvestment 的组合。
   - 考虑合约/制度因素（如长期合约、补贴、监管或税制），它们会改变剩余的分配结构。

   6) 可直接发给 TA 的一句问法（供你复制）：
   "课堂上讨论的 rent capture 问题，是在探讨公司创造的超额价值最终归谁（消费者、员工/供应商、政府 或 股东）的问题。请问在做这类分配分析时老师通常优先检查哪些证据来判断超额收益最终落到股东手里（价格与 MC 差、需求弹性、维持性再投资规模、长约/切换成本 等）？"

   小结：这段讨论不是单纯问“我们现在需不需要付钱给谁”，而是要分析价值创造后的分配链条——谁先拿走（成本/税/再投），谁最终得到股东收益。
