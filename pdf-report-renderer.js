import { CHART_COLORS } from './chart-palette.js';

const PAGE_LEFT = 8;
const PAGE_RIGHT = 8;
const PAGE_TOP = 12;
const FOOTER_MARGIN = 23;
const TEXT_COLOR = [23, 33, 43];
const MUTED_COLOR = [82, 97, 111];
const BORDER_COLOR = [213, 220, 227];
const HEADER_COLOR = [237, 242, 246];
const SURFACE_COLOR = [247, 249, 251];
const PAGE_WIDTH = 297;
const PAGE_HEIGHT = 210;
const SCORE_VERDICT_COLORS = {
  low: [201, 232, 200],
  moderate: [248, 221, 162],
  high: [245, 208, 209],
  highlyConcentrated: [245, 208, 209],
  concentrated: [246, 214, 188],
  moderatelyDiversified: [248, 221, 162],
  wellDiversified: [220, 228, 185],
  highlyDiversified: [201, 232, 200],
};

function addSectionTitle(pdf, title, y = PAGE_TOP) {
  pdf.setFont('SpaceGrotesk', 'bold');
  pdf.setFontSize(18);
  pdf.setTextColor(...TEXT_COLOR);
  pdf.text(title, PAGE_LEFT, y);
  pdf.setDrawColor(...TEXT_COLOR);
  pdf.setLineWidth(0.6);
  pdf.line(PAGE_LEFT, y + 3, PAGE_WIDTH - PAGE_RIGHT, y + 3);
  return y + 11;
}

function addSubheading(pdf, title, y, options = {}) {
  const { size = 11, before = 3, after = 5 } = options;
  const nextY = y + before;
  pdf.setFont('SpaceGrotesk', 'bold');
  pdf.setFontSize(size);
  pdf.setTextColor(...TEXT_COLOR);
  pdf.text(title, PAGE_LEFT, nextY);
  return nextY + after;
}

function addCategoryPageHeading(pdf, parentTitle, categoryTitle) {
  const y = addSectionTitle(pdf, parentTitle);
  return addSubheading(pdf, categoryTitle, y, { size: 11, before: 0, after: 5 });
}

function addTable(pdf, autoTable, options) {
  autoTable(pdf, {
    theme: 'grid',
    margin: { left: PAGE_LEFT, right: PAGE_RIGHT, top: PAGE_TOP, bottom: FOOTER_MARGIN },
    styles: {
      font: 'SpaceGrotesk',
      fontStyle: 'normal',
      fontSize: 7.5,
      cellPadding: 2,
      textColor: TEXT_COLOR,
      lineColor: BORDER_COLOR,
      lineWidth: 0.2,
      overflow: 'linebreak',
      valign: 'middle',
    },
    headStyles: {
      font: 'SpaceGrotesk',
      fontStyle: 'bold',
      fillColor: HEADER_COLOR,
      textColor: TEXT_COLOR,
    },
    alternateRowStyles: { fillColor: [250, 251, 252] },
    rowPageBreak: 'avoid',
    showHead: 'everyPage',
    ...options,
  });
  return pdf.lastAutoTable?.finalY || options.startY || PAGE_TOP;
}

function addPageTitle(pdf, title) {
  pdf.addPage();
  return addSectionTitle(pdf, title);
}

