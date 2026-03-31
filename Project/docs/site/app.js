const I18N = {
  zh: {
    lang_label: '语言 / Language',
    hero_title: 'AI 价值投资分析网站',
    hero_sub: '这是一个基于哥伦比亚大学价值投资课程（Graham & Dodd）方法论搭建的小型估值网站，用真实股票数据展示 AV / EPV / FV 三层估值框架。',
    btn_repo: '查看项目仓库',
    btn_json: '下载结果 JSON',
    section_results: '真实样例结果（本地模型计算）',
    sample_line: '样例标的',
    analysis_date: '分析日期',
    data_source: '数据来源',
    assumptions_title: '课件对标假设（本次样例）',
    checks_title: '公式校验与一致性检查',
    av_desc: '从账面权益出发，对 PPE、商誉、品牌、员工价值等进行调整，衡量资产安全垫。',
    epv_desc: '基于可持续盈利能力（平滑利润 + 调整项 + WACC）估算企业在零增长假设下的价值。',
    fv_desc: '当 `ROIC > WACC` 时增长创造价值；在严格课件模式下，`ROIC < WACC` 会得到负 FV（增长摧毁价值）。',
    valuation_chart_title: '总估值对比（可交互）',
    valuation_chart_note: '悬停查看金额、相对市值比例、相对总估值比例',
    av_chart_title: 'AV 组件拆解（可交互）',
    av_chart_note: '悬停查看每个组件金额及在 AV 中的占比',
    logic_title: '分析逻辑（简化）',
    logic_1: 'Step 1：抓取与清洗财务数据（资产负债表、利润表、现金流、市场数据）',
    logic_2: 'Step 2：计算 AV（资产重估）与 EPV（持续盈利价值）',
    logic_3: 'Step 3：比较 ROIC 与 WACC，计算 FV（增长价值）与总估值',
    logic_4: 'Step 4：输出结构化结果并做可视化，便于快速决策与沟通',
    value_title: '项目价值',
    value_desc: '将课堂估值方法变成可复用工具链：数据获取 → 模型计算 → 可视化解释 → 报告导出。面向投研场景可快速复现并扩展到不同公司。',
    doc_formula: '公式对照文档',
    doc_process: 'WMT 过程说明',
    doc_assumptions: 'WMT 假设 JSON',
    doc_gaps: '已知边界与限制',
    kpi_market_cap: '市值',
    kpi_av: 'AV',
    kpi_epv: 'EPV',
    kpi_fv: 'FV',
    kpi_total: '总价值',
    kpi_wacc: 'WACC',
    kpi_roic: 'ROIC',
    kpi_mos: '安全边际',
    tooltip_amount: '金额',
    tooltip_vs_mkt: '占市值',
    tooltip_vs_total: '占总估值',
    tooltip_vs_av: '占 AV',
    no_assumptions: '暂无假设说明',
    no_checks: '暂无校验项'
  },
  en: {
    lang_label: 'Language / 语言',
    hero_title: 'AI Value Investing Analytics Site',
    hero_sub: 'A compact valuation website built on Columbia (Graham & Dodd) methodology, showing AV / EPV / FV outputs with real stock data.',
    btn_repo: 'View GitHub Repository',
    btn_json: 'Download Result JSON',
    section_results: 'Real Sample Output (Local Model Run)',
    sample_line: 'Sample Ticker',
    analysis_date: 'Analysis Date',
    data_source: 'Data Source',
    assumptions_title: 'Course-Aligned Assumptions (This Run)',
    checks_title: 'Formula & Consistency Checks',
    av_desc: 'Starts from book equity and applies PPE/goodwill/brand/workforce adjustments to estimate asset protection value.',
    epv_desc: 'Estimates zero-growth value from sustainable earnings (smoothed profit + adjustments + WACC).',
    fv_desc: 'When `ROIC > WACC`, growth creates value; under strict course mode, `ROIC < WACC` yields negative FV.',
    valuation_chart_title: 'Valuation Comparison (Interactive)',
    valuation_chart_note: 'Hover to see amount, % of market cap, and % of total valuation',
    av_chart_title: 'AV Component Breakdown (Interactive)',
    av_chart_note: 'Hover to see amount and % contribution to AV',
    logic_title: 'Analysis Logic (Simplified)',
    logic_1: 'Step 1: Fetch and normalize financial statements and market data',
    logic_2: 'Step 2: Compute AV (asset revaluation) and EPV (earning power)',
    logic_3: 'Step 3: Compare ROIC vs WACC and compute FV plus total valuation',
    logic_4: 'Step 4: Output structured results and visualization for communication',
    value_title: 'Project Value',
    value_desc: 'Turns classroom valuation methods into a reusable pipeline: data fetch → model compute → explainable charts → report export.',
    doc_formula: 'Formula Mapping',
    doc_process: 'WMT Process Notes',
    doc_assumptions: 'WMT Assumptions JSON',
    doc_gaps: 'Known Gaps & Limits',
    kpi_market_cap: 'Market Cap',
    kpi_av: 'AV',
    kpi_epv: 'EPV',
    kpi_fv: 'FV',
    kpi_total: 'Total Value',
    kpi_wacc: 'WACC',
    kpi_roic: 'ROIC',
    kpi_mos: 'Margin of Safety',
    tooltip_amount: 'Amount',
    tooltip_vs_mkt: '% vs Market Cap',
    tooltip_vs_total: '% vs Total Value',
    tooltip_vs_av: '% of AV',
    no_assumptions: 'No assumptions available',
    no_checks: 'No checks available'
  }
};

