# Cambridge IGCSE Past Papers Toolkit ```UWC-2025-KD9F7XQ2```

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

A comprehensive Python toolkit for downloading, organizing, validating, and processing Cambridge IGCSE examination papers. Automates the entire workflow from download to final indexed PDFs with page numbers.

## 🎯 Features

- 🔽 **Automated Downloads** - Fetch papers from multiple sources with built-in retry logic and health checks
- ✅ **PDF Validation** - Comprehensive integrity checks including file size, headers, and page count verification
- 🔧 **Corruption Repair** - Fix damaged PDFs using multiple repair strategies (pikepdf + PyPDF2)
- 📑 **Smart Indexing** - Generate detailed indices with automatic page mapping and exam labels
- 🔢 **Page Numbering** - Add centered page numbers to merged documents with configurable settings
- 📊 **Detailed Reporting** - Track success rates, identify issues, and generate comprehensive logs

## 📁 Project Structure

```
cambridge-papers-toolkit/
│
├── download/                           # Paper download scripts
│   ├── download.py                    # Basic downloader for subject 0971
│   ├── download_enhanced.py           # Enhanced with MS/QP organization
│   ├── download_chemistry_0620.py     # Chemistry (0620) specialized downloader
│   └── url_generator.py               # URL generator and CSV exporter
│
├── validation/                         # PDF integrity tools
│   ├── health_checker.py              # Scan and validate PDF files
│   └── pdf_cleaner.py                 # Repair corrupted PDFs
│
├── processing/                         # PDF processing and merging
│   ├── index_builder.py               # Build indices and merge papers
│   ├── index_mixer.py                 # Combine index with content PDFs
│   └── page_numbering.py              # Add page numbers to documents
│
├── requirements.txt                    # Python dependencies
├── .gitignore                         # Git ignore patterns
├── README.md                          # This file
└── PROJECT_STRUCTURE.md               # Detailed documentation
```

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# Install Ghostscript (required for PDF merging)
# Windows: Download from https://www.ghostscript.com/
# Linux: sudo apt-get install ghostscript
# macOS: brew install ghostscript
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cambridge-papers-toolkit.git
cd cambridge-papers-toolkit

# Install Python dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# 1. Download papers (choose one based on your subject)
python download/download_enhanced.py          # For subject 0971
python download/download_chemistry_0620.py    # For Chemistry 0620

# 2. Validate downloads
python validation/health_checker.py

# 3. Repair any damaged files (if needed)
python validation/pdf_cleaner.py

# 4. Build merged PDFs with indices
python processing/index_builder.py

# 5. Combine index with content (optional)
python processing/index_mixer.py