function addMetricCards(pdf, entries, y) {
  const gap = 4;
  const cardWidth = (PAGE_WIDTH - PAGE_LEFT - PAGE_RIGHT - gap * 2) / 3;
  const cardHeight = 20;
  const rowGap = 3;
  const rowCount = Math.ceil(entries.length / 3);

  entries.forEach(([label, value], index) => {
    const column = index % 3;
    const row = Math.floor(index / 3);
    const x = PAGE_LEFT + column * (cardWidth + gap);
    const cardY = y + row * (cardHeight + rowGap);
    pdf.setDrawColor(...BORDER_COLOR);
    pdf.setFillColor(...SURFACE_COLOR);
    pdf.roundedRect(x, cardY, cardWidth, cardHeight, 1, 1, 'FD');
    pdf.setFont('SpaceGrotesk', 'normal');
    pdf.setFontSize(7);
    pdf.setTextColor(...MUTED_COLOR);
    const labelLines = pdf.splitTextToSize(label, cardWidth - 4).slice(0, 2);
    pdf.text(labelLines, x + 2, cardY + 5);
    pdf.setFont('SpaceGrotesk', 'bold');
    pdf.setFontSize(11);
    pdf.setTextColor(...TEXT_COLOR);
    pdf.text(String(value), x + 2, cardY + 16);
  });
  return y + rowCount * (cardHeight + rowGap) + 2;
}

function addScoreCards(pdf, entries, y) {
  const gap = 4;
  const cardWidth = (PAGE_WIDTH - PAGE_LEFT - PAGE_RIGHT - gap) / 2;
  const cardHeight = 20;

  entries.forEach(({ label, value, verdict, verdictColor }, index) => {
    const x = PAGE_LEFT + index * (cardWidth + gap);
    pdf.setDrawColor(...BORDER_COLOR);
    pdf.setFillColor(...SURFACE_COLOR);
    pdf.roundedRect(x, y, cardWidth, cardHeight, 1, 1, 'FD');
    pdf.setFont('SpaceGrotesk', 'normal');
    pdf.setFontSize(7);
    pdf.setTextColor(...MUTED_COLOR);
    pdf.text(pdf.splitTextToSize(label, cardWidth - 6).slice(0, 1), x + 3, y + 5);
    pdf.setFont('SpaceGrotesk', 'bold');
    pdf.setFontSize(11);
    pdf.setTextColor(...TEXT_COLOR);
    pdf.text(String(value), x + 3, y + 16);

    if (verdict && verdictColor) {
      const badgeWidth = Math.min(verdict.length * 2 + 6, cardWidth / 2);
      const badgeX = x + cardWidth - badgeWidth - 3;
      const badgeY = y + 10;
      pdf.setFillColor(...verdictColor);
      pdf.roundedRect(badgeX, badgeY, badgeWidth, 7, 1, 1, 'F');
      pdf.setFont('SpaceGrotesk', 'bold');
      pdf.setFontSize(6.5);
      pdf.setTextColor(...TEXT_COLOR);
      pdf.text(verdict, badgeX + 3, badgeY + 4.7);
    }
  });
  return y + cardHeight + 2;
}

function addRollupCards(pdf, analytics, { t, translateTaxonomy, formatPercent, unavailable }, y) {
  const groups = [
    [t('rollup.sectorExposure'), analytics.rollups?.sector],
    [t('rollup.regionExposure'), analytics.rollups?.region],
    [t('rollup.currencyExposure'), analytics.rollups?.currency],
  ];
  const gap = 4;
  const cardWidth = (PAGE_WIDTH - PAGE_LEFT - PAGE_RIGHT - gap * 2) / 3;
  const entriesByGroup = groups.map(([title, values]) => {
    const entries = Object.entries(values || {}).sort((first, second) => second[1] - first[1]);
    if (entries.length > 20) {
      const remainder = entries.slice(20).reduce((total, [, value]) => total + (Number(value) || 0), 0);
      entries.splice(20, entries.length - 20, [null, remainder]);
    }
    return [title, entries];
  });
  const rowCount = Math.max(1, ...entriesByGroup.map(([, entries]) => entries.length));
  const rowHeight = 3.2;
  const cardHeight = 11 + rowCount * rowHeight;

  entriesByGroup.forEach(([title, entries], index) => {
    const x = PAGE_LEFT + index * (cardWidth + gap);
    pdf.setDrawColor(...BORDER_COLOR);
    pdf.setFillColor(...SURFACE_COLOR);
    pdf.roundedRect(x, y, cardWidth, cardHeight, 1, 1, 'FD');
    pdf.setFont('SpaceGrotesk', 'bold');
    pdf.setFontSize(8);
    pdf.setTextColor(...TEXT_COLOR);
    pdf.text(title, x + 3, y + 5);
    if (!entries.length) {
      pdf.setFont('SpaceGrotesk', 'normal');
      pdf.setFontSize(7);
      pdf.setTextColor(...MUTED_COLOR);
      pdf.text(unavailable, x + 3, y + 10);
      return;
    }
    entries.forEach(([label, value], row) => {
      const rowY = y + 10 + row * rowHeight;
      pdf.setFont('SpaceGrotesk', 'normal');
      pdf.setFontSize(6.8);
      pdf.setTextColor(...TEXT_COLOR);
      const displayLabel = label === null ? t('export.otherRollup') : translateTaxonomy(label);
      const labelLines = pdf.splitTextToSize(displayLabel, cardWidth - 28).slice(0, 1);
      pdf.text(labelLines, x + 3, rowY);
      pdf.setFont('SpaceGrotesk', 'medium');
      pdf.text(formatPercent(value), x + cardWidth - 3, rowY, { align: 'right' });
    });
  });
  return y + cardHeight + 2;
}