function t(lang, key) {
  return (I18N[lang] && I18N[lang][key]) || I18N.zh[key] || key;
}

function num(value, digits = 2) {
  return Number(value ?? 0).toFixed(digits);
}

function pct(value, digits = 2) {
  return `${num(value, digits)}%`;
}

function translateStatic(lang) {
  document.documentElement.lang = lang === 'en' ? 'en' : 'zh-CN';
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.getAttribute('data-i18n');
    el.textContent = t(lang, key);
  });
}

function localizeName(name, lang) {
  const map = {
    'Market Cap': { zh: '市值', en: 'Market Cap' },
    'Total Value': { zh: '总价值', en: 'Total Value' },
    'Book Equity': { zh: '账面权益', en: 'Book Equity' },
    'Current Asset Adj': { zh: '流动资产调整', en: 'Current Asset Adj' },
    'PPE Adj': { zh: 'PPE 调整', en: 'PPE Adj' },
    'Goodwill Adj': { zh: '商誉调整', en: 'Goodwill Adj' },
    'Operating Lease': { zh: '经营租赁', en: 'Operating Lease' },
    'Brand Value': { zh: '品牌价值', en: 'Brand Value' },
    'Workforce Value': { zh: '员工价值', en: 'Workforce Value' },
    'Product Portfolio': { zh: '产品组合', en: 'Product Portfolio' }
  };
  return (map[name] && map[name][lang]) || name;
}

function renderValuationChart(payload, lang) {
  if (!window.echarts) return;
  const dom = document.getElementById('valuationChart');
  const chart = echarts.init(dom);

  const marketCap = Number(payload.summary.market_cap_b || 0);
  const totalValue = Number(payload.summary.total_value_b || 0);
  const values = payload.chart_data.valuation_compare || [];

  chart.setOption({
    backgroundColor: 'transparent',
    grid: { left: 55, right: 20, top: 28, bottom: 40 },
    xAxis: {
      type: 'category',
      data: values.map(v => v.name),
      axisLabel: { color: '#c4cde8', fontSize: 11 },
      axisLine: { lineStyle: { color: '#3b4a78' } }
    },
    yAxis: {
      type: 'value',
      name: 'USD Bn',
      nameTextStyle: { color: '#9eb0d8' },
      axisLabel: { color: '#c4cde8' },
      splitLine: { lineStyle: { color: '#23325a' } }
    },
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(11,16,32,0.95)',
      borderColor: '#3a4d85',
      textStyle: { color: '#e7efff' },
      formatter: (p) => {
        const v = Number(p.value || 0);
        const pctMkt = marketCap > 0 ? (v / marketCap * 100) : 0;
        const pctTotal = totalValue > 0 ? (v / totalValue * 100) : 0;
        return [
          `<strong>${localizeName(p.name, lang)}</strong>`,
          `${t(lang, 'tooltip_amount')}：${num(v)} B`,
          `${t(lang, 'tooltip_vs_mkt')}：${pct(pctMkt)}`,
          `${t(lang, 'tooltip_vs_total')}：${pct(pctTotal)}`
        ].join('<br/>');
      }
    },
    series: [{
      type: 'bar',
      data: values.map(v => Number(v.value_b || 0)),
      barMaxWidth: 44,
      itemStyle: {
        borderRadius: [8, 8, 0, 0],
        color: (p) => ['#6c7ea8', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'][p.dataIndex] || '#6a8dff'
      },
      label: {
        show: true,
        position: 'top',
        color: '#dbe6ff',
        formatter: (x) => `${num(x.value, 1)}B`
      }
    }]
  });

  window.addEventListener('resize', () => chart.resize());
}

