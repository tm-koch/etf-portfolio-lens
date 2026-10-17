function pairKey(isinA, isinB) {
  return [isinA, isinB].sort().join('\u0000');
}

export function buildPairwiseOverlapIndex(pairwiseOverlap) {
  const index = new Map();
  if (pairwiseOverlap?.version !== 1 || !Array.isArray(pairwiseOverlap.pairs)) {
    return index;
  }

  for (const pair of pairwiseOverlap.pairs) {
    if (
      typeof pair?.isinA !== 'string'
      || !pair.isinA
      || typeof pair.isinB !== 'string'
      || !pair.isinB
      || pair.isinA === pair.isinB
      || typeof pair.available !== 'boolean'
    ) {
      continue;
    }
    if (
      pair.available
      && (!Number.isFinite(pair.overlapPct) || pair.overlapPct < 0 || pair.overlapPct > 100)
    ) {
      continue;
    }
    index.set(pairKey(pair.isinA, pair.isinB), pair);
  }
  return index;
}

export function getPairwiseOverlap(index, isinA, isinB) {
  if (!index || !isinA || !isinB || isinA === isinB) return null;
  return index.get(pairKey(isinA, isinB)) || null;
}

export function buildPairwiseMatrix(positions, index, threshold) {
  return positions.map((position, rowIndex) => ({
    product: {
      isin: position.isin,
      ticker: position.entry.ticker,
      name: position.entry.name,
    },
    cells: positions.map((other, columnIndex) => {
      if (columnIndex === rowIndex) return { type: 'diagonal' };
      if (columnIndex > rowIndex) return { type: 'empty' };

      const pair = getPairwiseOverlap(index, position.isin, other.isin);
      if (!pair || !pair.available || !Number.isFinite(pair.overlapPct)) {
        return { type: 'unavailable', pair };
      }
      return {
        type: 'overlap',
        overlapPct: pair.overlapPct,
        coveragePctA: pair.coveragePctA,
        coveragePctB: pair.coveragePctB,
        nearIdentical: pair.overlapPct >= threshold,
      };
    }),
  }));
}

export function findNearIdenticalPairs(positions, index, threshold) {
  return buildPairwiseMatrix(positions, index, threshold).flatMap((row, rowIndex) =>
    row.cells.flatMap((cell, columnIndex) => {
      if (cell.type !== 'overlap' || !cell.nearIdentical) return [];
      const other = positions[columnIndex];
      return [{
        productA: row.product,
        productB: {
          isin: other.isin,
          ticker: other.entry.ticker,
          name: other.entry.name,
        },
        overlapPct: cell.overlapPct,
      }];
    })
  );
}