function hasPortfolioValue(value) {
  return value != null
    && !(typeof value === 'string' && !value.trim())
    && Number.isFinite(Number(value));
}

function buildPortfolioRows(snapshot, { allocationOnly, t, formatCount, formatPercent, formatCurrency }) {
  const headers = [t('ui.etf'), t('export.portfolioStatus')];
  if (!allocationOnly) {
    headers.push(
      snapshot.portfolioMode === 'percentage' ? t('export.allocation') : t('export.shares'),
      t('export.unitPrice'),
      t('export.marketValue'),
    );
  }
  headers.push(t('export.portfolioWeight'));

  const rows = snapshot.etfs.map(({ entry, portfolioPosition }) => {
    const inPortfolio = Boolean(portfolioPosition);
    const valuation = portfolioPosition?.valuation;
    const row = [
      `${entry?.ticker || entry?.isin || ''} · ${entry?.name || ''}`,
      t(inPortfolio ? 'export.inPortfolio' : 'export.catalogOnly'),
    ];
    if (!allocationOnly) {
      row.push(
        !inPortfolio || !hasPortfolioValue(portfolioPosition?.shares)
          ? '—'
          : snapshot.portfolioMode === 'percentage'
            ? formatPercent(Number(portfolioPosition.shares))
            : formatCount(Number(portfolioPosition.shares)),
        !hasPortfolioValue(valuation?.price)
          ? '—'
          : formatCurrency(valuation.price, valuation.currency || 'CHF'),
        !hasPortfolioValue(valuation?.valueChf)
          ? '—'
          : formatCurrency(valuation.valueChf, 'CHF'),
      );
    }
    row.push(hasPortfolioValue(portfolioPosition?.weightPct)
      ? formatPercent(portfolioPosition.weightPct)
      : '—');
    return row;
  });
  return { headers, rows };
}

function renderPortfolio(pdf, autoTable, { snapshot, portfolioShareUrl, allocationOnly, t, formatCount, formatPercent, formatCurrency }) {
  let y = addSectionTitle(pdf, t('export.sectionPortfolio'));
  if (portfolioShareUrl) {
    const linkLabel = t('export.openPortfolio');
    const linkY = y + 2;
    pdf.setFont('SpaceGrotesk', 'medium');
    pdf.setFontSize(7);
    pdf.setTextColor(37, 99, 235);
    pdf.text(linkLabel, PAGE_LEFT, linkY);
    pdf.link(PAGE_LEFT, linkY - 3, pdf.getTextWidth(linkLabel), 4, { url: portfolioShareUrl });
    y += 8;
  }
  const { headers, rows } = buildPortfolioRows(snapshot, {
    allocationOnly,
    t,
    formatCount,
    formatPercent,
    formatCurrency,
  });
  const columnStyles = { 0: { cellWidth: 112 } };
  if (headers.length > 2) {
    columnStyles[1] = { cellWidth: 36 };
  }
  addTable(pdf, autoTable, {
    startY: y,
    head: [headers],
    body: rows,
    tableWidth: 'auto',
    columnStyles,
  });
}

