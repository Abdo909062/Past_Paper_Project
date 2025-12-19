# Cambridge IGCSE Past Papers Toolkit For ```UWC-2025-KD9F7XQ2```

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

A comprehensive Python toolkit for downloading, organizing, validating, and processing Cambridge IGCSE examination papers. Automates the entire workflow from download to final indexed PDFs with page numbers.

## Features

- 🔽 **Automated Downloads** - Fetch papers from multiple sources with built-in retry logic
- ✅ **PDF Validation** - Comprehensive health checks for file integrity
- 🔧 **Corruption Repair** - Fix damaged PDFs using multiple repair strategies
- 📑 **Smart Indexing** - Generate detailed indices with automatic page mapping
- 🔢 **Page Numbering** - Add centered page numbers to merged documents
- 📊 **Detailed Reporting** - Track success rates and identify issues

## Quick Start

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
# 1. Download papers
python download/download_2.py

# 2. Validate downloads
python validation/health_checker.py

# 3. Build merged PDFs with indices
python processing/index.py

# 4. Add page numbers
python processing/numbering.py
```

## Project Structure

```
cambridge-papers-toolkit/
│
├── .gitignore
├── project_key.txt              # Contains the project ownership key: UWC-2025-KD9F7XQ2
├── PROJECT_STRUCTURE.md         # Documentation of the project structure
├── requirements.txt             # Python dependencies
└── README.md                    # Project description and usage instructions [ This File ]
│
├── download/                    # Exam download scripts
│   ├── Download.py              # Basic downloader for subjects
│   ├── download_chemistry_0620.py  # Specialized downloader for Chemistry 0620
│   └── url_generator.py         # Generates URLs and organizes them into CSV
│
├── processing/                  # PDF processing and merging
│   ├── index_builder.py         # Build indices and merge exam papers
│   ├── index_mixer.py           # Combine index with content PDFs
│   └── page_numbering.py        # Add page numbers to documents
│
└── validation/                  # PDF integrity and validation tools
    ├── health_checker.py        # Scan and validate PDF files
    └── pdf_cleaner.py           # Repair corrupted PDF files
```

## Detailed Usage

### Downloading Papers

The toolkit supports multiple subjects and sources:

**Subject 0971 (Computer Science)**
```bash
python download/download_2.py
```
- Downloads from papacambridge.com
- Covers 2018-2025 (June and November sessions)
- Organizes into `Year/Season/MS|QP/` structure

**Subject 0620 (Chemistry)**
```bash
python download/0620_paper.py
```
- Downloads from physicsandmathstutor.com
- Includes all paper variants (v1, v2, v3)
- Handles specimen papers automatically

**Configuration**

Edit the script to customize:
```python
subject = "0971"                    # Change subject code
papers = ["21", "22", "41", "42"]  # Select paper numbers
DELAY_BETWEEN_DOWNLOADS = 2         # Adjust rate limiting (seconds)
```

### Validating PDFs

**Run Health Check**
```bash
python validation/health_checker.py
```

The validator performs:
- File size verification (rejects files < 1KB)
- PDF header validation
- Page count analysis
- Read integrity testing

Damaged files are automatically moved to `DAMAGED_FILES/` directory.

**Repair Corrupted Files**
```bash
python validation/cleaner.py
```

The cleaner:
- Creates backups before any modifications
- Uses pikepdf for robust repair operations
- Falls back to PyPDF2 if needed
- Generates detailed logs (`pdf_cleaning.log`)

### Processing Papers

**Build Indices and Merge**
```bash
python processing/index.py
```

Creates merged PDFs organized by:
- Paper type (P2, P4, P6)
- Document type (MS, QP)

Output includes:
- `Combined_{MS|QP}_Paper_{2|4|6}.pdf` - Merged examination papers
- `INDEX_{MS|QP}.txt` - Detailed index with exam names and page numbers

**Combine Index with Content**
```bash
python processing/mixing-index.py
```

Merges index PDFs with content PDFs. Attempts Adobe Acrobat integration first, falls back to PyPDF2 for compatibility.

**Add Page Numbers**
```bash
python processing/numbering.py
```

Adds centered page numbers starting from page 3 (configurable):
```python
start_from_page=3    # First page to number
start_number=1       # Number to display
```

## Output Structure

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
└── 2024/
    ├── June/
    └── November/
```

### After Processing
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

## Requirements

### Python Packages
```
requests>=2.31.0
PyPDF2>=3.0.0
pikepdf>=8.0.0
reportlab>=4.0.0
```

### External Dependencies
- **Ghostscript** - Required for `index.py` PDF merging operations
- **Adobe Acrobat** (optional) - Enhanced PDF operations in `mixing-index.py`

## Configuration Examples

### Custom Subject Download
```python
# In download_2.py
subject = "0580"  # Mathematics
papers = ["11", "12", "21", "22", "31", "32", "41", "42"]
```

### Adjust Page Numbering
```python
# In numbering.py
add_centered_page_numbers(
    input_pdf,
    output_pdf,
    start_from_page=1,   # Start from first page
    start_number=5       # Begin numbering at 5
)
```

## Error Handling

The toolkit includes comprehensive error handling:
- **Download failures** - Logged with status codes, skips to next file
- **Corrupted PDFs** - Quarantined to `DAMAGED_FILES/` or `PDF_Errors/`
- **Missing Ghostscript** - Clear error message with installation instructions
- **Merge failures** - Fallback strategies and detailed error logs

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Ghostscript not found` | Install Ghostscript and add to system PATH |
| `PDF appears corrupted` | Run `cleaner.py` on the affected directory |
| Download failures | Check internet connection, verify source URLs |
| Memory errors | Process fewer papers at once, increase available RAM |
| Permission errors | Run with appropriate permissions or change output directory |

## Contributing

Contributions are welcome! Areas for improvement:
- Support for additional subjects
- Alternative download sources
- Enhanced error recovery mechanisms
- Performance optimizations for large-scale operations
- Cross-platform testing

Please open an issue first to discuss proposed changes.

## License

MIT License - See LICENSE file for details.

This project is for educational and archival purposes only. Users must comply with Cambridge Assessment International Education's terms of service and copyright policies.

## Acknowledgments

- Paper sources: [PapaCambridge](https://papacambridge.com/), [Physics & Maths Tutor](https://www.physicsandmathstutor.com/)
- Built with [PyPDF2](https://github.com/py-pdf/pypdf), [pikepdf](https://github.com/pikepdf/pikepdf), and [ReportLab](https://www.reportlab.com/)
- Inspired by the need for organized, accessible examination resources

## Support

Found this helpful? Give it a ⭐️ on GitHub!

For issues or questions, please open an issue on the GitHub repository.


```UWC-2025-KD9F7XQ2``` | Built with ❤️ for IGCSE students worldwide

---

**Note**: This toolkit downloads publicly available past papers. Ensure you have the right to access and use these materials according to your institution's policies and Cambridge's terms of service.
