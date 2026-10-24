# Spec Delta

## ADDED Requirements

### Requirement: Name the Saxo report in the import instruction
The Saxo PDF file-drop instruction SHALL identify the expected document as a transaction and balance report using the selected interface language.

#### Scenario: English import instruction
- **WHEN** the interface language is English (`en-CH`)
- **THEN** the instruction reads `Drop a transaction and balance report here or choose a PDF.`

#### Scenario: German import instruction
- **WHEN** the interface language is German (`de-CH`)
- **THEN** the instruction reads `Ziehen Sie hier einen Transaktions- und Saldobericht hinein oder wählen Sie eine PDF-Datei aus.`

#### Scenario: Polish import instruction
- **WHEN** the interface language is Polish (`pl-PL`)
- **THEN** the instruction reads `Upuść tutaj raport transakcji i sald lub wybierz plik PDF.`