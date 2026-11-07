const jsPDFConstructor = globalThis.jspdf?.jsPDF;
const autoTable = globalThis.autoTable;
const applyPlugin = globalThis.applyPlugin;

if (
  typeof jsPDFConstructor === 'function'
  && typeof autoTable === 'function'
  && typeof applyPlugin === 'function'
  && !jsPDFConstructor.API.autoTable
) {
  applyPlugin(jsPDFConstructor);
}

export { autoTable, jsPDFConstructor };
