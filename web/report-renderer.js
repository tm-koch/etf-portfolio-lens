const REPORT_COLORS = [
  '#2563eb', '#0f9d8a', '#e76f51', '#d4a72c', '#8b5cf6', '#0891b2',
  '#db2777', '#65a30d', '#ea580c', '#475569', '#7c3aed', '#059669',
];

function createElement(tagName, className, text) {
  const element = document.createElement(tagName);
  if (className) element.className = className;
  if (text !== undefined && text !== null) element.textContent = text;
  return element;
}

function appendCell(row, text, tagName = 'td', className = '') {
  row.append(createElement(tagName, className, text));
}

function buildTable(headers, rows, className) {
  const table = createElement('table', className);
  const head = table.createTHead().insertRow();
  headers.forEach((header) => appendCell(head, header, 'th', ''));
  const body = table.createTBody();
  rows.forEach((values) => {
    const row = body.insertRow();
    values.forEach((value) => appendCell(row, value.text, 'td', value.className || ''));
  });
  return table;
}

export function partitionReportColumns(columns, maximumPerPanel = 8) {
  const panels = [];
  for (let start = 0; start < columns.length; start += maximumPerPanel) {
    panels.push({ start, end: Math.min(start + maximumPerPanel, columns.length), columns: columns.slice(start, start + maximumPerPanel) });
  }
  return panels;
}

function appendSection(root, title, key) {
  const section = createElement('section', 'pdf-report-section');
  section.dataset.reportSection = key;
  section.append(createElement('h2', 'pdf-report-section-title', title));
  root.append(section);
  return section;
}

function appendDefinitionList(container, entries) {
  const list = createElement('dl', 'pdf-report-metrics');
  for (const [label, value] of entries) {
    const metric = createElement('div', 'pdf-report-metric');
    metric.append(createElement('dt', '', label), createElement('dd', '', value));
    list.append(metric);
  }
  container.append(list);
}

function appendRollup(container, title, values, { translateTaxonomy, formatPercent, unavailable }) {
  const block = createElement('section', 'pdf-report-rollup');
  block.append(createElement('h4', '', title));
  const entries = Object.entries(values || {}).sort((first, second) => second[1] - first[1]);
  if (!entries.length) {
    block.append(createElement('p', 'pdf-report-unavailable', unavailable));
  } else {
    const list = createElement('ul', 'pdf-report-rollup-list');
    for (const [label, value] of entries) {
      const item = createElement('li');
      item.append(createElement('span', '', translateTaxonomy(label)), createElement('strong', '', formatPercent(value)));
      list.append(item);
    }
    block.append(list);
  }
  container.append(block);
}

function appendChart(container, key, title, chartData, options) {
  const figure = createElement('figure', 'pdf-report-chart');
  figure.dataset.reportChart = key;
  figure.append(createElement('h3', '', title));
  if (!chartData?.labels?.length || !chartData.series?.length) {
    figure.append(createElement('p', 'pdf-report-unavailable', options.unavailable));
    container.append(figure);
    return;
  }

  const canvas = createElement('canvas', 'pdf-report-chart-canvas');
  canvas.width = 720;
  canvas.height = 420;
  canvas.setAttribute('role', 'img');
  canvas.setAttribute('aria-label', title);
  const canvasFrame = createElement('div', 'pdf-report-chart-canvas-wrap');
  canvasFrame.append(canvas);
  figure.append(canvasFrame);

  const legend = createElement('ul', 'pdf-report-chart-legend');
  chartData.labels.forEach((label, index) => {
    const item = createElement('li');
    const swatch = createElement('span', 'pdf-report-chart-swatch');
    swatch.style.backgroundColor = REPORT_COLORS[index % REPORT_COLORS.length];
    swatch.setAttribute('aria-hidden', 'true');
    item.append(swatch, createElement('span', '', options.translateTaxonomy(label)));
    legend.append(item);
  });
  figure.append(legend);
  container.append(figure);

  const Chart = globalThis.Chart;
  if (typeof Chart !== 'function') return;
  const displayLabels = chartData.labels.map(options.translateTaxonomy);
  const datasets = chartData.series.map((series, index) => ({
    label: series.label,
    data: chartData.labels.map((label) => Number(series.values?.[label]) || 0),
    backgroundColor: chartData.labels.map((_, labelIndex) => REPORT_COLORS[labelIndex % REPORT_COLORS.length]),
    borderColor: '#ffffff',
    borderWidth: 2,
    weight: chartData.series.length > 1 ? 1 : 2,
  }));
  const chart = new Chart(canvas, {
    type: 'doughnut',
    data: { labels: displayLabels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      cutout: '28%',
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label(context) {
              return `${context.dataset.label}: ${options.formatPercent(Number(context.raw) || 0)}`;
            },
          },
        },
      },
    },
  });
  options.chartInstances.push(chart);
}

