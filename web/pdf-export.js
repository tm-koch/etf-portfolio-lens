import { renderReportDocument } from './pdf-report-renderer.js';
import { autoTable as bundledAutoTable, jsPDFConstructor as bundledJsPDF } from './pdf-vendor.js';

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
    pdf.setFont('SpaceGrotesk', 'normal');
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
    filename: `etf-portfolio-lens-report-${filenameDate}.pdf`,
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'landscape', compress: true },
  };
}

async function addReportFonts(pdf, fetchImpl) {
  const fontFaces = [
    ['space-grotesk-400.ttf', 'normal'],
    ['space-grotesk-500.ttf', 'medium'],
    ['space-grotesk-700.ttf', 'bold'],
  ];
  for (const [filename, style] of fontFaces) {
    const response = await fetchImpl(new URL(`./fonts/${filename}`, import.meta.url));
    if (!response.ok) throw new Error(`Could not load the local report font: ${filename}`);
    const bytes = new Uint8Array(await response.arrayBuffer());
    let binary = '';
    for (let offset = 0; offset < bytes.length; offset += 0x8000) {
      binary += String.fromCharCode(...bytes.subarray(offset, offset + 0x8000));
    }
    pdf.addFileToVFS(filename, globalThis.btoa(binary));
    pdf.addFont(filename, 'SpaceGrotesk', style, 'Identity-H');
  }
}

export async function generateReportPdf({
  snapshot,
  analytics,
  allocationOnly = false,
  t,
  formatCount,
  formatDecimal,
  formatPercent,
  formatCurrency,
  formatTimestamp,
  translateTaxonomy,
  jsPDFConstructor = bundledJsPDF,
  autoTable = bundledAutoTable,
  fetchImpl = globalThis.fetch?.bind(globalThis),
} = {}) {
  if (typeof jsPDFConstructor !== 'function' || typeof autoTable !== 'function' || typeof fetchImpl !== 'function') {
    throw new Error('The local PDF generator is unavailable.');
  }
  const options = createReportPdfOptions(snapshot);
  const pdf = new jsPDFConstructor(options.jsPDF);
  await addReportFonts(pdf, fetchImpl);
  renderReportDocument({
    pdf,
    autoTable,
    snapshot,
    analytics,
    allocationOnly,
    t,
    formatCount,
    formatDecimal,
    formatPercent,
    formatCurrency,
    translateTaxonomy,
  });
  stampReportPdf(pdf, { snapshot, t, formatTimestamp });
  pdf.save(options.filename);
  return options.filename;
}
