const TAXONOMY_LABEL_KEYS = new Map([
  ['Asia', 'taxonomy.region.asia'],
  ['Europe', 'taxonomy.region.europe'],
  ['North America', 'taxonomy.region.northAmerica'],
  ['Cash and/or Derivatives', 'taxonomy.sector.cashDerivatives'],
  ['Communication Services', 'taxonomy.sector.communicationServices'],
  ['Consumer Discretionary', 'taxonomy.sector.consumerDiscretionary'],
  ['Consumer Staples', 'taxonomy.sector.consumerStaples'],
  ['Energy', 'taxonomy.sector.energy'],
  ['Financials', 'taxonomy.sector.financials'],
  ['Health Care', 'taxonomy.sector.healthCare'],
  ['Industrials', 'taxonomy.sector.industrials'],
  ['Information Technology', 'taxonomy.sector.informationTechnology'],
  ['Materials', 'taxonomy.sector.materials'],
  ['Real Estate', 'taxonomy.sector.realEstate'],
  ['Utilities', 'taxonomy.sector.utilities'],
  ['Unknown', 'taxonomy.unknown'],
  ['Other', 'taxonomy.other'],
]);

export function translateTaxonomyLabel(label, translate) {
  const key = TAXONOMY_LABEL_KEYS.get(String(label).trim());
  return key ? translate(key) : label;
}