function appendHeatmap(container, rows, options) {
  if (!rows?.length) {
    container.append(createElement('p', 'pdf-report-unavailable', options.unavailable));
    return;
  }
  const products = rows.map((row) => row.product);
  const panels = partitionReportColumns(products);
  panels.forEach((panel, panelIndex) => {
    const panelElement = createElement('div', `pdf-report-heatmap-panel${panelIndex ? ' pdf-report-company-panel--continued' : ''}`);
    if (panels.length > 1) {
      panelElement.append(createElement('h4', '', options.t('export.overlapPanel', {
        start: panel.start + 1,
        end: panel.end,
      })));
    }
    const table = createElement('table', 'pdf-report-heatmap');
    const head = table.createTHead().insertRow();
    appendCell(head, '', 'th', 'pdf-report-heatmap-identity');
    panel.columns.forEach((product) => appendCell(head, product.ticker, 'th', ''));
    const body = table.createTBody();
    rows.forEach((row) => {
      const tableRow = body.insertRow();
      appendCell(tableRow, row.product.ticker, 'th', 'pdf-report-heatmap-identity');
      panel.columns.forEach((_, columnOffset) => {
        const cell = row.cells[panel.start + columnOffset];
        let text = '';
        let className = 'pdf-report-heatmap-cell';
        if (cell.type === 'diagonal') {
          text = '—';
          className += ' is-diagonal';
        } else if (cell.type === 'unavailable') {
          text = options.unavailable;
          className += ' is-unavailable';
        } else if (cell.type === 'overlap') {
          text = options.formatPercent(cell.overlapPct);
          className += cell.nearIdentical ? ' is-near-identical' : ' is-overlap';
        }
        appendCell(tableRow, text, 'td', className);
      });
    });
    panelElement.append(table);
    container.append(panelElement);
  });
}

export function destroyReportCharts(chartInstances = []) {
  chartInstances.forEach((chart) => chart?.destroy());
  chartInstances.length = 0;
}