# 6. Add page numbers (optional)
python processing/page_numbering.py
```

## 📖 Detailed Usage

### 1. Downloading Papers

#### Subject 0971 (Computer Science)
```bash
python download/download_enhanced.py
```
- Downloads from papacambridge.com
- Covers 2018-2025 (June and November sessions)
- Organizes into `Year/Season/MS|QP/` structure
- Papers: 21, 22, 41, 42, 61, 62

#### Subject 0620 (Chemistry)
```bash
python download/download_chemistry_0620.py
```
- Downloads from physicsandmathstutor.com
- Includes all paper variants (v1, v2, v3)
- Handles specimen papers automatically
- Papers: 2, 4, 6 (with variants)

**Customization:**
Edit the script to modify:
```python
SUBJECT = "0971"                    # Change subject code
PAPERS = ["21", "22", "41", "42"]  # Select paper numbers
DELAY_BETWEEN_DOWNLOADS = 2         # Adjust rate limiting (seconds)
BASE_URL = "..."                    # Change download source
```

#### Generate URL Lists
```bash
python download/url_generator.py
```
- Creates complete URL lists for batch operations
- Exports to `cambridge_past_papers_urls.csv`
- Useful for external download managers or audit trails

### 2. Validating PDFs

**Run Health Check:**
```bash
python validation/health_checker.py
```

The validator performs:
- ✓ File size verification (rejects files < 1KB)
- ✓ PDF header validation (checks for `%PDF-` signature)
- ✓ Page count analysis
- ✓ Read integrity testing (attempts to read first page)

**Output:**
- Damaged files moved to `DAMAGED_FILES/` directory
- Generates `HEALTH_CHECK_REPORT.txt` with statistics

**Repair Corrupted Files:**
```bash
python validation/pdf_cleaner.py
```

The cleaner:
- Creates backups in `PDF_Backups/` before any modifications
- Uses pikepdf for robust repair operations
- Falls back to PyPDF2 if pikepdf fails
- Removes encryption and normalizes content streams
- Generates detailed logs in `pdf_cleaning.log`
- Moves unfixable files to `PDF_Errors/`

### 3. Processing Papers

**Build Indices and Merge:**
```bash
python processing/index_builder.py
```

Features:
- Groups papers by type (P2, P4, P6) and document type (MS, QP)
- Merges PDFs using Ghostscript for optimal compression
- Generates index files with exam names and page numbers
- Handles specimen papers separately

**Output Structure:**
```
Release/
├── Paper_2/
│   ├── MS/
│   │   ├── Combined_MS_Paper_2.pdf
│   │   └── INDEX_MS.txt
│   └── QP/
│       ├── Combined_QP_Paper_2.pdf
│       └── INDEX_QP.txt
├── Paper_4/
└── Paper_6/
```

**Combine Index with Content:**
```bash
python processing/index_mixer.py
```
- Merges index PDFs with content PDFs
- Attempts Adobe Acrobat integration first
- Falls back to PyPDF2 for cross-platform compatibility
- Maintains proper page ordering

**Add Page Numbers:**
```bash
python processing/page_numbering.py
```

Customization:
```python
add_centered_page_numbers(
    input_pdf,
    output_pdf,
    start_from_page=3,   # First page to number (default: 3)
    start_number=1       # Starting number (default: 1)
)
```

## 📂 Output Structure

### After Download
```
Cambridge_Past_Papers_0971/
├── 2025/
│   └── June/
│       ├── MS/
│       │   ├── 0971_s25_ms_21.pdf
│       │   ├── 0971_s25_ms_22.pdf
│       │   └── ...
│       └── QP/
│           ├── 0971_s25_qp_21.pdf
│           └── ...
├── 2024/
│   ├── June/
│   │   ├── MS/
│   │   └── QP/
│   └── November/
│       ├── MS/
│       └── QP/
└── ...
```

### After Processing
```
Release/
├── Paper_2/
│   ├── MS/
│   │   ├── Combined_MS_Paper_2.pdf      # All MS merged
│   │   └── INDEX_MS.txt                 # Page mappings
│   └── QP/
│       ├── Combined_QP_Paper_2.pdf      # All QP merged
│       └── INDEX_QP.txt
├── Paper_4/
│   ├── MS/
│   └── QP/
└── Paper_6/
    ├── MS/
    └── QP/
```

### After Numbering
```
Numbered_PDF/
├── Paper_2/
│   ├── Paper_2_MS_Numbered.pdf
│   └── Paper_2_QP_Numbered.pdf
├── Paper_4/
└── Paper_6/
```

## 📋 Requirements

### Python Packages
```
requests>=2.31.0      # HTTP requests for downloading
PyPDF2>=3.0.0         # PDF manipulation
pikepdf>=8.0.0        # Advanced PDF operations
reportlab>=4.0.0      # PDF generation (for page numbers)
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

