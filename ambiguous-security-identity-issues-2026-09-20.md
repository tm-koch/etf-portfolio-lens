# Security identity review queue

Generated from:

```text
python -m etf_ingestion_backend --all --fixtures --update-catalog
```

Run date: 2026-09-20

The latest fixture run produced 6,262 matched, 646 overridden, 264 ISIN-only, 62 ambiguous, and 35 excluded holdings. The remaining warning output contains 37 unique ticker/context conflicts and 39 unique missing-ISIN identifiers. Some warnings repeat because the same holding appears in more than one ETF fixture.

## 1. Ambiguous exact-name matches

The security master has two records for each name. A name-only override is unsafe because the candidates have different listings and, in several cases, different ISINs.

| Provider name | Candidate 1 | Candidate 2 | Open question |
| --- | --- | --- | --- |
| `AVIVA PLC` | selected `AV` / LSE / `GB00BPQY8M80` | `AIVAF` / OTC / `GB0002162385` | Resolved to the LSE ordinary listing. |
| `TELECOM ITALIA` | `TQI` / Xetra / `IT0003497168` | selected `0H6I` / LSE / `IT0005712671` | Resolved to the LSE listing. |
| `AEROPORTS DE PARIS SA` | selected `0NP8` / LSE / `FR0010340141` | `ARRPY` / OTC / `US00786A1079` | Resolved to the ordinary French security. |
| `QIAGEN NV` | `QGEN` / NYSE / `NL0015002CX3` | selected `0RLT` / LSE / `NL0015002SN0` | Resolved previously as Qiagen NV from the Xetra provider rows. |

Source context observed in the ambiguous rows:

- `AVIVA PLC`: provider name only in the affected row; resolved by review to `GB00BPQY8M80`.
- `TELECOM ITALIA`: ticker `TIT`, Italy, Borsa Italiana; resolved by review to `IT0005712671`.
- `AEROPORTS DE PARIS SA`: provider name only in the affected row; resolved by review to `FR0010340141`.
- `QIAGEN NV`: resolved previously as `NL0015002SN0` from the Xetra provider rows.

## 2. Ticker conflicts with provider context

These rows have a ticker present in the security master, but the candidate ticker records do not agree with the provider exchange/country context. The matcher deliberately leaves them ambiguous rather than selecting a possibly wrong company or listing.

| Provider context | Tickers |
| --- | --- |
| London Stock Exchange / United Kingdom | `ADM`, `CNA`, `EDV`, `LAND`, `NXT`, `WISE` |
| Euronext Amsterdam / Netherlands | `AGN`, `CVC`, `NN` |
| Nasdaq OMX Nordic / Sweden | `ALFA`, `BOL`, `EVO` |
| Euronext Paris / France | `AMUN`, `CA`, `LI`, `RXL`, `SW` |
| Euronext Lisbon / Portugal | `BCP`, `BES`, `JMT` |
| Xetra / Germany | `BNR`, `CON`, `MTX`, `NEM`, `RAA` |
| Borsa Italiana / Italy | `CPR`, `FBK`, `REC`, `SRG`, `UNI` |
| Euronext Brussels / Belgium | `DIE`, `SOF` |
| Bolsa de Madrid / Spain | `IAG`, `IDR`, `REP` |
| Oslo Bors / Norway | `SALM`, `TEL` |

Open question for this group: for each ticker, which exact ISIN should be assigned to the provider row, and is the provider's exchange/country context authoritative, or is the security-master listing context the intended one? An ISIN or provider-native security identifier is the preferred answer; a ticker-only answer is not sufficient where the ticker is reused across listings.

## 3. Missing source ISINs

These rows have no source ISIN. They are currently `unmatched`; the system should not infer an identity from ticker alone where the ticker is absent, reused, malformed, or context-dependent.

| Provider identifier | Fixture occurrence |
| --- | ---: |
| `ACS.D` | 1 |
| `ADDT B` | 1 |
| `AGS` | 2 |
| `BALD B` | 1 |
| `BEIJ B` | 1 |
| `CARL B` | 1 |
| `COLO B` | 1 |
| `DSFIR` | 2 |
| `EDPR` | 2 |
| `ELI` | 2 |
| `ENX` | 2 |
| `ESSITY B` | 1 |
| `GALP` | 2 |
| `GBLB` | 2 |
| `ICSEAGD` | 2 |
| `ICSSAGD` | 1 |
| `INDU A` | 1 |
| `INDU C` | 1 |
| `INPST` | 2 |
| `LATO B` | 1 |
| `LDO` | 2 |
| `LIFCO B` | 1 |
| `LUND B` | 1 |
| `NIBE B` | 1 |
| `OCTV SDB` | 1 |
| `OMV` | 2 |
| `QIA` | 1 |
| `ROCK B` | 1 |
| `SAAB B` | 1 |
| `SAGA B` | 1 |
| `SCA B` | 1 |
| `SECU B` | 1 |
| `SKA B` | 1 |
| `SKF B` | 1 |
| `SN.` | 1 |
| `SYENS` | 2 |
| `TEL2 B` | 1 |
| `TREL B` | 1 |

### External resolutions

The following mappings were supplied for the missing-ISIN review. Provider exchange/country is retained as context, while the ISIN is the authoritative identity key.

