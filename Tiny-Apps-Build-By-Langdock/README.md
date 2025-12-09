# Tiny Apps Built by Langdock

These single-file HTML applications were **fully built by Claude Opus in the Langdock Chat**. No coding required — just describe what you need and Langdock creates it for you.

## How to Use

1. **Download** any `.html` file from this folder
2. **Open** the file directly in your web browser (double-click or drag into browser)
3. **Done!** The app runs immediately — no installation, no server, no setup

## Privacy & Security

**Your files never leave your device.** All processing happens directly in your browser using JavaScript. No data is uploaded to any server. You can verify this by:

- Disconnecting from the internet after loading the page — the apps still work
- Inspecting the code yourself (right-click → View Source)
- Checking the Network tab in browser DevTools — no file data is transmitted

---

## Available Apps

### 📄 Compress PDF (`Compress_PDFs.html`)

Reduces PDF file size while maintaining quality.

**How it works:**
- Drag & drop or click to upload a PDF file
- Choose a compression level (Low/Medium/High) and image quality percentage
- The app reads each page of your PDF, renders it as an image at the selected quality, and rebuilds a new smaller PDF
- Download your compressed file

**Technical details:** Uses [pdf.js](https://mozilla.github.io/pdf.js/) to read the PDF and [jsPDF](https://github.com/parallax/jsPDF) to create the compressed output. Pages are converted to JPEG images at your chosen quality level.

---

### 🔄 Convert Files (`Convert_File.html`)

Converts images and documents between different formats.

**Supported conversions:**
| From | To |
|------|-----|
| PNG | JPG, PDF, WEBP |
| JPG | PNG, PDF, WEBP |
| WEBP | PNG, JPG, PDF |
| GIF | PNG, JPG |
| BMP | PNG, JPG, PDF |
| SVG | PNG, JPG |
| PDF | JPG, PNG (each page becomes a separate image) |

**How it works:**
- Drop one or more files of the same type
- Select your target format from the dropdown
- Click "Convert" — each file is processed and a download button appears
- For PDFs with multiple pages, each page is exported as a separate image

**Technical details:** Uses HTML Canvas API for image-to-image conversions (the file is drawn onto an invisible canvas, then exported in the new format). PDF operations use pdf.js and jsPDF.

---

### 📑 Merge PDF (`Merge_PDF.html`)

Combines multiple PDF files into a single document.

**How it works:**
- Drop or select multiple PDF files
- Drag the files in the list to reorder them (the numbered badges show the merge order)
- Click "Merge PDFs"
- Download your combined document

**Technical details:** Each page from every PDF is rendered at high resolution, then assembled into a new PDF in your specified order. Page counts are shown for each file so you know exactly what you're merging.

---

### ✂️ Split PDF (`Split_PDF.html`)

Extract specific pages from a PDF with visual page selection.

**How it works:**
- Upload a PDF file
- See thumbnail previews of every page
- Click pages to select/deselect them (blue highlight = selected)
- Use "Select All", "Clear", or "Invert" buttons for quick selection
- Click "Extract Selected Pages" to create a new PDF with only your chosen pages

**Technical details:** Generates thumbnail previews at 50% scale for fast loading, then renders selected pages at full quality for the output PDF.

---

## Libraries Used

All apps load these open-source libraries from CDN (content delivery network):

- **[pdf.js](https://mozilla.github.io/pdf.js/)** — Mozilla's PDF rendering library (reads PDF files)
- **[jsPDF](https://github.com/parallax/jsPDF)** — Creates PDF files from JavaScript
- **[JSZip](https://stuk.github.io/jszip/)** — Used in Split PDF for handling zip operations

The libraries are loaded when you open the HTML file, so you need an internet connection the first time. After that, your browser may cache them.

---

## Customize These Apps with Langdock

Want to modify these apps or add new features? It's easy with Langdock:

### How to Modify an App

1. **Upload** the HTML file to a Langdock chat
2. **Describe** what you want to change in plain language
3. **Download** the modified file Langdock creates

### Example Requests

- *"Add a dark/light theme toggle button"*
- *"Change the accent color from purple to blue"*
- *"Add a feature to rotate pages 90 degrees before merging"*
- *"Make it show file size in KB instead of MB for small files"*
- *"Add the ability to password-protect the output PDF"*
- *"Combine the merge and split tools into one app"*

Langdock understands the code structure and can make targeted changes while keeping everything else working.

---

## Create Your Own Apps

You can create entirely new tools by describing them to Langdock:

- *"Build me a tool that converts CSV files to JSON"*
- *"Create an app that resizes images to specific dimensions"*
- *"Make a QR code generator that works offline"*
- *"Build a markdown editor with live preview"*

The resulting HTML files work the same way — download and open in any browser.

---

## License

These apps are provided as examples. Feel free to use, modify, and distribute them.