function renderTopCompanies(pdf, autoTable, analytics, { t, formatCount, formatPercent, unavailable }) {
  const columns = analytics.etfColumns || [];
  const panels = partitionReportColumns(columns);
  const parentTitle = t('export.sectionAnalytics');
  const categoryTitle = t('export.topCompanies');
  pdf.addPage();
  let y = addCategoryPageHeading(pdf, parentTitle, categoryTitle);

  if (!analytics.companies?.length) {
    pdf.setFont('SpaceGrotesk', 'normal');
    pdf.setFontSize(8);
    pdf.setTextColor(...MUTED_COLOR);
    pdf.text(unavailable, PAGE_LEFT, y + 3);
    return;
  }

  panels.forEach((panel, panelIndex) => {
    if (panelIndex > 0) {
      pdf.addPage();
      y = addCategoryPageHeading(pdf, parentTitle, categoryTitle);
      pdf.setFont('SpaceGrotesk', 'medium');
      pdf.setFontSize(8);
      pdf.text(t('export.contributionPanel', { start: panel.start + 1, end: panel.end }), PAGE_LEFT, y);
      y += 5;
    }
    const headers = [t('export.rank'), t('export.company'), t('export.totalContribution'), ...panel.columns.map((column) => column.ticker)];
    const rows = analytics.companies.map((company) => [
      formatCount(company.rank),
      company.name,
      formatPercent(company.totalContribution),
      ...company.contributions.slice(panel.start, panel.end).map((entry) => entry.value == null ? '—' : formatPercent(entry.value)),
    ]);
    const columnStyles = {
      0: { cellWidth: 11, halign: 'right' },
      1: { cellWidth: 65 },
      2: { cellWidth: 30, halign: 'right' },
    };
    panel.columns.forEach((_, index) => {
      columnStyles[index + 3] = { cellWidth: 21.5, halign: 'right' };
    });
    y = addTable(pdf, autoTable, {
      startY: y,
      head: [headers],
      body: rows,
      margin: { left: PAGE_LEFT, right: PAGE_RIGHT, top: 32, bottom: FOOTER_MARGIN },
      willDrawPage: ({ pageNumber }) => {
        if (pageNumber > 1) addCategoryPageHeading(pdf, parentTitle, categoryTitle);
      },
      columnStyles,
      styles: { fontSize: 7, cellPadding: 1.6 },
    });
  });
}

function createDonutImage(chartData, { translateTaxonomy, formatPercent }) {
  const Chart = globalThis.Chart;
  if (typeof Chart !== 'function' || !globalThis.document?.createElement) return null;
  if (!chartData?.labels?.length || !chartData.series?.length) return null;

  const canvas = globalThis.document.createElement('canvas');
  canvas.width = 720;
  canvas.height = 720;
  const labels = chartData.labels.map(translateTaxonomy);
  const datasets = chartData.series.map((series, seriesIndex) => ({
    label: series.label,
    data: chartData.labels.map((label) => Number(series.values?.[label]) || 0),
    backgroundColor: chartData.labels.map((_, index) => CHART_COLORS[index % CHART_COLORS.length]),
    borderColor: '#ffffff',
    borderWidth: 2,
    weight: chartData.series.length > 1 ? 1 : 2,
  }));
  const chart = new Chart(canvas, {
    type: 'doughnut',
    data: { labels, datasets },
    options: {
      responsive: false,
      maintainAspectRatio: false,
      animation: false,
      cutout: '28%',
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label(context) {
              return `${context.dataset.label}: ${formatPercent(Number(context.raw) || 0)}`;
            },
          },
        },
      },
    },
  });
  const image = canvas.toDataURL('image/png');
  chart.destroy();
  return image;
}

