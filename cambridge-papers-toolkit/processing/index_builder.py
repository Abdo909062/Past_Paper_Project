"""
PDF Index Builder and Merger
Builds comprehensive indices for all papers and merges them using Ghostscript
Generates index files with exam labels and page mappings
"""

import os
import subprocess
from pathlib import Path
import PyPDF2

# Configuration
PARENT_FOLDER = "Cambridge_Past_Papers_0620"
SPECIMEN_FOLDER = os.path.join(PARENT_FOLDER, "Specimen")
RELEASE_FOLDER = "Release"

PAPER_GROUPS = {
    "2": ["21", "22", "23"],
    "4": ["41", "42", "43"],
    "6": ["61", "62", "63"],
}

EXAM_MAPPINGS = {
    "June": "June",
    "March": "March",
    "November": "Nov."
}


def setup_release_folder():
    """Create Release folder structure."""
    Path(RELEASE_FOLDER).mkdir(exist_ok=True)
    
    for paper in ["2", "4", "6"]:
        for doc_type in ["MS", "QP"]:
            folder_path = os.path.join(RELEASE_FOLDER, f"Paper_{paper}", doc_type)
            Path(folder_path).mkdir(parents=True, exist_ok=True)
    
    print(f"✓ Release folder structure created\n")


def find_ghostscript():
    """
    Find Ghostscript executable.
    
    Returns:
        str: Path to Ghostscript executable or None
    """
    gs_paths = [
        'gs',
        'gswin64c.exe',
        'gswin32c.exe',
        r'C:\Program Files\gs\gs10.01.2\bin\gswin64c.exe',
        r'C:\Program Files (x86)\gs\gs10.01.2\bin\gswin32c.exe',
    ]
    
    for gs_path in gs_paths:
        try:
            result = subprocess.run([gs_path, '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✓ Ghostscript found: {result.stdout.strip()}\n")
                return gs_path
        except:
            pass
    
    return None


def check_pdf_integrity(file_path):
    """
    Check if PDF is valid.
    
    Args:
        file_path (str): Path to PDF file
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    try:
        with open(file_path, 'rb') as f:
            f.seek(0, 2)
            file_size = f.tell()
            if file_size < 1000:
                return False, "File too small"
            
            f.seek(0)
            pdf_reader = PyPDF2.PdfReader(f)
            num_pages = len(pdf_reader.pages)
            if num_pages == 0:
                return False, "No pages"
            
            try:
                _ = pdf_reader.pages[0]
            except:
                return False, "Cannot read pages"
            
            return True, f"OK ({num_pages} pages)"
    except Exception as e:
        return False, str(e)[:40]


def get_pdf_page_count(file_path):
    """
    Get page count.
    
    Args:
        file_path (str): Path to PDF file
        
    Returns:
        int: Number of pages
    """
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            return len(pdf_reader.pages)
    except:
        return 0


def get_specimen_file(paper_num, doc_type):
    """
    Get specimen file.
    
    Args:
        paper_num (str): Paper number
        doc_type (str): Document type (MS/QP)
        
    Returns:
        str: Path to specimen file or None
    """
    folder_path = os.path.join(SPECIMEN_FOLDER, doc_type)
    if not os.path.exists(folder_path):
        return None
    
    files = os.listdir(folder_path)
    for file in files:
        if f"paper-{paper_num}" in file.lower():
            return os.path.join(folder_path, file)
    return None


def build_index_for_paper(paper, doc_type):
    """
    Build index for a specific paper and document type.
    
    Args:
        paper (str): Paper number
        doc_type (str): Document type (MS/QP)
        
    Returns:
        tuple: (index_data, valid_files, invalid_files)
    """
    index_data = []
    valid_files = []
    invalid_files = []
    
    specimen_file = get_specimen_file(paper, doc_type)
    if specimen_file:
        is_valid, msg = check_pdf_integrity(specimen_file)
        if is_valid:
            page_count = get_pdf_page_count(specimen_file)
            if page_count > 0:
                index_data.append({
                    'year': 2000,
                    'season': 'Specimen',
                    'label': f"Specimen - {paper}",
                    'pages': page_count,
                    'path': specimen_file,
                    'is_specimen': True
                })
                valid_files.append(specimen_file)
        else:
            invalid_files.append((specimen_file, msg))
    
    for root, dirs, files in os.walk(PARENT_FOLDER):
        if "DAMAGED_FILES" in root or "Specimen" in root:
            continue
        
        path_parts = root.split(os.sep)
        if len(path_parts) >= 3:
            year_str = path_parts[-2]
            season_str = path_parts[-1]
            
            try:
                year = int(year_str)
                if season_str in ["June", "November"]:
                    doc_folder = os.path.join(root, doc_type)
                    if os.path.exists(doc_folder):
                        doc_files = os.listdir(doc_folder)
                        for sub_paper in PAPER_GROUPS[paper]:
                            matching_files = [f for f in doc_files if f"_{sub_paper}.pdf" in f]
                            if matching_files:
                                pdf_path = os.path.join(doc_folder, matching_files[0])
                                is_valid, msg = check_pdf_integrity(pdf_path)
                                
                                if is_valid:
                                    page_count = get_pdf_page_count(pdf_path)
                                    if page_count > 0:
                                        exam_label = f"{EXAM_MAPPINGS[season_str]} {year} - {sub_paper}"
                                        index_data.append({
                                            'year': year,
                                            'season': season_str,
                                            'label': exam_label,
                                            'pages': page_count,
                                            'path': pdf_path,
                                            'is_specimen': False
                                        })
                                        valid_files.append(pdf_path)
                                else:
                                    invalid_files.append((pdf_path, msg))
            except:
                pass
    
    index_data.sort(key=lambda x: (not x['is_specimen'], x['year'], 0 if x['season'] == 'June' else 1))
    
    return index_data, valid_files, invalid_files


def merge_pdfs_ghostscript(pdf_files, output_file, gs_path):
    """
    Merge PDFs using Ghostscript.
    
    Args:
        pdf_files (list): List of PDF files to merge
        output_file (str): Output file path
        gs_path (str): Path to Ghostscript executable
        
    Returns:
        bool: Success status
    """
    try:
        cmd = [
            gs_path,
            '-q',
            '-dNOPAUSE',
            '-dBATCH',
            '-dSAFER',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/ebook',
            f'-sOutputFile={output_file}'
        ] + pdf_files
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False


def create_merged_pdf(index_data, valid_files, gs_path, output_file):
    """
    Create merged PDF.
    
    Args:
        index_data (list): Index data
        valid_files (list): List of valid PDF files
        gs_path (str): Path to Ghostscript
        output_file (str): Output file path
        
    Returns:
        list: Index entries or None
    """
    if len(valid_files) == 0:
        return None
    
    success = merge_pdfs_ghostscript(valid_files, output_file, gs_path)
    
    if success:
        is_valid, msg = check_pdf_integrity(output_file)
        if is_valid:
            current_page = 1
            index_entries = []
            for entry in index_data:
                if entry['path'] in valid_files:
                    index_entries.append({
                        'no': len(index_entries) + 1,
                        'exam': entry['label'],
                        'start_page': current_page,
                        'pages': entry['pages']
                    })
                    current_page += entry['pages']
            
            return index_entries
    
    return None


def save_index(index_entries, output_file):
    """
    Save index to file.
    
    Args:
        index_entries (list): Index entries
        output_file (str): Output file path
    """
    if not index_entries:
        return
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for entry in index_entries:
                f.write(str(entry['no']) + "\n")
            
            f.write("\n" + "=" * 70 + "\n\n")
            
            for entry in index_entries:
                f.write(entry['exam'] + "\n")
            
            f.write("\n" + "=" * 70 + "\n\n")
            
            for entry in index_entries:
                f.write(str(entry['start_page']) + "\n")
    except:
        pass


def process_all():
    """Process all papers and document types."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "AUTOMATED PDF MERGER - ALL PAPERS" + " " * 20 + "║")
    print("╚" + "=" * 68 + "╝\n")
    
    setup_release_folder()
    
    gs_path = find_ghostscript()
    if not gs_path:
        print("✗ Ghostscript not found! Please install it first.")
        return
    
    for paper in ["2", "4", "6"]:
        print(f"\n{'=' * 70}")
        print(f"Processing Paper {paper}")
        print(f"{'=' * 70}\n")
        
        for doc_type in ["MS", "QP"]:
            print(f"Building {doc_type} for Paper {paper}...")
            
            index_data, valid_files, invalid_files = build_index_for_paper(paper, doc_type)
            
            if len(valid_files) == 0:
                print(f"  ✗ No valid files found for Paper {paper} ({doc_type})")
                continue
            
            print(f"  ✓ Found {len(valid_files)} valid files")
            
            output_pdf = os.path.join(RELEASE_FOLDER, f"Paper_{paper}", doc_type, f"Combined_{doc_type}_Paper_{paper}.pdf")
            index_file = os.path.join(RELEASE_FOLDER, f"Paper_{paper}", doc_type, f"INDEX_{doc_type}.txt")
            
            print(f"  Merging PDFs...")
            index_entries = create_merged_pdf(index_data, valid_files, gs_path, output_pdf)
            
            if index_entries:
                print(f"  ✓ Created: {os.path.basename(output_pdf)}")
                save_index(index_entries, index_file)
                print(f"  ✓ Created: {os.path.basename(index_file)}")
            else:
                print(f"  ✗ Failed to create merged PDF")
    
    print(f"\n{'=' * 70}")
    print("COMPLETE!")
    print(f"{'=' * 70}")
    print(f"\n✓ All files organized in: {RELEASE_FOLDER}/")
    print("\nStructure:")
    print("Release/")
    print("├── Paper_2/")
    print("│   ├── MS/")
    print("│   │   ├── Combined_MS_Paper_2.pdf")
    print("│   │   └── INDEX_MS.txt")
    print("│   └── QP/")
    print("│       ├── Combined_QP_Paper_2.pdf")
    print("│       └── INDEX_QP.txt")
    print("├── Paper_4/")
    print("│   ├── MS/")
    print("│   └── QP/")
    print("└── Paper_6/")
    print("    ├── MS/")
    print("    └── QP/")
    print()


if __name__ == "__main__":
    process_all()