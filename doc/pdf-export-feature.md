[[ETF Portfolio Lens]], [[ETF Website Features]]

To add a client-side PDF export feature to the **ETF Portfolio Lens** application—specifically separating holdings and analysis plots across multiple pages—the best JavaScript framework for the job is `**html2pdf.js**` (which combines `**jsPDF**` and `**html2canvas**` under the hood).

### Why `html2pdf.js` is the Best Choice for This Project

1. **Flawless Handling of Complex Charts/Plots:** The "compare" and "explore" tabs contain canvas- or SVG-based charts. Pure text-and-vector PDF libraries (like raw jsPDF) struggle to parse complex CSS layouts and charts, often resulting in blank spaces or broken graphics. `html2canvas` captures these charts exactly as they appear on the screen.
2. **Built-in Multi-Page & Page-Break Support:** It natively supports CSS page-break rules (`page-break-before`, `break-inside: avoid`, etc.), making it easy to force your analysis plots onto a fresh page separate from the holdings.
3. **Zero Backend Required:** Since the ETF Portfolio Lens is a static client-side web application hosted on GitHub Pages, `html2pdf.js` runs entirely within the user's browser without needing a server-side PDF generation backend.

### Implementation Guide

#### 1. Include the Library

You can load `html2pdf.js` via CDN directly into your HTML file:

<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>

#### 2. Structure Your HTML Layout for Export

To control what goes on Page 1 (holdings) versus Page 2 (plots), wrap your sections with specific classes or IDs, applying a CSS page break between them.

<div id="pdf-export-container">
  <!-- PAGE 1: Holdings -->
  <div class="pdf-page">
    <h2>Portfolio Holdings</h2>
    <!-- Insert your holdings table/element here -->
    <div id="holdings-content">...</div>
  </div>

  {/* Force a page break */}
  <div style="page-break-before: always;"></div>

  <!-- PAGE 2: Analysis Plots -->
  <div class="pdf-page">
    <h2>Portfolio Analysis & Plots</h2>
    <!-- Insert your compare and explore charts container here -->
    <div id="plots-content">...</div>
  </div>
</div>

#### 3. Trigger the PDF Generation via JavaScript

Add a button to your user interface (`<button id="export-btn">Export PDF</button>`) and bind the export logic:

document.getElementById('export-btn').addEventListener('click', () => {
  const element = document.getElementById('pdf-export-container');
  
  const options = {
    margin:       10, // mm
    filename:     'etf-portfolio-report.pdf',
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { 
      scale: 2,         // Increases clarity/resolution of charts
      useCORS: true     // Handles cross-origin icons/assets if any
    },
    jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' },
    pagebreak:    { mode: ['css', 'legacy'] } // Respects page-break-before: always
  };

  // Generate and download the PDF
  html2pdf().from(element).set(options).save();
});

### Alternative Consideration

- If your application is built heavily within a framework like **React** or **Vue**, you can look at `react-to-print` or framework-specific wrappers, but standard `html2pdf.js` remains the most lightweight and straightforward drop-in solution for vanilla JavaScript or bundled SPAs.