function addChartLegend(pdf, labels, x, y, width, translateTaxonomy, columns = 2) {
  const columnWidth = width / columns;
  const rowHeights = [];
  const translated = labels.map(translateTaxonomy);
  translated.forEach((label, index) => {
    const column = index % columns;
    const row = Math.floor(index / columns);
    const itemX = x + column * columnWidth;
    const lines = pdf.splitTextToSize(label, columnWidth - 6);
    const itemY = y + row * 5;
    pdf.setFillColor(...hexToRgb(CHART_COLORS[index % CHART_COLORS.length]));
    pdf.rect(itemX, itemY - 2.2, 2.2, 2.2, 'F');
    pdf.setFont('SpaceGrotesk', 'normal');
    pdf.setFontSize(6.5);
    pdf.setTextColor(...TEXT_COLOR);
    pdf.text(lines.slice(0, 2), itemX + 3.5, itemY);
    rowHeights[row] = Math.max(rowHeights[row] || 5, Math.max(lines.length, 1) * 3.1);
  });
  return y + Math.max(0, ...rowHeights) * Math.ceil(translated.length / columns);
}

function hexToRgb(hex) {
  const normalized = hex.slice(1);
  return [0, 2, 4].map((offset) => Number.parseInt(normalized.slice(offset, offset + 2), 16));
}

function renderReportCover(pdf, { snapshot, coverIcon, t, formatTimestamp }) {
  if (coverIcon) {
    pdf.addImage(coverIcon, 'PNG', PAGE_LEFT, 59, 32, 32);
  }
  pdf.setFont('SpaceGrotesk', 'bold');
  pdf.setFontSize(24);
  pdf.setTextColor(...TEXT_COLOR);
  pdf.text('ETF Portfolio Lens', PAGE_LEFT + 40, 76);
  pdf.setDrawColor(...TEXT_COLOR);
  pdf.setLineWidth(0.6);
  pdf.line(PAGE_LEFT, 105, PAGE_WIDTH - PAGE_RIGHT, 105);

  const unavailable = t('common.unavailable');
  const format = typeof formatTimestamp === 'function'
    ? formatTimestamp
    : (value) => value || unavailable;
  const metadata = [
    [t('export.generatedAt'), format(snapshot.generatedAt)],
    [t('export.buildIdentifier'), snapshot.provenance.buildId || unavailable],
    [t('export.etfSnapshot'), format(snapshot.provenance.snapshotTimestamp)],
    [t('export.livePrices'), format(snapshot.provenance.livePricesTimestamp)],
  ];
  const gap = 16;
  const columnWidth = (PAGE_WIDTH - PAGE_LEFT - PAGE_RIGHT - gap) / 2;
  metadata.forEach(([label, value], index) => {
    const column = index % 2;
    const row = Math.floor(index / 2);
    const x = PAGE_LEFT + column * (columnWidth + gap);
    const y = 125 + row * 36;
    pdf.setFont('SpaceGrotesk', 'medium');
    pdf.setFontSize(7);
    pdf.setTextColor(...MUTED_COLOR);
    pdf.text(label, x, y);
    pdf.setFont('SpaceGrotesk', 'normal');
    pdf.setFontSize(9);
    pdf.setTextColor(...TEXT_COLOR);
    pdf.text(pdf.splitTextToSize(String(value), columnWidth).slice(0, 2), x, y + 8);
  });
}

