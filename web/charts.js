const CHART_COLORS = [
  '#1f7ae0',
  '#18a0d6',
  '#19b7b0',
  '#2ac18a',
  '#60c85a',
  '#8cc83f',
  '#f0b83d',
  '#f08b3d',
  '#f05b76',
  '#e056a6',
  '#9b7bff',
  '#5f8cff',
];

function hexToRgba(hex, alpha) {
  const normalized = hex.replace('#', '');
  const red = Number.parseInt(normalized.slice(0, 2), 16);
  const green = Number.parseInt(normalized.slice(2, 4), 16);
  const blue = Number.parseInt(normalized.slice(4, 6), 16);
  return `rgba(${red}, ${green}, ${blue}, ${alpha})`;
}

function paletteColor(index, alpha = 0.9) {
  return hexToRgba(CHART_COLORS[index % CHART_COLORS.length], alpha);
}

function colorForLabel(label, index, alpha = 0.9, labelColorOverrides = new Map()) {
  const override = labelColorOverrides.get(label);
  if (override) {
    return hexToRgba(override, alpha);
  }
  return paletteColor(index, alpha);
}

function buildDatasets(metricData, labels, labelColorOverrides = new Map()) {
  return metricData.map((series, index) => ({
    label: series.label,
    data: labels.map((label) => series.values.get(label) ?? 0),
    backgroundColor: labels.map((label, labelIndex) => colorForLabel(label, labelIndex, 0.94 - index * 0.04, labelColorOverrides)),
    borderColor: '#ffffff',
    borderWidth: 1,
    weight: metricData.length > 1 ? 1 : 2,
  }));
}

function createOptions(title, options = {}) {
  const {
    legendLabelOverrides = new Map(),
    legendMode = 'datasets',
    labelColorOverrides = new Map(),
  } = options;

  return {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '36%',
    rotation: 0,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#152033',
          boxWidth: 12,
          usePointStyle: true,
          pointStyle: 'circle',
          generateLabels(chart) {
            if (legendMode === 'labels') {
              const labelTexts = chart.data.labels || [];
              const colors = chart.data.datasets[0]?.backgroundColor || [];
              return labelTexts.map((labelText, index) => ({
                text: legendLabelOverrides.get(labelText) || labelText,
                fillStyle: colors[index] || '#67d3ff',
                strokeStyle: '#ffffff',
                lineWidth: 1,
                hidden: false,
                index,
              }));
            }

            const labels = Chart.defaults.plugins.legend.labels.generateLabels(chart);
            return labels.map((label) => ({
              ...label,
              text: legendLabelOverrides.get(label.text) || label.text,
            }));
          },
        },
      },
      title: {
        display: false,
        text: title,
      },
      tooltip: {
        callbacks: {
          title(context) {
            const first = context[0];
            if (!first) {
              return [];
            }
            const seriesLabel = first.dataset.label || 'Series';
            const heading = seriesLabel === 'Portfolio reference (share-weighted)'
              ? seriesLabel
              : `ETF: ${seriesLabel}`;
            return [heading, `${title}: ${first.label}`];
          },
          label(context) {
            const value = Number(context.raw || 0);
            return `Share: ${value.toFixed(1)}%`;
          },
        },
      },
    },
  };
}

export function renderComparisonChart(chartRef, canvas, title, metricData, labels, options = {}) {
  if (!canvas) {
    return null;
  }
  if (chartRef.current) {
    chartRef.current.destroy();
  }
  if (!metricData.length || !labels.length) {
    const context = canvas.getContext('2d');
    if (context) {
      context.clearRect(0, 0, canvas.width, canvas.height);
    }
    return null;
  }
  chartRef.current = new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels,
      datasets: buildDatasets(metricData, labels, options.labelColorOverrides),
    },
    options: createOptions(title, options),
  });
  return chartRef.current;
}

export function destroyComparisonCharts(chartRefs) {
  for (const ref of chartRefs) {
    if (ref.current) {
      ref.current.destroy();
      ref.current = null;
    }
  }
}