| Provider identifier | Provider exchange/country | ISIN | Canonical company name | Notes |
| --- | --- | --- | --- | --- |
| `ACS.D` | Spain (BME) | `ES0167050915` | ACS, Actividades de Construcción y Servicios, S.A. | `.D` may denote provider-specific rights/dividend-line handling; map to the underlying ordinary share. |
| `ADDT B` | Nasdaq Stockholm (Sweden) | `SE0014781795` | Addtech AB (publ), Class B | Swedish Class B share. |
| `BALD B` | Nasdaq Stockholm (Sweden) | `SE0017832488` | Fastighets AB Balder, Class B | Swedish Class B share. |
| `BEIJ B` | Nasdaq Stockholm (Sweden) | `SE0015949748` | Beijer Ref AB, Class B | Swedish Class B share. |
| `CARL B` | Nasdaq Copenhagen (Denmark) | `DK0010181759` | Carlsberg A/S, Class B | Danish Class B share. |
| `COLO B` | Nasdaq Copenhagen (Denmark) | `DK0060448595` | Coloplast A/S, Class B | Danish Class B share. |
| `EDPR` | Euronext Lisbon (Portugal) | `ES0127797019` | EDP Renováveis, S.A. | Ordinary equity; confirm if the provider uses another listing. |
| `ELI` | Euronext Brussels (Belgium) | `BE0003845626` | Elia Group SA/NV | Ordinary equity. |
| `ENX` | Euronext Paris (France) | `NL0006294274` | Euronext N.V. | Ordinary equity. |
| `ESSITY B` | Sweden | `SE0009922164` | Essity AB, Class B | Class B share. |
| `GALP` | Euronext Lisbon (Portugal) | `PTGAL0AM0009` | Galp Energia, SGPS, S.A. | Ordinary equity. |
| `GBLB` | Euronext Brussels (Belgium) | `BE0003797140` | Groupe Bruxelles Lambert SA | Holding company. |
| `INDU A` | Sweden | `SE0000107203` | Industrivärden, Class A | User-provided `INDU Aa/C` mapping interpreted as the A share. |
| `INDU C` | Sweden | `SE0000190126` | Industrivärden, Class C | User-provided `INDU Aa/C` mapping interpreted as the C share. |
| `LDO` | Borsa Italiana (Italy) | `IT0003856405` | Leonardo S.p.A. | Ordinary equity. |
| `LATO B` | Sweden | `SE0010100958` | Latour AB, Class B | Class B share. |
| `LIFCO B` | Sweden | `SE0015949201` | Lifco AB, Class B | Class B share. |
| `LUND B` | Sweden | `SE0000108847` | Lundbergföretagen, Class B | Class B share. |
| `NIBE B` | Sweden | `SE0015988019` | NIBE Industrier AB, Class B | Class B share. |
| `OMV` | Vienna Stock Exchange (Austria) | `AT0000743059` | OMV AG | Ordinary equity. |
| `ROCK B` | Denmark | `DK0010219153` | Rockwool A/S, Class B | Class B share. |
| `SAAB B` | Sweden | `SE0021921269` | Saab AB, Class B | Class B share. |
| `SAGA B` | Sweden | `SE0015193875` | Sagax AB, Class B | Class B share. |
| `SCA B` | Sweden | `SE0000112724` | Svenska Cellulosa AB SCA, Class B | Class B share. |
| `SECU B` | Sweden | `SE0000163594` | Securitas AB, Class B | Class B share. |
| `SKA B` | Sweden | `SE0000113250` | Skanska AB, Class B | Class B share. |
| `SKF B` | Sweden | `SE0000108227` | AB SKF, Class B | Class B share. |
| `SYENS` | Euronext Brussels (Belgium) | `BE0974464977` | Syensqo SA | Spin-off from Solvay; ordinary equity. |
| `TEL2 B` | Sweden | `SE0005190238` | Tele2 AB, Class B | Class B share. |
| `TREL B` | Sweden | `SE0000114837` | Trelleborg AB, Class B | Class B share. |

### Special handling and remaining questions

| Provider identifier | Decision or open question |
| --- | --- |
| `ICSEAGD` | Exclude from company identity; BlackRock ICS Euro Liquidity Fund. |
| `ICSSAGD` | Exclude from company identity; BlackRock ICS Sterling Liquidity Fund. |
| `AGS` | ISIN supplied: `BE0974264930`; canonical name and provider exchange/country still need confirmation. |
| `DSFIR` | ISIN supplied: `CH1216478797`; identity is DSM-Firmenich. Provider listing context still needs confirmation. |
| `INPST` | ISIN supplied: `LU2290522684`; canonical name and provider exchange/country still need confirmation. |
| `OCTV SDB` | ISIN supplied: `SE0028329433`; identity is Octave Intelligence plc. The meaning of `SDB` still needs confirmation. |
| `QIA` | Resolved as Qiagen NV with ISIN `NL0015002SN0`; preserve provider context `Deutsche Börse Xetra / Germany`. The security master labels this ISIN as LSE, so retain that venue-label discrepancy in provenance. |
| `SN.` | ISIN supplied: `GB0009223206`; canonical name and provider exchange/country still need confirmation. |

The supplied information provides ISINs for all six remaining identifiers. `QIA` is resolved as Qiagen NV; `QA0006929895` remains the separate Qatar Islamic Bank identity and must not be assigned to the `QIA` provider rows.

## Review response format

The smallest useful response is a mapping with one row per issue, for example:

```text
provider name or ticker | provider exchange/country | ISIN | canonical company name | notes
```

For the four exact-name collisions, selecting one candidate ISIN is enough to resolve the identity decision. For the ticker-conflict and missing-ISIN groups, a batch mapping is preferable.

## Related generated artifacts

- Latest normalized snapshots: `data/raw/2026-09-20/snapshots/`
- Raw warning capture from the run: `ingestion-warning-run.txt` (temporary, not part of the review report)
