# Design

## Context

The ingestion pipeline already applies version-controlled identity overrides before serializing normalized holdings. An override can match an exact ISIN and set `company_id` and `canonical_name`; snapshots retain provider fields separately from normalized security data. See `proposal.md` for motivation.

The checked-in sample snapshots do not contain the target holdings, so their exact provider ISINs must be verified before adding selectors.

## Goals / Non-Goals

**Goals:**

- Normalize both Alphabet share classes to one company identity while retaining distinct instrument identities.
- Display the MediaTek holding as `MediaTek Inc.` while preserving its original provider source fields verbatim in provenance.
- Keep the change within existing override and snapshot behavior, with no source-download edits or new runtime mechanism.

**Non-Goals:**

- Combining the two Alphabet instruments into one holding row or changing their weights.
- Adding a general-purpose display-alias field or changing security-master alias matching.
- Editing historical snapshots or rewriting downloaded provider files.

## Decisions

1. **Use exact-ISIN selectors for all three mappings.** Verify each ISIN against the relevant provider holding row before adding an override. This avoids matching on company-name variants or potentially ambiguous tickers.
2. **Keep Alphabet instruments separate and share only company identity.** Assign both class-specific overrides `company_id: alphabet-inc` and `canonical_name: Alphabet Inc`; preserve each row's ISIN, ticker, and exposure.
3. **Use the existing canonical name for MediaTek display.** The MediaTek override will set `canonical_name: MediaTek Inc.` and the stable `company_id: mediatek-inc`. This uses the existing normalized display path rather than adding an alias output field.
4. **Do not add a spec delta.** Existing `security-identity-enrichment` and `etf-holdings-ingestion` specifications already cover exact overrides, shared company identity across distinct instruments, canonical names, and source-field preservation.

## Risks / Trade-offs

- **The checked-in samples do not show these provider rows** -> Confirm the exact ISINs from the relevant source data before adding mappings; do not fall back to an unverified ticker or name selector.
- **A canonical name may change company-level labels across snapshots** -> Regenerate affected normalized snapshots and verify that only company identity/display fields change while instrument data and provenance remain intact.

## Migration Plan

Add the verified override entries, run focused normalization tests, then regenerate snapshots for affected ETF inputs through the existing ingestion workflow. Roll back by removing the new override entries and regenerating snapshots; downloaded sources and prior dated snapshots remain unchanged.