function renderAVChart(payload, lang) {
  if (!window.echarts) return;
  const dom = document.getElementById('avChart');
  const chart = echarts.init(dom);

  const avTotal = Number(payload.summary.av_b || 0);
  const entries = payload.chart_data.av_breakdown || [];

  chart.setOption({
    backgroundColor: 'transparent',
    grid: { left: 58, right: 24, top: 28, bottom: 70 },
    xAxis: {
      type: 'category',
      data: entries.map(i => i.name),
      axisLabel: {
        color: '#c4cde8',
        interval: 0,
        rotate: 25,
        fontSize: 10
      },
      axisLine: { lineStyle: { color: '#3b4a78' } }
    },
    yAxis: {
      type: 'value',
      name: 'USD Bn',
      nameTextStyle: { color: '#9eb0d8' },
      axisLabel: { color: '#c4cde8' },
      splitLine: { lineStyle: { color: '#23325a' } }
    },
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(11,16,32,0.95)',
      borderColor: '#3a4d85',
      textStyle: { color: '#e7efff' },
      formatter: (p) => {
        const v = Number(p.value || 0);
        const share = avTotal > 0 ? (v / avTotal * 100) : 0;
        return [
          `<strong>${localizeName(p.name, lang)}</strong>`,
          `${t(lang, 'tooltip_amount')}：${num(v)} B`,
          `${t(lang, 'tooltip_vs_av')}：${pct(share)}`
        ].join('<br/>');
      }
    },
    series: [{
      type: 'bar',
      barMaxWidth: 34,
      data: entries.map(i => Number(i.value_b || 0)),
      itemStyle: {
        borderRadius: [8, 8, 0, 0],
        color: '#22d3ee'
      },
      label: {
        show: true,
        position: 'top',
        color: '#dbe6ff',
        fontSize: 10,
        formatter: (x) => `${num(x.value, 1)}B`
      }
    }]
  });

  window.addEventListener('resize', () => chart.resize());
}

function renderPage(data, lang) {
  const kpis = document.getElementById('kpis');
  const companyName = document.getElementById('companyName');
  const ticker = document.getElementById('ticker');
  const analysisDate = document.getElementById('analysisDate');
  const dataSource = document.getElementById('dataSource');
  const assumptionsList = document.getElementById('assumptionsList');
  const checksList = document.getElementById('checksList');

  const s = data.summary;

  companyName.textContent = s.company;
  ticker.textContent = s.ticker;
  analysisDate.textContent = s.analysis_date;
  dataSource.textContent = `${data.source.provider} + ${data.source.engine}`;

  const rows = [
    [t(lang, 'kpi_market_cap'), `${num(s.market_cap_b)}B`],
    [t(lang, 'kpi_av'), `${num(s.av_b)}B`],
    [t(lang, 'kpi_epv'), `${num(s.epv_b)}B`],
    [t(lang, 'kpi_fv'), `${num(s.fv_b)}B`],
    [t(lang, 'kpi_total'), `${num(s.total_value_b)}B`],
    [t(lang, 'kpi_wacc'), pct(s.wacc_pct)],
    [t(lang, 'kpi_roic'), pct(s.roic_pct)],
    [t(lang, 'kpi_mos'), pct(s.margin_of_safety_pct)]
  ];

  kpis.innerHTML = rows
    .map(([label, value]) => `<div class="kpi"><div class="label">${label}</div><div class="value">${value}</div></div>`)
    .join('');

  const assumptions = data.assumptions || {};
  assumptionsList.innerHTML = Object.entries(assumptions)
    .map(([k, v]) => `<div class="mini-item"><div class="k">${k}</div><div class="v">${v}</div></div>`)
    .join('') || `<div class="mini-item"><div class="v">${t(lang, 'no_assumptions')}</div></div>`;

  const checks = data.consistency_checks || {};
  checksList.innerHTML = Object.entries(checks)
    .map(([k, v]) => `<div class="mini-item"><div class="k">${k}</div><div class="v">${v}</div></div>`)
    .join('') || `<div class="mini-item"><div class="v">${t(lang, 'no_checks')}</div></div>`;

  renderValuationChart(data, lang);
  renderAVChart(data, lang);
}

async function loadData() {
  const langSelect = document.getElementById('langSelect');

  try {
    const resp = await fetch('./assets/sample_results.json');
    const data = await resp.json();
    const preferredLang = localStorage.getItem('site_lang') || 'zh';
    langSelect.value = preferredLang;
    translateStatic(preferredLang);
    renderPage(data, preferredLang);

    langSelect.addEventListener('change', () => {
      const lang = langSelect.value;
      localStorage.setItem('site_lang', lang);
      translateStatic(lang);
      renderPage(data, lang);
    });
  } catch (e) {
    const kpis = document.getElementById('kpis');
    kpis.innerHTML = '<div class="card">Unable to load result file / 无法加载结果文件</div>';
  }
}

loadData();
