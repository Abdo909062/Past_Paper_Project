# Cambridge Past Papers Toolkit - Complete Project Structure

## Repository Organization

```
cambridge-papers-toolkit/
│
├── download/                           # Paper download scripts
│   ├── download.py                    # Basic downloader for subject 0971
│   ├── download_enhanced.py           # Enhanced with MS/QP organization
│   ├── download_chemistry_0620.py     # Chemistry specialized downloader
│   └── url_generator.py               # URL list generator and CSV exporter
│
├── validation/                         # PDF integrity and repair tools
│   ├── health_checker.py              # Scan and validate PDF integrity
│   └── pdf_cleaner.py                 # Repair corrupted PDFs
│
├── processing/                         # PDF processing and merging
│   ├── index_builder.py               # Build indices and merge papers
│   ├── index_mixer.py                 # Combine index with content PDFs
│   └── page_numbering.py              # Add page numbers to documents
│
├── requirements.txt                    # Python package dependencies
├── .gitignore                         # Git ignore patterns
├── README.md                          # Main documentation
└── PROJECT_STRUCTURE.md               # This file
```

## File Descriptions

### Download Module (`download/`)

#### `download.py`
- **Purpose**: Basic downloader for Cambridge subject 0971 (Computer Science)
- **Source**: papacambridge.com
- **Features**: 
  - Downloads Mark Schemes (MS) and Question Papers (QP)
  - Covers years 2018-2025
  - Organized by Year/Season structure
- **Usage**: `python download/download.py`

#### `download_enhanced.py`
- **Purpose**: Enhanced version with separated MS/QP folders
- **Features**:
  - Same as download.py but with better organization
  - Creates Year/Season/MS|QP/ structure
  - More detailed progress reporting
- **Usage**: `python download/download_enhanced.py`

#### `download_chemistry_0620.py`
- **Purpose**: Specialized downloader for Chemistry (0620)
- **Source**: physicsandmathstutor.com
- **Features**:
  - Handles multiple paper variants (v1, v2, v3)
  - Includes specimen papers
  - Built-in PDF validation during download
  - Rate limiting and health checks
- **Usage**: `python download/download_chemistry_0620.py`

#### `url_generator.py`
- **Purpose**: Generate complete URL lists
- **Features**:
  - Creates comprehensive URL lists for all papers
  - Exports to CSV format
  - Useful for batch operations and audit trails
- **Output**: `cambridge_past_papers_urls.csv`
- **Usage**: `python download/url_generator.py`

### Validation Module (`validation/`)

#### `health_checker.py`
- **Purpose**: Comprehensive PDF integrity checker
- **Features**:
  - File size validation (rejects < 1KB)
  - PDF header verification
  - Page count analysis
  - Read integrity testing
  - Automatic quarantine of damaged files
  - Detailed health reports
- **Output**: 
  - Moves damaged files to `DAMAGED_FILES/`
  - Generates `HEALTH_CHECK_REPORT.txt`
- **Usage**: `python validation/health_checker.py`

#### `pdf_cleaner.py`
- **Purpose**: Repair and clean corrupted PDFs
- **Features**:
  - Uses pikepdf for robust repairs
  - Falls back to PyPDF2 if needed
  - Creates backups before modification
  - Removes encryption and normalizes content
  - Detailed logging to `pdf_cleaning.log`
- **Output**:
  - Backups saved to `PDF_Backups/`
  - Unfixable files moved to `PDF_Errors/`
- **Usage**: `python validation/pdf_cleaner.py`

### Processing Module (`processing/`)

#### `index_builder.py`
- **Purpose**: Build indices and merge papers
- **Features**:
  - Groups papers by type (P2, P4, P6)
  - Merges PDFs using Ghostscript
  - Generates index files with page mappings
  - Handles specimen papers separately
- **Requirements**: Ghostscript must be installed
- **Output**:
  - `Combined_{MS|QP}_Paper_{2|4|6}.pdf`
  - `INDEX_{MS|QP}.txt`
- **Usage**: `python processing/index_builder.py`

#### `index_mixer.py`
- **Purpose**: Combine index PDFs with content PDFs
- **Features**:
  - Attempts Adobe Acrobat integration first
  - Falls back to PyPDF2 for compatibility
  - Maintains proper page ordering
- **Input**: Separate index and content PDFs
- **Output**: `Paper_{X}_{MS|QP}_Merged.pdf`
- **Usage**: `python processing/index_mixer.py`

#### `page_numbering.py`
- **Purpose**: Add centered page numbers to merged PDFs
- **Features**:
  - Configurable start page (default: page 3)
  - Configurable start number (default: 1)
  - Centers numbers at bottom of pages
  - Preserves original PDF quality