function renderExposureCharts(pdf, analytics, { t, translateTaxonomy, formatPercent, unavailable }) {
  const charts = [
    ['chart.titleSectors', analytics.charts?.sector],
    ['chart.titleRegions', analytics.charts?.region],
    ['chart.titleCurrencies', analytics.charts?.currency],
  ];
  const gap = 10;
  const cardWidth = (PAGE_WIDTH - PAGE_LEFT - PAGE_RIGHT - gap * 2) / 3;
  const chartSize = 66.7;
  const imageY = 37;

  charts.forEach(([titleKey, chartData], index) => {
    const x = PAGE_LEFT + index * (cardWidth + gap);
    pdf.setFont('SpaceGrotesk', 'bold');
    pdf.setFontSize(9);
    pdf.setTextColor(...TEXT_COLOR);
    pdf.text(t(titleKey), x, 31);
    pdf.setDrawColor(...BORDER_COLOR);
    pdf.setLineWidth(0.35);
    pdf.line(x, 34, x + cardWidth, 34);
    const image = createDonutImage(chartData, { translateTaxonomy, formatPercent });
    if (image) {
      pdf.addImage(image, 'PNG', x + (cardWidth - chartSize) / 2, imageY, chartSize, chartSize);
      const legendColumns = index === 2 ? 4 : 2;
      addChartLegend(pdf, chartData.labels, x + 2, imageY + chartSize + 13, cardWidth - 4, translateTaxonomy, legendColumns);
    } else {
      pdf.setFont('SpaceGrotesk', 'normal');
      pdf.setFontSize(7);
      pdf.setTextColor(...MUTED_COLOR);
      pdf.text(unavailable, x + 3, imageY + chartSize / 2, { maxWidth: cardWidth - 6, align: 'center' });
    }
  });
}

function heatmapCell(value, unavailable, formatPercent) {
  if (value.type === 'diagonal') {
    return { content: '—', styles: { fillColor: [238, 242, 245], textColor: MUTED_COLOR } };
  }
  if (value.type === 'unavailable') {
    return { content: unavailable, styles: { textColor: MUTED_COLOR } };
  }
  if (value.type === 'empty') {
    return { content: '', styles: { fillColor: SURFACE_COLOR } };
  }
  if (value.nearIdentical) {
    return { content: formatPercent(value.overlapPct), styles: { fillColor: [252, 165, 165] } };
  }
  return { content: formatPercent(value.overlapPct), styles: { fillColor: [191, 219, 254] } };
}

function renderPairwiseHeatmap(pdf, autoTable, rows, { t, formatPercent, unavailable }) {
  const parentTitle = t('export.sectionExposure');
  const categoryTitle = t('export.pairwiseOverlap');
  pdf.addPage();
  let y = addCategoryPageHeading(pdf, parentTitle, categoryTitle);
  if (!rows?.length) {
    pdf.setFont('SpaceGrotesk', 'normal');
    pdf.setFontSize(8);
    pdf.setTextColor(...MUTED_COLOR);
    pdf.text(unavailable, PAGE_LEFT, y + 3);
    return;
  }
  const products = rows.map((row) => row.product);
  const panels = partitionReportColumns(products);
  panels.forEach((panel, panelIndex) => {
    if (panelIndex > 0) {
      pdf.addPage();
      y = addCategoryPageHeading(pdf, parentTitle, categoryTitle);
      pdf.setFont('SpaceGrotesk', 'bold');
      pdf.setFontSize(10);
      pdf.setTextColor(...TEXT_COLOR);
      pdf.text(t('export.overlapPanel', { start: panel.start + 1, end: panel.end }), PAGE_LEFT, y);
      y += 5;
    }
    const headers = ['', ...panel.columns.map((product) => product.ticker)];
    const body = rows.map((row) => [
      row.product.ticker,
      ...panel.columns.map((_, offset) => heatmapCell(row.cells[panel.start + offset], unavailable, formatPercent)),
    ]);
    const columnStyles = { 0: { cellWidth: 24, fontStyle: 'bold' } };
    panel.columns.forEach((_, index) => {
      columnStyles[index + 1] = { cellWidth: 30, halign: 'center', fontSize: 6.8 };
    });
    addTable(pdf, autoTable, {
      startY: y,
      head: [headers],
      body,
      margin: { left: PAGE_LEFT, right: PAGE_RIGHT, top: 32, bottom: FOOTER_MARGIN },
      willDrawPage: ({ pageNumber }) => {
        if (pageNumber > 1) addCategoryPageHeading(pdf, parentTitle, categoryTitle);
      },
      columnStyles,
      styles: { halign: 'center', fontSize: 6.8, cellPadding: 1.5 },
      pageBreak: 'auto',
    });
  });
}

