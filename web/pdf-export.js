import { renderReportDocument } from './pdf-report-renderer.js';
import { autoTable as bundledAutoTable, jsPDFConstructor as bundledJsPDF } from './pdf-vendor.js';

export const REPORT_WEBSITE_URL = 'https://tm-koch.github.io/etf-portfolio-lens/';

export function stampReportPdf(pdf, { snapshot, t, formatTimestamp }) {
  const pageCount = pdf.internal.getNumberOfPages();
  const pageHeight = pdf.internal.pageSize.getHeight();
  const pageWidth = pdf.internal.pageSize.getWidth();
  const left = 8;
  const right = pageWidth - 8;
  const websiteLabel = 'ETF Portfolio Lens';
  const websiteLabelWidth = pdf.getTextWidth(websiteLabel);
  const footerText = `ETF Portfolio Lens | Generated: ${formatTimestamp(snapshot.generatedAt)}`;
  const footerY = pageHeight - 8;

  pdf.setProperties({
    title: 'ETF Portfolio Lens report',
    subject: 'ETF portfolio and exposure report',
    creator: 'ETF Portfolio Lens',
  });
  for (let page = 1; page <= pageCount; page += 1) {
    pdf.setPage(page);
    pdf.setFont('SpaceGrotesk', 'normal');
    pdf.setFontSize(7.5);
    pdf.setTextColor(71, 85, 105);
    pdf.text(footerText, left, footerY);
    pdf.text(t('export.page', { page, total: pageCount }), right, footerY, { align: 'right' });
    pdf.link(left, footerY - 3, websiteLabelWidth, 4, { url: REPORT_WEBSITE_URL });
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

async function loadReportCoverIcon(fetchImpl) {
  const filename = 'launchericon-512x512.png';
  const response = await fetchImpl(new URL(`./icons/${filename}`, import.meta.url));
  if (!response.ok) throw new Error(`Could not load the local report icon: ${filename}`);
  const bytes = new Uint8Array(await response.arrayBuffer());
  let binary = '';
  for (let offset = 0; offset < bytes.length; offset += 0x8000) {
    binary += String.fromCharCode(...bytes.subarray(offset, offset + 0x8000));
  }
  return `data:image/png;base64,${globalThis.btoa(binary)}`;
}

export async function generateReportPdf({
  snapshot,
  analytics,
  portfolioShareUrl = null,
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
  const coverIcon = await loadReportCoverIcon(fetchImpl);
  renderReportDocument({
    pdf,
    autoTable,
    snapshot,
    analytics,
    portfolioShareUrl,
    coverIcon,
    allocationOnly,
    t,
    formatCount,
    formatDecimal,
    formatPercent,
    formatCurrency,
    formatTimestamp,
    translateTaxonomy,
  });
  stampReportPdf(pdf, { snapshot, t, formatTimestamp });
  pdf.save(options.filename);
  return options.filename;
}