- **Output**: `Paper_{X}_{MS|QP}_Numbered.pdf`
- **Usage**: `python processing/page_numbering.py`

## Standard Workflow

### Complete Pipeline

```bash
# Step 1: Download papers
python download/download_enhanced.py

# Step 2: Validate downloads
python validation/health_checker.py

# Step 3: Repair issues (if any found)
python validation/pdf_cleaner.py

# Step 4: Build indices and merge
python processing/index_builder.py

# Step 5: Combine with indices
python processing/index_mixer.py

# Step 6: Add page numbers
python processing/page_numbering.py
```

### Quick Start for New Subject

1. Edit download script configuration:
   ```python
   SUBJECT = "YOUR_SUBJECT_CODE"
   PAPERS = ["11", "12", "21", "22", ...]
   ```

2. Run the pipeline above

3. Find output in respective directories

## Configuration Options

### Download Scripts
- `SUBJECT`: Subject code (e.g., "0971", "0620")
- `PAPERS`: List of paper numbers to download
- `DELAY_BETWEEN_DOWNLOADS`: Rate limiting in seconds
- `BASE_URL`: Source URL for downloads

### Processing Scripts
- `start_from_page`: First page to add numbers (in page_numbering.py)
- `start_number`: Starting number for pagination
- `PARENT_FOLDER`: Input directory for processing
- `OUTPUT_DIR` / `RELEASE_FOLDER`: Output destinations

## Output Directories

### After Download
```
Cambridge_Past_Papers_0971/
├── 2025/June/MS/
├── 2025/June/QP/
├── 2024/June/MS/
├── 2024/June/QP/
├── 2024/November/MS/
└── 2024/November/QP/
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

### After Numbering
```
Numbered_PDF/
├── Paper_2/
│   ├── Paper_2_MS_Numbered.pdf
│   └── Paper_2_QP_Numbered.pdf
├── Paper_4/
└── Paper_6/
```

## Dependencies

### Python Packages (requirements.txt)
- `requests>=2.31.0` - HTTP requests for downloading
- `PyPDF2>=3.0.0` - PDF manipulation
- `pikepdf>=8.0.0` - Advanced PDF operations
- `reportlab>=4.0.0` - PDF generation (for page numbers)

### External Tools
- **Ghostscript** - Required for index_builder.py
  - Windows: Download from ghostscript.com
  - Linux: `sudo apt-get install ghostscript`
  - macOS: `brew install ghostscript`
- **Adobe Acrobat** (optional) - Enhanced operations in index_mixer.py

## Error Handling

Each script includes comprehensive error handling:
- Download failures: Logged with status codes, continues to next file
- Corrupted PDFs: Quarantined to designated folders
- Missing dependencies: Clear error messages with installation instructions
- Processing failures: Detailed logs and fallback strategies

## Best Practices

1. **Always validate after downloading**: Run health_checker.py
2. **Create backups**: pdf_cleaner.py does this automatically
3. **Check Ghostscript installation**: Required for merging
4. **Monitor disk space**: Combined PDFs can be large
5. **Review logs**: Check pdf_cleaning.log for issues
6. **Test on small sets first**: Before processing entire collections

## Troubleshooting

| Issue | Solution | Related File |
|-------|----------|-------------|
| Download failures | Check internet, verify URLs | download/*.py |
| Corrupted PDFs | Run pdf_cleaner.py | validation/pdf_cleaner.py |
| Ghostscript not found | Install and add to PATH | processing/index_builder.py |
| Memory errors | Process fewer files at once | processing/*.py |
| Missing files | Check DAMAGED_FILES folder | validation/health_checker.py |

## Extending the Toolkit

### Adding New Subjects
1. Create new download script based on existing templates
2. Update configuration variables
3. Test with small date range first
4. Run full pipeline

### Custom Processing
- Modify `PAPER_GROUPS` in index_builder.py for different paper structures
- Adjust `start_from_page` in page_numbering.py for different layouts
- Create custom merge strategies by extending index_mixer.py

## Version Control

Files tracked by Git:
- All `.py` scripts
- `requirements.txt`
- `.gitignore`
- Documentation files

Files ignored by Git (see `.gitignore`):
- Downloaded PDFs
- Backup directories
- Log files
- Temporary files
- Virtual environments

## License & Legal

This toolkit is for educational and archival purposes. Users must:
- Comply with Cambridge Assessment International Education's terms
- Respect copyright laws
- Use papers ethically and legally
- Verify rights to access materials

## Support & Contributing

- Report issues via GitHub issues
- Suggest improvements through pull requests
- Focus areas: additional subjects, alternative sources, performance
- Follow existing code style and documentation standards