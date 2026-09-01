const SAXO_MARKERS = ['saxo bank', 'transaktions und saldenbericht'];
const SAXO_HOLDINGS_MARKER = 'bestande';
const ISIN_PATTERN = /\b[A-Z]{2}[A-Z0-9]{9}\d\b/g;
const SUPPORTED_CURRENCIES = new Set(['CHF', 'EUR']);
const EUR_TO_CHF_RATE = 1;

export function normalizeIsin(value) {
  return String(value || '').replace(/\s+/g, '').toUpperCase();
}

function normalizeSearchText(value) {
  return String(value || '')
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[\u00ad\u200b\u200c\u200d\ufeff]/g, '')
    .toLowerCase()
    .replace(/[-\u2010-\u2015]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

export function parseGermanNumber(value) {
  const normalizedValue = String(value || '').replace(/\s/g, '');
  const normalized = normalizedValue.includes(',')
    ? normalizedValue.replace(/\./g, '').replace(',', '.')
    : /\.\d{1,2}$/.test(normalizedValue) || /\.\d{4,}$/.test(normalizedValue)
      ? normalizedValue
      : normalizedValue.replace(/\./g, '');
  const parsed = Number(normalized);
  return Number.isFinite(parsed) ? parsed : null;
}

export function calculateImportedPosition(shares, price, currency) {
  const value = shares * price;
  return {
    value,
    valueChf: currency === 'EUR' ? value * EUR_TO_CHF_RATE : value,
  };
}

function normalizePageText(items) {
  const positionedItems = items
    .filter((item) => item.str?.trim())
    .map((item) => ({
      text: item.str.trim(),
      x: item.transform?.[4] ?? 0,
      y: item.transform?.[5] ?? 0,
    }));
  if (!positionedItems.some((item) => item.y)) {
    return items.map((item) => item.str).join(' ').replace(/\s+/g, ' ').trim();
  }

  const lines = [];
  for (const item of positionedItems) {
    const line = lines.find((candidate) => Math.abs(candidate.y - item.y) <= 2);
    if (line) line.items.push(item);
    else lines.push({ y: item.y, items: [item] });
  }
  return lines
    .sort((left, right) => right.y - left.y)
    .map((line) => line.items
      .sort((left, right) => left.x - right.x)
      .map((item) => item.text)
      .join(' '))
    .join('\n')
    .replace(/[ \t\f\r]+/g, ' ')
    .trim();
}

function findCurrency(text) {
  const match = text.match(/\b(CHF|EUR)\b/);
  return match?.[1] || null;
}

function parseSaxoNumericColumns(text) {
  const normalizedText = text
    .replace(/(\d{1,2})\s*([-.\/])\s*/g, '$1$2')
    .replace(/\s+([,.])\s+/g, '$1')
    .replace(/([,.])\s+/g, '$1')
    .replace(/\s+([,.])/g, '$1');
  const dateMatch = normalizedText.match(/\b\d{1,2}\s*[-./]\s*(?:[A-Za-zÄÖÜäöü]{3,}|\d{1,2})(?:\s*[-./]\s*|\s+)\d{2,4}\b/i);
  if (!dateMatch) return null;
  const tail = normalizedText.slice(dateMatch.index + dateMatch[0].length);
  const columns = [...tail.matchAll(/\b\d[\d.,]*\b/g)].map((entry) => entry[0]);
  if (columns.length < 7 || parseGermanNumber(columns[1]) !== 1) return null;
  return {
    shares: parseGermanNumber(columns[0]),
    price: parseGermanNumber(columns[3]),
    marketValue: parseGermanNumber(columns[6]),
  };
}

function extractHoldingRows(text, pageNumber) {
  const sectionStart = text.search(/Börsengehandelte Produkte\s*\(ETF,\s*ETC,\s*ETN\)/i);
  const sectionText = sectionStart >= 0 ? text.slice(sectionStart) : text;
  const sectionEnd = sectionText.search(/\nGesamt\b/i);
  const holdingsText = sectionEnd >= 0 ? sectionText.slice(0, sectionEnd) : sectionText;
  const isinMatches = [...holdingsText.matchAll(ISIN_PATTERN)];
  const numericRows = [...holdingsText.matchAll(/\b\d{1,2}\s*[-./]\s*[A-Za-zÄÖÜäöü]{3,}\s*[-./]\s*\d{2,4}\b/gi)]
    .map((match, index, matches) => {
      const end = matches[index + 1]?.index ?? holdingsText.length;
      return parseSaxoNumericColumns(holdingsText.slice(match.index, end));
    })
    .filter(Boolean);
  const sectionCurrency = holdingsText.match(/Bestände[^\n]*\b(CHF|EUR)\b/i)?.[1]?.toUpperCase() || null;
  const rows = [];
  for (const [index, match] of isinMatches.entries()) {
    const isin = normalizeIsin(match[0]);
    const end = isinMatches[index + 1]?.index ?? holdingsText.length;
    const context = holdingsText.slice(Math.max(0, match.index - 180), end);
    const rowMatch = context.match(
      /(?:[A-Z0-9]+:[a-z]+)\s+\d+\s+(CHF|EUR)\s+\d{1,2}-[A-Za-z]{3}-\d{4}\s+([\d.,]+)\s+1[,.]0000\s+([\d.,]+)\s+([\d.,]+)\s+[\d.,]+\s*%\s+([\d.,]+)\s+([\d.,]+)/i
    );
    const numericColumns = numericRows[index] || null;
    const parsedColumns = numericColumns || parseSaxoNumericColumns(context);
    const currency = rowMatch?.[1] || sectionCurrency || findCurrency(context);
    const shares = parsedColumns?.shares ?? (rowMatch ? parseGermanNumber(rowMatch[2]) : null);
    const price = parsedColumns?.price ?? (rowMatch ? parseGermanNumber(rowMatch[4]) : null);
    const marketValue = parsedColumns?.marketValue ?? (rowMatch ? parseGermanNumber(rowMatch[6]) : null);
    const derived = shares !== null && price !== null && currency
      ? calculateImportedPosition(shares, price, currency)
      : { value: marketValue, valueChf: currency === 'EUR' && marketValue !== null ? marketValue * EUR_TO_CHF_RATE : marketValue };
    rows.push({
      isin,
      shares,
      price,
      currency,
      value: derived.value,
      valueChf: derived.valueChf,
      pageNumber,
      sourceText: context.trim(),
      warnings: [],
    });
  }
  return rows;
}

export function validateImportedRow(row) {
  const warnings = [];
  if (!/^[A-Z]{2}[A-Z0-9]{9}\d$/.test(row.isin)) warnings.push('Invalid ISIN');
  if (!Number.isFinite(row.shares) || row.shares < 0) warnings.push('Shares are missing or invalid');
  if (!Number.isFinite(row.price) || row.price < 0) warnings.push('Price is missing or invalid');
  if (!SUPPORTED_CURRENCIES.has(row.currency)) warnings.push('Currency is missing or unsupported');
  return { ...row, warnings };
}

export function parseSaxoPages(pages) {
  const fullText = pages.map((page) => page.text).join(' ');
  const normalizedFullText = normalizeSearchText(fullText);
  if (!SAXO_MARKERS.every((marker) => normalizedFullText.includes(marker))) {
    throw new Error('This PDF is not a supported Saxo Bank report.');
  }
  const holdingsPages = pages.filter((page) => normalizeSearchText(page.text).includes(SAXO_HOLDINGS_MARKER));
  if (!holdingsPages.length) {
    throw new Error('No Saxo holdings pages were found in this PDF.');
  }
  const rows = holdingsPages.flatMap((page) => extractHoldingRows(page.text, page.pageNumber));
  const seen = new Set();
  return rows.map((row) => {
    const validated = validateImportedRow(row);
    if (seen.has(validated.isin)) validated.warnings = [...validated.warnings, 'Duplicate ISIN'];
    seen.add(validated.isin);
    return validated;
  });
}

export async function extractPdfPages(file, pdfjs = window.pdfjsLib) {
  if (!pdfjs) throw new Error('PDF.js is unavailable. Reload the page and try again.');
  pdfjs.GlobalWorkerOptions.workerSrc = new URL('./vendor/pdf.worker.min.js', import.meta.url).href;
  const document = await pdfjs.getDocument({ data: await file.arrayBuffer() }).promise;
  const pages = [];
  for (let pageNumber = 1; pageNumber <= document.numPages; pageNumber += 1) {
    const page = await document.getPage(pageNumber);
    const content = await page.getTextContent();
    pages.push({ pageNumber, text: normalizePageText(content.items) });
  }
  return pages;
}

export function matchImportedRows(rows, catalogMaps) {
  return rows.map((row) => {
    const entry = catalogMaps.byIsin.get(row.isin);
    return {
      ...row,
      entry,
      matchStatus: entry ? 'matched' : 'unmatched',
      included: Boolean(entry && !row.warnings.length),
    };
  });
}