export function partitionReportColumns(columns, maximumPerPanel = 8) {
  const panels = [];
  for (let start = 0; start < columns.length; start += maximumPerPanel) {
    panels.push({ start, end: Math.min(start + maximumPerPanel, columns.length), columns: columns.slice(start, start + maximumPerPanel) });
  }
  return panels;
}

export function renderReportDocument({
  pdf,
  autoTable,
  snapshot,
  analytics,
  portfolioShareUrl = null,
  coverIcon = null,
  allocationOnly = false,
  t,
  formatCount,
  formatDecimal,
  formatPercent,
  formatCurrency,
  formatTimestamp,
  translateTaxonomy,
} = {}) {
  const unavailable = t('export.noData');
  renderReportCover(pdf, { snapshot, coverIcon, t, formatTimestamp });
  pdf.addPage();
  renderPortfolio(pdf, autoTable, { snapshot, portfolioShareUrl, allocationOnly, t, formatCount, formatPercent, formatCurrency });

  let y = addPageTitle(pdf, t('export.sectionAnalytics'));
  y = addSubheading(pdf, t('export.summaryMetrics'), y);
  const summaryEntries = [
    [t('summary.positions'), formatCount(analytics.summary.positions || 0)],
    [t('summary.underlyingHoldings'), formatCount(analytics.summary.underlyingHoldings || 0)],
    [t('summary.sharedCompanies'), formatCount(analytics.summary.sharedCompanies || 0)],
  ];
  if (!allocationOnly) {
    summaryEntries.splice(1, 0, [t('summary.shareUnits'), analytics.summary.shareUnits == null ? unavailable : formatCount(analytics.summary.shareUnits)]);
    summaryEntries.splice(2, 0, [t('summary.totalValue'), analytics.summary.totalValueChf == null ? unavailable : formatCurrency(analytics.summary.totalValueChf, 'CHF')]);
  }
  y = addMetricCards(pdf, summaryEntries, y);
  y = addSubheading(pdf, t('export.exposureRollups'), y);
  y = addRollupCards(pdf, analytics, { t, translateTaxonomy, formatPercent, unavailable }, y);
  y = addSubheading(pdf, t('export.portfolioScores'), y);
  const scoreEntries = [
    {
      label: t('export.redundancy'),
      value: analytics.redundancy?.available ? formatPercent(analytics.redundancy.score) : unavailable,
      verdict: analytics.redundancy?.available && analytics.redundancy.level
        ? t(`explore.redundancy.${analytics.redundancy.level}`)
        : null,
      verdictColor: SCORE_VERDICT_COLORS[analytics.redundancy?.level],
    },
    {
      label: t('export.diversification'),
      value: analytics.diversification?.available ? formatDecimal(analytics.diversification.score) : unavailable,
      verdict: analytics.diversification?.available && analytics.diversification.rating
        ? t(`explore.diversification.${analytics.diversification.rating}`)
        : null,
      verdictColor: SCORE_VERDICT_COLORS[analytics.diversification?.rating],
    },
  ];
  addScoreCards(pdf, scoreEntries, y);

  renderTopCompanies(pdf, autoTable, analytics, { t, formatCount, formatPercent, unavailable });
  y = addPageTitle(pdf, t('export.sectionExposure'));
  renderExposureCharts(pdf, analytics, { t, translateTaxonomy, formatPercent, unavailable });
  renderPairwiseHeatmap(pdf, autoTable, analytics.pairwiseHeatmap, { t, formatPercent, unavailable });
  return pdf;
}
