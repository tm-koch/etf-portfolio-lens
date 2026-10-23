export const REPORT_WEBSITE_URL = 'https://tm-koch.github.io/etf-portfolio-lens/';

export function stampReportPdf(pdf, { snapshot, t, formatTimestamp, websiteUrl = REPORT_WEBSITE_URL }) {
  const pageCount = pdf.internal.getNumberOfPages();
  const pageWidth = pdf.internal.pageSize.getWidth();
  const pageHeight = pdf.internal.pageSize.getHeight();
  const left = 8;
  const right = pageWidth - 8;
  const firstLine = `${t('export.generatedAt')}: ${formatTimestamp(snapshot.generatedAt)}  |  ${t('export.buildIdentifier')}: ${snapshot.provenance.buildId || t('common.unavailable')}`;
  const secondLine = `${t('export.etfSnapshot')}: ${formatTimestamp(snapshot.provenance.snapshotTimestamp)}  |  ${t('export.livePrices')}: ${formatTimestamp(snapshot.provenance.livePricesTimestamp)}`;
  const websiteLabel = `${t('export.website')}: `;
  const websiteLine = `${websiteLabel}${websiteUrl}`;
  const footerTop = pageHeight - 18;

  pdf.setProperties({
    title: 'ETF Portfolio Lens report',
    subject: 'ETF portfolio and exposure report',
    creator: 'ETF Portfolio Lens',
  });
  for (let page = 1; page <= pageCount; page += 1) {
    pdf.setPage(page);
    pdf.setFont('helvetica', 'normal');
    pdf.setFontSize(6.5);
    pdf.setTextColor(71, 85, 105);
    pdf.setDrawColor(203, 213, 225);
    pdf.line(left, footerTop - 3, right, footerTop - 3);
    pdf.text(pdf.splitTextToSize(firstLine, right - left), left, footerTop);
    pdf.text(pdf.splitTextToSize(secondLine, right - left), left, footerTop + 3.5);
    pdf.text(websiteLine, left, footerTop + 7);
    const websiteLinkStart = left + pdf.getTextWidth(websiteLabel);
    const websiteLinkWidth = pdf.getTextWidth(websiteUrl);
    pdf.link(websiteLinkStart, footerTop + 4.5, websiteLinkWidth, 3.5, { url: websiteUrl });
    pdf.text(t('export.page', { page, total: pageCount }), right, footerTop + 7, { align: 'right' });
  }
  return pdf;
}

export function createReportPdfOptions(snapshot) {
  const filenameDate = String(snapshot.generatedAt || new Date().toISOString()).slice(0, 10);
  return {
    margin: [8, 8, 23, 8],
    filename: `etf-portfolio-lens-report-${filenameDate}.pdf`,
    image: { type: 'png', quality: 1 },
    enableLinks: true,
    html2canvas: {
      scale: 2,
      useCORS: false,
      backgroundColor: '#ffffff',
      logging: false,
      scrollX: 0,
      scrollY: 0,
      windowWidth: 1040,
    },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'landscape', compress: true },
    pagebreak: {
      mode: ['css', 'legacy'],
      before: [
        '.pdf-report-section[data-report-section="analytics"]',
        '.pdf-report-section[data-report-section="exposure"]',
        '.pdf-report-top-companies-title',
        '.pdf-report-pairwise-title',
        '.pdf-report-company-panel--continued',
      ],
      avoid: ['.pdf-report-section-title', '.pdf-report-chart', '.pdf-report-table tr', '.pdf-report-heatmap tr'],
    },
  };
}

export async function generateReportPdf({
  root,
  snapshot,
  t,
  formatTimestamp,
  html2pdf = globalThis.html2pdf,
} = {}) {
  if (typeof html2pdf !== 'function') {
    throw new Error('The local PDF generator is unavailable.');
  }
  if (globalThis.document?.fonts?.ready) {
    await globalThis.document.fonts.ready;
  }

  const options = createReportPdfOptions(snapshot);
  const worker = html2pdf().set(options).from(root).toPdf().get('pdf');
  return worker
    .then((pdf) => stampReportPdf(pdf, { snapshot, t, formatTimestamp }))
    .save(options.filename);
}