export function renderReportDocument({
  root,
  snapshot,
  analytics,
  allocationOnly = false,
  t,
  formatCount,
  formatDecimal,
  formatPercent,
  formatCurrency,
  translateTaxonomy,
  chartInstances = [],
} = {}) {
  destroyReportCharts(chartInstances);
  root.replaceChildren();
  root.lang = snapshot.locale;
  root.classList.add('pdf-report');
  const unavailable = t('export.noData');

  const portfolio = appendSection(root, t('export.sectionPortfolio'), 'portfolio');
  const privateColumns = allocationOnly ? [] : [
    { key: 'shares', label: snapshot.portfolioMode === 'percentage' ? t('export.allocation') : t('export.shares') },
    { key: 'unitPrice', label: t('export.unitPrice') },
    { key: 'marketValue', label: t('export.marketValue') },
  ];
  const headers = [t('ui.etf'), t('export.portfolioStatus'), ...privateColumns.map((column) => column.label), t('export.portfolioWeight')];
  const positionRows = snapshot.etfs.map(({ entry, portfolioPosition }) => {
    const inPortfolio = Boolean(portfolioPosition);
    const valuation = portfolioPosition?.valuation;
    const quantity = snapshot.portfolioMode === 'percentage'
      ? formatPercent(Number(portfolioPosition?.shares) || 0)
      : formatCount(Number(portfolioPosition?.shares) || 0);
    const price = valuation?.price == null
      ? unavailable
      : formatCurrency(valuation.price, valuation.currency || 'CHF');
    const value = valuation?.valueChf == null ? unavailable : formatCurrency(valuation.valueChf, 'CHF');
    const cells = [
      { text: `${entry?.ticker || entry?.isin || ''} · ${entry?.name || ''}` },
      { text: t(inPortfolio ? 'export.inPortfolio' : 'export.catalogOnly') },
    ];
    if (!allocationOnly) {
      cells.push(
        { text: inPortfolio ? quantity : unavailable },
        { text: inPortfolio ? price : unavailable },
        { text: inPortfolio ? value : unavailable },
      );
    }
    cells.push({ text: inPortfolio ? formatPercent(portfolioPosition.weightPct) : unavailable });
    return cells;
  });
  portfolio.append(buildTable(headers, positionRows, 'pdf-report-table pdf-report-portfolio-table'));

  const analyticsSection = appendSection(root, t('export.sectionAnalytics'), 'analytics');
  analyticsSection.append(createElement('h3', '', t('export.summaryMetrics')));
  const summaryEntries = [
    [t('summary.positions'), formatCount(analytics.summary.positions || 0)],
    [t('summary.underlyingHoldings'), formatCount(analytics.summary.underlyingHoldings || 0)],
    [t('summary.sharedCompanies'), formatCount(analytics.summary.sharedCompanies || 0)],
  ];
  if (!allocationOnly) {
    summaryEntries.splice(1, 0, [
      t('summary.shareUnits'),
      analytics.summary.shareUnits == null ? unavailable : formatCount(analytics.summary.shareUnits),
    ]);
    summaryEntries.splice(2, 0, [
      t('summary.totalValue'),
      analytics.summary.totalValueChf == null ? unavailable : formatCurrency(analytics.summary.totalValueChf, 'CHF'),
    ]);
  }
  appendDefinitionList(analyticsSection, summaryEntries);

  analyticsSection.append(createElement('h3', '', t('export.exposureRollups')));
  const rollups = createElement('div', 'pdf-report-rollups');
  appendRollup(rollups, t('rollup.sectorExposure'), analytics.rollups.sector, { translateTaxonomy, formatPercent, unavailable });
  appendRollup(rollups, t('rollup.regionExposure'), analytics.rollups.region, { translateTaxonomy, formatPercent, unavailable });
  appendRollup(rollups, t('rollup.currencyExposure'), analytics.rollups.currency, { translateTaxonomy, formatPercent, unavailable });
  analyticsSection.append(rollups);

  analyticsSection.append(createElement('h3', '', t('explore.redundancyTitle')));
  const scoreEntries = [
    [t('export.redundancy'), analytics.redundancy?.available ? formatPercent(analytics.redundancy.score) : unavailable],
    [t('export.diversification'), analytics.diversification?.available ? formatDecimal(analytics.diversification.score) : unavailable],
    [t('export.coverage'), analytics.diversification?.coveragePct == null ? unavailable : formatPercent(analytics.diversification.coveragePct)],
  ];
  appendDefinitionList(analyticsSection, scoreEntries);

  analyticsSection.append(createElement('h3', 'pdf-report-top-companies-title', t('export.topCompanies')));
  const companyPanels = partitionReportColumns(analytics.etfColumns);
  if (analytics.companies.length) {
    companyPanels.forEach((panel, panelIndex) => {
      const panelElement = createElement('div', `pdf-report-company-panel${panelIndex ? ' pdf-report-company-panel--continued' : ''}`);
      if (companyPanels.length > 1) {
        panelElement.append(createElement('h4', '', t('export.contributionPanel', {
          start: panel.start + 1,
          end: panel.end,
        })));
      }
      const companyHeaders = [
        t('export.rank'),
        t('export.company'),
        t('export.totalContribution'),
        ...panel.columns.map((column) => column.ticker),
      ];
      const companyRows = analytics.companies.map((company) => [
        { text: formatCount(company.rank) },
        { text: company.name },
        { text: formatPercent(company.totalContribution) },
        ...company.contributions.slice(panel.start, panel.end).map((contribution) => ({
          text: contribution.value == null ? '—' : formatPercent(contribution.value),
          className: contribution.value == null ? 'is-unavailable' : '',
        })),
      ]);
      panelElement.append(buildTable(companyHeaders, companyRows, 'pdf-report-table pdf-report-company-table'));
      analyticsSection.append(panelElement);
    });
  } else {
    analyticsSection.append(createElement('p', 'pdf-report-unavailable', unavailable));
  }

  const exposure = appendSection(root, t('export.sectionExposure'), 'exposure');
  const charts = createElement('div', 'pdf-report-charts');
  exposure.append(charts);
  appendChart(charts, 'sector', t('chart.titleSectors'), analytics.charts.sector, { chartInstances, unavailable, translateTaxonomy, formatPercent });
  appendChart(charts, 'region', t('chart.titleRegions'), analytics.charts.region, { chartInstances, unavailable, translateTaxonomy, formatPercent });
  appendChart(charts, 'currency', t('chart.titleCurrencies'), analytics.charts.currency, { chartInstances, unavailable, translateTaxonomy, formatPercent });
  exposure.append(createElement('h3', 'pdf-report-pairwise-title', t('export.pairwiseOverlap')));
  appendHeatmap(exposure, analytics.pairwiseHeatmap, { unavailable, formatPercent, t });
  return root;
}