### External Dependencies
- **Ghostscript** - Required for `index_builder.py` PDF merging
  - Windows: Download from [ghostscript.com](https://www.ghostscript.com/)
  - Linux: `sudo apt-get install ghostscript`
  - macOS: `brew install ghostscript`
  
- **Adobe Acrobat** (optional) - Enhanced PDF operations in `index_mixer.py`
  - Falls back to PyPDF2 if not available

## ⚙️ Configuration Examples

### Custom Subject Download

Edit `download_enhanced.py`:
```python
SUBJECT = "0580"  # Mathematics
PAPERS = ["11", "12", "21", "22", "31", "32", "41", "42"]
BASE_URL = "your_download_source_url"
```

### Adjust Page Numbering

Edit `page_numbering.py`:
```python
# Start numbering from page 1 instead of page 3
add_centered_page_numbers(
    input_pdf,
    output_pdf,
    start_from_page=1,   # Start from first page
    start_number=5       # Begin numbering at 5
)
```

### Change Paper Groupings

Edit `index_builder.py`:
```python
PAPER_GROUPS = {
    "2": ["21", "22", "23"],      # Paper 2 variants
    "4": ["41", "42", "43"],      # Paper 4 variants
    "6": ["61", "62", "63"],      # Paper 6 variants
}
```

## 🔍 Error Handling

The toolkit includes comprehensive error handling:

| Component | Error Handling |
|-----------|----------------|
| **Downloads** | Logged with status codes, skips to next file, retries on timeout |
| **Corrupted PDFs** | Quarantined to `DAMAGED_FILES/` or `PDF_Errors/` folders |
| **Missing Ghostscript** | Clear error message with installation instructions |
| **Merge failures** | Fallback strategies and detailed error logs |
| **File access** | Permission checks and alternative path suggestions |

## 🛠️ Troubleshooting

| Issue | Solution | Command |
|-------|----------|---------|
| `Ghostscript not found` | Install Ghostscript and add to system PATH | See installation section |
| `PDF appears corrupted` | Run the PDF cleaner on affected directory | `python validation/pdf_cleaner.py` |
| Download failures | Check internet connection, verify source URLs still valid | Check `HEALTH_CHECK_REPORT.txt` |
| Memory errors during merge | Process fewer papers at once, increase available RAM | Split processing by year |
| Permission errors | Run with appropriate permissions or change output directory | Use `sudo` on Linux/macOS |
| Missing dependencies | Install required packages | `pip install -r requirements.txt` |

### Common Issues

**"Module not found" error:**
```bash
pip install -r requirements.txt
```

**Ghostscript not detected:**
- Verify installation: `gs --version` (Linux/macOS) or `gswin64c --version` (Windows)
- Add to PATH if installed but not detected

**Download returns 404:**
- URLs may have changed on source websites
- Update `BASE_URL` in download scripts
- Check if papers are still available

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- ✨ Support for additional Cambridge subjects (0580, 0455, etc.)
- 🌐 Alternative download sources for redundancy
- 🔧 Enhanced error recovery mechanisms
- ⚡ Performance optimizations for large-scale operations
- 🧪 Unit tests and integration tests
- 🌍 Cross-platform testing (Windows, Linux, macOS)

**How to contribute:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please open an issue first to discuss proposed changes.

## 📄 License

MIT License - See LICENSE file for details.

**Important:** This project is for educational and archival purposes only. Users must comply with:
- Cambridge Assessment International Education's terms of service
- Copyright laws and regulations
- Fair use guidelines
- Local educational policies

The toolkit downloads publicly available past papers. Ensure you have the right to access and use these materials according to your institution's policies.

## 🙏 Acknowledgments

- **Paper Sources:** [PapaCambridge](https://papacambridge.com/), [Physics & Maths Tutor](https://www.physicsandmathstutor.com/)
- **Built With:** [PyPDF2](https://github.com/py-pdf/pypdf), [pikepdf](https://github.com/pikepdf/pikepdf), [ReportLab](https://www.reportlab.com/)
- **Inspired By:** The need for organized, accessible examination resources for students

## 📞 Support

- **Found this helpful?** Give it a ⭐️ on GitHub!
- **Issues or questions?** Open an issue on the GitHub repository
- **Want to discuss?** Start a discussion in the Discussions tab

## 📊 Statistics

Typical performance metrics:
- Download speed: ~2-5 papers per minute (with rate limiting)
- Validation: ~100 PDFs per minute
- Merge time: ~1 minute per 50 papers (depends on file sizes)
- Success rate: 95%+ with proper internet connection

## 🗺️ Roadmap

- [ ] GUI interface for easier operation
- [ ] Batch processing multiple subjects
- [ ] Automatic update checker for new papers
- [ ] PDF compression options
- [ ] OCR integration for text extraction
- [ ] Web interface for remote access
- [ ] Docker containerization

---

**Disclaimer:** This toolkit downloads publicly available past papers. Ensure you have the right to access and use these materials. Always respect copyright laws and Cambridge's terms of service. This project is not affiliated with Cambridge Assessment International Education.
